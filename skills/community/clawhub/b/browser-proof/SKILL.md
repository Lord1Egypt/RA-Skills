---
name: browser-proof
description: Browser Proof is a public ClawHub browser-QA evidence skill. Use it when the user says "browser proof", "browser QA report", "browser debugging evidence", or wants a machine-readable bundle with steps, artifacts, checks, and a shareable report.
version: 1.0.5
homepage: https://github.com/zack-dev-cm/browser-proof
license: MIT-0
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/browser-proof","skillKey":"browser-proof","requires":{"anyBins":["python3","python"]}}}
---

# Browser Proof

Search intent: `browser proof`, `browser QA`, `browser debugging evidence`, `QA evidence pack`

## Goal

Turn a browser session into a release-grade evidence pack:

- one machine-readable session manifest
- one ordered step log
- one structural bundle check
- one shareable markdown report

This skill is for browser evidence capture and handoff quality.
It does not replace Playwright, OpenClaw, or a test runner.

## Use This Skill When

- the user wants a reproducible browser bug report instead of loose screenshots
- a launch or QA flow needs a shareable proof bundle
- browser debugging needs expected result, actual result, and artifacts captured in one place
- you need a clean handoff from OpenClaw, Playwright, or manual QA to another engineer
- the same browser issue keeps getting re-explained from chat history instead of one artifact bundle
- a Chrome extension publish or review flow needs proof against the exact packaged ZIP and browser version

## Quick Start

1. Initialize the session manifest.
   - Use `python3 {baseDir}/scripts/init_browser_proof_session.py --out <json> --session-id <id> --app <name> --goal <goal>`.
   - Add `--base-url`, repeatable `--surface`, and optional `--run-context` or `--environment` fields.

2. Append each browser step as you go.
   - Use `python3 {baseDir}/scripts/append_browser_proof_step.py --manifest <json> --step-id <id> --action <text> --expected <text> --actual <text> --status passed|failed|blocked`.
   - Attach evidence with `--screenshot`, `--dom-dump`, `--console-log`, `--network-log`, `--video`, and repeatable `--issue-key`.

3. Check the bundle before sharing it.
   - Use `python3 {baseDir}/scripts/check_browser_proof_bundle.py --manifest <json> --repo-root <repo> --out <json>`.
   - Fix missing screenshots, absolute paths, empty failed-step notes, or missing session metadata before publishing the report.

4. Render the report.
   - Use `python3 {baseDir}/scripts/render_browser_proof_report.py --manifest <json> --out <md>`.
   - Share the rendered markdown instead of rewriting the run from memory.

## Operating Rules

### Session rules

- Keep one manifest per browser run or tightly related run batch.
- Record the app, goal, base URL, and surfaces near the start.
- Prefer relative artifact paths so the bundle is portable.

### Step rules

- Every step should say what you tried, what you expected, and what actually happened.
- Failed steps should include either a note or at least one issue key.
- Attach a screenshot for every failed step and for important checkpoints.
- Keep statuses limited to `passed`, `failed`, or `blocked`.

### Chrome extension rules

- Record the exact ZIP or unpacked extension path, manifest version, extension ID when available, and Chrome version in session metadata or the first step.
- For action popup flows, record the selected text or input source, action clicked, target language or option, and observed result.
- Capture extension errors, console output, and API availability states when the claim depends on browser APIs.
- If a Chrome Web Store draft is already pending review, capture status evidence only; do not turn a proof run into a cancel/resubmit instruction unless a verified acceptance blocker exists.

### Bundle rules

- Do not store secrets, cookies, or raw tokens in notes or artifact paths.
- Avoid absolute filesystem paths in the final manifest.
- Check the bundle before sending it to GitHub, Linear, Slack, or a release channel.

## Bundled Scripts

- `scripts/init_browser_proof_session.py`
  - Create a machine-readable session manifest for a browser QA or debugging run.
- `scripts/append_browser_proof_step.py`
  - Append one evidence-backed step to the session manifest.
- `scripts/check_browser_proof_bundle.py`
  - Validate bundle structure, artifact paths, and minimum evidence quality.
- `scripts/render_browser_proof_report.py`
  - Render a concise markdown report from the session manifest.
