const fs = require('fs').promises;
const path = require('path');
const { google } = require('googleapis');
const config = require('./config.js');

class BloggerAuth {
  constructor() {
    this.oAuth2Client = null;
  }

  async loadCredentials() {
    try {
      const content = await fs.readFile(config.credentialsPath);
      const credentials = JSON.parse(content);
      
      const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;
      this.oAuth2Client = new google.auth.OAuth2(
        client_id,
        client_secret,
        redirect_uris[0] || config.redirectUri
      );
      
      console.log('✓ Credentials loaded successfully');
      return this.oAuth2Client;
    } catch (error) {
      console.error('✗ Error loading credentials:', error.message);
      throw error;
    }
  }

  async loadToken() {
    try {
      const token = await fs.readFile(config.tokenPath);
      this.oAuth2Client.setCredentials(JSON.parse(token));
      console.log('✓ Token loaded successfully');
      return true;
    } catch (error) {
      console.log('ℹ No existing token found, need to authorize');
      return false;
    }
  }

  async getAuthUrl() {
    if (!this.oAuth2Client) {
      await this.loadCredentials();
    }
    
    const authUrl = this.oAuth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: config.scopes,
      prompt: 'consent'
    });
    
    return authUrl;
  }

  async getTokenFromCode(code) {
    if (!this.oAuth2Client) {
      await this.loadCredentials();
    }
    
    const { tokens } = await this.oAuth2Client.getToken(code);
    this.oAuth2Client.setCredentials(tokens);
    
    // Save token for future use
    await fs.writeFile(config.tokenPath, JSON.stringify(tokens));
    console.log('✓ Token saved to', config.tokenPath);
    
    return tokens;
  }

  async authorize() {
    await this.loadCredentials();
    
    const hasToken = await this.loadToken();
    if (hasToken) {
      return this.oAuth2Client;
    }
    
    console.log('\n=== Authorization Required ===');
    console.log('1. Open this URL in your browser:');
    const authUrl = await this.getAuthUrl();
    console.log(authUrl);
    console.log('\n2. Authorize the application');
    console.log('3. Copy the authorization code from the URL');
    console.log('4. Run: node auth.js --code YOUR_AUTHORIZATION_CODE');
    console.log('=============================\n');
    
    return null;
  }

  async authorizeWithCode(code) {
    await this.loadCredentials();
    await this.getTokenFromCode(code);
    console.log('✓ Authorization complete!');
    return this.oAuth2Client;
  }
}

// Command line interface
if (require.main === module) {
  const auth = new BloggerAuth();
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log('Usage:');
    console.log('  node auth.js                    - Start authorization flow');
    console.log('  node auth.js --code CODE        - Complete authorization with code');
    console.log('  node auth.js --check            - Check current authorization');
    console.log('  node auth.js --logout           - Remove token');
    process.exit(0);
  }
  
  if (args.includes('--logout')) {
    fs.unlink(config.tokenPath).then(() => {
      console.log('✓ Token removed');
    }).catch(() => {
      console.log('ℹ No token to remove');
    });
    process.exit(0);
  }
  
  if (args.includes('--check')) {
    auth.loadCredentials().then(() => {
      return auth.loadToken();
    }).then(hasToken => {
      if (hasToken) {
        console.log('✓ Authorized and ready to use');
      } else {
        console.log('✗ Not authorized, run: node auth.js');
      }
    }).catch(error => {
      console.error('Error:', error.message);
    });
    process.exit(0);
  }
  
  const codeIndex = args.indexOf('--code');
  if (codeIndex !== -1 && args[codeIndex + 1]) {
    const code = args[codeIndex + 1];
    auth.authorizeWithCode(code).catch(error => {
      console.error('Authorization failed:', error.message);
      process.exit(1);
    });
  } else {
    auth.authorize().catch(error => {
      console.error('Error:', error.message);
      process.exit(1);
    });
  }
}

module.exports = BloggerAuth;