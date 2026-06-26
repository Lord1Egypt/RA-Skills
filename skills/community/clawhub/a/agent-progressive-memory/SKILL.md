---
name: progressive-memory
description: "群聊渐进式记忆披露协议。当 Agent 需要在群聊/团队/项目协作场景中访问历史记忆时启用。避免 Agent 一次性加载所有记忆或跳过索引直接读子目录。不适用：单次无群聊场景的标准问答。"
---

# Progressive Memory — 渐进式披露协议

Agent 在群聊中访问记忆时必须遵守的**分层披露协议**：先读索引，再按需逐层加载。

## 核心规则

### 1. 入口管制
- 群聊记忆的唯一入口是 `memory/groups/{group_name}.md`（索引文件）
- **禁止**直接读取 `memory/groups/{group_name}/` 下的任何子文件
- 禁止绕过索引直接 `memory_search` 子目录
- **群名映射规则**：Matrix room ID（如 `!xxx:matrix.example.com`）需先查 `memory/group_names.json` 映射为友好名称 `{group_name}` 后再用

### 2. 五步加载流程

| 步骤 | 动作 | 产出 |
|------|------|------|
| 0. 群名映射 | 查 `memory/group_names.json`，将 Matrix room ID 转为 `{group_name}` | 友好名称 |
| 1. 路由定位 | `memory_get("memory/groups/{group_name}.md")` | Hard Rules + 路由索引表 |
| 2. 意图匹配 | 匹配当前消息到索引表中一个触发场景 | 确定要加载的文件 |
| 3. 显式加载 | `memory_get("memory/groups/{group_name}/{文件}.md")` | 实际记忆内容 |
| 4. 子层控制 | 仅当 Step 3 文件引用了 `conventions/` 时才加载 | 1 个子文件 |
| 5. 预算熔断 | 累计超过 `memory_budget` 时停止，提示用户 | 预算保护 |

> Step 0 是新增步骤：每次进入群聊记忆时，**必须先执行群名映射**，将 Matrix 原始 room ID 转为友好名称，再进行后续文件操作。
> 群名映射文件 `group_names.json` 格式：`{room_id}: {name, display_name}`

每次只匹配**一个**最匹配的文件（优先级最高）。

### 3. 加载纪律
- 单会话最多 **2 个 P0-P2 文件 + 1 个 P3 文件**
- `conventions/` 一次只加载 **1 个**
- `attention.md` 标记「已归档」时，只加载 `project.md`
- 切换群聊时先清理旧上下文，再重新走 Step 1

### 4. 更新回写
- 新决策 → 追加 `experience.md`
- 任务状态变化 → 更新 `attention.md`
- 索引文件只增不删（删除时标记 `[DEPRECATED]`）

## 文件结构

```
memory/groups/
├── {group_name}.md          # L0: 入口+阀门（必读）
└── {group_name}/            # 群聊私有记忆（禁止直接访问）
    ├── attention.md       # P0: 当前聚焦
    ├── project.md         # P1: 项目静态信息
    ├── experience.md      # P2: 经验/决策日志
    ├── people.md         # P3: 人员画像
    └── conventions/       # L3: 细分规范
        ├── api.md
        ├── db.md
        └── ...
```

> **命名规范**：所有文件和目录一律使用友好名称 `{group_name}`，禁止直接使用 Matrix room ID（如 `!xxx:matrix.example.com`）。通过 `memory/group_names.json` 做 ID → 名称映射。

## 优先级定义

| 优先级 | 文件 | 内容 | 加载时机 |
|--------|------|------|----------|
| P0 | `attention.md` | 活跃任务、阻断项、环境快照 | 任何与当前工作相关的对话 |
| P1 | `project.md` | 技术栈、架构约束、规范索引 | 技术选型、架构讨论、新人 onboarding |
| P2 | `experience.md` | 历史决策、踩坑记录、复盘 | memory_search 命中后追加加载 |
| P3 | `people.md` | 人员角色、审批流程、联系方式 | 需要找人的时候 |

## 反模式速查

```
❌ 一次加载索引所有引用文件     → ✅ 每次只加载一个
❌ 跳过索引直接读子文件         → ✅ 先加载索引
❌ 同时加载两个群聊            → ✅ 切换时清理再重载
❌ 全文加载 experience.md      → ✅ 搜索命中后片段加载
```

## 索引文件模板

```markdown
---
group_name: your-group    # 来自 group_names.json 的映射名称
last_updated: YYYY-MM-DD
status: active
memory_budget: 6000
---

# {Group Name} — 渐进式披露索引

> ⚠️ 本文件是访问此群聊记忆的**唯一合法入口**。

## Hard Rules

- 规则1
- 规则2

## 路由索引

| 触发场景 | 加载文件 | 优先级 |
|---------|---------|--------|
| 当前任务、Sprint、阻断项 | `attention.md` | P0 |
| 技术栈、架构约束 | `project.md` | P1 |
| 历史决策、踩坑记录 | `experience.md` | P2 |
| 人员分工、联系方式 | `people.md` | P3 |
| API 开发细节 | `conventions/api.md` | P2-L3 |
```

---

## 5. Memory Flush — 周期性记忆冲刷 ⭐

> 本协议的第四条规定了"手动更新"，本扩展规定了**自动周期性冲刷**。

渐进式披露解决了"读什么"，这个扩展解决"什么时候写、写什么"。

### 5.1 冲刷触发时序

| 优先级 | 触发器 | 触发条件 | 动作 |
|--------|--------|---------|------|
| P0 | **Hook: `/remem`** 🪝 | 用户在任意聊天发送 `/remem` | 6 步完整冲刷：context 检测 → 发现 groups → 对比旧记忆 → 更新文件 → stamp 时间戳 → 写 flush-state |
| P1 | **Cron 定时** ⏰ | 每天 06:17 和 18:17 Asia/Shanghai | 两次定时冲刷，确保增量不丢 |
| P2 | **手动触发** ✋ | Agent 感知到重要决策/状态变更 | 立即写回记忆文件 |

> **关键设计**：`/remem` 在**会话活跃时**触发，hook 拿到的是当前 session 的完整上下文，而不是空状态。

### 5.1a 默认配置

| 项目 | 配置 |
|------|------|
| Hook 事件 | `message:received`（监听 `/remem` 命令） |
| Hook 路径 | `~/.openclaw/hooks/remem-flush/` |
| Cron 定时 | 每天 06:17 和 18:17 Asia/Shanghai |
| Cron 模式 | `--system-event` 发到 main session，不走 agent 对话 |
| 执行逻辑 | 6 步：context 用量检测 → 发现 memory groups → 读旧记忆找 deltas → 执行更新 → stamp 时间戳 → 写 flush-state |

### ⚠️ 为什么不用 `/new` hook？

内置 `memory-flush` hook 监听 `command:new`（即 `/new`），但存在根本性冲突：

1. `/new` 的语义是**创建新 session**
2. Hook 在 `/new` 触发时，新 session 已创建，**旧 session 的上下文已丢失**
3. Hook 拿到的 `previousSessionEntry` 在新 session 创建后可能已经不可访问
4. 结果：hook 执行了，但没有任何历史内容可冲刷，**命令被静默吞掉**

**解决方案**：自定义 `remem-flush` hook 监听 `message:received`，在消息层拦截 `/remem`。此时 session 仍然活跃，完整上下文可用。

### 5.1b remem-flush Hook 安装

Hook 文件已打包在 skill 目录中，安装时需复制到 OpenClaw hooks 目录：

```bash
# Skill 包内路径（安装后位于 skill 目录）
# hooks/remem-flush/
#   ├── HOOK.md       # 元数据 + 文档
#   └── handler.js    # 处理逻辑

# 安装命令（从 skill 目录复制）
cp -r hooks/remem-flush/ ~/.openclaw/hooks/remem-flush/
```

**安装后目录结构：**
```
~/.openclaw/hooks/remem-flush/
├── HOOK.md       # 元数据 + 文档
└── handler.js    # 处理逻辑
```

**注意**：内置 `memory-flush` hook 必须禁用（`enabled: false`），否则 `/new` 会被它拦截且失败。

### 5.1c precompact-remem Hook（可选，推荐安装）

**自动**在 session context 压缩前执行 memory flush，无需人工触发：

| 项目 | 配置 |
|------|------|
| Hook 事件 | `session:compact:before` |
| Hook 路径 | `~/.openclaw/hooks/precompact-remem/` |
| 触发条件 | session 有 ≥10 条消息 或 ≥1000 tokens |

```bash
# 安装
cp -r hooks/precompact-remem/ ~/.openclaw/hooks/precompact-remem/
```

**安装后需在 OpenClaw 中启用**：
```bash
openclaw hooks enable precompact-remem
```

两个 hook 互补：
- `remem-flush` — 用户手动 `/remem` 触发
- `precompact-remem` — **自动**在 context 压缩前触发（推荐开启）

### 5.2 冲刷内容判定

#### ✅ 值得写

| 类别 | 目标文件 | 判断标准 |
|------|---------|---------|
| 已确认的决策 | `experience.md` | 用户明确同意/确认，或有执行动作 |
| 任务状态变化 | `attention.md` | 从进行中→完成/阻断/变更 |
| 新项目约定 | `project.md` | 两条不同消息交叉确认 |
| 人员角色变更 | `people.md` | 明确的角色指派或变更 |
| 环境/配置变更 | `attention.md` | 服务器迁移、端口变更、密钥轮换 |
| 踩坑/修复记录 | `experience.md` | 描述问题+解决方案的完整记录 |

#### ❌ 不写

| 类别 | 理由 |
|------|------|
| 闲聊、打招呼、日常 | 无信息价值 |
| 仅有观点未落地 | 未形成决策 |
| 重复已有内容 | 与记忆文件已有条目一致 |
| 临时的探索性讨论 | 方向未定，变了还需改 |

### 5.3 写回规范

- **`experience.md`**：追加-only，按时间倒序，每条含 `YYYY-MM-DD` 标记、背景、决策、执行
- **`attention.md`**：直接覆盖旧状态（任务进度是事实性更新，不是日志）
- **`project.md`、`people.md`**：增补为主，删除需显式确认
- **`group_names.json`**：发现新成员或角色变化时可追加，不做破坏性更新

### 5.4 冲刷状态文件

引入 `memory/flush-state.json` 追踪冲刷状态：

```json
{
  "last_flush_time": "2026-05-15T07:30:00+08:00",
  "attention_last_updated": "2026-05-15T07:00:00+08:00",
  "experience_last_appended": "2026-05-15T06:00:00+08:00",
  "context_usage_at_flush": 45,
  "pending_items": ["确认张三是新 PM"],
  "session_id": "last-session-id"
}
```

使用规则：
- 每次冲刷后更新 `last_flush_time`
- `pending_items` 存储暂未确认但值得留意的线索
- 下次冲刷时先处理 `pending_items` 再扫增量

### 5.5 与渐进式披露的配合

```
        读：Progressive Disclosure        写：Memory Flush
              ↓                                ↓
        索引 → 按需加载                会话增量 → 写回文件
              ↓                                ↓
         省 token + 精准读取            不丢信息 + 自动维护
              ↓                                ↓
              └── 组成完整记忆闭环 ←───────────┘
```

在加载文件后，应向 HUMAN 说明该文件的上次冲刷时间（如 `attention.md 上次更新: 2026-05-14，当前会话有 2 项任务状态变更待刷`）

## 完整协议清单

1. **入口管制** — 索引唯一入口，禁止直接读子目录
2. **五步加载流程** — 群名映射 → 路由定位 → 意图匹配 → 显式加载 → 子层控制 → 预算熔断
3. **加载纪律** — 2+1 文件限制，切换清除
4. **手动更新回写** — 新决策/状态变更立即写回
5. **Memory Flush** — `/remem` 触发（推荐）+ Cron 兜底（06:17 & 18:17）
6. **Auto-Flush** — `precompact-remem` hook 在 session compaction 前自动执行 flush
