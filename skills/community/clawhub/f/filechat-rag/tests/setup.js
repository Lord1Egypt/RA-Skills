const { execSync } = require('child_process');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

const credentialsPath = path.join(__dirname, 'credentials.json');
const credentialsStr = fs.readFileSync(credentialsPath, 'utf8');
const credentials = JSON.parse(credentialsStr);

const env = {
  ...process.env,
  GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE: credentialsPath,
  GOOGLE_WORKSPACE_CLI_CLIENT_ID: credentials.installed.client_id,
  GOOGLE_WORKSPACE_CLI_CLIENT_SECRET: credentials.installed.client_secret,
  GEMINI_API_KEY: 'AIzaSyAOx5NDLxsyRjd0qWT33LXZ_KKwMtyzOe4'
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function main() {
  console.log('Checking GWS authentication status...');
  try {
    const statusOutput = execSync('npx @googleworkspace/cli auth status', { env, encoding: 'utf-8' });
    const status = JSON.parse(statusOutput);

    if (!status.has_refresh_token) {
      console.log('\\n--- GWS CLI Authentication Required ---');
      console.log('We need to authenticate the Google Workspace CLI first.');
      console.log('This will try to open a browser window. If it fails, please copy the URL printed below.');
      console.log('Please log in with your Google account, and grant the requested Drive permissions.');
      console.log('Once you are redirected to http://localhost..., copy the FULL URL from the browser address bar.\\n');
      
      // We run the login process interactively. 
      // It might try to spin up a local server, or we might just need to paste the code/URL
      try {
        // We use stdio: 'inherit' so the user can interact if gws prompts them
        execSync('npx @googleworkspace/cli auth login --services drive', { env, stdio: 'inherit' });
        console.log('\\nAuthentication completed successfully!');
      } catch (e) {
        console.error('Authentication failed:', e.message);
        process.exit(1);
      }
    } else {
      console.log('GWS CLI is already authenticated.');
    }

    console.log('\\n--- Test Configuration ---');
    const folderId = await askQuestion('Please enter the Google Drive Folder ID you want to test with: ');
    
    if (!folderId) {
      console.error('Folder ID is required for testing.');
      process.exit(1);
    }

    console.log(`\\nRunning tests with Folder ID: ${folderId}`);
    
    // Run Jest tests, passing the folder ID as an env var
    const testEnv = { ...env, TEST_FOLDER_ID: folderId };
    try {
      execSync('npx jest tests/skill.test.js --runInBand', { env: testEnv, stdio: 'inherit' });
    } catch (e) {
      // Jest will print the failure details, so we just exit with an error code
      process.exit(1);
    }
  } catch (error) {
    console.error('Setup failed:', error.message);
    process.exit(1);
  } finally {
    rl.close();
  }
}

main();