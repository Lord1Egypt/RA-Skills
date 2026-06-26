---
name: editorial-content-strategy
description: Load reusable editorial audience and channel strategy for content production. Use when writing, rewriting, or optimizing content for a specific target reader and publication channel, especially for OpenClaw content aimed at light-technical workplace learners on WeChat public accounts or Xiaohongshu. Requires two parameters: target audience and publication channel. If either is missing, ask before proceeding.
---

# Editorial Content Strategy

## 1. Purpose

Use this skill for content creation work that needs reader positioning and channel fit, but not chief-editor orchestration.

## 2. Required parameters

Lock these before writing:
- target audience
- publication channel

If either is missing, ask first.

## 3. Loading order

### 3.1 Load audience strategy first
Read the matching file under `references/audiences/`.

### 3.2 Load channel strategy second
Read the matching file under `references/channels/`.

### 3.3 Then write or optimize
After both strategies are loaded, produce content that matches the active reader and channel.

## 4. Current direct references

Read these files directly when needed:
- `references/audiences/light-technical-workplace-learners.md`
- `references/channels/wechat-public-account.md`
- `references/channels/xiaohongshu.md`

## 5. Boundary

This skill does not cover multi-agent orchestration, assignment governance, or chief-editor acceptance flow.
It only covers:
- audience positioning
- channel-fit writing strategy
- writing depth control
- tone, structure, and packaging guidance
