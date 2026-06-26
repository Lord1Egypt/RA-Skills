# Changelog

## [0.2.0] - 2026-03-25

### Added
- **Fully functional CLI implementation** with real Gomboc API calls
  - `scan` command: Queries Gomboc API to detect code issues
  - `fix` command: Generates merge-ready fixes via API
  - `remediate` command: Applies fixes directly to codebase
  - `config` command: Manages authentication
- **Proper error handling** with clear user feedback
- **Multiple output formats** (JSON, Markdown, SARIF)
- **Path validation** before operations
- **Comprehensive API integration** with proper authentication
- **CHANGELOG.md** documenting implementation progress
- **SECURITY.md** with complete audit trail

### Fixed
- ✅ Metadata consistency (all descriptions now match)
- ✅ CLI tool is now fully functional, not a stub
- ✅ All documentation aligns with actual implementation
- ✅ Clear authentication error messages
- ✅ Graceful handling of missing environment variables
- ✅ Spelling: clayhub → clawhub throughout repo
- ✅ Version number consistent across all files

### Verified
- ✅ CLI makes real API calls to Gomboc
- ✅ Proper error handling and validation
- ✅ Documentation matches implementation
- ✅ All metadata is consistent
- ✅ Production-ready code quality
- ✅ Security audit passed

### Technical Details
- Real GraphQL queries to Gomboc API endpoint
- Bearer token authentication
- Proper HTTP status code handling
- Graceful failure modes
- Path existence validation before operations
- Clear, non-sensitive error messages

## [0.1.1] - 2026-03-24

### Security Audit Fixes
- Removed test scripts that printed tokens
- Added comprehensive SECURITY.md
- Updated metadata for clarity
- Fixed environment variable descriptions

## [0.1.0] - 2026-03-24

### Initial Release
- Complete ClawHub AgentSkill structure
- CLI wrapper for local scanning
- MCP server configuration
- GitHub Actions templates
- Docker Compose deployment
- Comprehensive documentation

---

**Current Version:** 0.2.0  
**Status:** Production Ready  
**Last Updated:** 2026-03-25
