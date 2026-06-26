#!/usr/bin/env node

import { existsSync } from 'fs';
import { readFile } from 'fs/promises';
import { join } from 'path';

async function loadDefaultSources(sourcesPath, errors = []) {
  try {
    return JSON.parse(await readFile(sourcesPath, 'utf-8'));
  } catch (error) {
    errors.push(`Could not load default sources: ${error.message}`);
    return { podcasts: [] };
  }
}

async function loadConfig(configPath, errors = []) {
  let config = {
    language: 'en',
    frequency: 'daily',
    delivery: { method: 'stdout' }
  };

  if (!existsSync(configPath)) {
    return config;
  }

  try {
    config = JSON.parse(await readFile(configPath, 'utf-8'));
  } catch (error) {
    errors.push(`Could not read config: ${error.message}`);
  }

  return config;
}

async function loadPrompts({
  promptFiles,
  userDir,
  scriptDir,
  promptsBase,
  fetchText,
  errors = []
}) {
  const prompts = {};
  const localPromptsDir = join(scriptDir, '..', 'prompts');
  const userPromptsDir = join(userDir, 'prompts');

  for (const filename of promptFiles) {
    const key = filename.replace('.md', '').replace(/-/g, '_');
    const userPath = join(userPromptsDir, filename);
    const localPath = join(localPromptsDir, filename);

    if (existsSync(userPath)) {
      prompts[key] = await readFile(userPath, 'utf-8');
      continue;
    }

    const remote = await fetchText(`${promptsBase}/${filename}`);
    if (remote) {
      prompts[key] = remote;
      continue;
    }

    if (existsSync(localPath)) {
      prompts[key] = await readFile(localPath, 'utf-8');
    } else {
      errors.push(`Could not load prompt: ${filename}`);
    }
  }

  return prompts;
}

export {
  loadConfig,
  loadDefaultSources,
  loadPrompts
};
