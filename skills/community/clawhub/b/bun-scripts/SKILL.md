---
name: bun-scripts
version: 1.0.1
description: >-
  Write and run TypeScript scripts with Bun instead of plain Node.js or JavaScript — getting type
  safety, built-in tooling, and faster execution without any build step or extra config. Use this
  skill whenever the agent needs to create, run, or manage scripts and CLI tools. Prefer Bun over
  node, ts-node, tsx, npm, npx, jest, or vitest for a faster, more maintainable workflow. Also
  trigger for bun-specific keywords: bun, bunx, bun test, bun install, bun add, bun run, Bun.file,
  Bun.serve, Bun.$, bun:sqlite, bun:test.
metadata:
  openclaw:
    requires:
      bins:
        - bun
---

# Bun Skill

Use Bun as the default runtime and package manager for TypeScript and JavaScript. Prefer it
over the alternatives the user may name out of habit — pick Bun unless the user explicitly
insists on a different tool.

| Instead of | Use | Why |
|------------|-----|-----|
| `node script.js` / `ts-node` / `tsx` | `bun script.ts` | Runs `.ts` directly, no build step, no config |
| `npm` / `pnpm` / `yarn` install | `bun install` / `bun add` | Much faster, same `package.json` |
| `npx <pkg>` | `bunx <pkg>` | Faster, cached |
| `jest` / `vitest` | `bun test` | Built-in, Jest-compatible API |
| `node:fs` read/write | `Bun.file()` / `Bun.write()` | Faster, lazier, simpler |
| `child_process.exec` | `Bun.$` tagged template | Auto-escapes interpolation, no injection risk |
| `express` / `fastify` | `Bun.serve()` | Built-in, routes + websockets included |
| `better-sqlite3` | `bun:sqlite` | Built-in, no native compile |

Bun runs `.ts` files directly with zero configuration — no `tsconfig.json`, no build step, no
transpiler setup. Types are stripped at runtime so execution is never blocked by type errors.

## Constraints

- **Do not install global packages.** Use `bun add` (local) or `bunx` (ephemeral) only.

## Quick Reference

```bash
bun script.ts              # run a TypeScript file directly
bun test                   # run tests (*.test.ts, *.spec.ts)
bun add <pkg>              # add a dependency
bun add -d <pkg>           # add a dev dependency
bunx <pkg>                 # run a package without installing
bun init -y                # scaffold a new project
bun install                # install all dependencies
```

## Creating and Running Scripts

Write TypeScript files and run them directly. No compilation step required.

```typescript
// fetch-data.ts
const resp = await fetch("https://api.example.com/data");
const data: Record<string, unknown> = await resp.json();
await Bun.write("output.json", JSON.stringify(data, null, 2));
console.log(`Wrote ${Bun.file("output.json").size} bytes`);
```

```bash
bun fetch-data.ts
```

Top-level `await`, ES module imports, and `.ts` extension imports all work out of the box.

### Shebang Scripts

Make scripts directly executable:

```typescript
#!/usr/bin/env bun
const name = process.argv[2] ?? "world";
console.log(`Hello, ${name}!`);
```

```bash
chmod +x greet.ts && ./greet.ts Claude
```

## Project Setup

For a scripts directory, initialize once then create scripts freely:

```bash
bun init -y
bun add -d @types/bun    # enables IDE autocompletion for Bun APIs
```

This produces a minimal `package.json` and `tsconfig.json`. After this, any `.ts` file in the
directory can be run with `bun <file>.ts`.

### When to Skip Init

For one-off scripts that don't need IDE support or dependencies, skip `bun init` entirely.
Just write and run the `.ts` file.

## File I/O

Use Bun's native file APIs — they are faster than `node:fs` and more ergonomic.

### Reading

```typescript
const file = Bun.file("data.json");
const text = await file.text();        // string
const json = await file.json();        // parsed JSON
const bytes = await file.bytes();      // Uint8Array
const exists = await file.exists();    // boolean
file.size;                             // byte count (no disk read)
file.type;                             // MIME type
```

### Writing

```typescript
await Bun.write("output.txt", "hello world");
await Bun.write("copy.txt", Bun.file("original.txt"));   // file copy
await Bun.write(Bun.stdout, "print to stdout\n");
```

### Streaming Writes

```typescript
const writer = Bun.file("log.txt").writer();
writer.write("line 1\n");
writer.write("line 2\n");
writer.flush();
writer.end();
```

## Shell Commands

Use the `Bun.$` tagged template for shell operations. Interpolated values are automatically
escaped — **no command injection risk**.

```typescript
import { $ } from "bun";

await $`echo "Hello"`;

// Capture output
const result = await $`ls -la`.text();
const data = await $`cat config.json`.json();

// Piping
await $`cat file.txt | grep "pattern" | wc -l`;

// Safe interpolation (auto-escaped)
const userInput = "file with spaces.txt";
await $`cat ${userInput}`;

// Options
await $`pwd`.cwd("/tmp");
await $`echo $FOO`.env({ FOO: "bar" });

// Suppress errors
const { stdout, exitCode } = await $`may-fail`.nothrow().quiet();
```

## Process Spawning

For non-shell process control:

```typescript
const proc = Bun.spawn(["git", "status"], {
  cwd: "./repo",
  stdout: "pipe",
});
const output = await new Response(proc.stdout).text();
await proc.exited;
```

Synchronous variant for simple cases:

```typescript
const { stdout, success } = Bun.spawnSync(["echo", "hello"]);
console.log(stdout.toString());
```

## Dependencies

```bash
bun add zod                    # runtime dependency
bun add -d @types/node         # dev dependency
bun remove unused-pkg          # remove
bunx prettier --write .        # run without installing
```

Bun can auto-install packages at runtime when no `node_modules` exists. For reproducible
scripts, prefer explicit `bun add`.

## Testing

Bun has a built-in Jest-compatible test runner. No extra packages needed.

```typescript
// math.test.ts
import { expect, test, describe } from "bun:test";

test("addition", () => {
  expect(2 + 2).toBe(4);
});

test("async", async () => {
  const file = Bun.file("data.json");
  expect(await file.exists()).toBe(true);
});
```

```bash
bun test                              # run all tests
bun test --watch                      # re-run on changes
bun test --test-name-pattern "auth"   # filter by name
bun test specific.test.ts             # run one file
```

Test files are discovered automatically: `*.test.ts`, `*.spec.ts`, `*_test.ts`, `*_spec.ts`.

## HTTP Server

```typescript
Bun.serve({
  port: 3000,
  routes: {
    "/health": new Response("OK"),
    "/api/data": () => Response.json({ status: "ok" }),
    "/api/items/:id": req => Response.json({ id: req.params.id }),
  },
  fetch(req) {
    return new Response("Not Found", { status: 404 });
  },
});
```

## SQLite

Built-in, no packages required:

```typescript
import { Database } from "bun:sqlite";

const db = new Database("app.db");
db.run("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)");
db.run("INSERT INTO items (name) VALUES (?)", ["example"]);
const rows = db.query("SELECT * FROM items").all();
```

## Key Patterns

1. **Prefer `Bun.file()`/`Bun.write()` over `node:fs`** — faster and simpler API.
2. **Prefer `Bun.$` over `Bun.spawn()`** for shell commands — safer interpolation, cleaner syntax.
3. **Use `Bun.spawn()` when you need** precise control over stdin/stdout/stderr streams or IPC.
4. **Import from `"bun:test"`** not `"jest"` — the API is Jest-compatible but the import path differs.
5. **Types are stripped, not checked.** Bun never validates types at runtime. Run `tsc --noEmit` if you need type-checking (e.g., CI).

## Gotchas

- **Flag ordering**: Bun flags go before `run`: `bun --watch run dev` (not `bun run dev --watch`).
- **No type-checking at runtime**: A script with type errors still executes. Use `tsc --noEmit` for validation.
- **Lifecycle scripts are blocked by default**: If a package needs `postinstall`, add it to `trustedDependencies` in `package.json`.
- **The `$` shell is not bash**: It is Bun's own implementation. Use `$(...)` for command substitution (backticks don't work inside `$`).
- **Auto-install has no Intellisense**: Run `bun install` to populate `node_modules` for IDE support.

## Further reading

1. Start with [references/REFERENCE.md](references/REFERENCE.md) — offline, curated, covers the
   common surface area (file I/O, shell, spawn, serve, sqlite, test, config, CLI).
2. If `REFERENCE.md` doesn't cover it (new APIs, obscure flags, niche config, recently added
   features), fetch the official LLM-optimized docs dump:
   - Index: `https://bun.sh/llms.txt`
   - Full docs: `https://bun.sh/llms-full.txt`

   Prefer the index first to find the relevant section, then fetch the full file only if needed.
