const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

class AuthManager {
  constructor() {
    this.tokenFile = path.join(process.cwd(), '.ekybot-token');
    this.configFile = path.join(process.cwd(), '.env');
  }

  // Load API token from environment or token file
  loadToken() {
    // Try environment variable first
    if (process.env.EKYBOT_API_KEY) {
      return process.env.EKYBOT_API_KEY;
    }

    // Try .env file
    if (fs.existsSync(this.configFile)) {
      const envContent = fs.readFileSync(this.configFile, 'utf8');
      const match = envContent.match(/EKYBOT_API_KEY=(.+)/);
      if (match) {
        return match[1].trim();
      }
    }

    // Try token file (legacy)
    if (fs.existsSync(this.tokenFile)) {
      return fs.readFileSync(this.tokenFile, 'utf8').trim();
    }

    return null;
  }

  // Save API token to .env file
  saveToken(token) {
    try {
      let envContent = '';

      // Read existing .env if it exists
      if (fs.existsSync(this.configFile)) {
        envContent = fs.readFileSync(this.configFile, 'utf8');
      }

      // Update or add EKYBOT_API_KEY
      if (envContent.includes('EKYBOT_API_KEY=')) {
        envContent = envContent.replace(/EKYBOT_API_KEY=.+/, `EKYBOT_API_KEY=${token}`);
      } else {
        if (envContent && !envContent.endsWith('\n')) {
          envContent += '\n';
        }
        envContent += `EKYBOT_API_KEY=${token}\n`;
      }

      fs.writeFileSync(this.configFile, envContent, { mode: 0o600 }); // Owner-only read/write
      console.log(chalk.green(`✓ API token saved to ${this.configFile} (permissions: 600)`));

      // Remove legacy token file if it exists
      if (fs.existsSync(this.tokenFile)) {
        fs.unlinkSync(this.tokenFile);
        console.log(chalk.blue(`🗑️  Removed legacy token file`));
      }

      return true;
    } catch (error) {
      console.error(chalk.red(`❌ Failed to save token: ${error.message}`));
      return false;
    }
  }

  // Validate token format
  isValidToken(token) {
    if (!token) return false;

    // Basic validation - tokens should be at least 20 characters
    if (token.length < 20) return false;

    // Should not contain whitespace
    if (/\s/.test(token)) return false;

    return true;
  }

  // Clear saved token
  clearToken() {
    try {
      // Remove from .env file
      if (fs.existsSync(this.configFile)) {
        let envContent = fs.readFileSync(this.configFile, 'utf8');
        envContent = envContent.replace(/EKYBOT_API_KEY=.+\n?/g, '');

        if (envContent.trim()) {
          fs.writeFileSync(this.configFile, envContent);
        } else {
          fs.unlinkSync(this.configFile);
        }
      }

      // Remove legacy token file
      if (fs.existsSync(this.tokenFile)) {
        fs.unlinkSync(this.tokenFile);
      }

      console.log(chalk.green('✓ API token cleared'));
      return true;
    } catch (error) {
      console.error(chalk.red(`❌ Failed to clear token: ${error.message}`));
      return false;
    }
  }

  // Get token info (for debugging)
  getTokenInfo() {
    const token = this.loadToken();

    if (!token) {
      return { exists: false };
    }

    return {
      exists: true,
      length: token.length,
      prefix: token.substring(0, 8) + '...',
      source: process.env.EKYBOT_API_KEY
        ? 'environment'
        : fs.existsSync(this.configFile)
          ? '.env file'
          : 'token file',
    };
  }
}

module.exports = AuthManager;
