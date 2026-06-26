#!/usr/bin/env node

import { execFile } from 'child_process';
import { mkdtemp, readFile, rm, writeFile } from 'fs/promises';
import { tmpdir } from 'os';
import { dirname, join } from 'path';
import { promisify } from 'util';
import { fileURLToPath } from 'url';

const execFileAsync = promisify(execFile);

function detectReceiveIdType(target) {
  if (!target) return 'open_id';
  if (target.startsWith('oc_')) return 'chat_id';
  if (target.startsWith('ou_')) return 'open_id';
  if (target.startsWith('on_')) return 'union_id';
  return 'open_id';
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = {
    accountId: null,
    avatarFallbackAccount: null,
    file: null,
    dryRunFile: null,
    mode: 'openclaw_account',
    printCard: false,
    to: null,
    receiveIdType: null
  };

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    switch (arg) {
      case '--file':
        parsed.file = args[++i];
        break;
      case '--account':
        parsed.accountId = args[++i];
        break;
      case '--avatar-fallback-account':
        parsed.avatarFallbackAccount = args[++i];
        break;
      case '--mode':
        parsed.mode = args[++i];
        break;
      case '--to':
        parsed.to = args[++i];
        break;
      case '--receive-id-type':
        parsed.receiveIdType = args[++i];
        break;
      case '--dry-run-file':
        parsed.dryRunFile = args[++i];
        break;
      case '--print-card':
        parsed.printCard = true;
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return parsed;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf-8');
}

async function readStructuredInput(filePath) {
  const raw = filePath
    ? await readFile(filePath, 'utf-8')
    : await readStdin();
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Input is not valid JSON: ${error.message}`);
  }
}

async function withAvatarTempDir(run) {
  const tempDir = await mkdtemp(join(tmpdir(), 'follow-builders-card-'));
  try {
    return await run(tempDir);
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
}

async function cropAvatarToCircle(buffer, tempDir) {
  const sourcePath = join(tempDir, `avatar-${Date.now()}-${Math.random().toString(16).slice(2)}.img`);
  const outputPath = join(tempDir, `avatar-${Date.now()}-${Math.random().toString(16).slice(2)}.png`);
  const scriptPath = join(dirname(fileURLToPath(import.meta.url)), 'circle-avatar.py');

  await writeFile(sourcePath, buffer);
  await execFileAsync('python3', [scriptPath, sourcePath, outputPath, '88']);
  return readFile(outputPath);
}

async function writeCardJson(filePath, card) {
  await writeFile(filePath, JSON.stringify(card, null, 2));
}

export {
  detectReceiveIdType,
  parseArgs,
  readStructuredInput,
  withAvatarTempDir,
  cropAvatarToCircle,
  writeCardJson
};
