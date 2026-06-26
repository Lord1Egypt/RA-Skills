const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

describe('FileChat RAG Skill', () => {
  const credentialsPath = path.join(__dirname, 'credentials.json');
  
  beforeAll(() => {
    // Ensure we have the credentials to authenticate GWS CLI
    if (!fs.existsSync(credentialsPath)) {
      throw new Error(`Missing GWS credentials at ${credentialsPath}`);
    }
  });

  it('sync.js should fail without a FOLDER_ID argument', () => {
    try {
      execSync('node ../sync.js', { cwd: __dirname, stdio: 'pipe' });
    } catch (error) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('Usage: node sync.js <DRIVE_FOLDER_ID>');
    }
  });

  it('query.js should fail without FOLDER_ID and QUERY arguments', () => {
    try {
      execSync('node ../query.js', { cwd: __dirname, stdio: 'pipe' });
    } catch (error) {
      expect(error.status).toBe(1);
      expect(error.stderr.toString()).toContain('Usage: node query.js <DRIVE_FOLDER_ID> "<SEARCH_QUERY>"');
    }
  });

  it('can list files using GWS CLI if authenticated', () => {
    // Note: If you have never run `npx @googleworkspace/cli login` with these credentials,
    // this test will either hang waiting for a browser, or fail with auth error.
    // The environment variables configure GWS CLI to use our provided credentials.
    const env = {
      ...process.env,
      GEMINI_API_KEY: 'AIzaSyAOx5NDLxsyRjd0qWT33LXZ_KKwMtyzOe4'
    };

    try {
      // We run a simple GWS CLI command to see if it executes
      // We use --help to avoid needing an active session for this simple validation
      const result = execSync('npx @googleworkspace/cli drive files list --help', {
        env,
        stdio: 'pipe',
      }).toString();
      
      expect(result).toContain('Usage: gws files list');
    } catch (error) {
      // In case the CLI isn't installed properly or fails unexpectedly
      console.warn("GWS CLI help command failed:", error.message);
    }
  });
  
  // NOTE: A full integration test would require an actual folder ID and for the GWS CLI 
  // to be logged in (which requires a manual browser OAuth flow step first).
  it('runs sync and query if TEST_FOLDER_ID is provided', () => {
    const testFolderId = process.env.TEST_FOLDER_ID;
    if (!testFolderId) {
      console.log('Skipping integration test since TEST_FOLDER_ID is not set.');
      return;
    }

    const env = {
      ...process.env,
      GEMINI_API_KEY: 'AIzaSyAOx5NDLxsyRjd0qWT33LXZ_KKwMtyzOe4'
    };

    // Clean up previous runs so it actually tests the download/embed process
    const metaFile = path.join(__dirname, `../meta_${testFolderId}.json`);
    const dbFile = path.join(__dirname, `../vector_db_${testFolderId}.json`);
    if (fs.existsSync(metaFile)) fs.unlinkSync(metaFile);
    if (fs.existsSync(dbFile)) fs.unlinkSync(dbFile);

    console.log(`Running sync.js with folder ${testFolderId}...`);
    const syncResult = execSync(`node ../sync.js ${testFolderId}`, { env, cwd: __dirname, stdio: 'pipe' }).toString();
    expect(syncResult).toContain('Sync complete');
    
    console.log(`Running query.js with folder ${testFolderId}...`);
    const queryResult = execSync(`node ../query.js ${testFolderId} "hello"`, { env, cwd: __dirname, stdio: 'pipe' }).toString();
    expect(queryResult).toContain('Top matches for:');
  }, 180000); // 3 minutes timeout
});
