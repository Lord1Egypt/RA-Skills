# SimpleViking 技能

模仿 [OpenViking](https://github.com/volcengine/OpenViking) 的上下文管理思想，实现一个轻量级的文件系统范式上下文数据库。

## 核心概念

- **文件系统范式**：所有的上下文（记忆、资源、技能）都通过 `viking://` URI 访问
- **三级上下文 (L0/L1/L2)**：自动生成摘要、概览、详情，按需加载
- **目录递归检索**：先定位目录，再细化搜索，提高检索精度
- **会话自迭代**：从对话历史提取长期记忆，Agent 越用越聪明

## 工具列表

| 工具 | 描述 |
|------|------|
| `sv_find` | 在 viking 上下文中搜索关键词 |
| `sv_read` | 读取 viking:// URI 的内容（可选分层：l0/l1/l2）|
| `sv_write` | 写入内容并自动更新父目录的 L0/L1 元数据 |
| `sv_update_layers` | 手动更新目录层级 |
| `sv_extract_memory` | 从会话记录提取记忆 |

## 快速开始

### 初始化工作空间

```bash
# 环境变量设置（可选）
export SV_WORKSPACE="$HOME/.openclaw/viking"

# 初始化目录结构
sv init
```

### 写入内容

```bash
sv_write viking://resources/my_project/README.md "# 项目名称\n\n这是项目简介。"
```

这会自动：
- 创建文件
- 更新父目录的 `.abstract` 和 `.overview`

### 检索

```bash
# 简单关键词检索
sv_find "API 认证"

# 从特定目录开始
sv_find "用户设置" viking://user/memories
```

输出示例：
```
=== 路径匹配 ===
FILE: viking://resources/auth/README.md
=== 内容匹配 ===
viking://resources/auth/README.md:5 | 认证流程 steps...
```

### 读取内容

```bash
# 读取全文（L2）
sv_read viking://resources/auth/README.md

# 读取摘要（L0）或概览（L1）
sv_read viking://resources/auth --layer l0
sv_read viking://resources/auth --layer l1
```

### 会话记忆提取

```bash
sv_extract_memory --session /path/to/session.jsonl
```

会自动：
- 提取用户偏好 → `user/memories/preferences.log`
- 提取经验教训 → `agent/memories/lessons.log`
- 生成会话摘要 → `resources/sessions/YYYY-MM-DD/session_xxx.md`
- 更新相关目录层级

## 目录结构

```
~/.openclaw/viking/
├── resources/           # 资源：文档、网页、代码
│   ├── project-a/
│   │   ├── .abstract   # L0 摘要 (~100 tokens)
│   │   ├── .overview   # L1 概览 (~2k tokens)
│   │   └── README.md   # L2 详情
├── user/memories/
│   ├── preferences.log # 用户偏好列表
│   └── habits/         # 习惯目录
├── agent/
│   ├── skills/         # 技能库
│   ├── memories/       # 任务记忆
│   └── instructions/   # 系统指令
└── sessions/           # 会话记录
    └── 2025-03-08/
        └── session_abcdef.jsonl
```

## 在 OpenClaw 中集成

每个工具（`sv_find`, `sv_read` 等）都是独立的可执行文件，位于 `skills/simple-viking/tools/`。

在 OpenClaw 的 skill 定义中，可以将它们注册为工具，通过 `exec` 或直接调用。

示例调用（Agent 内部）：

```bash
# 使用 exec 工具
exec(command="sv_find \"用户偏好\"", input="")

# 使用 sessions_send 让另一个 agent 调用
sessions_send(sessionKey="...", message="请运行 sv_find \"API\"")
```

## 注意事项

- 这是一个简化实现，检索基于关键词匹配。语义检索需要额外集成 embedding 模型（参考 OpenViking 的 dense embedding 支持）。
- L0/L1 自动生成是启发式的（截取开头），可扩展为调用模型生成摘要。
- 文件系统存储在本地，git 友好，可手动编辑。

## 灵感来源

- [OpenViking](https://github.com/volcengine/OpenViking) - 面向 AI Agent 的上下文数据库
- 文件系统范式、三级上下文、目录递归检索策略等概念均源自 OpenViking 设计。

---

**版本:** 0.1.0
**作者:** 猫经理 (maojingli)
**许可证:** Apache-2.0 (继承 OpenViking)