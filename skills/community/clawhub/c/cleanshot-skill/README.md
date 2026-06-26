# CleanShot Skill

CleanShot Skill is an optional OpenClaw Skill for using the CleanShot Tool plugin.

It helps an OpenClaw agent choose the right CleanShot tool, capture mode, action, and workflow for screenshots, repeated regions, annotation, pinned references, scrolling capture, OCR, screen recording, CleanShot history, and troubleshooting.

## Tool Vs Skill

`openclaw-plugin-cleanshot` is the CleanShot Tool. It is the executable OpenClaw Tool Plugin that dispatches CleanShot X URL Scheme commands.

`openclaw-skill-cleanshot` is the CleanShot Skill. It does not contain executable tools and does not call CleanShot directly. It provides workflow guidance for an OpenClaw agent that already has access to the CleanShot Tool plugin.

```text
CleanShot-OpenCaw/
├─ openclaw-plugin-cleanshot/  # CleanShot Tool
└─ openclaw-skill-cleanshot/   # CleanShot Skill
```

## Requirements

- OpenClaw
- CleanShot Tool plugin installed and loaded
- macOS
- CleanShot X installed
- CleanShot X API enabled

Enable the CleanShot API in:

```text
CleanShot X -> Settings -> Advanced -> API -> Allow Applications to control CleanShot
```

## What This Skill Covers

- Default screenshot behavior
- Sending or sharing screenshots when the environment supports attachments
- Fullscreen, window, area, previous-area, and self-timer screenshots
- Repeated-region workflows
- Screenshot actions: copy, save, annotate, upload, and pin
- CleanShot All-In-One
- CleanShot Quick Access and history
- Scrolling capture
- OCR trigger workflows
- Screen recording trigger workflows
- Annotating image files
- Pinning image files as references
- Display and multi-monitor capture/recording guidance
- Troubleshooting common CleanShot Tool plugin issues

## Display And Multi-Monitor Support

CleanShot Skill can use `cleanshot_get_displays` from CleanShot Tool v1.1.0 or later.

If no display is specified, the agent should use the main display / display 1. If a display is specified, the agent should use that display.

Named regions such as left half, right half, top half, bottom half, thirds, or second-monitor regions can be calculated from display geometry. If geometry is unclear, the agent should use manual area selection.

## Publication Status

This skill is prepared as an instruction-only ClawHub/OpenClawHub skill package. It assumes the CleanShot Tool plugin is installed separately and does not include executable tools.
