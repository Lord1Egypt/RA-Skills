#!/usr/bin/env node
'use strict';
// Shared helpers for planning-with-files path resolution.
// Uses windowsHide to avoid console windows on Windows/RemoteApp.

const fs = require('fs');
const path = require('path');

const PLANNING_ROOT = process.env.PLANNING_WITH_FILES_ROOT || 'docs/sessions';

function findActivePlanFile() {
  const scopedDir = process.env.PLANNING_WITH_FILES_PLAN_DIR || '';
  if (scopedDir) {
    const candidate = path.join(scopedDir, 'task_plan.md');
    if (fs.existsSync(candidate)) return candidate;
  }

  if (!fs.existsSync(PLANNING_ROOT)) return null;

  let latest = null;
  let latestTime = 0;

  function walk(dir) {
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (entry.name === 'task_plan.md') {
        try {
          const mtime = fs.statSync(full).mtimeMs;
          if (mtime > latestTime) { latest = full; latestTime = mtime; }
        } catch {}
      }
    }
  }

  walk(PLANNING_ROOT);
  return latest;
}

function describeActiveLocation() {
  const planFile = findActivePlanFile();
  return planFile ? path.dirname(planFile).replace(/\\/g, '/') : `${PLANNING_ROOT}/<task-slug>`;
}

module.exports = { PLANNING_ROOT, findActivePlanFile, describeActiveLocation };
