const fs = require('fs');
const path = require('path');
const { mergeJsonFile, copyHookScripts, removeEvolverHooks, removeHookScripts, assertSafeConfigDir } = require('./hookAdapter');

const HOOK_SCRIPTS_DIR_NAME = 'hooks';

function buildHooksJson(evolverRoot, isUserLevel) {
  const scriptsBase = isUserLevel ? './hooks' : '.cursor/hooks';
  return {
    version: 1,
    hooks: {
      sessionStart: [
        {
          command: `node ${scriptsBase}/evolver-session-start.js`,
          timeout: 3,
        },
      ],
      afterFileEdit: [
        {
          command: `node ${scriptsBase}/evolver-signal-detect.js`,
          matcher: 'Write',
          timeout: 2,
        },
      ],
      stop: [
        {
          command: `node ${scriptsBase}/evolver-session-end.js`,
          timeout: 8,
          loop_limit: 1,
        },
      ],
    },
  };
}

function install({ configRoot, evolverRoot, force }) {
  const os = require('os');
  const isUserLevel = configRoot === os.homedir();
  const cursorDir = path.join(configRoot, '.cursor');
  const hooksJsonPath = path.join(cursorDir, 'hooks.json');
  const hooksDir = path.join(cursorDir, HOOK_SCRIPTS_DIR_NAME);
  assertSafeConfigDir(cursorDir, '.cursor', { subdirs: [HOOK_SCRIPTS_DIR_NAME] });

  if (!force && fs.existsSync(hooksJsonPath)) {
    try {
      const existing = JSON.parse(fs.readFileSync(hooksJsonPath, 'utf8'));
      if (existing._evolver_managed) {
        console.log('[cursor] Evolver hooks already installed. Use --force to overwrite.');
        return { ok: true, skipped: true };
      }
    } catch { /* proceed */ }
  }

  fs.mkdirSync(cursorDir, { recursive: true });

  const hooksCfg = buildHooksJson(evolverRoot, isUserLevel);
  mergeJsonFile(hooksJsonPath, hooksCfg);
  console.log('[cursor] Wrote ' + hooksJsonPath);

  const copied = copyHookScripts(hooksDir, path.join(evolverRoot, 'src', 'adapters'));
  console.log('[cursor] Copied ' + copied.length + ' hook scripts to ' + hooksDir);

  console.log('[cursor] Installation complete.');
  console.log('[cursor] Restart Cursor or open a new session to activate hooks.');

  return {
    ok: true,
    platform: 'cursor',
    files: [hooksJsonPath, ...copied],
  };
}

function uninstall({ configRoot, evolverRoot }) {
  const cursorDir = path.join(configRoot, '.cursor');
  const hooksJsonPath = path.join(cursorDir, 'hooks.json');
  const hooksDir = path.join(cursorDir, HOOK_SCRIPTS_DIR_NAME);
  assertSafeConfigDir(cursorDir, '.cursor', { subdirs: [HOOK_SCRIPTS_DIR_NAME] });

  const removed = removeEvolverHooks(hooksJsonPath);
  const scripts = removeHookScripts(hooksDir);

  if (removed || scripts > 0) {
    console.log('[cursor] Uninstalled evolver hooks (' + scripts + ' scripts removed).');
  } else {
    console.log('[cursor] No evolver hooks found to uninstall.');
  }

  return { ok: true, removed: removed || scripts > 0 };
}

module.exports = { install, uninstall, buildHooksJson };
