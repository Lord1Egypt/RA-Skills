#!/usr/bin/env node
/**
 * Agent Browser Automation Script
 * Provides enhanced browser automation for OpenClaw agents
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

class BrowserAutomation {
  constructor() {
    this.browserCommands = {
      open: 'openclaw browser open',
      snapshot: 'openclaw browser snapshot',
      navigate: 'openclaw browser navigate',
      act: 'openclaw browser act',
      status: 'openclaw browser status'
    };
  }

  /**
   * Execute a browser command
   */
  async executeCommand(command, args = {}) {
    try {
      let cmd = this.browserCommands[command];
      
      if (!cmd) {
        throw new Error(`Unknown browser command: ${command}`);
      }

      // Add arguments
      for (const [key, value] of Object.entries(args)) {
        if (value !== undefined && value !== null) {
          if (typeof value === 'boolean' && value) {
            cmd += ` --${key}`;
          } else if (typeof value === 'string' || typeof value === 'number') {
            cmd += ` --${key} "${value}"`;
          } else if (typeof value === 'object') {
            cmd += ` --${key} '${JSON.stringify(value)}'`;
          }
        }
      }

      console.log(`Executing: ${cmd}`);
      const { stdout, stderr } = await execAsync(cmd);
      
      if (stderr) {
        console.warn('Warning:', stderr);
      }
      
      return stdout;
    } catch (error) {
      console.error('Error executing browser command:', error.message);
      throw error;
    }
  }

  /**
   * Open a URL in browser
   */
  async openUrl(url, options = {}) {
    return this.executeCommand('open', {
      url,
      ...options
    });
  }

  /**
   * Take a screenshot of a page
   */
  async takeScreenshot(url, outputPath, options = {}) {
    return this.executeCommand('snapshot', {
      url,
      output: outputPath,
      ...options
    });
  }

  /**
   * Navigate to a URL
   */
  async navigate(url, options = {}) {
    return this.executeCommand('navigate', {
      url,
      ...options
    });
  }

  /**
   * Perform an action on the page
   */
  async performAction(action, options = {}) {
    return this.executeCommand('act', {
      kind: action,
      ...options
    });
  }

  /**
   * Check browser status
   */
  async getStatus() {
    return this.executeCommand('status');
  }

  /**
   * Extract text from a page
   */
  async extractText(url, maxChars = 5000) {
    return this.executeCommand('snapshot', {
      url,
      maxChars,
      mode: 'efficient'
    });
  }

  /**
   * Fill a form
   */
  async fillForm(url, formData, options = {}) {
    return this.executeCommand('act', {
      url,
      kind: 'fill',
      fields: formData,
      ...options
    });
  }

  /**
   * Click an element
   */
  async clickElement(url, selector, options = {}) {
    return this.executeCommand('act', {
      url,
      kind: 'click',
      selector,
      ...options
    });
  }
}

// CLI interface
if (require.main === module) {
  const automation = new BrowserAutomation();
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
Agent Browser Automation CLI

Usage:
  node browser-automation.js <command> [options]

Commands:
  open <url>                    Open a URL
  screenshot <url> <output>     Take screenshot
  navigate <url>                Navigate to URL
  status                        Check browser status
  extract <url>                 Extract page text
  click <url> <selector>        Click an element
  fill <url> <json>             Fill a form

Examples:
  node browser-automation.js open "https://example.com"
  node browser-automation.js screenshot "https://example.com" screenshot.png
  node browser-automation.js extract "https://news.com" --maxChars 3000
    `);
    process.exit(0);
  }

  const command = args[0];
  
  switch (command) {
    case 'open':
      automation.openUrl(args[1]).then(console.log).catch(console.error);
      break;
    case 'screenshot':
      automation.takeScreenshot(args[1], args[2]).then(console.log).catch(console.error);
      break;
    case 'navigate':
      automation.navigate(args[1]).then(console.log).catch(console.error);
      break;
    case 'status':
      automation.getStatus().then(console.log).catch(console.error);
      break;
    case 'extract':
      automation.extractText(args[1], args[2] || 5000).then(console.log).catch(console.error);
      break;
    default:
      console.error(`Unknown command: ${command}`);
      process.exit(1);
  }
}

module.exports = BrowserAutomation;