# Changelog

All notable changes to the `clawbox-media-server` skill are documented here.

## [1.0.1] - 2026-03-06

### Fixed
- Corrected systemd service `WorkingDirectory` paths to use `clawbox-media-server` (was `lan-media-server`)
- Made process termination more precise to avoid killing unrelated Node/Python processes
- Added `BIND_ADDR` environment variable to both servers to allow binding to specific LAN interface (security enhancement)

### Improved
- Security documentation expanded with firewall guidance and manual testing recommendations
- Installer now saves PIDs for cleaner restarts
- Systemd service files include `BIND_ADDR` by default

## [1.0.0] - 2026-03-06

### Added
- Initial release
- Media server (port 18801) with directory listing
- Upload server (port 18802) with drag-and-drop web UI
- Same-origin design to avoid CORS/Safari issues
- Systemd service files for auto-start
- One-click installer (`install-all.sh`)
- Bidirectional LAN file sharing workflow
- Configurable bind address (`BIND_ADDR`) for tighter security
- More precise process termination (PID-based, avoids killing unrelated processes)

### Security & Safety
- Added `BIND_ADDR` environment variable to restrict binding to specific LAN interface
- Enhanced documentation with security warnings and best practices
- Updated systemd services to include `BIND_ADDR`
- Improved installer to use exact PID matching for old process cleanup
- Clear guidance on manual testing before enabling systemd auto-start
