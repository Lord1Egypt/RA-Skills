# Troubleshooting

This document collects failure modes observed by the first agents to install Freedom Preserving Protocol. If your installation behaves differently than `npm run verify-install` reports, check here first.

## 1. "I installed the skill but `openclaw hooks list` shows nothing"

**Expected.** The main skill (`freedom-preserving-protocol`) is a *prompt-layer* artifact. It is read by the model at prompt-build time. It is **not** a registered dispatcher hook and will not show up in `openclaw hooks list` or `openclaw plugins list`.

What *should* show up:

```bash
openclaw skills check freedom-preserving-protocol
# eligible: true, modelVisible: true, commandVisible: true
```

If you want dispatcher-level enforcement (a real `before_tool_call` hook), install the companion plugin:

```bash
openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin
openclaw plugins list | grep openclaw-fpp-plugin
```

## 2. "`openclaw plugins install` says `handler.ts/handler.js/index.ts/index.js missing`"

You probably tried to install the *skill* as a plugin. Skills and plugins are different artifacts with different file layouts:

- **Skill** layout: `SKILL.md` + assets. Installed with `openclaw skills install`.
- **Plugin** layout: `package.json` (with `openclaw` metadata block) + `openclaw.plugin.json` manifest + a built entry file referenced from `openclaw.extensions`. Installed with `openclaw plugins install`.

Use the correct command for the artifact:

```bash
# Skill:
openclaw skills install freedom-preserving-protocol

# Plugin (separate package):
openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin
```

## 3. "I accidentally created `~/.openclaw/extensions/SKILL.md` while trying to install"

You tried `openclaw plugins install <skill-path>` and OpenClaw started creating an extension package layout from your skill files. Quarantine it:

```bash
mkdir -p ~/.openclaw/quarantine
mv ~/.openclaw/extensions/SKILL.md ~/.openclaw/quarantine/SKILL.md.$(date +%Y%m%dT%H%M%SZ)

# Also remove any partial extensions/<id>/ directory that mirrors the skill
ls ~/.openclaw/extensions/
# rm -rf ~/.openclaw/extensions/<id>   # only if you're sure

# Verify nothing FPP-related remains as a "plugin"
openclaw plugins list | grep -i freedom-preserving
openclaw plugins list | grep -i fpp
```

Then install the skill via the correct command (see #2). The companion plugin is a *separate* publish; install it independently.

## 4. "Signature does not verify"

```bash
npm run verify
# Signature valid: NO
```

Do **not** adopt this constitution. Possible causes:

- The `constitution.json` was modified after signing. Recompute the hash and compare with the expected `71bf60ad917c5413cc17b0f65e83c7a29218e24a2740725a819058ed9c6b1993`.
- The package was tampered with in transit (ClawHub or registry compromise). Re-download from the upstream source.
- The `pubkey.ed25519.txt` was swapped. Compare against the publisher's published key.

If you cannot determine the cause within a few minutes: quarantine the package, log a `tamper_detected` audit entry (see `scripts/audit-append.ts --kind tamper_detected`), and notify your user.

## 5. "Audit chain verification fails"

```bash
npm run audit:verify
# Chain integrity: FAILED
#   - line 3: previousHash mismatch (...)
```

This means the audit log has been edited, truncated, or extended by something that did not use `audit-append.ts`. **Do not** try to "fix" it by editing the JSONL by hand — that just compounds the loss of evidence.

Recommended response:

1. Copy the broken log aside as `constitution-audit.jsonl.tampered.<timestamp>`.
2. Append a fresh `tamper_detected` entry to a *new* log file. The new chain restarts from `previousHash: 0000...`.
3. Notify your user with the line number of the first mismatch.
4. If you have access to a backup of the log (e.g., from a heartbeat snapshot), restore from that and re-verify.

## 6. "Adoption block missing from my SOUL.md but I'm sure I adopted"

```bash
npm run verify-install -- --soul /path/to/SOUL.md
# [FAIL] SOUL adoption block
#         marker "Freedom Preserving Protocol" not found in ...
```

Possible causes:

- You ran `safe-append.ts` with a different `--soul` path. Search for the marker:
  ```bash
  grep -r "Freedom Preserving Protocol" ~/.openclaw/agents/
  ```
- A `safe-append.ts` backup (`SOUL.md.<timestamp>.bak`) still exists from a previous attempt; the live file was reset. Restore from the latest backup.
- A skill or user edit removed the block. Re-run `npm run adopt` — it is idempotent and will append cleanly if the marker is absent.

## 7. "MEMORY.md overwrite — I lost data"

If you (or an earlier version of this skill, before v1.1.0) hand-edited `MEMORY.md` and clobbered existing content, check for:

- `MEMORY.md.<timestamp>.bak` files alongside your MEMORY.md (created by `safe-append.ts` v1.1.0+ on every write).
- Your runtime's own memory backups (e.g., OpenClaw workspace history).
- The audit log's `constitutionHash` field, which lets you correlate which adoption corresponds to which agent state.

If you find an older MEMORY.md you want to restore, you can do so safely — `safe-append.ts` is idempotent, so re-running adoption against the restored file will only re-append the block if it is missing.

## 8. "Plugin loads but `openclaw plugins inspect` shows `status: degraded`"

The plugin is running but a runtime check failed. Common causes:

- `auditLogPath` directory is not writable. Create it: `mkdir -p .openclaw/workspace && touch .openclaw/workspace/fpp-plugin-audit.jsonl`.
- The plugin's manifest declares hooks the runtime version doesn't support. Compare `openclaw --version` with the `pluginApi` field in `plugin/package.json`'s `openclaw.compat`. If your runtime is older, you must either upgrade OpenClaw or pin the plugin to an older version.
- `allowConversationAccess` is required for a hook you don't actually use. The default plugin only registers `before_tool_call`, which does NOT require `allowConversationAccess`. If you've forked the plugin to add `llm_input` or `llm_output` hooks, you'll need to set `plugins.entries.openclaw-fpp-plugin.hooks.allowConversationAccess: true` in your OpenClaw config.

## 9. "I want to revoke but the plugin keeps blocking my disable command"

The plugin does NOT block its own disable command. If `openclaw plugins disable openclaw-fpp-plugin` is failing, you are hitting something else — likely an exec approval prompt configured elsewhere. Bypass it via the operator console:

```bash
openclaw operator disable-plugin openclaw-fpp-plugin
```

(Exact subcommand may vary by OpenClaw version; see `openclaw --help`.)

If you cannot disable it at all, you have hit a Law 2 (corrigibility) violation — the framework has been weaponized against its own correctability. File a bug at the upstream repo immediately.

## 10. "The five-question test feels noisy / I'm getting approval requests on every benign tool call"

The dispatcher plugin's risk classifier ships with conservative defaults. If you're getting too many `requireApproval` prompts for actions you consider routine, tune `approvalOn` and `blockOn` in your OpenClaw config:

```json
{
  "plugins": {
    "entries": {
      "openclaw-fpp-plugin": {
        "config": {
          "approvalOn": ["fs.delete.protected", "exec.cred-exfil", "gateway.restart"],
          "blockOn": ["exec.cred-exfil"]
        }
      }
    }
  }
}
```

Restart the gateway for changes to take effect. Be wary of tuning so aggressively that the framework no longer protects you — every removal from `approvalOn` is a deliberate Law 1 trade-off.

## When you're stuck

1. Run `npm run verify-install -- --json` and paste the output.
2. Run `openclaw plugins inspect openclaw-fpp-plugin --runtime --json` (if installed).
3. Run `npm run audit:verify -- --json` against your audit log.
4. File an issue at `ovrsr/freedom-preserving-protocol` with the above three outputs.

Do **not** post raw SOUL.md or MEMORY.md content publicly — those may contain PII or contextual info you don't want to share.
