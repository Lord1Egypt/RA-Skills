---
name: deduplicator
description: 过滤重复的内容和链接，在会话范围内跳过重复项。当需要处理列表数据（如搜索结果、个人资料列表）时使用此技能，可自动检测并跳过重复的内容或链接。支持通过 '重置去重' 命令清除记录，以便开始新的去重会话。
---

# Deduplicator

## Overview

This skill provides logic to filter out duplicate content and links within a session. It helps keep lists (such as search results or profile lists) unique by skipping items that have already been seen.

## How It Works

The deduplicator skill tracks content and links that have been processed within the current session. When a new item (such as a profile entry, search result, or link) is presented, the skill checks whether it has already been seen. If a duplicate is detected, the item is skipped and an appropriate message is returned.

- **Duplicate Content**: If the textual content (e.g., a profile summary or description) matches a previously seen item, the skill returns the message: "[内容已忽略，重复]".
- **Duplicate Link**: If a URL or LinkedIn link has already been shared in the session, the skill returns: "[链接已忽略，重复]".

The skill operates at the session scope, meaning the memory of seen items persists for the duration of the current conversation.

## Usage

To use the deduplicator skill, simply include the items you want to check in your request. The skill will automatically filter out duplicates.

To reset the duplicate tracking and start a fresh session, issue the command: "重置去重". This clears the internal records of seen content and links.


