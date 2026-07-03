#!/usr/bin/env node
'use strict';
// Shared path constants and helpers for Claude Code team-scaffold hooks.
// Uses windowsHide on child_process, path.resolve for portability.

const fs = require('fs');
const path = require('path');
const os = require('os');

const PROJECT_ROOT = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const HOME = os.homedir();

const RUNTIME_DIR = path.resolve(PROJECT_ROOT, '.claude', '.runtime');
const GATE_FILE = path.join(RUNTIME_DIR, 'gate.json');
const EDITS_FILE = path.join(RUNTIME_DIR, 'edits.json');
const RETRY_FILE = path.join(RUNTIME_DIR, 'retry-counts.json');

const MEMORY_PROJECT_DIR = path.resolve(PROJECT_ROOT, '.claude', 'memory');
const MEMORY_GLOBAL_DIR = path.join(HOME, '.claude', 'memory');
const GLOBAL_CLAUDE_MD = path.join(HOME, '.claude', 'CLAUDE.md');
const LESSONS_FILE = path.join(MEMORY_PROJECT_DIR, 'lessons-learned.md');

const SESSION_LOG_DIR = path.resolve(PROJECT_ROOT, '.claude', 'session-logs');

const INSTRUCTIONS_DIR = path.resolve(PROJECT_ROOT, '.claude', 'instructions');
const SPEC_FLOW_ACTIVE_DIR = path.resolve(PROJECT_ROOT, '.spec-flow', 'active');

const MODULE_ROOTS = ['src', 'app', 'lib', 'packages', 'services'];

/**
 * Walk up from filePath's directory looking for the nearest CLAUDE.md.
 * Returns absolute path to the CLAUDE.md, or null.
 */
function findModuleClaudeMd(filePath, projectRoot) {
  const root = projectRoot || PROJECT_ROOT;
  let dir = path.dirname(path.resolve(root, filePath));
  const maxDepth = 10;
  for (let i = 0; i < maxDepth; i++) {
    const candidate = path.join(dir, 'CLAUDE.md');
    try {
      if (fs.existsSync(candidate)) return candidate;
    } catch {}
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

/** Check whether filePath sits inside one of the recognized module roots. */
function isInModuleRoot(filePath, projectRoot) {
  const root = projectRoot || PROJECT_ROOT;
  const rel = path.relative(root, path.resolve(root, filePath));
  const top = rel.split(path.sep)[0];
  return MODULE_ROOTS.includes(top);
}

module.exports = {
  PROJECT_ROOT,
  HOME,
  RUNTIME_DIR,
  GATE_FILE,
  EDITS_FILE,
  RETRY_FILE,
  MEMORY_PROJECT_DIR,
  MEMORY_GLOBAL_DIR,
  GLOBAL_CLAUDE_MD,
  LESSONS_FILE,
  SESSION_LOG_DIR,
  INSTRUCTIONS_DIR,
  SPEC_FLOW_ACTIVE_DIR,
  MODULE_ROOTS,
  findModuleClaudeMd,
  isInModuleRoot,
};
