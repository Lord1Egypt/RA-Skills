# CI/CD Pipeline Documentation
# =============================

This document describes the continuous integration and deployment pipeline for **Auto Video Generator**.

## Overview

The CI/CD system is designed to:
- ✅ Ensure code quality with automated linting and testing
- 🎬 Test video generation in isolated environments
- 📦 Build and publish packages to PyPI
- 🚀 Deploy to production automatically on releases

## Supported Platforms

| Platform | Configuration File | Status |
|----------|-------------------|--------|
| **GitHub Actions** | `.github/workflows/*.yml` | ✅ Primary |
| **GitLab CI** | `.gitlab-ci.yml` | ✅ Supported |
| **Docker** | `Dockerfile.ci` | ✅ Available |

---

## GitHub Actions Workflows

### 1. Main CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main`, `develop`, or `feature/*` branches (when Python/TS files change)
- Pull requests to `main`
- Manual dispatch (with optional video generation)

**Jobs:**

| Job | Purpose | Duration |
|-----|---------|----------|
| `lint-and-test` | Code quality, linting, unit tests across Python versions | ~5 min |
| `build-package` | Build sdist/wheel, verify with Twine | ~2 min |
| `video-generation-test` | Generate demo videos from test pages | ~10 min |
| `build-vscode-extension` | Compile TypeScript, package .vsix | ~3 min |
| `build-docker-image` | Build & push Docker image to GHCR | ~5 min |
| `ci-summary` | Aggregate results, generate summary | <1 min |

**Manual Triggers:**
```bash
# Trigger via GitHub API or UI
# Options available:
# - generate_video: true/false
# - test_url: "https://example.com"
# - fps: "4" (1-30)
```

### 2. Video Regression Tests (`video-regression.yml`)

**Schedule:** Daily at 6:00 AM UTC (2:00 PM Beijing time)

**Test Suites:**
- `basic`: Simple HTML pages, dashboard, forms
- `components`: All component handlers (Table, Form, DatePicker...)
- `frameworks`: Each framework adapter (Ant Design Vue, Element UI...)
- `performance`: Benchmark timing and memory usage

### 3. Release Pipeline (`release.yml`)

**Triggers:**
- Push of version tag (`v*`)
- Manual dispatch with version number

**Process:**
1. Validate version format
2. Run full test suite (must pass)
3. Build distribution packages
4. Publish to PyPI (requires `PYPI_API_TOKEN`)
5. Create GitHub Release with changelog
6. Update documentation site
7. Send notifications (Slack, etc.)

**Secrets Required:**
- `PYPI_API_TOKEN` - PyPI upload token
- `SLACK_WEBHOOK_URL` - Optional Slack notification
- `DOCS_DEPLOY_TOKEN` - For docs site update

### 4. PR Checks (`pr-check.yml`)

**Runs on:** Every PR to main/develop

**Checks:**
- Quick validation (required files, version format)
- Code quality (Ruff, Black, MyPy)
- Unit tests (Python 3.9 + 3.11)
- Integration smoke test
- Code complexity analysis
- Auto-labeling for breaking changes

---

## GitLab CI Pipeline

### Structure

```yaml
stages:
  - lint          # Code quality checks
  - test          # Unit and integration tests
  - build         # Package builds
  - video-test    # Video generation testing (optional)
  - release       # Publishing releases
```

### Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHON_VERSION` | Python version to use | `3.11` |
| `VIDEO_TEST` | Enable video generation tests | `false` |
| `REGRESSION_TEST` | Run regression suite | `false` |
| `PYPI_API_TOKEN` | PyPI upload token | Required for release |

### Manual Jobs

Some jobs require manual trigger:
- `video:test-generation` - Test video generation in CI
- `release:pypi` - Publish to PyPI

---

## Docker Image for CI

### Build Command

```bash
docker build -f Dockerfile.ci -t avg-ci:latest .
```

### Usage in CI

```yaml
video-test:
  image: avg-ci:latest
  script:
    - avg generate ./test.html --output ./output.mp4
```

### Pre-installed Components

- Python 3.11 with all dependencies
- Playwright Chromium browser
- FFmpeg for video processing
- CJK fonts support
- Xvfb for headless display

---

## Running Locally

### Simulate CI Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dev dependencies
pip install -e ".[dev]"

# Run linters
black --check auto_video_generator/
isort --check-only auto_video_generator/
flake8 auto_video_generator/

# Run tests
pytest tests/test_package.py -v --cov=auto_video_generator

# Run benchmarks
python ci/scripts/run_benchmarks.py

# Generate test report
python ci/scripts/generate_test_report.py \
    --input-dir ./artifacts/ \
    --output ./report.html
```

### Test Pages Generation

```bash
python ci/scripts/create_test_pages.py --output-dir ./test-pages

# This creates:
# - simple.html
# - dashboard.html  
# - form.html
# - tabs.html
```

### Changelog Generation

```bash
python ci/scripts/generate_changelog.py \
    --version 3.1.0 \
    --previous 3.0.0 \
    --output CHANGELOG_RELEASE.md
```

---

## Troubleshooting

### Common Issues

#### 1. Playwright Installation Fails

```bash
# Solution: Install system dependencies first
sudo apt-get update
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 \
    libxkbcommon0 libatspi2.0-0 libxcomposite1 \
    libxdamage1 libxrandr2 gbm libpango-1.0-0 \
    libcairo2 libasound2

playwright install chromium
playwright install-deps chromium
```

#### 2. Video Generation Timeout in CI

```yaml
# Increase timeout in workflow
- name: Generate video
  timeout-minutes: 10
  run: avg generate ... --duration 30
```

#### 3. Memory Issues

```yaml
# Add resource limits
resources:
  limits:
    memory: 4Gi
    cpu: '2'
```

#### 4. Font Rendering Issues (CJK Characters)

The Docker image includes CJK fonts by default. If missing:

```dockerfile
RUN apt-get install -y fonts-noto-cjk fonts-wqy-microhei
```

---

## Performance Metrics

### Typical CI Times

| Job Type | Average Time | Resources |
|----------|--------------|-----------|
| Lint & Format Check | 2-3 min | 1 CPU, 2GB RAM |
| Unit Tests | 3-5 min | 2 CPU, 4GB RAM |
| Integration Tests | 8-12 min | 2 CPU, 4GB RAM |
| Package Build | 1-2 min | 1 CPU, 2GB RAM |
| Video Generation | 5-10 min | 2 CPU, 4GB RAM |

### Optimization Tips

1. **Cache Dependencies**: Use pip caching and Playwright cache
2. **Parallel Jobs**: Run independent jobs concurrently
3. **Selective Testing**: Only run affected tests based on changes
4. **Pre-built Images**: Use cached Docker layers

---

## Security Considerations

### Secrets Management

Never commit secrets to repository. Use:
- GitHub Secrets / GitLab CI/CD Variables
- Environment-specific `.env` files (gitignored)
- Vault integration for sensitive data

### Dependency Scanning

Enable automatic vulnerability scanning:
- GitHub: Dependabot + CodeQL
- GitLab: Dependency Scanning included

### Container Security

Scan Docker images:
```bash
trivy image avg-ci:latest
```

---

## Contributing to CI/CD

### Adding New Workflow

1. Create YAML file in `.github/workflows/`
2. Follow naming convention: `{purpose}.yml`
3. Include proper triggers and conditions
4. Add artifact uploads for debugging
5. Update this documentation

### Adding New Test Script

1. Place in `ci/scripts/`
2. Make executable: `chmod +x`
3. Add argument parsing with argparse
4. Include error handling
5. Document usage in comments

---

## Support

For issues with the CI/CD pipeline:
- Check [GitHub Actions logs](https://github.com/avg-team/auto-video-generator/actions)
- Review [GitLab CI/CD docs](https://docs.gitlab.com/ee/ci/)
- Open an issue with `CI/CD` label

---

*Last updated: 2026-05-30*
