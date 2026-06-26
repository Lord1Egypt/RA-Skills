const fs = require('fs');
const path = require('path');

const FOLDERS_FILE = path.join(__dirname, 'folders.json');

function loadFolders() {
  if (!fs.existsSync(FOLDERS_FILE)) return [];
  return JSON.parse(fs.readFileSync(FOLDERS_FILE, 'utf8'));
}

function saveFolders(folders) {
  fs.writeFileSync(FOLDERS_FILE, JSON.stringify(folders, null, 2));
}

const action = process.argv[2];

if (action === 'add') {
  const name = process.argv[3];
  const id = process.argv[4];
  if (!name || !id) {
    console.error("Usage: node folders.js add \"Folder Name\" <ID>");
    process.exit(1);
  }
  const folders = loadFolders();
  if (folders.find(f => f.id === id)) {
    console.log(`Folder ${id} already exists.`);
    process.exit(0);
  }
  const isDefault = folders.length === 0; // First folder is default
  folders.push({ name, id, isDefault });
  saveFolders(folders);
  console.log(`Added folder: ${name} (${id}). Default: ${isDefault}`);
} else if (action === 'list') {
  const folders = loadFolders();
  console.log(JSON.stringify(folders, null, 2));
} else if (action === 'default') {
  const idOrName = process.argv[3];
  const folders = loadFolders();
  let found = false;
  for (let f of folders) {
    if (f.id === idOrName || f.name === idOrName) {
      f.isDefault = true;
      found = true;
      console.log(`Set ${f.name} as default.`);
    } else {
      f.isDefault = false;
    }
  }
  if (!found) console.log("Folder not found.");
  else saveFolders(folders);
} else if (action === 'get-default') {
  const folders = loadFolders();
  const def = folders.find(f => f.isDefault) || folders[0];
  if (def) console.log(def.id);
  else console.log("");
} else if (action === 'get') {
  const idOrName = process.argv[3];
  const folders = loadFolders();
  const f = folders.find(f => f.id === idOrName || f.name.toLowerCase() === idOrName.toLowerCase());
  if (f) console.log(f.id);
  else console.log("");
}
