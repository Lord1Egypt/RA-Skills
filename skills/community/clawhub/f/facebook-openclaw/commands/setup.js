#!/usr/bin/env node
/**
 * Setup command for Facebook Page posting
 * Usage: openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]
 */

const fs = require('fs');
const path = require('path');

const os = require('os');
const workspaceDir = path.join(os.homedir(), '.openclaw', 'workspace');
const configPath = path.join(workspaceDir, 'facebook-config.json');

module.exports = async (pageId, accessToken, pageName) => {
  console.log('🔧 Setting up Facebook Page posting...\n');

  // Validate inputs
  if (!pageId || !accessToken) {
    console.error('❌ Error: page_id and access_token are required');
    console.error('Usage: openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]');
    process.exit(1);
  }

  // Create config object
  const config = {
    page_id: pageId,
    access_token: accessToken,
    page_name: pageName || null,
    created_at: new Date().toISOString()
  };

  // Ensure workspace directory exists
  if (!fs.existsSync(workspaceDir)) {
    fs.mkdirSync(workspaceDir, { recursive: true });
  }

  // Write config file
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

  console.log('✅ Configuration saved successfully!');
  console.log(`📁 Config file: ${configPath}`);
  console.log(`📄 Page ID: ${pageId}`);
  if (pageName) {
    console.log(`📄 Page Name: ${pageName}`);
  }
  console.log('\n📝 Next steps:');
  console.log('   - Test with: openclaw-facebook-posting fb-post-test');
  console.log('   - Post with: openclaw-facebook-posting fb-post "Your message"');
  console.log('   - See help: openclaw-facebook-posting --help');
};

// CLI entry point
if (require.main === module) {
  const [, , pageId, accessToken, pageName] = process.argv;
  module.exports(pageId, accessToken, pageName);
}
