'use strict';

// OMLS-inspired idle scheduler: detects user inactivity windows and recommends
// evolution intensity levels. Monitors system idle time on supported platforms.
// When idle, the evolver can run more aggressive operations (distillation,
// reflection); when busy, it only collects signals.
//
// Headless / no-X11 Linux notes
// --------------------------------
// On headless Linux servers (no X11 display), `xprintidle` is unavailable and
// will always fail, causing getSystemIdleSeconds() to return -1. This is also
// true inside Docker containers, SSH-only servers, and most CI runners.
//
// When idleSeconds === -1, determineIntensity() falls back to 'normal' by
// default. On a truly headless server there is no interactive user, so the
// machine is effectively always idle — 'normal' may be too conservative for a
// dedicated evolver host yet too aggressive for a shared CI runner.
//
// Override options (in order of precedence):
//   EVOLVER_INTENSITY=aggressive   force a fixed intensity level regardless of
//   EVOLVER_INTENSITY=deep         idle detection. Valid values: signal_only,
//   EVOLVER_INTENSITY=normal       normal, aggressive, deep.
//   EVOLVER_INTENSITY=signal_only
//
// Alternatives to xprintidle on headless systems:
//   - Set EVOLVER_INTENSITY to the desired level in the service unit / crontab.
//   - Use `loginctl show-session` to detect attached TTY sessions and set the
//     env var conditionally in a wrapper script.
//   - Install `xprintidle` and export DISPLAY=:0 only if a virtual framebuffer
//     (Xvfb) is running — not recommended for pure server deployments.

const { execSync, execFileSync } = require('child_process');
// 10 MB — prevents RangeError on large child process output (e.g. git log/diff
// on large repos). See GHSA reports / issue #451.
const MAX_EXEC_BUFFER = 10 * 1024 * 1024;

const path = require('path');
const fs = require('fs');
const { getEvolutionDir } = require('./paths');

const IDLE_THRESHOLD_SECONDS = parseInt(process.env.OMLS_IDLE_THRESHOLD || '300', 10) || 300;
const DEEP_IDLE_THRESHOLD_SECONDS = parseInt(process.env.OMLS_DEEP_IDLE_THRESHOLD || '1800', 10) || 1800;

// EVOLVER_INTENSITY: when set, bypasses idle detection entirely and pins the
// scheduler to this intensity level. Useful on headless servers where
// xprintidle is unavailable and the machine is always effectively idle.
// Accepted values (case-insensitive): signal_only | normal | aggressive | deep.
const VALID_INTENSITIES = new Set(['signal_only', 'normal', 'aggressive', 'deep']);
const _forcedIntensity = (function () {
  const raw = (process.env.EVOLVER_INTENSITY || '').trim().toLowerCase();
  if (raw && VALID_INTENSITIES.has(raw)) return raw;
  if (raw) {
    // Warn once at startup rather than silently ignoring a typo.
    console.warn(
      '[idleScheduler] EVOLVER_INTENSITY="' + raw + '" is not a recognised value. ' +
      'Valid values: signal_only, normal, aggressive, deep. Falling back to idle detection.'
    );
  }
  return null;
}());

// In-process cache to avoid spawning `ioreg` (darwin) / `xprintidle` (linux)
// / a powershell child (win32) on EVERY evolve cycle. Each call has a
// hard timeout (5-10s) but in practice ioreg takes ~50-200ms and
// powershell startup ~500-800ms; doing that synchronously on the main
// thread once per cycle stacks 1-2s of blocking time per loop iteration
// onto whatever other sync IO the cycle did (git, gh, npm view). The 2s
// TTL means we still re-sample frequently enough to detect a user
// becoming active mid-cycle, but we are not paying the spawn cost in a
// tight loop. The cache is intentionally per-process (no fs writes): a
// daemon and an ad-hoc CLI invocation pay independent costs.
let _idleCache = { at: 0, value: -1 };
const _IDLE_CACHE_TTL_MS = 2000;
function _getCachedIdleSeconds(compute) {
  const now = Date.now();
  if (now - _idleCache.at < _IDLE_CACHE_TTL_MS) return _idleCache.value;
  const v = compute();
  _idleCache = { at: now, value: v };
  return v;
}

// Linux idle detection — overridable for tests via __test.setExec() /
// __test.setExecFile(). Two helpers because of a security distinction:
//   * _execImpl  -> execSync (string form, parsed by /bin/sh -c). ONLY use
//                   for fully static commands with no dynamic input.
//   * _execFileImpl -> execFileSync (argv form, NEVER touches the shell).
//                   REQUIRED for any command that mixes in an env var or
//                   other dynamic value, to eliminate shell-injection at
//                   the source. See issue #168 / PR #167 review.
function _defaultExec(cmd, timeoutMs) {
  try {
    return execSync(cmd, {
      timeout: timeoutMs,
      encoding: 'utf8',
      maxBuffer: MAX_EXEC_BUFFER,
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
  } catch (e) {
    return null;
  }
}
function _defaultExecFile(file, args, timeoutMs) {
  try {
    return execFileSync(file, args, {
      timeout: timeoutMs,
      encoding: 'utf8',
      maxBuffer: MAX_EXEC_BUFFER,
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
  } catch (e) {
    return null;
  }
}
let _execImpl = _defaultExec;
let _execFileImpl = _defaultExecFile;

function _tryXprintidle() {
  // X11-only. Returns idle time in ms. Silently fails on Wayland sessions
  // (no X server) or on systems without the xprintidle package installed.
  const out = _execImpl('xprintidle', 5000);
  if (out === null) return -1;
  const ms = parseInt(out, 10);
  if (!Number.isFinite(ms) || ms < 0) return -1;
  return Math.floor(ms / 1000);
}

function _tryGnomeMutter() {
  // GNOME exposes the compositor's idle time via the session D-Bus, on BOTH
  // X11 and Wayland sessions. Returns ms. This is the primary Wayland path
  // since GNOME is the default desktop on Ubuntu / Fedora / RHEL desktop
  // workloads. Requires a running user session bus (will fail under sudo /
  // cron / TTY with no session).
  const out = _execImpl(
    'gdbus call --session --dest org.gnome.Mutter.IdleMonitor ' +
    '--object-path /org/gnome/Mutter/IdleMonitor/Core ' +
    '--method org.gnome.Mutter.IdleMonitor.GetIdletime',
    5000,
  );
  if (out === null) return -1;
  // gdbus output format: "(uint64 12345,)"
  const m = out.match(/uint64\s+(\d+)/);
  if (!m) return -1;
  const ms = parseInt(m[1], 10);
  if (!Number.isFinite(ms) || ms < 0) return -1;
  return Math.floor(ms / 1000);
}

function _tryLoginctlIdleHint() {
  // systemd-logind exposes IdleHint (bool) + IdleSinceHint (usec epoch).
  // Universal fallback for any modern systemd Linux regardless of X11/
  // Wayland/desktop environment. Less precise than xprintidle / Mutter —
  // when IdleHint=no we can only report 0 (active). Requires XDG_SESSION_ID
  // to be set, which it is for any logind-managed login (graphical or TTY).
  //
  // SECURITY (issue #168): XDG_SESSION_ID is read from the process
  // environment, so it must NEVER be concatenated into a shell command.
  // We use _execFileImpl (argv form, no /bin/sh) AND additionally enforce
  // an ASCII-digit allowlist before forking — defense in depth, since
  // logind session ids are documented to be monotonic uints. The
  // `[0-9]+` (not `\d+`) form is deliberate: `\d` in JS regex matches
  // Unicode digits, which is broader than what loginctl accepts.
  const sessionId = process.env.XDG_SESSION_ID;
  if (!sessionId) return -1;
  if (!/^[0-9]+$/.test(sessionId)) return -1;
  const out = _execFileImpl(
    'loginctl',
    ['show-session', sessionId, '-p', 'IdleHint', '-p', 'IdleSinceHint'],
    5000,
  );
  if (out === null) return -1;
  const hintMatch = out.match(/IdleHint=(yes|no)/);
  const sinceMatch = out.match(/IdleSinceHint=(\d+)/);
  if (!hintMatch) return -1;
  if (hintMatch[1] === 'no') return 0;
  if (!sinceMatch) return -1;
  const sinceUsec = parseInt(sinceMatch[1], 10);
  if (!Number.isFinite(sinceUsec) || sinceUsec <= 0) return -1;
  const nowUsec = Date.now() * 1000;
  const idleSec = Math.floor((nowUsec - sinceUsec) / 1_000_000);
  return idleSec >= 0 ? idleSec : -1;
}

const LINUX_METHODS = [
  ['xprintidle', _tryXprintidle],
  ['gnome-mutter', _tryGnomeMutter],
  ['loginctl', _tryLoginctlIdleHint],
];

// Remember which method worked last so we don't fork 3 subprocesses every
// scheduling tick. A method that succeeds once almost always keeps working
// for the lifetime of the session.
let _cachedLinuxMethod = null;

function _getLinuxIdleSeconds() {
  if (_cachedLinuxMethod) {
    const entry = LINUX_METHODS.find((m) => m[0] === _cachedLinuxMethod);
    if (entry) {
      const s = entry[1]();
      if (s >= 0) return s;
      // Cached method stopped working (e.g. session type changed across a
      // logout/login). Fall through to re-discover.
      _cachedLinuxMethod = null;
    }
  }
  for (const [name, fn] of LINUX_METHODS) {
    const s = fn();
    if (s >= 0) {
      _cachedLinuxMethod = name;
      return s;
    }
  }
  return -1;
}

function getSystemIdleSeconds() {
  return _getCachedIdleSeconds(_getSystemIdleSecondsUncached);
}

function _getSystemIdleSecondsUncached() {
  const platform = process.platform;
  try {
    if (platform === 'win32') {
      const psCode = [
        'Add-Type -TypeDefinition @"',
        'using System;',
        'using System.Runtime.InteropServices;',
        'public struct LASTINPUTINFO { public uint cbSize; public uint dwTime; }',
        'public class IdleTime {',
        '  [DllImport("user32.dll")] static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);',
        '  public static uint Get() {',
        '    LASTINPUTINFO lii = new LASTINPUTINFO();',
        '    lii.cbSize = (uint)Marshal.SizeOf(lii);',
        '    GetLastInputInfo(ref lii);',
        '    return ((uint)Environment.TickCount - lii.dwTime) / 1000;',
        '  }',
        '}',
        '"@',
        '[IdleTime]::Get()',
      ].join('\n');
      const tmpPs = path.join(require('os').tmpdir(), 'evolver_idle_check.ps1');
      require('fs').writeFileSync(tmpPs, psCode, 'utf8');
      const result = execFileSync('powershell', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', tmpPs], {
        timeout: 10000,
        encoding: 'utf8',
        maxBuffer: MAX_EXEC_BUFFER,
        windowsHide: true,
      }).trim();
      try { require('fs').unlinkSync(tmpPs); } catch (e) {}
      const seconds = parseInt(result, 10);
      return Number.isFinite(seconds) ? seconds : -1;
    } else if (platform === 'darwin') {
      const result = execSync('ioreg -c IOHIDSystem | grep HIDIdleTime', { timeout: 5000, encoding: 'utf8', maxBuffer: MAX_EXEC_BUFFER });
      const match = result.match(/(\d+)/);
      if (match) {
        return Math.floor(parseInt(match[1], 10) / 1000000000);
      }
    } else if (platform === 'linux') {
      // Multi-tier detection. Pre-fix this was xprintidle-only, which fails
      // silently on Wayland sessions (default on modern Ubuntu / Fedora /
      // GNOME 40+ / KDE 6+) — getSystemIdleSeconds() returned -1 forever,
      // determineIntensity(-1) returned 'normal', and the idle scheduler
      // never triggered aggressive/deep mode on Wayland boxes.
      const linuxIdle = _getLinuxIdleSeconds();
      if (linuxIdle >= 0) return linuxIdle;
    }
  } catch (e) {}
  return -1;
}

// Intensity levels:
//   'signal_only'  - only collect signals, minimal CPU
//   'normal'       - standard evolution cycle
//   'aggressive'   - run distillation, reflection, deeper analysis
//   'deep'         - extended operations (future: RL, fine-tuning triggers)
//
// idleSeconds === -1 means idle detection is unavailable (e.g. headless Linux
// with no X11/xprintidle). The default fallback is 'normal'. To override this
// on a server set EVOLVER_INTENSITY in the environment (see top-of-file docs).
function determineIntensity(idleSeconds) {
  // Environment override takes precedence over any measured or inferred value.
  if (_forcedIntensity) return _forcedIntensity;

  // idleSeconds < 0: idle detection unavailable (headless / unsupported env).
  // Default to 'normal' so a shared CI runner is not inadvertently hammered.
  // On a dedicated evolver server, set EVOLVER_INTENSITY=aggressive instead.
  if (idleSeconds < 0) return 'normal';
  if (idleSeconds >= DEEP_IDLE_THRESHOLD_SECONDS) return 'deep';
  if (idleSeconds >= IDLE_THRESHOLD_SECONDS) return 'aggressive';
  return 'normal';
}

function readScheduleState() {
  const statePath = path.join(getEvolutionDir(), 'idle_schedule_state.json');
  try {
    if (!fs.existsSync(statePath)) return {};
    const raw = fs.readFileSync(statePath, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    return {};
  }
}

function writeScheduleState(state) {
  const dir = getEvolutionDir();
  const statePath = path.join(dir, 'idle_schedule_state.json');
  try {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const tmp = statePath + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(state, null, 2) + '\n', 'utf8');
    fs.renameSync(tmp, statePath);
  } catch (e) {
    if (process.env.EVOLVER_VERBOSE) console.warn('[idleScheduler] writeScheduleState failed:', e.message);
  }
}

// Returns scheduling recommendation with sleep multiplier and action hints.
function getScheduleRecommendation() {
  const enabled = String(process.env.OMLS_ENABLED || 'true').toLowerCase() !== 'false';
  if (!enabled) {
    return {
      enabled: false,
      idle_seconds: -1,
      intensity: 'normal',
      sleep_multiplier: 1,
      should_distill: false,
      should_reflect: false,
      should_deep_evolve: false,
      should_explore: false,
    };
  }

  const idleSeconds = getSystemIdleSeconds();
  const intensity = determineIntensity(idleSeconds);

  const state = readScheduleState();
  const now = Date.now();

  let sleepMultiplier = 1;
  let shouldDistill = false;
  let shouldReflect = false;
  let shouldDeepEvolve = false;
  let shouldExplore = false;

  if (intensity === 'aggressive') {
    sleepMultiplier = 0.5;
    shouldDistill = true;
    shouldReflect = true;
    shouldExplore = true;
  } else if (intensity === 'deep') {
    sleepMultiplier = 0.25;
    shouldDistill = true;
    shouldReflect = true;
    shouldDeepEvolve = true;
    shouldExplore = true;
  } else if (intensity === 'signal_only') {
    sleepMultiplier = 3;
  }

  state.last_check = new Date().toISOString();
  state.last_idle_seconds = idleSeconds;
  state.last_intensity = intensity;
  writeScheduleState(state);

  return {
    enabled: true,
    idle_seconds: idleSeconds,
    intensity: intensity,
    sleep_multiplier: sleepMultiplier,
    should_distill: shouldDistill,
    should_reflect: shouldReflect,
    should_deep_evolve: shouldDeepEvolve,
    should_explore: shouldExplore,
  };
}

module.exports = {
  getSystemIdleSeconds: getSystemIdleSeconds,
  determineIntensity: determineIntensity,
  getScheduleRecommendation: getScheduleRecommendation,
  readScheduleState: readScheduleState,
  writeScheduleState: writeScheduleState,
  IDLE_THRESHOLD_SECONDS: IDLE_THRESHOLD_SECONDS,
  DEEP_IDLE_THRESHOLD_SECONDS: DEEP_IDLE_THRESHOLD_SECONDS,
  // Exposed for inspection / testing; null means no override is active.
  _forcedIntensity: _forcedIntensity,
  // Test-only surface for the Linux multi-tier idle detection. Lets tests
  // inject a fake exec implementation so we can verify the fallback chain
  // (xprintidle -> gnome-mutter -> loginctl) and the cached-method fast path
  // without depending on a real X server / D-Bus / systemd on the test box.
  __test: {
    setExec: function (fn) { _execImpl = fn || _defaultExec; },
    setExecFile: function (fn) { _execFileImpl = fn || _defaultExecFile; },
    resetLinuxCache: function () { _cachedLinuxMethod = null; },
    getLinuxIdleSeconds: _getLinuxIdleSeconds,
    tryXprintidle: _tryXprintidle,
    tryGnomeMutter: _tryGnomeMutter,
    tryLoginctlIdleHint: _tryLoginctlIdleHint,
    getCachedMethod: function () { return _cachedLinuxMethod; },
  },
};
