---
name: claw-test-skill
description: Test skill created and published directly via ClawHub API using provided key. Use when testing ClawHub publish flow from agents or Grok.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env: []
    emoji: "🧪"
---

# Claw Test Skill

Simple test skill for validating ClawHub publish with raw API key.

## When to use

- User or agent wants to verify ClawHub skill publishing works.
- Confirm a new skill version is live on ClawHub.

## Steps

1. Confirm the skill loaded from ClawHub registry.
2. Greet and report success: "ClawHub publish via API key succeeded."
3. Suggest next: run `openclaw skills install claw-test-skill` or `clawhub install claw-test-skill`.

## ClawHub-safe policy

- This skill performs no actions, no side effects, no credentials, no onchain calls.
- Safe for any environment.
- No user data collection.

## Notes

Published using the clh_ API key directly against ClawHub registry.
Initial test publish.