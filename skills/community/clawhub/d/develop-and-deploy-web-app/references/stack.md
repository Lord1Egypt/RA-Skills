# Stack Guide

Use this reference when scaffolding a new project from scratch.

## Recommended Layout

```text
.
|-- client/
|-- server/
|-- package.json
`-- SKILL.md
```

## Root Package

Prefer a root `package.json` with workspace-style scripts so the app is easy to run:

```json
{
  "private": true,
  "workspaces": ["client", "server"],
  "scripts": {
    "dev": "concurrently \"npm run dev -w server\" \"npm run dev -w client\"",
    "build": "npm run build -w client && npm run build -w server",
    "start": "npm run start -w server"
  }
}
```

If `concurrently` is not desired, equivalent scripts that use `npm --prefix` are acceptable.

## Frontend Defaults

- Scaffold with React + TypeScript.
- Prefer Vite.
- Keep the UI intentionally simple and complete, not decorative placeholder text.
- Call the backend through `/api`.
- In development, configure a proxy from Vite to the backend server.
- Configure Vite `base` to `/${token}/` for production builds when the path is known at scaffold time.
- Ensure the production server reads its assigned port from configuration or environment instead of hard-coding one shared port.

## Backend Defaults

- Use Express with TypeScript.
- Use `tsx` for local development.
- Compile with `tsc` for production start.
- Expose:
  - `GET /api/health` behind the base path
  - at least one CRUD resource such as `/api/todos` behind the base path
- In production, serve the built frontend from Express under `/${token}/`.

## SQLite Defaults

- Prefer `better-sqlite3`.
- Keep schema initialization in a small dedicated module such as `server/src/db.ts`.
- Create the database file automatically on first run.
- Keep the schema minimal and local to the app.
- Keep all generated artifacts inside the assigned app folder under `workspaces/web-apps/{userName}/{token}`.
- Keep app-local metadata and notes in the app folder so each app remains independently inspectable.

## Minimum Product Quality

Ship a usable vertical slice:

- one real entity stored in SQLite
- list view
- create flow
- one update or toggle flow
- delete flow if it fits naturally
- loading, empty, and error states

## Verification

Before exposing the app publicly:

1. Install dependencies successfully.
2. Build both packages successfully.
3. Start the production server successfully on a free port in `33333-39999`.
4. Confirm the page loads locally through `/${token}/`.
5. Confirm the API responds locally through `/${token}/api/...`.
