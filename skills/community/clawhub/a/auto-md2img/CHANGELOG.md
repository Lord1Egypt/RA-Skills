# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2026-03-15

### Added
- **Height-based pagination mode** - Split content by pixel height threshold instead of line count, independent of line count statistics
- **JPEG quality adjustment** - Add `quality` parameter (1-100) to balance image quality and file size
- **Debug mode** - Enable with `--debug` flag, outputs detailed processing logs and saves intermediate files for troubleshooting
- **Auto directory creation** - Automatically creates parent directories if they don't exist, no manual setup required
- Complete Chinese documentation with full parameter descriptions in Chinese

### Fixed
- **ENOENT error on missing output directory** - Fixed issue where conversion would fail when output directory doesn't exist
- **PNG quality parameter error** - Fixed "png screenshots do not support quality" error by only passing quality parameter to JPEG format
- **JPEG quality not working** - Fixed bug where quality setting had no effect on JPEG output

### Improved
- **Performance** - 50%+ performance improvement for repeated conversions through browser instance reuse
- **Cache cleaning** - More aggressive cache cleaning policy for better privacy protection
- **Documentation** - Updated all documentation with new parameters and usage examples

### Changed
- Updated command line parameter format to support new features while maintaining backward compatibility
- Added font-face definitions in HTML template for better Chinese font rendering

## [1.2.0] - 2026-03-13

### Added
- Initial release with core functionality
- Line-based pagination
- GitHub-style markdown rendering
- Full Chinese and Emoji support

