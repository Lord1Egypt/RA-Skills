# Contributing Guide

Thank you for considering contributing to Auto Video Generator! This document provides guidelines and instructions for contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- **Be respectful** and inclusive
- **Welcome newcomers** and help them learn
- **Focus on constructive feedback**
- **Assume good intentions**

Please report unacceptable behavior to team@avg.dev

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- pip / poetry (package manager)
- FFmpeg installed
- Basic knowledge of:
  - Python (async/await)
  - Web technologies (HTML/CSS/JS)
  - Playwright browser automation
  - Video processing concepts

### First Time Setup

```bash
# 1. Fork the repository on GitHub
#    https://github.com/avg-team/auto-video-generator/fork

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/auto-video-generator.git
cd auto-video-generator

# 3. Add upstream remote
git remote add upstream https://github.com/avg-team/auto-video-generator.git

# 4. Create virtual environment
python -m venv venv

# 5. Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 6. Install development dependencies
pip install -e ".[dev]"

# 7. Install Playwright browsers
playwright install chromium
playwright install-deps chromium

# 8. Verify installation
avg version
pytest tests/
```

---

## Development Setup

### Recommended IDE Configuration

#### VS Code

Install these extensions:
- Python (Microsoft)
- Pylance (Microsoft)
- Black Formatter (Microsoft)
- isort (Microsoft)

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "[python]": {
        "editor.tabSize": 4
    }
}
```

#### PyCharm

1. Open project folder
2. Settings → Project → Interpreter → Select venv python
3. Settings → Tools → External Tools → Configure Black, isort, pytest
4. Enable "Emacs-style line endings"

---

## Project Structure

```
auto_video_generator/
├── __init__.py              # Package entry point, exports
├── cli.py                   # Command-line interface
├── generator.py             # Core VideoGenerator class
├── config_manager.py        # Configuration handling
├── environment_detector.py  # Framework detection
├── framework_adapters.py    # Framework adapter system
├── component_handlers.py    # UI component handlers
├── error_handler.py         # Error handling & retry logic
├── performance_monitor.py   # Metrics & logging
└── utils.py                 # Helper functions

tests/
├── conftest.py              # Shared fixtures
├── test_package.py          # Package-level tests
├── test_generator.py        # VideoGenerator tests
├── test_config.py           # Config manager tests
├── test_adapters.py         # Framework adapter tests
└── test_handlers.py         # Component handler tests

docs/                        # Documentation (MkDocs)
├── mkdocs.yml               # Documentation config
├── index.md                 # Homepage
├── getting-started/         # Getting started guides
├── api/                     # API reference
├── tutorials/               # Tutorials
├── guides/                  # Best practices
└── troubleshooting/         # Help docs

ci/                          # CI/CD scripts
├── scripts/                 # Build/test scripts
│   ├── create_test_pages.py
│   ├── run_benchmarks.py
│   └── generate_test_report.py
└── workflows/               # GitHub Actions configs

.github/
├── workflows/               # CI pipeline definitions
│   ├── ci.yml
│   ├── video-regression.yml
│   └── release.yml
└── actions/                 # Reusable actions
```

---

## Contribution Workflow

### 1. Choose What to Work On

Check existing issues for ideas:
- [Good first issue](https://github.com/avg-team/auto-video-generator/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - For newcomers
- [Help wanted](https://github.com/avg-team/auto-video-generator/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) - Community contributions
- [Bug reports](https://github.com/avg-team/auto-video-generator/issues?q=is%3Aissue+is%3Aopen+label%3Abug) - Fix bugs

Or propose your own idea via [Discussion](https://github.com/avg-team/auto-video-generator/discussions).

### 2. Create a Branch

```bash
# Sync with upstream first
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# Or for bug fix:
git checkout -b fix/bug-description
```

**Branch naming convention:**
- Features: `feature/description`
- Bug fixes: `fix/description`
- Docs: `docs/description`
- Tests: `test/description`

Examples:
- `feature/add-vuetify-support`
- `fix/memory-leak-in-recording`
- `docs/update-api-reference`
- `test/add-datepicker-handler-tests`

### 3. Make Your Changes

#### Code Changes

Follow these steps:

1. **Write code** following coding standards (see below)
2. **Add tests** for new functionality
3. **Update documentation** if API changes
4. **Run linters** to ensure code quality
5. **Run tests** to verify nothing broke

```bash
# Format code
black .
isort .

# Lint
flake8 auto_video_generator tests --max-line-length=100

# Type check (optional but recommended)
mypy auto_video_generator/

# Run tests
pytest tests/ -v --cov=auto_video_generator

# Run specific test file
pytest tests/test_generator.py -v
```

#### Documentation Changes

If you're updating documentation:

1. Edit `.md` files in `docs/` directory
2. Preview locally: `mkdocs serve`
3. Check for broken links: `mkdocs build --strict`

### 4. Commit Your Changes

**Commit message format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring without changing functionality
- `perf`: Performance improvement
- `test`: Adding or correcting tests
- `chore`: Maintenance tasks, dependency updates

**Examples:**

```bash
# Good commit messages
git commit -m "feat(handlers): add DatePickerHandler component"

git commit -m "fix(generator): resolve memory leak in batch generation"

git commit -m "docs(api): update VideoGenerator.generate() examples"

git commit -m "test(adapters): add unit tests for ElementUIAdapter"

# Bad commit messages (avoid these!)
git commit -m "Fixed bug"           # Too vague
git commit -m "Updates"            # No context
git commit -m "WIP"                # Not descriptive
```

**Commit best practices:**
- Keep commits atomic (one logical change per commit)
- Write subject line in imperative mood ("add" not "added")
- Limit subject line to 50 characters
- Wrap body at 72 characters
- Explain *what* and *why*, not *how*

### 5. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name
```

Then create PR on GitHub:

1. Visit: https://github.com/avg-team/auto-video-generator/compare
2. Select your branch
3. Fill out PR template:
   - **Description**: What changed and why
   - **Type of change**: Feature/Bugfix/Docs/etc.
   - **Screenshots**: If UI changes
   - **Testing**: How you tested it
4. Submit PR

**PR Template:**

```markdown
## Description
[Clear description of changes]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing behavior to change)
- [ ] Documentation update

## How Has This Been Tested?
[Describe test coverage]

## Screenshots (if applicable):
[Add screenshots here]

## Checklist:
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged
- [ ] I have updated documentation accordingly
```

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications enforced by tools:

#### Formatting (Black + isort)

Run before committing:
```bash
black .
isort .
```

**Key rules:**
- Line length: **100 characters** (not default 79)
- Use double quotes for strings
- Import order: stdlib → third-party → local
- Trailing commas in multi-line structures

Example:
```python
"""Correct formatting example."""

from pathlib import Path
from typing import Dict, List, Optional

import asyncio
from playwright.async_api import Page

from auto_video_generator.config import ConfigurationManager


class ExampleClass:
    """Example class demonstrating style."""
    
    def __init__(
        self,
        name: str,
        items: Optional[List[str]] = None,
    ) -> None:
        self.name = name
        self.items = items or []
    
    async def process_items(self) -> Dict[str, int]:
        """Process items and return counts."""
        result = {}
        
        for item in self.items:
            result[item] = result.get(item, 0) + 1
        
        return result
```

#### Type Hints

All public APIs must include type hints:

```python
def generate(
    self,
    source: str,
    output: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
) -> GenerationResult:
    """Generate video from source."""
```

#### Docstrings

Use Google-style docstrings:

```python
def calculate_duration(
    frames: int,
    fps: float,
    include_buffer: bool = True,
) -> float:
    """
    Calculate video duration from frame count and FPS.
    
    Args:
        frames: Total number of captured frames.
        fps: Frames per second used during recording.
        include_buffer: Whether to add 0.5s buffer at end.
    
    Returns:
        Duration in seconds as float.
    
    Raises:
        ValueError: If fps <= 0 or frames < 0.
    
    Example:
        >>> calculate_duration(120, 4)
        30.5
    """
    if fps <= 0:
        raise ValueError("FPS must be positive")
    
    base_duration = frames / fps
    
    if include_buffer:
        return base_duration + 0.5
    
    return base_duration
```

#### Error Handling

Use custom exception hierarchy:

```python
from auto_video_generator.exceptions import (
    VideoGenerationError,
    SourceLoadError,
)

async def load_source(self, source: str) -> Page:
    """Load source page into browser."""
    try:
        if source.startswith(("http://", "https://")):
            page = await self.browser.new_page()
            await page.goto(source, timeout=self.timeout_ms)
            return page
        elif Path(source).exists():
            page = await self.browser.new_page()
            file_url = f"file://{Path(source).absolute()}"
            await page.goto(file_url)
            return page
        else:
            raise SourceLoadError(f"Source not found: {source}")
            
    except Exception as e:
        raise SourceLoadError(f"Failed to load {source}: {e}") from e
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| **Modules/files** | snake_case | `video_generator.py` |
| **Classes** | PascalCase | `VideoGenerator` |
| **Functions/methods** | snake_case | `generate_video()` |
| **Variables** | snake_case | `frame_count` |
| **Constants** | UPPER_SNAKE | `MAX_RETRIES` |
| **Private methods** | _leading_underscore | `_internal_method()` |
| **Protected attrs** | _leading_underscore | `_browser_instance` |

---

## Testing Guidelines

### Test Structure

```python
"""Tests for VideoGenerator class."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from auto_video_generator import VideoGenerator


class TestVideoGeneratorGenerate:
    """Test suite for generate() method."""
    
    @pytest.fixture
    def generator(self):
        """Create generator instance for testing."""
        return VideoGenerator(config={"browser": {"headless": True}})
    
    @pytest.mark.asyncio
    async def test_generate_from_url(self, generator):
        """Test generation from URL source."""
        # Arrange
        url = "https://example.com"
        
        # Act
        result = await generator.generate(url)
        
        # Assert
        assert result.status == "success"
        assert result.output_path.endswith(".mp4")
        assert result.duration_seconds > 0
    
    @pytest.mark.asyncio
    async def test_generate_from_local_file(self, generator):
        """Test generation from local HTML file."""
        # Arrange
        test_file = Path(__file__).parent / "fixtures" / "test.html"
        
        # Act
        result = await generator.generate(str(test_file))
        
        # Assert
        assert result.frames_captured > 0
    
    @pytest.mark.asyncio
    async def test_generate_invalid_source_raises_error(self, generator):
        """Test that invalid source raises SourceLoadError."""
        from auto_video_generator.exceptions import SourceLoadError
        
        with pytest.raises(SourceLoadError):
            await generator.generate("nonexistent-file.html")
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_generator.py -v

# Run with coverage
pytest tests/ -v --cov=auto_video_generator --cov-report=term-missing

# Run only fast tests (skip slow integration tests)
pytest tests/ -v -m "not slow"

# Run tests matching keyword
pytest tests/ -k "test_generate" -v

# Run with verbose output and show local variables on failure
pytest tests/ -vv --tb=long
```

### Test Categories

Use markers to categorize tests:

```python
@pytest.mark.unit      # Fast, isolated unit tests
@pytest.mark.integration  # Slower, need external services
@pytest.mark.slow      # Very slow (skip in CI by default)
@pytest.mark.skipif(condition, reason="...")  # Conditional skip
```

### Test Coverage Goal

Maintain minimum **80%** code coverage. Check before submitting:

```bash
pytest tests/ --cov=auto_video_generator --cov-fail-under=80
```

---

## Documentation Standards

### Code Documentation

- All public modules, classes, methods must have docstrings
- Include usage examples in complex APIs
- Update `CHANGELOG.md` for user-facing changes

### User Documentation

- Edit files in `docs/` directory using Markdown
- Follow [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) syntax
- Preview locally: `mkdocs serve`
- Include code examples that actually work
- Add screenshots for UI-related features

### API Reference Updates

When adding new public APIs:

1. Update relevant file in `docs/api/`
2. Add example usage
3. Note breaking changes clearly
4. Update version in changelog

---

## Pull Request Process

### Review Criteria

PRs are evaluated on:

✅ **Code Quality**
- Follows style guidelines
- Properly typed
- Well-documented
- No obvious bugs

✅ **Testing**
- Adequate test coverage
- Tests pass
- Edge cases covered

✅ **Documentation**
- Updated if needed
- Clear commit messages
- Changelog updated

✅ **Functionality**
- Solves stated problem
- Doesn't break existing features
- Backward compatible (or documented breaking change)

### Review Process

1. Automated checks run (lint, test, build)
2. Maintainer reviews within 48 hours
3. Address review comments (respond to each one)
4. Once approved, maintainer merges

### After Merge

- 🎉 Thank you for contributing!
- Your contribution will appear in next release
- Consider helping review others' PRs

---

## Recognition

Contributors are recognized in:
- **README.md** Contributors section
- **Release notes** for significant features
- **Documentation** for tutorials/guides written

---

## Need Help?

- 💬 Ask questions in [Discussions](https://github.com/avg-team/auto-video-generator/discussions)
- 📖 Read [documentation](https://auto-video-generator.readthedocs.io)
- 🐛 Report issues via [Issues](https://github.com/avg-team/auto-video-generator/issues)
- 📧 Email maintainers: team@avg.dev

---

**Happy contributing! 🚀**

Your efforts make Auto Video Generator better for everyone.
