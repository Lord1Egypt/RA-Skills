---
name: automation
description: Automation tools. Schedule tasks, trigger engine, room management, memory/note system, skill management.
version: 1.2.31
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Automation & Utility Tools

> **Parent skill:** [SKILL.md](../SKILL.md) — provides cross-platform tools and MCP endpoint config.

## Schedule

| Tool | Arguments | Returns |
|------|-----------|---------|
| `schedule/add` | `name`, `scheduledTime`, `toolName`, `toolArgs`, `repeat`, `repeatDays` (opt) | Task ID |
| `schedule/list` | — | `tasks[]` |
| `schedule/get` | `id` | Task detail |
| `schedule/update` | `id` + fields to update | Update result |
| `schedule/delete` | `id` | Delete result |
| `schedule/cancel` | `id` | Cancel result |

**Repeat types:** `none` / `daily` / `weekdays` / `weekends` / `weekly` / `custom_days`

**Example:**
```json
{
  "name": "schedule/add",
  "arguments": {
    "name": "睡前关灯",
    "scheduledTime": "2026-05-16T23:00:00+08:00",
    "toolName": "xiaomi/set_property",
    "toolArgs": "{\"device_id\":\"xxx\",\"siid\":2,\"piid\":1,\"value\":false}",
    "repeat": "daily"
  }
}
```

## Trigger Engine (PC proxy)

| Tool | Arguments | Returns |
|------|-----------|---------|
| `trigger/create` | `name`, `cameras`, `condition`, `actions` | Rule ID |
| `trigger/list` | — | `rules[]` |
| `trigger/update` | `id`, fields to update | Update result |
| `trigger/delete` | `id` | Delete result |
| `trigger/toggle` | `id`, `enabled` | Toggle result |
| `trigger/logs` | `limit`, `rule_id` (opt) | `logs[]` |

## Room Management

| Tool | Arguments | Returns |
|------|-----------|---------|
| `room/list` | — | Unique room name list |
| `room/set_device` | `device_ids` (string[]), `room_name` (string) | Assignment result |

## Memory System

| Tool | Arguments | Returns |
|------|-----------|---------|
| `memory/read` | — | All long-term memories |
| `memory/add` | `content`, `category` (opt) | Added entry |
| `memory/update` | `id`, `content` | Update result |
| `memory/delete` | `id` | Delete result |
| `memory/search` | `keyword` | Matching entries |
| `memory/note` | `content` | Add today's note |
| `memory/today` | — | Today's notes |

## Skill System

| Tool | Arguments | Returns |
|------|-----------|---------|
| `skill/list` | — | Available skills |
| `skill/read` | `id` | Skill content |
| `skill/manage` | `action` (add/update/delete) + other fields | Manage result |
