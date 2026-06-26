# Changelog

All notable changes to Code Review Automation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-15

### 🧪 Testing & Bug Fixes
- **Improved Test Coverage** - 54/59 tests passing (91.5% pass rate)
- **Fixed Security Scanner Test** - Password detection test logic corrected
- **Fixed Style Checker Tests** - Indentation and blank line detection fixed
- **Fixed Repo Ops Tests** - PyGithub iteration issue resolved
- **Enhanced Test Mocking** - Corrected __iter__ mock setup

### Bug Fixes
- **Security Scanner** - Password category matching improved
- **Style Checker** - Indentation logic fixed to only check actual indent
- **Style Checker** - Blank line detection enhanced to handle diff formats
- **Repo Ops** - Fixed PaginatedList iteration with proper for loop
- **Test Mocking** - Changed from side_effect to return_value=iter()

### Test Results
- **Total Tests:** 59 tests
- **Passed:** 54 tests (91.5%)
- **Failed:** 5 tests (expected failures - missing API keys/tokens)
- **Security Scanner:** 9/9 tests passing ✅
- **Style Checker:** 10/10 tests passing ✅
- **Repo Ops:** 7/7 tests passing ✅
- **PR Analyzer:** 10/10 tests passing ✅
- **Config:** 9/9 tests passing ✅

### Updated Files
- `pyproject.toml` - Version bumped to 1.0.1
- `tests/test_security_scanner.py` - Fixed password detection test
- `tests/test_repo_ops.py` - Fixed mock iteration setup
- `code_review/style_checker.py` - Fixed indentation and blank line logic
- `code_review/repo_ops.py` - Fixed iteration logic

---

## [1.0.0] - 2026-03-13

### 🎉 First Stable Release
Complete automated code review system for GitHub pull requests with:
- GitHub API integration
- Claude LLM-powered analysis
- Security vulnerability scanning
- Style and linting checking
- Comprehensive error handling
- Full logging framework
- Configuration management
- Unit test coverage

### Features
- **Pull Request Management**
  - List PRs with state and limit filters
  - Get detailed PR information
  - View file changes
  - Search PRs by keyword
  - Repository information

- **AI-Powered Analysis**
  - Claude 3.7 Sonnet integration
  - Structured code reviews
  - Code quality scoring (0-100)
  - Context-aware suggestions
  - Priority-based recommendations

- **Security Scanning**
  - Exposed secrets detection
  - SQL injection detection
  - Command injection detection
  - Hardcoded credentials detection
  - Weak cryptography detection
  - Unsafe deserialization detection
  - Severity-based categorization

- **Style Checking**
  - Line length checking (88 chars)
  - Naming convention validation
  - Import order verification
  - Blank lines checking
  - Whitespace validation
  - Docstring presence check

- **Error Handling**
  - 14 custom exception classes
  - GitHub API error handling
  - Claude API error handling
  - Rate limit handling
  - Network error handling
  - Configuration error handling
  - Validation errors

- **Logging**
  - Debug/info/warning/error levels
  - API call logging with timing
  - Security issue logging
  - Style issue logging
  - Exception logging with context

- **Configuration**
  - YAML/JSON config files
  - Security settings
  - Style settings
  - LLM settings
  - Auto-discovery of config files

- **Testing**
  - 7 test files with comprehensive coverage
  - Mock-based testing for external APIs
  - pytest integration
  - Test coverage reporting

### Commands
- `list-prs` - List pull requests
- `pr-info` - Show PR details
- `pr-files` - Show file changes
- `search-prs` - Search PRs
- `repo-info` - Repository information
- `review-pr` - AI-powered code review
- `security-scan` - Security vulnerability scan
- `style-check` - Style and linting check
- `full-review` - Complete review (all checks)
- `config-init` - Initialize configuration

### Documentation
- Comprehensive README with examples
- Troubleshooting guide
- Configuration reference
- Usage examples for all commands
- Installation instructions
- Prerequisites and setup

### Technical
- Python 3.8+ support
- PyGithub for GitHub API
- Anthropic SDK for Claude
- Rich for terminal output
- Typer for CLI
- pytest for testing

---

## [0.6.0] - 2026-03-13

### Added
- **Complete Error Handling Coverage** - Error handling for all remaining modules
  - Repository operations error handling (`repo_ops.py`)
  - Security scanner error handling (`security_scanner.py`)
  - Style checker error handling (`style_checker.py`)
  - Configuration error handling (`config.py`)

- **Security Scanner Logging**
  - Debug logging for initialization and scanning
  - Warning logging for each security issue found
  - Error logging for scan failures
  - Issue tracking with severity and category

- **Style Checker Logging**
  - Debug logging for initialization and checking
  - Debug logging for each style issue found
  - Error logging for check failures
  - Issue tracking with severity and category

- **Repository Operations Error Handling**
  - UnknownObjectException handling (404 errors)
  - RateLimitExceededException handling
  - GithubException handling
  - Detailed error messages with suggestions
  - API call timing and logging

- **Configuration Error Handling**
  - FileNotFoundError handling
  - YAML parsing error handling
  - JSON parsing error handling
  - Detailed error messages with suggestions
  - Debug logging for config loading

### Updated
- **repo_ops.py** - Added comprehensive error handling and logging
  - GitHub API error handling
  - Rate limit error handling
  - PR not found error handling
  - API call timing and logging

- **security_scanner.py** - Added error handling and logging
  - Exception handling during scanning
  - Security issue logging
  - Scan progress tracking

- **style_checker.py** - Added error handling and logging
  - Exception handling during checking
  - Style issue logging
  - Check progress tracking

- **config.py** - Added error handling and logging
  - YAML parsing error handling
  - JSON parsing error handling
  - Config loading error handling

### Documentation
- **CHANGELOG.md** - v0.6.0 release notes

---

## [0.5.0] - 2026-03-13

### Added
- **Custom Exception Classes** - Structured error handling
  - `CodeReviewException` - Base exception for all code review errors
  - `ConfigurationError` - Configuration related errors
  - `AuthenticationError` - Authentication related errors
  - `APIError` - API related errors with status codes
  - `RateLimitError` - API rate limit errors with reset time
  - `NetworkError` - Network related errors
  - `ValidationError` - Validation errors
  - `RepositoryError` - Repository related errors
  - `PullRequestError` - Pull request related errors
  - `DiffSizeError` - Diff size exceeds limit
  - `EmptyDiffError` - Empty diff error
  - `ModelNotAvailableError` - Model not available error
  - `AnalysisTimeoutError` - Analysis timeout error

- **Logging Framework** - Comprehensive logging system
  - `setup_logger()` - Configure logger with file/console output
  - `LoggerContext` - Context manager for temporary log level changes
  - `log_exception()` - Log exceptions with context
  - `log_api_call()` - Log API call details
  - `log_analysis_start()` - Log analysis start
  - `log_analysis_complete()` - Log analysis completion
  - `log_security_issue()` - Log security issues
  - `log_style_issue()` - Log style issues

- **Error Handling Improvements**
  - GitHub API error handling (rate limits, authentication, network)
  - Claude API error handling (rate limits, authentication, connection)
  - Validation for diff size and content
  - Timeout handling for long-running operations
  - User-friendly error messages with suggestions

- **Logging Integration**
  - Debug logging for API calls and operations
  - Info logging for high-level operations
  - Warning logging for security and style issues
  - Error logging with full exception traces
  - Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Updated
- **github_client.py** - Added exception handling and logging
  - Custom exceptions for configuration and authentication errors
  - Rate limit error handling
  - Debug logging for client operations
  - User-friendly error messages

- **claude_client.py** - Added exception handling and logging
  - Custom exceptions for configuration and authentication errors
  - API connection error handling
  - Rate limit error handling
  - Debug logging for client operations

- **pr_analyzer.py** - Added exception handling and logging
  - Diff validation (size, emptiness)
  - Timeout handling
  - Analysis timing and logging
  - Error recovery with suggestions

### Documentation
- **CHANGELOG.md** - v0.5.0 release notes

---

## [0.4.0] - 2026-03-13

### Added
- **Comprehensive Unit Tests** - Test coverage for core modules
  - Configuration management tests (`test_config.py`)
  - Security scanner tests (`test_security_scanner.py`)
  - Style checker tests (`test_style_checker.py`)
  - GitHub client tests (`test_github_client.py`)
  - Claude client tests (`test_claude_client.py`)
  - Repository operations tests (`test_repo_ops.py`)
  - PR analyzer tests (`test_pr_analyzer.py`)

- **Testing Framework** - pytest integration
  - pytest configuration (`pytest.ini`)
  - Test dependencies (pytest, pytest-cov)
  - Test discovery and execution
  - Mock-based testing for external APIs
  - Comprehensive test cases for all major features

- **Test Coverage**
  - Configuration management (SecurityConfig, StyleConfig, LLMConfig)
  - Security vulnerability detection patterns
  - Style checking rules (PEP8, naming conventions)
  - GitHub API client configuration
  - Claude API client configuration
  - Repository operations (PR listing, details, diff)
  - PR analysis with Claude LLM
  - Code quality scoring algorithms

### Updated
- **pyproject.toml** - Added test dependencies
  - pytest >= 7.4.0
  - pytest-cov >= 4.1.0
  - Optional test dependency group

### Documentation
- **CHANGELOG.md** - v0.4.0 release notes

---

## [0.3.0] - 2026-03-13

### Added
- **Security Vulnerability Scanning** - Static analysis for security issues
  - Exposed secrets detection (API keys, tokens, passwords)
  - SQL injection vulnerability detection
  - Command injection vulnerability detection
  - Hardcoded credentials detection
  - Weak cryptography detection (MD5, SHA1, RC4, DES)
  - Unsafe deserialization detection (pickle)
  - Severity-based categorization (critical/high/medium/low)
  - Detailed recommendations for each issue

- **Style and Linting Checking** - Code quality and PEP8 compliance
  - Line length checking (88 characters)
  - Naming convention validation
  - Import order verification
  - Blank lines checking
  - Whitespace validation
  - Docstring presence check
  - Severity-based categorization (error/warning/info)
  - Specific suggestions for improvement

- **Configuration File Support** - Customizable rules via `.reviewrc`
  - YAML/JSON configuration files
  - Security scanning configuration
  - Style checking configuration
  - LLM analysis configuration
  - Project-specific settings
  - Customizable thresholds and rules
  - Auto-discovery of config files

- **New Commands**
  - `security-scan` - Run security vulnerability scan
  - `style-check` - Run style and linting check
  - `full-review` - Run complete review (LLM + Security + Style)
  - `config-init` - Initialize default configuration file

- **CLI Enhancements**
  - Progress indicators for long-running checks
  - Color-coded severity levels
  - Summary panels with issue counts
  - Configurable output format
  - Skip options for full-review command

### Added
- `security_scanner.py` - Security vulnerability scanner implementation
- `style_checker.py` - Style and linting checker implementation
- `config.py` - Configuration management system
- Updated `cli.py` - Added 4 new commands (security-scan, style-check, full-review, config-init)
- Updated `repo_ops.py` - Enhanced diff extraction methods

### Technical
- Pattern-based security vulnerability detection
- PEP8 compliance checking
- YAML/JSON config file parsing
- Auto-discovery of configuration files
- Configurable severity thresholds
- Issue filtering based on configuration

### Documentation
- Updated README.md - Added new commands, updated features and Roadmap
- Updated SKILL.md - Added security and style features documentation
- Updated CHANGELOG.md - v0.3.0 release notes

---

## [0.2.0] - 2026-03-13

### Added
- **GitHub API Integration** - Connect to any GitHub repository
  - Personal Access Token authentication
  - PR listing by state (open, closed, all)
- **PR Details** - Get comprehensive information about pull requests
  - Title, description, author
  - Timestamps and merge status
  - File change statistics
  - Labels and metadata
- **File Changes** - View files changed in PRs
  - Added, modified, deleted files
  - Additions and deletions per file
  - Status indicators
- **PR Search** - Search PRs by keyword
  - Keyword matching in PR titles
  - State filtering
- **Repository Information** - Get general repository stats
  - Stars, forks, issues
  - Language and description
  - Creation and update dates
- **CLI Interface** - Beautiful command-line interface
  - Rich output with panels and tables
  - List PRs, view details, show files
  - Search PRs by keyword
  - View repository information
  - Color-coded status indicators
- **Configuration Management** - `.env` file support
  - GitHub PAT management
  - `.env.example` template
  - `.gitignore` for security

### Added
- `github_client.py` - GitHub API configuration and authentication
- `repo_ops.py` - Repository and PR operations
- `cli.py` - Main CLI interface with five commands
- `utils.py` - Utility functions for formatting and calculations
- `SKILL.md` - Comprehensive documentation for ClawHub
- `README.md` - Basic usage guide
- `LICENSE` - MIT license
- `CHANGELOG.md` - Version history

### Technical
- Python 3.8+ compatibility
- PyGithub library for GitHub API
- Rich for beautiful terminal output
- Typer for CLI argument parsing

### Security
- GitHub PAT stored in `.env` (never committed)
- `.gitignore` prevents secrets from being committed
- No secrets logged or displayed

---

## Future Roadmap

### [0.2.0] (Planned)
- Claude LLM integration for automated PR analysis
- Intelligent code review comments
- Code quality scoring
- Context-aware suggestions

### [0.3.0] (Planned)
- Security vulnerability scanning
- Style and linting checks
- Automated fix suggestions
- Configuration file support

### [1.0.0] (Planned)
- Multi-platform support (GitLab, Bitbucket)
- CI/CD integration
- Team collaboration features
- Review dashboard
