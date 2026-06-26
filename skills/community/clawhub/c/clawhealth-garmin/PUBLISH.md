# Release Checklist

## 0. Confirm manifest.yaml

This skill is distributed with a manifest for ClawHub publishing.
Update version and metadata before release:

```bash
type {baseDir}/manifest.yaml
```

## 0.1 Verify source fetch (optional)
```bash
python {baseDir}/fetch_src.py --help
```

## 1. Prerequisites
- OpenClaw installed
- Python 3.10+
- Optional: network access to install Python deps (unless using a prepatched image)

## 2. Validate
```bash
python {baseDir}/validate_skill.py
```

## 3. Minimal Tests
```bash
python {baseDir}/test_minimal.py
```

## 4. Optional Integration Test (real account)
```bash
python {baseDir}/test_integration_optional.py
```

## 5. Bootstrap Dependencies (if needed)
```bash
python {baseDir}/bootstrap_deps.py
```

## 6. Release Notes
Use `RELEASE_TEMPLATE.md` at repo root.

## 7. Optional: Package the skill folder
If you want a single artifact for distribution, zip this folder (`{baseDir}/`) and share the zip.
