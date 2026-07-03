// JXA keycode poster — posts raw keycodes (optionally with cmd) to a specific PID
// via CGEventPostToPid. This is what makes dia-ask-v2 focus-safe: events are
// delivered to Dia's process, not the frontmost app, so they neither steal focus
// nor collide with the user's own typing in another app.
//
//   osascript -l JavaScript dia-cgpost.js <pid> <kc[:cmd]> <kc[:cmd]> ...
//   e.g. dia-cgpost.js 1501 0:cmd 51 9:cmd   (Cmd+A, Delete, Cmd+V)
//
// Why keycodes and not CGEventKeyboardSetUnicodeString: Dia's React input ignores
// the unicode-string carried by a posted event (validated 2026-06-08 spike) — it
// only honors real keycodes. Arbitrary unicode therefore travels via the clipboard
// (set by the caller) + Cmd+V here.
'use strict';
ObjC.import('CoreGraphics');
ObjC.import('Foundation');
const CMD = 0x100000;   // kCGEventFlagMaskCommand
const SHIFT = 0x20000;  // kCGEventFlagMaskShift

// Per-key pacing (seconds). Dia's web input drops events posted back-to-back with
// no gap (validated 2026-06-08: a 13-digit filename lost characters at 0ms). A
// few ms between key down/up reliably lands every keystroke. Override with the
// 2nd CLI arg "--gap <ms>" if needed.
function run(argv) {
  let gap = 0.009;
  const a = argv.slice();
  const gi = a.indexOf('--gap');
  if (gi !== -1) { gap = (parseFloat(a[gi + 1]) || 9) / 1000; a.splice(gi, 2); }

  const pid = parseInt(a[0], 10);
  if (!pid) return 'ERROR: missing pid';
  const src = $.CGEventSourceCreate(0); // kCGEventSourceStateCombinedSessionState
  if (gap) $.NSThread.sleepForTimeInterval(0.04); // settle: first posted event is otherwise dropped
  let n = 0;
  for (let i = 1; i < a.length; i++) {
    const parts = String(a[i]).split(':');
    const kc = parseInt(parts[0], 10);
    if (Number.isNaN(kc)) continue;
    let flags = 0;
    for (let j = 1; j < parts.length; j++) {
      if (parts[j] === 'cmd') flags |= CMD;
      else if (parts[j] === 'shift') flags |= SHIFT;
    }
    const d = $.CGEventCreateKeyboardEvent(src, kc, true);
    const u = $.CGEventCreateKeyboardEvent(src, kc, false);
    if (flags) { $.CGEventSetFlags(d, flags); $.CGEventSetFlags(u, flags); }
    $.CGEventPostToPid(pid, d);
    if (gap) $.NSThread.sleepForTimeInterval(gap);
    $.CGEventPostToPid(pid, u);
    if (gap) $.NSThread.sleepForTimeInterval(gap);
    n++;
  }
  return `posted ${n} keycodes to pid ${pid}`;
}
