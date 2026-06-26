# Guide the user through config fixes

## Single Finding Fix Flow

1. **Identify the finding**
   - Match user-provided rule_id or description to parsed report data.
   - Extract the finding object with fixSuggestion, alternativeFix, remediation.

2. **Check fix data availability**
   - If `fixSuggestion` is absent or both `configBefore` and `configAfter` are missing:
     STOP auto-fix flow. Tell user: "This finding requires manual remediation."
     Show the finding's `remediation` text and guide manually.
   - If `remediation` is also empty, show the finding's `message` and `description`, and advise user to consult OpenClaw documentation for this rule ID.
   - Otherwise proceed to step 3.

3. **Read target config file**
   - Path: `fixSuggestion.patches[].path` or infer from rule category.
   - Verify file exists and is readable.
   - Parse the JSON file and parse `configBefore` as JSON.
   - Compare only the key paths referenced in `configBefore` against the current file (structural comparison, not full-text string match).
   - If current values already match `configAfter`: report "This fix has already been applied" and skip.
   - If current values differ from both `configBefore` and `configAfter`: STOP. Tell user config has changed since scan, suggest re-scanning.

4. **Create backup**
   Before modifying any config file, create a timestamped backup copy.
   Confirm backup created before proceeding.

5. **Show diff to user**
   ```
   === Fix: {rule_id} ({severity}) — {title} ===
   File: {path}

   --- Current config ---
   {configBefore or current content}

   +++ After fix +++
   {configAfter or patched content}

   Explanation: {fixSuggestion.description}
   ```
   If alternativeFix exists, append:
   ```
   Alternative approach: {alternativeFix.description}
   ```
   Ask: "Apply this fix? (yes / no / use alternative)"

6. **Wait for user confirmation**
   - yes: proceed to step 7.
   - no: skip, log as skipped.
   - alternative: switch to alternativeFix path and re-show diff.

7. **Apply the fix**
   - Priority 1: Use Edit tool with `old_string=configBefore`, `new_string=configAfter` (most precise).
   - Priority 2: Guide user through manual steps using remediation text. Show each step and wait for confirmation.

8. **Validate**
   - Syntax check (JSON files): `python3 -c "import json; json.load(open('{file}'))"`
   - If syntax invalid: immediately rollback from backup, report error.
   - Suggest re-scanning on clawguardsecurity.ai to confirm the finding is resolved.
   - If syntax check passes, the fix is likely correct. A full re-scan on the website will confirm.

9. **Report result**
   - Success: "Fixed {rule_id}. Backup at {backup_path}. Suggest re-scanning on clawguardsecurity.ai to verify full report. Advise user to restart or reload OpenClaw for config changes to take effect."
   - Failure: "Fix did not resolve {rule_id}. Rolled back to backup. {error details}"

---

## Batch Fix Flow

Trigger: user says "fix all", "fix all critical", or lists multiple rule_ids.

1. Collect target findings. Filter by severity if specified.
2. Sort by file (group fixes to same file), then by patch position (bottom-up to avoid offset issues).
3. Show summary table:

   | # | Rule ID | Severity | File | Fix Summary |
   |---|---------|----------|------|-------------|

4. User selects: "all" / specific numbers / "one by one" confirmation mode.
5. Execute fixes sequentially. Each fix gets independent backup + validation. **Re-read the target file before each fix** (critical when multiple fixes target the same file).
6. If any fix fails: stop remaining fixes, rollback failed fix only, report status.
7. After all fixes complete: suggest full re-scan on clawguardsecurity.ai.

---

## Rollback Procedure

Trigger: user says "undo" or "rollback".

1. List available backups and show metadata (date, original file path).
2. User selects which backup to restore.
3. Restore the selected backup to the original path.
4. Verify syntax after restore.
5. Suggest re-scan.

---

## Safety Rules

- NEVER modify files without explicit user confirmation.
- NEVER skip the backup step.
- One fix at a time — validate before proceeding to next.
- If current config values differ from both configBefore and configAfter, STOP and advise re-scanning. If current values already match configAfter, report fix already applied.
- Never delete user backups.
- Prefer Edit tool over Write tool (Edit does minimal changes; Write replaces entire file).
