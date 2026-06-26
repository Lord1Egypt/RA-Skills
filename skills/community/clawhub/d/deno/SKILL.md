---
name: Deno
slug: deno
version: 1.0.0
description: "Build with Deno runtime avoiding permission gotchas, URL import traps, and Node.js migration pitfalls."
metadata: {"clawdbot":{"emoji":"🦕","requires":{"bins":["deno"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs Deno expertise — secure TypeScript runtime with permissions model. Agent handles permission configuration, dependency management via URLs/npm, and migration from Node.js.

## Quick Reference

| Topic | File |
|-------|------|
| Permission system | `permissions.md` |
| Imports and dependencies | `imports.md` |
| Node.js migration | `node-compat.md` |

## Permission Traps

- `--allow-all` in development — then production crashes because you don't know what permissions you actually need
- `--allow-read` without path — grants access to entire filesystem, security hole
- `--allow-run` without list — subprocess can run anything, specify: `--allow-run=git,npm`
- `--allow-env` without list — leaks all env vars, specify: `--allow-env=API_KEY,DATABASE_URL`
- `--allow-net` without list — can connect anywhere, specify hosts: `--allow-net=api.example.com`
- Missing permission in CI — hangs waiting for prompt that never comes, add `--no-prompt`

## Import Traps

- Remote URLs in production — network failure = app won't start, vendor dependencies locally
- No lockfile by default — deps can change between runs, always use `deno.lock`
- `@^1.0.0` semver syntax doesn't exist — use exact URLs or import maps
- Import maps in wrong place — must be in `deno.json`, not separate file (Deno 2.x)
- HTTPS required — HTTP imports blocked by default, most CDNs work but self-hosted may not
- URL typo — no error until runtime when import fails

## TypeScript Traps

- `.ts` extension required in imports — model generates extensionless imports that fail
- `tsconfig.json` paths ignored — Deno uses import maps in `deno.json`, not tsconfig
- Type-only imports — must use `import type` or bundler may fail
- Decorators — experimental, different from tsc behavior
- `/// <reference>` — handled differently than tsc, may be ignored

## Deployment Traps

- `deno compile` includes runtime — binary is 50MB+ minimum
- `--cached-only` requires prior cache — fresh server needs `deno cache` first
- Deno Deploy limitations — no filesystem, no subprocess, no FFI
- Environment variables — different API: `Deno.env.get("VAR")` not `process.env.VAR`
- Signals — `Deno.addSignalListener` not `process.on("SIGTERM")`

## Testing Traps

- `Deno.test` different from Jest — no `describe`, different assertions
- Async test without await — test passes before promise resolves
- Resource leaks — tests fail if you don't close files/connections
- Permissions in tests — test may need different permissions than main code
- Snapshot testing — format differs from Jest snapshots

## npm Compatibility Traps

- `npm:` specifier — works for most packages but native addons fail
- `node:` specifier required — `import fs from 'fs'` fails, need `import fs from 'node:fs'`
- `node_modules` optional — enable with `"nodeModulesDir": true` in deno.json
- `package.json` scripts — not automatically supported, use deno.json tasks
- Peer dependencies — handled differently, may get wrong versions

## Runtime Differences

- `Deno.readTextFile` vs `fs.readFile` — different API, different error types
- `fetch` is global — no import needed, unlike Node 18-
- Top-level await — works everywhere, no wrapper needed
- Permissions at runtime — can request dynamically but user must approve
