#!/usr/bin/env node
/**
 * List scheduled posts for Facebook Page
 * Usage: openclaw-facebook-posting fb-post-schedule-list
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const os = require('os');
const workspaceDir = path.join(os.homedir(), '.openclaw', 'workspace');
const configPath = path.join(workspaceDir, 'facebook-config.json');

function makeHttpsRequest(method, path, body, accessToken) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : '';
    const options = {
      hostname: 'graph.facebook.com',
      port: 443,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API Error (${res.statusCode}): ${JSON.stringify(response)}`));
          }
        } catch (e) {
          reject(new Error(`Invalid response: ${responseData}`));
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

module.exports = async () => {
  // Load config
  if (!fs.existsSync(configPath)) {
    console.error('❌ Error: Configuration not found. Run setup first:');
    console.error('   openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const { page_id, access_token } = config;

  console.log('📋 Fetching scheduled posts...\n');

  try {
    const response = await makeHttpsRequest(
      'GET',
      `/${page_id}/scheduled_posts?access_token=${access_token}`,
      null,
      access_token
    );

    if (!response.data || response.data.length === 0) {
      console.log('ℹ️  No scheduled posts found.');
      return;
    }

    console.log(`📊 Found ${response.data.length} scheduled post(s):\n`);
    response.data.forEach((post, index) => {
      const date = post.scheduled_publish_time 
        ? new Date(post.scheduled_publish_time * 1000).toLocaleString()
        : 'Unknown';
      console.log(`${index + 1}. ${post.message?.substring(0, 50) || 'No message'}...`);
      console.log(`   📅 Scheduled: ${date}`);
      console.log(`   📄 ID: ${post.id}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Failed to fetch scheduled posts:', error.message);
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  module.exports();
}
