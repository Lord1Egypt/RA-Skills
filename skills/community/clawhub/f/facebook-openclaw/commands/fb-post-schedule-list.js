#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-schedule-list
 * List scheduled posts on Facebook Page.
 * 
 * Usage:
 *   openclaw fb-post-schedule-list
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');

const program = new Command();

program
  .name('fb-post-schedule-list')
  .description('List scheduled posts')
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
    
    console.log('📅 Fetching scheduled posts...\n');
    
    // Scheduled posts are in the feed with filter=scheduled
    const options = {
      hostname: 'graph.facebook.com',
      path: `/${page_id}/feed?limit=${limit}&filter=scheduled&access_token=${access_token}`,
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
            process.exit(1);
          }
          
          const posts = result.data || [];
          
          if (posts.length === 0) {
            console.log('ℹ️  No scheduled posts found.');
            console.log('');
            console.log('To schedule a post:');
            console.log('  openclaw fb-post-schedule "Your message" "tomorrow 9am"');
            return;
          }
          
          console.log(`Found ${posts.length} scheduled post(s):\n`);
          
          posts.forEach((post, index) => {
            const scheduledTime = new Date(post.scheduled_publish_time * 1000);
            const now = new Date();
            const timeUntil = Math.floor((scheduledTime.getTime() - now.getTime()) / (1000 * 60 * 60)); // hours
            
            console.log(`${index + 1}. ID: ${post.id}`);
            console.log(`   Message: ${post.message || '(no message)'}`);
            console.log(`   Scheduled: ${scheduledTime.toLocaleString()}`);
            if (timeUntil > 0) {
              console.log(`   In: ${timeUntil} hour(s)`);
            } else if (timeUntil === 0) {
              console.log(`   In: < 1 hour`);
            } else {
              console.log(`   (overdue)`);
            }
            console.log();
          });
          
          console.log('Commands:');
          console.log('  openclaw fb-post-schedule-delete <post_id>  - Cancel a scheduled post');
          
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
