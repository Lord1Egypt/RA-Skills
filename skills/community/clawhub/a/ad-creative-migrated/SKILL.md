---
name: ad-creative
description: Skill migrada desde examples - ad-creative con capacidades completas
version: 1.0.0 (migrated from examples)
tags: [migrated, ad,creative, examples]
color: Purple
---

# ad-creative (Migrated)

## Overview

Esta skill ha sido migrada desde `./examples` y mejorada para Qwen Code.





## Usage Examples

### Example 1: Basic Usage

```javascript
const skill = require('~/.opencode/skills/ad-creative');
const result = await skill.execute();
```

### Example 2: Advanced Usage

```javascript
const { OptimizedSubagent } = require('~/.opencode/skills/subagente-optimizado');

const agent = new OptimizedSubagent({
    taskName: 'ad-creative task',
    taskType: 'ad',
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
const skill = bs.searchByName('ad-creative');
```

### Exa Search

```javascript
const search = require('~/.opencode/skills/exa-search');
const results = await search.searchWeb('ad-creative best practices 2026');
```

## Optimization

Esta skill usa las optimizaciones de quota:
- Context compression (650 tokens vs 10K)
- Tool restriction (3-4 tools max)
- Iteration limits (3 max)
- Result caching (TTL: 1h)

## References

- Source: `./examples/claude-skills-main/.gemini/skills/ad-creative`
- Migrated: 2026-03-29
