# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-09

### Added
- Initial release of Boat Daily Check skill
- Victron VRM API integration for real-time power system monitoring
- Beautiful responsive HTML email reports
- Support for multiple installations (boats, RVs, off-grid systems)
- Battery monitoring: SOC%, voltage, current, temperature
- Solar generation tracking: power, daily yield, max charge
- Inverter/AC power status monitoring
- Active alarm detection and reporting
- JSON and CSV data exports
- Complete documentation with examples
- API reference guides for customization

### Features
- Automated daily email reports via OpenClaw cron
- Professional HTML design with visual battery indicators
- Multi-boat support in single email
- Environment variable configuration for security
- Graceful error handling
- Rate-limit aware API calls

## [Unreleased]

### Planned
- Historical data visualization
- Threshold-based alerts (low SOC, overvoltage, etc.)
- Integration with Slack/Discord notifications
- Web dashboard for real-time monitoring
- Support for additional Victron widgets
- Multi-user support
