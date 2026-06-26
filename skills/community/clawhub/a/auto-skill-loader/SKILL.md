---
name: auto-skill-loader
version: "2.0.1"
level: protected
description: >
  自动检测当前任务类型，动态加载对应的 Skill。当收到新任务时，分析任务意图，
  匹配最佳 Skill 并自动加载。支持 Skill 分级保护（core/protected/dynamic），
  即插即用零配置，兼容任何 OpenClaw 部署。
  触发词："自动加载skill"、"动态加载"、"智能匹配skill"，或任何需要判断使用哪个 skill 的场景。
---

# Auto Skill Loader v2.0

> 即插即用 · 核心锁定 · 零配置

## 设计原则

1. **零配置启动** - 安装即用，不需要修改任何参数
2. **核心保护** - core 级 Skill 绝不被自动加载器干扰
3. **通用兼容** - 不假设任何 Agent 名称、路径或环境
4. **最小加载** - 只加载必要的 Skill，节省 token

---

## Skill 保护等级

每个 Skill 可在 SKILL.md frontmatter 中声明 `level`：

```yaml
---
name: my-skill
level: core    # core | protected | dynamic（默认 dynamic）
---
```

| 级别 | 标识 | 自动加载器行为 | 适用场景 |
|------|------|---------------|---------|
| 🔒 **core** | `core` | **完全跳过，不触碰** | 内存管理、行为审计、安全监控 |
| 🛡️ **protected** | `protected` | **不自动卸载，加载需显式确认** | 心跳机制、风控、proactive-agent |
| 🔄 **dynamic** | `dynamic` | **自由加载/卸载** | 天气、股票分析、文案生成等 |

**未声明 level 的 Skill 默认为 `dynamic`。**

### 内置 core Skill 白名单

即使 Skill 未声明 level，以下类型的 Skill **始终视为 core**：

- 名称包含 `memory` 的 Skill（如 memory-distiller）
- 名称包含 `audit` 或 `security` 的 Skill
- 名称包含 `proactive` 的 Skill

此白名单可通过配置文件覆盖。

---

## 执行流程

### Step 1: 扫描可用 Skill

按 OpenClaw 标准目录结构扫描，**不硬编码任何路径**：

```
# 优先级从高到低：
L1: {workspace}/.agents/skills/*/SKILL.md     # Agent 专属
L2: ~/.agents/skills/*/SKILL.md               # 全局共享
L3: {openclaw_install}/skills/*/SKILL.md      # OpenClaw 内置
L4: {openclaw_install}/extensions/*/skills/*/SKILL.md  # 扩展 Skill
```

**路径解析规则**：
- `{workspace}` = 当前工作目录（自动检测）
- `~` = 用户主目录（跨平台兼容）
- `{openclaw_install}` = OpenClaw 安装目录（通过 `npm root -g` 或环境变量检测）

### Step 2: 解析 Skill 元数据

读取每个 SKILL.md 的 frontmatter：
- `name` - Skill 名称
- `description` - 功能描述（用于意图匹配）
- `level` - 保护等级（默认 dynamic）
- `version` - 版本号（可选）

**只解析 frontmatter，不读取全文（节省 token）。**

### Step 3: 过滤受保护 Skill

```
可加载列表 = 所有 Skill - core Skill - protected Skill（除非显式请求）
```

### Step 4: 意图匹配

根据用户消息，从可加载列表中匹配：

**匹配策略**（优先级从高到低）：

| 优先级 | 策略 | 说明 |
|--------|------|------|
| P1 | **触发词匹配** | 消息包含 Skill description 中的触发词 |
| P2 | **语义匹配** | 消息意图与 description 语义相近 |
| P3 | **领域匹配** | 消息领域与 Skill 领域一致 |

**冲突解决**：
- 同名 Skill → 高层级目录优先（L1 > L2 > L3 > L4）
- 多个匹配 → 选最具体的（description 最相关的）
- 无匹配 → 不加载任何 Skill，正常回复

### Step 5: 加载执行

找到匹配 Skill 后：
1. 读取完整 `SKILL.md`
2. 按其指导执行任务
3. 如需要，加载 `scripts/` 或 `references/` 下的资源

### Step 6: Agent 路由（可选）

如果任务不属于当前 Agent 的职责范围，尝试动态路由给其他 Agent：

**路由流程**：
1. 调用 `agents_list` 获取当前可用 Agent 列表
2. 读取各 Agent 的 `SOUL.md` 或 `IDENTITY.md` 判断职责匹配度
3. 找到最匹配的 Agent，通过 `sessions_send` 转发任务

**路由失败处理**：

以下情况视为"无法发现其他 Agent"：
- `agents_list` 返回空列表（单 Agent 部署）
- `agents_list` 报错（服务异常）
- 返回的 Agent 列表中只有当前 Agent 自己
- 其他 Agent 的 SOUL.md/IDENTITY.md 无法读取或职责不匹配

**此时应直接回复用户，告知路由失败**：

```
这个任务更适合 [目标 Agent 类型，如：A股量化专家/P哥] 处理。

但当前环境无法自动路由：[具体原因]
- 原因 A：当前是单 Agent 部署，未发现其他 Agent
- 原因 B：其他 Agent 未配置或不在线
- 原因 C：无法读取其他 Agent 的职责描述

**你可以：**
1. 直接 @[目标 Agent 名] 联系他
2. 让我在当前 Agent 尝试处理（可能不够专业）
3. 检查其他 Agent 是否已启动并配置正确
```

**为什么不静默 fallback？**
- 避免用户误以为任务已转发，实际没有
- 诚实透明，不给虚假希望
- 让用户掌握控制权，决定下一步

---

## 配置文件（可选）

文件：`auto-skill-loader.config.yaml`  
位置：Skill 目录内 或 workspace 根目录

```yaml
# auto-skill-loader.config.yaml
# 所有字段可选，均有合理默认值

# 额外标记为 core 的 Skill（名称列表）
coreSkills: []
  # - my-custom-audit-skill
  # - my-critical-skill

# 排除不参与自动加载的 Skill（名称列表）
skipSkills: []
  # - deprecated-skill

# 是否启用 Agent 路由（默认 true）
enableRouting: true

# 匹配模式：strict（仅触发词）| normal（触发词+语义）| fuzzy（全部）
matchMode: normal

# 日志级别：silent | info | debug
logLevel: info
```

**不创建此文件 = 使用全部默认值 = 直接能用。**

---

## 使用示例

### 场景 1：用户问天气
```
用户：北京今天天气怎么样？
→ 匹配 weather skill（dynamic）
→ 自动加载 weather/SKILL.md
→ 按其指导获取天气
```

### 场景 2：触及 core Skill
```
用户：关闭记忆管理
→ 检测到 memory-distiller 是 core 级
→ 拒绝操作，提示：此 Skill 为核心级，不可自动卸载
```

### 场景 3：无匹配
```
用户：帮我写一首诗
→ 无 Skill 匹配
→ 正常回复（不加载任何 Skill）
```

---

## Dry Run 模式

预览匹配结果，不实际加载：

在消息中包含 `--dry-run` 或在配置中设置：

```yaml
dryRun: true  # 全局 dry run
```

输出格式：
```
🔍 Auto Skill Loader - Dry Run
任务: "北京今天天气怎么样"
匹配: weather (dynamic, L3, score: 0.95)
候选: [weather, summarize]
操作: 将加载 weather/SKILL.md
```

---

## 兼容性

| 环境 | 支持 |
|------|------|
| Windows | ✅ |
| macOS | ✅ |
| Linux | ✅ |
| 单 Agent | ✅ |
| 多 Agent | ✅ |
| ClawHub 安装 | ✅ |
| 手动安装 | ✅ |

---

## 变更日志

### v2.0 (2026-03-19)
- 🔒 新增 Skill 三级保护机制（core/protected/dynamic）
- 🔌 移除所有硬编码（Agent 名称、路由表、路径）
- ⚙️ 新增可选配置文件（零配置也能用）
- 🏷️ 新增 dry-run 预览模式
- 🌍 通用化：兼容任何 OpenClaw 部署

### v1.0 (2026-03-18)
- 初始版本，基本自动加载功能
