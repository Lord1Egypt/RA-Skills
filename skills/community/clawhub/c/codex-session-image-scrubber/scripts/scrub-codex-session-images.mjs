#!/usr/bin/env node
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';

const DEFAULT_MIN_BYTES = 100000;
const PLACEHOLDER = '[removed image payload from local session log]';

function usage() {
  return `Usage:
  scrub-codex-session-images.mjs --thread-id <id> [--write]
  scrub-codex-session-images.mjs --file <path> [--write]

Options:
  --thread-id <id>       Find a Codex session JSONL by thread id.
  --file <path>          Scrub a specific JSONL file.
  --write                Rewrite the file. Without this, dry-run only.
  --backup-dir <path>    Backup directory. Default: ~/.codex/session_backups
  --sessions-dir <path>  Sessions root. Default: ~/.codex/sessions
  --min-bytes <n>        Large image-field threshold. Default: ${DEFAULT_MIN_BYTES}
  --help                 Show this help.
`;
}

function expandHome(value) {
  if (!value || value === '~') return os.homedir();
  if (value.startsWith('~/')) return path.join(os.homedir(), value.slice(2));
  return value;
}

function parseArgs(argv) {
  const args = {
    backupDir: '~/.codex/session_backups',
    sessionsDir: '~/.codex/sessions',
    minBytes: DEFAULT_MIN_BYTES,
    write: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      const value = argv[i + 1];
      if (!value || value.startsWith('--')) {
        throw new Error(`Missing value for ${arg}`);
      }
      i += 1;
      return value;
    };

    if (arg === '--thread-id') args.threadId = next();
    else if (arg === '--file') args.file = next();
    else if (arg === '--write') args.write = true;
    else if (arg === '--dry-run') args.write = false;
    else if (arg === '--backup-dir') args.backupDir = next();
    else if (arg === '--sessions-dir') args.sessionsDir = next();
    else if (arg === '--min-bytes') args.minBytes = Number(next());
    else if (arg === '--help' || arg === '-h') {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (args.file && args.threadId) {
    throw new Error('Use either --file or --thread-id, not both.');
  }
  if (!args.file && !args.threadId) {
    throw new Error('Provide --file or --thread-id.');
  }
  if (!Number.isFinite(args.minBytes) || args.minBytes < 0) {
    throw new Error('--min-bytes must be a non-negative number.');
  }

  args.backupDir = expandHome(args.backupDir);
  args.sessionsDir = expandHome(args.sessionsDir);
  if (args.file) args.file = expandHome(args.file);
  return args;
}

async function* walkJsonlFiles(dir) {
  let entries;
  try {
    entries = await fsp.readdir(dir, { withFileTypes: true });
  } catch {
    return;
  }

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walkJsonlFiles(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.jsonl')) {
      yield fullPath;
    }
  }
}

async function findSessionFileByThreadId(threadId, sessionsDir) {
  const matches = [];
  for await (const file of walkJsonlFiles(sessionsDir)) {
    if (path.basename(file).includes(threadId)) {
      matches.push(file);
    }
  }

  if (matches.length === 1) return matches[0];
  if (matches.length > 1) {
    throw new Error(`Multiple session files match ${threadId}:\n${matches.join('\n')}`);
  }
  throw new Error(`No session JSONL found for thread id ${threadId} under ${sessionsDir}`);
}

function looksLikeImageString(value) {
  return typeof value === 'string' && (
    value.startsWith('data:image/') ||
    /^iVBORw0KGgo/.test(value) ||
    /^\/9j\//.test(value) ||
    /^UklGR/.test(value)
  );
}

function byteLength(value) {
  return Buffer.byteLength(value, 'utf8');
}

function countImageBytes(value) {
  if (typeof value === 'string') {
    return looksLikeImageString(value) ? byteLength(value) : 0;
  }
  if (!value || typeof value !== 'object') return 0;
  if (Array.isArray(value)) {
    return value.reduce((sum, item) => sum + countImageBytes(item), 0);
  }
  return Object.values(value).reduce((sum, item) => sum + countImageBytes(item), 0);
}

function scrub(value, stats, options, key = '', parent = null) {
  if (typeof value === 'string') {
    const isLargeImageField =
      byteLength(value) > options.minBytes &&
      (key === 'image_url' || (key === 'data' && /image/i.test(String(parent?.type ?? parent?.mimeType ?? ''))));

    if (looksLikeImageString(value) || isLargeImageField) {
      stats.imageStringsReplaced += 1;
      stats.approxBytesRemoved += Math.max(0, byteLength(value) - byteLength(PLACEHOLDER));
      return PLACEHOLDER;
    }
    return value;
  }

  if (!value || typeof value !== 'object') return value;

  if (Array.isArray(value)) {
    if (key === 'images' && value.some(looksLikeImageString)) {
      stats.imageArraysCleared += 1;
      for (const item of value) {
        const bytes = typeof item === 'string' ? byteLength(item) : countImageBytes(item);
        if (bytes > 0) {
          stats.imageStringsReplaced += 1;
          stats.approxBytesRemoved += Math.max(0, bytes - byteLength(PLACEHOLDER));
        }
      }
      return [];
    }
    return value.map((item) => scrub(item, stats, options, '', value));
  }

  if (value.type === 'input_image' && typeof value.image_url === 'string') {
    stats.imageItemsReplaced += 1;
    stats.approxBytesRemoved += Math.max(0, byteLength(value.image_url) - byteLength(PLACEHOLDER));
    return { type: 'input_text', text: PLACEHOLDER };
  }

  if ((value.type === 'image' || value.type === 'input_image') && typeof value.data === 'string') {
    stats.imageItemsReplaced += 1;
    stats.approxBytesRemoved += Math.max(0, byteLength(value.data) - byteLength(PLACEHOLDER));
    return { type: 'text', text: PLACEHOLDER };
  }

  const output = {};
  for (const [childKey, childValue] of Object.entries(value)) {
    output[childKey] = scrub(childValue, stats, options, childKey, value);
  }
  return output;
}

function backupName(file) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  return `${path.basename(file, '.jsonl')}.before-image-scrub-${stamp}.jsonl`;
}

async function scrubFile(file, options) {
  const stat = await fsp.stat(file);
  if (!stat.isFile()) throw new Error(`Not a file: ${file}`);

  const tmp = `${file}.scrub-tmp-${Date.now()}`;
  const stats = {
    file,
    mode: options.write ? 'write' : 'dry-run',
    sizeBefore: stat.size,
    sizeAfter: 0,
    lines: 0,
    parseErrors: 0,
    imageItemsReplaced: 0,
    imageArraysCleared: 0,
    imageStringsReplaced: 0,
    approxBytesRemoved: 0,
    backupFile: null,
  };

  const input = fs.createReadStream(file, { encoding: 'utf8' });
  const rl = readline.createInterface({ input, crlfDelay: Infinity });
  const output = options.write ? fs.createWriteStream(tmp, { encoding: 'utf8', mode: stat.mode }) : null;

  try {
    for await (const line of rl) {
      stats.lines += 1;
      if (line.length === 0) {
        stats.sizeAfter += 1;
        if (output) output.write('\n');
        continue;
      }

      let parsed;
      try {
        parsed = JSON.parse(line);
      } catch (error) {
        stats.parseErrors += 1;
        throw new Error(`Failed to parse line ${stats.lines}: ${error.message}`);
      }

      const scrubbed = scrub(parsed, stats, options);
      const outLine = `${JSON.stringify(scrubbed)}\n`;
      stats.sizeAfter += byteLength(outLine);
      if (output) output.write(outLine);
    }

    if (!options.write) return stats;

    if (stats.approxBytesRemoved === 0) {
      await new Promise((resolve, reject) => output.end((err) => err ? reject(err) : resolve()));
      await fsp.rm(tmp, { force: true });
      return stats;
    }

    await fsp.mkdir(options.backupDir, { recursive: true });
    stats.backupFile = path.join(options.backupDir, backupName(file));
    await fsp.copyFile(file, stats.backupFile, fs.constants.COPYFILE_EXCL);

    await new Promise((resolve, reject) => output.end((err) => err ? reject(err) : resolve()));
    await fsp.chmod(tmp, stat.mode);
    try {
      await fsp.chown(tmp, stat.uid, stat.gid);
    } catch {
      // Non-root users may not be allowed to chown; preserving mode is enough.
    }
    await fsp.rename(tmp, file);
    return stats;
  } catch (error) {
    if (output) output.destroy();
    await fsp.rm(tmp, { force: true }).catch(() => {});
    throw error;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const file = args.file ?? await findSessionFileByThreadId(args.threadId, args.sessionsDir);
  const stats = await scrubFile(file, args);
  console.log(JSON.stringify(stats, null, 2));
  if (!args.write) {
    console.error('Dry-run only. Re-run with --write to modify the file and create a backup.');
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
