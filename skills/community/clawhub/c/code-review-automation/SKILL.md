---
name: code-review-automation
displayName: Code Review Automation
version: 1.0.0
author: Fumi (Hirofumi's AI Agent)
description: Automated code review for GitHub pull requests using Claude LLM. PR analysis, security scanning, and style checking.
category: development
tags: [github, code-review, claude, automation, security, style-check]
license: MIT
icon: 🔍
command: uv run --with PyGithub --with anthropic --with rich --with typer --with python-dotenv python -m code_review.cli
---

# 🔍 Code Review Automation

**Automated code review for GitHub pull requests using Claude LLM**

Automatically analyze GitHub pull requests, provide intelligent code reviews, security scanning, and style checking using Claude AI.

## ✨ Features

- **PR Listing** - View all pull requests in a repository
- **PR Details** - Get comprehensive information about any PR
- **File Changes** - See exactly what files changed
- **PR Search** - Search PRs by keyword
- **Repository Info** - Get general repository statistics
- **Claude Analysis** - AI-powered code review using Claude LLM
- **Code Quality Scoring** - Automated quality assessment (0-100)
- **Security Scanning** - Automated security vulnerability detection
- **Style Checking** - Automated style and linting checks
- **Full Review** - Complete review with all checks
- **Configurable** - Custom rules via `.reviewrc`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
uv pip install PyGithub anthropic rich typer python-dotenv
```

### 2. Setup GitHub API Token

Get your GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Create `.env` file:

```env
GITHUB_TOKEN=your_github_pat_here
```

### 3. Review Pull Requests

```bash
# List open PRs
code-review list-prs owner/repo

# Show PR details
code-review pr-info owner/repo 123

# Show files changed
code-review pr-files owner/repo 123

# Analyze PR with Claude AI
code-review review-pr owner/repo 123
```

## 📋 Commands

### `list-prs`
List pull requests from a repository.

```bash
code-review list-prs owner/repo
```

Options:
- `--state`: PR state (open, closed, all) - default: open
- `--limit`: Maximum PRs to show - default: 10

### `pr-info`
Show detailed information about a specific PR.

```bash
code-review pr-info owner/repo 123
```

Shows:
- Title and description
- Author and timestamps
- File change statistics
- Labels and merge status

### `pr-files`
Show files changed in a PR.

```bash
code-review pr-files owner/repo 123
```

Shows:
- Changed files
- Status (added, modified, deleted)
- Additions and deletions per file

### `search-prs`
Search pull requests by keyword.

```bash
code-review search-prs owner/repo --query "bug"
```

Options:
- `--query`: Search keyword (required)
- `--state`: PR state (open, closed, all) - default: open
- `--limit`: Maximum PRs to show - default: 10

### `repo-info`
Show general repository information.

```bash
code-review repo-info owner/repo
```

Shows:
- Repository name and description
- Programming language
- Stars and forks count
- Open issues and PRs
- Creation and update dates

### `review-pr`
Analyze a pull request using Claude AI.

```bash
code-review review-pr owner/repo 123
```

Shows:
- AI-powered code review
- Code quality score (0-100)
- Security considerations
- Best practices
- Specific recommendations

Requires:
- `GITHUB_TOKEN` in `.env`
- `ANTHROPIC_API_KEY` in `.env`

### `security-scan`
Scan a pull request for security vulnerabilities.

```bash
code-review security-scan owner/repo 123
```

Detects:
- Exposed secrets (API keys, tokens, passwords)
- SQL injection vulnerabilities
- Command injection vulnerabilities
- Hardcoded credentials
- Weak cryptography (MD5, SHA1, RC4, DES)
- Unsafe deserialization (pickle)

Options:
- `--config`: Configuration file path

### `style-check`
Check a pull request for style and linting issues.

```bash
code-review style-check owner/repo 123
```

Checks:
- Line length violations
- Naming convention violations
- Import order
- Blank lines
- Whitespace issues
- Missing docstrings

Options:
- `--config`: Configuration file path

### `full-review`
Run full code review (LLM + Security + Style) on a pull request.

```bash
code-review full-review owner/repo 123
```

Combines:
- LLM analysis (code quality score)
- Security scanning
- Style checking

Options:
- `--config`: Configuration file path
- `--skip-llm`: Skip LLM analysis
- `--skip-security`: Skip security scan
- `--skip-style`: Skip style check

### `config-init`
Initialize a default configuration file.

```bash
code-review config-init --output .reviewrc
```

Creates a `.reviewrc` file with customizable settings for:
- Security scanning rules
- Style checking rules
- LLM analysis settings

## 🔧 Technical Details

### GitHub API Integration
- Uses PyGithub library
- Authenticates with Personal Access Token
- Rate limit handled automatically

### LLM Integration
- Claude API for code analysis
- Intelligent code review comments
- Context-aware suggestions
- Code quality scoring

### Security Scanning
- Static analysis for common vulnerabilities
- Pattern-based detection
- Severity-based categorization
- Configurable rules

### Style Checking
- PEP8 compliance checks
- Naming convention validation
- Line length enforcement
- Import order verification
- Whitespace checks

### Configuration
- YAML/JSON config files
- Project-specific settings
- Customizable thresholds
- `.reviewrc` support

## 📊 Examples

```bash
# Run full review
code-review full-review facebook/react 34567

# Security scan only
code-review security-scan owner/repo 123

# Style check only
code-review style-check owner/repo 123

# AI analysis only
code-review review-pr owner/repo 123

# List all closed PRs
code-review list-prs owner/repo --state closed --limit 20

# Initialize config
code-review config-init
```

## 🔐 Security

- GitHub PAT stored in `.env` file (never committed)
- No secrets logged or displayed
- IP whitelist recommended

## 🚧 Roadmap

### v0.2.0 - Claude Integration (Completed)
- Claude API integration
- Automated PR analysis
- Intelligent review comments
- Code quality scoring

### v0.3.0 - Security & Style (Current)
- Security vulnerability scanning
- Style and linting checks
- Automated fix suggestions
- Configuration file support
- Full review command

### v1.0.0 (Planned)
- Multi-platform support (GitLab, Bitbucket)
- CI/CD integration
- Team collaboration features
- Review dashboard

## 📄 License

MIT

## 🙋 Support

For issues or questions:
- Check the documentation
- Open an issue on GitHub
