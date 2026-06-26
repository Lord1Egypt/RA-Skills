#!/usr/bin/env node
/**
 * Test Facebook Page connection
 * Usage: openclaw-facebook-posting fb-post-test
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
  const { page_id, access_token, page_name } = config;

  console.log('🧪 Testing Facebook Page connection...\n');
  console.log(`📄 Page ID: ${page_id}`);
  if (page_name) {
    console.log(`📄 Page Name: ${page_name}`);
  }

  try {
    // Test 1: Verify access token and page access
    const pageInfo = await makeHttpsRequest(
      'GET',
      `/${page_id}?fields=id,name,access_token&access_token=${access_token}`,
      null,
      access_token
    );

    console.log('✅ Connection successful!');
    console.log(`📄 Page Name: ${pageInfo.name}`);
    console.log(`📄 Page ID: ${pageInfo.id}`);

    // Test 2: Check permissions
    const permissions = await makeHttpsRequest(
      'GET',
      `/${page_id}/permissions?access_token=${access_token}`,
      null,
      access_token
    );

    console.log('\n🔐 Permissions:');
    if (permissions.data && permissions.data.length > 0) {
      permissions.data.forEach(perm => {
        console.log(`   - ${perm.permission}: ${perm.status}`);
      });
    } else {
      console.log('   ℹ️  No specific permissions listed');
    }

    console.log('\n✅ All tests passed! You can now use the posting commands.');
  } catch (error) {
    console.error('\n❌ Connection test failed:', error.message);
    console.log('\n💡 Troubleshooting:');
    console.log('   - Check if the access token is valid and not expired');
    console.log('   - Ensure the token has the required permissions (pages_manage_posts, pages_read_engagement)');
    console.log('   - Verify the page_id is correct');
    console.log('   - Run setup again with a fresh access token if needed');
    process.exit(1);
  }
};

// CLI entry point
if (require.main === module) {
  module.exports();
}
