#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post
 * Post a message immediately to Facebook Page.
 * 
 * Usage:
 *   openclaw fb-post "<message>"
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');

const program = new Command();

program
  .name('fb-post')
  .description('Post a message to Facebook Page')
  .argument('<message>', 'The message to post')
  .action((message) => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    if (!fs.existsSync(configPath)) {
      console.error('❌ Configuration file not found: facebook-posting.json');
      console.error('Run "openclaw fb-post-setup" first.');
      process.exit(1);
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { access_token, page_id } = config;
    
    console.log('📝 Posting to Facebook...\n');
    console.log(`Page: ${config.page_name || page_id}`);
    console.log(`Message: "${message}"\n`);
    
    const bodyData = {
      message: message,
      access_token: access_token
    };
    
    const queryString = Object.keys(bodyData)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(bodyData[key])}`)
      .join('&');
    
    const options = {
      hostname: 'graph.facebook.com',
      path: `/${page_id}/feed?${queryString}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.id) {
            console.log('✅ Post successful!');
            console.log(`Post ID: ${result.id}`);
            console.log(`URL: https://facebook.com/${page_id}/posts/${result.id}`);
          } else {
            console.error('❌ Error posting:');
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
  });

program.parse();
