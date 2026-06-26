# Changelog

All notable changes to ClawMobile Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-31

### Added

#### Core Features
- ✅ Complete AutoX.js HTTP API integration
- ✅ Workflow management system (CRUD operations)
- ✅ Task recording functionality with UI capture
- ✅ AI intervention for intelligent error recovery
- ✅ Three-tier membership system (Free/VIP/SVIP)
- ✅ Redeem code activation system
- ✅ HTTP RESTful API client and server
- ✅ Batch workflow execution support
- ✅ Connection management (local and remote)

#### Membership System
- ✅ Free tier: 3 daily runs, basic features
- ✅ VIP tier: Unlimited runs, scheduling, AI intervention
- ✅ SVIP tier: All VIP features plus parameter auto-decision
- ✅ Redeem code format: `C-VENDORCODE-YY-DDM-CHECKSUM`
- ✅ Permission-based feature access control
- ✅ Membership history tracking

#### Workflow Features
- ✅ Create, read, update, delete workflows
- ✅ Parameterized workflow support
- ✅ Scheduled task execution (VIP/SVIP)
- ✅ Workflow validation and analytics
- ✅ Import/export workflows (VIP/SVIP)
- ✅ Natural language workflow generation

#### Recording Features
- ✅ UI operation recording
- ✅ AutoX.js code generation
- ✅ Screenshot capture
- ✅ UI tree capture
- ✅ Recording pause/resume/stop controls
- ✅ Workflow creation from recordings

#### AI Intervention
- ✅ Unknown page intelligent recognition
- ✅ Automatic decision and recovery
- ✅ Context-aware execution
- ✅ Learning-based decision optimization
- ✅ Decision statistics and analytics

#### API Endpoints
- ✅ `GET /api/v1/health` - Health check
- ✅ `GET /status` - Server status
- ✅ `POST /execute` - Execute workflow
- ✅ `POST /check_status` - Check task status
- ✅ `POST /stop` - Stop task
- ✅ `GET /workflows` - List workflows
- ✅ `GET /workflows/{id}` - Get workflow details
- ✅ `POST /workflows` - Create workflow
- ✅ `PUT /workflows/{id}` - Update workflow
- ✅ `DELETE /workflows/{id}` - Delete workflow
- ✅ `POST /recording/start` - Start recording
- ✅ `POST /recording/pause` - Pause recording
- ✅ `POST /recording/resume` - Resume recording
- ✅ `POST /recording/stop` - Stop recording
- ✅ `POST /intervention` - Request AI intervention
- ✅ `GET /api/v1/membership/status` - Get membership status
- ✅ `POST /api/v1/membership/validate` - Validate redeem code
- ✅ `POST /api/v1/membership/check-permission` - Check permission
- ✅ `GET /api/v1/membership/history` - Get membership history
- ✅ `POST /api/v1/connection/test` - Test connection
- ✅ `GET /api/v1/connection/status` - Get connection status

#### Documentation
- ✅ Complete SKILL.md with usage guide
- ✅ Comprehensive README.md
- ✅ API documentation reference
- ✅ Data models documentation
- ✅ Membership system guide
- ✅ Redeem code format specification
- ✅ Integration test guide
- ✅ Troubleshooting guide

#### Scripts and Tools
- ✅ Setup script for easy installation
- ✅ Validation script for skill integrity
- ✅ Test script for functionality verification
- ✅ Mock API server for testing
- ✅ API integration test suite

#### Configuration
- ✅ YAML-based configuration system
- ✅ Environment variable support
- ✅ Default configuration with overrides
- ✅ Connection settings management
- ✅ Membership configuration
- ✅ Recording configuration
- ✅ Logging configuration

### Dependencies

#### Required
- Python 3.7+
- AutoX.js 6.5.5.10+
- ADB (Android Debug Bridge)

#### Python Packages
- requests>=2.31.0
- pyyaml>=6.0

### Security
- ✅ Bearer token authentication
- ✅ Environment variable for sensitive data
- ✅ No hardcoded secrets in code
- ✅ Permission-based access control

### Testing
- ✅ Unit tests for core components
- ✅ Integration tests for API endpoints
- ✅ Mock server for isolated testing
- ✅ Test coverage for membership system
- ✅ Test coverage for recording functionality

### Compatibility
- ✅ Android 7.0+ (API 24+)
- ✅ AutoX.js 6.5.5.10+
- ✅ Python 3.7+
- ✅ Windows, Linux, macOS

### Performance
- ✅ Connection pooling for HTTP requests
- ✅ Configurable timeout and retry logic
- ✅ Efficient data serialization
- ✅ Minimal memory footprint

---

## [Unreleased]

### Planned
- Webhook notifications
- Cloud workflow storage
- Multi-device management
- Advanced analytics dashboard
- Visual workflow editor
- Community workflow marketplace

---

## Version Format

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

---

*Changelog v1.0.0 | Last Updated: 2026-03-31*
