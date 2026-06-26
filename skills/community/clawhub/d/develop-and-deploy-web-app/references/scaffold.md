# Scaffold Commands

Use these commands when the workspace does not already contain an app.

## Baseline Approach

Prefer a root workspace with separate `client` and `server` packages.

## Typical Command Sequence

```bash
npm create vite@latest client -- --template react-ts
mkdir server
cd server
npm init -y
npm install express cors better-sqlite3
npm install -D typescript tsx @types/node @types/express
cd ..
npm init -y
npm install -D concurrently
```

Then add:

- a root `package.json` configured as a workspace
- a `server/tsconfig.json`
- a `server/src/` tree
- a Vite proxy in `client/vite.config.ts`
- a Vite `base` value set to `/${token}/`
- app-local docs: `APP-META.json` and `APP-NOTES.md`

## Backend Package Defaults

Prefer scripts like:

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc -p tsconfig.json",
    "start": "node dist/index.js"
  }
}
```

Prefer reading the production port from `process.env.PORT`.

## Frontend Package Defaults

Prefer scripts Vite already provides:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  }
}
```

## Root Script Defaults

Prefer:

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

## API Shape

Use a small SQLite-backed CRUD resource. A todo flow is the default when the user does not provide a domain:

- `GET /{token}/api/health`
- `GET /{token}/api/todos`
- `POST /{token}/api/todos`
- `PATCH /{token}/api/todos/:id`
- `DELETE /{token}/api/todos/:id`

## Production Serving

Make Express serve the built frontend:

- serve static files from `client/dist` under `/${token}/`
- return `index.html` for non-API routes inside that base path
- keep API routes under `/${token}/api`

This makes the app compatible with platform auto-loading at `http://host:{port}/{token}/`.
This also keeps the app compatible with independent-process hosting on any assigned port in `33333-39999`.
