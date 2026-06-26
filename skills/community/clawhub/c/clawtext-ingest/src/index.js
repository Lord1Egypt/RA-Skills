import fs from 'fs/promises';
import fssync from 'fs';
import path from 'path';
import crypto from 'crypto';
import { glob } from 'glob';

/**
 * ClawText Ingestion Engine
 * Multi-source data ingestion with automatic metadata generation
 */

export class ClawTextIngest {
  constructor(memoryDir = null, hashFile = null) {
    this.memoryDir = memoryDir || path.join(process.env.HOME, '.openclaw/workspace/memory');
    this.hashFile = hashFile || path.join(this.memoryDir, '.ingest_hashes.json');
    this.importedCount = 0;
    this.skippedCount = 0;
    this.errors = [];
    this.hashes = this.loadHashes();
  }

  /**
   * Load existing content hashes to enable deduplication
   */
  loadHashes() {
    try {
      if (fssync.existsSync(this.hashFile)) {
        return JSON.parse(fssync.readFileSync(this.hashFile, 'utf-8'));
      }
    } catch (err) {
      console.warn('Failed to load hashes:', err.message);
    }
    return {};
  }

  /**
   * Save content hashes to file
   */
  saveHashes() {
    try {
      fssync.mkdirSync(this.memoryDir, { recursive: true });
      fssync.writeFileSync(this.hashFile, JSON.stringify(this.hashes, null, 2));
    } catch (err) {
      console.error('Failed to save hashes:', err.message);
    }
  }

  /**
   * Check if content already ingested (by SHA1 hash)
   */
  isDuplicate(content) {
    const hash = crypto.createHash('sha1').update(content).digest('hex');
    return { isDup: this.hashes[hash] !== undefined, hash };
  }

  /**
   * Generate YAML frontmatter from source metadata
   */
  generateFrontmatter(metadata = {}) {
    const {
      date = new Date().toISOString().split('T')[0],
      type = 'fact',
      project = null,
      entities = [],
      source = null,
      keywords = []
    } = metadata;

    const frontmatter = {
      date,
      project: project || 'ingestion',
      type,
      entities: Array.isArray(entities) ? entities : [entities].filter(Boolean),
      keywords: Array.isArray(keywords) ? keywords : [keywords].filter(Boolean)
    };

    if (source) frontmatter.source = source;

    const yaml = Object.entries(frontmatter)
      .map(([k, v]) => {
        if (Array.isArray(v)) return `${k}: [${v.map(x => `"${x}"`).join(', ')}]`;
        return `${k}: ${v}`;
      })
      .join('\n');

    return `---\n${yaml}\n---\n`;
  }

  /**
   * Ingest from file glob patterns with deduplication
   */
  async fromFiles(patterns, metadata = {}, options = {}) {
    const patterns_ = Array.isArray(patterns) ? patterns : [patterns];
    const { checkDedupe = true } = options;
    let imported = 0;

    for (const pattern of patterns_) {
      const files = await glob(pattern, { absolute: true });
      
      for (const file of files) {
        try {
          const content = await fs.readFile(file, 'utf-8');
          
          if (checkDedupe) {
            const { isDup, hash } = this.isDuplicate(content);
            if (isDup) {
              this.skippedCount++;
              continue;
            }
          }

          const fileName = path.basename(file);
          const sourceDate = metadata.date || new Date().toISOString().split('T')[0];
          
          const memory = this.generateFrontmatter({
            ...metadata,
            date: sourceDate,
            source: `file:${file}`
          }) + content;

          const outFile = path.join(this.memoryDir, `ingested-files-${sourceDate}.md`);
          await fs.appendFile(outFile, `\n## ${fileName}\n\n${memory}\n\n---\n\n`);
          
          const { hash } = this.isDuplicate(content);
          this.hashes[hash] = { file, date: sourceDate };
          imported++;
        } catch (err) {
          this.errors.push({ file, error: err.message });
        }
      }
    }

    this.importedCount += imported;
    return { imported, skipped: this.skippedCount, errors: this.errors };
  }

  /**
   * Ingest from URLs (requires web_fetch capability)
   */
  async fromUrls(urls, metadata = {}) {
    const urls_ = Array.isArray(urls) ? urls : [urls];
    let imported = 0;

    for (const url of urls_) {
      try {
        // Use OpenClaw's web_fetch capability if available
        const response = await fetch(url);
        const content = await response.text();
        
        const memory = this.generateFrontmatter({
          ...metadata,
          source: `url:${url}`
        }) + `\n${content}\n`;

        const outFile = path.join(this.memoryDir, `ingested-web-${new Date().toISOString().split('T')[0]}.md`);
        await fs.appendFile(outFile, `\n## ${url}\n\n${memory}\n\n---\n\n`);
        
        imported++;
      } catch (err) {
        this.errors.push({ url, error: err.message });
      }
    }

    this.importedCount += imported;
    return { imported, errors: this.errors };
  }

  /**
   * Ingest from JSON data with deduplication
   */
  async fromJSON(data, metadata = {}, options = {}) {
    const {
      keyMap = {},
      transform = null
    } = options;

    const items = Array.isArray(data) ? data : [data];
    let imported = 0;

    for (const item of items) {
      try {
        const content = item[keyMap.contentKey] || JSON.stringify(item);
        const { isDup, hash } = this.isDuplicate(content);

        if (isDup) {
          this.skippedCount++;
          continue;
        }

        const itemDate = item[keyMap.dateKey]?.split('T')[0] || metadata.date;
        const author = item[keyMap.authorKey] || 'unknown';

        let memory = content;
        if (transform) memory = await transform(item, memory);

        const entry = this.generateFrontmatter({
          ...metadata,
          date: itemDate,
          entities: [author]
        }) + `\n${memory}\n`;

        const outFile = path.join(this.memoryDir, `ingested-json-${itemDate}.md`);
        await fs.appendFile(outFile, `\n${entry}\n\n---\n\n`);
        
        this.hashes[hash] = { source: 'json', date: itemDate };
        imported++;
      } catch (err) {
        this.errors.push({ item, error: err.message });
      }
    }

    this.importedCount += imported;
    return { imported, skipped: this.skippedCount, errors: this.errors };
  }

  /**
   * Ingest from text (raw or pre-formatted)
   */
  async fromText(text, metadata = {}) {
    try {
      const { isDup, hash } = this.isDuplicate(text);

      if (isDup) {
        this.skippedCount++;
        return { imported: 0, skipped: 1, errors: [] };
      }

      fssync.mkdirSync(this.memoryDir, { recursive: true });
      const memory = this.generateFrontmatter(metadata) + text;
      const fileName = metadata.filename || `ingested-text-${new Date().toISOString().split('T')[0]}.md`;
      const outFile = path.join(this.memoryDir, fileName);
      
      await fs.appendFile(outFile, `\n${memory}\n\n---\n\n`);
      this.hashes[hash] = { type: 'text', date: metadata.date || new Date().toISOString().split('T')[0] };
      this.importedCount += 1;
      return { imported: 1, skipped: 0, errors: [] };
    } catch (err) {
      const error = { text: text.substring(0, 50), error: err.message };
      this.errors.push(error);
      return { imported: 0, skipped: 0, errors: [error] };
    }
  }

  /**
   * Batch ingest from multiple sources with deduplication
   */
  async ingestAll(sources) {
    const results = [];

    for (const source of sources) {
      const { type, data, metadata, options } = source;

      let result;
      switch (type) {
        case 'files':
          result = await this.fromFiles(data, metadata);
          break;
        case 'urls':
          result = await this.fromUrls(data, metadata);
          break;
        case 'json':
          result = await this.fromJSON(data, metadata, options);
          break;
        case 'text':
          result = await this.fromText(data, metadata);
          break;
        default:
          result = { imported: 0, errors: [{ source: type, error: 'Unknown source type' }] };
      }

      results.push({ type, result });
    }

    // Persist all hashes after ingest completes
    this.saveHashes();

    return {
      totalImported: this.importedCount,
      totalSkipped: this.skippedCount,
      results,
      errors: this.errors
    };
  }

  /**
   * Signal ClawText to rebuild clusters
   */
  async rebuildClusters() {
    try {
      const clustersPath = path.join(this.memoryDir, 'clusters');
      // Remove stale clusters to trigger rebuild on next session
      const files = await fs.readdir(clustersPath);
      for (const file of files) {
        await fs.unlink(path.join(clustersPath, file));
      }
      return { success: true, message: 'Clusters marked for rebuild' };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  /**
   * Get ingestion report
   */
  getReport() {
    return {
      totalImported: this.importedCount,
      totalSkipped: this.skippedCount,
      errorCount: this.errors.length,
      errors: this.errors,
      memoryDir: this.memoryDir,
      dedupeHashes: Object.keys(this.hashes).length
    };
  }

  /**
   * Persist hashes to disk after ingest
   */
  async commit() {
    this.saveHashes();
    return this.getReport();
  }
}

export default ClawTextIngest;
