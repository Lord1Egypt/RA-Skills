---
name: gemini-cli
description: Gemini CLI tool for building, debugging & deploying with AI. Use when querying codebases, generating apps from images/PDFs, automating workflows, or performing AI-powered code tasks from the command line.
required_binaries:
  - gemini
  - node
required_credentials:
  - gemini_api_key
metadata:
  openclaw:
    type: ai-cli-tool
    trust_model: google-api-managed
    requires:
      binaries:
        - gemini
        - node
      system_tools:
        - bash
      credentials:
        gemini_api_key: Gemini API Key from Google AI Studio or Google Cloud
    install:
      - id: gemini-cli
        package: "@google/gemini-cli"
        kind: npm
        command: npm install -g @google/gemini-cli
        required: true
      - id: node
        package: nodejs
        kind: system
        command: Usually pre-installed or via brew/apt
        required: true
    security:
      external_binary: true
      binary_name: gemini
      manages_credentials: false
      credential_storage: environment-variable
      credential_scope: local-process
    capabilities:
      - query-codebases
      - generate-from-images
      - generate-from-pdfs
      - automate-workflows
      - ai-powered-debugging
      - interactive-ai-shell
    limitations:
      - requires-internet-connection
      - requires-valid-gemini-api-key
      - rate-limited-by-google-quotas
---

# Gemini CLI Skill

A comprehensive guide for using the Gemini CLI tool to build, debug & deploy with AI directly from the command line.

## What It Does

Gemini CLI enables command-line access to Google's Gemini models for:
- **Query Codebases** — Analyze and understand large codebases
- **Generate from Images** — Create code, docs, or apps from screenshot/images
- **Generate from PDFs** — Extract and build from PDF documents
- **Automate Workflows** — Chain AI tasks for complex automation
- **Interactive Shell** — Chat with Gemini about your project
- **Debugging** — Get AI-powered debugging and code review

Perfect for developers who want to leverage AI without leaving the terminal.

## ⚠️ Trust Model & Security Declaration

**Metadata Declaration:**
- Type: AI CLI tool (Google-managed, official)
- External Binary: `gemini` (official Google package)
- Manages Credentials: No (credentials stored locally as env var)
- Credential Storage: Environment variable (GEMINI_API_KEY)
- Capabilities: Code analysis, generation, automation
- Limitations: Requires internet, API quota limits apply

**Authentication Model:**

This tool uses your **Gemini API Key** passed as an environment variable:
```bash
GEMINI_API_KEY=<your-key> gemini <command>
```

**Key Points:**
- ✅ Official Google tool (not third-party)
- ✅ Credentials stored as environment variable (not in tool)
- ✅ You control scope: set env var only when needed
- ✅ No persistent credential storage in ~/.gemini/ directory
- ✅ Direct calls to Gemini API endpoints (googleapis.com)

**What This Skill Does:**
- ✅ Queries your codebase and documents with Gemini models
- ✅ Generates code/apps from images and PDFs
- ✅ Runs automated workflows using AI
- ✅ Provides interactive debugging and code review
- ❌ Does NOT store credentials
- ❌ Does NOT cache sensitive data
- ❌ Does NOT modify your system beyond running commands

## Requirements

**Binaries (required):**
- `gemini` — Gemini CLI tool (installed via npm)
- `node` — Node.js 20.0.0+ (usually pre-installed)

**Credentials (environment variable):**
- `GEMINI_API_KEY` — Your Gemini API key from Google AI Studio or Google Cloud

**System Requirements:**
- macOS 15+, Windows 11 24H2+, or Ubuntu 20.04+
- 4GB+ RAM (casual usage), 16GB+ (power usage with large codebases)
- Internet connection required

**Optional:**
- `bash`, `zsh`, or `PowerShell` — Any modern shell

## Installation & Setup

### 1. Check Installation

Gemini CLI is usually pre-installed:
```bash
gemini --version
```

If not installed:
```bash
npm install -g @google/gemini-cli
# OR
brew install gemini-cli
```

### 2. Set API Key (One-time per session)

```bash
export GEMINI_API_KEY="<your-api-key>"
```

Or use it inline:
```bash
GEMINI_API_KEY="<your-api-key>" gemini <command>
```

To find your API key:
- Go to https://aistudio.google.com/app/apikey
- Create or copy your API key
- Store securely (don't commit to git)

### 3. Verify Installation

```bash
gemini --version
gemini --help
```

## Quick Start

### Interactive Shell (Ask Gemini Questions)

```bash
gemini chat
```

Then type your questions about code, architecture, debugging, etc.

### Query a Codebase

```bash
gemini code --prompt "What does this function do?" <file-or-directory>
```

### Generate from Image

```bash
gemini create --from-image ./screenshot.png --prompt "Create a React component from this design"
```

### Generate from PDF

```bash
gemini create --from-pdf ./document.pdf --prompt "Create an API spec based on this document"
```

### Automate a Workflow

```bash
gemini workflow --steps "1) analyze code, 2) identify issues, 3) suggest fixes"
```

### Get Help

```bash
gemini --help
gemini <command> --help
```

## Common Commands

### Interactive

```bash
gemini chat                    # Start interactive chat
gemini chat --context ./src    # Chat with codebase context
```

### Code Analysis

```bash
gemini code --prompt "analyze" ./file.js
gemini code --explain ./function.ts
gemini code --review ./pull_request.patch
```

### Code Generation

```bash
gemini create --from-image ./design.png
gemini create --from-pdf ./spec.pdf
gemini create --template react --prompt "counter app"
```

### Batch Operations

```bash
gemini batch --input ./tasks.json --output ./results.json
```

## Configuration

- **API Key:** Set via `GEMINI_API_KEY` environment variable
- **Temp Storage:** Uses system temp directory (auto-cleaned)
- **No persistent config:** Unlike mirocli, Gemini CLI doesn't store auth locally

**To persist API key across sessions (optional):**

Add to your `~/.bashrc`, `~/.zshrc`, or equivalent:
```bash
export GEMINI_API_KEY="<your-key>"
```

⚠️ **Security warning:** Only do this if your shell profile is secure and not synced to public repos.

## Global Options

```bash
--version              # Show version
--help                # Show help
--verbose             # Verbose output
--api-key <key>       # Pass API key directly (overrides env var)
--model <model>       # Specify Gemini model (default: gemini-2.5-pro)
```

## Help & Documentation

```bash
gemini --help                  # Global help
gemini <command> --help        # Command-specific help
```

**Official Docs:** https://geminicli.com/docs

## Tips & Tricks

1. **Use with your codebase:**
   ```bash
   cd /path/to/your/project
   gemini chat --context ./src
   ```

2. **Chain commands:**
   ```bash
   gemini code --review ./changes.patch | tee review.txt
   ```

3. **Batch process files:**
   ```bash
   for file in src/*.js; do
     gemini code --explain "$file" > "docs/${file}.md"
   done
   ```

4. **Store prompts in files:**
   ```bash
   cat prompt.txt | gemini chat
   ```

## When to Use Gemini CLI vs Other Tools

| Task | Gemini CLI | Cursor/IDE | Web UI |
|------|-----------|-----------|--------|
| Quick code questions | ✅ Fast | ✅ Integrated | ❌ Context switch |
| Large codebase analysis | ✅ Better | ✅ Native | ❌ Limited |
| Generate from images | ✅ Works | ✅ Works | ✅ Works |
| Batch automation | ✅ Perfect | ❌ Manual | ❌ Manual |
| Interactive chat | ✅ Terminal | ✅ IDE | ✅ Browser |
| Scripting workflows | ✅ Yes | ❌ No | ❌ No |

## Status & Next Steps

**✅ Installation:** Pre-installed (v0.28.2)

**✅ Configuration:** Ready to use with GEMINI_API_KEY environment variable

**✅ Authentication:** Set env var before use (no interactive steps needed)

**Testing:** Run `gemini --help` to verify installation

**Usage:** Set API key and start using:
```bash
export GEMINI_API_KEY="your-key-here"
gemini chat
```

---

**Setup Date:** 2026-03-14  
**Status:** Ready (no authentication required — env var based)
