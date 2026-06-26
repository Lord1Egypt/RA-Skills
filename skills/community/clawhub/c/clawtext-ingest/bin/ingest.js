#!/usr/bin/env node

/**
 * ClawText-Ingest CLI
 * Command-line tool for multi-source data ingestion
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { ClawTextIngest } from '../src/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Parse command-line arguments
 */
function parseArgs(args) {
  const parsed = { _: [] };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      parsed[key] = value || true;
    } else if (arg.startsWith('-')) {
      parsed[arg.slice(1)] = args[++i];
    } else {
      parsed._.push(arg);
    }
  }

  return parsed;
}

/**
 * Display help message
 */
function showHelp() {
  console.log(`
ClawText-Ingest CLI v1.2.0
Multi-source data ingestion for memory management

USAGE:
  clawtext-ingest [command] [options]

COMMANDS:
  ingest-files    Ingest files matching glob patterns
  ingest-urls     Ingest content from URLs
  ingest-json     Ingest JSON data
  ingest-text     Ingest raw text
  batch           Batch ingest from multiple sources
  rebuild         Rebuild ClawText clusters after ingestion
  status          Show ingestion status
  help            Show this help message

OPTIONS:
  --input, -i          Input data (file, URL, or JSON)
  --type, -t           Input type (files, urls, json, text)
  --output, -o         Output memory directory (default: ~/.openclaw/workspace/memory)
  --project, -p        Project name for metadata
  --source, -s         Source identifier for metadata
  --date, -d           Date for metadata (YYYY-MM-DD)
  --model, -m          Model override for semantic processing (gpt-4o, etc.)
  --no-dedupe          Skip deduplication checks (faster, risky)
  --verbose, -v        Verbose output
  --help, -h           Show this help message

EXAMPLES:

  # Ingest files
  clawtext-ingest ingest-files --input="docs/*.md" --project="myproject"

  # Ingest URLs
  clawtext-ingest ingest-urls --input="https://example.com" --project="research"

  # Ingest JSON from Discord thread
  clawtext-ingest ingest-json --input=thread-messages.json --source="discord" --type="discord-thread"

  # Batch ingest (file + URL)
  clawtext-ingest batch --config=ingest.json

  # Rebuild clusters after ingestion
  clawtext-ingest rebuild

  # Show current ingestion status
  clawtext-ingest status

For full documentation: https://github.com/ragesaq/clawtext-ingest
`);
}

/**
 * Main CLI handler
 */
async function main() {
  const args = process.argv.slice(2);
  const parsed = parseArgs(args);
  const command = parsed._[0] || 'help';

  if (parsed.help || parsed.h || command === 'help') {
    showHelp();
    process.exit(0);
  }

  const memoryDir = parsed.output || parsed.o || path.join(process.env.HOME, '.openclaw/workspace/memory');
  const ingest = new ClawTextIngest(memoryDir);
  const verbose = parsed.verbose || parsed.v;

  try {
    switch (command) {
      case 'ingest-files': {
        if (!parsed.input && !parsed.i) {
          console.error('Error: --input required for ingest-files');
          process.exit(1);
        }

        const pattern = parsed.input || parsed.i;
        const metadata = {
          project: parsed.project || parsed.p || 'ingestion',
          source: parsed.source || parsed.s || `cli:files`,
          date: parsed.date || parsed.d,
          type: 'file'
        };

        const options = {
          checkDedupe: !(parsed['no-dedupe'])
        };

        if (verbose) console.log(`📁 Ingesting files: ${pattern}`);
        const result = await ingest.fromFiles(pattern, metadata, options);
        
        if (verbose || !result.errors.length) {
          console.log(`✅ Ingested: ${result.imported} files`);
          if (result.skipped) console.log(`⏭️  Skipped: ${result.skipped} duplicates`);
        }
        if (result.errors.length) {
          console.error(`❌ Errors: ${result.errors.length}`);
          if (verbose) result.errors.forEach(e => console.error(`   - ${e.file}: ${e.error}`));
        }

        const committed = await ingest.commit();
        if (verbose) console.log(`💾 Saved ${committed.dedupeHashes} dedup hashes`);
        break;
      }

      case 'ingest-urls': {
        if (!parsed.input && !parsed.i) {
          console.error('Error: --input required for ingest-urls');
          process.exit(1);
        }

        const urls = (parsed.input || parsed.i).split(',').map(u => u.trim());
        const metadata = {
          project: parsed.project || parsed.p || 'ingestion',
          source: parsed.source || parsed.s || `cli:urls`,
          date: parsed.date || parsed.d,
          type: 'url'
        };

        if (verbose) console.log(`🌐 Ingesting URLs: ${urls.join(', ')}`);
        const result = await ingest.fromUrls(urls, metadata);
        
        console.log(`✅ Ingested: ${result.imported} URLs`);
        if (result.errors.length) {
          console.error(`❌ Errors: ${result.errors.length}`);
          if (verbose) result.errors.forEach(e => console.error(`   - ${e.url}: ${e.error}`));
        }

        const committed = await ingest.commit();
        if (verbose) console.log(`💾 Saved dedup hashes`);
        break;
      }

      case 'ingest-json': {
        if (!parsed.input && !parsed.i) {
          console.error('Error: --input required for ingest-json');
          process.exit(1);
        }

        let data;
        const inputPath = parsed.input || parsed.i;

        try {
          if (inputPath.startsWith('{') || inputPath.startsWith('[')) {
            data = JSON.parse(inputPath);
          } else {
            const fileContent = fs.readFileSync(inputPath, 'utf-8');
            data = JSON.parse(fileContent);
          }
        } catch (err) {
          console.error(`Error: Failed to parse JSON input: ${err.message}`);
          process.exit(1);
        }

        const metadata = {
          project: parsed.project || parsed.p || 'ingestion',
          source: parsed.source || parsed.s || `cli:json`,
          date: parsed.date || parsed.d,
          type: parsed.type || parsed.t || 'json'
        };

        const options = {
          checkDedupe: !(parsed['no-dedupe']),
          keyMap: {
            contentKey: 'content',
            dateKey: 'date',
            authorKey: 'author'
          }
        };

        if (verbose) console.log(`📊 Ingesting JSON data (${Array.isArray(data) ? data.length : 1} items)`);
        const result = await ingest.fromJSON(data, metadata, options);

        console.log(`✅ Ingested: ${result.imported} items`);
        if (result.skipped) console.log(`⏭️  Skipped: ${result.skipped} duplicates`);
        if (result.errors.length) {
          console.error(`❌ Errors: ${result.errors.length}`);
          if (verbose) result.errors.forEach(e => console.error(`   - ${JSON.stringify(e)}`));
        }

        const committed = await ingest.commit();
        if (verbose) console.log(`💾 Saved ${committed.dedupeHashes} dedup hashes`);
        break;
      }

      case 'ingest-text': {
        if (!parsed.input && !parsed.i) {
          console.error('Error: --input required for ingest-text');
          process.exit(1);
        }

        let text;
        const input = parsed.input || parsed.i;

        // Check if it's a file path
        if (fs.existsSync(input)) {
          text = fs.readFileSync(input, 'utf-8');
        } else {
          text = input;
        }

        const metadata = {
          project: parsed.project || parsed.p || 'ingestion',
          source: parsed.source || parsed.s || `cli:text`,
          date: parsed.date || parsed.d,
          type: 'text',
          filename: parsed.filename || `ingested-text-${new Date().toISOString().split('T')[0]}.md`
        };

        if (verbose) console.log(`📝 Ingesting text (${text.length} chars)`);
        const result = await ingest.fromText(text, metadata);

        if (result.imported) {
          console.log(`✅ Ingested: ${text.length} characters`);
        } else if (result.skipped) {
          console.log(`⏭️  Skipped: Content is a duplicate`);
        }

        if (result.errors.length) {
          console.error(`❌ Errors: ${result.errors.length}`);
          if (verbose) result.errors.forEach(e => console.error(`   - ${e.error}`));
        }

        const committed = await ingest.commit();
        if (verbose) console.log(`💾 Saved dedup hashes`);
        break;
      }

      case 'batch': {
        if (!parsed.config && !parsed.c) {
          console.error('Error: --config required for batch ingestion');
          process.exit(1);
        }

        const configPath = parsed.config || parsed.c;
        const configData = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

        if (verbose) console.log(`📦 Running batch ingestion from ${configPath}`);
        const result = await ingest.ingestAll(configData.sources || []);

        console.log(`✅ Batch complete:`);
        console.log(`   Imported: ${result.totalImported}`);
        console.log(`   Skipped: ${result.totalSkipped}`);
        if (result.errors.length) {
          console.error(`❌ Total errors: ${result.errors.length}`);
        }

        if (verbose) {
          result.results.forEach(r => {
            console.log(`   ${r.type}: imported=${r.result.imported}, skipped=${r.result.skipped}`);
          });
        }
        break;
      }

      case 'rebuild': {
        if (verbose) console.log(`🔄 Rebuilding ClawText clusters...`);
        const result = await ingest.rebuildClusters();

        if (result.success) {
          console.log(`✅ Clusters marked for rebuild`);
        } else {
          console.error(`❌ Error: ${result.error}`);
          process.exit(1);
        }
        break;
      }

      case 'status': {
        const report = ingest.getReport();
        console.log(`\nClawText-Ingest Status:`);
        console.log(`  Total Imported: ${report.totalImported}`);
        console.log(`  Total Skipped: ${report.totalSkipped}`);
        console.log(`  Errors: ${report.errorCount}`);
        console.log(`  Dedup Hashes: ${report.dedupeHashes}`);
        console.log(`  Memory Dir: ${report.memoryDir}`);
        
        if (report.errors.length && verbose) {
          console.log(`\n  Recent Errors:`);
          report.errors.slice(0, 5).forEach(e => {
            console.log(`    - ${JSON.stringify(e).substring(0, 80)}`);
          });
        }
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        console.log(`Run 'clawtext-ingest help' for usage.`);
        process.exit(1);
    }
  } catch (err) {
    console.error(`❌ Fatal error: ${err.message}`);
    if (verbose) console.error(err.stack);
    process.exit(1);
  }
}

main().catch(err => {
  console.error(`❌ Unexpected error: ${err.message}`);
  process.exit(1);
});
