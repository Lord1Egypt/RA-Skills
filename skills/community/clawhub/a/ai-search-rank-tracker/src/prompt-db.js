const fs = require('fs');
const path = require('path');

const DB_DIR = path.join(__dirname, '..', 'prompt-db');

function readPack(name) {
  const file = path.join(DB_DIR, `${name}.json`);
  if (!fs.existsSync(file)) {
    throw new Error(`Prompt pack not found: ${name}`);
  }
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function listPacks() {
  return fs.readdirSync(DB_DIR)
    .filter((name) => name.endsWith('.json') && name !== 'prompts.json')
    .map((name) => name.replace(/\.json$/, ''))
    .sort();
}

function resolvePrompts(config) {
  const promptPack = config.promptPack || config.promptPacks;
  if (!promptPack) {
    return {
      prompts: config.prompts || [],
      promptRecords: (config.prompts || []).map((prompt) => ({ prompt }))
    };
  }

  const packs = Array.isArray(promptPack) ? promptPack : [promptPack];
  const records = packs.flatMap((pack) => readPack(pack));
  const deduped = [];
  const seen = new Set();

  for (const record of records) {
    if (seen.has(record.prompt)) continue;
    seen.add(record.prompt);
    deduped.push(record);
  }

  return {
    prompts: deduped.map((item) => item.prompt),
    promptRecords: deduped,
  };
}

module.exports = {
  readPack,
  listPacks,
  resolvePrompts,
};
