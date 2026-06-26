# Custom License Policy

Create `.license-policy.json` in the project root to define custom rules.

## Schema

```json
{
  "allowed_classifications": ["permissive", "weak-copyleft"],
  "allowed_licenses": ["MIT", "Apache-2.0", "LGPL-2.1-only"],
  "blocked_licenses": ["AGPL-3.0-only", "SSPL-1.0"],
  "exceptions": ["some-internal-package"]
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `allowed_classifications` | string[] | License categories: `permissive`, `weak-copyleft`, `strong-copyleft` |
| `allowed_licenses` | string[] | Specific SPDX IDs to allow regardless of classification |
| `blocked_licenses` | string[] | Specific SPDX IDs to always reject |
| `exceptions` | string[] | Package names to skip (pre-approved) |

## Examples

### Permissive only, with one exception
```json
{
  "allowed_classifications": ["permissive"],
  "exceptions": ["internal-gpl-lib"]
}
```

### Enterprise (no AGPL/SSPL)
```json
{
  "allowed_classifications": ["permissive", "weak-copyleft", "strong-copyleft"],
  "blocked_licenses": ["AGPL-3.0-only", "AGPL-3.0-or-later", "SSPL-1.0"]
}
```

## CI Integration

```bash
# GitHub Actions
- name: License audit
  run: python3 scripts/license_audit.py . --policy custom --ci

# GitLab CI
license-audit:
  script: python3 scripts/license_audit.py . --policy custom --ci --format json > license-report.json
  artifacts:
    paths: [license-report.json]
```
