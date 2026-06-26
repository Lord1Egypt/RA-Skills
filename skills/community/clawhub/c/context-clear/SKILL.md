---
name: context-clear
description: "Memory management system with automated tiered storage (hot/warm/gist/forgotten), time-decay organization, promotion engine, layer-search protocol, and session-injection plugin. Use when managing conversation memory, running /refresh, organizing checkpoint files, retrieving past memories, promoting important content to long-term storage, or cleaning up stale context."
---

# Context Clear — 记忆整理与上下文清空

纯文件系统的 SRS（间隔重复）记忆管理方案 + OpenClaw 插件。核心目标：在 token 成本和信息保留之间做自动平衡。

## 存储结构

```
~/.openclaw/memory_fs/
├── hot/       (< 3h)            原始完整    ← 自动注入 session
├── warm/      (3h~7d)           原始完整
├── gist/      (7d~30d)          摘要+标签    ← warm/ 保留同名原始文件
└── forgotten/ (≥14d 无检索)      等待物理删除

~/.openclaw/refcount.json    ← 引用计数 + 检索记录
```

## 记忆粒度

各层能提供的信息量不同 — 检索时据此判断结果的可信度：

| 层 | 时间窗 | 粒度 | 内容形式 | 检索置信度 |
|----|--------|------|---------|-----------|
| hot/ | < 3h | 🔴 原始完整 | 对话原文、工具输出、checkpoint 全文 | 高 — 可精确引用原文 |
| warm/ | 3h~7d | 🟠 原始完整 | 同上，未被压缩 | 高 — 同 hot |
| gist/ | 7d~30d | 🟡 摘要标签 | `#标题\n标签: xxx\n摘要` | 中 — 定位话题，细节可回 warm/ 看同名原件 |
| forgotten/ | ≥14d 无检索 | 🔵 遗忘中 | 原始/摘要格式 | 极低 — 即将物理删除 |

**设计原则：** 记忆质感随时间自然衰减。近 3h 的事可精确复述，3h~7d 可回顾细节，7d~30d 仅能回忆话题方向。warm/ 始终保留原始文件（gist 是它的摘要副本），检索命中 gist 时可按文件名回 warm/ 读原文。

---

## 生命周期

```
创建
  │
  ├─3h→ hot/     (原始完整，自动注入 session)
  │
  ├─7d→ warm/    (原始完整)
  │     │
  │     ├── copy → gist/ (摘要副本，keep warm 原件)
  │     │
  │     └── 14d 无检索 → forgotten/
  │                     │
  │                     └── 30d → 物理删除
  │
  检索命中（任一层）
       │
       └── 轮动回 hot/ (forgotten 回 warm/)
```

### 正向衰减（organize.py 三步）

| 步骤 | 职责 | 判据 |
|------|------|------|
| 1. mtime 分层 | hot→warm（move），warm→gist（copy，warm 保留原件） | 文件 mtime |
| 2. 遗忘检查 | warm/gist→forgotten | refcount 最后检索时间距今 >14d |
| 3. 清理 | forgotten 中 >30d → 物理删除 | mtime，跳过 user_marked |

### 逆向轮动（检索命中 → 回热层）

| 来源 | 动作 | 原因 |
|------|------|------|
| hot/ | 不动 | 已在最热层 |
| warm/ | mv 回 hot/ + touch | 被回查 = 仍相关 |
| gist/ | mv 摘要文件回 hot/；warm 原件同回 hot/ | 完整信息双份带回 |
| forgotten/ | mv 回 warm/ + 标记 user_marked | 被检索 = 仍需要，从 warm 重新走衰减 |

---

## 组件

| 组件 | 功能 |
|------|------|
| `organize.py` | 三步职责：mtime 分层（warm→gist copy）→ 14d 遗忘检查 → forgotten 清理 |
| `promote.py` | 读取 refcount.json，筛选晋升候选，输出 promote_report.md |
| 插件 `/refresh` | 触发 organize → promote → session reset |

## 晋升机制

### 晋升条件（满足任一）

| 条件 | 门槛 |
|------|------|
| 7天内引用 | ≥ 3 次 |
| 14天内引用 | ≥ 5 次 |
| 总引用 | ≥ 8 次 |
| 用户标记 | user_marked = true |

### 晋升后处理

子 session 读取 `promote_report.md` 分类搬运：
- **Skill 类** → `skills/<skill>/docs/retrospect.md`
- **偏好/事实类** → `MEMORY.md`
- **需判定** → 留待人工分类

晋升后从 refcount 标记 `promoted: true`，不再重复提名。

---

## 逐层检索协议

### 触发条件

当前 session 上下文找不到答案时启动：

| 信号 | 表现 |
|------|------|
| 用户提之前讨论过的话题 | "我们上次是不是讨论过 XXX" |
| 用户问之前达成的共识 | "XX 的结论是什么" |
| 自我感知 | 我注意到信息不在当前上下文中 |
| 用户明示 | "之前说过""之前写过" |

### 检索顺序

```
hot/ → warm/ → gist/ → forgotten/    找到即停
```

### 检索方法

```bash
# hot/warm — 原始内容，关键词 grep
grep -ril "关键词1\|关键词2" ~/.openclaw/memory_fs/hot/
grep -ril "关键词1\|关键词2" ~/.openclaw/memory_fs/warm/

# gist — 先按标签再按关键词
grep -ril "tag1\|tag2" ~/.openclaw/memory_fs/gist/
grep -ril "关键词" ~/.openclaw/memory_fs/gist/

# forgotten — 最低优先级
grep -ril "关键词" ~/.openclaw/memory_fs/forgotten/
```

关键词：从用户问题+上下文提炼 2-5 个核心词。匹配 >3 个时缩小重试。

### 命中处理

| 步骤 | 动作 |
|------|------|
| 1 | 读入匹配文件内容 |
| 2 | **轮动**：按来源层执行逆向轮动（见上表） |
| 3 | **更新 refcount**：`total` +1，`timestamps` 追加时间戳 |
| 4 | gist 层命中但摘要不够 → 去 warm/ 读同名原始文件（原件完好 ✓） |

匹配 >3 个文件 → 缩小关键词重试，不一次性读入。

### 未命中处理

> memory_fs 中未找到关于 'XXX' 的记录。可能原因：
> 1. 从未被记录过
> 2. 已物理删除（进入 forgotten 后 30 天无调用自动清理）
> 3. 关键词不对，换组词再试

### 引用计数联动

每次命中递增 refcount → 频繁被回查的信息自然达到晋升门槛 → 自动存入 MEMORY.md。

```json
{
  "warm/my-checkpoint.md": {
    "total": 5,
    "7d": 3,
    "timestamps": [1748073600, 1748160000],
    "user_marked": false,
    "summarized": false,
    "created": 1748000000
  }
}
```

### 搜索决策树（速查）

```
当前上下文找不到信息？
  → hot/ → 命中？→ 读入，不轮动
  → warm/ → 命中？→ 读入，mv 回 hot/
  → gist/ → 命中？
     → 摘要够？→ 直接读，摘要文件 mv 回 hot/
     → 不够？→ warm/ 读同名原始文件，双份回 hot/
  → forgotten/ → 命中？
     → mv 回 warm/ + 标记 user_marked，提醒用户已找回历史记忆
  → 都没找到 → 如实告知
```

---

### 注意要点

- 始终优先搜 hot/（最近、最相关）
- 先读文件名确认相关，再读文件内容
- gist 摘要不够用时，warm/ 有同名原始文件可读 — organize.py 已从 move 改为 copy
- forgotten 命中后轮动回 warm/，从 warm 重新走衰减周期
