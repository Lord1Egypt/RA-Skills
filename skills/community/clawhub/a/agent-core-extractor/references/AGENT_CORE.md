# Agent Core Design

This document is for AI systems reading an exported pack.

## Definition

`agent core` means the smallest source-only set of files that defines how an agent behaves.

It includes only the parts that control:

- identity
- instructions
- context loading
- runtime defaults
- tool and permission boundaries
- subagent or role definitions
- prompt composition

It excludes unrelated implementation details.

## Core Components

### 1. Identity Layer

This defines who the agent is.

Examples:

- `AGENTS.md`
- `CLAUDE.md`
- `SOUL.md`
- `IDENTITY.md`
- manifest descriptions

Responsibility:

- personality
- role
- values
- operator relationship

### 2. Instruction Layer

This defines durable behavior rules.

Examples:

- top-level instruction markdown
- built-in prompt templates
- role prompt text

Responsibility:

- how the agent should act
- collaboration style
- safety posture
- communication style

### 3. Context Layer

This defines what persistent context is loaded into the agent.

Examples:

- `USER.md`
- `MEMORY.md`
- `HEARTBEAT.md`
- workspace templates
- prompt-builder file order

Responsibility:

- bootstrap files
- memory sources
- heartbeat/task context
- injection order

### 4. Runtime Layer

This defines how the agent runtime is configured.

Examples:

- config schemas
- config examples
- config loaders
- runtime config docs

Responsibility:

- model/provider defaults
- config path and format
- channels
- MCP
- hooks
- cron

### 5. Capability Layer

This defines what the agent is allowed to do.

Examples:

- tool allowlists
- shell patterns
- workspace restrictions
- network restrictions
- approval rules

Responsibility:

- tools
- permissions
- safety boundaries
- external-action gating

### 6. Multi-Agent Layer

This defines subagents, built-in roles, or manifests.

Examples:

- `agents/*/agent.toml`
- built-in role `.toml` files
- delegate agent config

Responsibility:

- available roles
- per-role prompts
- per-role tools
- per-role limits

### 7. Composition Layer

This defines how the final prompt or runtime identity is assembled.

Examples:

- `prompt.rs`
- `prompt.zig`
- prompt markdown templates

Responsibility:

- assembly order
- static sections
- dynamic sections
- file injection strategy

## Framework Detection

AgentPearl detects framework type before extraction.

Current supported framework signatures:

- `nanoclaw-ts-bootstrap`
- `nanobot-py-templates`
- `nullclaw-zig-bootstrap`
- `zeroclaw-rs-config-prompt`
- `openfang-rs-manifests`
- `codex-rs-builtins`

## Extraction Principle

Extraction is source-only.

AgentPearl copies files that directly define the layers above and ignores:

- tests
- build outputs
- dependency directories
- unrelated application code
- migration or target-framework metadata

## How To Read An Exported Pack

When consuming a pack:

1. Identify the project and detected framework from `MANIFEST.txt`.
2. Read identity and instruction files first.
3. Read config and prompt-composition files next.
4. Read multi-agent manifests if present.
5. Treat the pack as raw source material, not as an interpreted migration result.
