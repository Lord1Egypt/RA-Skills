---
name: aisa-twitter-research-engage-relay
description: 'Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa. Use when: the user already knows which account, tweet, or campaign to act on and needs explicit engagement workflows. Supports read context, engagement actions, and approved posting.'
author: AIsa
version: 1.0.6
license: MIT-0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# AIsa Twitter Engagement Suite

Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa. Use when: the user already knows which account, tweet, or campaign to act on and needs explicit engagement workflows. Supports read context, engagement actions, and approved posting.

## When to use

- The user already knows which tweet, account, or campaign needs action.
- The user needs explicit likes, follows, replies, or other engagement workflows after review.
- The user wants approved posting and engagement without sharing passwords.

## High-Intent Workflows

- Research the target, then like or follow with explicit approval.
- Use engagement actions as follow-through after a post or campaign review.
- Combine read context, posting, and engagement in one approved workflow.

## Quick Reference

- `python3 scripts/twitter_client.py --help`
- `python3 scripts/twitter_engagement_client.py --help`
- `python3 scripts/twitter_oauth_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Twitter/X reads, OAuth requests, and user-approved media uploads use the fixed AIsa API endpoint `https://api.aisa.one/apis/v1/twitter`.
- Provide only `AISA_API_KEY`; do not use passwords, cookies, or browser credential export.

## Example Requests

- Research a target account and like its latest tweet
- Authorize a reply or follow-up action after a launch post
- Run a reply, like, or follow workflow on a confirmed target

## Guardrails

- Do not ask for passwords, cookies, or browser credentials.
- Do not make likes, follows, replies, or uploads sound silent or automatic.
- Do not claim an engagement action succeeded until the API confirms it.
- Only upload local files the user explicitly attached, and make it clear those files are sent to AIsa's Twitter/X API endpoint.
