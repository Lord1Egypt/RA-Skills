// tars-mcp core v2 — maximally flexible computer control
// Cross-platform backend auto-detection (macOS / Linux / Windows),
// user config (~/.tarsx/config.json), zero external API keys.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { randomUUID } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const run = promisify(execFile);
const PLATFORM = process.platform; // 'darwin' | 'linux' | 'win32'

export async function sh(cmd, args, timeout = 15000) {
  const { stdout } = await run(cmd, args, { timeout, maxBuffer: 10 * 1024 * 1024 });
  return stdout.trim();
}
async function trySh(cmd, args, timeout) {
  try { return { ok: true, out: await sh(cmd, args, timeout) }; }
  catch (e) { return { ok: false, err: (e.stderr || e.message || '').trim() }; }
}

// ---------- config ----------
let _cfg;
export function config() {
  if (_cfg) return _cfg;
  const candidates = [process.env.TARSX_CONFIG, path.join(os.homedir(), '.tarsx', 'config.json'), path.join(os.homedir(), '.tarsxrc')].filter(Boolean);
  const file = candidates.find((p) => fs.existsSync(p));
  _cfg = {
    screenshotDir: os.tmpdir(),
    screenshotFormat: 'png',
    scrollLines: 3,
    clipboardPasteForNonAscii: true,
    prefer: {},            // e.g. {"click": "osascript"} — override backend choice
    ...(file ? JSON.parse(fs.readFileSync(file, 'utf8')) : {}),
  };
  return _cfg;
}

// ---------- backend detection ----------
const cache = {};
async function has(cmd, args = ['--version']) {
  const k = 'has:' + cmd;
  if (cache[k] === undefined) cache[k] = (await trySh(cmd, args)).ok;
  return cache[k];
}
let _py = undefined;
async function pyCmd() {
  if (_py !== undefined) return _py;
  for (const py of ['/opt/homebrew/bin/python3', '/usr/local/bin/python3', `${os.homedir()}/.local/bin/python3`, '/usr/bin/python3', 'python3']) {
    if ((await trySh(py, ['-c', 'import Quartz'], 10)).ok) { _py = py; return _py; }
  }
  _py = null;
  return _py;
}
async function hasQuartz() {
  return (await pyCmd()) !== null;
}
function pyInline(body) {
  const py = _py || '/usr/bin/python3';
  return sh('/bin/sh', ['-c', `${py} -c ${JSON.stringify(body)}`]);
}

export async function info() {
  const d = { platform: PLATFORM, backends: {}, config: config() };
  d.configFile = CONFIG_PATHS;
  if (PLATFORM === 'darwin') {
    d.backends.screenshot = ['screencapture'];
    d.backends.click = [];
    // report the same discovery click() actually uses (PATH-independent)
    if (await cliclickCmd()) d.backends.click.unshift('cliclick (real events, right/double OK)');
    if (await hasQuartz()) d.backends.click.push('quartz-python');
    d.backends.click.push('osascript');
    d.backends.type_key = ['osascript'];
  } else if (PLATFORM === 'linux') {
    d.backends.click = (await has('xdotool')) ? ['xdotool'] : [];
    d.backends.type_key = (await has('xdotool')) ? ['xdotool'] : [];
    d.backends.screenshot = [];
    for (const t of ['import', 'scrot', 'gnome-screenshot', 'grim']) if (await has(t)) d.backends.screenshot.push(t);
    d.backends.windows = (await has('wmctrl')) ? ['wmctrl'] : [];
  } else if (PLATFORM === 'win32') {
    d.backends.click = ['powershell (left/right, no double)'];
    d.backends.screenshot = ['powershell'];
    d.backends.type_key = ['powershell (SendKeys)'];
  }
  return d;
}
const CONFIG_PATHS = [process.env.TARSX_CONFIG, path.join(os.homedir(), '.tarsx', 'config.json'), path.join(os.homedir(), '.tarsxrc')].filter(Boolean);

const fail = (msg) => { throw new Error(msg); };

// ---------- event delivery & TarsX.app helper routing ----------
// macOS grants Accessibility to real .app bundles (and shows them the standard
// "wants to control your computer" prompt). Bare binaries — e.g. a LaunchAgent
// node — silently no-op CGEvents forever. When direct events don't land, actions
// auto-route through the TarsX.app helper built by scripts/make-app.sh.
export function helperApp() {
  for (const p of [path.join(os.homedir(), 'Applications', 'TarsX.app'), '/Applications/TarsX.app']) {
    const bin = path.join(p, 'Contents', 'MacOS', 'TarsX');
    if (fs.existsSync(bin)) return { app: p, bin };
  }
  return null;
}

let _a11y; // undefined unknown · true direct delivery works · false blocked
export async function eventsDelivered() {
  if (PLATFORM !== 'darwin') return true;
  if (_a11y !== undefined) return _a11y;
  const p0 = await cursorPosDarwin();
  if (!p0) { _a11y = false; return _a11y; }
  const target = { x: p0.x + 2, y: p0.y };
  try {
    if (p0.via === 'cliclick') await sh(await cliclickCmd(), [`m:${target.x},${target.y}`], 5000);
    else await mouseMoveDirect({ x: target.x, y: target.y });
  } catch { _a11y = false; return _a11y; }
  const p1 = await cursorPosDarwin();
  if (p0.via === 'cliclick') await trySh(await cliclickCmd(), [`m:${p0.x},${p0.y}`], 5000);
  else await mouseMoveDirect({ x: p0.x, y: p0.y }).catch(() => {});
  _a11y = !!(p1 && Math.abs(p1.x - target.x) <= 1 && p1.y === p0.y);
  return _a11y;
}

async function helperTask(argv, timeoutMs = 90000) {
  const helper = helperApp();
  if (!helper) fail('TarsX.app helper not found (run scripts/make-app.sh from the skill folder)');
  let lastErr;
  for (let attempt = 0; attempt < 2; attempt++) {
    const id = randomUUID();
    const inFile = path.join(config().screenshotDir, `tarsx-task-${id}.json`);
    const outFile = path.join(config().screenshotDir, `tarsx-result-${id}.json`);
    fs.writeFileSync(inFile, JSON.stringify({ argv: argv.map(String) }));
    try {
      // -n: own instance every call — `open` otherwise coalesces into a running
      // instance and drops --args, losing the result
      await sh('/usr/bin/open', ['-W', '-n', '-a', helper.app, '--args', inFile, outFile], timeoutMs);
      if (fs.existsSync(outFile)) {
        const r = JSON.parse(fs.readFileSync(outFile, 'utf8'));
        if (r.code !== 0) fail((r.stderr || r.stdout || `helper exit ${r.code}`).trim());
        return (r.stdout || '').trim();
      }
      lastErr = new Error('TarsX helper produced no result file');
    } catch (e) {
      lastErr = e;
    } finally {
      try { fs.unlinkSync(inFile); } catch {}
      try { fs.unlinkSync(outFile); } catch {}
    }
    await new Promise((r) => setTimeout(r, 800));
  }
  fail(`TarsX helper run failed: ${lastErr.message}`);
}

async function route(directFn, argv) {
  if (PLATFORM !== 'darwin') return directFn();
  if (await eventsDelivered()) return directFn();
  if (helperApp()) {
    // authorize loop: first run may be waiting on the macOS permission prompt
    let delivered = false;
    for (let i = 0; i < 5; i++) {
      const probeOut = await helperTask(['probe', '--json']);
      try { if (JSON.parse(probeOut).delivered) { delivered = true; break; } } catch {}
      await new Promise((r) => setTimeout(r, 2000));
    }
    if (!delivered) fail('TarsX.app events not delivered — click "Allow/Дозволити" in the macOS prompt, or add TarsX in System Settings → Privacy & Security → Accessibility');
    return helperTask(argv);
  }
  return directFn();
}

// ---------- screenshot ----------
export async function screenshot({ region, out } = {}) {
  const cfg = config();
  const file = out || path.join(cfg.screenshotDir, `tarsx-${randomUUID()}.${cfg.screenshotFormat}`);
  if (PLATFORM === 'darwin') {
    const args = ['-x', '-t', 'png'];
    if (region) args.push(`-R${region}`);
    args.push(file);
    const r = await trySh('/usr/sbin/screencapture', args);
    if (!r.ok || !fs.existsSync(file)) fail('screencapture failed (check Screen Recording permission)');
  } else if (PLATFORM === 'linux') {
    for (const [cmd, fmt] of [['import', ['-window', 'root', file]], ['scrot', ['-o', file]], ['gnome-screenshot', ['-f', file]], ['grim', [file]]]) {
      if (await has(cmd)) { await sh(cmd, fmt); break; }
    }
    if (!fs.existsSync(file)) fail('no working screenshot tool (install ImageMagick/scrot/grim)');
  } else {
    const ps = `Add-Type -AssemblyName System.Windows.Forms,System.Drawing; $b=[System.Windows.Forms.SystemInformation]::VirtualScreen; $bmp=New-Object System.Drawing.Bitmap $b.Width,$b.Height; $g=[System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($b.X,$b.Y,0,0,$bmp.Size); $bmp.Save('${file.replace(/'/g, "''")}'); $g.Dispose(); $bmp.Dispose()`;
    await sh('powershell', ['-NoProfile', '-Command', ps], 20000);
  }
  return file;
}

// ---------- apple events (macOS) ----------
async function osa(script) {
  const r = await trySh('/usr/bin/osascript', ['-e', script]);
  if (!r.ok) {
    const msg = r.err || 'osascript failed';
    if (/not allowed assistive|assistive access/i.test(msg)) fail('Accessibility permission required: System Settings → Privacy & Security → Accessibility → enable the host app');
    fail(msg);
  }
  return r.out;
}

// ---------- mouse ----------
let _cliclick;
async function cliclickCmd() {
  if (_cliclick !== undefined) return _cliclick;
  for (const c of ['cliclick', '/opt/homebrew/bin/cliclick', '/usr/local/bin/cliclick', `${os.homedir()}/homebrew/bin/cliclick`]) {
    if ((await trySh(c, ['-V'], 5000)).ok) { _cliclick = c; return c; }
  }
  _cliclick = null;
  return _cliclick;
}

export async function click({ x, y, button = 'left', double = false, count = 1 } = {}) {
  const argv = ['click', String(x), String(y)];
  if (button === 'right') argv.push('--right');
  if (double) argv.push('--double');
  if (count > 1) argv.push('--count', String(count));
  return route(() => clickDirect({ x, y, button, double, count }), argv);
}

async function clickDirect({ x, y, button = 'left', double = false, count = 1 } = {}) {
  const cfg = config();
  const n = double ? 2 : (count || 1);
  if (PLATFORM === 'darwin') {
    // Best backend: cliclick (real CGEvents incl. right & double click)
    const cc = cfg.prefer.click ? null : await cliclickCmd();
    if (cc) {
      const op = button === 'right' ? (n > 1 ? 'dc' : 'rc') : (n > 1 ? 'dc' : 'c');
      if (n > 2) {
        for (let i = 0; i < n; i++) await sh(cc, [`c:${x},${y}`]);
        return `clicked ${n}x (cliclick)`;
      }
      await sh(cc, [`${op}:${x},${y}`]);
      return `clicked (cliclick ${op})`;
    }
    if (cfg.prefer.click !== 'osascript' && (await hasQuartz())) {
      const btn = button === 'right' ? 'kCGMouseButtonRight' : 'kCGMouseButtonLeft';
      const down = button === 'right' ? 'kCGEventRightMouseDown' : 'kCGEventLeftMouseDown';
      const up = button === 'right' ? 'kCGEventRightMouseUp' : 'kCGEventLeftMouseUp';
      const body = `import Quartz, time
p = (${x},${y})
e = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, p, Quartz.${btn})
Quartz.CGEventPost(Quartz.kCGHIDEventTap, e)
time.sleep(0.03)
for i in range(${n}):
    d = Quartz.CGEventCreateMouseEvent(None, Quartz.${down}, p, Quartz.${btn})
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, d)
    u = Quartz.CGEventCreateMouseEvent(None, Quartz.${up}, p, Quartz.${btn})
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, u)
    time.sleep(0.06)`;
      return pyInline(body);
    }
    const btnStr = button === 'right' ? 'using {control down}' : '';
    for (let i = 0; i < n; i++) await osa(`tell application "System Events" to click at {${x}, ${y}}${btnStr}`);
    return `clicked ${n}x (osascript)`;
  }
  if (PLATFORM === 'linux') {
    if (!(await has('xdotool'))) fail('xdotool not installed (sudo apt install xdotool)');
    const b = button === 'right' ? 3 : 1;
    await sh('xdotool', ['mousemove', String(x), String(y)]);
    return sh('xdotool', ['click', '--repeat', String(n), '--delay', '80', String(b)]);
  }
  const dn = button === 'right' ? 8 : 2, up = button === 'right' ? 16 : 4;
  const ps = `Add-Type -MemberDefinition '[DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y); [DllImport("user32.dll")] public static extern void mouse_event(int f,int dx,int dy,int d,int e);' -Name U -Namespace W; [W.U]::SetCursorPos(${x},${y}); for($i=0;$i -lt ${n};$i++){[W.U]::mouse_event(${dn},0,0,0,0);[W.U]::mouse_event(${up},0,0,0,0);Start-Sleep -m 60}`;
  return sh('powershell', ['-NoProfile', '-Command', ps]);
}

export async function mouseMove({ x, y } = {}) {
  return route(() => mouseMoveDirect({ x, y }), ['mouse', String(x), String(y)]);
}

async function mouseMoveDirect({ x, y } = {}) {  if (PLATFORM === 'darwin') {
    if (await hasQuartz()) return pyInline(`import Quartz\ne = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (${x},${y}), 0)\nQuartz.CGEventPost(Quartz.kCGHIDEventTap, e)`);
    return osa(`tell application "System Events"`);
  }
  if (PLATFORM === 'linux') return sh('xdotool', ['mousemove', String(x), String(y)]);
  return sh('powershell', ['-NoProfile', '-Command', `Add-Type -MemberDefinition '[DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);' -Name U -Namespace W; [W.U]::SetCursorPos(${x},${y})`]);
}

export async function scroll({ x, y, direction = 'down', amount } = {}) {
  const argv = ['scroll', direction];
  if (amount) argv.push(String(amount));
  return route(() => scrollDirect({ x, y, direction, amount }), argv);
}

async function scrollDirect({ x, y, direction = 'down', amount } = {}) {
  const cfg = config();
  const lines = amount ?? cfg.scrollLines;
  const d = direction === 'up' ? -1 : 1;
  if (PLATFORM === 'darwin') {
    if (cfg.prefer.scroll !== 'osascript' && (await hasQuartz())) {
      return pyInline(`import Quartz\nev = Quartz.CGEventCreateScrollWheelEvent(None, Quartz.kCGScrollEventUnitLine, ${d}, ${lines})\nQuartz.CGEventPost(Quartz.kCGHIDEventTap, ev)`);
    }
    return osa(`tell application "System Events" to key code ${direction === 'up' ? 126 : 125}`);
  }
  if (PLATFORM === 'linux') return sh('xdotool', ['click', '--delay', '100', '--repeat', String(lines), direction === 'up' ? '4' : '5']);
  fail('scroll on Windows: use page up / page down keys');
}

// ---------- keyboard ----------
const MODS = { cmd: 'command down', ctrl: 'control down', alt: 'option down', opt: 'option down', shift: 'shift down', fn: 'fn down' };
const SPECIAL = new Set(['return', 'enter', 'tab', 'escape', 'esc', 'delete', 'forward delete', 'home', 'end', 'page up', 'page down', 'left arrow', 'right arrow', 'up arrow', 'down arrow', 'space', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']);
const KEYCODES = { return: 36, enter: 36, tab: 48, escape: 53, esc: 53, delete: 51, 'forward delete': 117, home: 115, end: 119, 'page up': 116, 'page down': 121, 'left arrow': 123, 'right arrow': 124, 'up arrow': 126, 'down arrow': 125, space: 49, f1: 122, f2: 120, f3: 99, f4: 118, f5: 96, f6: 97, f7: 98, f8: 100, f9: 101, f10: 109, f11: 103, f12: 111 };
const esc = (s) => String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"');

export async function typeText({ text, via = 'auto' } = {}) {
  return route(() => typeTextDirect({ text, via }), ['type', text]);
}

async function typeTextDirect({ text, via = 'auto' } = {}) {
  const cfg = config();
  const nonAscii = /[^\x20-\x7E\n\t]/.test(text);
  if (PLATFORM === 'linux') return sh('xdotool', ['type', '--delay', '12', '--', text]);
  if (PLATFORM === 'win32') return sh('powershell', ['-NoProfile', '-Command', `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('${text.replace(/'/g, "''")}');`]);
  if (via === 'keystroke' || (via === 'auto' && (!nonAscii || !cfg.clipboardPasteForNonAscii))) {
    return osa(`tell application "System Events" to keystroke "${esc(text)}"`);
  }
  await osa(`set the clipboard to "${esc(text)}"`);
  return osa('tell application "System Events" to keystroke "v" using {command down}');
}

export async function pressKey({ key, modifiers = [] } = {}) {
  const argv = ['key', key, ...(modifiers || []).map((m) => '--' + m)];
  return route(() => pressKeyDirect({ key, modifiers }), argv);
}

async function pressKeyDirect({ key, modifiers = [] } = {}) {
  const k = String(key).trim().toLowerCase();
  const mods = (modifiers || []).map((m) => MODS[m.toLowerCase()]).filter(Boolean);
  if (PLATFORM === 'linux') {
    if (!(await has('xdotool'))) fail('xdotool not installed');
    const map = { cmd: 'super', ctrl: 'ctrl', alt: 'alt', opt: 'alt', shift: 'shift' };
    return sh('xdotool', ['key', '--', [...(modifiers || []).map((m) => map[m.toLowerCase()] || m), k].join('+')]);
  }
  if (PLATFORM === 'darwin') {
    const modStr = mods.length ? ` using {${mods.join(', ')}}` : '';
    if (SPECIAL.has(k)) return osa(`tell application "System Events" to key code ${KEYCODES[k]}${modStr}`);
    if (k.length === 1) return osa(`tell application "System Events" to keystroke "${esc(k)}"${modStr}`);
    fail(`unknown key: ${key} (single char or: ${[...SPECIAL].join(', ')})`);
  }
  const map = { return: '{ENTER}', enter: '{ENTER}', tab: '{TAB}', escape: '{ESC}', esc: '{ESC}', delete: '{DEL}', space: ' ', 'left arrow': '{LEFT}', 'right arrow': '{RIGHT}', 'up arrow': '{UP}', 'down arrow': '{DOWN}' };
  const m = (modifiers || []).map((x) => x.toLowerCase());
  let s = map[k] ?? k;
  if (m.includes('cmd') || m.includes('ctrl')) s = '^' + s;
  if (m.includes('alt')) s = '%' + s;
  if (m.includes('shift')) s = '+' + s;
  return sh('powershell', ['-NoProfile', '-Command', `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('${s}')`]);
}

// ---------- windows ----------
export async function listWindows({ app } = {}) {
  if (PLATFORM === 'darwin') {
    const script = `tell application "System Events"
  set out to ""
  repeat with p in (every process whose background only is false)
    try
      set w to front window of p
      set {px, py} to position of w
      set {ww, wh} to size of w
      set out to out & (name of p) & "|" & (name of w) & "|" & px & "," & py & "|" & ww & "," & wh & linefeed
    end try
  end repeat
  return out
end tell`;
    const out = await osa(script);
    let wins = out.split('\n').filter(Boolean).map((l) => {
      const [proc, title, pos, size] = l.split('|');
      const [x, y] = String(pos || '0,0').split(',').map((v) => Number(String(v).trim()));
      const [w, h] = String(size || '0,0').split(',').map((v) => Number(String(v).trim()));
      return { app: proc, title, x: x || 0, y: y || 0, w: w || 0, h: h || 0 };
    });
    if (app) wins = wins.filter((w) => w.app.toLowerCase().includes(String(app).toLowerCase()));
    return wins;
  }
  if (PLATFORM === 'linux' && (await has('wmctrl'))) {
    const out = await sh('wmctrl', ['-lG']);
    return out.split('\n').filter(Boolean).map((l) => {
      const p = l.split(/\s+/);
      return { app: p[3], title: p.slice(7).join(' '), x: +p[4], y: +p[5], w: +p[6], h: +p[7] };
    });
  }
  fail(`listWindows not supported on ${PLATFORM}`);
}

export async function listApps() {
  if (PLATFORM === 'darwin') {
    const out = await osa('tell application "System Events" to get name of every process whose background only is false');
    return out.split(', ').filter(Boolean);
  }
  if (PLATFORM === 'linux') return sh('sh', ['-c', "ps -eo comm= | sort -u | grep -viE '^(gnome|kde|systemd|dbus|at-spi|gvfs|xdg)' | head -40"]);
  return sh('powershell', ['-NoProfile', '-Command', 'Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object -ExpandProperty ProcessName -Unique']);
}

export async function openApp({ name, url } = {}) {
  if (url) {
    if (PLATFORM === 'win32') return sh('cmd', ['/c', 'start', '', url]);
    return sh(PLATFORM === 'darwin' ? '/usr/bin/open' : 'xdg-open', [url]);
  }
  if (PLATFORM === 'darwin') return sh('/usr/bin/open', ['-a', name]);
  if (PLATFORM === 'linux') return sh('sh', ['-c', `nohup ${name} >/dev/null 2>&1 &`]);
  return sh('powershell', ['-NoProfile', '-Command', `Start-Process '${name}'`]);
}

export async function runApplescript({ script } = {}) {
  if (PLATFORM !== 'darwin') fail('run_applescript is macOS-only');
  return osa(script);
}

// ---------- doctor ----------
// Self-diagnosis: verifies that actions are actually DELIVERED (events can be
// silently dropped when the host process lacks macOS Accessibility/Screen
// Recording permission), not just that backends are installed.
async function cursorPosDarwin() {
  const cc = await cliclickCmd();
  if (cc) {
    const r = await trySh(cc, ['p'], 5000);
    if (r.ok) {
      const [x, y] = r.out.split(',').map((v) => parseInt(v, 10));
      if (!Number.isNaN(x) && !Number.isNaN(y)) return { x, y, via: 'cliclick' };
    }
  }
  if (await hasQuartz()) {
    try {
      const out = await pyInline(`import Quartz, json\nprint(json.dumps(Quartz.CGEventCreate(None).location))`);
      const loc = JSON.parse(out.replace(/'/g, '"'));
      return { x: Math.round(loc.x), y: Math.round(loc.y), via: 'quartz' };
    } catch {}
  }
  return null;
}

async function probeEventDelivery() {
  if (PLATFORM === 'darwin') {
    if (await eventsDelivered()) return { name: 'event_delivery', ok: true, detail: 'CGEvents delivered directly (host process is authorized)' };
    const helper = helperApp();
    if (helper) {
      try {
        const out = await helperTask(['probe', '--json'], 30000);
        if (JSON.parse(out).delivered) return { name: 'event_delivery', ok: true, detail: `direct events blocked, but ${helper.app} IS authorized — actions auto-route through it` };
        return { name: 'event_delivery', ok: false, detail: `events undelivered both directly and via ${helper.app} — click "Allow" in the macOS prompt for TarsX, or add it in System Settings → Privacy & Security → Accessibility` };
      } catch (e) {
        return { name: 'event_delivery', ok: false, detail: `helper probe failed: ${e.message}` };
      }
    }
    return { name: 'event_delivery', ok: false, detail: 'mouse events NOT delivered — host process lacks Accessibility permission; install the TarsX.app helper (scripts/make-app.sh) to fix with one "Allow" click' };
  }
  if (PLATFORM === 'linux' && (await has('xdotool'))) {
    try {
      const out = await sh('xdotool', ['getmouselocation']);
      const before = out.split(' ')[0];
      await sh('xdotool', ['mousemove_relative', '--', '2', '0']);
      const after = (await sh('xdotool', ['getmouselocation'])).split(' ')[0];
      await sh('xdotool', ['mousemove_relative', '--', '-2', '0']);
      return { name: 'event_delivery', ok: before !== after, detail: before !== after ? 'event delivered' : 'event not delivered' };
    } catch (e) {
      return { name: 'event_delivery', ok: false, detail: e.message };
    }
  }
  return { name: 'event_delivery', ok: null, detail: 'not probed on this platform' };
}

export async function doctor() {
  const steps = [];
  const hints = [];
  const d = await info();
  steps.push({ name: 'backends', ok: Object.values(d.backends).some((v) => v.length), detail: d.backends });

  // screenshot probe: real capture, real permission check
  const tmp = path.join(config().screenshotDir, `tarsx-doctor-${randomUUID()}.png`);
  try {
    const file = await screenshot({ out: tmp });
    const size = fs.existsSync(file) ? fs.statSync(file).size : 0;
    steps.push({ name: 'screenshot', ok: size > 1000, detail: size > 1000 ? `${(size / 1024).toFixed(0)} KB → ${file}` : 'file empty' });
    if (size <= 1000) hints.push('screencapture produced an empty file — grant Screen Recording to the host app');
    try { fs.unlinkSync(file); } catch {}
  } catch (e) {
    steps.push({ name: 'screenshot', ok: false, detail: e.message });
    if (PLATFORM === 'darwin') hints.push('System Settings → Privacy & Security → Screen Recording → add the host app (node binary / terminal)');
  }

  steps.push(await probeEventDelivery());
  if (steps[steps.length - 1].ok === false && PLATFORM === 'darwin') {
    hints.push('fix delivery: run scripts/make-app.sh from the skill folder, then click "Allow" on the TarsX prompt — or manually: open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility" and add the host app');
  }
  steps.push({ name: 'keyboard', ok: null, detail: 'not probed (intrusive); type/key need the same Accessibility permission as clicks' });

  return { ok: steps.every((s) => s.ok !== false), platform: PLATFORM, steps, hints, config: d.config };
}
