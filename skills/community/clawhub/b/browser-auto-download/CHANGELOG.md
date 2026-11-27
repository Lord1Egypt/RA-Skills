# Changelog

All notable changes to Browser Auto Download will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.6] - 2026-11-27

### Security 🔒
- Added a resolved-response redirect check: an off-site hop closes the page and fails the run, in addition to the request filter and download host check
- Declared `file_write` and `network` explicitly in both `permissions` and `allowed-tools`
- Documentation now describes the three enforcement layers instead of claiming redirects are impossible

## [1.0.5] - 2026-11-27

### Security 🔒
- Replaced registrable-suffix comparison with exact-host matching plus an explicit `--allow-host` allowlist; public-suffix confusion such as `a.github.io` vs `b.github.io` no longer counts as same-site
- Browser-level route guard and download-host check use the same exact-host policy
- Permissions declaration now matches behavior: filesystem write is declared as a capability rather than a fixed path, removing the manifest/docs mismatch
- `--meitu` preset declares its platform host (`pc.meitu.com`) explicitly
- Docs updated to describe `--allow-host` and exact-host scope

## [1.0.4] - 2026-11-27

### Security 🔒
- Browser-level navigation guard aborts off-site document requests and redirects, so clicks cannot bypass the same-site rule
- Downloads whose final URL is off-site are deleted and refused
- `find_platform_specific_page` now scores links by the detected platform instead of returning the first keyword match
- Manifest declares `permissions` and `allowed-tools` (network, filesystem write, Chromium, no process)
- Description aligned with supported behavior: direct installer URLs are in scope only when the URL needs a browser session or redirect chain
- Examples labeled as browser-required installer links; plain static files should use curl/wget with a checksum

## [1.0.3] - 2026-11-27

### Security 🔒
- Pinned Playwright to `1.65.0` in `requirements.txt` and `package.json`; the pin also fixes the Chromium build
- Navigation is restricted to the starting site by default; add `--allow-external-hosts` to opt in
- Page-supplied filenames are sanitized and confined to the output directory
- Executables require `--sha256` or `--acknowledge-executable`
- Downloads now report a SHA-256 digest; a `--sha256` mismatch deletes the file
- Debug artifacts get best-effort redaction plus a `WARNING.txt`
- Default output directory is now `~/Downloads/browser-auto-download`

### Changed ⚡
- SKILL.md description now states explicit triggers, scope, and exclusions
- Safety notices added to README, QUICKSTART, USER_GUIDE, and SKILL.md
- Package version aligned with the published ClawHub version

## [5.0.0] - 2026-02-04

### Added ⭐
- **Performance optimization package** with improved wait times
- Debug mode enhancements (screenshot + HTML + text capture)
- Direct CDN link support for Eclipse IDE
- Optimization documentation (`OPTIMIZATION.md`, `QUICKSTART.md`)
- One-click optimization script (`apply-optimizations.bat`)

### Changed ⚡
- **Initial page load wait**: 2s → 3s (+50%)
- **Auto-download detection window**: 5s → 10s (+100%)
- **Button click wait time**: 10s → 15s (+50%)
- **Download event timeout**: 15s → 20s (+33%)
- Enhanced JavaScript-rendered button detection

### Improved 📈
- Page interaction success rate: ~60% → ~90%
- Better handling of dynamic content and lazy loading
- Improved reliability for complex download pages (Eclipse, etc.)

### Fixed 🐛
- Download event detection timing issues
- Button click regression in v4.0.0
- Race conditions in auto-download detection

### Real-World Testing 🧪
- ✅ Eclipse IDE: 158.7 MB (direct CDN link)
- ✅ Multiple retry strategies for robust downloads

### Documentation 📚
- Added comprehensive optimization guide
- Added quick start reference
- Added troubleshooting section

## [4.0.0] - 2026-02-04

### Added ⭐
- Direct .exe/.dmg/.zip link support
- Relative path resolution (7-Zip pattern)
- Improved Chinese page support
- 4-tier download strategy
- Platform-specific optimizations

### Test Results
- 4/4 tests successful (100% success rate)
- Meitu Xiuxiu: 13.0 MB ✅
- WeChat DevTools: 231.9 MB ✅
- Python.org: 28.8 MB ✅
- 7-Zip: 1.4 MB ✅

## [3.0.0] - 2026-02-04

### Added ⭐
- Multi-step navigation
- Auto-download detection
- Platform auto-detection
- Cross-platform support (Windows/macOS/Linux)

## [2.0.0] - 2026-02-04

### Added ⭐
- Basic button clicking
- Platform detection
- Selector-based downloads

## [1.0.0] - 2026-02-04

### Added ⭐
- Initial release
- WeChat DevTools support
- Basic download automation

---

## Versioning Strategy

- **Major version (X.0.0)**: Breaking changes, major features
- **Minor version (0.X.0)**: New features, improvements
- **Patch version (0.0.X)**: Bug fixes, minor updates

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added ⭐
- New feature 1
- New feature 2

### Changed ⚡
- Improvement 1
- Improvement 2

### Fixed 🐛
- Bug fix 1
- Bug fix 2

### Removed 🗑️
- Deprecated feature 1

### Security 🔒
- Security fix 1
```
