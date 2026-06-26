#!/usr/bin/env node
/**
 * Vault Discovery Module
 * Auto-discovers Obsidian vault location cross-platform
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Known Obsidian config locations by platform
const OBSIDIAN_CONFIG_PATHS = {
  linux: [
    path.join(os.homedir(), '.config', 'obsidian', 'obsidian.json'),
    path.join(os.homedir(), '.var', 'app', 'md.obsidian.Obsidian', 'config', 'obsidian', 'obsidian.json'),
  ],
  darwin: [
    path.join(os.homedir(), 'Library', 'Application Support', 'obsidian', 'obsidian.json'),
  ],
  win32: [
    path.join(os.homedir(), 'AppData', 'Roaming', 'obsidian', 'obsidian.json'),
  ],
};

const DEFAULT_FALLBACK = path.join(os.homedir(), 'obsidian-vault');

/**
 * Read Obsidian's config file to find registered vaults
 * @returns {string|null} First vault path found, or null
 */
function readObsidianConfig() {
  const platform = os.platform();
  const configPaths = OBSIDIAN_CONFIG_PATHS[platform] || OBSIDIAN_CONFIG_PATHS.linux;

  for (const configPath of configPaths) {
    try {
      if (fs.existsSync(configPath)) {
        const content = fs.readFileSync(configPath, 'utf8');
        const config = JSON.parse(content);
        
        if (config.vaults && Object.keys(config.vaults).length > 0) {
          // Return the first vault path
          const vaultIds = Object.keys(config.vaults);
          return config.vaults[vaultIds[0]].path;
        }
      }
    } catch (err) {
      // Continue to next path
    }
  }
  return null;
}

/**
 * Check if a path is a valid Obsidian vault
 * @param {string} vaultPath 
 * @returns {boolean}
 */
function isValidVault(vaultPath) {
  try {
    const stats = fs.statSync(vaultPath);
    if (!stats.isDirectory()) return false;
    
    // Check for .obsidian directory
    const obsidianDir = path.join(vaultPath, '.obsidian');
    return fs.existsSync(obsidianDir) && fs.statSync(obsidianDir).isDirectory();
  } catch (err) {
    return false;
  }
}

/**
 * Attempt to resolve symlink and get real vault path
 * @param {string} vaultPath 
 * @returns {string}
 */
function resolveVaultPath(vaultPath) {
  try {
    return fs.realpathSync(vaultPath);
  } catch (err) {
    return vaultPath;
  }
}

/**
 * Discover the vault path using multiple strategies
 * @param {Object} options
 * @param {string} [options.preferred] - Preferred vault path (highest priority)
 * @returns {Object} Discovery result with path and metadata
 */
function discoverVault(options = {}) {
  const strategies = [];
  
  // Strategy 1: User-provided preferred path
  if (options.preferred) {
    strategies.push({ name: 'preferred', path: options.preferred });
  }
  
  // Strategy 2: Environment variable
  if (process.env.OBSIDIAN_VAULT) {
    strategies.push({ name: 'env', path: process.env.OBSIDIAN_VAULT });
  }
  
  // Strategy 3: Obsidian config file
  const configVault = readObsidianConfig();
  if (configVault) {
    strategies.push({ name: 'obsidian-config', path: configVault });
  }
  
  // Strategy 4: Fallback to ~/obsidian-vault
  strategies.push({ name: 'fallback', path: DEFAULT_FALLBACK });

  // Try each strategy
  for (const strategy of strategies) {
    const resolved = resolveVaultPath(strategy.path);
    if (isValidVault(resolved)) {
      return {
        success: true,
        path: resolved,
        strategy: strategy.name,
        isValid: true,
      };
    }
  }

  // No valid vault found
  return {
    success: false,
    path: null,
    strategy: null,
    isValid: false,
    tried: strategies.map(s => s.path),
  };
}

/**
 * List all discovered vaults from Obsidian config
 * @returns {Array<{id: string, path: string}>}
 */
function listAllVaults() {
  const platform = os.platform();
  const configPaths = OBSIDIAN_CONFIG_PATHS[platform] || OBSIDIAN_CONFIG_PATHS.linux;
  const vaults = [];

  for (const configPath of configPaths) {
    try {
      if (fs.existsSync(configPath)) {
        const content = fs.readFileSync(configPath, 'utf8');
        const config = JSON.parse(content);
        
        if (config.vaults) {
          for (const [id, vault] of Object.entries(config.vaults)) {
            vaults.push({
              id,
              path: vault.path,
              open: vault.open || false,
            });
          }
        }
      }
    } catch (err) {
      // Continue
    }
  }
  
  return vaults;
}

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'list') {
    const vaults = listAllVaults();
    console.log(JSON.stringify(vaults, null, 2));
  } else if (command === 'discover') {
    const preferred = args[1] || process.env.OBSIDIAN_VAULT;
    const result = discoverVault({ preferred });
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  } else {
    const result = discoverVault();
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  }
}

module.exports = {
  discoverVault,
  listAllVaults,
  isValidVault,
  resolveVaultPath,
  readObsidianConfig,
  DEFAULT_FALLBACK,
};
