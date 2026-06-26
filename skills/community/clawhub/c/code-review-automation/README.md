# Code Review Automation

Automated code review for GitHub pull requests using Claude LLM, security scanning, and style checking.

## Features

- **Pull Request Management** - List, search, and get details for PRs
- **AI-Powered Analysis** - Claude LLM for intelligent code reviews
- **Code Quality Scoring** - Automated 0-100 scoring system
- **Security Scanning** - Detect vulnerabilities (secrets, SQL injection, weak crypto, etc.)
- **Style Checking** - PEP8 compliance, naming conventions, linting
- **Full Review** - Combined analysis (LLM + Security + Style)
- **Configurable** - Custom rules via `.reviewrc` configuration files

## Installation

### Prerequisites

- Python 3.8 or higher
- GitHub Personal Access Token (PAT)
- (Optional) Anthropic API Key for LLM analysis

### 1. Install Dependencies

```bash
# Using pip
pip install PyGithub anthropic rich typer python-dotenv

# Using uv (recommended)
uv pip install PyGithub anthropic rich typer python-dotenv
```

### 2. Setup GitHub API Token

Create a `.env` file in the skill directory:
```env
GITHUB_TOKEN=your_github_pat_here
```

Get your GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token (classic)
3. Select `repo` scope (required for full functionality)
4. Copy the token and add it to `.env` file

### 3. Setup Claude API Key (Optional, for LLM analysis)

Add to your `.env` file:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Get your Anthropic API Key:
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add it to `.env` file

## Quick Start

```bash
# Initialize configuration (optional)
python -m code_review.cli config-init

# List open PRs
python -m code_review.cli list-prs owner/repo

# Run full review on a PR
python -m code_review.cli full-review owner/repo 123
```

## Usage Examples

### Basic PR Operations

```bash
# List open PRs
python -m code_review.cli list-prs facebook/react

# List closed PRs with limit
python -m code_review.cli list-prs owner/repo --state closed --limit 20

# Show PR details
python -m code_review.cli pr-info owner/repo 123

# Show files changed
python -m code_review.cli pr-files owner/repo 123

# Search PRs
python -m code_review.cli search-prs owner/repo --query "bug fix"
```

### Code Analysis

```bash
# AI-powered code review
python -m code_review.cli review-pr owner/repo 123

# Security scan only
python -m code_review.cli security-scan owner/repo 123

# Style check only
python -m code_review.cli style-check owner/repo 123

# Full review (all checks)
python -m code_review.cli full-review owner/repo 123

# Full review with custom config
python -m code_review.cli full-review owner/repo 123 --config .reviewrc

# Skip specific checks
python -m code_review.cli full-review owner/repo 123 --skip-security
python -m code_review.cli full-review owner/repo 123 --skip-style
```

### Configuration

```bash
# Initialize default config
python -m code_review.cli config-init

# Initialize config with custom path
python -m code_review.cli config-init --output ~/my-config.yaml
```

## Commands Reference

### `list-prs`
List pull requests from a repository.

```bash
python -m code_review.cli list-prs owner/repo
```

**Options:**
- `--state`: PR state (open, closed, all) - default: open
- `--limit`: Maximum PRs to show - default: 10

### `pr-info`
Show detailed information about a PR.

```bash
python -m code_review.cli pr-info owner/repo 123
```

Shows:
- Title and description
- Author and timestamps
- File change statistics
- Labels and merge status

### `pr-files`
Show files changed in a PR.

```bash
python -m code_review.cli pr-files owner/repo 123
```

Shows:
- Changed files
- Status (added, modified, deleted)
- Additions and deletions per file

### `search-prs`
Search PRs by keyword.

```bash
python -m code_review.cli search-prs owner/repo --query "bug"
```

**Options:**
- `--query`: Search keyword (required)
- `--state`: PR state (open, closed, all) - default: open
- `--limit`: Maximum PRs to show - default: 10

### `repo-info`
Show general repository information.

```bash
python -m code_review.cli repo-info owner/repo
```

Shows:
- Repository name and description
- Programming language
- Stars and forks count
- Open issues and PRs
- Creation and update dates

### `security-scan`
Scan a pull request for security vulnerabilities.

```bash
python -m code_review.cli security-scan owner/repo 123
```

**Detects:**
- Exposed secrets (API keys, tokens, passwords)
- SQL injection vulnerabilities
- Command injection vulnerabilities
- Hardcoded credentials
- Weak cryptography (MD5, SHA1, RC4, DES)
- Unsafe deserialization (pickle)

**Options:**
- `--config`: Configuration file path

### `style-check`
Check a pull request for style and linting issues.

```bash
python -m code_review.cli style-check owner/repo 123
```

**Checks:**
- Line length violations
- Naming convention violations
- Import order
- Blank lines
- Whitespace issues
- Missing docstrings

**Options:**
- `--config`: Configuration file path

### `full-review`
Run full code review (LLM + Security + Style) on a pull request.

```bash
python -m code_review.cli full-review owner/repo 123
```

**Combines:**
- LLM analysis (code quality score)
- Security scanning
- Style checking

**Options:**
- `--config`: Configuration file path
- `--skip-llm`: Skip LLM analysis
- `--skip-security`: Skip security scan
- `--skip-style`: Skip style check

### `review-pr`
Analyze a pull request using Claude AI.

```bash
python -m code_review.cli review-pr owner/repo 123
```

**Shows:**
- AI-powered code review
- Code quality score (0-100)
- Security considerations
- Best practices
- Specific recommendations

**Requires:**
- `GITHUB_TOKEN` in `.env`
- `ANTHROPIC_API_KEY` in `.env`

### `config-init`
Initialize a default configuration file.

```bash
python -m code_review.cli config-init --output .reviewrc
```

Creates a `.reviewrc` file with customizable settings for:
- Security scanning rules
- Style checking rules
- LLM analysis settings
- General configuration

## Configuration

Create a `.reviewrc` file in your project root to customize behavior:

```yaml
security:
  enabled: true
  severity_threshold: "medium"
  check_secrets: true
  check_sql_injection: true
  check_command_injection: true
  check_hardcoded_credentials: true
  check_weak_crypto: true
  check_unsafe_deserialization: true

style:
  enabled: true
  severity_threshold: "warning"
  check_line_length: true
  max_line_length: 88
  check_naming: true
  check_imports: true
  check_blank_lines: true
  check_whitespace: true
  check_docstrings: true

llm:
  enabled: true
  model: "claude-3-7-sonnet-20250219"
  max_tokens: 4096
  temperature: 0.7
  quality_threshold: 70

max_diff_size: 100000
timeout: 60
output_format: "markdown"
show_code_snippets: true
show_recommendations: true
```

## Troubleshooting

### Common Issues

**"GITHUB_TOKEN not found"**
- Ensure `.env` file exists in the skill directory
- Check that the token is correctly formatted as `GITHUB_TOKEN=your_token`

**"Repository not found or you don't have access"**
- Verify the repository name format (owner/repo)
- Check that your PAT has the `repo` scope
- Ensure you have access to the repository

**"ANTHROPIC_API_KEY not found"**
- LLM analysis requires an Anthropic API key
- Add `ANTHROPIC_API_KEY=your_key` to `.env` file
- Get your key from [Anthropic Console](https://console.anthropic.com/)

**"Rate limit exceeded"**
- GitHub API has rate limits (60 requests/hour for unauthenticated)
- Use a PAT with proper scopes
- Wait for the rate limit to reset

**"Diff size exceeds maximum"**
- Large diffs may exceed the default 100KB limit
- Increase `max_diff_size` in `.reviewrc` configuration
- Or review PRs with smaller changes

### Debug Mode

Enable debug logging for more information:

```bash
# Set environment variable
export CODE_REVIEW_LOG_LEVEL=DEBUG

# Or modify .reviewrc to increase logging
```

## Roadmap

### v0.1.0 (Completed)
- GitHub API integration
- PR listing and details
- File change visualization
- PR search functionality
- Repository information

### v0.2.0 (Completed)
- Claude LLM integration for code analysis
- Automated review comments
- Code quality scoring

### v0.3.0 (Completed)
- Security vulnerability scanning
- Style and linting checking
- Configuration file support
- Full review command

### v0.4.0 (Completed)
- Comprehensive unit tests
- Test framework integration
- Coverage tracking

### v0.5.0 (Completed)
- Custom exception classes
- Logging framework
- Error handling improvements

### v0.6.0 (Completed)
- Error handling for all modules
- Security scanner logging
- Style checker logging
- Configuration error handling

### v1.0.0 (Current)
- Complete documentation
- Usage examples
- Production-ready release

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
- Check the documentation
- Review the troubleshooting section
- Open an issue on GitHub
