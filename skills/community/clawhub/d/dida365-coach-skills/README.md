# Dida-Coach：滴答清单 AI 任务教练

[![Stars](https://img.shields.io/github/stars/siyuanfeng636-cpu/dida365-coach-skills?style=social)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.2.0-blue.svg)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills/releases)

> **让滴答清单成为你的 AI 效率教练。**
> 不只是待办清单，而是一套覆盖目标拆解、专注执行、管理视角、复盘改进的生产力系统。

```text
"$dida-coach 帮我把'提高英语口语'拆成 3 个月计划"
```

---

## 为什么选择 Dida-Coach？

大多数 AI 效率工具止步于*创建*任务。Dida-Coach 更进一步：它能**规划**、**排程**、**追踪**、**复盘**，并从你的执行数据中**学习**，全程通过自然对话完成。

| 痛点 | Dida-Coach 的解决方案 |
| :--- | :--- |
| AI 方案停在聊天窗口，永远到不了手机上 | 通过 MCP 协议同步至滴答清单，手机、平板、手表随时可用 |
| 通用番茄钟无视任务上下文 | 根据任务类型与精力状态推荐 25 / 30 / 50 / 90 分钟时间盒 |
| 错过截止日期后无人跟进 | 闭环状态机：创建 → 执行 → 检查点 → 完成 / 重排 / 取消 |
| 复盘只是模糊的“今天感觉如何？” | 模式识别可定位何时、为何拖延，并给出自动化建议 |
| 只有执行，没有管理视角 | 新增本地生产力管控层，沉淀 dashboard、承诺、等待项、专注与周月复盘 |

---

## 核心功能

### 1. 目标拆解

将长期目标拆分为阶段性计划与可衡量的里程碑，避免“只有愿望，没有执行层”。

```text
$dida-coach 帮我把“系统学习 Rust”拆成两个月计划
```

### 2. 智能 Time-Boxing（时间盒）

每个时间盒都包含一个**可验证的交付物**，而不只是时长。

| 方法 | 专注时长 | 适用场景 |
| :--- | :--- | :--- |
| 经典番茄钟 | 25 分钟 | 快速任务、邮件批处理 |
| 弹性番茄钟 | 30 分钟 | 通用知识工作 |
| 长番茄钟 | 50 分钟 | 深度写作、编程 |
| 超日节律 | 90 分钟 | 创意工作、复杂分析 |

### 3. 全面任务管理

通过自然语言管理滴答清单：

- 查询任务、清单、筛选条件
- 创建任务、更新时间、提醒、优先级
- 标记完成、跨清单移动
- 所有写操作默认执行后回读验证

### 4. 多客户端 MCP 支持

支持 Claude Desktop、Claude Code、ChatGPT、Cursor、VS Code、OpenClaw、ClawHub 等客户端。

- 有 `Connect`、`Authorize`、`Sign in` 按钮时，优先直接点击
- OpenClaw 支持“半自动接入”：先自动写本地 MCP 配置，再点击连接
- Claude Code 仍保留 `claude mcp add` 作为兜底路径

### 5. MCP 工具路由约束

严格把用户意图映射到*真实存在的*滴答 MCP 工具名，并要求写后回读：

```text
"今天有什么任务？"   -> list_undone_tasks_by_time_query
"创建一个任务"       -> create_task -> get_task_by_id
"把任务移到工作清单" -> move_task -> get_task_by_id
"做周复盘"           -> list_completed_tasks_by_date + list_undone_tasks_by_date
```

### 6. 四种教练人格

可配置温暖鼓励型、严格教练型、理性分析型、幽默风趣型，也可在对话中临时覆盖。

### 7. 深度复盘与拖延检测

支持日复盘、周复盘、月复盘，并分析：

- 完成率与高峰时段
- 任务类型分布
- 拖延模式
- 自动化候选项
- 下阶段最小有效改进动作

### 8. 闭环状态机

每个任务都走完整闭环：

```text
已创建 -> 执行中 -> 检查点 -> 已完成
                   ↓
                已重排 -> 执行中 -> ...
                   ↓
                已取消（附原因）
```

### 9. 本地生产力管控层（v1.2.0 新增）

在滴答执行层之上，新增本地生产力系统，固定目录：

- `~/.dida-coach/productivity/`

它负责沉淀：

- `dashboard.md`：当前重点、风险、过载提醒
- `commitments/`：承诺、等待项、委派事项
- `planning/`：日计划、周计划、专注块
- `reviews/`：周复盘、月复盘
- `focus/`：专注记录、干扰模式
- `routines/`：晨间流程、收尾流程

这层**不是第二套任务数据库**，不会复制完整滴答任务库，只保存管理所需的摘要和索引。

### 10. OpenClaw 半自动接入（v1.2.0 新增）

对 OpenClaw，Dida-Coach 现在优先走半自动接入：

1. 自动把 dida365 写进 `~/.openclaw/openclaw.json`
2. 刷新或重启 OpenClaw
3. 在 MCP / Tools / 依赖面板里点击 `Connect`、`Authorize` 或 `Sign in`
4. 浏览器完成 OAuth 后回到对话继续

注意：

- 不要把 `/mcp` 当成 shell 命令
- 不要裸打开 `https://mcp.dida365.com/oauth/authorize`

### 11. 像 Getnote 一样的本地 OAuth（v1.2.0 新增）

如果你想要更接近 Getnote 的体验，也可以走**滴答开放平台本地 OAuth**：

1. 在滴答开放平台创建应用
2. 回调地址填 `http://localhost:38000/callback`
3. 使用本仓库内置 helper 生成授权链接
4. 授权成功后自动把 token 写入 `~/.dida-coach/dida-openapi.env`

这条路线适合希望“点授权后自动落盘凭证”的用户。

---

## 快速上手

### 1. 安装技能

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path .
```

安装后重启 Codex、OpenClaw 或兼容客户端。

### 2. 连接滴答清单 MCP

默认优先远程 MCP 路线：

- 服务地址：`https://mcp.dida365.com`
- OpenClaw：优先半自动接入
- 其他客户端：优先页面里的 `Connect` / `Authorize`

Claude Code 兜底命令：

```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

不同客户端的最短配置方式见：

- [`references/mcp-client-setup.md`](references/mcp-client-setup.md)

### 3. 可选：使用本地 Open API OAuth

如果你想要“像 Getnote 一样”的授权体验：

1. 去滴答开放平台创建应用
2. 回调地址填 `http://localhost:38000/callback`
3. 运行：

```bash
python3 scripts/dida_openapi_oauth.py \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --open-browser
```

详细说明见：

- [`references/openapi-auth-setup.md`](references/openapi-auth-setup.md)

### 4. 开始使用

```text
$dida-coach 帮我把今天的报告排成 2 小时时间盒
$dida-coach 告诉我今天有哪些未完成任务
$dida-coach 列出所有清单并把“买牛奶”移到生活清单
$dida-coach 复盘今天为什么效率差
$dida-coach 帮我建立生产力系统，并从现有滴答任务生成初稿
$dida-coach 看一下我当前最该推进什么
$dida-coach 帮我梳理这周承诺和等待项
$dida-coach 记录这次专注和干扰原因
$dida-coach 做月复盘，看看为什么推进不动
```

### 5. 个性化配置（可选）

编辑 `config.yaml`，可以设置：

- 默认教练人格
- 工作方法
- 提醒时间
- 本地生产力系统根目录与受管文件

---

## 时区与性能说明

- 所有“现在 / 今天 / 明天 / 还有多久 / 下午几点前”这类相对时间判断，都以用户当前本地时区为准
- 说“还有 X 分钟 / 小时”前，必须基于当前本地时间和目标绝对时间重新计算
- 含远程 MCP 的 skill 比纯本地 prompt 慢，因为远程 HTTP MCP 有网络往返，写后还会做回读校验
- 想更快时，优先用单次只读请求；批量写入时尽量一次把意图说完整

---

## 仓库结构

- [`SKILL.md`](SKILL.md)：技能入口说明
- [`skill.yaml`](skill.yaml)：技能元数据与触发器
- [`config.yaml`](config.yaml)：默认人格、工作法、提醒与本地系统配置
- [`prompts/`](prompts/)：任务管理、生产力管控、时间盒、复盘等提示词
- [`references/`](references/)：MCP 接入、开放平台 OAuth、字段语义与工具路由说明
- [`tools/`](tools/)：MCP 检测、本地配置写入、Open API OAuth、本地生产力系统逻辑
- [`scripts/`](scripts/)：本地 OAuth helper
- [`tests/`](tests/)：回归测试

## 版本

当前稳定版本：`v1.2.0`
