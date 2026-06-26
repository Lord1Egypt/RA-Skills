# create-skill

Create a new skill through an interactive CLI-style flow.

## Philosophy

A skill should define **behavior**, not just store documentation.

- A good skill tells the agent **when** to use it
- A good skill tells the agent **what tools** to use  
- A good skill defines the **workflow**
- A good skill specifies the **expected output**
- A good skill knows its **constraints**

Static documentation has little value - the agent can fetch that itself. The skill's value is in **encoding the behavior pattern**.

## Quick Start

```
You: Help me create a skill
Agent: Create a new skill.

1) Quick guidance
2) Full guidance

Choice [1]:
```

## Flow

1. Choose guidance mode
2. Define the task (what problem to solve)
3. Define trigger conditions (when to use)
4. Define required tools
5. Define workflow (step by step)
6. Define expected output
7. Define constraints
8. (Optional) Fetch docs and analyze
9. Confirm and create

## Key Change

The skill now focuses on **behavior extraction**, not documentation storage.

When you provide a documentation URL:
1. It fetches the content
2. **Analyzes and extracts behavioral patterns**
3. Generates a skill that tells the agent:
   - When to trigger
   - What tools to use
   - The exact workflow
   - Expected output
   - Constraints

## Output

Creates:
- `SKILL.md` - Behavioral definition (not static docs)
- `README.md` - Human-readable usage guide

## Compatible Agents

Works with any AgentSkills-compatible agent:
- OpenClaw
- Claude Code
- Codex
- Pi
