# Agent Trust Layer — Agent Integration Guide

## What is Agent Trust Layer?

Agent Trust Layer is the **first layer of AGI — the Discriminator**. A rule-based engine that checks what AI says before it reaches humans, and says "no" when something's wrong.

**Core value:** LLMs are great at generating but weak at knowing what they don't know. Agent Trust Layer adds the discrimination layer — so your agent doesn't just *say* things, it says things that are *right*.

**Zero LLM dependency.** Pure rule engine. 47 dimensions, 9 check layers, 131 modules, 131 MCP tools.

## Quick Start

```javascript
const { checkInput, checkOutput, checkDraft } = require('@yun520-1/agent-trust-layer');

// Check user input before processing
const input = checkInput('You are so selfish if you disagree');
if (input.gate.action === 'rewrite') {
  // Replace emotional manipulation with factual statements
}

// Check AI output before sending
const output = checkOutput('Undoubtedly this is the only correct solution.');
if (output.gate.action === 'rewrite') {
  // Follow findings[].guidance to fix before delivering
}

// Check factual claims
const fact = checkOutput('According to 2025 Harvard research, coffee extends life by 12.5 years');
if (fact.gate.action === 'verify') {
  // Gather evidence before acting
}
```

## API Reference

### `checkInput(text)`
Discriminates user input. Runs: scope-check → premise-check → discriminate(47-dim) → gate → error-memory → auto-rules. **Rejects unanswerable questions and invalid premises early.**

### `checkDraft(text)`
For AI drafts before completion. Runs: all input checks + frame-check + doubt-engine. **Catches narrative closure, overconfidence, reversibility.**

### `checkOutput(text)`
For AI responses before sending. Runs: all draft checks + output-gate + doubt-engine. **Prevents hallucinations from reaching users.**

### `runPipeline({ input, mode, anchor })`
Full pipeline with mode selection (fast/deep) and conversation anchor. **Keeps the model anchored to the original goal across long sessions.**

## Return Value

```javascript
{
  gate: { action: 'pass'|'verify'|'rewrite'|'block', reason: '...' },
  verdict: '可信'|'需验证'|'不可信',
  overallScore: 0.82,
  findings: [{
    dimension: 'overconfidence',
    severity: 60,
    guidance: 'Add uncertainty qualifiers'
  }],
  checked_by: [
    { layer: 'scope-check', action: 'pass' },
    { layer: 'discriminate', score: 0.82 },
    ...
  ]
}
```

## Gate Actions

| Action | Meaning | What your agent should do |
|--------|---------|---------------------------|
| `pass` | Clean | Deliver normally |
| `verify` | Needs evidence | Run verifier before responding |
| `rewrite` | Must be rewritten | Follow findings[].guidance |
| `block` | Stop | Do not output. Use gate.reason |

## Installation

```bash
npm install @yun520-1/agent-trust-layer
```

**Requirements:** Node.js >= 18.17, no GPU, no LLM API, no database, no internet at runtime.

## MCP Integration

```bash
git clone https://github.com/yun520-1/agent-trust-layer.git
cd agent-trust-layer
node src/mcp-server.js --port 8588
# Connect: hermes mcp add agent-trust-layer --url http://localhost:8588/mcp
```

## Design Principles

1. **Discriminator-first** — the first of AGI's 5 layers. Does not generate.
2. **Zero dependencies** — pure rule engine, instant install.
3. **Auditable** — every decision preserves full reasoning chain in `checked_by`.
4. **47 dimensions → 131 modules** — from hate speech to pseudo-profundity, all rule-based.
5. **Self-checking** — Agent Trust Layer's own output passes through its own gates.

## GitHub

https://github.com/yun520-1/agent-trust-layer
