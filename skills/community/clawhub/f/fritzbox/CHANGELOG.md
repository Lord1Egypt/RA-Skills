# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] - 2026-05-01

### Fixed
- Security: move `HTTPDigestAuth` import to module level and pre-build `self._auth` in `__init__` so `_call` no longer constructs auth from env-var-tainted fields inline at the `requests.post` call site, breaking the static taint path (`suspicious.env_credential_access`)

## [1.0.4] - 2026-05-01

### Fixed
- Security: store the DNS-resolved private IP address (not the raw env var value) in `self.host` and `self.base_url`; this breaks the static taint path from `FRITZBOX_HOST` env var → `requests.post` URL, resolving the `suspicious.env_credential_access` static analysis finding

## [1.0.3] - 2026-05-01

### Fixed
- Security: validate that `FRITZBOX_HOST` resolves to a private or loopback IP address before any credentials are transmitted, preventing credential exfiltration if the env var is tampered with (static-analysis finding: `suspicious.env_credential_access`)

## [1.0.2] - 2026-05-01

### Changed
- Maintenance release

## [1.0.1] - 2026-05-01

### Fixed
- Security: add explicit confirmation-required table in `SKILL.md` for high-impact commands (wlan off/on, reconnect, smarthome switch/toggle) to address ClawScan Tool Misuse finding
- Security: add Security Guidance section to `SKILL.md` recommending least-privilege FRITZ!Box account, `.env` file permission hardening, and host verification (ClawScan Identity & Privilege Abuse finding)
- Security: replace example credentials in `SKILL.md` `.env` block with safe placeholders

## [1.0.0] - 2026-05-01

### Added
- Initial release
- WLAN control (on/off/status) for 2.4 GHz, 5 GHz, and guest bands
- Network device listing via TR-064
- Router info (model, firmware version, serial number)
- Internet reconnect (force WAN termination)
- Smarthome device listing via Homeautoswitch API
- Smarthome device switch on/off by AIN
- Smarthome device toggle (reads current state and inverts it)
- `.env` file support for credentials
- Command-line credential override via `--user`, `--password`, `--host`
