#!/usr/bin/env node
// One-line installer for the deepseek-web-search skill.
// Run via `npx github:mingzeng21/deepseek-web-search` or `node bin/install.mjs`.
import { readFileSync, existsSync, cpSync, mkdirSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createInterface } from 'readline';
import { Writable } from 'stream';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SKILL_NAME = 'deepseek-web-search';
const KEY_URL = 'https://platform.deepseek.com';
const KEY_PLACEHOLDER = 'sk-在此填入你的DeepSeek_API_Key';

const HOME = process.env.HOME || '';
const TARGETS = {
  claude: { label: 'Claude Code', dir: join(HOME, '.claude', 'skills') },
  agents: { label: 'Codex / Gemini CLI / Copilot CLI', dir: join(HOME, '.agents', 'skills') },
};

const SKILL_FILES = ['SKILL.md', 'search.mjs'];
const PLUGIN_DIR = join(ROOT, '.claude-plugin');

function printHelp() {
  console.log(`deepseek-web-search installer

Usage:
  npx github:mingzeng21/deepseek-web-search [--claude] [--codex] [--skip-key]

  (no flag)   install to every supported harness (default)
  --claude    only ~/.claude/skills/    (Claude Code)
  --codex     only ~/.agents/skills/    (Codex / Gemini CLI / Copilot CLI)
  --all       install to every supported harness
  --skip-key  do not prompt for an API key (add it later)
  --help      show this help`);
}

function needsConfig(key) {
  return !existsSync(join(TARGETS[key].dir, SKILL_NAME, 'config.json'));
}

// Ask for input with keystrokes hidden from the terminal.
function askHidden(question) {
  return new Promise((resolve) => {
    const muted = { value: false };
    const output = new Writable({
      write(chunk, enc, cb) {
        if (muted.value) cb();
        else process.stdout.write(chunk, enc, cb);
      },
    });
    const rl = createInterface({ input: process.stdin, output, terminal: true });
    rl.question(question, (answer) => {
      muted.value = false;
      process.stdout.write('\n');
      rl.close();
      resolve(answer.trim());
    });
    muted.value = true;
  });
}

async function resolveApiKey(skipPrompt) {
  const envKey = (process.env.DEEPSEEK_API_KEY || '').trim();
  if (envKey) {
    console.log(`  DEEPSEEK_API_KEY is set — the script will read it (config.json gets a placeholder).`);
    return '';
  }
  if (skipPrompt) {
    console.log(`  Skipping API key prompt (--skip-key). Add the key later to config.json or set DEEPSEEK_API_KEY.`);
    return '';
  }
  if (!process.stdin.isTTY) {
    console.log(`  Non-interactive shell — add your API key later to config.json or set DEEPSEEK_API_KEY.`);
    return '';
  }
  const answer = await askHidden(`  Paste your DeepSeek API key (get one at ${KEY_URL}) [Enter to skip]: `);
  if (answer) {
    console.log('  API key saved to config.json.');
    return answer;
  }
  console.log(`  No key provided — add it later to config.json (get one at ${KEY_URL}).`);
  return '';
}

function install(key, apiKey) {
  const { label, dir } = TARGETS[key];
  const dest = join(dir, SKILL_NAME);
  mkdirSync(dest, { recursive: true });
  for (const f of SKILL_FILES) cpSync(join(ROOT, f), join(dest, f));
  if (existsSync(PLUGIN_DIR)) cpSync(PLUGIN_DIR, join(dest, '.claude-plugin'), { recursive: true });

  const config = join(dest, 'config.json');
  if (!existsSync(config)) {
    writeFileSync(config, JSON.stringify({ apiKey: apiKey || KEY_PLACEHOLDER }, null, 2) + '\n', { mode: 0o600 });
    if (apiKey) console.log(`  wrote API key -> ${config}`);
    else console.log(`  created ${config} - paste your DeepSeek API key in it`);
  }
  console.log(`  installed -> ${dest}  (${label})`);
}

const allArgs = process.argv.slice(2);
if (allArgs.includes('--help') || allArgs.includes('-h')) { printHelp(); process.exit(0); }
const skipPrompt = allArgs.includes('--skip-key');
const args = allArgs.filter((a) => a !== '--skip-key');

let selected;
if (args.length === 0 || args.includes('--all')) {
  selected = Object.keys(TARGETS);
} else {
  selected = args
    .map((a) => a.replace(/^--/, ''))
    .filter((a) => TARGETS[a]);
  if (selected.length === 0) { printHelp(); process.exit(1); }
}

console.log(`Installing "${SKILL_NAME}" skill...`);

let apiKey = '';
if (selected.some(needsConfig)) {
  apiKey = await resolveApiKey(skipPrompt);
}
for (const key of selected) install(key, apiKey);
console.log('\nDone. Restart your harness (or run /reload-plugins in Claude Code) to load the skill.');
