---
name: agent-designer
description: Skill migrada desde examples - agent-designer con capacidades completas
version: 1.0.0 (migrated from examples)
tags: [migrated, agent,designer, examples]
color: Cyan
---

# agent-designer (Migrated)

## Overview

Esta skill ha sido migrada desde `./examples` y mejorada para Qwen Code.





## Usage Examples

### Example 1: Basic Usage

```javascript
const skill = require('~/.opencode/skills/agent-designer');
const result = await skill.execute();
```

### Example 2: Advanced Usage

```javascript
const { OptimizedSubagent } = require('~/.opencode/skills/subagente-optimizado');

const agent = new OptimizedSubagent({
    taskName: 'agent-designer task',
    taskType: 'agent',
    context: { userGoal: 'Objective' }
});

const result = await agent.execute(async ({ context, tools }) => {
    // Implementation
});
```

## Integration

### Buscador de Skills

```javascript
const bs = require('~/.opencode/skills/buscador_de_skills');
const skill = bs.searchByName('agent-designer');
```

### Exa Search

```javascript
const search = require('~/.opencode/skills/exa-search');
const results = await search.searchWeb('agent-designer best practices 2026');
```

## Optimization

Esta skill usa las optimizaciones de quota:
- Context compression (650 tokens vs 10K)
- Tool restriction (3-4 tools max)
- Iteration limits (3 max)
- Result caching (TTL: 1h)

## References

- Source: `./examples/claude-skills-main/.gemini/skills/agent-designer`
- Migrated: 2026-03-29
