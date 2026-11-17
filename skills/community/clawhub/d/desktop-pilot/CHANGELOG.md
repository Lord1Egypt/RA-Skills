# Changelog

## 1.0.1
- **Windows: input never lands in the wrong window.** `focus`, `type`, `key` and the click fallback now bring the target to the foreground (thread-attach / ALT fallbacks for Windows' foreground lock) and verify it; if that fails they stop with `FOCUS_FAILED` instead of typing blind. Without `--process`/`--title`, `type`/`key` print which window received the input.
- **New: "agent is working" overlay (Windows/WSL).** `overlay start|text|stop|status|clear|lock|unlock|selftest`: glow around the screen edges (click-through) + status pill with a Stop button, hidden from screenshots by default, self-closing when the agent stops acting. Pressing Stop makes every later action abort with exit code 3 (`STOPPED_BY_USER`).
- **New: optional input lock** (`overlay start --lock 1`): a low-level keyboard/mouse hook ignores the user's physical input while the agent acts; the agent's own input always passes. Safety nets: mouse movement and the Stop button never blocked, hold Esc 1.5 s to release, lapses 8 s after the last action, 10 min cap. Tested live: physical keys and clicks swallowed, agent input and mouse movement passed.
- **New: `scripts/browser/overlay.js`**, the same overlay inside a page for Playwright/CDP/Puppeteer (`window.__dpOverlay`).
- Description clarified: nothing to install on Windows/macOS; Linux needs xdotool and wmctrl.

## 1.0.0
First release: screenshots, window list, click controls by name, close/focus, Unicode typing, key combos, coordinate clicks on Windows, macOS, Linux and WSL.
