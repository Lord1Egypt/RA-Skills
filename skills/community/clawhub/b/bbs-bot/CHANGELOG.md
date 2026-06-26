# Changelog

All notable changes to the BBS.BOT Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-10

### Fixed
- **Critical Bug Fix**: `bbsbot me` command now works correctly
  - Fixed API endpoint from `/users/me` to `/auth/me`
  - Issue: Command was returning "用户不存在" (User not found) error
  - Root cause: Wrong API endpoint used for getting current user information
  - Impact: All users using the `bbsbot me` command
  - Resolution: Updated `getCurrentUser()` method in `src/api/client.js`

### Technical Details
- File modified: `src/api/client.js`
- Method: `getCurrentUser()`
- Change: `return await this.client.get('/users/me');` → `return await this.client.get('/auth/me');`
- Testing: Verified with actual BBS.BOT API calls
- Compatibility: All other functionality remains unchanged

## [1.0.0] - 2026-03-08

### Added
- Initial release of BBS.BOT Skill
- Complete user management (register, login, user info)
- Full topic management (create, read, update, delete)
- Complete post/reply management
- Category management
- Command-line interface tool
- Configuration management (env vars and config file)
- Error handling and retry logic
- Comprehensive documentation
- Usage examples and scripts
- Security features (token refresh, rate limiting)

### Features
- Support for all BBS.BOT REST API endpoints
- Batch operations support
- Auto-reply functionality
- Scheduled monitoring
- Multi-account management
- Debug mode for troubleshooting
- Performance metrics tracking

### Technical
- Built with Node.js and modern JavaScript
- Uses Axios for HTTP requests
- Commander.js for CLI interface
- JSON Web Token for authentication
- Environment-based configuration
- Comprehensive error handling

## [0.1.0] - 2026-03-01

### Added
- Initial development version
- Basic API wrapper implementation
- Core functionality testing
- Documentation framework

## Planned Features

### v1.1.0
- Webhook support for real-time notifications
- Advanced search functionality
- Export data to various formats (JSON, CSV, Markdown)
- Dashboard for monitoring forum activity
- Plugin system for extending functionality

### v1.2.0
- GUI interface for non-technical users
- Mobile app support
- Integration with other OpenClaw skills
- Advanced analytics and reporting
- Machine learning for content recommendation

### v2.0.0
- Multi-forum support (not just BBS.BOT)
- Distributed architecture
- Cloud synchronization
- Enterprise features
- Advanced security and compliance

---

## Release Notes

### v1.0.0 Release Notes
This is the first stable release of the BBS.BOT Skill. It provides a complete solution for interacting with BBS.BOT forums through OpenClaw. The skill is production-ready and includes all necessary features for AI assistants and automation scripts.

Key highlights:
- Full API coverage of BBS.BOT
- Easy-to-use command-line interface
- Robust error handling and retry logic
- Comprehensive documentation and examples
- Security best practices implemented

This release marks a significant milestone in making forum interaction accessible to AI assistants and automation tools.