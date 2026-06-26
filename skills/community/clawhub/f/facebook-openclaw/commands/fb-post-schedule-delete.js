#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-schedule-delete
 * Cancel/delete a scheduled post.
 * 
 * Usage:
 *   openclaw fb-post-schedule-delete <post_id>
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const readline = require('readline');

const program = new Command();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

program
  .name('fb-post-schedule-delete')
  .description('Cancel a scheduled post')
  .argument('<post_id>', 'The ID of the scheduled post to cancel')
  .option('--confirm', 'Skip confirmation prompt')
  .action(async (postId, options) => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    if (!fs.existsSync(configPath)) {
      console.error('❌ Configuration file not found: facebook-posting.json');
      console.error('Run "openclaw fb-post-setup" first.');
      process.exit(1);
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { access_token } = config;
    
    console.log('🗑️  Canceling scheduled post...\n');
    console.log(`Post ID: ${postId}`);
    
    // Confirm deletion
    if (!options.confirm) {
      const confirm = await question('⚠️  This will cancel the scheduled post. Continue? (y/N): ');
      
      if (confirm.toLowerCase() !== 'y' && confirm.toLowerCase() !== 'yes') {
        console.log('❌ Cancellation cancelled.');
        rl.close();
        process.exit(0);
      }
    }
    
    console.log('');
    
    const https = require('https');
    
    const deleteOptions = {
      hostname: 'graph.facebook.com',
      path: `/${postId}?access_token=${access_token}`,
      method: 'DELETE'
    };
    
    const req = https.request(deleteOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.success === true || res.statusCode === 200) {
            console.log('✅ Scheduled post canceled successfully!');
          } else {
            console.error('❌ Error canceling post:');
            if (result.error) {
              console.error(result.error.message);
            } else {
              console.error(result);
            }
            process.exit(1);
          }
        } catch (err) {
          console.error('❌ Error parsing response:', err.message);
          process.exit(1);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('❌ Request error:', err.message);
      process.exit(1);
    });
    
    req.end();
    
    rl.close();
  });

program.parse();
