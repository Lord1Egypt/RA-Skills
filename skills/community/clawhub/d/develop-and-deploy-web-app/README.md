# develop-and-deploy-web-app

A local toolkit for scaffolding, running, and managing small full-stack web apps inside this repository.

It organizes app workspaces by `userName` under `workspaces/web-apps/`, with helper scripts in `scripts/` for initialization, build, start, restart, restore, removal, metadata sync, and registry updates. `appKind` and `appLabel` are derived from the app's title and goal, or can be provided explicitly when needed. Generated apps use a React + TypeScript + Vite frontend, an Express + TypeScript backend, and SQLite for local persistence.

## Structure

- `scripts/` - app lifecycle and registry utilities
- `workspaces/web-apps/` - generated app workspaces
- `references/` - stack, scaffold, and UI guidance
- `agents/` - agent configuration

## Common Commands

- `node scripts/init-app.js --userName <name> --token <token>`
- `node scripts/scaffold-app.js --userName <name> --token <token>`
- `node scripts/deploy-app.js --userName <name> --token <token>`
- `node scripts/status-app.js --userName <name> --token <token>`
- `node scripts/remove-app.js --userName <name> --token <token>`
- `node scripts/restore-apps.js --skipBuild`

## Notes

- Apps are served under `/<token>/`
- All LiteApps share the public port `33333`
- Each app process still uses its own internal port in `33334-39999`, routed through the shared host on `33333`
- Tokens must be globally unique across generated apps
- `workspaces/web-apps/registry.json` is the only source of truth for managed apps; scripts do not scan folders to discover apps
- Each user can only operate on apps registered under that same `userName`
- Runtime metadata is stored in `APP-META.json`, `APP-NOTES.md`, `.ai.md`, and registry files under `workspaces/web-apps/`
- Before modifying an existing generated app, read its `.ai.md`
- A platform-wide app list is synchronized to `../platform_data/web-app-registry.json` relative to the `.openclaw` root directory
- Platform registry records include `name`, `token`, `file_path`, `port`, `created_at`, `modified_at`, `user_name`, `app_kind`, and `app_label`
