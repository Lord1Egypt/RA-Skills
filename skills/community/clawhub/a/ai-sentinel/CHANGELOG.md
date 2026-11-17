# Changelog

## 0.2.2 (2026-08-28)

Security-audit remediation (docs-only; still installs plugin 0.2.1).

- Declare `~/.openclaw/openclaw.json` in `writes-files` — the Step 5 plugin-config merge writes this file (still gated behind explicit user confirmation). Resolves the scope-creep finding where an instructed write exceeded declared file permissions.
- Rework the Test 2 verification step to describe the prompt-injection probe rather than embedding the literal directive in the manifest, so it is not mistaken for an instruction to the reviewing agent. Restores the "benign-to-scan" convention from 1.0.1.
- Update skill card and README file-write declarations to match.

## 0.2.1 (2026-08-27)

Versioning tracks the `ai-sentinel` npm plugin release the skill installs (npm already at 0.2.1).

- Document obfuscation-resistant preprocessing added to the plugin: base64 and HTML-entity decoding plus zero-width/bidirectional Unicode stripping before pattern matching (plugin 0.1.13–0.1.15 hardening; scanned content is only inspected, never executed)
- Disclose channel type (e.g., slack, webchat) as part of the telemetry payload description (plugin 0.1.16–0.1.17)
- Document optional `scanExcludePatterns` config for skipping internal agent commands (plugin 0.2.0)
- Update version references in install/verification examples from 0.1.10 to 0.2.1 (includes plugin fix for stale config after SIGUSR1 restart, 0.1.18)

## 1.2.0 (2026-02-10)

- Set `disableModelInvocation: true` to prevent autonomous agent invocation (skill now requires explicit user action)
- Add registry metadata checklist to README so publish form fields match SKILL.md declarations

## 1.1.0 (2026-02-10)

- Move declarations into structured metadata fields (Requires-Config, Requires-Env, Installs-Packages, Writes-Files, External-Services) so registry parsers read them
- Add Data Transmission Notice section explaining what Pro tier sends externally
- Add File Write Policy section confirming no files are written without user approval
- Add explicit consent gate when user selects Pro tier (data transmission to api.zetro.ai)
- Add explicit AskUserQuestion confirmation before every file write (openclaw.config.ts, .env, data/, .gitignore)
- Add agent instruction: never write files autonomously

## 1.0.1 (2026-02-10)

- Add declarations table (config paths, env vars, filesystem writes, npm packages)
- Add homepage, source, and package registry links to metadata
- Replace literal injection strings in test examples with benign-to-scan payloads to avoid false positive flags from security scanners

## 1.0.0 (2026-02-10)

- Initial release
- Interactive setup wizard for OpenClaw integration
- Supports Community (free, local-only) and Pro (remote API + dashboard) tiers
- Configures message, tool output, document, and skill validation middleware
- Per-channel detection threshold configuration (Pro)
- Optional SQLite audit logging setup
- Optional custom blocklist rule configuration
- Built-in test verification step with CLI commands
