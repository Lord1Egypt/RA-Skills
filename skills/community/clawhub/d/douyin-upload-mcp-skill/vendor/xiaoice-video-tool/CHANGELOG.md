# Changelog

## [Unreleased]

### Added

- Phase 2 service extraction record for standalone `video-task-service` runtime.
- `README.md` runbook update for `npm run service` with key service environment variables.
- Extracted `video-task-service` runtime implementation into `src/service/server.js` with CLI entry `src/service/cli.js`.
- Added Node integration tests for service endpoints in `tests/video-task-service.integration.test.js`.
- Added service run scripts (`npm run service`, `npm start`) and expanded `.env.example` for Phase 2 runtime configuration.
- Implemented stdio MCP server runtime and tool handler in `src/mcp/server.js`, `src/mcp/tool.js`, and `src/mcp/cli.js`.
- Added MCP test coverage in `tests/mcp-tool.test.js` and `tests/mcp-server.protocol.test.js`.
- Added MCP run script `npm run mcp`.
- Entered Phase 4 execution tracks: shared service client, OpenClaw native thin plugin, and public field hard cut to `vhBizId`.

### Changed

- Unified public docs/examples on canonical field `vhBizId`; removed external alias usage.
- Renamed runtime config example key to canonical `VIDEO_PROVIDER_VH_BIZ_ID`.

### Clarified

- MCP server work is not marked complete in this round; stdio integration remains a later phase.

## [0.1.0] - 2026-03-13

### Added

- Bootstrapped `src/service`, `src/mcp`, `src/shared` and root entry `src/index.js`.
- Added baseline Node built-in test runner tests under `tests/`.
- Added project runtime metadata and scripts in `package.json`.
