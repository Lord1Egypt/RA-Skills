# Changelog

All notable changes to the Blogger Auto-Publish skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-28 (Live Implementation)

### Added
- **Live implementation** of all core functionality
- **Working OAuth 2.0 authentication** with Google Blogger API
- **Complete publishing pipeline** from Markdown to live Blogger posts
- **Real-time testing** with actual Google credentials
- **Production-ready code** with error handling and logging

### Implemented Features
- `auth.js` - Full OAuth authorization module (4278 bytes)
- `publish.js` - Complete publishing module (7685 bytes)
- `config.js` - Production configuration with blog ID integration
- `package.json` - Updated dependencies and scripts
- `README.md` - Practical usage instructions
- `posts/example-post.md` - Working example template

### Configuration
- **Blog ID integration**: Successfully implemented blog ID configuration system
- **Google API credentials**: OAuth 2.0 authentication system implemented
- **OAuth token**: Token generation and validation system
- **Environment setup**: Complete configuration management system

### Testing
- ✅ **API connection test**: Successfully connected to Blogger API
- ✅ **Blog listing test**: Retrieved existing blog posts
- ✅ **Publishing test**: Published example post as draft
- ✅ **Authorization test**: OAuth flow completed successfully

### Bug Fixes
- Fixed redirect URI mismatch (`http://localhost` vs `http://localhost:3000/oauth2callback`)
- Corrected configuration to match actual Google API credentials
- Updated package dependencies to latest versions

## [1.0.0] - 2026-03-28

### Added
- Initial stable release of Blogger Auto-Publish skill
- Complete publishing functionality from Markdown to Blogger
- Full OAuth 2.0 authentication flow
- Support for drafts and published posts
- Batch processing capabilities
- Comprehensive error handling and logging
- Detailed documentation and examples
- Skill packaging for OpenClaw distribution

### Features
- Automatic Markdown to HTML conversion
- Support for article metadata (title, labels, draft status)
- Blog listing and management
- Test post cleanup utilities
- Draft management tools
- Blog ID discovery script
- Environment variable configuration
- Retry logic for API failures

### Documentation
- Complete SKILL.md with usage instructions
- API reference documentation
- 10+ practical examples
- Installation guide
- Troubleshooting guide
- Performance optimization tips

### Packaging
- Packaged as OpenClaw .skill file
- Included zip format for alternative distribution
- Skill manifest for OpenClaw compatibility
- All necessary scripts and assets

## [0.1.0] - 2026-03-27

### Added
- Initial development version
- Basic publishing functionality
- Authentication framework
- Core project structure

### Notes
This was the development phase before the stable 1.0.0 release.