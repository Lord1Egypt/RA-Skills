# Core Implementation Contract

Read this file before implementing any CLI with `agent-cli-builder`. It reflects the current `@renxqoo/agent-cli-sdk` source contract.

## Contents

1. Project and dependency setup
2. Command definitions
3. CLI assembly and entry point
4. Runtime context
5. Output, errors, and logs

## 1. Project and dependency setup

Prefer modifying the user's existing project. For a new project, use TypeScript, ESM, Node.js 20+, and the repository's package manager and test stack.

Before installing the framework, inspect `package.json` and the lockfile:

- In a monorepo, reuse its existing workspace version.
- In a standalone project, use the requested version; otherwise verify the current stable version and commit the lockfile.
- Do not silently install global dependencies or copy `@latest` blindly.

A publishable business package normally includes:

```json
{
  "type": "module",
  "bin": { "my-cli": "./dist/index.js" },
  "files": ["dist", "skills"],
  "engines": { "node": ">=20" }
}
```

Keep only scripts that actually run, typically `build`, `typecheck`, `test`, and `prepack`. Publish compiled output, not `src`. Bundle and minify distributed JavaScript or standalone binaries, retain source maps where operational debugging requires them, and verify the packed artifact rather than assuming a TypeScript compile is a release build.

## 2. Command definitions

```ts
import { defineCommand, defineCommands } from "@renxqoo/agent-cli-sdk";
import * as z from "zod";

export const todoCommands = defineCommands({
  list: defineCommand({
    name: "list",
    description: "List todos",
    args: {
      schema: z.object({
        limit: z.coerce.number().int().min(1).max(100).describe("Maximum items").default(20),
      }),
    },
    async run(ctx, args) {
      const res = await ctx.get<{ items: Array<{ id: string; title: string }> }>("/todos", {
        limit: args.limit,
      });
      return { data: res.data.items, meta: { count: res.data.items.length } };
    },
  }),
});
```

`args` rules:

| Setting                   | Behavior                                               |
| ------------------------- | ------------------------------------------------------ |
| omitted `args`            | No business parameters; `run` receives `{}`            |
| omitted `type` / `"argv"` | Native argv mode                                       |
| `schema`                  | Direct Zod object; the only validator and type source  |
| `pos: ["id"]`             | Consume schema field `id` as a positional operand      |
| `type: "json"`            | One complete JSON document; no business flags or `pos` |

A required positional cannot follow an optional positional. Use `z.coerce.number()` for numeric argv fields because the shell supplies strings. Zod defines requiredness, defaults, enums, refinements, transforms, descriptions, and the `args` inference in `run(ctx, args)`.

`defineCommand` is the only command-definition API. Do not add manual `Args` generics or helper wrappers. Componentized stateful groups should use `defineCommands<State>({...})`; incompatible groups are rejected by `defineCli<State>`.

For many or nested payload fields, add Zod 4 to the business package and pass the schema directly:

```ts
import * as z from "zod";

const UpdateOrder = z.strictObject({ id: z.string(), status: z.string() });

const update = defineCommand({
  name: "update",
  description: "Update an order",
  args: { type: "json", schema: UpdateOrder },
  policy: { mode: "write", confirmation: "required", idempotency: "required" },
  async run(ctx, args) {
    return { data: (await ctx.post("/orders/update", args)).data };
  },
});
```

Do not wrap Zod or introduce a second schema protocol. The same Zod object drives validation, inferred args, help, and `--input-schema`. Read `structured-input.md` for JSON transports, shell composition, and write policy.

Framework-reserved names include `json`, `no-json`, `api-key`, `help`, `version`, `input`, `input-file`, `input-schema`, `input-example`, `dry-run`, `yes`, and `idempotency-key`. There is no `--input-stdin`; pipes and redirection are native stdin.

## 3. CLI assembly and entry point

```ts
#!/usr/bin/env node
import { realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { homedir } from "node:os";
import { join } from "node:path";
import { defineCliApp } from "@renxqoo/agent-cli-sdk";
import { todoCommands } from "./commands/todos.js";

const app = await defineCliApp({
  name: "my-cli",
  binName: "my-cli",
  description: "Query and manage todos",
  // The app's one directory decision; plugins receive this local state via apply(services).
  dir: join(homedir(), ".my-cli"),
  baseUrl: process.env.TODOS_API_URL ?? "https://api.example.com",
  commands: todoCommands,
  errorOnStatus: { 404: "not_found", 429: "rate_limited", "5xx": "server_error" },
  defaultFormat: "auto",
  skillsDir: "./skills",
});

function isMainEntry(): boolean {
  try {
    return realpathSync(process.argv[1] ?? "") === fileURLToPath(import.meta.url);
  } catch {
    return false;
  }
}

if (isMainEntry()) await app.run(process.argv.slice(2));
export default app;
```

Global installation makes `argv[1]` a symlink, so compare real paths. Never run the CLI when the module is imported.

Key `defineCliApp` options:

| Option          | Rule                                                                                    |
| --------------- | --------------------------------------------------------------------------------------- |
| `dir`           | The app's one local-state root (`dir` XOR `localState`; injected via `apply(services)`) |
| `name`          | Output `source`, pipe type, and Skill identity                                          |
| `binName`       | The actual shell command; set it explicitly                                             |
| `commands`      | Required top-level commands; use for one domain                                         |
| `namespaces`    | Use only for multiple unrelated domains                                                 |
| `plugins`       | Plain Plugin objects (`defineAuth` and friends are sync factories), never Promises      |
| `errorOnStatus` | HTTP status to registered subtype mapping                                               |
| `defaultFormat` | `auto` by default, or `json` / `human`                                                  |
| `skillsDir`     | Enables built-in `skills` commands                                                      |
| `skillsTargets` | Overrides default synchronization targets                                               |

The install wizard is a plugin-provided command, not an entry-point intercept. Add `defineInstaller({ skillsSource })` to the app's plugins and `rxcli install [--lang zh|en]` routes through the normal pipeline; the entry point stays a plain `app.run(argv)`.

## 4. Runtime context

Every command receives `run(ctx, args)`. In argv and JSON mode alike, `args` is exactly the validated Zod output object. Framework policy and input-provenance fields are not mixed into it. Commands can use:

- `ctx.get/post/put/patch/delete`, returning `{ status, data, headers }`.
- `ctx.request` for custom methods, query, body, headers, or timeout.
- `ctx.state` for typed state shared by plugins.
- `ctx.log` for stderr-only logs.
- `ctx.pipe` for upstream `PipeRecord` input.
- `ctx.credentials` after auth initialization.

Type requests from the verified API. Do not use `any` or multi-field fallbacks to conceal an unknown contract.

## 5. Output, errors, and logs

```ts
return {
  data: objectOrArrayOrNull,
  meta: {
    count: 10,
    pagination: { complete: false, nextToken: "cursor" },
    rollback: "Run my-cli item restore <id> to undo",
  },
};
```

- A pure side effect may return `void`; the framework emits `data: null`.
- `{}`, `{ data: undefined }`, and scalar data cause `internal/contract_violation`.
- Pagination metadata is never automatic. Map it explicitly to `complete` and `nextToken`; omit `nextToken` when complete.
- Successful JSON goes to stdout. Errors and logs go to stderr.
- Optional update awareness uses `createUpdateNotifier` and stderr-only `<system-message>` output. It runs once per app run (`afterAppRun`, successful runs only), reads a local cache, and refreshes npm metadata in a detached helper for a later run; it never adds update fields to stdout.
- `auto` renders text on a TTY and JSON in pipes or CI; agents should still pass `--json` explicitly.
- Business commands must not write to stdout. Raw `skills read` output is an internal exception.

```ts
const updateNotifier = createUpdateNotifier({
  packageName: "@scope/my-cli",
  currentVersion: "1.2.0",
  updateCommand: "npm install -g @scope/my-cli",
});

const app = await defineCliApp({/* dir, plugins: [updateNotifier], ... */});
```

`defineCliApp({ dir })` is the app's one directory decision. The assembler creates a single local state and injects it into every plugin through `apply(services)`. Layout: `<dir>/config/<ns>.json` (per-namespace app config), `<dir>/credentials/<ns>.json`, and `<dir>/cache/updates/`; the high-level APIs have no independent directory parameters.

This capability is opt-in because it adds cache writes and a throttled registry request. `NO_UPDATE_NOTIFIER=1` disables it. A Skill may recognize the system message and report it after the business task, but it must not parse it as business data or execute the suggested installation without user authorization.

Throw `errs.*` for business failures. A bare `Error` becomes `internal/unknown` and is appropriate only for a genuinely unexpected internal failure. Put shared HTTP semantics in `errorOnStatus`; throw command-specific errors in `run`, never both for the same status.
