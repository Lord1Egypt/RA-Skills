#!/usr/bin/env node
/**
 * Hide (unpublish) a Facebook Page post
 * Note: Facebook deprecated direct post deletion via API since v2.4
 * This command hides the post from public view instead.
 * Usage: openclaw-facebook-posting fb-post-hide <post_id>
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
    }

    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData || '{}');
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API Error (${res.statusCode}): ${JSON.stringify(response)}`));
          }
        } catch (e) {
          // POST requests may return empty body on success
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ success: true });
          } else {
            reject(new Error(`Invalid response: ${responseData}`));
          }
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(data);
    }
    req.end();
  });
}

module.exports = async (postId) => {
  if (!postId) {
    console.error('❌ Error: post_id is required');
    console.error('Usage: openclaw-facebook-posting fb-post-hide <post_id>');
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

  console.log(`👻 Hiding post: ${postId}\n`);
  console.log('📝 This will unpublish the post (hide from public view).');
  console.log('📝 The post will not be visible to Page visitors.\n');
  console.log('🔄 Fetching Page Access Token...');

  try {
    // Step 1: Get Page Access Token using User Token
    const pageTokenResponse = await makeHttpsRequest(
      'GET',
      `/${page_id}?fields=access_token&access_token=${userToken}`,
      null,
      null
    );

    if (!pageTokenResponse.access_token) {
      throw new Error('Failed to retrieve Page Access Token. Ensure you are an Admin of the Page.');
    }

    const pageAccessToken = pageTokenResponse.access_token;
    console.log('✅ Page Access Token retrieved successfully.');

    // Step 2: Hide (unpublish) the post
    // This is the recommended approach since deletion is deprecated
    console.log(`👻 Hiding post from public view...`);
    
    const response = await makeHttpsRequest(
      'POST',
      `/${postId}`,
      { is_published: false },
      pageAccessToken
    );

    console.log('✅ Post hidden successfully!');
    console.log(`📄 Post ID: ${postId}`);
    console.log(`📊 The post is now unpublished and hidden from public view.`);
    console.log(`📊 Response:`, response);
  } catch (error) {
    console.error('❌ Failed to hide post:', error.message);
    
    if (error.message.includes('403')) {
      console.log('\n💡 Troubleshooting:');
      console.log('   - Ensure the User Token has `pages_manage_posts` permission');
      console.log('   - Ensure the user is an Admin of the Page');
      console.log('   - The Page Access Token must be used, not the User Token');
    } else if (error.message.includes('404')) {
      console.log('\n💡 Troubleshooting:');
      console.log('   - The post ID may be incorrect');
      console.log('   - Verify the post exists on the Page');
    } else {
      console.log('\n💡 Troubleshooting:');
      console.log('   - Check your Page Access Token permissions');
      console.log('   - Ensure the post belongs to this Page');
    }
    
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  const [, , postId] = process.argv;
  if (!postId) {
    console.error('❌ Error: post_id is required');
    console.error('Usage: openclaw-facebook-posting fb-post-hide <post_id>');
    console.error('\nNote: This command hides (unpublishes) a post, it does not delete it.');
    console.error('      To permanently delete, visit Facebook Page Settings manually.');
    process.exit(1);
  }
  module.exports(postId);
}
