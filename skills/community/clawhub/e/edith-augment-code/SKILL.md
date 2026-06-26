---
name: edith-augment-code
description: Use Augment Code (Auggie CLI) to analyze, generate, and modify code through Edith smart glasses or OpenClaw. Triggers when the user asks to build, code, debug, analyze, or prototype something.
user-invocable: true
---

# Augment Code via Auggie CLI

Use Augment Code's powerful context engine and agentic coding capabilities through OpenClaw. This skill wraps the `auggie` CLI to let users generate code, analyze projects, debug issues, and build prototypes — hands-free through Edith glasses or any OpenClaw channel.

## Prerequisites

- Auggie CLI installed: `npm install -g @augmentcode/auggie`
- Logged in: `auggie login`

## When to use

Trigger this skill when the user asks to:
- Build, create, or scaffold something ("build me a landing page", "create a REST API")
- Analyze or review code ("analyze this codebase", "review this function")
- Debug or fix issues ("why is this failing", "fix the auth bug")
- Prototype or generate code ("prototype a todo app", "generate a React component")
- Get code suggestions or insights ("how should I structure this", "what's wrong with this approach")

## How to use

### Generate code or build something

Run auggie in print mode for one-shot tasks:

```bash
auggie --print "Build a simple Express API with /health and /users endpoints" 2>&1
```

### Analyze the current project

```bash
auggie --print "Analyze this codebase and give me a summary of the architecture" 2>&1
```

### Debug an issue

```bash
auggie --print "Look at the recent error in src/ws-relay.ts and suggest a fix" 2>&1
```

### Get quiet/structured output

For clean responses without step details:

```bash
auggie --print --quiet "What dependencies does this project use and are any outdated?" 2>&1
```

## Response formatting

When returning results to the user (especially through Edith glasses voice output):
- Summarize the key output concisely
- For code generation: describe what was created and where
- For analysis: give the top 3-5 findings
- For debugging: state the root cause and fix
- Keep it conversational and brief — this may be spoken aloud through glasses

## Error handling

- If `auggie` is not installed: tell the user to run `npm install -g @augmentcode/auggie`
- If not logged in: tell the user to run `auggie login`
- If the command times out: suggest breaking the task into smaller pieces
- Auggie may take 10-30 seconds for complex tasks — warn the user if it's a big request
