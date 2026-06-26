---
name: skill-discovery
description: >
  Automatically discover, search, and install skills from ClawHub — the public skill registry for OpenClaw —
  when no locally installed skill can fulfill the user's request. Acts as a "skill gap filler": when the agent
  encounters a task it cannot handle with existing skills or built-in tools, it searches ClawHub for a matching
  skill, presents options to the user, and installs their choice with one command.

  Use when: (1) the user asks for a capability that no installed skill can fulfill,
  (2) the user explicitly says "find a skill", "search for a skill", "is there a skill for X",
  "install a skill from ClawHub", or "search ClawHub",
  (3) the agent determines that a specialized ClawHub skill would handle the task better than
  general-purpose reasoning or existing tools,
  (4) the user asks "what skills are available for X" or "can OpenClaw do X".

  Triggers on phrases like: "find a skill", "search skills", "install a skill", "search ClawHub",
  "is there a plugin for", "can you do X", "I need a tool for", "有没有能做X的技能",
  "帮我找个技能", "搜一下技能", "装个技能". Also activates when no available_skills entry
  matches the user's intent and the task is clearly skill-shaped (domain-specific workflow,
  specialized integration, or multi-step procedure).
---

# Skill Discovery

Automatically search ClawHub for skills that match the user's needs and offer to install them.

## When to Activate

- No local skill matches the user's request
- User explicitly asks to find or install a skill
- Agent determines a specialized skill would handle the task better than general-purpose reasoning

## Workflow

### 1. Identify the Need

Extract 1-3 concise search keywords from the user's request. Focus on the core capability, not the full sentence.

Examples:
- "帮我管理 Docker 容器" → `docker`
- "I need to process CSV files" → `csv`
- "能不能帮我发邮件" → `email`

### 2. Search ClawHub

```bash
openclaw skills search "<keywords>"
```

If no results, try alternative keywords or broader terms.

### 3. Present Results

Show the user what was found in a concise list:
- Skill name / slug
- Brief description
- Relevance to their request

If nothing relevant is found, tell the user honestly and suggest they could create one or check [clawhub.ai](https://clawhub.ai) manually.

### 4. Install (with user confirmation)

**Always ask the user before installing.** Never auto-install.

```bash
openclaw skills install <slug>
```

After install, inform the user:
- The skill is installed
- They need to **start a new session** (or the agent needs a restart) for the skill to take effect
- Alternatively, they can read the new SKILL.md immediately to use it in the current session

### 5. Immediate Use (optional)

If the user wants to use the skill right away in the current session:

1. Read the newly installed skill's SKILL.md
2. Follow its instructions to handle the original request

## Guidelines

- **Don't over-search**: Only trigger when there's a genuine gap. If the task can be done with existing tools (exec, read, web_fetch, etc.), just do it.
- **Be specific**: Use precise keywords. "weather" not "get the current weather forecast for my city".
- **Respect the user**: Always confirm before installing. Show what you found, let them decide.
- **One at a time**: Search and install one skill per request. Don't bulk-install.
