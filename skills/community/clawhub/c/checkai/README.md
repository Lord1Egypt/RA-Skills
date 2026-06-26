<h1 align="center">Vibe Learning</h1>

<p align="center">
  <strong>Turn waiting into learning.</strong><br />
  A micro-learning knowledge feed for developers who are waiting on AI coding agents.
</p>

<p align="center">
  <img src="./vibe-learning.png" alt="Vibe Learn preview" width="960" />
</p>

<p align="center">
  <em>Context-aware knowledge cards for the moments when your agent is still working.</em>
</p>

Vibe Learn detects when a user is in a "waiting mode" and turns that idle time into a short, relevant, high-signal learning feed. Instead of staring at a terminal or chat window, users get a set of knowledge cards tailored to their current work context.

## At a glance

| Area | Details |
| --- | --- |
| Trigger | The user is waiting during an agent workflow |
| Input | Current task context from the conversation |
| Output | React artifact plus a standalone HTML page |
| Goal | Deliver 4-6 useful, adjacent learning cards fast |

## What it does

When triggered, Vibe Learn will:

1. **Understand the current task context**
   - Detect the language, framework, domain, and tools in the current conversation
   - Infer what the user is working on and their likely familiarity with the topic

2. **Find adjacent, useful knowledge**
   - Search for topics related to the current work without repeating what the user already knows
   - Mix practical tips, recent updates, deeper reads, and surprising facts

3. **Curate a micro-learning feed**
   - Select 4-6 high-quality items
   - Present them as fast, scannable knowledge cards

4. **Render the feed clearly**
   - Show cards inline as a React artifact
   - Also generate a standalone HTML page for browser viewing, bookmarking, or sharing

## Why this exists

AI coding agents often create small pockets of waiting time:

- waiting for a build
- waiting for a long codegen step
- waiting for search, retrieval, or analysis
- waiting between iterations of an agent workflow

Those moments are usually wasted.

Vibe Learn turns those gaps into micro-learning moments that are:

- relevant to what the user is already doing
- useful in practice
- short enough to consume in a few minutes
- visually polished instead of dry

## Trigger phrases

This skill activates when the user says things like:

- "I'm waiting"
- "what can I learn while waiting"
- "vibe learn"
- "feed me something"
- "knowledge cards"
- "learn something"
- "waiting mode"
- "等一下学点东西"
- "摸鱼学习"

It can also be used proactively when the user is clearly idle between coding tasks and would benefit from a short learning feed.

## Output format

Vibe Learn produces two outputs:

### 1. React artifact

An inline, visually polished micro-learning dashboard that includes:

- a context-aware header
- 4-6 knowledge cards
- type badges such as `trending`, `tip`, `deep_dive`, and `quick_fact`
- title
- short summary
- why it matters for the current task
- source name and source link
- estimated reading time

### 2. Standalone HTML page

A self-contained HTML file:

- no React dependency
- inline CSS and JS
- clickable cards
- visually consistent with the React version
- easy to open later in a browser

Default output path:

```bash
/mnt/user-data/outputs/vibe-learn-feed.html
```
