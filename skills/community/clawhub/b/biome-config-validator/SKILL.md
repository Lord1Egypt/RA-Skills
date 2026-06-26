---
name: biome-config-validator
description: Validate and lint Biome (biome.json) configuration files for structure, rule conflicts, deprecated options, and best practices. 22 rules across structure, linting, formatting, and compatibility categories.
---

# Biome Config Validator

Validate `biome.json` configuration files for correctness, conflicts, deprecated options, and best practices.

## Commands

```bash
# Validate a biome.json file (all rules)
python3 scripts/biome_config_validator.py lint biome.json

# Check for rule conflicts only
python3 scripts/biome_config_validator.py conflicts biome.json

# Check for deprecated options
python3 scripts/biome_config_validator.py deprecated biome.json

# Validate structure only
python3 scripts/biome_config_validator.py validate biome.json

# JSON output
python3 scripts/biome_config_validator.py lint biome.json --format json

# Summary only
python3 scripts/biome_config_validator.py lint biome.json --format summary
```

## Rules (22)

### Structure (5)
- Invalid JSON syntax
- Unknown top-level keys
- Invalid schema version ($schema URL)
- Missing recommended sections (linter, formatter)
- Invalid file patterns in includes/excludes

### Linting (7)
- Unknown lint rule names
- Rules in wrong category
- Conflicting rules (e.g., useConst vs noConst)
- Disabled recommended rules without justification
- Invalid rule severity values
- Empty rule groups
- Deprecated rule names

### Formatting (5)
- Invalid indent style/width combination
- Conflicting formatter settings
- Line width out of reasonable range
- Invalid quote style values
- Tab width mismatch with indent width

### Best Practices (5)
- Missing VCS integration settings
- Overly broad ignore patterns
- No organizeImports configuration
- Missing JavaScript/TypeScript specific settings
- Extends pointing to non-existent config

## Output Formats

- **text** (default): Human-readable with colors and severity icons
- **json**: Machine-readable with file, rule, severity, message
- **summary**: Counts by severity only

## Exit Codes

- 0: No issues (or warnings only)
- 1: Errors found
- 2: Invalid input
