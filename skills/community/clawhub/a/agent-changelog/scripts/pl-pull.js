#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const WORKSPACE_CFG = path.join(WORKSPACE, '.agent-changelog.json');
const BASE_URL = 'https://api.promptlayer.com';

function loadWorkspaceConfig() {
  try {
    return JSON.parse(fs.readFileSync(WORKSPACE_CFG, 'utf8'));
  } catch {
    return {};
  }
}

function saveWorkspaceConfig(config) {
  fs.writeFileSync(WORKSPACE_CFG, JSON.stringify(config, null, 2) + '\n');
}

function listFiles(rootDir) {
  const results = [];
  const stack = [rootDir];
  while (stack.length) {
    const current = stack.pop();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const abs = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(abs);
      } else if (entry.isFile()) {
        const rel = path.relative(rootDir, abs).split(path.sep).join('/');
        results.push(rel);
      }
    }
  }
  return results;
}


function unzipToDir(zipBuffer) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agent-changelog-'));
  const zipPath = path.join(tmpDir, 'snapshot.zip');
  const extractDir = path.join(tmpDir, 'extract');
  fs.writeFileSync(zipPath, zipBuffer);
  fs.mkdirSync(extractDir, { recursive: true });
  if (process.platform === 'win32') {
    const psZip = zipPath.replace(/'/g, "''");
    const psDest = extractDir.replace(/'/g, "''");
    execSync(`powershell -NoProfile -Command "Expand-Archive -LiteralPath '${psZip}' -DestinationPath '${psDest}' -Force"`);
  } else {
    execSync(`unzip -o ${JSON.stringify(zipPath)} -d ${JSON.stringify(extractDir)}`);
  }
  // PromptLayer wraps files under a root_path prefix (e.g. .openclaw/).
  // If there's a single top-level directory, treat its contents as the root.
  const topEntries = fs.readdirSync(extractDir, { withFileTypes: true });
  if (topEntries.length === 1 && topEntries[0].isDirectory()) {
    return { tmpDir, extractDir: path.join(extractDir, topEntries[0].name) };
  }
  return { tmpDir, extractDir };
}

function diffAndApply(extractDir) {
  const remoteFiles = listFiles(extractDir);
  const remoteSet = new Set(remoteFiles);
  const trackedFiles = execSync('git ls-files', { cwd: WORKSPACE })
    .toString().trim().split('\n').filter(Boolean);

  const changed = [];
  const added = [];

  // Check for changed or added files
  for (const filePath of remoteFiles) {
    const src = path.join(extractDir, filePath);
    const dest = path.join(WORKSPACE, filePath);
    const srcContent = fs.readFileSync(src);

    if (!fs.existsSync(dest)) {
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      fs.copyFileSync(src, dest);
      added.push(filePath);
    } else {
      const destContent = fs.readFileSync(dest);
      if (!srcContent.equals(destContent)) {
        fs.copyFileSync(src, dest);
        changed.push(filePath);
      }
    }
  }

  // Non-destructive: never remove local-only files.
  // Only PL additions and modifications are applied.

  return { all: remoteFiles, changed, added };
}

async function main() {
  const args = process.argv.slice(2);
  let version = null;
  let label = null;
  let connectIdentifier = null;
  let reason = '';
  let force = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--version' && args[i + 1]) version = args[++i];
    if (args[i] === '--label' && args[i + 1]) label = args[++i];
    if (args[i] === '--connect' && args[i + 1]) connectIdentifier = args[++i];
    if (args[i] === '--reason' && args[i + 1]) reason = args[++i];
    if (args[i] === '--force') force = true;
  }

  const workspaceConfig = loadWorkspaceConfig();
  const pl = workspaceConfig.promptlayer || {};
  const apiKeyValue = process.env.PROMPTLAYER_API_KEY || '';

  if (!apiKeyValue) {
    console.error('Missing API key. Set PROMPTLAYER_API_KEY in your environment.');
    process.exit(1);
  }

  const identifier = connectIdentifier || pl?.collectionId;
  if (!identifier) {
    console.error('No PromptLayer collection configured. Run setup first.');
    process.exit(1);
  }

  const dirty = execSync('git status --porcelain', { cwd: WORKSPACE }).toString().trim();
  if (dirty && !force) {
    console.error('Local changes detected. Confirm overwrite and re-run with --force.');
    process.exit(1);
  }

  const params = new URLSearchParams();
  if (version) params.set('version', version);
  if (label) params.set('label', label);
  const query = params.toString() ? `?${params}` : '';

  const collectionUrl = `${BASE_URL}/api/public/v2/skill-collections/${encodeURIComponent(identifier)}`;

  const metaRes = await fetch(`${collectionUrl}${query}`, { headers: { 'X-API-KEY': apiKeyValue } });
  if (!metaRes.ok) {
    const err = await metaRes.text();
    console.error(`PromptLayer API error ${metaRes.status}: ${err}`);
    process.exit(1);
  }
  const { skill_collection, version: versionInfo } = await metaRes.json();
  const versionNumber = versionInfo?.number ?? 'latest';
  const versionLabel = label || versionInfo?.release_label || '';

  const zipParams = new URLSearchParams(params);
  zipParams.set('format', 'zip');
  const zipRes = await fetch(`${collectionUrl}?${zipParams}`, { headers: { 'X-API-KEY': apiKeyValue } });
  if (!zipRes.ok) {
    const err = await zipRes.text();
    console.error(`PromptLayer API error ${zipRes.status}: ${err}`);
    process.exit(1);
  }
  const outerZipBuffer = Buffer.from(await zipRes.arrayBuffer());
  let tmpDir;
  try {
    const extracted = unzipToDir(outerZipBuffer);
    tmpDir = extracted.tmpDir;
    const { all: snapshotFiles, changed, added } = diffAndApply(extracted.extractDir);

    if (connectIdentifier) {
      workspaceConfig.promptlayer = {
        enabled: true,
        skillName: skill_collection.name,
        collectionId: skill_collection.id,
        provider: skill_collection.provider || 'openclaw',
      };
      saveWorkspaceConfig(workspaceConfig);
      console.log(`✅ Connected "${skill_collection.name}" (${skill_collection.id}) — pulled ${snapshotFiles.length} files from v${versionNumber}`);
      // Always report what changed
      const touchedConnect = [...changed, ...added];
      if (touchedConnect.length > 0) {
        const parts = [];
        if (changed.length) parts.push(`${changed.length} modified`);
        if (added.length) parts.push(`${added.length} added`);
        console.log(`\n📋 Changes from v${versionNumber}: ${parts.join(', ')}`);
        if (changed.length) changed.forEach(f => console.log(`  M ${f}`));
        if (added.length) added.forEach(f => console.log(`  A ${f}`));
      } else {
        console.log(`\n✓ All files already match v${versionNumber}`);
      }
      return;
    }

    const touchedFiles = [...changed, ...added];
    if (touchedFiles.length === 0) {
      console.log('✓ Already up to date');
      return;
    }

    // Stage only the files that changed
    for (const filePath of [...changed, ...added]) {
      try {
        execSync(`git add ${JSON.stringify(filePath)}`, { cwd: WORKSPACE });
      } catch { /* skip unstage-able paths */ }
    }
    // Read actor from .version-context
    let actor = 'skill invocation', actorId = 'skill invocation', channel = 'unknown';
    try {
      const ctx = JSON.parse(fs.readFileSync(path.join(WORKSPACE, '.version-context'), 'utf8'));
      actor = ctx.user || actor;
      actorId = ctx.userId || actorId;
      channel = ctx.channel || channel;
    } catch { /* no active context */ }

    const entry = {
      ts: Date.now(),
      user: actor,
      userId: actorId,
      channel,
      action: 'pl-pull',
      target: String(versionNumber),
      from: versionLabel,
      reason,
      files: touchedFiles,
    };

    fs.appendFileSync(path.join(WORKSPACE, 'pending_commits.jsonl'), JSON.stringify(entry) + '\n');

    const versionStr = versionLabel ? `v${versionNumber} (${versionLabel})` : `v${versionNumber}`;
    const parts = [];
    if (changed.length) parts.push(`${changed.length} modified`);
    if (added.length) parts.push(`${added.length} added`);
    console.log(`⬇️  **Pulled** ${versionStr} — ${parts.join(', ')}`);
    if (changed.length) changed.forEach(f => console.log(`  M ${f}`));
    if (added.length) added.forEach(f => console.log(`  A ${f}`));
    console.log(`_by ${actor}_`);
    console.log(`Commit with \`/agent-changelog commit\``);
  } finally {
    if (tmpDir) fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
