#!/usr/bin/env node
/**
 * Delete a scheduled post
 * Usage: openclaw-facebook-posting fb-post-schedule-delete <post_id>
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

module.exports = async (postId) => {
  if (!postId) {
    console.error('❌ Error: post_id is required');
    console.error('Usage: openclaw-facebook-posting fb-post-schedule-delete <post_id>');
    process.exit(1);
  }

  // Load config
  if (!fs.existsSync(configPath)) {
    console.error('❌ Error: Configuration not found. Run setup first:');
    console.error('   openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const { access_token } = config;

  console.log('🗑️  Deleting scheduled post...\n');

  try {
    const response = await makeHttpsRequest(
      'DELETE',
      `/${postId}?access_token=${access_token}`,
      null,
      access_token
    );

    if (response.success) {
      console.log('✅ Scheduled post deleted successfully!');
    } else {
      console.error('❌ Failed to delete scheduled post');
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ Failed to delete scheduled post:', error.message);
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  const [, , postId] = process.argv;
  module.exports(postId);
}
