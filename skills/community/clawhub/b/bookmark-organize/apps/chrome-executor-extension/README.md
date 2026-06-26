# Chrome Executor Extension

This extension is the local bookmark executor for the OpenClaw bookmark organize skill.

## Responsibilities

- expose bookmark context from Chrome
- validate candidate action plans against the live bookmark tree
- apply supported bookmark actions
- keep a best-effort undo record for the latest apply

## Installation

1. Open `chrome://extensions`
2. Enable Developer Mode
3. Click `Load unpacked`
4. Select the `apps/chrome-executor-extension` folder
5. Start the local bridge server with `npm run bridge:server`
6. Keep Chrome open while using the skill

## Current Status

The service worker implements the bookmark execution logic and a message-based bridge surface.

Current development transport:

- the extension connects to `ws://127.0.0.1:8787/ws`
- the local bridge server exposes HTTP endpoints on `http://127.0.0.1:8787`

This is intended as a first working bridge for local development and can later be replaced by a sturdier transport if needed.
