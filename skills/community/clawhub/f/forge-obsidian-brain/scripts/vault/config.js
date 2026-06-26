#!/usr/bin/env node
/**
 * Obsidian Config Reader Module
 * Parses .obsidian/app.json and plugin configs
 */

const fs = require('fs');
const path = require('path');

/**
 * Read and parse a JSON config file safely
 * @param {string} filePath 
 * @returns {Object|null}
 */
function readJsonFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    return null;
  }
}

/**
 * Write a JSON config file safely
 * @param {string} filePath 
 * @param {Object} data 
 * @returns {boolean}
 */
function writeJsonFile(filePath, data) {
  try {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (err) {
    return false;
  }
}

/**
 * Read Obsidian's core app.json config
 * @param {string} vaultPath 
 * @returns {Object|null}
 */
function readAppConfig(vaultPath) {
  const configPath = path.join(vaultPath, '.obsidian', 'app.json');
  const config = readJsonFile(configPath);
  return config || {};
}

/**
 * Read Obsidian's appearance config
 * @param {string} vaultPath 
 * @returns {Object|null}
 */
function readAppearanceConfig(vaultPath) {
  const configPath = path.join(vaultPath, '.obsidian', 'appearance.json');
  const config = readJsonFile(configPath);
  return config || {};
}

/**
 * Read daily notes configuration (core plugin)
 * @param {string} vaultPath 
 * @returns {Object}
 */
function readDailyNotesConfig(vaultPath) {
  // Core daily notes config is in app.json
  const appConfig = readAppConfig(vaultPath);
  
  // Default daily notes settings
  const defaults = {
    folder: 'Daily',
    format: 'YYYY-MM-DD',
    template: '',
  };

  // Obsidian uses nested config for daily notes
  if (appConfig['daily-notes']) {
    return {
      ...defaults,
      folder: appConfig['daily-notes'].folder || defaults.folder,
      format: appConfig['daily-notes'].format || defaults.format,
      template: appConfig['daily-notes'].template || defaults.template,
    };
  }

  return defaults;
}

/**
 * Read templates configuration (core plugin)
 * @param {string} vaultPath 
 * @returns {Object}
 */
function readTemplatesConfig(vaultPath) {
  const appConfig = readAppConfig(vaultPath);
  
  const defaults = {
    folder: 'Templates',
  };

  if (appConfig.templates) {
    return {
      ...defaults,
      folder: appConfig.templates.folder || defaults.folder,
    };
  }

  return defaults;
}

/**
 * Get all core Obsidian settings
 * @param {string} vaultPath 
 * @returns {Object}
 */
function getAllSettings(vaultPath) {
  return {
    app: readAppConfig(vaultPath),
    appearance: readAppearanceConfig(vaultPath),
    dailyNotes: readDailyNotesConfig(vaultPath),
    templates: readTemplatesConfig(vaultPath),
  };
}

/**
 * Update a configuration value
 * @param {string} vaultPath 
 * @param {string} configType - 'app', 'appearance', etc.
 * @param {string} key 
 * @param {*} value 
 * @returns {boolean}
 */
function updateConfig(vaultPath, configType, key, value) {
  const configFiles = {
    app: 'app.json',
    appearance: 'appearance.json',
  };

  const filename = configFiles[configType];
  if (!filename) {
    return false;
  }

  const configPath = path.join(vaultPath, '.obsidian', filename);
  let config = readJsonFile(configPath) || {};
  
  config[key] = value;
  
  return writeJsonFile(configPath, config);
}

/**
 * Ensure default folder structure exists for AI Brain
 * @param {string} vaultPath 
 * @returns {Object} Created folders
 */
function ensureBrainFolders(vaultPath) {
  const folders = [
    'Brain',
    'Brain/Thoughts',
    'Brain/Research',
    'Brain/Conversations',
    'Brain/Entities',
    'Brain/Relations',
  ];

  const results = {};

  for (const folder of folders) {
    const folderPath = path.join(vaultPath, folder);
    try {
      if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
        results[folder] = { created: true, path: folderPath };
      } else {
        results[folder] = { created: false, exists: true, path: folderPath };
      }
    } catch (err) {
      results[folder] = { created: false, error: err.message };
    }
  }

  return results;
}

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  const vaultPath = args[0] || process.env.OBSIDIAN_VAULT;

  if (!vaultPath) {
    console.error('Error: Vault path required');
    console.error('Usage: config.js <vault-path> [command]');
    process.exit(1);
  }

  const command = args[1] || 'all';

  switch (command) {
    case 'all':
      console.log(JSON.stringify(getAllSettings(vaultPath), null, 2));
      break;
    case 'daily-notes':
      console.log(JSON.stringify(readDailyNotesConfig(vaultPath), null, 2));
      break;
    case 'templates':
      console.log(JSON.stringify(readTemplatesConfig(vaultPath), null, 2));
      break;
    case 'ensure-folders':
      console.log(JSON.stringify(ensureBrainFolders(vaultPath), null, 2));
      break;
    default:
      console.error(`Unknown command: ${command}`);
      process.exit(1);
  }
}

module.exports = {
  readJsonFile,
  writeJsonFile,
  readAppConfig,
  readAppearanceConfig,
  readDailyNotesConfig,
  readTemplatesConfig,
  getAllSettings,
  updateConfig,
  ensureBrainFolders,
};
