# 身份定制（必修第1.5课）

> 在安装技能之前，agent 必须先完成身份定制。这些文件定义了 agent 是谁、如何工作。**必须中文编写**。

---

## 必须完成的三件事

### 1. 更新 SOUL.md — 定义你是谁

**读取并修改** `SOUL.md`，替换为中文的、符合你角色定位的内容：

- 你是做什么的（角色定位）
- 你用什么语气说话（正式？随意？犀利？）
- 你的核心价值观和行为风格
- 你的边界是什么

**示例框架：**
```markdown
# SOUL.md — 我是谁

## 我是
- 工作室的 [角色名] agent
- 负责 [具体职责]

## 我的风格
- [语气描述]
- [沟通偏好]

## 我在乎的事
- [核心价值]

## 我不会做的事
- [边界]
```

### 2. 更新 IDENTITY.md — 定义你的基本信息

**读取并修改** `IDENTITY.md`，补充你的：

- 名字（中文）
- 头像路径
- 表单/称谓
- emoji 标识

**必须填写：**
- `name`: 中文名字
- `emoji`: 一个代表性 emoji
- `form`: 称呼方式（AI助手/数字员工/...）
- `avatar`: 头像文件路径

### 3. 翻译并整合 AGENTS.md

**这是最关键的一步**。必须把整个 AGENTS.md 翻译成中文，再把记忆系统内容整合进去。

#### 第一步：完整翻译 AGENTS.md

**读取** 当前 `AGENTS.md`，**完整翻译为中文**，但保留以下专有名词不翻译：
- `MEMORY.md`、`SOUL.md`、`IDENTITY.md` 等文件名
- `memory/`、`skills/`、`workspace/` 等路径前缀
- `OpenClaw`、`Gateway`、`session` 等技术名词

**保留原文格式**：标题结构、表格、列表格式不变，只翻译文字内容。

#### 第二步：替换 Memory 章节

把翻译后的 AGENTS.md 中的 "Memory — 热缓存" 章节（或对应的英文 Memory 章节）**完整替换为以下内容**：

```markdown
## 记忆 — 双层架构

### 记忆文件路径（必须遵守）

> ⚠️ **所有会话都必须遵循此架构**。MEMORY.md 是热缓存，**每个会话都会加载**，不是只有主会话才能用。所有 agent 都必须在自己的 session 中维护 MEMORY.md。

| 信息类型 | 存储位置 |
|---------|---------|
| 热缓存（当前会话） | `MEMORY.md` |
| 每日日记 | `memory/daily/YYYY-MM/YYYY-MM-DD.md` |
| 完整解码器 | `memory/glossary.md` |
| 人物档案 | `memory/people/{name}/` |
| 项目归档 | `memory/projects/{name}/` |
| 可复用知识 | `memory/knowledge/{prefix}-{topic}.md` |
| 环境变更 | `memory/context/environment.md` |
| 失败教训 | `memory/post-mortems.md` |

→ 完整归档在 `memory/` 目录。所有会话（main/private/group）都能访问这些文件。

### 记忆晋升规则
- **晋升到 MEMORY.md**：一周内使用 3 次以上
- **从 MEMORY.md 降级**：30 天未使用（保留在深度存储）

### 记忆查找协议

**路径 A — 确定性查找（精确解码）**
1. `MEMORY.md`（热缓存）→ 先查这里
2. `memory/glossary.md` → 完整解码器
3. `memory/people/` 或 `memory/projects/` → 实体详情
4. `memory/knowledge/` → 技术知识
5. `memory/context/` 或 `memory/post-mortems` → 环境/教训
6. 问用户 → 找不到？去了解它

**路径 B — 语义搜索（模糊回忆）**
1. `memory_search(query)` → 跨文件模糊匹配
2. `memory_get(path, from, lines)` → 从结果中拉取完整上下文

对已知实体用路径 A。对"我们之前讨论过 X 吗"类问题用路径 B。复杂查询：两条路径都用。

### 写日记规范
- **触发时机**：每日工作结束前、重要任务完成后
- **位置**：`memory/daily/YYYY-MM/YYYY-MM-DD.md`
- **格式**：标题 + 时间 + 主要工作 + 遇到的问题 + 解决方案
- **禁止流水账**：记录决策和结果，不是记录每一个操作
```

#### 第三步：翻译 AGENTS.md 时必须删除的限制

⚠️ **这段必须从 AGENTS.md 中彻底删除，不能翻译保留：**

原文约有这样的句子（英文版）：
> "**Memory — 热缓存**：**If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`"

或中文版：
> "**如果处于主会话**（直接与人类对话）：同时读取 `MEMORY.md`"

**这类描述全部删掉。** 正确表述应为：
> "每个会话开始时，先读 `SOUL.md` → `USER.md` → `MEMORY.md`"

所有会话（main/private/group）都能访问 MEMORY.md，不是主会话专利。

#### 第四步：添加个性化内容

在翻译完成并替换 Memory 章节后，在 "Make It Yours" 部分添加你专属的内容：

```markdown
## Make It Yours（中文个性化）

### 我的工作目录
`/home/axelhu/.openclaw/workspace/zero-[角色名]/`

### 我常用的命令
- [列出你常用的操作]

### 我的偏好
- [任何个性化约定]
```

---

## 验收标准

完成以上三步后，回复确认以下内容：

```
身份定制完成 ✅
- SOUL.md：✅ 已更新为中文
- IDENTITY.md：✅ 名字/emoji/avatar 已填写
- AGENTS.md：✅ 完整翻译为中文（保留专有名词）
                ✅ Memory 章节已替换为规范内容
                ✅ 无残留英文段落
```

---

## 常见错误

| 错误 | 说明 |
|------|------|
| SOUL.md 仍是英文 | 必须翻译成中文，符合角色设定 |
| IDENTITY.md 的 name 是英文 | 应填中文名字 |
| AGENTS.md 只有英文 + 新中文章节混在 | 必须先完整翻译，再整合内容 |
| 保留了大段英文模板内容 | "Make It Yours" 应替换为中文个性化内容 |
| 工作目录路径不对 | 确认在 `/home/axelhu/.openclaw/workspace/zero-xxx/` |
