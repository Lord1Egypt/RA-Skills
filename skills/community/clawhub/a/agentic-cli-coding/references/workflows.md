# Workflows — Worked Examples

These are the patterns that come up most often. Each one walks through the full discovery → plan → execute → verify cycle.

---

## Workflow 1 — Bug fix in a single file

**Scenario**: User reports `processRequest()` crashes when `req.body` is undefined.

```bash
# 1. Locate the function
oce find "function processRequest" --type js
# → src/server.js:45:function processRequest(req) {

# 2. Read the function with surrounding context
oce read src/server.js --around "function processRequest" --context 15

# 3. Make the fix — add a guard, surgical replacement
oce replace src/server.js \
  --old "function processRequest(req) {
  const data = req.body;" \
  --new "function processRequest(req) {
  if (!req.body) {
    throw new Error('Request body required');
  }
  const data = req.body;"

# 4. Confirm the change
oce diff src/server.js

# 5. Run the project's tests if a test command exists
# (oce doesn't run tests itself — use the project's npm test / pytest / go test / etc.)
```

Notes: the multi-line `--old` works fine — `oce replace` does literal string match including newlines. Indentation must match exactly.

---

## Workflow 2 — Adding a new file from scratch

**Scenario**: Create a new utility module.

```bash
# 1. Confirm where similar files live
oce tree src --depth 2

# 2. Write the new file (--new ensures we don't clobber an existing file)
cat <<'EOF' | oce write src/utils/sanitize.js --new
const escapeMap = { '<': '&lt;', '>': '&gt;', '&': '&amp;' };

function sanitize(input) {
  if (typeof input !== 'string') return input;
  return input.replace(/[<>&]/g, ch => escapeMap[ch]);
}

module.exports = { sanitize };
EOF

# 3. Wire it into the index if there is one
oce find "module.exports" src/utils/index.js
oce insert src/utils/index.js \
  --before-match "module.exports" \
  --content "const { sanitize } = require('./sanitize');"
oce replace src/utils/index.js \
  --old "module.exports = {" \
  --new "module.exports = {
  sanitize,"
```

---

## Workflow 3 — Multi-file rename / refactor

**Scenario**: Rename `validateToken` to `verifyToken` everywhere.

```bash
# 1. Find every reference
oce find "validateToken" --type js --files-only
# → src/auth.js, src/middleware.js, tests/auth.test.js

# 2. Open a transaction so any one failure rolls everything back
TXN=$(oce transaction begin)

# 3. For pure JS, AST rename is safest — only renames real identifiers,
#    not strings or comments
oce ast rename src/auth.js       --from validateToken --to verifyToken --txn "$TXN"
oce ast rename src/middleware.js --from validateToken --to verifyToken --txn "$TXN"

# 4. For test files (often have the name in describe blocks as a string),
#    use --all to catch everything including the strings
oce replace tests/auth.test.js \
  --old "validateToken" --new "verifyToken" \
  --all --txn "$TXN"

# 5. Validate the whole transaction
oce transaction validate "$TXN"

# 6. If everything looks good, commit. Otherwise rollback.
oce transaction commit "$TXN"
```

If validation fails partway through:
```bash
oce transaction rollback "$TXN"
```
Every file is restored from its pre-edit snapshot. The transaction directory is renamed to `rolled-back-<id>` so you can inspect what happened.

---

## Workflow 4 — Applying a precise multi-line patch

**Scenario**: You need to make a structural change with exact line control — adding a try/catch around an existing block.

```bash
# 1. Read the target block to make sure your patch lines align
oce read src/api.js --lines 40:60

# 2. Write the unified diff
cat > /tmp/wrap-trycatch.patch <<'EOF'
--- a/src/api.js
+++ b/src/api.js
@@ -42,9 +42,13 @@
 router.post('/users', async (req, res) => {
-  const user = await db.create(req.body);
-  res.json(user);
+  try {
+    const user = await db.create(req.body);
+    res.json(user);
+  } catch (err) {
+    res.status(500).json({ error: err.message });
+  }
 });
EOF

# 3. Dry-run first (oce patch automatically does this internally,
#    but you can also explicitly preview)
oce patch apply /tmp/wrap-trycatch.patch --dry-run

# 4. Apply for real
oce patch apply /tmp/wrap-trycatch.patch

# 5. Verify
oce diff src/api.js
```

If the patch context doesn't match exactly (file drifted, whitespace changed), the apply will fail before touching anything. Use `--fuzz 2` to tolerate small mismatches, or re-read the file and rewrite the patch.

---

## Workflow 5 — Vue / React component editing

**Scenario**: Add a prop to a Vue component.

```bash
# 1. Find the component
oce find "name: 'UserCard'" --type vue
# → src/components/UserCard.vue:8

# 2. Read the props block
oce read src/components/UserCard.vue --around "props:" --context 15

# 3. Add the prop. Vue and React components are JSX-like in templates,
#    so AST rename won't always work — use replace for surgical edits.
oce replace src/components/UserCard.vue \
  --old "props: {
    user: Object," \
  --new "props: {
    user: Object,
    showAvatar: { type: Boolean, default: true }," 

# 4. Add the corresponding template usage
oce replace src/components/UserCard.vue \
  --old "<img :src=\"user.avatar\"" \
  --new "<img v-if=\"showAvatar\" :src=\"user.avatar\""
```

Note: Vue's `<script>` block contains JS but the `.vue` file as a whole isn't valid JS, so post-edit syntax validation is best-effort. Run the project's build/lint to verify the full file (`npm run lint`, `vue-tsc --noEmit`, etc.).

---

## Workflow 6 — Removing dead code safely

**Scenario**: Remove a deprecated function and its callers.

```bash
# 1. Identify the function and find every caller
oce ast symbols src/legacy.js | grep oldHelper
oce find "oldHelper(" --type js --files-only

# 2. If callers exist, you have a choice:
#    a) Replace each call site with the new equivalent
#    b) Remove both the function and its call sites
#    Pick one — don't leave orphan calls.

# Choosing (b) — both go away. Use a transaction.
TXN=$(oce transaction begin)

# Remove call sites
oce delete src/main.js   --match "oldHelper(" --txn "$TXN"
oce delete src/api.js    --match "oldHelper(" --txn "$TXN"

# Remove the function definition. Use ast extract first to confirm what's there.
oce ast extract src/legacy.js oldHelper > /tmp/dead-code.js
cat /tmp/dead-code.js  # sanity check
oce ast replace-symbol src/legacy.js oldHelper --txn "$TXN" <<< ""
# ^ replacing with empty string deletes the function definition

oce transaction validate "$TXN"
oce transaction commit "$TXN"
```

---

## Workflow 7 — Configuration file edit

**Scenario**: Update `package.json` to bump a dependency.

```bash
# 1. JSON edits are dangerous with naive string replacement (escaping,
#    trailing commas, etc.) — read the exact value first
oce read package.json --around "express" --context 2

# 2. Use a literal replace for the version string
oce replace package.json \
  --old '"express": "^4.17.0"' \
  --new '"express": "^4.19.2"'

# 3. JSON validation is automatic — the post-edit check uses JSON.parse
#    and would have rolled back if the result were invalid

oce validate package.json
```

---

## Workflow 8 — Investigating before changing anything

**Scenario**: User asks "where does authentication happen in this codebase?"

```bash
# Pure-discovery flow, no edits
oce tree --depth 2
oce find "auth" --type js --files-only | head -20
oce find "passport\|jwt\|bearer" --type js --regex -i

# Pick the most relevant file and look at its symbols
oce ast symbols src/middleware/auth.js

# Read each entry point with context
oce grep-context "verify" src/middleware/auth.js -c 8
```

Now you can describe the auth flow back to the user before touching anything. Resist the urge to "fix it while you're in there" — the user asked a question, not for an edit.

---

## Workflow 9 — Recovering from a botched edit

**Scenario**: You ran an `oce replace` with `--all` and it changed too much.

```bash
# 1. List backups for the file
oce backup list src/server.js
# → newest first; position 0 is most recent

# 2. Compare the file vs. the most recent backup
oce backup diff src/server.js 0

# 3. If you want to undo, restore the most recent backup
oce backup restore src/server.js

# 4. If multiple bad edits happened, restore further back
oce backup restore src/server.js --at 3
```

Backups don't expire automatically. Run `oce backup clean 30` to remove anything older than 30 days when you want to free space.

---

## Workflow 10 — Working with TypeScript

**Scenario**: Edit a TypeScript file with full type-check validation.

```bash
# 1. AST commands work for the JS-compatible parts of TS but won't
#    parse advanced TS syntax (generics with constraints, decorators,
#    namespace declarations). For real type-check validation, the
#    project needs a local tsc.
oce doctor   # confirm tsc is available

# 2. For surgical edits, replace and patch work fine on .ts/.tsx files
oce replace src/types.ts \
  --old "type UserId = string;" \
  --new "type UserId = string & { readonly __brand: 'UserId' };"

# 3. The post-edit validator will run `tsc --noEmit` if available, which
#    catches type errors, not just syntax. If tsc isn't available, falls
#    back to acorn-with-types-stripped (syntax only).
```

For non-trivial TypeScript refactors, prefer the project's own tooling (ts-morph scripts, IDE refactors) for anything that requires real type information.

---

## A general note on planning

For any task that will touch more than two files or change more than ~20 lines, write the plan down before executing. Even a comment in your reasoning that says:

```
PLAN:
  - Add: src/utils/sanitize.js (new file, ~20 lines)
  - Modify: src/utils/index.js (export the new function)
  - Modify: src/server.js (call sanitize on user input at line 87)
  - Modify: tests/utils.test.js (add tests for sanitize)
  - Risk: any other place that handles user input might also need this
  - Validate: npm test should still pass; lint clean
```

...prevents the most common mode of agent failure: "made the change, didn't realize it broke something else."
