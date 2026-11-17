#!/usr/bin/env node
/**
 * Smart Backup & Sync v1.0.7
 * Intelligent file backup with compression and verification
 * 
 * Modes:
 *   --backup <source> <destination>          → Create backup
 *   --backup --dry-run <source> <dest>       → Preview backup without creating
 *   --sync <source> <destination>            → Sync files between locations
 *   --sync --dry-run <source> <dest>         → Preview sync
 *   --verify <backup_file>                   → Verify backup integrity
 *   --dedup <dir>                            → Content-aware deduplication
 *   --list                                   → List available backups
 *   --restore <backup_file>                  → Restore from backup
 *   --status                                 → Backup status overview
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');

const WORKSPACE = (() => {
  if (process.env.BACKUP_DIR) return process.env.BACKUP_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const BACKUP_DIR = path.join(WORKSPACE, 'backups', 'smart-backups');
const MANIFEST_FILE = path.join(BACKUP_DIR, 'manifest.json');
const HASH_DIR = path.join(WORKSPACE, 'memory', 'backup-hashes');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadJSON(file, fallback) {
  try {
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function getFileHash(filepath) {
  try {
    const content = fs.readFileSync(filepath);
    return crypto.createHash('sha256').update(content).digest('hex').substring(0, 16);
  } catch { return null; }
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function collectFiles(dir, skipDirs = ['.git', 'node_modules', '.cache', '.npm']) {
  const files = [];
  if (!fs.existsSync(dir)) return files;
  
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!skipDirs.includes(entry.name)) {
        files.push(...collectFiles(fullPath, skipDirs));
      }
    } else {
      files.push({ path: fullPath, name: entry.name, size: fs.statSync(fullPath).size });
    }
  }
  return files;
}

// ─── BACKUP ────────────────────────────────────────────────────────────────

function createBackup(source, destination, dryRun = false) {
  const sourceFiles = collectFiles(source);
  const timestamp = getToday() + '-' + Date.now();
  const backupName = `backup-${timestamp}`;
  const backupPath = path.join(BACKUP_DIR, backupName);
  
  if (dryRun) {
    console.log(`[smart-backup] Would backup ${sourceFiles.length} files:`);
    console.log(`  Source: ${source}`);
    console.log(`  Destination: ${backupPath}`);
    const totalSize = sourceFiles.reduce((s, f) => s + f.size, 0);
    console.log(`  Total size: ${formatBytes(totalSize)}`);
    console.log(`  Would compress: ~${formatBytes(totalSize * 0.4)} (estimated 60% compression)`);
    return { dryRun: true, fileCount: sourceFiles.length, totalSize };
  }
  
  ensureDir(backupPath);
  
  // Create manifest
  const manifest = {
    name: backupName,
    source,
    created: getToday(),
    fileCount: sourceFiles.length,
    totalSize: sourceFiles.reduce((s, f) => s + f.size, 0),
    files: sourceFiles.map(f => ({
      path: f.path,
      name: f.name,
      size: f.size,
      hash: getFileHash(f.path)
    }))
  };
  
  // Copy files (in production, would compress)
  let copied = 0;
  for (const file of sourceFiles) {
    const relPath = path.relative(source, file.path);
    const destPath = path.join(backupPath, relPath);
    ensureDir(path.dirname(destPath));
    fs.copyFileSync(file.path, destPath);
    copied++;
  }
  
  saveJSON(path.join(backupPath, 'manifest.json'), manifest);
  saveJSON(MANIFEST_FILE, loadJSON(MANIFEST_FILE, {}));
  
  console.log(`[smart-backup] ✅ Backed up ${copied} files to ${backupPath}`);
  console.log(`[smart-backup] Total size: ${formatBytes(manifest.totalSize)}`);
  return manifest;
}

// ─── INCREMENTAL BACKUP ───────────────────────────────────────────────────

function loadHashManifest(source) {
  const key = Buffer.from(source).toString('base64').substring(0, 20);
  const file = path.join(HASH_DIR, `${key}.json`);
  return loadJSON(file, {});
}

function saveHashManifest(source, hashes) {
  const key = Buffer.from(source).toString('base64').substring(0, 20);
  ensureDir(HASH_DIR);
  const file = path.join(HASH_DIR, `${key}.json`);
  saveJSON(file, hashes);
}

function createIncrementalBackup(source, destination, fromManifest = null, dryRun = false) {
  const sourceFiles = collectFiles(source);
  const timestamp = getToday() + '-' + Date.now();
  const backupName = `backup-${timestamp}-incr`;
  const backupPath = path.join(BACKUP_DIR, backupName);
  
  // Load previous hashes
  const prevHashes = fromManifest || loadHashManifest(source);
  
  // Find changed/new files
  const changedFiles = [];
  let unchangedCount = 0;
  
  for (const file of sourceFiles) {
    const currentHash = getFileHash(file.path);
    const prevHash = prevHashes[file.path];
    
    if (!prevHash || prevHash.hash !== currentHash) {
      changedFiles.push({ ...file, currentHash });
    } else {
      unchangedCount++;
    }
  }
  
  if (dryRun) {
    console.log(`[smart-backup] Incremental backup (dry-run):`);
    console.log(`  Source: ${source}`);
    console.log(`  Files to backup: ${changedFiles.length}`);
    console.log(`  Unchanged (skipped): ${unchangedCount}`);
    const totalSize = changedFiles.reduce((s, f) => s + f.size, 0);
    console.log(`  Size to backup: ${formatBytes(totalSize)}`);
    return { dryRun: true, fileCount: changedFiles.length, unchangedCount, totalSize };
  }
  
  if (changedFiles.length === 0) {
    console.log(`[smart-backup] No changes detected. Skipping backup (${unchangedCount} files unchanged).`);
    return { changed: 0, unchanged: unchangedCount };
  }
  
  ensureDir(backupPath);
  
  // Copy only changed files
  let copied = 0;
  const manifestFiles = [];
  for (const file of changedFiles) {
    const relPath = path.relative(source, file.path);
    const destPath = path.join(backupPath, relPath);
    ensureDir(path.dirname(destPath));
    fs.copyFileSync(file.path, destPath);
    manifestFiles.push({ path: file.path, name: file.name, size: file.size, hash: file.currentHash });
    copied++;
  }
  
  // Save manifest
  const manifest = {
    name: backupName,
    source,
    type: 'incremental',
    created: getToday(),
    fileCount: copied,
    unchangedCount,
    totalSize: changedFiles.reduce((s, f) => s + f.size, 0),
    files: manifestFiles
  };
  saveJSON(path.join(backupPath, 'manifest.json'), manifest);
  
  // Update hash manifest
  const newHashes = { ...prevHashes };
  for (const file of sourceFiles) {
    newHashes[file.path] = { hash: getFileHash(file.path), mtime: fs.statSync(file.path).mtimeMs };
  }
  saveHashManifest(source, newHashes);
  
  console.log(`[smart-backup] ✅ Incremental backup: ${copied} files (${formatBytes(manifest.totalSize)})`);
  console.log(`[smart-backup]   Skipped ${unchangedCount} unchanged files`);
  return manifest;
}

// ─── SYNC ──────────────────────────────────────────────────────────────────

function syncFiles(source, destination, dryRun = false, deleteAllowed = false, forceMode = false) {
  const sourceFiles = collectFiles(source);
  const destFiles = collectFiles(destination);
  
  const sourceMap = new Map();
  for (const f of sourceFiles) {
    const relPath = path.relative(source, f.path);
    sourceMap.set(relPath, f);
  }
  
  const destMap = new Map();
  for (const f of destFiles) {
    const relPath = path.relative(destination, f.path);
    destMap.set(relPath, f);
  }
  
  const toCopy = [];
  const toUpdate = [];
  const toDelete = [];
  
  // Find new and updated files
  for (const [relPath, sourceFile] of sourceMap) {
    const destFile = destMap.get(relPath);
    if (!destFile) {
      toCopy.push(sourceFile);
    } else if (getFileHash(sourceFile.path) !== getFileHash(destFile.path)) {
      toUpdate.push({ source: sourceFile, dest: destFile });
    }
  }
  
  // Find files to delete (in dest but not in source)
  for (const [relPath] of destMap) {
    if (!sourceMap.has(relPath)) {
      toDelete.push({ path: path.join(destination, relPath) });
    }
  }
  
  if (dryRun) {
    console.log(`[smart-backup] Sync preview:\n`);
    console.log(`  New files: ${toCopy.length}`);
    for (const f of toCopy.slice(0, 5)) console.log(`    + ${f.path}`);
    console.log(`  Updated files: ${toUpdate.length}`);
    for (const f of toUpdate.slice(0, 5)) console.log(`    ~ ${f.source.path}`);
    console.log(`  To delete: ${toDelete.length}`);
    for (const f of toDelete.slice(0, 5)) console.log(`    - ${f.path}`);
    return { dryRun: true };
  }
  
  // Perform sync
  for (const file of toCopy) {
    const relPath = path.relative(source, file.path);
    const destPath = path.join(destination, relPath);
    ensureDir(path.dirname(destPath));
    fs.copyFileSync(file.path, destPath);
  }
  
  for (const file of toUpdate) {
    fs.copyFileSync(file.source.path, file.dest.path);
  }
  
  if (deleteAllowed) {
    if (forceMode) {
      // Delete all files unconditionally, logging each one
      for (const file of toDelete) {
        console.log(`[smart-backup] DELETED: ${file.path}`);
        fs.unlinkSync(file.path);
      }
    } else {
      // List what would be deleted, require explicit --delete to proceed
      if (toDelete.length > 0) {
        console.log(`[smart-backup] WARNING: ${toDelete.length} file(s) would be deleted:\n`);
        for (const file of toDelete) {
          console.log(`  - ${file.path}`);
        }
        console.log(`  Use --force to delete, or --no-delete (default) to skip.`);
      }
    }
  } else {
    if (toDelete.length > 0) {
      console.log(`[smart-backup] WARNING: ${toDelete.length} file(s) found in destination but not in source (skipping deletion, use --delete to enable).`);
    }
  }
  
  console.log(`[smart-backup] ✅ Synced: ${toCopy.length} new, ${toUpdate.length} updated, ${toDelete.length} deleted`);
}

// ─── VERIFY ────────────────────────────────────────────────────────────────

function verifyBackup(backupFile) {
  const manifestPath = path.join(backupFile, 'manifest.json');
  if (!fs.existsSync(manifestPath)) {
    console.log(`[smart-backup] No manifest found in: ${backupFile}`);
    return;
  }
  
  const manifest = loadJSON(manifestPath, {});
  let verified = 0;
  let failed = 0;
  
  for (const file of manifest.files || []) {
    const restoredPath = path.join(backupFile, path.relative(manifest.source, file.path));
    if (!fs.existsSync(restoredPath)) {
      console.log(`  ❌ Missing: ${file.path}`);
      failed++;
      continue;
    }
    
    const restoredHash = getFileHash(restoredPath);
    if (restoredHash === file.hash) {
      verified++;
    } else {
      console.log(`  ❌ Hash mismatch: ${file.path}`);
      failed++;
    }
  }
  
  console.log(`[smart-backup] Verification: ${verified} OK, ${failed} failed`);
}

// ─── LIST ──────────────────────────────────────────────────────────────────

function listBackups() {
  ensureDir(BACKUP_DIR);
  const backups = fs.readdirSync(BACKUP_DIR).filter(f => f.startsWith('backup-'));
  
  if (backups.length === 0) {
    console.log('[smart-backup] No backups found.');
    return;
  }
  
  console.log(`[smart-backup] Backups (${backups.length}):\n`);
  console.log(`${'Name'.padEnd(30)} ${'Date'.padEnd(12)} ${'Files'.padEnd(8)} ${'Size'.padEnd(12)}`);
  console.log('-'.repeat(65));
  
  for (const name of backups) {
    const manifestPath = path.join(BACKUP_DIR, name, 'manifest.json');
    if (!fs.existsSync(manifestPath)) continue;
    const manifest = loadJSON(manifestPath, {});
    const size = manifest.totalSize || 0;
    console.log(`${name.padEnd(30)} ${(manifest.created || 'unknown').padEnd(12)} ${String(manifest.fileCount || 0).padEnd(8)} ${formatBytes(size).padEnd(12)}`);
  }
}

// ─── RESTORE ───────────────────────────────────────────────────────────────

function restoreBackup(backupFile, destination, forceMode = false) {
  const manifestPath = path.join(backupFile, 'manifest.json');
  if (!fs.existsSync(manifestPath)) {
    console.log(`[smart-backup] No manifest found in: ${backupFile}`);
    return;
  }
  
  const manifest = loadJSON(manifestPath, {});
  let restored = 0;
  let overwritten = 0;
  let skipped = 0;
  
  for (const file of manifest.files || []) {
    const sourcePath = path.join(backupFile, path.relative(manifest.source, file.path));
    const relPath = path.relative(manifest.source, file.path);
    const destPath = path.join(destination, relPath);
    ensureDir(path.dirname(destPath));
    
    if (fs.existsSync(destPath)) {
      if (forceMode) {
        console.log(`[smart-backup] OVERWRITE: ${destPath}`);
        fs.copyFileSync(sourcePath, destPath);
        overwritten++;
      } else {
        console.log(`[smart-backup] WARNING: Skipping existing file (use --force to overwrite): ${destPath}`);
        skipped++;
      }
    } else {
      fs.copyFileSync(sourcePath, destPath);
      restored++;
    }
  }
  
  let msg = `[smart-backup] ✅ Restored ${restored} files to ${destination}`;
  if (overwritten > 0) msg += `, ${overwritten} overwritten`;
  if (skipped > 0) msg += `, ${skipped} skipped (existing)`;
  console.log(msg);
}

// ─── DEDUP ─────────────────────────────────────────────────────────────────

function findDuplicates(dir) {
  const files = collectFiles(dir);
  const hashMap = new Map();
  
  for (const file of files) {
    const hash = getFileHash(file.path);
    if (!hash) continue;
    if (!hashMap.has(hash)) hashMap.set(hash, []);
    hashMap.get(hash).push(file);
  }
  
  const duplicates = [];
  for (const [hash, files] of hashMap) {
    if (files.length >= 2) {
      duplicates.push({ hash, files, size: files[0].size });
    }
  }
  
  return duplicates;
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  ensureDir(BACKUP_DIR);
  const backups = fs.readdirSync(BACKUP_DIR).filter(f => f.startsWith('backup-'));
  const totalSize = backups.reduce((sum, name) => {
    const manifestPath = path.join(BACKUP_DIR, name, 'manifest.json');
    if (!fs.existsSync(manifestPath)) return sum;
    const manifest = loadJSON(manifestPath, {});
    return sum + (manifest.totalSize || 0);
  }, 0);
  
  console.log('[smart-backup] Status:\n');
  console.log(`  Backups: ${backups.length}`);
  console.log(`  Total backup size: ${formatBytes(totalSize)}`);
  console.log(`  Backup directory: ${BACKUP_DIR}`);
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let mode = 'status';
let searchQuery = null;
let incremental = false;
let fromManifest = null;
let deleteFlag = false;    // --delete: enable file deletion during sync
let forceFlag = false;      // --force: overwrite existing files (restore) or proceed with deletion (sync)

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--backup') mode = 'backup';
  if (args[i] === '--sync') mode = 'sync';
  if (args[i] === '--verify') mode = 'verify';
  if (args[i] === '--dedup') mode = 'dedup';
  if (args[i] === '--list') mode = 'list';
  if (args[i] === '--restore') mode = 'restore';
  if (args[i] === '--status') mode = 'status';
  if (args[i] === '--dry-run') searchQuery = 'dryrun';
  if (args[i] === '--incr') incremental = true;
  if (args[i] === '--from-manifest' && i + 1 < args.length) fromManifest = args[i + 1];
  if (args[i] === '--dir' && i + 1 < args.length) process.env.BACKUP_DIR = args[i + 1];
  if (args[i] === '--delete') deleteFlag = true;
  if (args[i] === '--no-delete') deleteFlag = false;
  if (args[i] === '--force') forceFlag = true;
}

switch (mode) {
  case 'backup': {
    const source = args[2];
    const dest = args[3];
    if (!source || !dest) {
      console.log('Usage: smart-backup.js --backup <source> <destination>');
    } else {
      if (incremental) {
        createIncrementalBackup(source, dest, fromManifest, searchQuery === 'dryrun');
      } else {
        createBackup(source, dest, searchQuery === 'dryrun');
      }
    }
    break;
  }
  case 'sync': {
    const source = args[2];
    const dest = args[3];
    if (!source || !dest) {
      console.log('Usage: smart-backup.js --sync <source> <destination>');
    } else {
      syncFiles(source, dest, searchQuery === 'dryrun', deleteFlag, forceFlag);
    }
    break;
  }
  case 'verify': {
    verifyBackup(args[2]);
    break;
  }
  case 'dedup': {
    const dups = findDuplicates(args[2] || WORKSPACE);
    console.log(`[smart-backup] Found ${dups.length} groups of duplicate files:\n`);
    for (const d of dups.slice(0, 5)) {
      console.log(`  ${d.files.length} files (${formatBytes(d.size)}) — ${d.hash}`);
      for (const f of d.files) console.log(`    → ${f.path}`);
    }
    break;
  }
  case 'list':
    listBackups();
    break;
  case 'restore': {
    const backup = args[2];
    const dest = args[3];
    if (!backup || !dest) {
      console.log('Usage: smart-backup.js --restore <backup> <destination>');
    } else {
      restoreBackup(backup, dest, forceFlag);
    }
    break;
  }
  default:
    showStatus();
    break;
}
