# Step 2: Create pnpm Patch

**Prerequisite:** Step 1 — patched pi-mono built successfully.

## How pnpm patch Works

`pnpm patch <pkg>` copies the installed package to a temp directory for editing. After making changes, `pnpm patch-commit <dir>` generates a `.patch` file and adds a `patchedDependencies` entry to `package.json`. On every subsequent `pnpm install`, the patch is re-applied automatically.

The patch only modifies file contents — it **cannot** add new dependencies to the resolution graph. Native dependencies (like `better-sqlite3`) must be handled separately (step 3).

## Action

### 1. Create the patch workspace

```bash
cd ~/openclaw
pnpm patch @mariozechner/pi-coding-agent@<version>
# Note the temp dir path, e.g.:
# /Users/.../node_modules/.pnpm_patches/@mariozechner/pi-coding-agent@0.61.1
```

### 2. Copy compiled output

```bash
PATCH_DIR="<temp-dir-from-above>"
SRC_DIR="<pi-mono>/packages/coding-agent/dist/core"

# New file
cp "$SRC_DIR/playfilo-db.js"      "$PATCH_DIR/dist/core/"
cp "$SRC_DIR/playfilo-db.js.map"  "$PATCH_DIR/dist/core/"
cp "$SRC_DIR/playfilo-db.d.ts"    "$PATCH_DIR/dist/core/"
cp "$SRC_DIR/playfilo-db.d.ts.map" "$PATCH_DIR/dist/core/"

# Modified files
for f in sdk session-manager agent-session; do
  cp "$SRC_DIR/$f.js"      "$PATCH_DIR/dist/core/"
  cp "$SRC_DIR/$f.js.map"  "$PATCH_DIR/dist/core/"
  cp "$SRC_DIR/$f.d.ts"    "$PATCH_DIR/dist/core/"
  cp "$SRC_DIR/$f.d.ts.map" "$PATCH_DIR/dist/core/"
done

echo "Copied all files"
```

### 3. Commit the patch

```bash
cd ~/openclaw
pnpm patch-commit '<temp-dir>'
```

This creates `patches/@mariozechner__pi-coding-agent@<version>.patch` and adds to `package.json`:

```json
"patchedDependencies": {
  "@mariozechner/pi-coding-agent@0.61.1": "patches/@mariozechner__pi-coding-agent@0.61.1.patch"
}
```

## Verify

```bash
# Patch file exists
ls ~/openclaw/patches/@mariozechner__pi-coding-agent@*.patch

# patchedDependencies in package.json
grep patchedDependencies ~/openclaw/package.json

# Patched file is present in node_modules
ls ~/openclaw/node_modules/@mariozechner/pi-coding-agent/dist/core/playfilo-db.js
```
