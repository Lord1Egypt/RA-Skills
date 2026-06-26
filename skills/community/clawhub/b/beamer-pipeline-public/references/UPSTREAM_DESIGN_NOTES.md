# Upstream Design Notes

This public skill is derived from a private local Beamer workflow, but the private runtime implementation is intentionally excluded from this package.

The public package keeps only the reusable, local-first Beamer contract and helper scripts:

- seven-phase Beamer generation shape
- prompt/workspace scaffolding
- local asset preparation for Markdown image references
- local validation helpers for slide/equation/acceptance contracts

The following private implementation layers are not included:

- Telegram or slash-command adapters
- private OpenClaw task queues or SQLite task databases
- private agent session recovery code
- local machine paths and launchd worker configuration
- private logs, caches, PDFs, generated decks, or user-specific state

If you need to connect this skill to an agent runtime, use the documented `--agent-cmd` hook and provide your own command in your own environment.
