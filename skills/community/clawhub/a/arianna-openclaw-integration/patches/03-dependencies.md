# Step 3: Add Native Dependencies

**Prerequisite:** Step 2 — pnpm patch committed.

## Why This is Needed

`pnpm patch` modifies file contents but cannot add packages to the dependency resolution graph. The patched `playfilo-db.js` imports `better-sqlite3` (a native C++ addon) and the patched `sdk.js` imports `@sinclair/typebox`. These must be resolvable at runtime.

## Action

Edit `~/openclaw/package.json` in the `pnpm` section:

### Add `better-sqlite3` to `onlyBuiltDependencies`

Find the existing `pnpm.onlyBuiltDependencies` array and add `"better-sqlite3"`:

```json
"onlyBuiltDependencies": [
  "@lydell/node-pty",
  "...",
  "sharp",
  "better-sqlite3"
],
```

**Why:** pnpm blocks native module build scripts by default. Without this, `better-sqlite3` installs but its C++ addon is not compiled.

### Add dependencies via `packageExtensions`

Find the existing `pnpm.packageExtensions["@mariozechner/pi-coding-agent"]` and extend it:

```json
"packageExtensions": {
  "@mariozechner/pi-coding-agent": {
    "dependencies": {
      "strip-ansi": "^7.2.0",
      "better-sqlite3": "^11.0.0",
      "ajv": "^8.17.1"
    }
  }
}
```

**Why `packageExtensions` instead of top-level dependencies:** This declares the deps where they belong (as deps of pi-coding-agent), following OpenClaw's existing pattern for `strip-ansi`.

### What about `@sinclair/typebox`?

Not needed — OpenClaw already resolves `@sinclair/typebox` at `0.34.48` via `pnpm.overrides`. With `node-linker=hoisted` (OpenClaw's `.npmrc`), it's available to pi-coding-agent without explicit declaration.

## Install

```bash
cd ~/openclaw
pnpm install
```

## Verify

```bash
# better-sqlite3 compiled successfully
ls ~/openclaw/node_modules/better-sqlite3/build/Release/better_sqlite3.node

# Can be required from pi-coding-agent's context
node -e "require('better-sqlite3')" && echo "OK"
```
