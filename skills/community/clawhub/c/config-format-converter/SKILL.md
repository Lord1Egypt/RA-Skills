---
name: config-format-converter
description: Convert and validate configuration files between JSON, YAML, and TOML formats. Use when working with config files that need format conversion, syntax validation, or pretty-printing. Supports package.json, pyproject.toml, .yaml/.yml configs, and any structured data files. Ideal for cross-platform project setup, CI/CD config migration, and developer tooling workflows.
---

# Config Format Converter

Universal configuration file format converter for JSON, YAML, and TOML.

## When to Use

- Converting `package.json` to `pyproject.toml` or vice versa
- Migrating CI/CD configs between formats (`.yaml` ↔ `.json`)
- Normalizing config files for cross-platform projects
- Validating syntax before committing config changes
- Pretty-printing minified config files

## Supported Formats

| Format | Extensions | Use Cases |
|--------|-----------|-----------|
| JSON | `.json` | npm, Node.js, VS Code settings |
| YAML | `.yaml`, `.yml` | Docker Compose, GitHub Actions, Kubernetes |
| TOML | `.toml` | Python Poetry, Rust Cargo, Go modules |

## Quick Start

### Convert Between Formats

```python
import json
import yaml
import toml

# JSON to YAML
with open('package.json') as f:
    data = json.load(f)
with open('package.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# YAML to JSON
with open('docker-compose.yaml') as f:
    data = yaml.safe_load(f)
with open('docker-compose.json', 'w') as f:
    json.dump(data, f, indent=2)

# TOML to JSON
with open('pyproject.toml') as f:
    data = toml.load(f)
with open('pyproject.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Validate Config Syntax

```python
import json
import yaml

def validate_json(filepath):
    try:
        with open(filepath) as f:
            json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, str(e)

def validate_yaml(filepath):
    try:
        with open(filepath) as f:
            yaml.safe_load(f)
        return True, "Valid YAML"
    except yaml.YAMLError as e:
        return False, str(e)
```

### Pretty-Print Configs

```python
import json

# Compact to pretty JSON
with open('config.min.json') as f:
    data = json.load(f)
with open('config.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## Common Workflows

### Migrate npm Project to Python Poetry

```python
import json
import toml

# Read package.json
with open('package.json') as f:
    pkg = json.load(f)

# Create pyproject.toml structure
pyproject = {
    'tool': {
        'poetry': {
            'name': pkg.get('name', ''),
            'version': pkg.get('version', '0.1.0'),
            'description': pkg.get('description', ''),
            'authors': [],
            'dependencies': {}
        }
    }
}

# Write TOML
with open('pyproject.toml', 'w') as f:
    toml.dump(pyproject, f)
```

### Convert Docker Compose YAML to JSON for CI

```python
import yaml
import json

with open('docker-compose.yaml') as f:
    compose = yaml.safe_load(f)

with open('docker-compose.json', 'w') as f:
    json.dump(compose, f, indent=2)
```

## Best Practices

- **Preserve comments**: YAML/TOML comments are lost in conversion; document important notes separately
- **Key ordering**: Use `sort_keys=False` to preserve original key order
- **Unicode**: Always use `ensure_ascii=False` for international configs
- **Validation**: Always validate output after conversion
- **Backup**: Keep original files before bulk conversion

## Error Handling

Common issues and solutions:

| Issue | Cause | Fix |
|-------|-------|-----|
| `ScannerError` | Invalid YAML syntax | Check indentation (spaces, not tabs) |
| `TomlDecodeError` | Invalid TOML syntax | Verify section headers `[section]` |
| `JSONDecodeError` | Trailing commas in JSON | Remove commas before `}` or `]` |
| Unicode errors | Encoding mismatch | Open files with `encoding='utf-8'` |

## Dependencies

```bash
pip install pyyaml toml
```
