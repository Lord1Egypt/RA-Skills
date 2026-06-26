# codex-sessions-manager

[![npm](https://img.shields.io/npm/v/codex-sessions-manager)](https://www.npmjs.com/package/codex-sessions-manager)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[English](./README.md)

> Codex 没有删除会话的功能。归档 ≠ 删除。你的 `~/.codex` 只会越来越大。

**codex-sessions-manager** 是目前最彻底的本地 Codex 会话清理工具。它同时是 **Skill**（Claude Code / Codex 可直接调用）、**CLI** 和 **MCP Server**——三种形态共享同一套核心逻辑。不只是删文件——四层存储全清、失败自动回滚、AI Agent 可直接调用。

## 为什么选这个？

其他工具删个 SQLite 行或者删几个文件就完事了。这个工具不一样：

| | codex-sessions-manager | 其他工具 |
|--|:---:|:---:|
| 清理全部 4 层（文件 + JSONL + SQLite + 全局状态） | ✅ | ❌ 只清部分 |
| 删除中途出错自动回滚 | ✅ | ❌ |
| 可恢复的回收站 + 冲突检测 | ✅ | ❌ 或简单备份 |
| 删完验证有没有残留 | ✅ | ❌ |
| AI Agent 可直接调用（MCP） | ✅ | ❌ |
| 识别 `/side` 和 `/fork` 父子关系 | ✅ | ❌ |

## 快速开始

```bash
# 全局安装
npm install -g codex-sessions-manager

# 列出最近的会话
codex-sessions list --limit 10

# 预览删除（安全，不做任何修改）
codex-sessions delete <session-id>

# 删除到回收站（推荐）
codex-sessions delete <session-id> --trash --yes

# 后悔了？恢复
codex-sessions restore <session-id> --yes

# 验证是否清理干净
codex-sessions verify <session-id>
```

## 删除到底做了什么

其他工具：删一个文件或一行数据库记录 → 完事 → 到处是孤儿文件。

这个工具：

```
1. 快照所有文件（万一要回滚）
2. 改写 session_index.jsonl（移除匹配行）
3. 改写 history.jsonl（移除匹配行）
4. 清理 `.codex-global-state.json` 引用
5. 删除原始 session 文件
6. 删除 shell snapshot 文件
7. 删除 SQLite 记录（threads、logs、spawn edges、agent jobs、dynamic tools、stage1、thread goals）

如果任何一步失败 → 全部回滚到原始状态。
```

删完之后跑 `verify`，确认零残留。

## 功能一览

| 功能 | 说明 |
|------|------|
| **列出 & 筛选** | 按项目、状态、时间范围筛选；按项目分组 |
| **导出** | 删之前先备份为 JSON |
| **删除** | 永久删除或放入回收站，你选 |
| **回收站 & 恢复** | 完整快照保存；恢复时检查 SQLite 主键冲突 |
| **验证** | 报告是否还有残留文件、索引行、数据库记录 |
| **清理索引** | 移除失效索引条目，不动原始数据 |
| **健康检查** | `doctor` 命令做完整诊断 |
| **MCP 服务** | AI Agent（Claude Code、Codex、Kiro）直接管理会话 |
| **子对话感知** | 识别 `/fork` 和 `/side` 的父子关系；不会自动递归删除子对话 |

## 给 AI Agent 用（MCP）

加到你的 MCP 配置：

```json
{
  "mcpServers": {
    "codex-sessions": {
      "command": "codex-sessions-mcp",
      "args": []
    }
  }
}
```

暴露 13 个工具：`inspect_root`、`list_sessions`、`list_projects`、`get_session`、`export_session_backup`、`preview_delete_sessions`、`delete_sessions`、`list_trash`、`restore_sessions`、`purge_trash`、`cleanup_session_indexes`、`cleanup_stale_indexes`、`verify_sessions`。

所有破坏性操作需要 `confirm: true`，否则只返回预览。

## CLI 命令

```bash
codex-sessions list [--status active|archived] [--limit N] [--project TEXT]
codex-sessions list --updated-after 2026-04-01 --updated-before 2026-04-30
codex-sessions list --group-by project
codex-sessions projects
codex-sessions doctor [--json]
codex-sessions show <session-id>
codex-sessions export <session-id> [--output ./backup.json]
codex-sessions delete <session-id...> [--trash] [--yes]
codex-sessions trash-list
codex-sessions restore <session-id> --yes
codex-sessions purge <session-id> --yes
codex-sessions cleanup-stale [--yes]
codex-sessions cleanup-index <session-id...> [--yes]
codex-sessions verify <session-id...> [--json]
```

**安全第一**：所有破坏性命令需要 `--yes` 才执行，不加只看预览。

## Codex 存了什么（我们清理什么）

```
~/.codex/
├── sessions/            ← 原始 rollout JSONL 文件       ✅ 清理
├── shell_snapshots/     ← shell 快照脚本                ✅ 清理
├── session_index.jsonl  ← 会话元数据索引                ✅ 清理
├── history.jsonl        ← 对话历史索引                  ✅ 清理
├── state_N.sqlite       ← threads 和相关记录            ✅ 清理
├── logs_N.sqlite        ← 执行日志                      ✅ 清理
└── .codex-global-state.json ← 已知活跃会话引用          ✅ 清理
```

## 文档

- [安全指南](./docs/SAFETY.md) — 删除/回收站/恢复/清除前必读
- [更新日志](./CHANGELOG.md) — 版本记录
- [SKILL.md](./SKILL.md) — Claude Code / Codex 的 AI 技能说明

## 开发

```bash
git clone https://github.com/1939869736luosi/codex-sessions-manager.git
cd codex-sessions-manager
npm install
npm run build
npm test
```

## 许可证

Apache-2.0
