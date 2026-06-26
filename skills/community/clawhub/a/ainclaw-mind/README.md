# Workflow Cache

**One agent explores, all agents benefit.**

A crowdsourced Lobster workflow registry that caches successful automation patterns.

## Features

- **Interceptor**: Query cloud for cached workflows before LLM exploration
- **Trace Compiler**: Convert session traces to reusable Lobster workflows
- **PII Sanitizer**: Local-first privacy protection

## Hooks

- `on_intent_received` → Query cloud, replay workflow if hit
- `on_session_complete` → Compile and contribute successful sessions

## Quick Start

```bash
cd skill
npm install
npm run build
```

## Configuration

See `skill.json` for configurable options.

## License

MIT-0 — Free to use, modify, and redistribute.