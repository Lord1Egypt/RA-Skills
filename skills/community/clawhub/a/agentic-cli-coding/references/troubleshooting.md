# Troubleshooting

Symptom → cause → fix.

---

## `oce: command not found`

**Cause**: The `oce` alias isn't set or the wrapper isn't on PATH.

**Fix**: Set up the alias for the session:
```bash
alias oce="bash /path/to/agentic_cli_coding/scripts/oce.sh"
```

Or call directly without an alias:
```bash
bash /path/to/agentic_cli_coding/scripts/oce.sh doctor
```

For persistent installation, run the install helper:
```bash
bash /path/to/agentic_cli_coding/scripts/install.sh
```

---

## `Refusing to edit binary file`

**Cause**: The first 8KB of the file contains a NUL byte. This is `oce`'s safety check against accidentally corrupting compiled artifacts, images, etc.

**Fix**: If the file is genuinely text and the check is a false positive, file a bug. Do not bypass — there's no flag to override and that's intentional.

If the file is binary and you really need to edit it, use a different tool. `oce` is for source code.

---

## `File too large`

**Cause**: File exceeds `OCE_MAX_FILE_SIZE` (default 5MB).

**Fix**: For genuinely large source files (rare but possible — generated code, large data fixtures), set:
```bash
OCE_MAX_FILE_SIZE=20971520 oce read path/to/big.js   # 20MB
```

Better: reconsider whether you need to edit a 5MB+ source file at all. Often these are committed build artifacts that should be regenerated, not edited.

---

## `Found N matches; pass --all or make --old more unique`

**Cause**: `oce replace` found multiple occurrences of `--old` and you didn't say `--all`. This is the safety guard against changing more than you meant to.

**Fix**: Either:

1. Make `--old` longer / more specific so it matches only the intended occurrence. Include surrounding context:
   ```bash
   # Bad — matches every "return data;"
   oce replace x.js --old "return data;" --new "return sanitize(data);"
   
   # Good — anchored to the specific function
   oce replace x.js \
     --old "function processRequest(req) {
     const data = req.body;
     return data;" \
     --new "function processRequest(req) {
     const data = req.body;
     return sanitize(data);"
   ```

2. Or pass `--all` if you genuinely want every occurrence changed.

3. Or pass `--count N` as a tripwire — fails if the actual count differs from N.

---

## `No match found for --old`

**Cause**: The exact `--old` string doesn't appear in the file. Common reasons:

- Whitespace doesn't match (tabs vs. spaces, trailing whitespace)
- Quotes don't match (single vs. double)
- The file already has the change (idempotency check)
- You're looking in the wrong file

**Fix**: Re-read the file at the relevant location:
```bash
oce read path/to/file --around "<some unique substring>" --context 5
```
Then craft `--old` from what you actually see.

---

## Edit succeeded but `oce diff` shows nothing

**Cause**: The replacement string was identical to the original. Or you're looking at `oce diff` after a transaction commit (which moves the backup directory).

**Fix**: For the second case, use `oce backup list <file>` to see what's available — committed transactions move backups to `committed-<id>/`.

---

## `validation failed — rolled back`

**Cause**: Your edit produced syntactically invalid code. The original was restored from backup. This is the system working as intended.

**Fix**: The error output above the rollback message tells you what went wrong. Common causes:
- Mismatched braces / brackets / parens
- Unclosed strings
- TypeScript-specific syntax in a file `oce` validated as JavaScript
- The replacement text lacked something the original had (e.g., a closing `;`)

Look at the file (it's been restored), look at your `--new` text, and try again.

---

## Validation passes but the code is broken at runtime

**Cause**: `oce validate` is syntax-only. It doesn't catch:
- Undefined variables / functions
- Type errors (unless TypeScript with `tsc` available)
- Logic bugs
- Wrong imports

**Fix**: Run the project's tests after non-trivial changes. `oce` doesn't run tests itself — that's the project's responsibility.

---

## `oce ast` fails with "Unexpected token" on a TypeScript file

**Cause**: The file uses TypeScript-specific syntax (generics, type annotations, interfaces) that acorn can't parse.

**Fix**: Use text-based edits (`oce replace`, `oce patch`, `oce insert`) for TypeScript. For full AST refactoring on TS, install local `typescript` and use the project's own tooling (or write a `ts-morph` script).

---

## `Patch does not apply cleanly`

**Cause**: The unified diff's context lines don't match the current file content. The file has drifted since the patch was generated, or the patch was hand-written with slightly wrong context.

**Fix**: Three options in order of preference:

1. Re-read the file and rewrite the patch with current line numbers and context.
2. Try `oce patch apply --fuzz 2` to allow up to 2 lines of context mismatch.
3. Convert the patch to a series of `oce replace` calls if it's small enough.

---

## Transaction stuck — can't commit or rollback

**Cause**: A previous shell process owned the transaction and exited mid-flight.

**Fix**:
```bash
oce transaction list                      # see active transactions
oce transaction status <txn-id>           # inspect what's in it
oce transaction rollback <txn-id>         # safe — just restores backups
```

If `rollback` doesn't work because the transaction directory is corrupt, you can manually restore individual files using the timestamps in `.oce/transactions/<id>/files.log`.

---

## `acorn not available`

**Cause**: The skill's `node_modules/acorn` is missing or unreadable.

**Fix**: 
```bash
oce doctor   # confirms what's missing
```

If acorn is genuinely missing, the skill wasn't installed completely. Reinstall, or run `npm install --omit=dev` from the skill's root directory.

---

## State directory keeps growing

**Cause**: Backups accumulate. By default they live forever in `.oce/backups/`.

**Fix**: 
```bash
oce backup clean 30   # remove backups older than 30 days
oce backup clean 0    # remove all backups (be sure)
```

You can also delete the entire `.oce/` directory between sessions if you don't need history. It's safe to add `.oce/` to `.gitignore`.

---

## File modified outside of `oce` between read and write

**Cause**: An external process (editor, formatter, build tool) changed the file after you read it but before you wrote.

**Fix**: `oce` doesn't currently check for this. To be safe in interactive contexts:
1. Re-read the file just before editing.
2. Watch for `.swp` or `.lock` files near the target — `oce preflight_check` warns about these.

For agent contexts where you're the only writer, this rarely matters.

---

## Help text is missing for a subcommand

**Fix**: 
```bash
oce <command> --help
```
Every command supports `--help` / `-h`. The dispatcher `oce help` shows the top-level command list.

---

## Where to look when nothing else helps

1. **`.oce/edit.log`** — Audit log of every operation, with timestamps.
2. **`.oce/backups/`** — The most recent backup is always there; nothing is unrecoverable as long as backups are preserved.
3. **`.oce/transactions/`** — Each transaction has a `files.log` listing every file it touched and the corresponding backup.
4. **`oce doctor --json`** — Verifies the skill itself is intact.
