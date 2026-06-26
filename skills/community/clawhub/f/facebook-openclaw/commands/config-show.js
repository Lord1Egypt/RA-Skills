#!/usr/bin/env node
/**
 * Show current Facebook configuration
 * Usage: openclaw-facebook-posting fb-config-show
 */

const fs = require('fs');
const path = require('path');

const os = require('os');
const workspaceDir = path.join(os.homedir(), '.openclaw', 'workspace');
const configPath = path.join(workspaceDir, 'facebook-config.json');

module.exports = async () => {
  if (!fs.existsSync(configPath)) {
    console.log('ℹ️  No configuration found.');
    console.log('\n📝 Run setup first:');
    console.log('   openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]');
    return;
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

  console.log('⚙️  Current Facebook Configuration:\n');
  console.log(`📁 Config file: ${configPath}`);
  console.log(`📄 Page ID: ${config.page_id}`);
  if (config.page_name) {
    console.log(`📄 Page Name: ${config.page_name}`);
  }
  console.log(`🔑 Access Token: ${config.access_token.substring(0, 15)}...${config.access_token.length} chars`);
  console.log(`📅 Created: ${new Date(config.created_at).toLocaleString()}`);
  console.log('\n💡 Commands:');
  console.log('   fb-post "<message>"              - Post text');
  console.log('   fb-post-image "<caption>" "<url>" - Post image');
  console.log('   fb-post-schedule "<msg>" "<time>" - Schedule post');
  console.log('   fb-post-schedule-list            - List scheduled posts');
  console.log('   fb-post-schedule-delete <id>     - Delete scheduled post');
  console.log('   fb-post-test                     - Test connection');
  console.log('   fb-config-show                   - Show this help');
  console.log('   fb-post-setup <id> <token>       - Reconfigure');
};

// CLI entry point
if (require.main === module) {
  module.exports();
}
