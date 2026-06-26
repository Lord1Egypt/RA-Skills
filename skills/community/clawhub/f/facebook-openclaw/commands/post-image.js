#!/usr/bin/env node
/**
 * Post image to Facebook Page
 * Usage: openclaw-facebook-posting fb-post-image "<caption>" "<image_url>"
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const os = require('os');
const workspaceDir = path.join(os.homedir(), '.openclaw', 'workspace');
const configPath = path.join(workspaceDir, 'facebook-config.json');

function makeHttpsRequest(method, path, body, accessToken) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
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
    req.write(data);
    req.end();
  });
}

module.exports = async (caption, imageUrl) => {
  if (!caption || !imageUrl) {
    console.error('❌ Error: caption and image_url are required');
    console.error('Usage: openclaw-facebook-posting fb-post-image "<caption>" "<image_url>"');
    process.exit(1);
  }

  // Load config
  if (!fs.existsSync(configPath)) {
    console.error('❌ Error: Configuration not found. Run setup first:');
    console.error('   openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const { page_id, access_token } = config;

  console.log('🖼️  Posting image to Facebook Page...\n');

  try {
    const response = await makeHttpsRequest(
      'POST',
      `/${page_id}/photos`,
      {
        message: caption,
        url: imageUrl
      },
      access_token
    );

    console.log('✅ Image post created successfully!');
    console.log(`📄 Post ID: ${response.id}`);
    console.log(`🔗 URL: https://www.facebook.com/${page_id}/posts/${response.id}`);
  } catch (error) {
    console.error('❌ Failed to create post:', error.message);
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  const [, , caption, imageUrl] = process.argv;
  module.exports(caption, imageUrl);
}
