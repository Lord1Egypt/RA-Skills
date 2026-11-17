# Changelog

All notable changes to ClawAPI Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-03-03

### Security
- **CRITICAL**: Removed all API keys from Git history
- Added  rules to prevent future key leaks
- Created example configuration files ( suffix)

### Added
- Config validation command (`validate`)
- Auto-fix command (`fix`) for common configuration issues
- Detection for invalid model ID formats
- Detection for invalid root-level keys
- Bilingual SKILL.md (English + 中文)

### Changed
- Updated SKILL.md to follow official Claude Skills format
- Improved documentation structure

### Fixed
- Fixed `Unknown model: anthropic/volcengine:doubao-seed-2.0-code` error
- Fixed invalid root-level `model` key causing config validation failure

## [1.1.0] - 2026-03-03

### Added
- Central server API key托管管理
- OpenRouter multi-key support with round-robin rotation
- Managed keys configuration file
- Quick management script (`claw_api_manager_central.py`)

### Changed
- Improved provider management workflow
- Enhanced backup strategy (keeps last 10 backups)

## [1.0.0] - 2026-03-02

### Added
- Initial release
- Multi-provider API key management
- Real-time cost monitoring
- Smart routing with OpenRouter integration
- Budget alerts (Telegram, Discord, Slack, Feishu, QQ, DingTalk)
- Key health monitoring
- Automated failover
- Circuit breaker pattern
- Daily cost reports

### Documentation
- Comprehensive README.md
- SKILL.md with usage examples
- Configuration examples
- Troubleshooting guide

---

## Upgrade Guide

### From 1.1.0 to 1.1.1

**⚠️ SECURITY UPDATE - Immediate action required**

1. Pull latest changes:
   ```bash
   cd ~/.openclaw/workspace/skills/clawapi-manager
   git pull origin master
   ```

2. Recreate your config files (old ones were removed for security):
   ```bash
   cp config/managed_keys_central.json.example config/managed_keys_central.json
   cp config/openrouter_keys.json.example config/openrouter_keys.json
   # Edit with your keys
   ```

3. Validate your configuration:
   ```bash
   python3 claw_api_manager_central.py validate
   ```

4. Auto-fix any issues:
   ```bash
   python3 claw_api_manager_central.py fix
   ```

5. Restart gateway:
   ```bash
   openclaw gateway restart
   ```

### From 1.0.0 to 1.1.0

No breaking changes. Simply pull latest changes and restart gateway.

---

## Roadmap

### v1.2.0 (Planned)
- [ ] Web UI for configuration management
- [ ] Advanced cost prediction
- [ ] Custom routing rules
- [ ] Multi-node synchronization
- [ ] Enhanced analytics dashboard

### v1.3.0 (Planned)
- [ ] API key expiration warnings
- [ ] Automatic key renewal (where supported)
- [ ] Cost optimization recommendations
- [ ] Integration with more providers

---

## Support

- **Issues**: [GitHub Issues](https://github.com/2233admin/clawapi-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/2233admin/clawapi-manager/discussions)
- **ClawHub**: [clawhub.com/skills/clawapi-manager](https://clawhub.com/skills/clawapi-manager)
