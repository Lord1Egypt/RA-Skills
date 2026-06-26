#!/usr/bin/env node

// ============================================================================
// Follow Builders CLI Tool
// ============================================================================
// Unified command-line interface for all Follow Builders operations.
//
// Usage: node cli.js <command> [args...]
// ============================================================================

import { readFile, writeFile, mkdir, unlink } from 'fs/promises';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PROJECT_DIR = join(SCRIPT_DIR, '..');
const CONFIG_PATH = join(PROJECT_DIR, 'config', 'config.json');
const STATE_PATH = join(PROJECT_DIR, 'state-feed.json');
const ENV_PATH = join(PROJECT_DIR, '.env');
const PROMPTS_DIR = join(PROJECT_DIR, 'prompts');

const CONFIG_SCHEMA = {
  language: { enum: ['en', 'zh', 'bilingual'], default: 'en' },
  sourceMode: { enum: ['merge', 'replace'], default: 'merge' },
  lookbackHours: { type: 'number', min: 1, max: 168, default: 24 },
  onboardingComplete: { type: 'boolean', default: false }
};

// ============================================================================
// Utility Functions
// ============================================================================

function success(data) {
  console.log(JSON.stringify({ status: 'ok', ...data }, null, 2));
  process.exit(0);
}

function error(message, code = 1) {
  console.error(JSON.stringify({ status: 'error', message }, null, 2));
  process.exit(code);
}

async function ensureDir(dir) {
  if (!existsSync(dir)) {
    await mkdir(dir, { recursive: true });
  }
}

async function readJSON(path) {
  try {
    const content = await readFile(path, 'utf-8');
    return JSON.parse(content);
  } catch (err) {
    if (existsSync(path)) {
      error(`Failed to parse JSON at ${path}: ${err.message}`);
    }
    return null;
  }
}

async function writeJSON(path, data) {
  await ensureDir(dirname(path));
  await writeFile(path, JSON.stringify(data, null, 2));
}

async function loadConfig() {
  const config = await readJSON(CONFIG_PATH);
  if (!config) {
    error(`Config file not found: ${CONFIG_PATH}`);
  }
  return config;
}

async function saveConfig(config) {
  await writeJSON(CONFIG_PATH, config);
}

function validateConfigKey(key, value) {
  const schema = CONFIG_SCHEMA[key];
  if (!schema) {
    error(`Invalid config key: ${key}`);
  }

  if (schema.enum && !schema.enum.includes(value)) {
    error(`Invalid value for ${key}: must be one of ${schema.enum.join(', ')}`);
  }

  if (schema.type === 'number') {
    const num = Number(value);
    if (isNaN(num)) {
      error(`Invalid number value for ${key}`);
    }
    if (schema.min && num < schema.min) {
      error(`Value for ${key} must be at least ${schema.min}`);
    }
    if (schema.max && num > schema.max) {
      error(`Value for ${key} must be at most ${schema.max}`);
    }
    return num;
  }

  if (schema.type === 'boolean') {
    return value === 'true' || value === true;
  }

  return value;
}

// ============================================================================
// Commands: Onboarding
// ============================================================================

async function cmdSetupEnv() {
  const args = process.argv.slice(3);

  const rettiwtApiKey = args[0] || '';

  if (rettiwtApiKey) {
    const envContent = `# Optional: Rettiwt API key for Twitter user auth (guest auth works without this)
RETTIWT_API_KEY=${rettiwtApiKey}
`;
    await writeFile(ENV_PATH, envContent);
    success({ message: 'Rettiwt API key saved. Twitter will use user auth.', path: ENV_PATH });
  } else {
    const envContent = `# Follow Builders - no API keys required
# Optionally add RETTIWT_API_KEY for Twitter user auth if guest auth is rate limited
# FB_PROXY=http://127.0.0.1:7897
# YT_DLP_COOKIES=chrome
`;
    await writeFile(ENV_PATH, envContent);
    success({ message: 'Environment file created. Twitter will use guest auth (no key needed). YouTube requires yt-dlp installed.', path: ENV_PATH });
  }
}

async function cmdInitConfig() {
  const args = process.argv.slice(3);

  const language = args[0] || 'en';
  const lookbackHours = args[1] ? Number(args[1]) : 24;

  if (!CONFIG_SCHEMA.language.enum.includes(language)) {
    error(`Invalid language: must be one of ${CONFIG_SCHEMA.language.enum.join(', ')}`);
  }

  if (isNaN(lookbackHours) || lookbackHours < 1 || lookbackHours > 168) {
    error('Invalid lookbackHours: must be a number between 1 and 168');
  }

  const config = await loadConfig();
  config.language = language;
  config.lookbackHours = lookbackHours;
  config.onboardingComplete = true;

  await saveConfig(config);
  success({ message: 'Config initialized successfully', config });
}

async function cmdCheckOnboarding() {
  const config = await readJSON(CONFIG_PATH);
  const envExists = existsSync(ENV_PATH);

  const configExists = config !== null;
  const isComplete = config?.onboardingComplete === true;

  success({
    onboardingComplete: isComplete,
    envExists,
    configExists,
    config: config || null
  });
}

// ============================================================================
// Commands: Config Management
// ============================================================================

async function cmdGetConfig() {
  const config = await loadConfig();
  success({ config });
}

async function cmdSetConfig() {
  const args = process.argv.slice(3);

  if (args.length < 2) {
    error('Usage: cli.js set-config <key> <value>');
  }

  const [key, value] = args;

  const config = await loadConfig();
  const validatedValue = validateConfigKey(key, value);
  config[key] = validatedValue;

  await saveConfig(config);
  success({ message: `Config updated`, key, value: validatedValue, config });
}

async function cmdUpdateConfig() {
  const args = process.argv.slice(3);

  if (args.length === 0) {
    error('Usage: cli.js update-config <json_string>');
  }

  const jsonStr = args[0];
  let updates;
  try {
    updates = JSON.parse(jsonStr);
  } catch (err) {
    error(`Invalid JSON: ${err.message}`);
  }

  const config = await loadConfig();

  for (const [key, value] of Object.entries(updates)) {
    const validatedValue = validateConfigKey(key, value);
    config[key] = validatedValue;
  }

  await saveConfig(config);
  success({ message: 'Config updated successfully', config });
}

// ============================================================================
// Commands: Source Management
// ============================================================================

async function cmdListSources() {
  const config = await loadConfig();
  success({
    mode: config.sourceMode || 'merge',
    sources: config.sources || {}
  });
}

async function cmdAddSource() {
  const args = process.argv.slice(3);

  if (args.length < 2) {
    error('Usage: cli.js add-source <type> <name> <...params>');
  }

  const [type, name, ...params] = args;
  const config = await loadConfig();
  if (!config.sources) config.sources = {};

  if (type === 'x') {
    if (params.length === 0) {
      error('Usage: cli.js add-source x <name> <handle>');
    }
    const handle = params[0];
    if (!config.sources.x_accounts) config.sources.x_accounts = [];

    // Check for duplicates
    const exists = config.sources.x_accounts.find(a => a.handle === handle);
    if (exists) {
      error(`Twitter account @${handle} already exists`);
    }

    config.sources.x_accounts.push({ name, handle, enabled: true });
  } else if (type === 'podcast') {
    if (params.length < 3) {
      error('Usage: cli.js add-source podcast <name> <channel_or_playlist> <url> <id>');
    }
    const [pType, url, id] = params;
    if (!config.sources.podcasts) config.sources.podcasts = [];

    if (!['youtube_channel', 'youtube_playlist'].includes(pType)) {
      error('Podcast type must be youtube_channel or youtube_playlist');
    }

    const podcast = { name, type: pType, url, enabled: true };
    if (pType === 'youtube_channel') {
      podcast.channelHandle = id;
    } else {
      podcast.playlistId = id;
    }

    config.sources.podcasts.push(podcast);
  } else if (type === 'blog') {
    if (params.length < 1) {
      error('Usage: cli.js add-source blog <name> <indexUrl> [articleBaseUrl]');
    }
    const [indexUrl, articleBaseUrl] = params;
    if (!config.sources.blogs) config.sources.blogs = [];

    const blog = {
      name,
      type: 'scrape',
      indexUrl,
      fetchMethod: 'http',
      enabled: true
    };

    if (articleBaseUrl) {
      blog.articleBaseUrl = articleBaseUrl;
    }

    config.sources.blogs.push(blog);
  } else {
    error(`Unknown source type: ${type}. Use x, podcast, or blog`);
  }

  await saveConfig(config);
  success({ message: 'Source added successfully', sources: config.sources });
}

async function cmdRemoveSource() {
  const args = process.argv.slice(3);

  if (args.length < 2) {
    error('Usage: cli.js remove-source <type> <id>');
  }

  const [type, id] = args;
  const config = await loadConfig();
  if (!config.sources) error('No sources configured');

  let removed = false;

  if (type === 'x') {
    if (!config.sources.x_accounts) error('No Twitter accounts configured');
    config.sources.x_accounts = config.sources.x_accounts.filter(a => {
      if (a.handle === id) {
        removed = true;
        return false;
      }
      return true;
    });
  } else if (type === 'podcast') {
    if (!config.sources.podcasts) error('No podcasts configured');
    config.sources.podcasts = config.sources.podcasts.filter(p => {
      const podcastId = p.channelHandle || p.playlistId;
      if (podcastId === id) {
        removed = true;
        return false;
      }
      return true;
    });
  } else if (type === 'blog') {
    if (!config.sources.blogs) error('No blogs configured');
    config.sources.blogs = config.sources.blogs.filter(b => {
      if (b.indexUrl === id || b.name === id) {
        removed = true;
        return false;
      }
      return true;
    });
  } else {
    error(`Unknown source type: ${type}. Use x, podcast, or blog`);
  }

  if (!removed) {
    error(`Source not found: ${type}/${id}`);
  }

  await saveConfig(config);
  success({ message: 'Source removed successfully', sources: config.sources });
}

async function cmdToggleSource() {
  const args = process.argv.slice(3);

  if (args.length < 3) {
    error('Usage: cli.js toggle-source <type> <id> <true|false>');
  }

  const [type, id, state] = args;
  const enabled = state === 'true' || state === true;

  const config = await loadConfig();
  if (!config.sources) error('No sources configured');

  let found = false;

  if (type === 'x') {
    if (!config.sources.x_accounts) error('No Twitter accounts configured');
    for (const account of config.sources.x_accounts) {
      if (account.handle === id) {
        account.enabled = enabled;
        found = true;
        break;
      }
    }
  } else if (type === 'podcast') {
    if (!config.sources.podcasts) error('No podcasts configured');
    for (const podcast of config.sources.podcasts) {
      const podcastId = podcast.channelHandle || podcast.playlistId;
      if (podcastId === id) {
        podcast.enabled = enabled;
        found = true;
        break;
      }
    }
  } else if (type === 'blog') {
    if (!config.sources.blogs) error('No blogs configured');
    for (const blog of config.sources.blogs) {
      if (blog.indexUrl === id || blog.name === id) {
        blog.enabled = enabled;
        found = true;
        break;
      }
    }
  } else {
    error(`Unknown source type: ${type}. Use x, podcast, or blog`);
  }

  if (!found) {
    error(`Source not found: ${type}/${id}`);
  }

  await saveConfig(config);
  success({ message: `Source ${enabled ? 'enabled' : 'disabled'}`, sources: config.sources });
}

async function cmdSetMode() {
  const args = process.argv.slice(3);

  if (args.length === 0) {
    error('Usage: cli.js set-mode <merge|replace>');
  }

  const mode = args[0];
  if (!['merge', 'replace'].includes(mode)) {
    error('Mode must be merge or replace');
  }

  const config = await loadConfig();
  config.sourceMode = mode;
  await saveConfig(config);
  success({ message: `Mode set to ${mode}`, config });
}

async function cmdResetSources() {
  const config = await loadConfig();
  // Reset sources to empty — user can re-add what they want
  config.sources = { x_accounts: [], podcasts: [], blogs: [] };
  await saveConfig(config);
  success({ message: 'Sources reset to empty. Add new sources or restore defaults from git.' });
}

// ============================================================================
// Commands: Prompt Management
// ============================================================================

async function cmdGetPrompt() {
  const args = process.argv.slice(3);

  if (args.length === 0) {
    error('Usage: cli.js get-prompt <name>');
  }

  const name = args[0];
  const filename = name.endsWith('.md') ? name : `${name}.md`;
  const localPath = join(PROMPTS_DIR, filename);

  if (!existsSync(localPath)) {
    error(`Prompt not found: ${name}`);
  }

  const content = await readFile(localPath, 'utf-8');
  success({ name, source: 'local', content });
}

async function cmdSetPrompt() {
  const args = process.argv.slice(3);

  if (args.length < 2) {
    error('Usage: cli.js set-prompt <name> <content>');
  }

  const [name, ...contentArgs] = args;
  const content = contentArgs.join(' ');
  const filename = name.endsWith('.md') ? name : `${name}.md`;
  const localPath = join(PROMPTS_DIR, filename);

  await writeFile(localPath, content);
  success({ message: 'Prompt saved successfully', path: localPath });
}

async function cmdResetPrompt() {
  const args = process.argv.slice(3);

  if (args.length === 0) {
    error('Usage: cli.js reset-prompt <name>');
  }

  success({ message: 'Prompt files are tracked in git. Use git checkout to restore defaults.', name: args[0] });
}

// ============================================================================
// Commands: Utilities
// ============================================================================

async function cmdGetStats() {
  const state = await readJSON(STATE_PATH);

  if (!state) {
    success({ message: 'No state file found' });
  }

  success({
    seenTweets: Object.keys(state.seenTweets || {}).length,
    seenVideos: Object.keys(state.seenVideos || {}).length,
    seenArticles: Object.keys(state.seenArticles || {}).length,
    state
  });
}

// ============================================================================
// Main
// ============================================================================

const commands = {
  // Onboarding
  'setup-env': cmdSetupEnv,
  'init-config': cmdInitConfig,
  'check-onboarding': cmdCheckOnboarding,

  // Config Management
  'get-config': cmdGetConfig,
  'set-config': cmdSetConfig,
  'update-config': cmdUpdateConfig,

  // Source Management
  'list-sources': cmdListSources,
  'add-source': cmdAddSource,
  'remove-source': cmdRemoveSource,
  'toggle-source': cmdToggleSource,
  'set-mode': cmdSetMode,
  'reset-sources': cmdResetSources,

  // Prompt Management
  'get-prompt': cmdGetPrompt,
  'set-prompt': cmdSetPrompt,
  'reset-prompt': cmdResetPrompt,

  // Utilities
  'get-stats': cmdGetStats,
  'help': () => {
    success({
      message: 'Follow Builders CLI Tool',
      commands: {
        onboarding: ['setup-env', 'init-config', 'check-onboarding'],
        config: ['get-config', 'set-config', 'update-config'],
        sources: ['list-sources', 'add-source', 'remove-source', 'toggle-source', 'set-mode', 'reset-sources'],
        prompts: ['get-prompt', 'set-prompt', 'reset-prompt'],
        utilities: ['get-stats']
      }
    });
  }
};

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    error('Usage: node cli.js <command> [args...]\nRun "node cli.js help" for available commands');
  }

  const [cmdName, ...cmdArgs] = args;
  const cmd = commands[cmdName];

  if (!cmd) {
    error(`Unknown command: ${cmdName}\nRun "node cli.js help" for available commands`);
  }

  cmd().catch(err => {
    error(err.message);
  });
}

main();
