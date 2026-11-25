---
name: browser-keyboard-testing
description: Build and debug browser keyboard testers and physical-key handling, covering KeyboardEvent.code vs key, keys the browser never sees, rollover and ghosting, key chatter, rapid trigger tap tests and SOCD / Snap Tap detection. Use when writing code that tracks which physical keys are held, a keyboard tester page, or keyboard input for games in the browser.
---

# Browser keyboard testing

These are the patterns behind HLPlanet's online keyboard tester (https://www.hlplanet.com/online-keyboard-tester-tool/) and the open-source Rapid Trigger & SOCD Tester (https://github.com/hlplanet/rt-socd-tester), which you can use as working references.

## Track physical keys

- Key the state by `event.code` (the physical position, such as `KeyA` or `IntlBackslash`), not `event.key`, which changes with the layout, Shift and dead keys.
- To label keys with the user's real layout, use `navigator.keyboard.getLayoutMap()` where it exists (Chromium), and fall back to US labels.
- ISO and JIS boards have extra codes: `IntlBackslash`, `IntlYen` and `IntlRo`. Include them in the drawn layout.
- Skip `event.repeat` events when counting presses, because auto-repeat is not a new press.
- Skip events where `event.isComposing` is true, so an IME doesn't produce phantom presses.
- `preventDefault()` on handled keys keeps Space, the arrow keys and `'` or `/` (quick find in Firefox) from scrolling or searching the page.

## Keys the browser misses or garbles

- **Fn** is handled inside the keyboard and never reaches the browser. Say so in the UI instead of drawing a dead key.
- **PrintScreen** on Windows usually arrives as `keyup` only. Count a press on `keyup` when no `keydown` came first.
- **macOS:** while Cmd is held, `keyup` for other keys is often never fired. Release every held key when Meta goes up.
- **Focus loss:** Alt+Tab or a click outside the window loses `keyup`. Clear all held keys on `blur` and on `visibilitychange`.
- **Browser and OS shortcuts:** Ctrl/Cmd+W, T, N and Alt+F4 can't be blocked. In fullscreen, Chromium's Keyboard Lock API (`navigator.keyboard.lock()`) can capture most of them, including Escape.

## Rollover and ghosting

- Show the highest number of keys held at once.
- Tell the user that a held key that doesn't light up means a rollover limit (6KRO is common on office keyboards) or a ghosting combination.
- The browser only sees what the OS reports, so it can't tell ghosting from a combination the keyboard blocks on purpose.

## Key chatter

Flag a key that fires `keydown` again within **20 ms** of its own `keyup`. A finger can't re-press that fast, so it's the switch bouncing. HLPlanet's tester uses that threshold.

```js
const CHATTER_MS = 20;
const lastUp = {};
addEventListener('keydown', (e) => {
  if (e.repeat || e.isComposing) return;
  const gap = e.timeStamp - (lastUp[e.code] ?? -Infinity);
  if (gap < CHATTER_MS) markChatter(e.code, gap);
});
addEventListener('keyup', (e) => { lastUp[e.code] = e.timeStamp; });
```

## Rapid trigger tap test

- Browsers only see press and release, never how deep a key is pressed. Reading actuation depth needs the keyboard maker's SDK or WebHID with the vendor's protocol. Don't claim to read depth from `KeyboardEvent`.
- Have the user tap one key as fast as they can for 5 or 10 seconds. Report taps per second, the peak tap rate, the average press length, and the shortest **release gap** (time from `keyup` to the next `keydown`).
- Rapid trigger resets a key as soon as it starts rising, so the release gap is where it shows up. Compare keyboards or settings with the same test.

## SOCD / Snap Tap detection

- SOCD (Snap Tap, Snappy Tappy) means that when two opposite keys are both held, the keyboard reports only the most recent one.
- **Test:** the user holds A, then presses and releases D while still holding A.
- **With SOCD on**, the keyboard itself sends `keyup` for A within a few milliseconds of `keydown` for D, then `keydown` for A again when D is released. HLPlanet's tester treats a swap within **6 ms** as done by the keyboard, because no finger is that fast.
- **With SOCD off**, both keys stay down while they overlap.
- Count overlaps and instant swaps over several tries. Report "mixed" when they disagree, which can happen with first-input or neutral SOCD modes.
- Work with A/D, W/S and the left/right arrows.

## Timing caveats

- `event.timeStamp` and `performance.now()` are coarsened by the browser, often to between 0.1 and 1 ms, and more with privacy settings.
- The OS also batches input, so a browser page can't measure keyboard latency or polling rate.
- Report gaps to 0.1 ms at most, and call them estimates.
