# Archive Project Skill

![Version](https://img.shields.io/badge/version-1.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Organize completed projects into complete, long-term searchable archives.

## Installation

```bash
# Via ClawhHub
clawdhub install archive-project

# Via Git
git clone https://github.com/KaigeGao1110/ArchiveProject ~/.openclaw/workspace/skills/archive-project
```

## Quick Start

### Via slash command

```
//archive cureforge-hr-assessment
```

### Via natural language

Say **"archive this"** or **"can we archive this"** when a project is complete.

## What It Does

- Creates a structured project archive directory
- Collects and backs up session transcripts (from configurable path)
- Runs sanitization to redact API keys, emails, phone numbers, IPs, and hostnames
- Generates `ARCHIVE.md` with timeline, decisions, and lessons
- Updates `MEMORY.md` for future reference
- Git-commits to the internal workspace

## Archive Structure

```
workspace/projects/<project-name>/
  ARCHIVE.md
  session_transcript.jsonl
  subagent_sessions/
  deliverables/
  decisions.md
```

## Data Privacy

**Archived data never leaves the internal workspace unless you explicitly approve.**

The skill includes a sanitization script (`scripts/sanitize_transcript.py`) that redacts:
- API keys (GitHub, OpenAI, Anthropic, AWS, etc.)
- Email addresses
- Phone numbers
- IP addresses (IPv4 and IPv6)
- Internal hostnames and AWS EC2 DNS names
- Generic secrets and high-entropy tokens

## Sanitization Script

`scripts/sanitize_transcript.py` provides deterministic, audited redaction.

### Usage

```bash
# Sanitize a transcript file
python3 scripts/sanitize_transcript.py session_transcript.jsonl -o sanitized.jsonl

# Run built-in tests
python3 scripts/sanitize_transcript.py --test
```

### What it redacts

| Category | Examples | Replacement |
|----------|----------|-------------|
| GitHub tokens | `ghp_xxx`, `github_pat_xxx` | `[REDACTED-GITHUB-TOKEN]` |
| OpenAI keys | `sk-xxx`, `sk-proj-xxx` | `[REDACTED-OPENAI-KEY]` |
| Anthropic keys | `sk-ant-xxx` | `[REDACTED-ANTHROPIC-KEY]` |
| AWS credentials | `AKIAxxx`, `aws_access_key_id=xxx` | `[REDACTED]` |
| Email addresses | `user@example.com` | `[REDACTED-EMAIL]` |
| Phone numbers | `+1 555-123-4567` | `[REDACTED-PHONE]` |
| IPv4/IPv6 | `192.168.1.1`, `2001:db8::1` | `[REDACTED-IP]` |
| Internal hostnames | `ip-10-0-1-43.local` | `[REDACTED-HOSTNAME]` |
| AWS EC2 DNS | `ec2-xxx.amazonaws.com` | `[REDACTED-AWS-HOST]` |

### Properties

- **Deterministic**: same input = same output
- **Non-destructive**: original file never modified
- **Structure-preserving**: JSON/JSONL structure maintained
- **Testable**: built-in `--test` mode

## Configuration

Session transcript path is configurable via the `SESSION_TRANSCRIPT_PATH` environment variable:

```bash
export SESSION_TRANSCRIPT_PATH="/custom/path/to/sessions/"
```

**Default:** `~/.openclaw/agents/main/sessions/` (standard for all users)

**Custom:** If you have a custom session storage path (e.g., an EFS mount), set `SESSION_TRANSCRIPT_PATH` to point to it.

## For AI Agents

Install into your OpenClaw workspace skills directory.

## Language

All deliverables produced by this skill are written in **English**, regardless of client language preference.
