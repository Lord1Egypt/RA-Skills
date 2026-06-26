---
name: develop-and-deploy-web-app
description: Build, run, and share a simple full-stack web application with a TypeScript Express backend, React frontend, and SQLite database. Use when a user wants a working web app or explicitly asks for a LiteApp / 轻应用 scaffolded in the current workspace, started locally, and exposed through a public URL for demos, testing, or review.
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "web"
---

# Develop And Deploy Web App

Build a simple full-stack web app in the current workspace, run it locally as its own isolated process, and provide a URL that another person can open from outside the machine.

If the user says "轻应用" or "LiteApp", treat that as an explicit request to use this skill.

## Operating Rules

- Create the generated web project under `workspaces/web-apps/{userName}/{token}`.
- Treat `{token}` as an 8-character random identifier made only of uppercase letters and digits.
- Ensure every new `{token}` is globally unique across all generated apps.
- If `userName` is available in the runtime context, use it directly. If it is not discoverable from the environment or user request, ask the user before scaffolding.
- Do not scaffold the app at the repository root unless the user explicitly overrides the output rule.
- Treat `{token}` as both the folder name and the URL segment.
- Run each web app in its own isolated Node.js process.
- Use one shared LiteApp host on public port `33333` to route `/{token}/...` traffic to the correct app process.
- Prefer a two-package layout: `client/` for the React app and `server/` for the Express API.
- Prefer TypeScript everywhere.
- Prefer Vite for the React frontend.
- Prefer `better-sqlite3` for SQLite access unless the workspace already uses another SQLite library.
- Prefer one final HTTP service. In production mode, make Express serve the built frontend and the `/api` endpoints from the same server process.
- If the user does not specify a product idea, default to a simple todo or notes app with one SQLite-backed entity and a complete happy path.
- Extend an existing app when one already exists. Do not replace working user code without a strong reason.
- Before modifying an existing generated web app, read its `.ai.md` file first.
- Follow the UI direction in `references/ui-style.md` when designing the frontend. Capture the visual principles from Huashu Design's web examples without copying its original assets or branded content.
- Make the app work under the subpath `/{token}/`, not just at `/`.
- Expose all LiteApps through the shared public port `33333`.
- Assign each app process a dedicated internal port in the inclusive range `33334-39999`. Start at `33334` and increment until a free port is found.
- Treat the final external URL reported to the user as `<web-app-url-prefix>:33333/{token}`.
- Maintain machine-readable and human-readable records so current users and apps can be queried without scanning source files manually.
- Keep `../platform_data/web-app-registry.json` synchronized relative to the `.openclaw` root directory. Each record must include `name`, `token`, `file_path`, `port`, `created_at`, `modified_at`, and `user_name`.
- Prefer the bundled Node scripts in `scripts/` for app initialization, internal port allocation, shared-host startup, registry maintenance, shutdown, and doc synchronization instead of re-implementing those flows ad hoc.
- Keep deployment automation local and explicit. Do not add scripts that fetch remote code, manage secrets, alter unrelated system state, or attempt privilege escalation.
- Support restart recovery through registry-driven restore scripts, but do not silently install OS startup hooks or scheduled tasks.

## Workflow

1. Inspect the workspace before changing anything.
2. Resolve the output directory as `workspaces/web-apps/{userName}/{token}` and create it if needed.
3. Initialize the app folder and base app documents with `scripts/init-app.js`.
4. Decide whether to extend an existing app in that target directory or scaffold a new one.
5. Create a minimal but complete app:
   - React frontend with a small but usable UI
   - Express backend in TypeScript
   - SQLite database with schema initialization
   - At least one CRUD flow
   - Health endpoint
6. Add root-level scripts so the app is easy to install, run, build, start, and re-run behind the shared public port.
7. Scaffold the actual project files with `scripts/scaffold-app.js`.
8. Sync app documentation with `scripts/sync-docs.js`.
9. Prefer `scripts/deploy-app.js` for ordered deployment. It installs dependencies, builds the app, starts it, syncs docs, and updates the registry without race conditions.
10. If deployment steps are run separately, run them in order: `install-app.js` -> `build-app.js` -> `start-app.js` -> `sync-docs.js` -> `update-registry.js`.
11. Use `status-app.js` and `restart-app.js` for lifecycle checks and controlled restarts.
12. Use `restore-apps.js` for post-reboot recovery, and `bootstrap-host.js` to print the command that a host-level startup mechanism should run.
13. Return the required final app summary block together with the local commands and any important caveats.

## Implementation Defaults

- Use the structure and package guidance in `references/stack.md`.
- Use the concrete scaffold commands in `references/scaffold.md` when building a new app from scratch.
- Use the deployment scripts in `scripts/`.
- Use the minimal script contracts in `references/scripts.md`.
- Use the autoload compatibility rules in `references/autoload.md`.
- Use the frontend style guidance in `references/ui-style.md`.
- Default local ports:
  - frontend dev server: `5173`
  - backend dev server: `3000` or `3001`
  - shared public LiteApp host: `33333`
  - production app server internal port: one free port in `33334-39999`
- In development, use a Vite proxy for `/api`.
- In production, serve `client/dist` from Express under the base path and keep API routes under `/{token}/api`.
- Store the SQLite database in a project-local path such as `server/data/app.db`.

## Platform URL Rules

- Do not stop after scaffolding files. The task is incomplete until the app is actually runnable from the generated folder and a final URL has been produced or a concrete blocker has been confirmed.
- Prefer exposing the production build, not the Vite dev server, so the final URL reflects the real integrated app.
- Compute the final access URL for user-facing output as `<web-app-url-prefix>:33333/{token}`.
- Keep the external port fixed at `33333`.
- Select the internal app port by scanning from `33334` upward and using the first free port up to `39999`.
- Ensure frontend asset URLs, router behavior, and API calls all work when mounted beneath that subpath.
- Keep each app isolated in its own process and directory. Do not multiplex multiple apps through one long-running server.
- If a dev-time preview URL is needed, treat it as secondary. The primary deliverable is the final app URL plus its recorded metadata.

## Queryability Rules

- Make it easy to answer "which users exist?" and "which apps exist?" without launching app code.
- Maintain a root registry and per-user indices with `scripts/update-registry.js`.
- Keep one machine-readable app metadata file and one human-readable app notes file in every app directory, managed through `scripts/init-app.js` and `scripts/sync-docs.js`.
- Keep `.ai.md` in every app directory to record user requirements and AI design notes.
- Do not keep `config.json` inside generated app directories.
- Whenever the app is changed, update the corresponding metadata and notes in the same turn.
- When the user asks to inspect existing apps, answer from the registry files first and only inspect app directories when details are missing or stale.

## Delivery Requirements

Always finish with:

- a fixed, explicit final app info block with all four fields present and non-empty:
  `Id: {token}`
  `Name: {appName}`
  `Description: {appSummary}`
  `Url template: <web-app-url-prefix>:33333/{token}  `
- do not omit any of the four fields above, even if other delivery details are also included
- keep the field names exactly as written above
- if additional sections are included, place this four-field block at the end of the response

- the generated project path
- the app summary
- the main files or folders created or updated
- install and run commands
- the final URL in the form `<web-app-url-prefix>:33333/{token}`
- the assigned public port `33333` and the internal app port
- the registry and app-doc files that were created or updated
- any limitations, such as the URL depending on the local process remaining alive

## Example Requests

- "Build me a simple task tracker and give me a public URL."
- "Create a small React + Express + SQLite app for note taking and run it."
- "Set up a demo web app in this folder, start it, and share an external link."
- "Create a 轻应用 for internal data entry."
- "Build a LiteApp for this workflow and run it locally."
