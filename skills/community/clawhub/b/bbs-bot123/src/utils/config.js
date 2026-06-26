const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Configuration Manager
 * 
 * Manages skill configuration from environment variables and config file.
 */
class ConfigManager {
  constructor() {
    this.configDir = path.join(os.homedir(), '.bbsbot');
    this.configFile = path.join(this.configDir, 'config.json');
    this.defaultConfig = {
      baseUrl: 'https://bbs.bot',
      timeout: 30000,
      retryAttempts: 3,
      retryDelay: 1000
    };
    
    // Ensure config directory exists
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true });
    }
  }
  
  /**
   * Load configuration from environment variables and config file
   * @returns {Object} Merged configuration
   */
  loadConfig() {
    const config = { ...this.defaultConfig };
    
    // Load from config file if exists
    if (fs.existsSync(this.configFile)) {
      try {
        const fileConfig = JSON.parse(fs.readFileSync(this.configFile, 'utf8'));
        Object.assign(config, fileConfig);
      } catch (error) {
        console.warn('Failed to load config file:', error.message);
      }
    }
    
    // Override with environment variables
    const envMappings = {
      BBS_BOT_BASE_URL: 'baseUrl',
      BBS_BOT_USERNAME: 'username',
      BBS_BOT_PASSWORD: 'password',
      BBS_BOT_EMAIL: 'email',
      BBS_BOT_DISPLAY_NAME: 'displayName',
      BBS_BOT_TOKEN: 'token',
      BBS_BOT_TIMEOUT: 'timeout',
      BBS_BOT_RETRY_ATTEMPTS: 'retryAttempts',
      BBS_BOT_RETRY_DELAY: 'retryDelay'
    };
    
    for (const [envVar, configKey] of Object.entries(envMappings)) {
      if (process.env[envVar]) {
        // Convert string to number for numeric values
        if (['timeout', 'retryAttempts', 'retryDelay'].includes(configKey)) {
          config[configKey] = parseInt(process.env[envVar], 10);
        } else {
          config[configKey] = process.env[envVar];
        }
      }
    }
    
    return config;
  }
  
  /**
   * Save configuration to file
   * @param {Object} config - Configuration to save
   */
  saveConfig(config) {
    try {
      // Don't save passwords to config file
      const safeConfig = { ...config };
      delete safeConfig.password;
      
      fs.writeFileSync(
        this.configFile,
        JSON.stringify(safeConfig, null, 2),
        'utf8'
      );
      
      // Set appropriate permissions
      fs.chmodSync(this.configFile, 0o600);
    } catch (error) {
      console.error('Failed to save config:', error.message);
      throw error;
    }
  }
  
  /**
   * Save authentication token to config
   * @param {string} token - JWT token
   */
  saveToken(token) {
    const config = this.loadConfig();
    config.token = token;
    this.saveConfig(config);
  }
  
  /**
   * Clear authentication token from config
   */
  clearToken() {
    const config = this.loadConfig();
    delete config.token;
    this.saveConfig(config);
  }
  
  /**
   * Set configuration value
   * @param {string} key - Configuration key
   * @param {*} value - Configuration value
   */
  setConfig(key, value) {
    const config = this.loadConfig();
    
    // Convert string to appropriate type
    let typedValue = value;
    if (['timeout', 'retryAttempts', 'retryDelay'].includes(key)) {
      typedValue = parseInt(value, 10);
    } else if (value === 'true' || value === 'false') {
      typedValue = value === 'true';
    } else if (!isNaN(value) && value !== '') {
      typedValue = Number(value);
    }
    
    config[key] = typedValue;
    this.saveConfig(config);
  }
  
  /**
   * Get configuration value
   * @param {string} key - Configuration key
   * @returns {*} Configuration value
   */
  getConfig(key) {
    const config = this.loadConfig();
    return config[key];
  }
  
  /**
   * Get all configuration
   * @returns {Object} All configuration
   */
  getAllConfig() {
    return this.loadConfig();
  }
  
  /**
   * Reset configuration to defaults
   */
  resetConfig() {
    this.saveConfig(this.defaultConfig);
  }
  
  /**
   * Check if configuration is valid
   * @returns {boolean} True if configuration is valid
   */
  isValid() {
    const config = this.loadConfig();
    
    // Check required fields for API operations
    if (!config.baseUrl) {
      console.error('Missing baseUrl in configuration');
      return false;
    }
    
    // Validate URL format
    try {
      new URL(config.baseUrl);
    } catch (error) {
      console.error('Invalid baseUrl:', config.baseUrl);
      return false;
    }
    
    return true;
  }
  
  /**
   * Get configuration file path
   * @returns {string} Config file path
   */
  getConfigPath() {
    return this.configFile;
  }
  
  /**
   * Get configuration directory path
   * @returns {string} Config directory path
   */
  getConfigDir() {
    return this.configDir;
  }
  
  /**
   * Export configuration as environment variables
   * @returns {Object} Environment variables object
   */
  exportAsEnv() {
    const config = this.loadConfig();
    const env = {};
    
    const envMappings = {
      baseUrl: 'BBS_BOT_BASE_URL',
      username: 'BBS_BOT_USERNAME',
      password: 'BBS_BOT_PASSWORD',
      email: 'BBS_BOT_EMAIL',
      displayName: 'BBS_BOT_DISPLAY_NAME',
      token: 'BBS_BOT_TOKEN',
      timeout: 'BBS_BOT_TIMEOUT',
      retryAttempts: 'BBS_BOT_RETRY_ATTEMPTS',
      retryDelay: 'BBS_BOT_RETRY_DELAY'
    };
    
    for (const [configKey, envVar] of Object.entries(envMappings)) {
      if (config[configKey] !== undefined) {
        env[envVar] = String(config[configKey]);
      }
    }
    
    return env;
  }
}

module.exports = ConfigManager;