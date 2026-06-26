# Security Considerations

## Overview

This skill has been audited for security before open-source publishing. No private data, API keys, or credentials are hardcoded.

## Input Validation

### RSS/URL Fetching
- All RSS feed URLs are user-configured in `config.yaml`
- Network requests use `urllib` with proper timeouts (10 seconds default)
- HTML content is sanitized with regex-based tag stripping
- User-Agent headers are set for polite crawling

### File Paths
- All file operations are relative to skill directory or explicitly configured
- No dynamic path construction from user input
- Pipeline uses `Path().parent.mkdir(parents=True, exist_ok=True)` for safe directory creation

## Subprocess Usage

### Safe Command Execution
The skill uses `subprocess.run()` in two places:

1. **pipeline.py**: Orchestrates script execution
   - Commands are hardcoded (python3 scripts/*.py)
   - No shell=True, no user input in command construction
   - Uses `check=True` for error detection

2. **upload.py**: AWS CLI for S3 upload
   - Commands are hardcoded (aws s3 cp)
   - File paths are sanitized/validated before use
   - Bucket names come from config.yaml (not command-line input)

## No Eval/Exec

The skill does NOT use:
- `eval()`
- `exec()`
- `compile()`
- `__import__()`
- `importlib` dynamic loading beyond known sources

## Configuration Security

### config.yaml
- Contains only user preferences (RSS URLs, interests, storage settings)
- No credentials stored directly (use environment variables or AWS CLI config)
- Example file has placeholder values only

### Credentials
- AWS credentials: Use `aws configure` or environment variables
- ElevenLabs API key: OpenClaw handles via tool integration
- No hardcoded keys in any file

## Dependency Management

### Zero External Dependencies
- Uses Python 3.7+ stdlib only
- No pip packages required for core discovery functionality
- Optional dependencies (aws CLI) are well-established tools

### Source Integrity
All source modules (`sources/*.py`) are:
- Included in this repository
- Reviewed for security
- Use only stdlib (urllib, json, re)

## LLM Integration

### Script Generation
- LLM access is via OpenClaw worker delegation
- No direct API calls with hardcoded keys
- Prompt templates in `templates/` are reviewed for injection risks
- Research data is structured JSON, not user-controlled strings injected into prompts

## Network Security

### Outbound Requests
1. RSS feeds (user-configured URLs)
2. Hacker News API (hardcoded Firebase endpoint)
3. Nature.com RSS (hardcoded URLs)
4. AWS S3 (if configured)

All requests use HTTPS where available and have timeouts.

## Data Privacy

### No User Tracking
- No analytics, telemetry, or phone-home
- No data sent to external services except:
  - Configured RSS feeds (standard HTTP requests)
  - ElevenLabs TTS (via OpenClaw tool)
  - S3 upload (if user configures it)

### Local Data Storage
- `output/` directory contains generated episodes
- `data/history.json` tracks past topics to avoid duplicates
- All files stored locally or in user-controlled S3 bucket

## Reporting Security Issues

If you discover a security issue, please report it via:
- GitHub Issues: [skill repository]
- ClawHub: Contact skill maintainers

Do NOT include exploit code in public reports.

## Audit History

- **2026-03-06**: Deep security audit before ClawHub publishing
  - Verified no credentials/API keys in code
  - Verified no phone numbers/emails present
  - Confirmed safe subprocess usage (no shell=True)
  - Documented external network calls
