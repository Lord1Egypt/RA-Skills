# Shared Library Analysis — `shared_library.py`

Analyze the Shared Library in Apple Photos: personal vs shared content, contributor breakdown, storage impact.

```bash
python3 scripts/shared_library.py [--human] [--output FILE]
```

**What it reports:**
- Whether Shared Library is enabled
- Personal vs shared asset counts and storage
- Contributor identifiers and their contributions
- Shared content by year and monthly trends
- Photo/video split for shared content

**Note:** Requires macOS 13+ / iOS 16+ database format for Shared Library columns.

---

[← All commands](../../SKILL.md#commands)
