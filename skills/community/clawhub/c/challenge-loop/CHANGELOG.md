# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-17

### Added
- Inline challenge mode: 4-line self-refutation block (strongest objection, invalidation conditions, when alternative wins, key assumptions) — zero latency, zero cost
- Subagent challenge mode: independent challenger with 3 intensity levels (⚡Light 1 round / 🔥Standard 3 rounds / 💀Brutal 5 rounds)
- Canonical prompt template shared across all platforms
- Platform support: Hermes (`delegate_task`), OpenClaw (`sessions_spawn`), Claude Code (`Agent` tool)
- Multi-language trigger phrases (English + Chinese)
- Anti-recursion guard at prompt level
- Cost breakers (word limit, timeout, spinning detection)
- MIT-0 license
