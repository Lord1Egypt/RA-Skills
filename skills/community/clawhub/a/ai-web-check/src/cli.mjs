#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { scan, runJourney, toMarkdown } from './core.mjs';

function usage() { return 'Usage: ai-web-check scan <url> [--format json|markdown] [--out file]\n       ai-web-check journey <url> --journey journey.json [--format json|markdown] [--out file]\n'; }
function args(argv) { const [command, url, ...rest] = argv; const flags = {}; for (let i = 0; i < rest.length; i += 1) if (rest[i].startsWith('--')) flags[rest[i].slice(2)] = rest[i + 1]?.startsWith('--') ? true : (rest[++i] ?? true); return { command, url, flags }; }

try {
  const { command, url, flags } = args(process.argv.slice(2));
  if (!['scan', 'journey'].includes(command) || !url) throw new Error(usage());
  const format = flags.format || 'json';
  if (!['json', 'markdown'].includes(format)) throw new Error('--format must be json or markdown');
  let result;
  if (command === 'scan') result = await scan(url);
  else { if (!flags.journey || flags.journey === true) throw new Error('journey requires --journey <file>'); result = await runJourney(url, JSON.parse(await readFile(flags.journey, 'utf8'))); }
  const output = format === 'markdown' ? toMarkdown(result) : `${JSON.stringify(result, null, 2)}\n`;
  if (flags.out && flags.out !== true) await writeFile(flags.out, output, 'utf8'); else process.stdout.write(output);
} catch (error) { process.stderr.write(`ai-web-check: ${error.message}\n`); process.exitCode = 2; }
