#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-setup
 * Configure Facebook Page posting.
 * 
 * Usage:
 *   openclaw fb-post-setup <page_id> <access_token> [page_name]
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');
const readline = require('readline');

const program = new Command();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

program
  .name('fb-post-setup')
  .description('Configure Facebook Page posting')
  .argument('<page_id>', 'Your Facebook Page ID')
  .argument('<access_token>', 'Your Facebook Page Access Token')
  .argument('[page_name]', 'Optional: Your Page name')
  .action(async (pageId, accessToken, pageName) => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    console.log('📘 Facebook Page Setup\n');
    
    // Validate inputs
    if (!pageId || !accessToken) {
      console.error('❌ Missing required arguments.');
      console.error('');
      console.error('Usage:');
      console.error('  openclaw fb-post-setup <page_id> <access_token> [page_name]');
      console.error('');
      console.error('Example:');
      console.error('  openclaw fb-post-setup "123456789" "EAAB...token..." "My Business Page"');
      console.error('');
      console.error('Get help:');
      console.error('  openclaw fb-post-setup-help');
      process.exit(1);
    }
    
    console.log('Configuration:');
    console.log(`  Page ID: ${pageId}`);
    console.log(`  Access Token: ${accessToken.substring(0, 15)}...${accessToken.substring(accessToken.length - 5)}`);
    console.log(`  Page Name: ${pageName || '(will fetch from API)'}`);
    console.log('');
    
    // Confirm
    const confirm = await question('Continue? (y/N): ');
    
    if (confirm.toLowerCase() !== 'y' && confirm.toLowerCase() !== 'yes') {
      console.log('❌ Setup cancelled.');
      rl.close();
      process.exit(0);
    }
    
    console.log('');
    console.log('🔗 Fetching Page information...\n');
    
    // Fetch page info from Graph API
    const options = {
      hostname: 'graph.facebook.com',
      path: `/${pageId}?fields=name&access_token=${accessToken}`,
      method: 'GET'
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          if (result.error) {
            console.error('❌ Error connecting to Facebook API:');
            console.error(result.error.message);
            console.error('');
            
            if (result.error.code === 190) {
              console.error('💡 Your access token has expired.');
              console.error('   Regenerate it at: https://developers.facebook.com/tools/explorer/');
            } else if (result.error.code === 10) {
              console.error('💡 Invalid token or missing permissions.');
              console.error('   Make sure you have:');
              console.error('   - pages_manage_posts');
              console.error('   - pages_read_engagement');
              console.error('   - pages_show_list');
            }
            
            rl.close();
            process.exit(1);
          }
          
          const actualPageName = pageName || result.name;
          
          console.log('✅ Connected successfully!');
          console.log(`   Page: ${actualPageName}`);
          console.log(`   ID: ${pageId}`);
          console.log('');
          
          // Create config
          const config = {
            page_id: pageId,
            access_token: accessToken,
            page_name: actualPageName,
            created_at: new Date().toISOString()
          };
          
          // Write config file
          fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
          
          console.log('📝 Configuration saved to:');
          console.log(`   ${configPath}`);
          console.log('');
          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          console.log('✅ Setup complete!');
          console.log('');
          console.log('Next steps:');
          console.log('  1. Test your connection:');
          console.log('     openclaw fb-post-test');
          console.log('');
          console.log('  2. Post your first message:');
          console.log('     openclaw fb-post "Hello from OpenClaw!"');
          console.log('');
          console.log('  3. See all available commands:');
          console.log('     openclaw --help | grep fb-post');
          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          
          rl.close();
        } catch (err) {
          console.error('❌ Error parsing response:', err.message);
          rl.close();
          process.exit(1);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('❌ Connection error:', err.message);
      console.error('');
      console.error('💡 Check your internet connection and try again.');
      rl.close();
      process.exit(1);
    });
    
    req.end();
  });

program.parse();
