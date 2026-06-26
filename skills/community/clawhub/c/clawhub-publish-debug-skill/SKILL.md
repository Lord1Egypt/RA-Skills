---
name: clawhub-publish-debug-skill
description: A minimal but concrete diagnostic skill used to verify whether ClawHub publish and install return the same SKILL.md content.
---

# ClawHub Publish Debug Skill

This skill exists only to verify that a freshly published SKILL.md is the same content later returned by ClawHub install/update.

## Expected verification marker

`debug-marker: 2026-04-01-a`

## How to verify

After installing this skill from ClawHub, open the installed `SKILL.md` and confirm that:

- the description mentions publish/install consistency
- the expected verification marker is exactly `2026-04-01-a`
- this file contains the phrase `freshly published skill content`

If any of those checks fail, the installed content does not match the published content.

## Why this exists

This is not a production skill. It is a controlled fixture for diagnosing possible stale content, cache mismatch, or registry/install inconsistencies in the ClawHub publish pipeline.

The expected phrase is: freshly published skill content.
