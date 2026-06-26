#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-image
 * Post an image to Facebook Page.
 * 
 * Usage:
 *   openclaw fb-post-image "<caption>" "<image_url>"
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');

const program = new Command();

program
  .name('fb-post-image')
  .description('Post an image to Facebook Page')
  .argument('<caption>', 'The caption for the image')
  .argument('<image_url>', 'URL of the image to post')
  .action((caption, imageUrl) => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    if (!fs.existsSync(configPath)) {
      console.error('❌ Configuration file not found: facebook-posting.json');
      console.error('Run "openclaw fb-post-setup" first.');
      process.exit(1);
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { access_token, page_id } = config;
    
    console.log('🖼️  Posting image to Facebook...\n');
    console.log(`Page: ${config.page_name || page_id}`);
    console.log(`Caption: "${caption}"`);
    console.log(`Image: ${imageUrl}\n`);
    
    const bodyData = {
      message: caption,
      url: imageUrl,
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
            console.log('✅ Image posted successfully!');
            console.log(`Post ID: ${result.id}`);
            console.log(`URL: https://facebook.com/${page_id}/posts/${result.id}`);
          } else {
            console.error('❌ Error posting image:');
            if (result.error) {
              console.error(result.error.message);
              
              if (result.error.code === 100) {
                console.log('');
                console.log('💡 Possible issues:');
                console.log('   - Image URL is not publicly accessible');
                console.log('   - Image URL is blocked by Facebook');
                console.log('   - Try a different image URL');
              }
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
