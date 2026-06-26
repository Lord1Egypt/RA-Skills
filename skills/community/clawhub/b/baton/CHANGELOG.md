# Changelog

## 1.8.2 - Security audit remediation

- Removed the unsafe `Function(...)` fallback parser from `scripts/lib/baton-common.mjs`.
- Added a safe JSON/JSONC/limited-JSON5 parser for local OpenClaw config files: comments, trailing commas, single-quoted strings, and bare object keys are handled without evaluating config text.
- Updated parser errors to state that config text is never executed.
- Updated validator/version metadata for the security-audit-fixed release.

## 1.8.0

- Added compact Planner-Orchestrator protocol.
- Preserved always-spawn policy.
- Reduced runtime prompt footprint.
