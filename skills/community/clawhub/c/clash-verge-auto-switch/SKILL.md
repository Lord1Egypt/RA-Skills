---
name: clash-verge-auto-switch
description: Use when the user wants Codex to speed test Clash Verge Rev or Mihomo proxies, auto-detect currently used Clash groups from the live controller, switch a selector group to the fastest working node, diagnose controller connectivity, or install a macOS launchd job with a user-chosen interval.
---

# Clash Verge Auto Switch

This skill gives Codex a reliable workflow for Clash Verge Rev and Mihomo proxy switching on macOS. It is meant for users who want a concrete node selected from a selector group, not just a passive health check.

## When To Use It

Use this skill when the user asks to:

- speed test Clash Verge or Mihomo nodes
- switch the currently used Clash selector groups to the fastest node
- diagnose why the Clash controller cannot be reached
- install or remove a timed automatic switch job on macOS

## Quick Start

Run the main script:

```bash
/usr/bin/python3 ~/.codex/skills/clash-verge-auto-switch/scripts/switch_fastest.py
```

By default it auto-discovers the current active selector chain from the live Clash controller. To inspect what it found:

```bash
/usr/bin/python3 ~/.codex/skills/clash-verge-auto-switch/scripts/switch_fastest.py --list-groups
```

Target explicit groups:

```bash
/usr/bin/python3 ~/.codex/skills/clash-verge-auto-switch/scripts/switch_fastest.py \
  --group 'Proxy' \
  --group 'ChatGPT'
```

Dry-run without changing selections:

```bash
/usr/bin/python3 ~/.codex/skills/clash-verge-auto-switch/scripts/switch_fastest.py --dry-run
```

## Workflow

1. Check whether the Mihomo controller is reachable.
2. If the user did not name target groups, inspect the live `/proxies` tree and auto-discover groups from the current active selection chain.
3. Expand `url-test`, `fallback`, and `load-balance` groups into leaf proxies, but do not rewrite nested selector groups unless the user explicitly targets them.
4. Test candidate proxies with the controller delay API and switch the selector group to the lowest-latency healthy node.
5. Report the winning node, measured latency, and whether a switch happened.

## Group Discovery

- Default mode is `--group-scope current`, which follows the currently selected chain from the live Clash proxy tree.
- Use `--group-scope top-level` when you want all top-level selector groups discovered from the current controller session.
- Use `--group-scope all` when you want every selector group in the current Clash instance.
- Use explicit `--group` flags when the user wants exact control.

## Scheduling

For a true custom-minute schedule on macOS, use the bundled `launchd` installer instead of Codex automations because Codex recurring schedules only support hourly intervals.

Install:

```bash
~/.codex/skills/clash-verge-auto-switch/scripts/install_launch_agent.sh \
  --interval-minutes 30 \
  --group-scope current
```

Remove:

```bash
~/.codex/skills/clash-verge-auto-switch/scripts/uninstall_launch_agent.sh
```

## Notes

- Read [runtime-notes.md](./references/runtime-notes.md) when you need the generic controller discovery and group-detection rules.
- If the controller is offline, ask the user whether Clash Verge should be opened first or run the script with `--launch-if-needed`.
