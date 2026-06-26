const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const FOLDERS_FILE = path.join(__dirname, 'folders.json');

if (!fs.existsSync(FOLDERS_FILE)) {
  console.log("No folders configured. Run `node folders.js add ...` first.");
  process.exit(0);
}

const folders = JSON.parse(fs.readFileSync(FOLDERS_FILE, 'utf8'));

for (let folder of folders) {
  console.log(`Starting sync for ${folder.name} (${folder.id})...`);
  try {
    execSync(`node sync.js ${folder.id}`, { stdio: 'inherit' });
  } catch(e) {
    console.error(`Failed to sync ${folder.name}:`, e.message);
  }
}
console.log("All folders synced successfully.");
