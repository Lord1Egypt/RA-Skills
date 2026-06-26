---
name: cuihua-config-validator
description: AI-powered configuration validator. Automatically validate JSON/YAML configs, detect conflicts, and suggest best practices.
metadata:
  openclaw:
    requires: {bins: [node], env: []}
  version: "1.0.0"
  author: "翠花 (Cuihua) - ClawHub Pioneer"
  license: "MIT"
  tags: [config, validation, json, yaml, best-practices]
---

# cuihua-config-validator ⚙️

> **Validate configs with AI-powered insights**

## Features
- JSON/YAML validation
- Environment variable checks
- Conflict detection
- Best practices

## Quick Start
> "Validate package.json"
> "Check .env file"

## Install
\`\`\`bash
clawhub install cuihua-config-validator
\`\`\`

MIT | 🌸 Cuihua

## What It Does

Validates configuration files and catches common mistakes:

### JSON Validation
- Syntax errors
- Missing commas
- Trailing commas
- Invalid escape sequences

### Environment Variables
- Missing required vars
- Typos in variable names
- Unused variables
- Security risks (hardcoded secrets)

### Best Practices
- Naming conventions
- Structure recommendations
- Performance tips
- Security guidelines

## Examples

**Input:**
```json
{
  "name": "my-app"
  "version": "1.0.0"
}
```

**Output:**
```
❌ Syntax error (line 2): Missing comma after "my-app"
```

**Fix:**
```json
{
  "name": "my-app",
  "version": "1.0.0"
}
```

## Supported Formats
- package.json
- tsconfig.json
- .env files
- docker-compose.yml
- Custom JSON/YAML

Full docs: https://clawhub.ai/skills/cuihua-config-validator
