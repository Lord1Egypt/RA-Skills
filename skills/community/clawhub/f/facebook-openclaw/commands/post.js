#!/usr/bin/env node
/**
 * Post text to Facebook Page
 * Usage: openclaw-facebook-posting fb-post "<message>"
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const os = require('os');
const workspaceDir = path.join(os.homedir(), '.openclaw', 'workspace');
const configPath = path.join(workspaceDir, 'facebook-config.json');

function makeHttpsRequest(method, path, body, accessToken) {
  return new Promise((resolve, reject) => {
    // If accessToken is provided and not already in path, append it
    let fullPath = path;
    if (accessToken && !path.includes('access_token=')) {
      fullPath = path + (path.includes('?') ? '&' : '?') + 'access_token=' + accessToken;
    }

    const data = body ? JSON.stringify(body) : null;
    console.log(`[DEBUG] Method: ${method}`);
    console.log(`[DEBUG] Full Path: ${fullPath}`);
    console.log(`[DEBUG] Body object:`, body);
    console.log(`[DEBUG] Stringified data: ${data}`);

    const options = {
      hostname: 'graph.facebook.com',
      port: 443,
      path: fullPath,
      method: method,
      headers: {}
    };

    if (data) {
      options.headers['Content-Type'] = 'application/json';
      options.headers['Content-Length'] = Buffer.byteLength(data);
      console.log(`[DEBUG] Headers set:`, options.headers);
    } else {
      console.log(`[DEBUG] No body, no Content-Type header`);
    }

    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        console.log(`[DEBUG] Status: ${res.statusCode}`);
        console.log(`[DEBUG] Response: ${responseData}`);
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

    req.on('error', (err) => {
      console.log(`[DEBUG] Request error:`, err.message);
      reject(err);
    });

    if (data) {
      console.log(`[DEBUG] About to write data: ${data}`);
      req.write(data);
      console.log(`[DEBUG] Data written`);
    }
    req.end();
    console.log(`[DEBUG] Request ended`);
  });
}

module.exports = async (message) => {
  if (!message) {
    console.error('❌ Error: message is required');
    console.error('Usage: openclaw-facebook-posting fb-post "<message>"');
    process.exit(1);
  }

  // Load config
  if (!fs.existsSync(configPath)) {
    console.error('❌ Error: Configuration not found. Run setup first:');
    console.error('   openclaw-facebook-posting fb-post-setup <page_id> <access_token> [page_name]');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const { page_id, access_token: userToken } = config;

  console.log('📝 Posting to Facebook Page...\n');
  console.log('🔄 Fetching Page Access Token...');

  try {
    // Step 1: Get Page Access Token using User Token
    // Request fields: access_token (the page token)
    const pageTokenResponse = await makeHttpsRequest(
      'GET',
      `/${page_id}?fields=access_token&access_token=${userToken}`,
      null,
      null // No body for GET
    );

    if (!pageTokenResponse.access_token) {
      throw new Error('Failed to retrieve Page Access Token. Ensure you are an Admin of the Page.');
    }

    const pageAccessToken = pageTokenResponse.access_token;
    console.log('✅ Page Access Token retrieved successfully.');

    // Step 2: Post using the Page Access Token
    console.log(`📝 Posting message: "${message}"`);
    console.log(`🔗 Request path: /${page_id}/feed?access_token=${pageAccessToken.substring(0, 20)}...`);
    console.log(`📦 Request body: { message: "${message}" }`);
    
    const response = await makeHttpsRequest(
      'POST',
      `/${page_id}/feed`,
      { message: message },
      pageAccessToken // Pass token as parameter instead of in URL
    );

    console.log('✅ Post created successfully!');
    console.log(`📄 Post ID: ${response.id}`);
    console.log(`🔗 URL: https://www.facebook.com/${page_id}/posts/${response.id}`);
  } catch (error) {
    console.error('❌ Failed to create post:', error.message);
    if (error.message.includes('403')) {
      console.log('\n💡 Troubleshooting:');
      console.log('   - Ensure the User Token has `pages_read_engagement` and `pages_manage_posts` permissions');
      console.log('   - Ensure the user is an Admin of the Page');
      console.log('   - The Page Access Token must be used for posting, not the User Token');
    }
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  const [, , message] = process.argv;
  module.exports(message);
}
