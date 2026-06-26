# Changelog

All notable changes to the Claw Code Suite skill will be documented in this file.

## [1.0.1] - 2026-04-06

### Security & Transparency
- **REMOVED**: Entire Rust workspace (api/, server/, runtime/, tools/, cli/, etc.)
- **REMOVED**: All network dependencies (reqwest, axum, HTTP clients)
- **REMOVED**: All AI provider integrations (OpenAI, Anthropic, xAI API clients)
- **REMOVED**: All OAuth and credential handling code
- **REMOVED**: All server/binding code (MCP server, SSE, web servers)
- **UPDATED**: SKILL.md to accurately reflect Python-only, offline nature
- **ADDED**: Security verification commands and documentation

### Functionality
- **PRESERVED**: All 184 tools from original Claw Code port
- **PRESERVED**: All 207 commands from original Claw Code port
- **PRESERVED**: Full Python harness functionality
- **PRESERVED**: All security analysis, code quality, and dev workflow tools

### Compliance
- ✅ Now passes ClawHub security scanner without "Suspicious" flags
- ✅ No network access capabilities
- ✅ No credential/API key requirements
- ✅ No background daemons or servers
- ✅ Pure offline operation
- ✅ Full source code transparency

## [1.0.0] - 2026-04-01

### Initial Release
- Initial integration of Claw Code Python port
- Included full Rust workspace (removed in v1.0.1)
- 184 tools and 207 commands available
- Basic harness wrapper and enhanced harness
- Test suite and verification scripts