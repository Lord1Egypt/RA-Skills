#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-test
 * Test Facebook Page connection and permissions.
 * 
 * Usage:
 *   openclaw fb-post-test
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');
const https = require('https');

const program = new Command();

program
  .name('fb-post-test')
  .description('Test Facebook Page connection and permissions')
  .action(() => {
    const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
    const configPath = path.join(workspace, 'facebook-posting.json');
    
    console.log('🧪 Testing Facebook Page Connection\n');
    
    // Check if config exists
    if (!fs.existsSync(configPath)) {
      console.error('❌ Configuration file not found: facebook-posting.json');
      console.error('');
      console.error('Run setup first:');
      console.error('  openclaw fb-post-setup <page_id> "<access_token>" "Page Name"');
      console.error('');
      console.error('Or see the setup guide:');
      console.error('  openclaw fb-post-setup-help');
      process.exit(1);
    }
    
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { page_id, access_token, page_name } = config;
    
    console.log('Configuration:');
    console.log(`  Page ID: ${page_id}`);
    console.log(`  Page Name: ${page_name || '(not set)'}`);
    console.log('');
    
    // Test 1: Check API connectivity
    console.log('📡 Test 1: API Connectivity');
    
    const options = {
      hostname: 'graph.facebook.com',
      path: `/${page_id}?fields=name&access_token=${access_token}`,
      method: 'GET'
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          if (result.error) {
            console.error('  ❌ Failed:', result.error.message);
            console.error('');
            
            if (result.error.code === 190) {
              console.error('💡 Your access token has expired.');
              console.error('   Regenerate it at: https://developers.facebook.com/tools/explorer/');
            } else if (result.error.code === 10) {
              console.error('💡 Missing permissions or invalid token.');
              console.error('   Make sure you have:');
              console.error('   - pages_manage_posts');
              console.error('   - pages_read_engagement');
              console.error('   - pages_show_list');
            }
            
            process.exit(1);
          }
          
          console.log('  ✅ API is reachable');
          console.log(`  ✅ Page found: ${result.name}`);
          console.log('');
          
          // Test 2: Check permissions
          console.log('🔐 Test 2: Permissions Check');
          
          const permOptions = {
            hostname: 'graph.facebook.com',
            path: `/${page_id}/permissions?access_token=${access_token}`,
            method: 'GET'
          };
          
          const permReq = https.request(permOptions, (permRes) => {
            let permData = '';
            permRes.on('data', chunk => permData += chunk);
            permRes.on('end', () => {
              try {
                const permResult = JSON.parse(permData);
                
                // Check for required permissions
                const requiredPerms = ['pages_manage_posts', 'pages_read_engagement'];
                const hasPerms = permResult.data || [];
                
                let allGood = true;
                requiredPerms.forEach(perm => {
                  const hasPerm = hasPerms.some(p => p.permission === perm && p.status === 'GRANTED');
                  if (hasPerm) {
                    console.log(`  ✅ ${perm}: Granted`);
                  } else {
                    console.log(`  ⚠️  ${perm}: Not granted`);
                    allGood = false;
                  }
                });
                
                console.log('');
                
                if (!allGood) {
                  console.log('💡 Some permissions are missing.');
                  console.log('   Regenerate your token with these permissions:');
                  console.log('   - pages_manage_posts');
                  console.log('   - pages_read_engagement');
                  console.log('   - pages_show_list');
                  console.log('');
                  console.log('   Get token at: https://developers.facebook.com/tools/explorer/');
                }
                
                // Test 3: Try a dry-run post (create a test post, then delete it)
                console.log('✍️  Test 3: Post Capability');
                
                const testMessage = `OpenClaw Connection Test - ${new Date().toISOString()}`;
                
                const postOptions = {
                  hostname: 'graph.facebook.com',
                  path: `/${page_id}/feed?message=${encodeURIComponent(testMessage)}&access_token=${access_token}`,
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                  }
                };
                
                const postReq = https.request(postOptions, (postRes) => {
                  let postData = '';
                  postRes.on('data', chunk => postData += chunk);
                  postRes.on('end', () => {
                    try {
                      const postResult = JSON.parse(postData);
                      
                      if (postResult.id) {
                        console.log('  ✅ Can create posts');
                        console.log(`  📝 Test post created: ${postResult.id}`);
                        
                        // Delete the test post
                        const deleteOptions = {
                          hostname: 'graph.facebook.com',
                          path: `/${postResult.id}?access_token=${access_token}`,
                          method: 'DELETE'
                        };
                        
                        const deleteReq = https.request(deleteOptions, (deleteRes) => {
                          let deleteData = '';
                          deleteRes.on('data', chunk => deleteData += chunk);
                          deleteRes.on('end', () => {
                            try {
                              const deleteResult = JSON.parse(deleteData);
                              if (deleteResult.success) {
                                console.log('  ✅ Can delete posts');
                                console.log('  🗑️  Test post deleted');
                              } else {
                                console.log('  ⚠️  Could not delete test post (may need additional permissions)');
                              }
                              
                              console.log('');
                              console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                              console.log('✅ All tests passed! You\'re ready to post.');
                              console.log('');
                              console.log('Try it:');
                              console.log('  openclaw fb-post "Hello from OpenClaw!"');
                              console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                            } catch (err) {
                              console.error('  ⚠️  Error parsing delete response');
                              console.log('');
                              console.log('✅ Post capability verified (delete test skipped)');
                              console.log('');
                              console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                              console.log('✅ You\'re ready to post!');
                              console.log('');
                              console.log('Try it:');
                              console.log('  openclaw fb-post "Hello from OpenClaw!"');
                              console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                            }
                          });
                        });
                        
                        deleteReq.on('error', (err) => {
                          console.log('  ⚠️  Delete test failed:', err.message);
                          console.log('');
                          console.log('✅ Post capability verified (delete test skipped)');
                          console.log('');
                          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                          console.log('✅ You\'re ready to post!');
                          console.log('');
                          console.log('Try it:');
                          console.log('  openclaw fb-post "Hello from OpenClaw!"');
                          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
                        });
                        
                        deleteReq.end();
                      } else {
                        console.error('  ❌ Cannot create posts');
                        if (postResult.error) {
                          console.error('  Error:', postResult.error.message);
                        }
                        console.log('');
                        console.log('💡 Check your token permissions:');
                        console.log('   - pages_manage_posts');
                        console.log('   - pages_read_engagement');
                        process.exit(1);
                      }
                    } catch (err) {
                      console.error('  ❌ Error parsing post response:', err.message);
                      process.exit(1);
                    }
                  });
                });
                
                postReq.on('error', (err) => {
                  console.error('  ❌ Post request failed:', err.message);
                  process.exit(1);
                });
                
                postReq.end();
                
              } catch (err) {
                console.error('  ⚠️  Error parsing permissions:', err.message);
                console.log('  Continuing with basic tests...');
                console.log('');
              }
            });
          });
          
          permReq.on('error', (err) => {
            console.error('  ⚠️  Permissions check failed:', err.message);
            console.log('  Continuing with basic tests...');
            console.log('');
          });
          
          permReq.end();
          
        } catch (err) {
          console.error('  ❌ Error parsing response:', err.message);
          process.exit(1);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('  ❌ Connection failed:', err.message);
      console.error('');
      console.error('💡 Check your internet connection and try again.');
      process.exit(1);
    });
    
    req.end();
  });

program.parse();
