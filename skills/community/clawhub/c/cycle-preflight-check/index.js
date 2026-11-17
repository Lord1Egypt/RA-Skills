const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE_ROOT || process.cwd();
const EVOLUTION_STATE = path.join(WORKSPACE, 'memory/evolution/evolution_state.json');
const VALIDATE_MODULES = path.join(WORKSPACE, 'scripts/validate-modules.js');
const VALIDATE_SUITE = path.join(WORKSPACE, 'scripts/validate-suite.js');

function loadJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function getRecentCycles(state, n = 8) {
  const cycles = (state && state.recent_cycles) || [];
  return cycles.slice(-n);
}

function checkDuplicateRecent(cycles) {
  const seen = new Set();
  const dupes = [];
  for (const c of cycles) {
    const key = `${c.intent}::${c.gene}`;
    if (seen.has(key)) dupes.push(key);
    seen.add(key);
  }
  return dupes;
}

function checkValidationScripts() {
  const missing = [];
  if (!fs.existsSync(VALIDATE_MODULES)) missing.push('scripts/validate-modules.js');
  if (!fs.existsSync(VALIDATE_SUITE)) missing.push('scripts/validate-suite.js');
  return missing;
}

function checkUncommittedChanges() {
  try {
    const { execSync } = require('child_process');
    const out = execSync('git status --porcelain', { encoding: 'utf8', cwd: WORKSPACE, stdio: ['ignore', 'pipe', 'ignore'] });
    const lines = out.split('\n').filter(Boolean);
    const untracked = lines.filter(l => l.startsWith('??')).length;
    const modified = lines.filter(l => !l.startsWith('??')).length;
    return { untracked, modified, total: lines.length };
  } catch {
    return { untracked: 0, modified: 0, total: 0 };
  }
}

function checkUncommittedSkillCode() {
  try {
    const { execSync } = require('child_process');
    const skillsRoot = path.join(WORKSPACE, 'skills');
    const out = execSync('git status --porcelain -- skills/', { encoding: 'utf8', cwd: WORKSPACE, stdio: ['ignore', 'pipe', 'ignore'] });
    const lines = out.split('\n').filter(Boolean);
    const codeRelevant = lines.filter(l => {
      const file = l.slice(3).trim();
      return file.startsWith('skills/') && (file.endsWith('index.js') || file.endsWith('SKILL.md') || file.endsWith('package.json'));
    });
    return codeRelevant.length;
  } catch {
    return 0;
  }
}

function main() {
  const state = loadJson(EVOLUTION_STATE);
  const cycles = getRecentCycles(state, 8);
  const dupes = checkDuplicateRecent(cycles);
  const missing = checkValidationScripts();
  const git = checkUncommittedChanges();
  const skillCodeChanges = checkUncommittedSkillCode();

  const findings = [];
  if (dupes.length) findings.push(`duplicate_recent_intent_gene=${dupes.length}`);
  if (missing.length) findings.push(`missing_validation_scripts=${missing.join(',')}`);
  if (skillCodeChanges === 0 && git.modified > 0) findings.push(`likely_hollow_commit=no_skill_code_changes`);
  if (git.total > 20) findings.push(`high_git_churn=${git.total}`);
  if (git.untracked > 10) findings.push(`many_untracked=${git.untracked}`);

  const status = findings.length === 0 ? 'PASS' : 'WARN';
  const hint = findings.length ? findings[0] : 'ok';

  console.log(`=== Cycle Preflight ===`);
  console.log(`Status: ${status}`);
  console.log(`Hint: ${hint}`);
  if (missing.length) console.log(`Missing: ${missing.join(', ')}`);
  console.log(`Git: ${git.modified} modified, ${git.untracked} untracked`);
  console.log(`Skill code changes: ${skillCodeChanges}`);
  console.log(`Cycles reviewed: ${cycles.length}`);

  return status;
}

if (require.main === module) {
  process.exit(main() === 'PASS' ? 0 : 1);
}

module.exports = { main };
