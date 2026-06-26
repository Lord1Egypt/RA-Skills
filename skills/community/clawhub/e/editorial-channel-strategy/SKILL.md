---
name: editorial-channel-strategy
description: Load reusable publication-channel strategy for layout, packaging, and publication-fit decisions. Use when preparing final content for a specific publication surface such as WeChat public accounts or Xiaohongshu. If the publication channel is missing, ask before proceeding.
---

# Editorial Channel Strategy

## 1. Purpose

Use this skill for layout, packaging, and publication-fit work.
It is for agents that need channel rules without the full editorial-orchestration logic.

## 2. Required parameter

Lock the publication channel before doing final packaging or layout.
If it is missing, ask first.

## 3. Loading order

### 3.1 Identify the publication channel
Examples:
- wechat-public-account
- xiaohongshu

### 3.2 Load the matching channel strategy
Read the matching file under `references/channels/`.

### 3.3 Then perform channel-fit layout or publication preparation
Use the active channel rules to guide structure, packaging, scanability, and final checks.

## 4. Current direct references

Read these files directly when needed:
- `references/channels/wechat-public-account.md`
- `references/channels/xiaohongshu.md`
