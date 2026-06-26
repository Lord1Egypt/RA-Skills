# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-05-30

### Added
- **Complete modular architecture rewrite**
  - New package structure: `auto_video_generator/`
  - Clean separation of concerns (generator, config, adapters, web)
  - Public API with type hints and documentation
  
- **8 new UI component handlers** (Phase A-1)
  - DatePickerHandler: Date selection, range picking
  - TreeHandler: Node expansion, checking, selection
  - UploadHandler: File upload simulation
  - TabsHandler: Tab switching, active tab detection
  - TableHandler: Sorting, filtering, pagination
  - FormHandler: Input filling, form submission
  - MessageHandler: Toast/notification handling
  - TooltipHandler: Show/hide tooltips

- **Production-grade error handling** (Phase A-2)
  - Custom exception hierarchy (VideoGenerationError, BrowserError, etc.)
  - Retry decorator with exponential backoff
  - Circuit breaker pattern (Closed/Open/Half-Open states)
  - Error context manager for detailed error reporting
  - Error handler registry for custom error processors

- **Performance monitoring system** (Phase A-3)
  - StructuredLogger with multiple log levels and formatters
  - PerformanceMonitor for metrics collection (timing, memory, frame rate)
  - Metric aggregation and statistics
  - Log file rotation management
  - Dashboard visualization support

- **Configuration management** (Phase A-4)
  - Multi-format config support (YAML, JSON, TOML)
  - Environment variable overrides (AVG_* prefix)
  - Configuration layering (default → user → project → env)
  - Configuration validation and type checking
  - Example configuration files

- **VS Code extension** (Phase B-1)
  - Visual configuration panel in sidebar
  - One-click video generation from current file
  - Environment detection integration
  - Performance dashboard view
  - Status bar indicator

- **Web UI interface** (Phase B-2)
  - Flask backend with REST API
  - WebSocket real-time communication
  - Responsive frontend design
  - File upload with drag & drop
  - Progress tracking with stage display
  - Video preview player
  - Multiple input modes (file, URL, template)

- **pip package distribution** (Phase C-1)
  - pyproject.toml with modern build system
  - CLI commands (avg, avg-generate, avg-web, avg-init)
  - Python API (VideoGenerator class)
  - Comprehensive documentation (README.md)
  - Test suite with pytest
  - Optional dependencies (dev, web, all)

### Changed
- **Breaking**: Package structure reorganized from flat modules to `auto_video_generator/` package
- **Breaking**: Import paths updated (`from auto_video_generator import ...`)
- Improved error messages with context information
- Enhanced logging output with Rich library formatting
- Better default configurations for common use cases
- Optimized memory usage during video generation

### Fixed
- Unicode encoding errors on Windows systems
- File handle leaks in logging system
- Race conditions in concurrent metric collection
- Configuration merge conflicts between layers

### Removed
- Deprecated synchronous-only APIs (replaced with async-first design)
- Old monolithic generator module (split into focused components)

---

## [2.0.0] - 2024-12-15

### Added
- Initial public release
- Basic video generation from HTML pages
- Edge TTS integration with Chinese voices
- Playwright-based browser automation
- Multi-framework UI detection (Vue, React)
- Basic component handlers (Button, Input, Modal)
- Command-line interface (basic version)

### Changed
- Initial architecture established
- Core generation pipeline implemented

---

## [1.0.0] - 2024-10-01

### Added
- Proof of concept implementation
- Basic screenshot capture
- Simple FFmpeg encoding
- Manual script execution mode

---

## [Unreleased]

### Planned Features (Future Phases)
- Phase B-3: CI/CD pipeline integration (automated regression test videos)
- Phase C-2: Complete documentation suite (API docs, tutorials, best practices)
- Phase C-3: Template marketplace (industry templates, scenario templates)
- Plugin system for custom component handlers
- Cloud deployment option for server-side rendering
- Team collaboration features (shared configs, project templates)
- Advanced audio processing (background music, sound effects)
- Multi-language narration support expansion
- Video editing capabilities (trimming, annotations, overlays)

---

## Migration Guide

### From v2.x to v3.0

```python
# OLD (v2.x)
from video_generator import generate_video
result = generate_video("https://example.com")

# NEW (v3.0)
import asyncio
from auto_video_generator import VideoGenerator

gen = VideoGenerator()
result = asyncio.run(gen.generate("https://example.com"))
```

### From CLI v2 to v3

```bash
# OLD
video-gen https://example.com

# NEW
avg generate https://example.com
```

---

[3.0.0]: https://github.com/avg-team/auto-video-generator/releases/tag/v3.0.0
[2.0.0]: https://github.com/avg-team/auto-video-generator/releases/tag/v2.0.0
[1.0.0]: https://github.com/avg-team/auto-video-generator/releases/tag/v1.0.0
