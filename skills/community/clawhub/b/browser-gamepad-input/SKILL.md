---
name: browser-gamepad-input
description: Read game controllers correctly in the browser with the Gamepad API and build controller testers that measure stick drift, circularity, built-in deadzones, analog triggers and vibration. Use when writing or debugging web code that calls navigator.getGamepads(), listens for gamepadconnected, or handles controller input in a game or tester page.
---

# Browser gamepad input

These are the patterns behind HLPlanet's stick drift tester (https://www.hlplanet.com/gamepad-tester/), which you can use as a working reference.

## Reading controllers

- Poll `navigator.getGamepads()` in a `requestAnimationFrame` loop. Chromium returns a new snapshot on every call, so never keep a `Gamepad` object between frames.
- Browsers hide controllers until the user presses a button on one while the page is visible. Show a "press any button" prompt, and poll every frame so controllers that connected before your script ran are found too.
- The API needs a secure context (HTTPS or localhost). If the page runs in a cross-origin iframe, add `allow="gamepad"` to the iframe, because some browsers block access there otherwise.
- Data stops while the tab is hidden. Pause any timed test on `visibilitychange`.
- With several controllers connected, follow the one where a button was pressed last.

```js
let active = null;
function frame() {
  const pads = [...navigator.getGamepads()].filter((p) => p && p.connected);
  const pressed = pads.find((p) => p.buttons.some((b) => b.pressed));
  const pad = pressed || pads.find((p) => p.index === active) || pads[0] || null;
  active = pad ? pad.index : null;
  if (pad) handle(pad); // read pad.axes and pad.buttons here
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

## Mapping

- Check `pad.mapping === 'standard'` before trusting indexes. With a non-standard mapping, sticks and buttons can be in any order, so warn the user.
- Standard axes are `0` and `1` for the left stick, `2` and `3` for the right stick. Positive Y means down.
- Standard buttons are: 0 A/Cross, 1 B/Circle, 2 X/Square, 3 Y/Triangle, 4 LB, 5 RB, 6 LT, 7 RT, 8 View/Share, 9 Menu/Options, 10 L3, 11 R3, 12 to 15 the D-pad (up, down, left, right), and 16 Home.
- Read triggers from `buttons[6].value` and `buttons[7].value`, which run from 0 to 1. Don't use `.pressed`, because its threshold varies by browser. With non-standard mappings, triggers often show up as axes that rest at -1, so convert them with `(v + 1) / 2`.
- Don't rely on `pad.id` to identify the exact model. On Windows, every XInput controller reports a similar generic name.

## Stick drift

Ask the user to let go of both sticks, record for about 4 seconds, and report the **peak** distance from the center, `Math.hypot(x, y)`. These are the bands HLPlanet's tester uses:

| Peak distance at rest | Verdict |
|---|---|
| below 0.05 | No drift |
| 0.05 to 0.10 | Slight drift |
| 0.10 to 0.20 | Drift |
| 0.20 and above | Severe drift |

**Built-in deadzones hide drift.** A controller with a built-in deadzone outputs exactly `0` near the center and then jumps to the edge of the deadzone. Track whether you saw exact zeros and the smallest non-zero distance:
- No exact zeros: the raw output is exposed.
- Exact zeros with a smallest non-zero distance of 0.02 or more: the deadzone is about that size, and small drift may be masked.

## Circularity

1. Ask the user to rotate each stick slowly along the outer edge.
2. Keep the maximum distance for each of 360 one-degree bins, counting only samples where the stick is more than 0.5 from the center.
3. Fast rotations skip degrees between frames, so fill the skipped bins by interpolating between the previous sample and the current one (only for gaps of 45° or less).
4. The error is the average of `|1 - max|` over the filled bins, shown as a percentage.
5. Only show the result once at least 90 bins (25% coverage) are filled, and show the coverage next to it.

## Vibration

```js
const act = pad.vibrationActuator;
if (typeof act?.playEffect === 'function') {
  act.playEffect('dual-rumble', { startDelay: 0, duration: 300, weakMagnitude: 0.5, strongMagnitude: 1 });
}
const hasTriggerRumble = Array.isArray(act?.effects) && act.effects.includes('trigger-rumble');
```

Firefox may expose `pad.hapticActuators` instead of `vibrationActuator`. Feature-detect both, and disable the buttons the browser can't drive rather than failing silently.

## Don't overclaim

- **Polling rate:** the browser samples controllers on its own schedule, so the Gamepad API can't measure a controller's USB or wireless polling rate. Use `pad.timestamp` only to tell whether new data arrived. HLPlanet explains how to test polling rate outside the browser at https://www.hlplanet.com/how-to-test-polling-rate-of-controller/.
- **Resolution:** an estimate from the smallest step between distinct axis values is a hint, not a measurement. For example, 8-bit sticks move in steps of about 2/255.
