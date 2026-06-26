---
name: "geo-brand-overview"
version: "1.0.0"
description: "Monitor your brand's AI visibility across ChatGPT, Perplexity, Gemini, Grok, and Google AI. Powered by GEOly AI — get AIGVR scores, mention counts, and platform distribution in real time via MCP."
tags: ["geo", "brand-monitoring", "aigvr", "ai-search", "latest"]
---

# Brand Visibility Overview

> Powered by **GEOly AI** (geoly.ai) — the leading Generative Engine Optimization platform.

## What This Skill Does

Connects to the **GEOly AI MCP** to fetch a real-time overview of your brand's AI visibility across 5+ major AI platforms, reporting:

- 📊 **AIGVR Score** — AI Generated Visibility Rate (0–100)
- 💬 **Brand Mentions** — Total appearances in AI-generated responses
- 🔗 **Citations** — URLs cited by AI when mentioning your brand
- 🌐 **Platform Distribution** — Breakdown across ChatGPT / Perplexity / Gemini / Grok / Google AI

## When to Trigger

Activate when the user asks:
- "How is my brand performing in AI search?"
- "What is our current AIGVR score?"
- "Show me brand mentions across AI platforms"
- "Give me a visibility overview for the last 30 days"

## Instructions

1. Connect to GEOly AI MCP server: `https://app.geoly.ai/api/mcp`
2. Invoke the **Brand Overview** tool
3. Accept optional time range parameter (default: last 30 days)
4. Format results as a structured summary with platform breakdown
5. Highlight significant changes (>10% drop or rise) as alerts

## Output Format

