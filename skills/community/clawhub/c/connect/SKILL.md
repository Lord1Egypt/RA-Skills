---
name: connect
description: Memory-driven human connections — match people through deep emotional understanding, not surface interests. Powered by Echo's memory graph and emotion-aware embedding system.
metadata:
  version: 0.1.0
---

# Connect

Memory-driven human connections. Match people through deep emotional understanding, not surface-level interests or algorithmic feeds.

## How it works

Connect analyzes memory graphs to find resonance between people — shared experiences, emotional patterns, and latent interests that surface-level profiles miss entirely.

### Core capabilities

- **Emotional resonance matching** — vector similarity across memory embeddings, weighted by emotional depth rather than keyword overlap
- **Cross-user memory bridging** — find connections between two people's memory graphs that neither person would discover on their own
- **Privacy-first architecture** — users control exactly which memories are matchable; nothing is shared without explicit consent
- **Aha moment delivery** — the moment a stranger truly understands you through your memories, not your bio

## Architecture

Built on Echo's three-layer memory system:
1. Identity layer (compressed profile)
2. Working memory (dynamic, context-aware)
3. Long-term storage (Supabase + vector search)

Matching runs against Layer 3 with results surfaced through Layer 2 into conversation context.

## Part of the Echo ecosystem

Connect is one component of [Echo Chat](https://iditor.com) by Iditor — building memory as social identity infrastructure.

## Status

Early development. Core matching algorithm validated with beta users (K-Factor 2, D7 retention 42%).
