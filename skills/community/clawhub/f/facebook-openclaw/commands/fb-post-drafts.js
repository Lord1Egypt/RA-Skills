#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-drafts
 * List draft posts on Facebook Page.
 * 
 * Usage:
 *   openclaw fb-post-drafts
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');

const program = new Command();

program
  .name('fb-post-drafts')
  .description('List draft posts on Facebook Page')
  .option('--limit <n>', 'Maximum number to show', '50')
  .action((options) => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    if (!fs.existsSync(configPath)) {
      console.error('❌ Configuration file not found: facebook-posting.json');
      console.error('Run "openclaw fb-post-setup" first.');
      process.exit(1);
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { access_token, page_id } = config;
    const limit = parseInt(options.limit, 10);
    
    console.log('📋 Fetching draft posts...\n');
    
    // Draft posts are in the feed with is_draft=true
    const options = {
      hostname: 'graph.facebook.com',
      path: `/${page_id}/feed?limit=${limit}&filter=custom&access_token=${access_token}`,
      method: 'GET'
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          if (result.error) {
            console.error('❌ Error:', result.error.message);
            console.error('');
            console.error('Note: Draft posts may not be available for all Page types.');
            process.exit(1);
          }
          
          const posts = result.data || [];
          
          // Filter for draft posts (those with is_draft=true)
          const drafts = posts.filter(post => post.is_draft === true);
          
          if (drafts.length === 0) {
            console.log('ℹ️  No draft posts found.');
            console.log('');
            console.log('To create a post:');
            console.log('  openclaw fb-post "Your message"');
            return;
          }
          
          console.log(`Found ${drafts.length} draft post(s):\n`);
          
          drafts.forEach((post, index) => {
            const createdTime = new Date(post.created_time);
            
            console.log(`${index + 1}. ID: ${post.id}`);
            console.log(`   Message: ${post.message || '(no message)'}`);
            console.log(`   Created: ${createdTime.toLocaleString()}`);
            console.log();
          });
          
          console.log('Commands:');
          console.log('  openclaw fb-post-delete <post_id>  - Delete a draft post');
          
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
  });

program.parse();
