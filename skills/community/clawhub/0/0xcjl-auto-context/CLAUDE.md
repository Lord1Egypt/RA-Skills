# Development Guide

This is an AI agent skill for context health checking.

## Project Structure
- SKILL.md - Main skill file (entry point)
- README.md - English documentation (default)
- README_zh.md - Chinese documentation
- README_ja.md - Japanese documentation
- README_es.md - Spanish documentation
- LICENSE - MIT license

## Key Conventions
- Language files are linked at the top of each README
- SKILL.md is the entry point for skill loading
- All documentation uses consistent formatting

## For Hermes Agent
- Install to: ~/.hermes/skills/auto-context/
- Manual trigger: /auto-context
- Auto-mode enabled by default

## Testing
Test the skill by calling /auto-context and verifying the health report format.
