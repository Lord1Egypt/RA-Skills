---
name: echo
description: Patch a locally installed OpenClaw Control UI so that finishing an assistant reply plays a short Web-Audio chime (multiple selectable presets, in-page 🔔 picker). ClawHub package: echo-cue. Use when the user wants an audible cue when OpenClaw finishes responding (especially in a background tab), asks to install / apply / remove / re-apply this notification-sound local patch, or to restore the patch after `openclaw update` overwrote dist files. Stop-gap mirror of upstream PR openclaw/openclaw#73894 as a zero-build local override; safe to leave installed (auto-skips when upstream lands).
---

# echo 🔔

> ClawHub package name: [`echo-cue`](https://clawhub.com/skills/echo-cue) (the slug `echo` is taken by another publisher; product is called `echo` locally).
>
> Source: <https://github.com/SymbolStar/echoCue>

![echo floating picker widget](https://raw.githubusercontent.com/SymbolStar/echoCue/main/docs/widget.png)

*Click the floating 🔔 in the bottom-right corner to open the picker: enable / disable, choose a preset, Preview each sound — no DevTools required.*

A zero-build local patch for OpenClaw Control UI (webchat) that plays a short
two-tone chime (A5 → E5, ~900ms) when an assistant reply finishes streaming.
Designed as a stop-gap until upstream PR
[openclaw/openclaw#73894](https://github.com/openclaw/openclaw/pull/73894)
(issue [#69186](https://github.com/openclaw/openclaw/issues/69186)) lands.

## Why this exists

OpenClaw Control UI has no completion sound on `main` yet. PR #73894 implements
it but has been OPEN without review since 2026-04-29. This skill injects an
equivalent IIFE into the bundled UI dist so it works **today**, and gracefully
steps aside when upstream ships.

## What you get

- Short ding-dong when the assistant finishes a reply
- Skipped for `NO_REPLY` / empty silent completions
- Always rings by default (foreground + background); set `onlyHidden=on` to limit to hidden tabs only
- 4-second hard rate-limit + content-fingerprint dedup → never double-rings on streaming re-renders
- Per-browser localStorage toggles (no UI surface added)
- One-shot apply / remove with backup
- Cache-bust: rewrites `index.html` to a new bundle filename so plain Cmd+R picks up the patch
- Patches **every** detected OpenClaw install (brew + nvm + OPENCLAW_HOME) so it works
  even when Gateway runs under a different node than `which openclaw` resolves
- Auto-detects upstream PR landing → skips itself

## Install

```bash
bash apply.sh
```

Then refresh your Control UI browser tab (regular Cmd+R is enough, the script
cache-busts the bundle filename). Click or press a key once on the page to
unlock the AudioContext (this happens automatically the first time you send a
message).

## Verify

DevTools console:

```js
window.__milly_cue_v1__   // → true
```

Send a question, switch to another tab — you should hear a ding-dong when the
assistant finishes.

## Toggle (per browser)

```js
// Disable entirely
localStorage.setItem('milly.completionCue', 'off')

// Re-enable
localStorage.removeItem('milly.completionCue')

// Ring even when the tab is in foreground (default behaviour as of 0.2.0):
localStorage.removeItem('milly.completionCue.onlyHidden')

// Limit ringing to hidden / unfocused tabs only:
localStorage.setItem('milly.completionCue.onlyHidden', 'on')
```

## Sound presets

Click the floating 🔔 button (bottom-right of Control UI) to open the picker:
enable / disable, switch preset (with Preview button per row), toggle
"Only when tab is hidden". Settings are stored in `localStorage` per browser.

| key | group | description |
|---|---|---|
| `chime` *(default)* | Basic | Original two-tone bell (A5 → E5, ~900ms). 叮咚。 |
| `tritone` | Basic | Approximation of the classic iPhone SMS "Tri-tone" — three quick bright pings (E6 / C6 / G6, ~420ms). |
| `pop` | Basic | Single bubble pop — quick upward swoop, ~110ms. 🫭 |
| `twinkle` | Basic | Fast C → E → G arpeggio (triangle, ~280ms). ✨ |
| `droplet` | Basic | Water droplet — downward sine sweep (1600 → 520 Hz, ~180ms). 💧 |
| `fishbite` | Animal Crossing | Fish-bite plonk (low sine plop + tiny splash, ~220ms). 🐟 |
| `villager` | Animal Crossing | Dialog "blip" — soft triangle chirp like villagers talking (~90ms). 🐾 |
| `acbell` | Animal Crossing | Item ding — single bright bell tone with shimmer (~260ms). 🔔 |
| `coin` | Super Mario | Classic two-note coin chirp (B5 → E6 square, ~220ms). 🪙 |
| `mariojump` | Super Mario | Jump — fast upward square pitch sweep (~150ms). 🍄 |
| `oneup` | Super Mario | 1-Up fanfare — ascending arpeggio E5-G5-E6-C6-E6-G6 (~450ms). 🍄 |
| `powerup` | Super Mario | Mushroom power-up — fast ascending climb (~360ms). 🌟 |
| `pipe` | Super Mario | Warp pipe — descending square slide (~280ms). 🟢 |
| `bump` | Super Mario | Block bonk — short low square thump with a click (~120ms). 🧱 |
| `nokia` | Retro | Nokia tune — iconic 13-note phrase from Tárrega's *Gran Vals* (square, ~1.2s). 📱 |
| `modem` | Retro | Dial-up modem mini-impression — hi/low tones + brief screech tail (~600ms). 📞 |

Add more presets by appending to the `SOUNDS` array in
`inject/completion-cue.iife.js` (each entry needs `key`, `label`, `play(ctx, master)`),
then re-run `bash apply.sh`. The widget picks them up automatically.

### Hide the floating button

```js
localStorage.setItem('milly.completionCue.widget', 'off')
localStorage.removeItem('milly.completionCue.widget')   // bring it back
```

DevTools fallback (still works):

```js
__milly_cue_sounds__              // list available presets
__milly_cue_preview__('tritone')  // preview without sending a message
localStorage.setItem('milly.completionCue.sound', 'tritone')
```

## Uninstall

```bash
bash remove.sh
```

Restores the original bundle from `index-*.js.milly.bak` and the original
`index.html` from `index.html.milly.bak`.

## After `openclaw update`

The update overwrites `dist/control-ui/...`, dropping the patch. Re-run:

```bash
bash apply.sh
```

`apply.sh` is idempotent and detects upstream:

- Already patched → skip
- Upstream `responseCompletionSound` shipped → skip + advise uninstall

## Known limits

- Anchor: `.chat-group.assistant` DOM class. If OpenClaw renames it the patch
  silently does nothing (fail-quiet, no breakage).
- AudioContext requires one user gesture per page load (browser policy).
- Webchat only. TUI / iOS / macOS / Android clients are not covered (they have
  their own native notification stacks).
- Single audible cue per assistant turn regardless of message length.

## File layout

| File | Purpose |
|---|---|
| `apply.sh` | Detect every OpenClaw install, idempotent inject IIFE, backup, cache-bust |
| `remove.sh` | Restore from `.milly.bak` files |
| `inject/completion-cue.iife.js` | The patch payload |
| `tests/manual.md` | 7-step verify checklist |

## Related

- Issue: [openclaw/openclaw#69186](https://github.com/openclaw/openclaw/issues/69186)
- Upstream PR (stop-gap target): [openclaw/openclaw#73894](https://github.com/openclaw/openclaw/pull/73894)
- Sibling skill (same pattern): `agent-tab-title`
