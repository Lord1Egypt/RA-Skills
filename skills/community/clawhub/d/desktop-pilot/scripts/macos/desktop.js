// Desktop Pilot - macOS backend (JXA, built in; needs Accessibility + Screen Recording permission for the terminal/agent).
// Usage: osascript -l JavaScript desktop.js <action> [--process P] [--title T] [--name N] [--text T] [--keys K] [--x N --y N] [--button B] [--out path]
ObjC.import('Cocoa');
ObjC.import('CoreGraphics');

function run(argv) {
  const action = argv[0] || 'help';
  const opt = {};
  for (let i = 1; i < argv.length; i++) if (argv[i].startsWith('--')) opt[argv[i].slice(2)] = argv[i + 1], i++;
  const se = Application('System Events');
  const app = Application.currentApplication(); app.includeStandardAdditions = true;

  const procs = () => {
    let list = se.processes.whose({ visible: true })();
    if (opt.process) list = list.filter(p => p.name().toLowerCase() === opt.process.toLowerCase());
    if (opt.title) list = list.filter(p => p.windows().some(w => (w.name() || '').includes(opt.title)));
    if (!list.length) throw new Error('No visible app matches ' + (opt.process || opt.title || '(specify --process or --title)'));
    return list;
  };
  const windowsOf = p => p.windows().filter(w => !opt.title || (w.name() || '').includes(opt.title));
  const firstWindow = () => { for (const p of procs()) { const w = windowsOf(p); if (w.length) return [p, w[0]]; } throw new Error('No window (app may be hidden: open it first)'); };
  const clickable = ['AXButton', 'AXMenuItem', 'AXCheckBox', 'AXRadioButton', 'AXLink', 'AXTab', 'AXPopUpButton', 'AXMenuButton'];
  const label = el => { try { return el.name() || el.description() || el.title() || ''; } catch (e) { return ''; } };

  const mouse = (x, y, kind) => {
    const pt = $.CGPointMake(x, y);
    const post = (type, btn, clicks) => { const e = $.CGEventCreateMouseEvent(null, type, pt, btn); if (clicks) $.CGEventSetIntegerValueField(e, $.kCGMouseEventClickState, clicks); $.CGEventPost($.kCGHIDEventTap, e); };
    post($.kCGEventMouseMoved, $.kCGMouseButtonLeft);
    if (kind === 'move') return;
    if (kind === 'right') { post($.kCGEventRightMouseDown, $.kCGMouseButtonRight); post($.kCGEventRightMouseUp, $.kCGMouseButtonRight); return; }
    const n = kind === 'double' ? 2 : 1;
    for (let c = 1; c <= n; c++) { post($.kCGEventLeftMouseDown, $.kCGMouseButtonLeft, c); post($.kCGEventLeftMouseUp, $.kCGMouseButtonLeft, c); }
  };
  const keyCodes = { enter: 36, return: 36, tab: 48, space: 49, backspace: 51, delete: 117, esc: 53, escape: 53, left: 123, right: 124, down: 125, up: 126,
    home: 115, end: 119, pageup: 116, pagedown: 121, f1: 122, f2: 120, f3: 99, f4: 118, f5: 96, f6: 97, f7: 98, f8: 100, f9: 101, f10: 109, f11: 103, f12: 111 };
  const modMap = { cmd: 'command down', command: 'command down', ctrl: 'control down', control: 'control down', alt: 'option down', option: 'option down', shift: 'shift down' };

  switch (action) {
    case 'screenshot': {
      const out = opt.out || '/tmp/desktop-pilot.png';
      app.doShellScript('screencapture -x ' + JSON.stringify(out).replace(/"/g, "'"));
      return 'OK screenshot ' + out;
    }
    case 'windows':
      return se.processes.whose({ visible: true })().flatMap(p => p.windows().map(w => p.unixId() + '\t' + p.name() + '\t' + (w.name() || ''))).join('\n');
    case 'buttons': {
      const [p, w] = firstWindow(); const lines = ['[window] ' + (w.name() || p.name())];
      w.entireContents().forEach(el => { try { const r = el.role(); const l = label(el); if (clickable.includes(r) && l) lines.push('  ' + r + '\t' + l); } catch (e) {} });
      return lines.join('\n');
    }
    case 'click': {
      if (!opt.name) throw new Error('Specify --name <visible label>');
      const [p, w] = firstWindow();
      const el = w.entireContents().find(e => { try { return label(e) === opt.name; } catch (x) { return false; } });
      if (!el) throw new Error("Control not found: '" + opt.name + "' (run 'buttons' to list exact labels)");
      p.frontmost = true; el.actions.byName('AXPress').perform();
      return "OK clicked '" + opt.name + "'";
    }
    case 'close': {
      const [p, w] = firstWindow();
      const btn = w.buttons().find(b => { try { return b.subrole() === 'AXCloseButton'; } catch (e) { return false; } });
      if (!btn) throw new Error('Window has no close button');
      btn.click(); return "OK closed '" + (w.name() || p.name()) + "'";
    }
    case 'focus': { const [p, w] = firstWindow(); p.frontmost = true; try { w.actions.byName('AXRaise').perform(); } catch (e) {} return "OK focused '" + (w.name() || p.name()) + "'"; }
    case 'type': {
      if (!opt.text) throw new Error('Specify --text');
      if (opt.process || opt.title) { firstWindow()[0].frontmost = true; delay(0.3); }
      se.keystroke(opt.text); return 'OK typed ' + opt.text.length + ' chars';
    }
    case 'key': {
      if (!opt.keys) throw new Error('Specify --keys (cmd+c, enter, alt+f4...)');
      if (opt.process || opt.title) { firstWindow()[0].frontmost = true; delay(0.3); }
      const parts = opt.keys.toLowerCase().split('+'); const k = parts.pop();
      const using = parts.map(m => { if (!modMap[m]) throw new Error('Unsupported modifier ' + m); return modMap[m]; });
      if (k in keyCodes) se.keyCode(keyCodes[k], { using }); else se.keystroke(k, { using });
      return 'OK keys ' + opt.keys;
    }
    case 'mouse': {
      const x = Number(opt.x), y = Number(opt.y);
      if (!(x >= 0 && y >= 0)) throw new Error('Specify --x and --y (points, from the screenshot)');
      mouse(x, y, opt.button || 'left'); return 'OK mouse ' + (opt.button || 'left') + ' at ' + x + ',' + y;
    }
    default:
      return 'actions: screenshot | windows | buttons | click --name | close | focus | type --text | key --keys | mouse --x --y [--button]';
  }
}
