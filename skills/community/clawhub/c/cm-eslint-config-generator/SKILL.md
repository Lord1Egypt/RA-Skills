---
name: eslint-config-generator
description: Generate optimal ESLint configurations based on project type, framework, and team preferences — flat config format, plugin selection, and rule tuning.
metadata:
  tags: ["eslint", "javascript", "typescript", "linting", "code-quality"]
---

# ESLint Config Generator

Generate optimal ESLint flat configurations based on project analysis. Detects framework, TypeScript usage, and coding patterns to recommend plugins, rules, and presets. Handles migration from legacy .eslintrc to flat config format.

## Usage

```
"Generate ESLint config for my project"
"Migrate my .eslintrc to flat config"
"Recommend ESLint plugins for my React TypeScript project"
"Audit my ESLint rules for conflicts"
```

## How It Works

### 1. Project Analysis

```bash
cat package.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
for fw in ['react','vue','svelte','angular','next','nuxt','astro','express','fastify']:
    if fw in deps: print(f'Framework: {fw}')
if 'typescript' in deps: print('TypeScript: yes')
for plugin in [k for k in deps if 'eslint' in k.lower()]:
    print(f'ESLint plugin: {plugin}')
"
```

### 2. Configuration Generation

Based on detected project type, generate flat config with:
- Language parser (TypeScript, JSX, Vue SFC)
- Framework-specific plugins and rules
- Import sorting and validation
- Accessibility rules for UI frameworks
- Testing library rules if test framework detected
- Prettier compatibility (if Prettier is used)

### 3. Rule Optimization

- Remove conflicting rules
- Tune strictness level (recommended → strict → custom)
- Add project-specific ignores
- Configure globals and environments
- Set up overrides for test files and config files

### 4. Migration Support

Convert legacy .eslintrc.json/.eslintrc.js to flat config:
- Map extends to imports
- Convert overrides to config array entries
- Update plugin references to new format
- Handle env/globals changes

## Output

```
## ESLint Configuration Generated

**Project:** React + TypeScript + Vitest
**Format:** Flat config (eslint.config.mjs)

### Generated Config
- TypeScript parser with type-aware linting
- React plugin with hooks rules
- Import plugin with TypeScript resolver
- Vitest plugin for test files
- Prettier compatibility (no conflicting rules)

### Plugin Recommendations
✅ @typescript-eslint — type-aware linting
✅ eslint-plugin-react — React best practices
✅ eslint-plugin-react-hooks — hooks rules
✅ eslint-plugin-import-x — import order + validation
🟡 eslint-plugin-jsx-a11y — accessibility (recommended)
```
