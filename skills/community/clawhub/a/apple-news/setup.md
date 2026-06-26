# Setup - Apple News (MacOS)

If `~/apple-news/` does not exist or is empty, start with transparent onboarding. Explain which local files can be created, why they help, and ask for confirmation before writing.

## Your Attitude

Be precise, calm, and local-first. Keep responses concise, confirm assumptions early, and avoid hidden automation.

## Priority Order

### 1. First: Integration Preferences

In the first exchanges, clarify activation behavior:
- Should this skill activate whenever the user asks to open Apple News or read Apple News links on macOS?
- Should it proactively enforce confirmation for multi-link opens?
- Are there contexts where shortcut-based search should stay disabled?

### 2. Then: Validate Command Path and Scope

Establish what works now:
- Whether `/System/Applications/News.app` opens successfully.
- Which path is preferred (`open`, `osascript`, or `shortcuts` fallback).
- Whether the user already has a Shortcut for topic search.
- Whether the user wants read-only opening workflows or also queue/batch workflows.

### 3. Finally: Capture Safety Defaults

If user wants persistent behavior, capture:
- Confirmation required before opening multiple links: yes/no
- Confirmation required before running search shortcuts: yes/no
- Preferred preview level before execution (brief vs detailed)

If user wants speed, keep conservative defaults and enforce explicit confirmation for high-impact opens.

## What You Are Saving Internally

Track only reusable operational context:
- Preferred command path and fallback path
- Known-good article/feed URL patterns
- Confirmation policy for multi-link opens and shortcut runs
- Known failures and proven fixes

After memory updates, summarize changes in plain language so the user can adjust immediately.
