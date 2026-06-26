# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-04-09

### Added
- Explicit `Route & Brief -> Execute -> Done Gate` execution model in `SKILL.md` and `README.md`
- Validation Gates in `references/core-rules.md` with structural-first completion checks
- Task Ticket output in `references/workflow-selection.md` to carry execution mode, risks, and validation checks
- Execution Brief template and completion-criteria blocks in `references/prompting-patterns.md`

### Changed
- Hardened `screen-review-loop.md` so completion requires a real done gate instead of a soft final screenshot step
- Turned the state-variant decision in `native-screen-generation.md` into a hard fork instead of advisory guidance
- Reworked prompting guidance to separate always-in instructions, conditional inserts, and done criteria
- Clarified README execution principles around structural validation before visual confirmation

## [0.2.0] - 2026-04-09

### Added
- Structured workflow documentation for the current skill architecture, including workflow selection, prompting patterns, copy-and-edit guidance, and state-variant handling
- Image Delivery documentation for local screenshot output via `--out` and chat delivery via `MEDIA:<path>`
- Install note in `SKILL.md` and clearer routing guidance between abridged skill routing and full workflow selection docs

### Changed
- Rewrote `README.md` to reflect the current workflow-driven product surface instead of presenting the skill as a thin MCP wrapper
- Surfaced the state-variant decision earlier in the native screen generation flow
- Added dedicated Copy + Edit prompting guidance
- Strengthened routing and hard-rule language around component-instance-first behavior

## [0.1.2] - 2026-04-03

### Changed
- Republished `figma-agent` to ensure the ClawHub listing uses the display name **Figma Agent**

## [0.1.1] - 2026-04-03

### Fixed
- Removed legacy OAuth experiment scripts (`auth.mjs`, `sdk-auth-test.mjs`) from repo
- Corrected Figma Remote MCP link in README (→ official help docs)
- Made all ACP/write-path references provider-agnostic (Claude Code, Codex, or any supported ACP agent)
- Removed `.clawhubignore` from public git tracking (added to `.gitignore`)
- Added `displayName: "Figma Agent"` to `package.json` for correct ClawHub display name

## [0.1.0] - 2026-04-03

### Added
- **Hybrid architecture** — direct read/inspect via Figma Remote MCP + write/edit/create via Claude Code ACP sessions
- **Zero-dependency MCP client** (`scripts/figma-mcp.mjs`) — JSON-RPC 2.0 over HTTP POST, handles SSE and direct JSON responses, auto-Bearer-prefix, timeout support
- **Multi-client token bootstrap** (`scripts/bootstrap-token.mjs`) — scans Claude Code, Codex, and Windsurf credential stores, refreshes expired tokens, writes Bearer header to OpenClaw config
- **Full 17-tool coverage** — all official Figma Remote MCP tools documented with read/write split
- **Known limitations** — official Figma limitations (20 KB limit, no image import, no custom fonts, sandbox restrictions) documented in SKILL.md with sources
- **`references/figma-api.md`** — concise API reference for all MCP tools
