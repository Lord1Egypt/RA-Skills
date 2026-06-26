import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import YAML from 'yaml';

const memoryDir = process.env.MEMORY_DIR || path.join(process.env.HOME, '.openclaw/workspace/memory');

export async function buildEntitiesAndHashes() {
  const files = (await fs.readdir(memoryDir)).filter(f => f.endsWith('.md'));
  const entities = {};
  const hashes = {};

  for (const file of files) {
    try {
      const fp = path.join(memoryDir, file);
      const raw = await fs.readFile(fp, 'utf8');
      // Extract frontmatter if present
      let fm = null;
      let content = raw;
      if (raw.startsWith('---')) {
        const parts = raw.split('---');
        if (parts.length >= 3) {
          fm = YAML.parse(parts[1]);
          content = parts.slice(2).join('---').trim();
        }
      }

      // Hash content for dedupe
      const hash = crypto.createHash('sha1').update(content).digest('hex');
      hashes[file] = hash;

      if (fm && fm.entities) {
        const entList = Array.isArray(fm.entities) ? fm.entities : [fm.entities];
        for (const e of entList) {
          const key = String(e).toLowerCase();
          entities[key] = entities[key] || [];
          entities[key].push({ file, date: fm.date || null, project: fm.project || null, type: fm.type || null });
        }
      }
    } catch (err) {
      console.error('postprocess error', file, err.message);
    }
  }

  await fs.writeFile(path.join(memoryDir, 'entities.json'), JSON.stringify(entities, null, 2));
  await fs.writeFile(path.join(memoryDir, '.ingest_hashes.json'), JSON.stringify(hashes, null, 2));

  return { filesProcessed: files.length, entityCount: Object.keys(entities).length };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  buildEntitiesAndHashes().then(r => console.log('Postprocess complete', r)).catch(e => console.error(e));
}
