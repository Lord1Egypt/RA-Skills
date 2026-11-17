#!/usr/bin/env node
// tarsx v2 — flexible CLI front-end for tars-mcp
// Global flags: --json (machine-readable output)
// Commands:
//   screenshot [out.png] [--region x,y,w,h]
//   click <x> <y> [--right] [--double] [--count n]
//   clickwin <AppName> [--offset dx,dy] [--right] [--double]
//   type "text"                       (non-ASCII → clipboard+paste automatically)
//   key <key> [--cmd] [--ctrl] [--alt] [--shift]
//   scroll [up|down] [lines]
//   windows [AppName] | wait <sec> | apps | open <app|url> | osa "script" | info
import * as core from './core.mjs';

const argv = process.argv.slice(2);
const json = argv.includes('--json');
const clean = argv.filter((a) => a !== '--json');
const cmd = (clean[0] || '').toLowerCase();
const rest = clean.slice(1);
const flags = rest.filter((a) => a.startsWith('--'));
const VALUE_FLAGS = ['--region', '--offset', '--count'];
const pos = rest.filter((a, i) => !a.startsWith('--') && !VALUE_FLAGS.includes(rest[i - 1]));
const flagVal = (name) => { const i = clean.indexOf(name); return i >= 0 ? clean[i + 1] : undefined; };
const num = (v) => { const n = Number(v); if (Number.isNaN(n)) throw new Error(`expected number, got: ${v}`); return n; };
const textArgs = () => rest.filter((a, i) => !a.startsWith('--') && !VALUE_FLAGS.includes(rest[i - 1])).join(' ');

const out = (v) => {
  if (json) console.log(typeof v === 'string' ? JSON.stringify({ result: v }) : JSON.stringify(v));
  else if (typeof v !== 'string') console.log(JSON.stringify(v, null, 2));
  else console.log(v);
};

async function windowCenter(app, off) {
  const wins = await core.listWindows({ app });
  if (!wins.length) throw new Error(`no visible window for app: ${app}`);
  const w = wins[0];
  let dx, dy;
  if (off && !Number.isNaN(Number(off.split(',')[0]))) [dx, dy] = off.split(',').map(Number);
  return { x: dx === undefined ? w.x + Math.floor(w.w / 2) : w.x + dx, y: dy === undefined ? w.y + Math.floor(w.h / 2) : w.y + dy, win: w };
}

try {
  switch (cmd) {
    case 'screenshot': {
      out(await core.screenshot({ region: flagVal('--region'), out: pos[0] }));
      break;
    }
    case 'click': {
      const target = pos[0];
      const yv = pos[1];
      const button = flags.includes('--right') ? 'right' : 'left';
      const double = flags.includes('--double');
      const count = num(flagVal('--count') || 1);
      let x, y;
      if (yv === undefined || Number.isNaN(Number(yv))) {
        // click <AppName> --offset dx,dy — click inside named app's window
        const t = await windowCenter(target, flagVal('--offset'));
        x = t.x; y = t.y;
      } else {
        x = num(target); y = num(yv);
      }
      await core.click({ x, y, button, double, count });
      out(`clicked ${x},${y}${button === 'right' ? ' right' : ''}${double ? ' double' : ''}`);
      break;
    }
    case 'clickwin': {
      const app = pos[0];
      if (!app) throw new Error('usage: tarsx clickwin <AppName> [--offset dx,dy]');
      const t = await windowCenter(app, flagVal('--offset'));
      await core.click({ x: t.x, y: t.y, button: flags.includes('--right') ? 'right' : 'left', double: flags.includes('--double') });
      out(`clicked window of ${app} at ${t.x},${t.y} (window ${t.win.x},${t.win.y} ${t.win.w}x${t.win.h})`);
      break;
    }
    case 'type': {
      const text = textArgs();
      if (!text) throw new Error('usage: tarsx type "text"');
      await core.typeText({ text });
      out('typed');
      break;
    }
    case 'key': {
      const modifiers = ['cmd', 'ctrl', 'alt', 'shift'].filter((m) => flags.includes('--' + m));
      await core.pressKey({ key: pos[0], modifiers });
      out(`pressed ${modifiers.map((m) => m + '+').join('')}${pos[0]}`);
      break;
    }
    case 'scroll': {
      await core.scroll({ direction: pos[0] || 'down', amount: pos[1] ? num(pos[1]) : undefined });
      out(`scrolled ${pos[0] || 'down'} ${pos[1] || ''}`.trimEnd());
      break;
    }
    case 'wait': {
      const s = num(pos[0] || 1);
      await new Promise((r) => setTimeout(r, s * 1000));
      out(`waited ${s}s`);
      break;
    }
    case 'windows': {
      out(await core.listWindows({ app: pos[0] }));
      break;
    }
    case 'apps': {
      out(await core.listApps());
      break;
    }
    case 'open': {
      const target = pos[0];
      if (!target) throw new Error('usage: tarsx open <AppName | URL>');
      await (/^https?:\/\//.test(target) ? core.openApp({ url: target }) : core.openApp({ name: target }));
      out(`opened ${target}`);
      break;
    }
    case 'osa': {
      out(await core.runApplescript({ script: textArgs() }));
      break;
    }
    case 'info': {
      out(await core.info());
      break;
    }
    case 'doctor': {
      out(await core.doctor());
      break;
    }
    case 'mouse': {
      await core.mouseMove({ x: num(pos[0]), y: num(pos[1]) });
      out(`moved ${pos[0]},${pos[1]}`);
      break;
    }
    case 'probe': {
      out({ delivered: await core.eventsDelivered() });
      break;
    }
    default: {
      console.log(`tarsx v2 — maximally flexible computer control
  screenshot [out.png] [--region x,y,w,h]
  click <x> <y> [--right] [--double] [--count n]
  clickwin <AppName> [--offset dx,dy] [--right] [--double]
  type "text" | key <key> [--cmd] [--ctrl] [--alt] [--shift]
  scroll [up|down] [lines] | wait <sec>
  apps | windows [AppName] | open <AppName|URL> | osa "script" | info
  doctor                              verify events are actually delivered (permissions)
  add --json anywhere for machine-readable output`);
      process.exit(cmd ? 1 : 0);
    }
  }
} catch (e) {
  if (json) console.log(JSON.stringify({ error: e.message }));
  else console.error('error:', e.message);
  process.exit(1);
}
