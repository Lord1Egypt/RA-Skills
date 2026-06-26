# Elite Human Memory — Hermes Optimized

A human-like, selective memory system for Hermes agents that combines semantic search, auto-promotion heuristics, conflict detection, and direct integration with the built-in Hermes `memory` tool.

This is the Hermes-tuned version (v2.0.0) of the Elite Human Memory skill. It keeps the philosophical, contextual, and low-noise approach of the original while taking full advantage of Hermes’ vector capabilities and tool ecosystem.

## Features

- **Layered Memory Architecture** — Working, Episodic, Semantic, and Vector layers
- **Semantic Search** — Vector embeddings over `MEMORY.md` and daily files for high-quality retrieval
- **Auto-Promotion** — Weighted heuristics that propose promotion of important memories while keeping the user in control
- **Conflict Detection & Resolution** — Automatic detection of contradictory memories with logging and resolution workflow
- **Metadata-Rich Context** — Every memory carries timestamp, scope, confidence, source, and relational links
- **Hermes-Native Integration** — Works alongside (not instead of) the built-in `memory` tool

## Quick Start

1. Place the skill in your Hermes skills directory.
2. The agent will automatically begin using semantic search + metadata filtering when the user references past decisions, preferences, or context.
3. Use explicit “remember this” instructions or let the agent detect strong signals for promotion.

See `INTEGRATION.md` for Hermes-specific setup and usage patterns.

## Version

**2.0.0** (Hermes Optimized) — May 2026

**Status:** Ready for local use and marketplace publishing.