#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const IMPORT_STATEMENT = "import '@beyondcorp/beyond-ui/dist/styles.css';";

function log(message) {
  console.log(`[beyond-ui-helper] ${message}`);
}

function main() {
  const entryArg = process.argv[2];
  if (!entryArg) {
    console.error('Usage: add-css-import.js <path-to-entry-file>');
    process.exit(1);
  }

  const entryPath = path.resolve(process.cwd(), entryArg);
  if (!fs.existsSync(entryPath)) {
    console.error(`Entry file not found: ${entryPath}`);
    process.exit(1);
  }

  const fileContents = fs.readFileSync(entryPath, 'utf8');
  if (fileContents.includes(IMPORT_STATEMENT)) {
    log('CSS import already present. No changes made.');
    return;
  }

  const updated = `${IMPORT_STATEMENT}\n${fileContents}`;
  fs.writeFileSync(entryPath, updated, 'utf8');
  log(`Prepended Beyond-UI CSS import to ${entryPath}`);
}

main();
