# readme-writer

## Description
Generate a production-quality README.md from code, a short description, or an existing bad README. Adapts structure to the project type: library, CLI tool, web app, API, or data pipeline. No filler, no fluff — just the README a maintainer would actually want.

## Use when
- "write a README for this"
- "my README is bad, rewrite it"
- "generate docs for this project"
- "I need a README"
- Any project without a README, or with a placeholder/skeleton README

## Input
Provide one or more of:
- The project's source code (or key files)
- A short description of what it does
- The existing README (if rewriting)

Optionally specify:
- Project type: library / CLI / web app / REST API / data pipeline / other
- Primary language/framework
- Target audience: end users / developers / both
- License
- Whether to include badges (CI, npm, PyPI, NuGet, etc.)

## Output format

Outputs a complete, ready-to-paste `README.md` in this structure (sections omitted if not applicable):

```markdown
# [Project Name]

[One-line description — what it is and what it does]

[Badges if requested: CI status, version, license, downloads]

## Features
[3–6 bullet points — concrete capabilities, not marketing copy]

## Quick Start
[Minimal working example — copy-paste runnable in under 60 seconds]

## Installation
[Package manager commands for all relevant platforms]

## Usage
[The most common use cases with code examples]

## API Reference
[For libraries: key classes, functions, parameters, return types]
[For CLIs: flags, subcommands, environment variables]

## Configuration
[Environment variables, config file format, defaults]

## Examples
[1–3 real-world examples beyond quick start]

## Contributing
[How to run locally, run tests, submit PRs]

## License
[License name and link]
```

## Writing rules
- First line after the title: one sentence, no jargon, a 10-year-old could understand
- Quick Start must be runnable — no "replace with your actual values" placeholders unless unavoidable
- API Reference uses the actual function/class names from the code
- No phrases: "seamlessly", "powerful", "robust", "leveraging", "game-changer", "easy to use"
- If something requires setup steps, number them — don't paragraph it
- Code blocks have language tags (```python, ```bash, ```json)
- Never write "TODO" or leave blank sections — omit sections that don't apply

## Project type adaptations

### Library
Include: Features, Installation, Quick Start, API Reference, Examples, Contributing
Skip: Deployment, Environment Variables (unless it's config)

### CLI tool
Include: Installation, Usage (with all flags), Examples, Configuration
Skip: API Reference

### Web app / SaaS
Include: Features, Quick Start (local dev), Installation, Configuration (env vars), Deployment, Contributing
Skip: API Reference (unless it exposes one)

### REST API
Include: Base URL, Authentication, Endpoints (method, path, params, response), Examples
Format: Use code blocks showing curl or example request/response JSON

### Data pipeline
Include: What data flows in / out, How to run, Configuration, Output format
Skip: Contributing (unless open source)

## Self-improvement instructions
After each README generated, note what information was missing from the input that required assumptions. After 20 READMEs, surface the top 3 things developers forget to include.
