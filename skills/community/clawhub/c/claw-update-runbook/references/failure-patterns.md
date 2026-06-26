# Failure Patterns

Use this file when the main skill identifies a likely upgrade regression and you need concrete examples of what to inspect.

Contribution rule:
- append new patterns or expand existing ones
- do not delete older patterns unless they are proven false
- preserve examples from other hosts even if the current host is healthy

## 1. Update channel drift

Symptom:
- host is intentionally on beta or a newer stable build
- `status --deep` says local version is newer than `npm latest`
- config still says `"update.channel": "stable"` after a beta install

What to inspect:
- `openclaw --version`
- `openclaw status --deep`
- `openclaw.json` update metadata

Why it matters:
- operators get misleading update advice
- handoff notes should call out when install/update channel state is not persisted

## 2. Stale config after upgrade

Symptom:
- `doctor` says provider or plugin is unknown
- runtime falls back to auto-detect or legacy behavior
- helper commands claim to fix config, but warnings remain

Common keys:
- `tools.web.search.provider`
- `plugins.allow`
- `plugins.entries.*`

Typical example:
- `tools.web.search.provider=brave` remains after host/plugin changes and becomes invalid

## 3. Bundled plugin vs global npm plugin shadowing

Symptom:
- bundled capability should work after host upgrade
- `plugins list` shows a global plugin path under `~/.openclaw/npm/node_modules`
- plugin version does not match host version

Example:
- host on `<current-version>`
- global `@openclaw/discord` still at `<previous-version>`
- gateway warns about missing compiled runtime output because the global plugin is source-only

What to inspect:
- `openclaw plugins inspect <id>`
- plugin `source`
- plugin `origin`
- plugin `version`
- presence of `dist/`

## 4. Install records drift from disk reality

Symptom:
- config or install registry says a plugin is installed
- recorded path under `~/.openclaw/npm/node_modules/@openclaw/` or `~/.openclaw/extensions/` does not exist
- plugin not found / phantom allowlist warnings

What to inspect:
- `~/.openclaw/plugins/installs.json`
- actual install path on disk
- `openclaw plugins registry --refresh`

This is the case where reinstalling the plugin is often correct.

## 5. Third-party plugin runtime deps removed

Symptom:
- after `doctor --fix` or cleanup, a third-party plugin fails to load
- error looks like `Cannot find module ...`
- plugin root still exists, but plugin-side `node_modules` is gone

What to inspect:
- plugin package directory
- plugin `package.json`
- whether dependencies are externalized at build time

Why it matters:
- cleanup can be too aggressive for non-bundled plugins

## 6. Context engine not registered after restart

Symptom:
- logs say context engine falls back to legacy
- plugin may still be installed but failed to initialize

Look for:
- plugin load errors
- missing dependencies
- plugin contract warnings
- plugin registry metadata drift

## 7. Event loop degradation after update

Symptom:
- `channels status --deep` reports degraded event loop
- logs show lane wait exceeded, active-memory timeouts, or restart blocked by active tasks

Common culprits:
- stale running tasks
- active-memory timeout loops
- plugin load retries
- long-running approval followups

Check:
- `openclaw tasks audit`
- recent `gateway.err.log`
- recent `gateway.log`

## 8. Task ledger blocks clean restart

Symptom:
- restart or drain says blocked by active task runs
- `tasks audit` shows `stale_running`, `lost`, or repeated delivery failures

Useful commands:
- `openclaw tasks show <id>`
- `openclaw tasks cancel <id>`
- `openclaw tasks maintenance --apply`

Fix the ledger if it is obviously wrong; otherwise every later health check becomes noisy.

## 9. Command-path disagreement

Symptom:
- `status --deep` says a channel token is unavailable in this command path
- `channels status --deep` says channel is connected and healthy

Treat this as a reporting mismatch first, not a real outage.

Additional example:
- A channel can be healthy in the gateway service with `token:env`, while `doctor` still warns that the corresponding token env var is absent in the doctor environment.
- Verify the service env file and `channels status`; do not treat the doctor shell-env warning alone as proof the live gateway is down.

## 10. What to hand the next operator or support contact

When a problem looks like an update regression, capture:

- host version before and after
- whether the capability was bundled, npm-installed, or ClawHub-installed
- the plugin source path actually loaded
- stale config keys still present after fix attempts
- exact `doctor` and `plugins doctor` messages
- startup log lines around the failure

## 11. Plugin updater follows stale install records

Symptom:
- core OpenClaw is updated, but `~/.openclaw/plugins/installs.json` still records older plugin specs
- `openclaw plugins update --all` tries to reinstall the older recorded versions instead of reconciling to the currently installed packages
- plugin directories under `~/.openclaw/npm/node_modules/@openclaw/` may disappear or config suddenly becomes invalid until the exact desired versions are reinstalled

Typical example:
- host core is updated
- install records still point at older plugin specs
- running `openclaw plugins update --all` attempts the old plugin specs and leaves channel plugins missing on disk until the intended package versions are reinstalled

What to inspect:
- `~/.openclaw/plugins/installs.json`
- actual package versions in `~/.openclaw/npm/node_modules/@openclaw/*/package.json`
- whether the plugin directories still exist after `plugins update --all`

Why it matters:
- the built-in updater can deepen an upgrade regression if install metadata drift is not corrected first
- prefer reconciling install records or reinstalling exact target versions before trusting `openclaw plugins update --all`

Refinement:
- `openclaw plugins registry --refresh` does NOT rewrite the install record's `spec` field. It refreshes `hostContractVersion` and compatibility data only.
- After a refresh, install records can still carry pinned specs like `<plugin>@<older-version>` even when the disk version is `<newer-version>`. `plugins update --all` will then **downgrade** the on-disk plugin to match the pinned spec.
- Correct sequence to actually move a third-party plugin forward:
  1. `openclaw plugins update <id> @<scope>/<pkg>@latest` (note: `update` accepts an explicit spec; this rewrites the install record's spec).
  2. Or `openclaw plugins install <pkg>@latest --force` to drop the pin.
- `--all` is safe only after every install record's `spec` already points at `@latest` or the desired version — never trust it after a host upgrade without spot-checking install records first.

## 12. Control UI token mismatch after restart

Symptom:
- gateway is healthy and reachable
- dashboard page loads, but websocket auth fails
- `gateway.err.log` shows `[ws] unauthorized ... reason=token_mismatch`
- log text may say `unauthorized: gateway token mismatch (open the dashboard URL and paste the token in Control UI settings)`

What to inspect:
- recent `~/.openclaw/logs/gateway.err.log` websocket auth lines
- whether `gateway.auth.token` or its SecretRef source changed during reinstall/restart
- whether the browser-side Control UI is still holding an older token

Why it matters:
- this can look like a gateway outage even when the backend is healthy
- separate UI auth cache problems from real startup or channel failures before changing server-side config again

## 13. Channel SecretRef resolves but runtime account still cannot use it

Symptom:
- `openclaw config validate` passes
- `openclaw secrets audit` reports `unresolved=0`
- `openclaw channels status` says a channel is configured but stopped/disconnected with `secret unavailable in this command path`
- logs say a channel token is unavailable, for example a channel delivery path says the bot token configured for account `default` is unavailable

What to inspect:
- the channel token config path, for example `channels.discord.token`
- the referenced secrets provider and backing file
- whether the gateway service env has a working token fallback
- whether the channel plugin prefers the broken config SecretRef over the env fallback

Observed workaround:
- add the token to the service env from the existing local secret source
- remove the broken channel token config field so the channel falls through to the env-token path
- restart gateway and verify `channels status` reports `token:env` and connected

Why it matters:
- schema validation and secrets audit can both pass while the channel runtime still cannot consume the SecretRef
- this can leave a channel integration down after an update even though the secret exists

Confirmed regression scope:
- Reproduced cleanly across multiple adjacent channel-plugin versions with a SecretRef pointing at a valid `secrets.json` entry.
- `openclaw secrets audit` reports `unresolved=0`, `openclaw secrets reload` says "Secrets reloaded.", but the channel plugin still throws `unresolved SecretRef ... Resolve this command against an active gateway runtime snapshot before reading it.` at startup.
- Sibling plugins using the same SecretRef shape (e.g. brave's `/brave_api_key`) resolve fine — the bug is plugin-side, not in the secrets layer.
- Pragmatic workaround (when env fallback isn't available): inline the literal token into the affected channel token field. This adds one entry to `secrets audit --plaintext` findings but restores the channel. Plan to revert once upstream `@openclaw/discord` ships a fix that resolves SecretRefs against the runtime snapshot.

Addendum — `token:config` in `channels status` is ambiguous:
- the same status row appears whether the token came from a successfully resolved SecretRef OR from an inline literal (workaround applied); it is not a signal that the upstream bug is fixed.
- To disambiguate, inspect the actual config field directly:
  - `node -e 'const c=JSON.parse(require("fs").readFileSync(process.env.HOME+"/.openclaw/openclaw.json","utf8")); console.log(typeof c.channels?.discord?.token, c.channels?.discord?.token)'`
  - `string` value → inline literal (workaround in place)
  - `object` value → SecretRef (relies on plugin runtime resolution)
- An operator running this runbook on an inherited host should not assume `token:config` means the regression is gone; verify the field shape before claiming the workaround is no longer needed.

## 14. Gateway CLI start reports argument error but managed service recovers

Symptom:
- after update, `openclaw gateway start` prints an argument-count error
- the command may still re-bootstrap the managed service afterward
- the service manager and open port check show the gateway running despite the CLI error

What to inspect:
- the host service-manager status command
- listener on the configured gateway port
- `openclaw status`
- gateway stdout/stderr logs

Why it matters:
- the CLI error is alarming but may not be the actual outage
- verify service reality before retrying installs or rolling back

## 15. `plugins uninstall` is destructive of every config trace, not just the install record

Symptom:
- after `openclaw plugins uninstall <id> --force`, the plugin disappears from `plugins list` as expected
- but the plugin then shows as `disabled` once you try to re-enable a sibling install (e.g., a copy under `~/.openclaw/extensions/`)
- exclusive slots (e.g., `plugins.slots.contextEngine`) silently revert to `legacy`

What `uninstall` can remove:
- the install record in `~/.openclaw/plugins/installs.json`
- the on-disk install directory
- `plugins.entries.<id>` from `openclaw.json`
- the `<id>` entry from `plugins.allow`
- exclusive slot assignments where `<id>` was the holder

Recovery after rolling back to a different copy of the same plugin:
- `openclaw plugins enable <id>` re-adds the entry, allowlist row, and slot assignment
- restart gateway

CLI flag note:
- `plugins uninstall` does not accept `--yes`, `-y`, or `--non-interactive`. Use `--force` to skip the confirmation prompt over a non-interactive shell.

Why it matters:
- treat `uninstall` as "wipe all traces", not as "remove just the install record"
- if you only wanted to swap install paths (npm → extensions or vice versa), prefer manual relocation + `plugins registry --refresh` over `uninstall` + reinstall

## 16. Third-party plugin declares optional peer dependency but compiled bundle imports it unconditionally

Symptom:
- after upgrading a third-party plugin, `plugins doctor` reports a load failure like `Error [ERR_MODULE_NOT_FOUND]: Cannot find package '<peer-package>'`
- the plugin's `package.json` lists the missing package under `peerDependenciesMeta` with `optional: true`, suggesting it should be skippable

Root cause:
- the published `dist/index.js` was emitted with an unconditional `import` of an "optional" peer dependency
- Node's ESM resolver cannot satisfy the import, so the plugin fails to load even though `package.json` says the dep is optional

Typical example:
- `<plugin>@<version>` declared `<peer-package>` as `peerDependenciesMeta.<dep>.optional: true`
- the plugin still failed to load because `dist/index.js` imported it unconditionally
- the previous version shipped a bundled `node_modules/` next to the plugin and worked fine
- `plugins update --all` on a host with a stale install record (pattern #11) may downgrade instead, masking this as a different failure mode

What to inspect:
- `package.json` `peerDependencies`, `peerDependenciesMeta`, `dependencies`, `devDependencies`
- the actual import sites in `dist/index.js` (`grep -E "from '@.*pi-" dist/index.js`)
- whether a previous version's bundled deps are still on disk (e.g., `~/.openclaw/extensions/<id>.stale-*` or `.backup-*` directories)

Recovery:
- roll back to the last known-good plugin version, ideally one that bundled its deps
- prefer renaming the broken install dir (e.g., to `<dir>.broken-<date>`) over deleting it, so the failure can still be reproduced for an upstream report
- share upstream or with support: declared optional deps in `package.json` vs unconditional imports in `dist`

Why two hosts on the same plugin version can show different results:
- the bug only surfaces when Node's ESM resolver cannot find the "optional" peer from the plugin's location
- on hosts where the peer is **hoisted** at `~/.openclaw/npm/node_modules/<scope>/<peer>` (sibling to the plugin), the import succeeds silently and `plugins doctor` reports clean
- the peer can also be satisfied by a copy under `<global-openclaw>/node_modules/<scope>/<peer>` (bundled with the host package), or by leftover `~/.openclaw/plugin-backups/<id>.*/node_modules/<scope>/<peer>` directories from a prior disabled install
- a host that recently ran a clean reinstall (or `npm prune`, or a `doctor --fix` cleanup that removed disabled plugin backups) is more likely to hit the failure than a host that has accumulated multiple historical copies of the peer
- if you reproduce the bug, also enumerate every on-disk copy of the peer before rolling back, so you can explain the divergence to upstream:
  ```
  find ~/.openclaw <global-node-modules> -maxdepth 6 -type d -name "<peer-package-name>"
  ```

Inspection note:
- `dist/index.js` is typically a single esbuild-bundled minified line; `grep` will appear to match the entire file. Use `grep -oE "from'@[^']+'" dist/index.js` (or similar token-level patterns) to enumerate actual import specifiers without dumping the bundle.

Why it matters:
- this is not a missing-dep on the operator's side — it is a packaging defect
- avoid the temptation to manually `npm install` the missing peer into the plugin dir, because the next `plugins update` will overwrite the directory and the fix will silently disappear
- the resolver-luck variance is itself the bug: a plugin that "works on my host" but breaks for the next operator is the same defect, not a host configuration difference; do not dismiss the upstream report because your host happens to satisfy the import

## 17. "Duplicate plugin id detected" warning text wraps in a self-referential way

Symptom:
- `plugins doctor` and `openclaw doctor` warn: `plugin <id>: duplicate plugin id detected; global plugin will be overridden by global plugin (/path/A)`
- only one path is visible at a glance; the second path is wrapped to a later line and easily missed
- on a narrow terminal the warning can look self-referential ("global plugin will be overridden by global plugin (X)") and is easy to dismiss as a UI bug

Reality:
- the warning is real — there are two on-disk plugin manifests for the same id
- the conflict is almost always between `~/.openclaw/extensions/<id>/` and `~/.openclaw/npm/node_modules/<scope>/<id>/` (or two copies under the same root)
- the npm path generally wins, but the extensions path still triggers the warning every restart

What to inspect:
- `find ~/.openclaw -maxdepth 4 -type d \( -name "<id>" -o -name "@*<id>*" \)`
- whether `plugins.load.paths` in `openclaw.json` is empty or pointing at an extra root
- whether a previous `plugins update --all` left a `.backup-*` directory next to the new install (those are typically ignored, but a renamed-not-deleted manual copy can be picked up)

Recovery:
- pick the canonical install (npm-tracked is preferred for plugins managed via `openclaw plugins install`)
- rename the unwanted copy to `<dir>.stale-<date>` (safer than `rm -rf` mid-runbook)
- restart gateway and confirm `plugins doctor` reports zero errors and the warning is gone

Why it matters:
- operators often dismiss this as cosmetic; it is not — the second path keeps generating doctor noise that masks new regressions
- the warning text formatter wraps poorly; always re-read the full multi-line warning before deciding the conflict is benign

True false-positive variant:
- after archiving every redundant on-disk copy and confirming `find ~/.openclaw -maxdepth 6 -name 'openclaw.plugin.json' | xargs grep -l '"<id>"'` returns only the canonical install path, the warning can still persist
- `openclaw plugins inspect <id>` then shows the warning's path field is **identical** to the loaded plugin's `Source` path — i.e., the warning is comparing the manifest against itself
- this looks like an OpenClaw bug where the same manifest is being matched twice (once via the `installs.json` install record, once via filesystem scan) and both lookups are tagged `Origin: global`, generating a phantom duplicate
- distinguishing genuine #17 (two real manifests on disk) from this false-positive: run `plugins inspect <id>` and compare the `Source` line to the path inside the WARN line. Same path = false positive. Different paths = genuine duplicate, keep hunting.
- when it is the false positive, leave it alone; do not delete the canonical install in an attempt to silence it

## 18. Bundled provider discovery mode change after host upgrade

Symptom:
- after upgrading the host package, `openclaw doctor` adds a new warning:
  `plugins.allow is restrictive, but bundled provider discovery is still in legacy compatibility mode. Bundled provider plugins can ... set plugins.bundledDiscovery to "allowlist" after confirming omitted providers.`
- previously absent config key is now expected: `plugins.bundledDiscovery`

Background:
- `plugins.allow` historically gated only third-party plugins; bundled provider plugins (anthropic, openai, gemini, etc.) were always discoverable.
- a host release introduced `plugins.bundledDiscovery` with two modes:
  - `"compat"` — preserves legacy behavior; bundled providers stay discoverable regardless of `plugins.allow`
  - `"allowlist"` — bundled providers must also appear in `plugins.allow`
- Hosts upgraded from an older config shape can inherit the legacy behavior implicitly, and doctor may flag it until the key is set explicitly.

What to do:
- if `plugins.allow` is restrictive and you intentionally rely on bundled providers, set `plugins.bundledDiscovery: "compat"` to lock in current behavior — note that this **does not silence the doctor warning**, it only pins the mode against a future default flip (see refinement below)
- if you want strict allowlisting end-to-end and want the warning gone, audit which bundled providers your agent fallback chains require, add them to `plugins.allow`, then set `plugins.bundledDiscovery: "allowlist"`

Refinement:
- Some releases auto-migrate `plugins.bundledDiscovery` to `"compat"` during the host upgrade, so the key may already be set even on hosts that never had it explicitly. Always re-read the live config before assuming the warning means the key is unset.
- Even with `"compat"` explicitly set, doctor continues to print: `plugins.allow is restrictive, but bundled provider discovery is still in legacy compatibility mode ... set plugins.bundledDiscovery to "allowlist" after confirming omitted bundled providers are intentionally blocked`. The warning is the doctor's nudge to migrate forward, not a "key missing" warning. Two paths to silence:
  1. Migrate to `"allowlist"` (recommended): enumerate the bundled providers your agents actually need by walking `c.agents.defaults.model.{primary,fallbacks}` and any agent-level overrides; the model strings are typically `provider/model` shaped (e.g., `anthropic/claude-opus-4-7`, `openai-codex/gpt-5.5`). Map each `provider/` prefix to its bundled plugin id (`openai-codex` → `openai`, since the openai plugin owns both `openai` and `openai-codex` provider ids). Add the corresponding plugin ids to `plugins.allow`, set `plugins.bundledDiscovery: "allowlist"`, restart, and re-run doctor.
  2. Accept the persistent warning and rely on `"compat"` — fine for now, but re-audit after every minor bump in case a future version changes the warning into an error.
- When migrating to `"allowlist"`, also confirm the corresponding API-key env vars are present in the service env (e.g., `ANTHROPIC_API_KEY` for the `anthropic` plugin); plugins added to `plugins.allow` without credentials will load but fail at first use, which is harder to diagnose than a discovery warning.

Why it matters:
- this is a config-shape change introduced silently by a minor version bump; treat it as a host-upgrade follow-up, not a one-off doctor warning
- ignoring it doesn't break anything today, but a future minor that flips the default to `"allowlist"` will instantly regress provider discovery on every host that hasn't pinned the mode

## 19. CLI uninstall confirmation prompt blocks non-interactive runbooks

Symptom:
- `openclaw plugins uninstall <id>` prints `Uninstall plugin "<id>"? [y/N]` and then exits without doing anything in a non-interactive shell (e.g., a single ssh command with no stdin).
- stderr may include an unrelated `Detected unsettled top-level await` warning that obscures the real reason (no input piped to the prompt).

What to do:
- always pass `--force` for non-interactive uninstalls
- `--yes` and `-y` may not be accepted; use `--force` when the command help confirms it skips the prompt
- if you also want a preview, run `--dry-run` first

Why it matters:
- a runbook that pipes a single `ssh` command without a TTY will silently no-op the uninstall, then proceed to "verify" steps that report the plugin still present and confuse the operator into deeper changes

## 20. Multi-step SSH update command disconnects mid-run while the box keeps working

Symptom:
- operator runs a single multi-step `ssh user@host '... stop ... npm install ... reinstall plugins ... start ...'` command
- the SSH session appears hung or returns no output to the operator's terminal
- reconnecting with a fresh ssh shows the box has actually completed most or all of the work — versions bumped, gateway running, plugins on disk

What's happening:
- when one of the inner steps restarts launchd or replaces the wrapper script the gateway plist sources, the parent shell association can break and the local ssh client stops receiving stdout, even though the remote `zsh -c '...'` keeps running detached and finishes the script.
- the remote orphan can persist as a `zsh -c` process for minutes after the parent ssh exits.

What to inspect:
- on the remote host: `pgrep -fl "openclaw/dist/index.js gateway"` (current gateway PID and command line)
- `pgrep -fl "zsh -c"` for orphan wrapper processes from the disconnected session
- on-disk plugin versions vs `npm view @openclaw/<id> version`
- `~/.openclaw/logs/gateway.log` for the latest `http server listening` line (confirms a fresh restart actually happened)

Recovery:
- kill orphan wrapper zsh processes (`kill <pid>`)
- re-run the verification suite (`openclaw --version`, `openclaw plugins doctor`, `openclaw channels status`, `openclaw tasks audit`) from a fresh ssh session
- do NOT re-run the update script blindly; it may have completed successfully and a second run can re-pin install records to versions that were just bumped

Practical advice:
- prefer breaking the update into separate ssh invocations per phase: stop → host update → plugin reinstalls → start → verify. A disconnect then loses only the current phase, not the whole sequence.
- where a single transactional run is unavoidable, redirect the script's output to a remote file (`> /tmp/openclaw-update.log 2>&1`) and tail it from a second ssh session, so the parent disconnect does not lose the audit trail.

Why it matters:
- treating an apparent hang as failure and rerunning can corrupt install records mid-flight
- the runbook's "verify" step must rely on freshly inspected box state, not on the success path of the update command's stdout

## 21. Version drift between operator sessions on hosts with autopilot agents

Symptom:
- operator returns to a host they audited recently and finds a different `openclaw --version` than what they last left it on
- no explicit operator-initiated update happened in the interim
- `update.auto.enabled` may be `false` in `openclaw.json`, but the host still moved versions

Background:
- some hosts run autopilot or scheduled cron agents (e.g., `gbrain`, `com.gbrain.autopilot.plist`, scheduled openclaw cron jobs) that may bump `openclaw` or its plugins out of band, ignoring the host-level update channel/auto flag
- the `meta.lastTouchedVersion` field in `openclaw.json` only reflects the last writer, not the last installer

What to do:
- always re-snapshot the live state at session start, even within hours of the previous session:
  - `openclaw --version`
  - per-plugin disk versions: `for d in ~/.openclaw/npm/node_modules/@*/*/; do node -e 'process.stdout.write(JSON.parse(require("fs").readFileSync(process.argv[1])).name+" "+JSON.parse(require("fs").readFileSync(process.argv[1])).version+"\n")' "$d/package.json"; done`
  - any service-env or config edits applied by previous workarounds
- do not rely on prior-session memory for current state; treat every session as a fresh audit

Why it matters:
- a stale mental model leads to the wrong fix path — e.g., applying an env-var workaround when a literal-inline workaround is already in place, or "rolling back" an update the operator never made
- two parallel operator sessions (or an operator + a long-running autopilot) can converge on contradictory workarounds if neither re-snapshots first

## 22. Cohort version snapshot before host update

Practice:
- before stopping the gateway, capture every plugin's installed version with a single command:
  ```
  for d in ~/.openclaw/npm/node_modules/@*/*/; do
    node -e 'const p=JSON.parse(require("fs").readFileSync(process.argv[1])); process.stdout.write(p.name+"@"+p.version+"\n")' "$d/package.json"
  done | sort > /tmp/openclaw-pre-upgrade-plugins.txt
  ```
- after the upgrade, re-run the same command into `/tmp/openclaw-post-upgrade-plugins.txt` and `diff` them.
- a clean cohort upgrade should show every plugin version moving in the diff; any plugin that did NOT move is a candidate for shadow drift (Pattern #3) once the host moves further.

Why it matters:
- a `plugins install <pkg>@latest --pin --force` no-op (e.g., from a network or registry hiccup, or because npm latest temporarily lagged ClawHub) is invisible until you hit a sub-feature that depends on the new version.
- without the snapshot/diff, the operator cannot prove the cohort actually moved — only that the host did.
- the snapshot also documents what to roll back to if the new cohort surfaces a packaging defect (Pattern #16).

## 23. Service-env writer corrupts string secrets with literal double-quote wrapping

Symptom:
- a previously working channel returns auth failure from the upstream API immediately after a host upgrade, even though `channels status` reports `token:env` and the channel was healthy before the upgrade
- `secrets audit` reports `unresolved=0` and the underlying value in `secrets.json` is unchanged
- the channel reconnects fine if you manually re-paste the token into the env file

Root cause:
- the service-env writer JSON-encodes string values from `secrets.json` (wrapping them in `"`) and **then** shell-single-quotes the result for the env file
- the resulting line looks like `export CHANNEL_TOKEN='"<token>"'` — the outer single quotes are correct shell quoting, but the inner literal `"` characters become part of the value when the env file is sourced
- the upstream API receives a token with stray leading and trailing `"` chars and rejects it
- the bug only surfaces the next time the env file is regenerated (a host upgrade, certain `doctor --fix` runs, plugin reinstalls), so it presents as "the upgrade broke the channel" rather than a config drift

What to inspect:
- the raw bytes of the env line, not just the masked output:
  ```
  node -e 'const fs=require("fs"); const p=process.env.HOME+"/.openclaw/service-env/<service-env-file>"; const l=fs.readFileSync(p,"utf8").split("\n").find(l=>l.startsWith("export <TOKEN_ENV_NAME>=")); console.log(JSON.stringify(l))'
  ```
- a clean line has a single shell-quoted token value with no inner literal double quotes
- a corrupted line has literal `"` characters just inside the shell quotes
- check every `*_TOKEN` / `*_API_KEY` line in the env file the same way; the same writer emits all of them

Recovery:
- back up the env file: `cp <env> <env>.bak-token-fix-<date>`
- rewrite the affected lines using the value from `secrets.json` (which is the canonical clean value), shell-single-quoted with no inner JSON wrapping; only safe if the secret itself contains no single quotes (almost always the case for API tokens)
- restart the gateway through the host service manager
- re-run `openclaw channels status --deep` and confirm the channel reconnects

Why it matters:
- this is a packaging defect in the env-file writer, not operator drift; the local fix is fragile because the next regeneration will re-corrupt the file
- share upstream or with support: exact line bytes, the source `secrets.json` value type (string), and the affected host version
- until upstream ships a fix, treat any operation that may rewrite `service-env/*.env` (host updates, plugin updates, `doctor --fix` involving secrets) as a channel-auth outage risk and re-verify channel auth immediately after

Workflow addendum:
- when post-update channel health shows auth failure, **inspect the env file's raw bytes for quote corruption before assuming the upstream credential was rotated**. The wrong diagnosis path leads to credential rotation and operator confusion; the right diagnosis takes 30 seconds.

## 24. Non-interactive SSH hides the OpenClaw binary

Symptom:
- `ssh host 'openclaw --version'` returns `command not found`
- the same host has a working managed service and `openclaw status` works in an interactive shell
- service-manager status may also look wrong if the operator guesses an old service label

What to inspect:
- `echo "$PATH"` inside the non-interactive SSH command
- common binary locations for the host's package manager and `~/.local/bin/openclaw`
- the actual service label or name
- the gateway command and port inside the service definition or `openclaw status --deep`

Observed example:
- non-interactive SSH inherited only `/usr/bin:/bin:/usr/sbin:/sbin`
- OpenClaw was installed under a package-manager prefix
- the gateway service label was not the older guessed label
- the live gateway port differed from an old hard-coded health port, so probing the old port falsely reported an outage

Why it matters:
- a stripped SSH `PATH` can look like a missing installation
- an old label or hard-coded port can make a healthy gateway look stopped
- always establish the command path, label, and port before running update or repair commands

## 25. Update stop phase may need service-manager fallback even after clean gateway SIGTERM

Symptom:
- `openclaw update --channel <channel>` prints that the normal service stop did not fully stop the service
- updater reports it used a stronger stop/unload fallback and left the service unloaded before continuing
- gateway logs may show a clean `SIGTERM` shutdown, followed by a short-lived restart that is immediately terminated before the package swap completes

What to inspect:
- update command stdout/stderr
- the host service-manager status command before and after the update
- recent gateway logs around the stop/restart window
- final `openclaw status --deep`, `/health`, and managed-service PID

Why it matters:
- this is a lifecycle hiccup, not necessarily an update failure
- do not rerun the update just because the normal stop needed fallback; first verify the final service is loaded/running and the gateway responds on its configured port
- include the stop/fallback lines in handoff notes, because they show service-manager semantics the updater had to recover from

## 26. Selected update channel has no matching external plugin release

Symptom:
- host updates successfully to a selected channel such as beta
- an external plugin cannot be found on npm for `<package>@<channel>`
- updater falls back to another tag such as `@latest`
- post-update `plugins doctor` can still be clean, but the host is now running a mixed channel cohort

Observed example:
- host updated to a selected channel build
- one third-party plugin had no `@beta` release and fell back to `@latest`
- a globally installed official channel plugin did update to the matching beta version
- plugin peer dependency links were repaired during the update

What to inspect:
- update output for `Package not found on npm` and `falling back` lines
- `openclaw plugins list --json` for each enabled plugin's `origin`, `source`, and `version`
- `~/.openclaw/plugins/installs.json` to see whether the recorded spec now points at the intended version/tag

Why it matters:
- "host on beta" does not imply every external plugin is on beta
- a clean `plugins doctor` proves loadability, not cohort consistency
- handoff notes should separate OpenClaw-bundled plugin behavior from external plugin publishing gaps

## 27. Transient post-restart scope and pricing warnings can coexist with healthy channels

Symptom:
- immediately after restart, gateway logs show websocket responses like `missing scope: operator.read`
- `status --deep` reports a noncritical external catalog or pricing fetch degraded
- channels remain connected and `/health` reports live

What to inspect:
- whether the scope errors are confined to the seconds after restart
- whether later `channels status --deep` is connected
- whether `/health` returns `{"ok":true,"status":"live"}`
- whether the warning is tied to a third-party catalog/pricing fetch rather than local gateway startup

Why it matters:
- these warnings are useful to report, but they should not be conflated with a failed package update
- stale Control UI/websocket clients can race the new gateway during restart
- external catalog/pricing fetch failures may degrade status without affecting channel delivery or plugin loading

## 28. Codex OAuth model migration succeeds in config but fails at runtime

Symptom:
- an OAuth-only OpenAI/Codex host has working `openai-codex/gpt-*` refs before upgrade
- `doctor` or `update` rewrites agent and cron refs to `openai/gpt-*`
- session/status tables may show the display model as `gpt-5.5` and the runtime as `OpenAI Codex`
- a direct agent run returns `status: ok`, but metadata shows the OpenAI/Codex primary route failed and a fallback provider won

What to inspect:
- `agents.defaults.model.primary`
- `agents.defaults.models` and every `agents.list[*].models` entry for `agentRuntime.id`
- cron payload models in `~/.openclaw/cron/jobs.json`
- direct smoke test metadata: provider, model, runtime/harness, and `fallbackAttempts`
- recent gateway logs around `agent model:` and provider fallback decisions

Typical failures:
- direct `openai/gpt-*` route fails with direct OpenAI API-key auth on an OAuth-only host
- migrated `openai/gpt-*` route selects a new `codex` runtime but fails before model execution
- restored `openai-codex/gpt-*` route reaches the old provider but fails on request-shaping or tool-schema validation

Why it matters:
- `status: ok` is not proof that the intended OpenAI/Codex route works; fallbacks can mask the primary-route regression
- cron jobs can be silently migrated independently of agent defaults and then fail later when they fire
- do not claim a model-routing fix is verified until a fresh direct run completes on the intended provider/runtime with no unexpected fallback

Verification command shape:
```
openclaw agent --agent main --session-id <fresh-id> --message "Reply exactly: SMOKE_OK" --timeout 120 --json
```

The result is healthy only if:
- the payload text is correct
- the final provider/model match the intended primary route
- runtime/harness matches the intended path
- `fallbackAttempts` is empty or contains only known benign retries

## 29. `@openclaw/codex` package import resolves `root-alias.cjs` as a directory

Symptom:
- update installs or enables `@openclaw/codex`
- model entries route `openai/gpt-*` through `agentRuntime.id: "codex"`
- direct agent smoke falls back with:
  `Cannot find module '<global-openclaw>/dist/plugin-sdk/root-alias.cjs/codex-native-task-runtime'`
- on disk, `root-alias.cjs` is a file and `codex-native-task-runtime.js` is its sibling

What to inspect:
- `~/.openclaw/npm/node_modules/@openclaw/codex/package.json`
- `~/.openclaw/npm/node_modules/@openclaw/codex/dist/run-attempt-*.js`
- `<global-openclaw>/dist/plugin-sdk/root-alias.cjs`
- `<global-openclaw>/dist/plugin-sdk/codex-native-task-runtime.js`
- whether `plugins.entries.codex` exists or whether `codex` is activated as a special runtime plugin outside normal plugin entries
- both `openclaw plugins inspect codex` and `openclaw plugins list --json`; these can disagree, with `inspect` reporting `Status: loaded` while the JSON list shows `"enabled": false` / `"status": "disabled"` for the same package

Useful snapshot:
```
node -e 'const fs=require("fs"); const p=process.env.HOME+"/.openclaw/npm/node_modules/@openclaw/codex/package.json"; console.log(JSON.stringify(JSON.parse(fs.readFileSync(p,"utf8")), null, 2))'
find <global-openclaw>/dist/plugin-sdk -maxdepth 2 -type f | grep -E "root-alias|codex-native"
```

Why it matters:
- this is likely an OpenClaw package/import-path bug, not local credential drift
- reverting only the model id may hide the package bug by moving traffic back to an older provider path
- handoff notes should include the exact package version and sanitized file layout
- `plugins doctor` may still say "No plugin issues detected"; do not treat plugin doctor alone as proof the `codex` agent runtime can execute

Observed in 2026.5.12-beta.2:
- update auto-installed missing configured plugin `codex` from `@openclaw/codex@beta`
- `plugins inspect codex` reported package version `2026.5.12-beta.2` and `Status: loaded`
- raw plugin JSON showed the same plugin as disabled
- direct smoke with `openclaw agent --model openai/gpt-5.5 --json` failed immediately with the `root-alias.cjs/codex-native-task-runtime` module path error
- the expected file existed as `<global-openclaw>/dist/plugin-sdk/codex-native-task-runtime.js`, adjacent to `<global-openclaw>/dist/plugin-sdk/root-alias.cjs`

## 30. OpenAI-compatible tool schema rejects arrays missing `items`

Symptom:
- the OpenAI/Codex route reaches request validation, then fails with a 400 schema error
- fallback succeeds on a provider with looser or different tool-schema validation
- error text resembles:
  `Invalid schema for function '<tool>': In context=('properties', '<array_field>'), array schema missing items.`

What to inspect:
- the failing tool name and plugin owner
- the generated tool schema passed to OpenAI/Codex
- plugin schema source if the tool belongs to a plugin
- request-shaping code that converts tool definitions between provider schema formats

Why it matters:
- this blocks the primary route even when credentials and runtime selection are correct
- fallback success can make the agent appear healthy while all GPT/OpenAI primary runs are actually rejected before completion
- the local workaround is usually to remove/fix the bad tool from the agent toolset or fall back to another provider, but the upstream fix should validate/sanitize schemas before dispatch

Handoff guidance:
- sanitize the tool name if it reveals private app naming, but keep the field path and JSON Schema error text
- state whether the same agent run succeeded only through fallback
- include the OpenClaw version and provider/model that rejected the schema

## 31. Updater restart step runs under the previous CLI after package swap

Symptom:
- `openclaw update --channel beta` reports a successful package swap from version X to version Y
- during restart it warns that config was written by version Y, but the current command is running version X
- updater then says the gateway already reports version Y and skips a redundant restart

What to inspect:
- `openclaw --version` from a fresh shell
- `which openclaw`
- `openclaw gateway status --deep` or `openclaw status --deep`
- managed-service command path and live gateway version

Why it matters:
- this may be harmless if the gateway is actually running the new version, but it is confusing in beta validation
- it can mask real CLI/global-install/service path mismatches
- capture the warning for the next operator or support contact, but verify service reality before rerunning the update

## 32. `cron run --expect-final` proves enqueue but not final completion

Symptom:
- `openclaw cron run <id> --expect-final --timeout <ms>` returns quickly with an enqueue-style JSON payload
- no final agent result is included even though help says the flag waits for the final response
- `openclaw cron runs` may require `--id`, which makes broad post-update polling less discoverable

What to inspect:
- exact CLI version
- `openclaw cron run --help`
- `openclaw cron runs --help`
- run history for the specific job id
- job status after a delay

Why it matters:
- cron verification after an update can be falsely marked complete when only enqueue was proven
- for handoff notes, distinguish "manual run enqueued" from "manual run completed successfully"
- pair manual cron runs with a delayed status/history poll before declaring cron healthy

## 33. Discord offline because the managed gateway service is installed but unloaded

Symptom:
- Discord shows the bot offline, and local channel status can only report config because the gateway is unreachable
- `openclaw doctor` reports `Gateway not running` and a managed service such as a LaunchAgent installed but not loaded
- `openclaw update status` may still work from SSH because it does not require the live gateway

Observed recovery:
- From an outside SSH shell, export the real package-manager path first
- Run the requested stable update explicitly, for example `openclaw update --channel stable --yes --timeout 1800`
- Re-run `openclaw status --deep` and `openclaw channels status --deep`
- A healthy recovery shows the service loaded/running, gateway reachable, the selected channel persisted, and Discord `running, connected`

What to inspect:
- `command -v openclaw` and `openclaw --version`
- `openclaw update status`
- `openclaw doctor --non-interactive --no-workspace-suggestions`
- `openclaw status --deep`
- `openclaw channels status --deep`

Why it matters:
- a channel outage can be a service-manager state problem rather than a Discord plugin problem
- updating from outside the OpenClaw-managed agent path can recover an unloaded gateway and move the host back to the intended stable channel in one pass
- record pre-update warnings separately from the package update result, especially plaintext-secret warnings, stale session metadata, and old task-ledger warnings

Remote access guardrail:
- If another host cannot be reached over SSH with a short timeout, including from an available jump host, classify it as a transport/access blocker
- Do not file an OpenClaw issue for an unreachable host unless you have logs or command output proving OpenClaw failed on that host

## 34. In-gateway self-update can leave the package changed but the service unloaded

Symptom:
- the user asks OpenClaw itself to update the running OpenClaw host
- the agent conversation reports an update attempt or partial success
- later SSH shows one of:
  - CLI package reached the requested stable/tag, but the managed LaunchAgent/service is installed and not loaded
  - host remained on the previous beta/stable even though the agent said it attempted the update
  - channels are offline because the gateway is not actually running

What to inspect:
- `openclaw --version`
- `openclaw update status`
- `openclaw gateway status --deep`
- `openclaw status --deep`
- `openclaw channels status --deep`
- service-manager state from the real service label, not a guessed label
- recent gateway logs around the update/restart window

Recovery:
- switch to an outside shell/SSH session
- run the explicit target update from there, for example:
  ```
  openclaw update --channel stable --yes --timeout 1800
  ```
  or, when the exact tag matters:
  ```
  openclaw update --tag <version> --yes --timeout 1800
  ```
- if the package is already at the target version but the service is unloaded, try:
  ```
  openclaw gateway restart
  ```
- then verify service loaded/running, `/health`, channels, plugin doctor, and tasks audit

Why it matters:
- this is different from a failed npm package install; the dangerous part is that the process supervising the agent is also the process being stopped/replaced
- a successful package swap is not enough if the service manager never reloads the gateway
- do not trust the agent's final chat response as proof of update success; trust the host state inspected from outside the managed gateway

## 35. Stable package installed while update channel still points at beta

Symptom:
- operator explicitly updates to the latest stable
- `openclaw --version` and gateway version show the stable build
- `openclaw update status` still offers a newer beta build or reports beta channel metadata
- the host may have been on a beta channel in previous sessions

What to inspect:
- `openclaw --version`
- `openclaw update status`
- `openclaw status --deep`
- `openclaw.json` update/channel fields
- whether the update command used `--channel stable`, `--tag <stable-version>`, or only a bare `update`

Recovery:
- if the user's intent is stable, explicitly set or preserve the stable channel with the update command rather than assuming a stable tag rewrites every channel preference
- after the update, record both facts in the audit:
  - installed/runtime version
  - configured update channel and next offered version
- if a future run must avoid accidental beta adoption, correct the config/channel state before running another automatic update

Why it matters:
- "latest stable installed" and "host will keep following stable" are separate claims
- leaving beta channel metadata behind can make the next operator accidentally move the machine back onto beta
- this is especially easy to miss when the gateway itself is healthy and channels are connected

## 36. Deprecated plugin runtime API warning is usually an attribution issue, not a blocker

Symptom:
- `openclaw plugins doctor` or `openclaw doctor` is otherwise clean but prints:
  `plugin runtime config.loadConfig() is deprecated (runtime-config-load-write); use config.current().`
- the gateway is healthy and channels are connected
- the warning may or may not identify which plugin emitted it, depending on OpenClaw version

What to inspect:
- `openclaw plugins doctor`
- `openclaw plugins list --json`
- `openclaw plugins inspect <id>` for third-party plugins loaded from npm
- recent gateway logs for the same warning with more context

How to treat it:
- do not block the update on this warning if all health checks pass
- include it in the audit report as technical debt
- if the warning is unattributed, note that the diagnostic itself is incomplete; later versions may improve attribution by naming the plugin/source path

Why it matters:
- repeated nonblocking warnings can hide fresh failures in long update runs
- it is useful upstream feedback, but it should not be conflated with a broken install, disconnected channel, or failed model route

## 37. Supply-chain advisory audit should combine exact version matching with IoC checks

Symptom:
- after update/plugin churn, the user asks whether npm packages are compromised
- a public advisory lists hundreds of affected packages and specific indicators of compromise
- top-level `npm ls` looks clean but does not cover nested plugin installs or persistence artifacts

What to inspect:
- the advisory's exact package/version table
- global npm roots such as `/opt/homebrew/lib/node_modules` or `/usr/local/lib/node_modules`
- OpenClaw plugin roots such as `~/.openclaw/npm/node_modules`
- workspace-level `node_modules` if the host uses one
- package lifecycle scripts, especially suspicious `preinstall` hooks
- dependency specs pointing at attacker-controlled git refs
- persistence artifacts named by the advisory
- lockfiles and config files for strong text IoCs

Observed Shai-Hulud-style IoCs to include when relevant:
- `preinstall` running `bun run index.js` or `bun index.js`
- dependency specs involving `@antv/setup` or `antvis/G2` git refs
- `~/Library/LaunchAgents/com.user.kitty-monitor.plist`
- `gh-token-monitor`-style scripts
- AI-agent hooks or VS Code folder-open tasks that run unexpected setup files

How to report:
- separate "no exact installed compromised package/version found" from "no IoCs found"
- state the scan limits: a live-system audit cannot prove a compromised package was never installed and removed earlier
- do not paste secrets, host IPs, local usernames, or raw tokens into any maintainer-facing report

Why it matters:
- package compromise checks are easy to under-scope; nested plugin dependency trees are where OpenClaw updates actually changed npm state
- IoC checks catch a different class of compromise than exact installed-version matching
- the maintainer/user needs a clear confidence statement, not just a pile of package names

## 38. Official plugin updates can leave bare npm specs even when resolution metadata is pinned

Symptom:
- after a successful host update, `openclaw security audit --deep` still reports:
  `plugins.installs_unpinned_npm_specs Plugin index includes unpinned npm specs`
- the affected records are official npm plugins such as `brave`, `codex`, `discord`, or `whatsapp`
- `~/.openclaw/plugins/installs.json` shows exact `resolvedSpec`, `resolvedVersion`, integrity, and shasum values, but the stored `spec` field is still a bare package name such as `@openclaw/discord`

What to inspect:
- `openclaw security audit --deep`
- `~/.openclaw/plugins/installs.json`
- `openclaw plugins list --json` for each plugin's `version`, `origin`, and `source`
- package.json for each global plugin under `~/.openclaw/npm/node_modules`

Recovery:
- rewrite each affected npm plugin install record with an exact version and `--pin`, for example:
  ```
  openclaw plugins install @openclaw/brave-plugin@<host-version> --force --pin
  openclaw plugins install @openclaw/codex@<host-version> --force --pin
  openclaw plugins install @openclaw/discord@<host-version> --force --pin
  openclaw plugins install @openclaw/whatsapp@<host-version> --force --pin
  openclaw gateway restart
  ```
- re-run `openclaw security audit --deep` and verify the unpinned-spec warning clears
- record both `spec` and `resolvedSpec` in handoff notes when explaining what changed

Why it matters:
- `resolvedSpec` plus integrity is useful provenance, but OpenClaw's security audit intentionally treats a bare stored `spec` as future-update risk
- an operator can falsely believe "new OpenClaw pins dependencies" if they only check the resolved metadata and miss the still-unpinned `spec`
- the smallest safe fix is to rewrite the records through the CLI with `--pin`, not to hand-edit install metadata

## 39. Healthy Discord status but direct messages do not answer because cron owns the DM session lane

Symptom:
- `openclaw status --deep` and channel health checks report Discord configured/OK
- direct messages arrive or the channel appears connected, but the assistant does not answer
- cron or long-running scheduled jobs are active, recently active, or recently interrupted

What to inspect:
- `openclaw tasks list --status running --json`
- `openclaw status --deep` session table for direct-message and cron session keys
- `openclaw cron list --json` for persisted `sessionKey` fields
- recent gateway logs around gateway drain/restart and cron job start/finish events

Bad shape:
```
sessionTarget: "isolated"
sessionKey: "agent:<agent>:discord:direct:<redacted-channel-or-user-id>"
```

Healthy isolated cron shape:
```
sessionKey: "agent:<agent>:cron:<job-id>:run:<run-id>"
```

Recovery:
- clear the stale `sessionKey` only from cron jobs that are supposed to use isolated sessions
- restart the gateway if a long-running cron turn already occupied the live channel lane
- verify no running tasks remain and send/receive on the affected channel works again

Why it matters:
- channel health can be true while the conversational lane is effectively blocked
- stale cron state can survive upgrades and only become visible when a long job runs
- do not rotate Discord tokens or reinstall the channel plugin until session ownership has been checked
- this is worth upstream reporting because cron isolation should prevent channel-bound session keys from blocking live replies

Handoff guidance:
- sanitize channel ids and direct-message ids, but keep the `agent:<agent>:discord:direct:*` vs `agent:<agent>:cron:*` key shape
- include whether the affected cron jobs had `sessionTarget: isolated`
- include whether clearing the keys plus gateway restart restored replies

## 40. Cron `turn-accepted` timeouts after provider/model route changes

Symptom:
- multiple cron jobs fail with:
  `cron: job execution timed out (last phase: turn-accepted)`
- logs may also show provider/harness timeout language such as a Codex/OpenAI client being retired after a timed-out turn
- direct agent smoke can return `status: ok` if fallback succeeds, while cron jobs on the primary route still fail later

What to inspect:
- `openclaw cron list --json` model counts and per-job `payload.model`
- counts by `agentId`, not only total model counts, because mini cron routes may be intentionally different from full-size jobs
- `openclaw cron runs --id <job-id> --limit <n>` for first bad run, prior-good run, provider, model, runtime, and duration
- gateway logs around provider fallback decisions and `turn-accepted` timeouts
- default model routing for cron jobs whose payload has no explicit model override

Typical investigation sequence:
1. Capture the pre-change cron model map, including jobs with no explicit model.
2. Move one representative failing job to a known-good provider and verify completion through run history, not just enqueue.
3. If applying a temporary bulk provider workaround, record the exact original split so it can be restored later.
4. When rolling back the workaround, preserve mini routes separately instead of flattening every cron job to the same model.

Why it matters:
- a provider workaround can hide the OpenClaw regression while also erasing useful model topology
- inherited/default cron models are easy to miss because they do not appear in simple `payload.model` counts
- stale last-run errors can remain after the route is fixed; run history tells whether the failure is still active or only historical
- the first bad run timestamp is more useful to maintainers than the time the operator noticed alerts

Handoff guidance:
- keep exact model ids such as `openai/gpt-5.5`, `openai/gpt-5.4-mini`, `openai-codex/gpt-5.5`, and provider/runtime labels
- sanitize private job names if needed, but keep generic categories such as "high-frequency sync", "health monitor", or "long-running nightly job"
- include at least one prior-good and first-bad run entry with provider/model/duration/error, after removing session ids and private output text

## 41. Gateway runs under a dedicated OS user with a private CLI shim

Symptom:
- SSH succeeds as one user, but `openclaw --version` returns `command not found`
  or `permission denied`
- process list shows a healthy gateway owned by a different OS user
- the gateway command points at a package-manager runtime such as
  `/usr/local/node24/bin/node .../openclaw/dist/index.js gateway --port <port>`
- the `openclaw` wrapper or symlink is readable/executable only by the gateway
  service user

What to inspect:
- `ps aux | grep -i '[o]penclaw'`
- the gateway process owner, command path, and port
- `launchctl list`, `systemctl --user`, or the service definition for the
  managed service label
- common package-manager paths such as `/usr/local/node24/bin/openclaw`,
  `/opt/homebrew/bin/openclaw`, and `~/.local/bin/openclaw`
- whether `sudo -H -u <service-user> env PATH=<package-bin>:$PATH openclaw ...`
  reaches the same config and state dir as the gateway

Recovery:
- run diagnostics and fixes as the gateway service user, not as the SSH login
  user
- export the package-manager bin dir explicitly in every non-interactive command
- derive the config path from `openclaw daemon status` / `gateway status` before
  editing files

Why it matters:
- the login user's missing PATH is not proof OpenClaw is uninstalled
- running `doctor --fix` as the wrong user can inspect or create the wrong
  `~/.openclaw` tree
- service health, config, plugins, and sessions must be audited from the same
  user context as the managed gateway

## 42. ClawHub Codex extension lags host while plugin doctor is clean

Symptom:
- host OpenClaw version is newer than the loaded `codex` plugin version
- `openclaw plugins doctor` reports no plugin issues
- `openclaw plugins inspect codex` shows `Origin: global` and
  `Source: ~/.openclaw/extensions/codex/dist/index.js`
- recent logs may contain stalled Codex embedded runs or fallback/cooldown
  history, but a simple service health check is green

What to inspect:
- `openclaw --version`
- `openclaw plugins inspect codex`
- `openclaw plugins list --json`
- `openclaw plugins update codex --dry-run`
- recent gateway logs around `codex`, `fallback`, `stalled_agent_run`, and
  `strict-agentic execution contract`

Observed healthy recovery shape:
- `plugins update codex --dry-run` reports a newer official ClawHub package
  matching the host version
- after backing up `~/.openclaw/extensions/codex`, run
  `openclaw plugins update codex`
- restart the managed gateway
- `plugins inspect codex` reports the host-matching version
- a fresh direct smoke run returns the intended payload with provider/model and
  harness matching Codex, and no unexpected fallback

Why it matters:
- `plugins doctor` proves loadability, not cohort consistency
- Codex is both a plugin and a model/runtime bridge; a stale but loadable
  extension can be the real runtime mismatch
- updating every plugin with `--all` is riskier than updating the single stale
  runtime plugin when the rest of the host is healthy

## 43. Personal Codex CLI assets are not loaded by isolated Codex homes

Symptom:
- `openclaw doctor` warns that personal Codex CLI assets exist under locations
  such as `~/.codex` or `~/.agents/skills`
- native Codex-mode OpenClaw agents use isolated per-agent Codex homes
- operators expect the personal Codex config, hooks, or skills to affect the
  native Codex app-server child, but the runtime behaves as if they are absent

What to inspect:
- the exact doctor warning text
- `openclaw migrate codex --dry-run`
- the target OpenClaw workspace and per-agent Codex home paths
- direct smoke metadata for the actual provider/model/harness used by OpenClaw

Important detail:
- a dry-run can report that only `config.toml` exists and that it will be
  archived for manual review, not activated automatically
- OpenClaw may copy skills into the current workspace when migration is applied,
  but Codex config, plugins, and hooks remain manual-review items

Why it matters:
- this warning is usually not the immediate fix for a host/package mismatch
- applying the migration does not automatically make personal Codex config drive
  the native OpenClaw Codex harness
- separate "assets not promoted into OpenClaw" from "primary model route failed"
  and prove the runtime with a direct smoke test before changing model config
