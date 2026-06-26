---
name: clawpolicy
description: Install and use ClawPolicy, an explainable autonomous execution policy engine for low-touch, auditable agent execution. Supports initialization, policy supervision, status checks, risky/suspended inspection, and Python API usage.
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3", "pip3"] },
      "install": [
        {
          "id": "pip",
          "kind": "python",
          "package": "clawpolicy",
          "bins": ["clawpolicy"],
          "label": "Install clawpolicy from PyPI"
        }
      ]
    }
  }
---

# ClawPolicy

ClawPolicy is an explainable autonomous execution policy engine for low-touch, auditable agent execution.

## What it does

- Initializes canonical local policy storage in `.clawpolicy/policy/`
- Tracks policy lifecycle: `hint -> candidate -> confirmed -> suspended -> archived`
- Exposes a supervision CLI: `clawpolicy policy ...`
- Provides a stable Python API for confirmation, policy storage, and Markdown conversion/export

## Install

```bash
python3 -m pip install clawpolicy
```

Optional extras:

```bash
python3 -m pip install "clawpolicy[phase3]"
```

## Quick start

```bash
clawpolicy init
clawpolicy analyze
clawpolicy policy status
clawpolicy policy recent
clawpolicy policy risky
clawpolicy policy suspended
```

## Verification

The published package should pass this minimal smoke path:

```bash
python3 -m pip install clawpolicy
clawpolicy --help
clawpolicy init
clawpolicy policy status
python -m clawpolicy policy status
```

## Python API

```python
from clawpolicy import (
    ConfirmationAPI,
    PolicyEvent,
    PolicyStore,
    Playbook,
    Rule,
    MarkdownToPolicyConverter,
    PolicyToMarkdownExporter,
    create_api,
)
```

## References

- Upstream repo: `https://github.com/DZMing/clawpolicy`
- Chinese README: `references/upstream-README.zh-CN.md`
- English README: `references/upstream-README.md`
- Changelog: `references/upstream-CHANGELOG.md`
- Security policy: `references/upstream-SECURITY.md`

## Notes

- This ClawHub package is a skill wrapper for the public `clawpolicy` project.
- Canonical source code, releases, and issue tracking remain in the upstream GitHub repository.
