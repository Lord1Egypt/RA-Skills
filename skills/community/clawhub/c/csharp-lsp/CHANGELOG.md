# Changelog

## [1.2.0] - 2026-03-05

### Changed
- SKILL.md rewritten in English (was Korean)
- Added ClawHub badge to README

### Added
- GitHub Actions workflow for automated ClawHub publish on tag push
- ClawHub install option in README

## [1.1.0] - 2026-03-05

### Changed
- Removed OmniSharp support — now csharp-ls only
- Self-contained: no longer depends on base `lsp` skill
- Rewrote SKILL.md for csharp-ls single-server focus

### Added
- `setup.sh` — idempotent one-time setup script with `--verify` option
- Docker-based clean environment testing
- `LSP_CSHARP_SERVER` env var removed (csharp-ls hardcoded)

### Fixed
- Server-to-client request handling (`client/registerCapability`, `workspace/configuration`, `window/workDoneProgress/create`)
- Solution loading wait logic (diagnostics-based, up to 30s)
- PATH detection for `~/.dotnet/tools`

## [1.0.0] - 2026-03-05

### Added
- Initial release
- csharp-ls integration via lsp-query daemon
- Hover, definition, references, symbols, diagnostics, workspace-symbols
- Daemon auto-fork on first call, 5-min idle shutdown
- Support for .sln and .csproj project detection
