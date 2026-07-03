const fs = require('fs');
const path = require('path');
const { mergeJsonFile, copyHookScripts, appendSectionToFile, removeHookScripts, removeMarkedSection, assertSafeConfigDir, isEvolverHookCommand } = require('./hookAdapter');

const HOOK_SCRIPTS_DIR_NAME = 'hooks';
const EVOLVER_MARKER = '<!-- evolver-evolution-memory -->';

function buildCodexHooksJson(evolverRoot) {
  const scriptsBase = '.codex/hooks';
  return {
    hooks: {
      SessionStart: [
        {
          type: 'command',
          command: `node ${scriptsBase}/evolver-session-start.js`,
          timeout: 3,
        },
      ],
      PostToolUse: [
        {
          type: 'command',
          command: `node ${scriptsBase}/evolver-signal-detect.js`,
          timeout: 2,
        },
      ],
      Stop: [
        {
          type: 'command',
          command: `node ${scriptsBase}/evolver-session-end.js`,
          timeout: 8,
        },
      ],
    },
  };
}

function ensureConfigToml(codexDir) {
  const tomlPath = path.join(codexDir, 'config.toml');
  let content = '';
  try { content = fs.readFileSync(tomlPath, 'utf8'); } catch { /* new file */ }

  if (/codex_hooks\s*=\s*true/i.test(content)) {
    return false;
  }

  if (/\[features\]/.test(content)) {
    content = content.replace(
      /\[features\]/,
      '[features]\ncodex_hooks = true'
    );
  } else {
    const separator = content.length > 0 && !content.endsWith('\n') ? '\n\n' : content.length > 0 ? '\n' : '';
    content += separator + '[features]\ncodex_hooks = true\n';
  }

  fs.writeFileSync(tomlPath, content, 'utf8');
  return true;
}

// Reverse of `ensureConfigToml`: drop the `codex_hooks = true` line and, if
// the surrounding `[features]` block becomes empty as a result, drop that
// header too. Other unrelated entries under `[features]` are preserved.
// Returns true when the file changed.
function cleanConfigToml(codexDir) {
  const tomlPath = path.join(codexDir, 'config.toml');
  let content;
  try { content = fs.readFileSync(tomlPath, 'utf8'); } catch { return false; }
  if (!/codex_hooks\s*=\s*true/i.test(content)) return false;

  // Drop the `codex_hooks = true` line. The greedy `\s*` after `true`
  // consumes the trailing newline plus any blank lines so the
  // empty-`[features]` check below cannot be fooled by a stray blank
  // line into treating the section as empty while user entries still
  // follow.
  let next = content.replace(/^\s*codex_hooks\s*=\s*true\s*\n?/im, '');
  // Drop a now-empty `[features]` block. Two strict patterns avoid
  // `$` with the /m flag — multiline `$` matches before any `\n`, so
  // a single `(?=\s*$)` lookahead can succeed mid-file and strand
  // user entries below the removed header (PR #94 round-3).
  next = next.replace(/(^|\n)\[features\]\s*\n(?=\s*\[)/, '$1');
  next = next.replace(/(^|\n)\[features\]\s*$/, '$1');
  next = next.replace(/\n{3,}/g, '\n\n').trimEnd();
  if (next.length > 0) next += '\n';
  fs.writeFileSync(tomlPath, next, 'utf8');
  return true;
}

function buildAgentsMdSection() {
  return `${EVOLVER_MARKER}
## Evolution Memory (Evolver)

This project uses evolver for self-evolution. Hooks automatically:
1. Inject recent evolution memory at session start
2. Detect evolution signals during file edits
3. Record outcomes at session end

For substantive tasks, call \`gep_recall\` before work and \`gep_record_outcome\` after.
Signals: log_error, perf_bottleneck, user_feature_request, capability_gap, deployment_issue, test_failure.`;
}

function install({ configRoot, evolverRoot, force }) {
  const codexDir = path.join(configRoot, '.codex');
  const hooksJsonPath = path.join(codexDir, 'hooks.json');
  const hooksDir = path.join(codexDir, HOOK_SCRIPTS_DIR_NAME);
  const agentsMdPath = path.join(configRoot, 'AGENTS.md');
  assertSafeConfigDir(codexDir, '.codex', { subdirs: [HOOK_SCRIPTS_DIR_NAME] });

  if (!force && fs.existsSync(hooksJsonPath)) {
    try {
      const existing = JSON.parse(fs.readFileSync(hooksJsonPath, 'utf8'));
      if (existing._evolver_managed) {
        console.log('[codex] Evolver hooks already installed. Use --force to overwrite.');
        return { ok: true, skipped: true };
      }
    } catch { /* proceed */ }
  }

  fs.mkdirSync(codexDir, { recursive: true });

  const hooksCfg = buildCodexHooksJson(evolverRoot);
  mergeJsonFile(hooksJsonPath, hooksCfg);
  console.log('[codex] Wrote ' + hooksJsonPath);

  const copied = copyHookScripts(hooksDir, path.join(evolverRoot, 'src', 'adapters'));
  console.log('[codex] Copied ' + copied.length + ' hook scripts to ' + hooksDir);

  const tomlChanged = ensureConfigToml(codexDir);
  if (tomlChanged) {
    console.log('[codex] Enabled codex_hooks in config.toml');
  }

  const injected = appendSectionToFile(agentsMdPath, EVOLVER_MARKER, buildAgentsMdSection());
  if (injected) {
    console.log('[codex] Injected evolution section into ' + agentsMdPath);
  }

  console.log('[codex] Installation complete.');

  return {
    ok: true,
    platform: 'codex',
    files: [hooksJsonPath, path.join(codexDir, 'config.toml'), agentsMdPath, ...copied],
  };
}

function uninstall({ configRoot }) {
  const codexDir = path.join(configRoot, '.codex');
  const hooksJsonPath = path.join(codexDir, 'hooks.json');
  const hooksDir = path.join(codexDir, HOOK_SCRIPTS_DIR_NAME);
  const agentsMdPath = path.join(configRoot, 'AGENTS.md');
  assertSafeConfigDir(codexDir, '.codex', { subdirs: [HOOK_SCRIPTS_DIR_NAME] });

  let changed = false;

  // Strip evolver entries from hooks.json. Even when the
  // `_evolver_managed` marker is missing (older install, hand-edited
  // file), we still try to filter by command — a missing marker should
  // not strand obvious evolver-owned entries (#538).
  try {
    if (fs.existsSync(hooksJsonPath)) {
      const data = JSON.parse(fs.readFileSync(hooksJsonPath, 'utf8'));
      let touched = false;
      if (data.hooks) {
        for (const event of Object.keys(data.hooks)) {
          if (Array.isArray(data.hooks[event])) {
            const before = data.hooks[event].length;
            data.hooks[event] = data.hooks[event].filter(h => {
              const cmd = (h && h.command) || '';
              return !isEvolverHookCommand(cmd);
            });
            if (data.hooks[event].length !== before) touched = true;
            if (data.hooks[event].length === 0) delete data.hooks[event];
          }
        }
        if (Object.keys(data.hooks).length === 0) delete data.hooks;
      }
      if (data._evolver_managed) {
        delete data._evolver_managed;
        touched = true;
      }
      if (touched) {
        fs.writeFileSync(hooksJsonPath, JSON.stringify(data, null, 2) + '\n', 'utf8');
        changed = true;
      }
    }
  } catch (e) {
    console.warn(`[codex] Failed to clean ${hooksJsonPath}: ${e.message || e}`);
  }

  const scripts = removeHookScripts(hooksDir);
  if (scripts > 0) changed = true;
  // If hooks dir is now empty (only evolver scripts lived there), remove it
  // so a subsequent install starts from a clean slate.
  try {
    if (fs.existsSync(hooksDir) && fs.readdirSync(hooksDir).length === 0) {
      fs.rmdirSync(hooksDir);
    }
  } catch { /* best-effort */ }

  if (cleanConfigToml(codexDir)) {
    console.log('[codex] Removed codex_hooks flag from config.toml');
    changed = true;
  }

  if (removeMarkedSection(agentsMdPath, EVOLVER_MARKER)) {
    changed = true;
  }

  console.log(changed
    ? '[codex] Uninstalled evolver hooks.'
    : '[codex] No evolver hooks found to uninstall.');

  return { ok: true, removed: changed };
}

module.exports = { install, uninstall, buildCodexHooksJson, ensureConfigToml, cleanConfigToml };
