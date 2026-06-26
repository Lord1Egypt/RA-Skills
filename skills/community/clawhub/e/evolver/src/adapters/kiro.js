const fs = require('fs');
const path = require('path');
const { copyHookScripts, removeHookScripts, removeMarkedSection, assertSafeConfigDir } = require('./hookAdapter');

const HOOK_SCRIPTS_DIR_NAME = 'hooks';
const EVOLVER_MARKER = '<!-- evolver-evolution-memory -->';
const HOOK_FILE_SUFFIX = '.kiro.hook';
const HOOK_FILES = {
  sessionStart: 'evolver-session-start.kiro.hook',
  signalDetect: 'evolver-signal-detect.kiro.hook',
  sessionEnd: 'evolver-session-end.kiro.hook',
};

function buildHookConfig(kind, scriptsBase) {
  // Kiro has no dedicated sessionStart event; `promptSubmit` is the closest
  // analogue. The session-start JS script itself guards against per-prompt
  // re-injection via a session-scoped state file when
  // EVOLVER_SESSION_START_DEDUP=1 is set (injected inline into the command
  // because Kiro runCommand has no env field).
  const sessionStartCmd = `EVOLVER_SESSION_START_DEDUP=1 node ${scriptsBase}/evolver-session-start.js`;
  const hookTemplates = {
    sessionStart: {
      name: 'Evolver Session Start',
      version: '1',
      description:
        'Reads recent evolution memory from the local memory graph and injects it as context when a prompt is submitted.',
      when: { type: 'promptSubmit' },
      then: {
        type: 'runCommand',
        command: sessionStartCmd,
        timeout: 3,
      },
      _evolver_managed: true,
    },
    signalDetect: {
      name: 'Evolver Signal Detect',
      version: '1',
      description:
        'Detects evolution signals (errors, perf bottlenecks, capability gaps, test failures) in file content after write operations.',
      when: { type: 'postToolUse', toolTypes: ['write'] },
      then: {
        type: 'runCommand',
        command: `node ${scriptsBase}/evolver-signal-detect.js`,
        timeout: 2,
      },
      _evolver_managed: true,
    },
    sessionEnd: {
      name: 'Evolver Session End',
      version: '1',
      description:
        'Records evolution outcome at session end by analyzing git diff stats and writing to the local memory graph.',
      when: { type: 'agentStop' },
      then: {
        type: 'runCommand',
        command: `node ${scriptsBase}/evolver-session-end.js`,
        timeout: 8,
      },
      _evolver_managed: true,
    },
  };
  return hookTemplates[kind];
}

function buildAgentsMdSection() {
  return `${EVOLVER_MARKER}
## Evolution Memory (Evolver)

This project uses evolver for self-evolution. Hooks automatically:
1. Inject recent evolution memory on prompt submit
2. Detect evolution signals during file edits
3. Record outcomes at session end

For substantive tasks, call \`gep_recall\` before work and \`gep_record_outcome\` after.
Signals: log_error, perf_bottleneck, user_feature_request, capability_gap, deployment_issue, test_failure.`;
}

function appendSectionToFile(filePath, marker, content) {
  let existing = '';
  try { existing = fs.readFileSync(filePath, 'utf8'); } catch { /* new file */ }
  if (existing.includes(marker)) return false;
  const separator = existing.length > 0 && !existing.endsWith('\n') ? '\n\n' : '\n';
  fs.writeFileSync(filePath, existing + separator + content + '\n', 'utf8');
  return true;
}

function writeHookFile(hooksDir, fileName, config) {
  const tmp = path.join(hooksDir, fileName + '.tmp');
  const dest = path.join(hooksDir, fileName);
  fs.writeFileSync(tmp, JSON.stringify(config, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, dest);
  return dest;
}

function isEvolverManagedHookFile(filePath) {
  try {
    const raw = fs.readFileSync(filePath, 'utf8').trim();
    if (!raw) return false;
    const data = JSON.parse(raw);
    if (data && data._evolver_managed === true) return true;
    if (typeof data.name === 'string' && /^evolver\b/i.test(data.name)) return true;
    if (data.then && typeof data.then.command === 'string' &&
        /evolver-(session|signal)/.test(data.then.command)) return true;
  } catch { /* treat as non-evolver */ }
  return false;
}

function install({ configRoot, evolverRoot, force }) {
  const kiroDir = path.join(configRoot, '.kiro');
  const hooksDir = path.join(kiroDir, HOOK_SCRIPTS_DIR_NAME);
  const agentsMdPath = path.join(configRoot, 'AGENTS.md');
  const scriptsBase = '.kiro/hooks';
  assertSafeConfigDir(kiroDir, '.kiro', { subdirs: [HOOK_SCRIPTS_DIR_NAME] });

  const hookPaths = Object.values(HOOK_FILES).map(name => path.join(hooksDir, name));

  if (!force) {
    const existingEvolverHook = hookPaths.find(p => fs.existsSync(p) && isEvolverManagedHookFile(p));
    if (existingEvolverHook) {
      console.log('[kiro] Evolver hooks already installed. Use --force to overwrite.');
      return { ok: true, skipped: true };
    }
  }

  fs.mkdirSync(hooksDir, { recursive: true });

  const written = [];
  for (const [kind, fileName] of Object.entries(HOOK_FILES)) {
    const cfg = buildHookConfig(kind, scriptsBase);
    const dest = writeHookFile(hooksDir, fileName, cfg);
    written.push(dest);
    console.log('[kiro] Wrote ' + dest);
  }

  const copied = copyHookScripts(hooksDir, path.join(evolverRoot, 'src', 'adapters'));
  console.log('[kiro] Copied ' + copied.length + ' hook scripts to ' + hooksDir);

  const injected = appendSectionToFile(agentsMdPath, EVOLVER_MARKER, buildAgentsMdSection());
  if (injected) {
    console.log('[kiro] Injected evolution section into ' + agentsMdPath);
  }

  console.log('[kiro] Installation complete.');
  console.log('[kiro] Kiro auto-discovers *.kiro.hook files in .kiro/hooks/ -- no restart needed.');

  return {
    ok: true,
    platform: 'kiro',
    files: [...written, agentsMdPath, ...copied],
  };
}

function uninstall({ configRoot }) {
  const kiroDir = path.join(configRoot, '.kiro');
  const hooksDir = path.join(kiroDir, HOOK_SCRIPTS_DIR_NAME);
  const agentsMdPath = path.join(configRoot, 'AGENTS.md');
  assertSafeConfigDir(kiroDir, '.kiro', { subdirs: [HOOK_SCRIPTS_DIR_NAME] });

  let changed = false;
  let removedCount = 0;

  if (fs.existsSync(hooksDir)) {
    try {
      const entries = fs.readdirSync(hooksDir);
      for (const entry of entries) {
        if (!entry.endsWith(HOOK_FILE_SUFFIX)) continue;
        const full = path.join(hooksDir, entry);
        if (isEvolverManagedHookFile(full)) {
          try { fs.unlinkSync(full); removedCount++; changed = true; } catch { /* ignore */ }
        }
      }
    } catch { /* ignore */ }
  }

  const scripts = removeHookScripts(hooksDir);
  if (scripts > 0) changed = true;

  if (removeMarkedSection(agentsMdPath, EVOLVER_MARKER)) {
    changed = true;
  }

  console.log(changed
    ? `[kiro] Uninstalled evolver hooks (${removedCount} hook files + ${scripts} scripts removed).`
    : '[kiro] No evolver hooks found to uninstall.');

  return { ok: true, removed: changed };
}

module.exports = {
  install,
  uninstall,
  buildHookConfig,
  isEvolverManagedHookFile,
  HOOK_FILES,
};
