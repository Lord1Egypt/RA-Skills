---
name: cursor-doctor
description: Diagnose and fix Cursor IDE errors, crashes, and configuration issues. Covers 16 error signatures across 6 categories (MCP connections, crashes, AI failures, proxy/network, environment, sync). Built from 77+ real pain signals from Chinese developer communities (V2EX, CSDN).
version: 1.1.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [Cursor, IDE, Debugging, AI-Tools, Error-Diagnosis, Developer-Tools]
    homepage: https://github.com/minirr890112-byte/cursor-doctor
prerequisites:
  commands: [cursor-doctor]
---

# cursor-doctor — Cursor IDE 故障诊断工具

Diagnose and fix Cursor IDE errors, crashes, and configuration issues with one command. Built from real pain signals mined from Chinese developer communities.

## 痛点来源 (Pain Signal Origins)

在 2026 年 4-5 月的中文开发者社区扫描中，Cursor IDE 报错/崩溃是 Top 3 最热话题：
- V2EX `cursor` 节点：15+ 讨论帖（Cursor 陨落、CLI 反代、模型限制）
- CSDN 技术博客：30+ 篇 Cursor 故障文章
- 来源覆盖：V2EX · CSDN · 掘金

## Quick Start

```bash
pip install cursor-doctor

# Full diagnosis
cursor-doctor diagnose

# Auto-fix common issues
cursor-doctor fix

# Match error text to known signatures
cursor-doctor match --text "MCP Client Closed"

# List all known error signatures
cursor-doctor signatures
```

## Error Categories (16 signatures)

| Category | Count | Examples |
|---|---|---|
| MCP/Agent Connection | 3 | MCP Client Closed, Shell Parse Failure, Auth Expired |
| Crash/Freeze | 3 | Startup White Screen, Plugin Crash, Memory Overflow |
| AI/Agent Malfunction | 3 | Request Timeout, Completion Quality Drop, Agent Loop |
| Proxy/Network | 2 | Proxy Conflict, GFW Blocked |
| Config/Environment | 3 | Config Corruption, Python Not Found, Node.js Error |
| File/Sync | 2 | Sync Conflict, File Watcher Error |

## Related Tools

- **[claude-intel-monitor](https://github.com/minirr890112-byte/claude-intel-monitor)** — 检测 Claude/GPT/DeepSeek 是否降智
- **[HermesMade](https://github.com/minirr890112-byte/HermesMade)** — 自动化开发者痛点扫描平台
