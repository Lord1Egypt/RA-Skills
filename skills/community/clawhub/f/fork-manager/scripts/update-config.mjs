#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(scriptDir, '..');

function usage() {
  console.error(`Usage:
  node scripts/update-config.mjs --repo-name <name> [--dry-run] [--check]
  node scripts/update-config.mjs --config <path> [--dry-run] [--check]

Options:
  --repo-name <name>  Uses repos/<name>/config.json relative to this skill.
  --config <path>    Uses an explicit config.json path.
  --author <author>  GitHub PR author filter. Defaults to the owner in config.fork, then @me.
  --dry-run          Print the updated config without writing it.
  --check            Exit 1 if the config would change.
`);
}

function parseArgs(argv) {
  const args = { dryRun: false, check: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--repo-name') args.repoName = argv[++i];
    else if (arg === '--config') args.configPath = argv[++i];
    else if (arg === '--author') args.author = argv[++i];
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--check') args.check = true;
    else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return args;
}

function readJson(filePath) {
  return JSON.parse(readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, value) {
  writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function ghJson(args) {
  const stdout = execFileSync('gh', args, { encoding: 'utf8' });
  return JSON.parse(stdout);
}

function ensureObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function noteEntry(pr, branch, status) {
  const entry = {
    title: pr.title ?? '',
    branch,
    detectedAt: new Date().toISOString(),
  };
  if (status === 'merged' && pr.mergedAt) entry.mergedAt = pr.mergedAt;
  if (status === 'closed' && pr.closedAt) entry.closedAt = pr.closedAt;
  if (status === 'closed') entry.reviewStatus = 'pending';
  return entry;
}

function viewClosedPr(repo, number) {
  return ghJson([
    'pr',
    'view',
    String(number),
    '--repo',
    repo,
    '--json',
    'number,title,state,mergedAt,closedAt,headRefName',
  ]);
}

function reconcileConfig(config) {
  if (!config.repo) {
    throw new Error('config.repo is required');
  }

  const forkOwner = typeof config.fork === 'string' ? config.fork.split('/')[0] : undefined;
  const author = args.author ?? forkOwner ?? '@me';

  const openPrs = ghJson([
    'pr',
    'list',
    '--state',
    'open',
    '--author',
    author,
    '--repo',
    config.repo,
    '--json',
    'number,title,headRefName,state',
    '--limit',
    '200',
  ]);

  const next = structuredClone(config);
  next.notes = ensureObject(next.notes);
  next.notes.mergedUpstream = ensureObject(next.notes.mergedUpstream);
  next.notes.closedWithoutMerge = ensureObject(next.notes.closedWithoutMerge);
  next.notes.droppedPatches = ensureObject(next.notes.droppedPatches);
  next.notes.conflictBranches = ensureObject(next.notes.conflictBranches);
  next.localPatches = ensureObject(next.localPatches);

  const existingBranches = ensureObject(next.prBranches);
  const existingOpen = new Set((next.openPRs ?? []).map(Number));
  const openByNumber = new Map(openPrs.map(pr => [Number(pr.number), pr]));
  const localPatchByOriginalPr = new Map();

  for (const [patchBranch, patch] of Object.entries(next.localPatches)) {
    if (patch && typeof patch === 'object' && patch.originalPR !== undefined) {
      localPatchByOriginalPr.set(Number(patch.originalPR), patchBranch);
    }
  }

  const actions = {
    added: [],
    updatedBranches: [],
    restoredFromNotes: [],
    promotedFromLocalPatches: [],
    merged: [],
    closedWithoutMerge: [],
    unchanged: [],
  };

  const nextBranches = {};

  for (const pr of openPrs.sort((a, b) => Number(a.number) - Number(b.number))) {
    const number = Number(pr.number);
    const key = String(number);
    const previousBranch = existingBranches[key];
    nextBranches[key] = pr.headRefName;

    if (!existingOpen.has(number)) {
      actions.added.push({ number, branch: pr.headRefName, title: pr.title });
    } else if (previousBranch !== pr.headRefName) {
      actions.updatedBranches.push({
        number,
        oldBranch: previousBranch,
        newBranch: pr.headRefName,
      });
    } else {
      actions.unchanged.push({ number, branch: pr.headRefName });
    }

    if (next.notes.closedWithoutMerge[key] || next.notes.droppedPatches[key]) {
      delete next.notes.closedWithoutMerge[key];
      delete next.notes.droppedPatches[key];
      actions.restoredFromNotes.push({ number, branch: pr.headRefName });
    }

    const localPatchBranch = localPatchByOriginalPr.get(number);
    if (localPatchBranch) {
      delete next.localPatches[localPatchBranch];
      actions.promotedFromLocalPatches.push({
        number,
        branch: pr.headRefName,
        localPatchBranch,
      });
    }
  }

  for (const number of [...existingOpen].sort((a, b) => a - b)) {
    if (openByNumber.has(number)) continue;

    const key = String(number);
    const branch = existingBranches[key];
    const pr = viewClosedPr(config.repo, number);

    if (pr.state === 'MERGED' || pr.mergedAt) {
      next.notes.mergedUpstream[key] = noteEntry(pr, branch, 'merged');
      delete next.notes.closedWithoutMerge[key];
      actions.merged.push({ number, branch, title: pr.title, mergedAt: pr.mergedAt });
    } else {
      next.notes.closedWithoutMerge[key] = noteEntry(pr, branch, 'closed');
      actions.closedWithoutMerge.push({
        number,
        branch,
        title: pr.title,
        closedAt: pr.closedAt,
      });
    }
  }

  next.openPRs = Object.keys(nextBranches).map(Number).sort((a, b) => a - b);
  next.prBranches = Object.fromEntries(
    next.openPRs.map(number => [String(number), nextBranches[String(number)]])
  );

  return { next, actions };
}

function summarize(actions, changed, dryRun, check) {
  const lines = [];
  lines.push(`update-config: ${changed ? 'changes detected' : 'config already current'}`);
  if (dryRun) lines.push('mode: dry-run (no files written)');
  if (check) lines.push('mode: check');

  for (const [label, items] of Object.entries(actions)) {
    if (!items.length || label === 'unchanged') continue;
    lines.push(`${label}:`);
    for (const item of items) {
      const number = item.number ? `#${item.number}` : '';
      const branch = item.branch ?? item.newBranch ?? '';
      const suffix = item.oldBranch ? ` (${item.oldBranch} -> ${item.newBranch})` : '';
      lines.push(`  - ${number} ${branch}${suffix}`.trimEnd());
    }
  }

  lines.push(`tracked open PRs: ${actions.unchanged.length + actions.added.length + actions.updatedBranches.length}`);
  return lines.join('\n');
}

let args;
try {
  args = parseArgs(process.argv.slice(2));
  const configPath = args.configPath
    ? path.resolve(args.configPath)
    : args.repoName
      ? path.join(skillDir, 'repos', args.repoName, 'config.json')
      : null;

  if (!configPath) {
    usage();
    process.exit(2);
  }
  if (!existsSync(configPath)) {
    throw new Error(`Config not found: ${configPath}`);
  }

  const beforeText = readFileSync(configPath, 'utf8');
  const config = JSON.parse(beforeText);
  const { next, actions } = reconcileConfig(config);
  const afterText = `${JSON.stringify(next, null, 2)}\n`;
  const changed = beforeText !== afterText;

  if (args.dryRun) {
    console.log(afterText);
  } else if (changed && !args.check) {
    writeJson(configPath, next);
  }

  console.error(summarize(actions, changed, args.dryRun, args.check));

  if (args.check && changed) {
    process.exit(1);
  }
} catch (error) {
  console.error(`update-config failed: ${error instanceof Error ? error.message : String(error)}`);
  process.exit(1);
}
