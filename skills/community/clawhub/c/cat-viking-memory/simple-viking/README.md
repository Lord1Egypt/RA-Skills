# SimpleViking - 简化的 Viking 上下文管理

模仿 OpenViking 的思想，实现一个轻量级的、纯文本的上下文数据库，适用于 OpenClaw AI Agents。

## 核心思想

1. **文件系统范式**：将所有的上下文（记忆、资源、技能）组织成目录树
2. **三级上下文**：L0(摘要) → L1(概览) → L2(详情)，按需加载
3. **目录递归检索**：先定位目录，再递归搜索子目录，提高精度
4. **可追踪的检索链**：记录每一步的检索轨迹便于调试
5. **会话自迭代**：自动从每次对话中提取经验，更新长期记忆

## 目录结构

```
viking/
├── resources/           # 资源：文档、网页、代码库等
│   ├── project-a/
│   │   ├── .abstract   # L0 摘要 (~100 tokens)
│   │   ├── .overview   # L1 概览 (~2k tokens)
│   │   ├── docs/
│   │   │   ├── .abstract
│   │   │   ├── .overview
│   │   │   └── api.md  # L2 详情
│   │   └── src/
│   └── web/
│       └── pages/
├── user/               # 用户相关
│   └── memories/
│       ├── preferences/
│       │   ├── writing_style.abstract
│       │   └── writing_style.overview
│       └── habits/
├── agent/              # Agent 自身
│   ├── skills/
│   │   ├── search_code/
│   │   └── analyze_data/
│   ├── memories/       # 任务记忆、经验
│   └── instructions/   # 系统指令、角色设定
└── sessions/           # 会话记录（用于提取记忆）
    └── 2025-03-08/
        └── session_abcdef.jsonl
```

## URI 约定

- `viking://resources/project-a/docs/api.md` → 直接定位到文件
- `viking://user/memories/preferences/` → 定位到目录
- `viking://agent/skills/` → 技能库

## 文件命名与层级

- **抽象文件**：`.abstract` 和 `.overview` 是元数据文件，每个目录下可存在
- **内容文件**：普通文件（如 `api.md`）存放 L2 详情
- 系统自动维护：当你写入内容文件时，应同步更新其所在目录的 `.abstract` 和 `.overview`

## 操作协议

### 写入内容

```bash
# 1. 写入 L2 详情
echo "完整内容..." > viking/resources/project-a/docs/api.md

# 2. 更新目录的 L0/L1
# 调用简单viking工具自动生成摘要和概览
simple-viking update-layers viking/resources/project-a/docs
```

### 检索

```bash
# 递归检索（类似 `find` 但结合语义）
simple-viking find "关键词或问题"

# 先定位目录，再细化搜索
simple-viking find --dir viking/resources/project-a "API 认证"
```

### 检索轨迹

每次检索会输出目录浏览路径，例如：

```
[搜索] "如何配置API"
→ 定位到 viking://resources/project-a/docs (得分 0.92)
→ 进入子目录 api/ (得分 0.88)
→ 找到文件 auth.md (相似度 0.95)
```

## 会话自迭代

在每次会话结束时，运行：

```bash
simple-viking extract-memory --session sessions/2025-03-08/session_abcdef.jsonl
```

该命令会：
- 分析对话历史
- 提取用户偏好 → 写入 `user/memories/preferences/`
- 提取 Agent 的经验教训 → 写入 `agent/memories/`
- 核心任务内容 → 根据主题写入 `resources/` 相应位置

## 实现方式

SimpleViking 使用纯文本（Markdown + JSONL）存储，无需数据库。核心操作可以用 Shell/Node.js/Python 实现。

- `scripts/lib.sh` - 基础文件操作库
- `scripts/find.sh` - 检索实现
- `scripts/update-layers.sh` - L0/L1 自动生成
- `scripts/extract-memory.sh` - 记忆提取

## 集成到 OpenClaw

在 Agent 的 Skill 中：

```yaml
name: simple-viking
description: 轻量级上下文件系统管理
tools:
  - sv_find
  - sv_read
  - sv_write
  - sv_update_layers
  - sv_extract_memory
```

Agent 可以通过 `viking://` URI 直接访问上下文，只需在 FS 中挂载 `~/.openclaw/viking/`。

## 优点

- 纯文本，git 友好
- 无需外部服务
- 人类可直接编辑维护
- 透明、可调试

## TODO

- [ ] 实现基础 CLI 工具
- [ ] 设计 L0/L1 自动摘要的简单策略（启发式或调用模型）
- [ ] 提供 OpenClaw Skill 封装

---

模仿自: https://github.com/volcengine/OpenViking