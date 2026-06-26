#!/usr/bin/env node
/**
 * Schedule a post to Facebook Page
 * Usage: openclaw-facebook-posting fb-post-schedule "<message>" "<scheduled_time>"
 * Time format: ISO 8601 (e.g., "2024-04-20T10:00:00Z")
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

module.exports = async (message, scheduledTime) => {
  if (!message || !scheduledTime) {
    console.error('❌ Error: message and scheduled_time are required');
    console.error('Usage: openclaw-facebook-posting fb-post-schedule "<message>" "<scheduled_time>"');
    console.error('Time format: ISO 8601 (e.g., "2024-04-20T10:00:00Z")');
    process.exit(1);
  }

  // Validate ISO 8601 format
  const date = new Date(scheduledTime);
  if (isNaN(date.getTime())) {
    console.error('❌ Error: Invalid date format. Use ISO 8601 (e.g., "2024-04-20T10:00:00Z")');
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

  console.log('⏰ Scheduling post to Facebook Page...\n');
  console.log(`📅 Scheduled for: ${date.toISOString()}`);

  try {
    const response = await makeHttpsRequest(
      'POST',
      `/${page_id}/feed`,
      {
        message: message,
        scheduled_publish_time: Math.floor(date.getTime() / 1000)
      },
      access_token
    );

    console.log('✅ Post scheduled successfully!');
    console.log(`📄 Post ID: ${response.id}`);
    console.log(`🔗 URL: https://www.facebook.com/${page_id}/posts/${response.id}`);
  } catch (error) {
    console.error('❌ Failed to schedule post:', error.message);
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  const [, , message, scheduledTime] = process.argv;
  module.exports(message, scheduledTime);
}
