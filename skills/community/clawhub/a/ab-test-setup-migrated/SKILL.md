---
name: ab-test-setup
description: Skill migrada desde examples - ab-test-setup con capacidades completas
version: 1.0.0 (migrated from examples)
tags: [migrated, ab,test,setup, examples]
color: Yellow
---

# ab-test-setup (Migrated)

## Overview

Esta skill ha sido migrada desde `./examples` y mejorada para Qwen Code.





## Usage Examples

### Example 1: Basic Usage

```javascript
const skill = require('~/.opencode/skills/ab-test-setup');
const result = await skill.execute();
```

### Example 2: Advanced Usage

```javascript
const { OptimizedSubagent } = require('~/.opencode/skills/subagente-optimizado');

const agent = new OptimizedSubagent({
    taskName: 'ab-test-setup task',
    taskType: 'ab',
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
const skill = bs.searchByName('ab-test-setup');
```

### Exa Search

```javascript
const search = require('~/.opencode/skills/exa-search');
const results = await search.searchWeb('ab-test-setup best practices 2026');
```

## Optimization

Esta skill usa las optimizaciones de quota:
- Context compression (650 tokens vs 10K)
- Tool restriction (3-4 tools max)
- Iteration limits (3 max)
- Result caching (TTL: 1h)

## References

- Source: `./examples/claude-skills-main/.gemini/skills/ab-test-setup`
- Migrated: 2026-03-29
