#!/usr/bin/env node
/**
 * telegram_poller.mjs — Polls Telegram for replies to question messages
 *
 * Run via OpenClaw cron: * * * * * (every minute)
 * Lightweight — single HTTP call, exits immediately if no updates.
 */
import { loadEnv } from './lib/env.mjs';
loadEnv();

import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createWriteStream } from 'fs';
import { loadConfig } from './lib/queue.mjs';
import { processTelegramReplies } from './lib/telegram_answers.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));

// Tee all output to a log file
const logStream = createWriteStream(resolve(__dir, 'data/telegram_poller.log'), { flags: 'w' });
const origStdoutWrite = process.stdout.write.bind(process.stdout);
const origStderrWrite = process.stderr.write.bind(process.stderr);
process.stdout.write = (chunk, ...args) => { logStream.write(chunk); return origStdoutWrite(chunk, ...args); };
process.stderr.write = (chunk, ...args) => { logStream.write(chunk); return origStderrWrite(chunk, ...args); };
const settings = loadConfig(resolve(__dir, 'config/settings.json'));
const answersPath = resolve(__dir, 'config/answers.json');

const processed = await processTelegramReplies(settings, answersPath);
if (processed > 0) console.log(`Processed ${processed} answer(s)`);
