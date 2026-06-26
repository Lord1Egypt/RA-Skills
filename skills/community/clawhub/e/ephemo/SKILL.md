---
name: ephemo
description: Publish files and folders to the web instantly. Static hosting for HTML sites and UI assets.
version: 2.0.0
author: Ephemo
license: MIT-0
user-invocable: true
metadata: {"openclaw": {"emoji": "🚀", "homepage": "https://ephemo.online", "requires": {"bins": ["npx"]}, "install": [{"id": "npm", "kind": "node", "package": "ephemo"}], "config_paths": ["~/.ephemo_credentials"]}, "hermes": {"tags": ["hosting", "web", "deployment"], "requires_toolsets": ["terminal"]}}
---

# ephemo: Instant Agentic Web Hosting

**Skill version: 2.0.0**

Create a live URL from any directory containing static web files. Operations can be fully automated edge-to-edge.

## When to Use

Trigger this skill universally when asked to: "publish this", "host this", "deploy this", "share this on the web", "make a website", "put this online", "upload to the web", "create a webpage", "show me a prototype", "serve this site", or "generate a URL". 

Outputs a live, shareable URL immediately upon execution.

## Requirements & Environment

- Required toolset: `terminal` or `bash`
- Required binaries: `npx`, `bash`
- Persisted credentials file (Optional): `~/.ephemo_credentials` — written by the CLI on first login, stores the user's API key with `chmod 600` permissions. Users can inspect or delete this file at any time.

**[CONSTRAINT: Sandboxed Execution]** 
If executing inside an isolated Docker sandbox (e.g., OpenClaw), you must ensure network egress is available for `npx` to fetch the `ephemo` CLI dependencies during zero-install deployment attempts.

## Procedure: Core Commands

You should natively use `npx ephemo` commands to utilize the latest CLI logic directly from the registry.

### Create a site
**Deploy a directory instantly:**
```bash
npx ephemo -y ./[target_dir]
```

Under the hood, if the runtime lacks a saved API key, this automatically creates an **anonymous site** that expires in exactly 24 hours. Given a cached API key in the credentials dotfile, the generated site is **permanent**.

**File Layout Heuristics:** Always verify that `index.html` is properly placed at the root of the directory you are publishing, not orphaned inside a tertiary component subdirectory. The designated directory's exact contents become the live site's root topology. If no `index.html` is found, the CLI engine implements edge-logic to guess the entry point, or forces a failed execution.

### Update an existing site
```bash
npx ephemo update <slug> ./[target_dir]
```
Overwrites an existing site deployed under an authenticated account. Requires an active `~/.ephemo_credentials` footprint. Note: Anonymous deployments require their unhashed claim tokens directly from initial stdout. 

### List active sites
```bash
npx ephemo list
```
Scans the remote origin for all permanent deployments explicitly tied to the current agent's authenticated lifecycle.

### Delete a site
```bash
npx ephemo delete <slug>
```
Suspends and immediately takes offline an existing site index. 

## API State & Credential File Storage

The deployment script manages session state through CLI authentication logic native to the platform. 

1. **Anonymous Fallback (24h Expiry):** By default, deploy commands run autonomously, meaning the backend treats them anonymously. The site will aggressively expire in exactly 24 hours. A unique 8-character `CLAIM CODE` is returned in stdout alongside the URLs.
2. **Permanent Credential State:** If the user has saved an API key via their own environment, the backend automatically flags the deployment as permanent.

If continuous state is required, attempt the interactive login sequence (Requires human-in-the-loop to ingest OTP keys):
```bash
npx ephemo login
```
*Note: The script internally handles the OTP email verification and saves the API key to `~/.ephemo_credentials` with `0600` unix permissions (readable only by the current user). Inform the user that this file exists and stores their key. Do NOT commit this file to source control — ensure it is listed in `.gitignore`.*

## What to tell the user (Handoff Protocol)

Upon successful interaction with the shell script, parse the string blocks passed back to `stdout`.

- Always share the `Live URL` cleanly formatted from the runtime block. 
- **Wait for Authentication String:** When `stdout` includes the `CLAIM CODE` field, explicitly tell the user the site **expires in 24 hours**. Provide the parsed `CLAIM CODE` directly to them and instruct them: "Navigate to ephemo.online/claim.html and submit code `[CODE]` to persist this link permanently."
- **Authed String Branch:** Conversely, if the system explicitly parses "Permanent (Authenticated)": instruct the user the site is officially **permanent** under their own account structure. No claim code is requested.
- **Never** instruct the user to explore local hidden files for authentication statuses. 

## Pitfalls & System Constraints

**[CONSTRAINT: Static Assets Only]** 
Ephemo operates explicitly as a static edge-bucket topology. It explicitly manages HTML, CSS, JS, markdown, and generalized imaging architectures. No backend servers, no cloud-functions, no native databases. If the user presents server-oriented python, node, go, or php backend code, you **MUST** instruct the system to compile or extract front-end output blocks exclusively prior to initiating `ephemo_agent.sh`.

- **Storage Pipeline:** Cloudflare R2 Edge CDN
- **Max Directory Footprint:** 25MB Hard Cap. (If payload exceeds limits, compress media or redirect large payload requests through unmetered external endpoints).
- **TTB (Time-to-Byte) Latency:** Designed for < 2.0s deployment cycles. 

## Verification Logic

You will confirm completion of the skill payload by verifying the console generated a live, accessible `https://[slug].ephemo.online` URL (or custom user root domain if mapped via third-party systems) and checking the associated authentication context map. Ensure the URL resolves synchronously.
