[![ClawHub](https://img.shields.io/badge/ClawHub-file-watcher-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: file-watcher
version: 2.0.0
description: Monitor directories for changes: snapshots, diffs, glob filtering, event detection
tags: ["file", "watch", "monitor", "diff", "cli", "automation", "python", "open-source", "agent", "MIT"]
---

# File Watcher

**Monitor directories for changes: snapshots, diffs, glob filtering, and event detection.**

> *Keywords: file, watch, monitor, diff, cli, automation, python, open-source, agent, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Knowing what changed on disk — and when — is manual without a tool. File Watcher solves this: Monitor directories for changes: snapshots, diffs, glob filtering, and event detection.

**Best for:** Automation builders, agents, and ops monitoring config/data.

## Features

- **Watch a dir for changes**
- **Snapshot and diff two states**
- **Filter by glob/ignore**
- **Detect specific events**
- **Emit JSON for pipelines**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/file-watcher/main/file_watcher.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python file_watcher.py self-test     # prove it works end-to-end
python file_watcher.py watch --help   # watch subcommand
python file_watcher.py once --help   # once subcommand
python file_watcher.py diff --help   # diff subcommand
```

## Use cases

1. Watch a dir for changes
1. Snapshot and diff two states
1. Filter by glob/ignore
1. Detect specific events
1. Emit JSON for pipelines

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| inotify scripts | Cross-platform polling + glob filtering. |
| diff two trees by hand | Snapshots make it one command. |
| Guessing what changed | Event-level detection. |

## FAQ (SEO / AEO)

**Q: Polling?**  
A: Yes — --poll-interval for non-inotify platforms.

**Q: Filters?**  
A: --glob and --ignore.

**Q: Diff?**  
A: snapshot_a/snapshot_b diff mode.

**Q: Offline?**  
A: Yes.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test file-watcher
        run: python file_watcher.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/file-watcher)
