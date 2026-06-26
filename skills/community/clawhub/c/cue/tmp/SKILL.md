# Cue - 你的专属调研助理 / Your AI Research Assistant

统一入口和智能路由中心，自动识别用户意图并路由到相应技能。基于 Cue 产品设计，提供专业化的深度研究体验。

> A unified entry and intelligent routing center that automatically recognizes user intent and routes to appropriate skills. Based on Cue product design, providing professional deep research experience.

## ⚠️ 安全声明 / Security Notice

**安装前请仔细阅读 / Please read before installing:**

本 Skill 是一个具有持久化状态和后台行为的金融研究+监控工具：
- 🔐 **本地存储 / Local Storage**: 会在 `$HOME/.cuecue` 创建持久化数据目录（用户数据、任务、监控配置、日志）
- ⏰ **后台任务 / Background Jobs**: 安装后会添加 cron 定时任务（每30分钟运行监控守护进程）
- 🌐 **外部 API / External APIs**: 需要访问 https://cuecue.cn 和可选的 https://api.tavily.com
- 🔑 **环境变量 / Environment Variables**: 需要 CUECUE_API_KEY（必需），可选 TAVILY_API_KEY
- 📢 **通知权限 / Notification**: 可能复用 OpenClaw 渠道令牌（如 FEISHU_*）发送通知

**This Skill is a financial research + monitoring tool with persistent state and background behavior:**
- Creates persistent local storage at `$HOME/.cuecue` (user data, tasks, monitors, logs)
- Installs cron job running every 30 minutes for monitoring
- Requires external API access to https://cuecue.cn
- Requires CUECUE_API_KEY (required), optional TAVILY_API_KEY
- May reuse OpenClaw channel tokens (e.g., FEISHU_*) for notifications

## Tags

deep-research, finance, business, industry, company-analysis, multi-agent, monitoring

---

## 中文说明 / Description

### 核心定位 / Core Positioning

**Cue** 是一款面向专业场景的 AI 调研助理，不只是给答案，还提供完整的证据链和可溯源的研究过程。

> **Cue** is an AI research assistant for professional scenarios. It doesn't just provide answers, but also offers complete evidence chains and traceable research processes.

### 核心价值 / Core Values

- 🔍 **低幻觉 / Low Hallucination** - 全局事实校验，多源交叉验证 / Global fact-checking with multi-source cross-validation
- 🔗 **可溯源 / Traceable** - 每个结论都有来源和证据链 / Every conclusion has sources and evidence chains
- 🤖 **Multi-Agent** - 自动搜集、验证、分析 / Automatic collection, verification, and analysis
- 💾 **可复用 / Reusable** - 优秀调研路径能沉淀为模板 / Excellent research paths can be templated

### 核心功能 / Core Functions

#### 1. 深度研究（Deep Research）

直接输入研究主题，AI 自动进行多 Agent 并行深度研究，40-60 分钟生成专业分析报告。

> Enter a research topic directly, and AI will automatically conduct multi-agent parallel deep research, generating professional analysis reports in 40-60 minutes.

**示例 / Examples:**
```
分析宁德时代竞争优势
新能源汽车行业前景如何？
```

#### 2. 研究视角模式 / Research Perspective Modes

系统根据主题自动匹配最适合的研究视角，生成结构化的调研指令（rewritten_mandate 格式）：

> System automatically matches the best research perspective and generates structured research mandate:

| 模式 / Mode | 自动匹配关键词 / Auto-match Keywords | 研究框架 / Framework |
|------------|-------------------------------------|---------------------|
| 短线交易 / Trader | 龙虎榜、涨停、游资、资金流向、换手率 | 市场微观结构与资金流向分析（Timeline Reconstruction） |
| 基金经理 / Fund Manager | 财报、估值、业绩、年报、ROE、PE | 基本面分析与估值模型框架 |
| 研究员 / Researcher | 产业链、竞争格局、技术路线、供应链 | 产业链拆解与竞争力评估（Peer Benchmarking） |
| 理财顾问 / Advisor | 投资建议、资产配置、风险控制、定投 | 资产配置与风险收益评估框架 |

**提示词格式 / Prompt Format:**
系统自动生成包含以下字段的深度调研指令：
- **【调研目标】** - 明确专家角色与研究目的
- **【信息搜集与整合框架】** - 指定搜索方法论（Timeline/Triangulation/Benchmarking/Evidence Chaining）
- **【信源与边界】** - 白名单/黑名单信源、时间窗口
- **【核心关注】** - 该视角下的重点分析维度

**使用方式 / Usage:**
```
/cue 今日龙虎榜分析           # 自动识别为短线交易视角
/cue --mode trader 涨停分析   # 手动指定短线交易视角
/cue 宁德时代2024财报          # 自动识别为基金经理视角
```

**示例输出 / Example Output:**
```
**【调研目标】**
以短线交易分析师的专业视角，针对"今日龙虎榜分析"进行全网深度信息搜集与分析...

**【信息搜集与整合框架】**
1. **市场微观结构与资金流向分析框架（Timeline Reconstruction）**：追踪龙虎榜席位动向...
2. **关键证据锚定**：针对核心争议点，查找并引用权威信源...
3. **多维视角交叉**：汇总不同利益相关方的观点差异...

**【信源与边界】**
- 优先信源：交易所龙虎榜、Level-2行情数据...
- 时间窗口：优先近6个月内的最新动态
```

#### 3. 智能路由 / Intelligent Routing

直接输入自然语言，系统自动判断最佳方案：

> Enter natural language directly, and the system automatically determines the best approach:

- 投资/产业关键词 → 深度研究 / Investment/industry keywords → Deep research
- 简单查询 → 快速搜索 / Simple queries → Quick search
- 估值关键词 → 基金经理模式 / Valuation keywords → Fund manager mode

### 可用命令 / Available Commands

| 命令 / Command | 功能 / Function | 耗时 / Duration |
|---------------|----------------|----------------|
| `/cue <主题>` | 智能调研（自动匹配研究视角）/ Smart research (auto-matches perspective) | 40-60 分钟 / mins |
| `/cue --mode <模式> <主题>` | 指定视角深度研究 / Deep research with specific perspective | 40-60 分钟 / mins |
| `/ct` | 查看所有研究任务状态 / View all research task statuses | 即时 / Instant |
| `/cm` | 查看监控项列表 / View all monitors | 即时 / Instant |
| `/cn [天数]` | 查看监控触发通知（默认3日）/ View monitor notifications | 即时 / Instant |
| `/cs <任务ID>` | 查看特定任务详情 / View specific task details | 即时 / Instant |
| `/ch` | 显示帮助 / Show help | 即时 / Instant |
| `/config` | 配置 API Key / Configure API keys | 即时 / Instant |

### 使用示例 / Usage Examples

**自然语言（推荐）/ Natural Language (Recommended):**
```
分析一下新能源行业竞争格局
基金经理视角分析茅台投资价值
```

**显式命令 / Explicit Commands:**
```
/cue 特斯拉 2024 财务分析
/cue --mode researcher 锂电池产业链
```

### 工作流程 / Workflow

```
用户输入 / User Input
    ↓
[Cue 智能路由 / Intelligent Routing]
    ↓
深度研究启动 / Research Started
    ↓
├─ 立即返回：任务ID + 进度链接 / Return: Task ID + Progress Link
├─ 每5分钟推送进度更新 / Progress update every 5 minutes
└─ 60分钟超时保护 / 60-minute timeout protection
    ↓
研究完成 / Research Completed
    ↓
自动推送结果 / Auto-push results
├─ 分享链接（分享对话/转发报告）/ Share links
├─ 核心结论摘要 / Core conclusion summary
└─ 监控项建议（回复 Y/N 创建）/ Monitor suggestions (Reply Y/N to create)
```

### 用户体验特性 / User Experience Features

**首次使用引导 / First-time User Guide:**
- 自动识别新用户并发送欢迎消息 / Auto-detects new users and sends welcome message
- 检测 API Key 配置状态，引导注册流程 / Detects API Key status and guides registration

**异步体验 / Asynchronous Experience:**
- 研究启动后立即返回进度链接 / Returns progress link immediately after starting
- 每 5 分钟推送进度更新 / Progress updates every 5 minutes
- 无需等待，可继续其他工作 / No need to wait, can continue other work
- 完成后自动推送结果到对话 / Auto-pushes results to conversation when completed

**详细进度追踪 / Detailed Progress Tracking:**
```
🔬 正在深度研究：[主题]

研究阶段：
• 0-10分钟：全网信息搜集与初步筛选
• 10-30分钟：多源交叉验证与事实核查
• 30-50分钟：深度分析与逻辑推理
• 50-60分钟：报告生成与质量检查

预计剩余时间：XX 分钟
```

**完成通知 / Completion Notification:**
研究完成后自动发送简洁通知：
> Auto-sends concise notification when research completes:
```
✅ 研究完成：[主题]

⏱️ 耗时：XX 分钟
📝 任务ID：xxx

🔗 https://cuecue.cn/c/xxx

🔔 建议监控：XX 等 N 项
💡 回复 Y 创建，N 跳过
```

### 部署方式 / Deployment Methods

**方式一：使用公共机器人服务 / Method 1: Use Public Bot Service**

使用他人部署的 Cue 机器人（如飞书群里的公共机器人），直接开始对话即可。

> Use Cue bot deployed by others (e.g., in Feishu groups), just start chatting.

**方式二：自建 OpenClaw + Cue Skill / Method 2: Self-host OpenClaw + Cue Skill**

在自己的 OpenClaw 实例中安装 Cue skill：

> Install Cue skill in your own OpenClaw instance:

```bash
clawhub install cue
```

**首次使用流程 / First-time Setup:**

1. **发送任意消息** → 触发欢迎消息
2. **获取 API Key** → 按提示访问 cuecue.cn 注册
3. **配置环境变量** → 设置 `CUECUE_API_KEY`
4. **开始研究** → 发送研究主题

```bash
# 配置环境变量
export CUECUE_API_KEY="your-api-key"
```

**推荐 / Recommended**：自建部署获得完整功能和最佳体验。
> Self-hosting for full functionality and best experience.

### 超时设置 / Timeout Settings

- **研究超时 / Research Timeout**：60 分钟 / minutes
- **进度推送间隔 / Progress Push Interval**：5 分钟 / minutes
- 超时后自动标记失败，支持重试 / Auto-marked as failed after timeout, supports retry

### 环境变量 / Environment Variables

```bash
CUECUE_API_KEY      # CueCue API 密钥（必需）/ API Key (Required)
```

### 智能监控 / Smart Monitoring

**监控建议生成 / Monitor Suggestion Generation:**
- 🤖 **AI 分析**：从报告中提取关键监控信号
- 📊 **量化指标**：提取可量化的监控维度
- 🔔 **自动创建**：回复 Y 自动创建监控项

**监控执行与触发 / Monitor Execution & Trigger:**
```
监控创建 → 监控执行 → 条件评估 → 触发通知
    ↓           ↓           ↓           ↓
 create    monitor    condition   notify
-monitor   -daemon    -evaluator  -trigger
```

**执行层级 / Execution Layers:**
1. **Search 层**：通过搜索获取信息（快速）
2. **Browser 层**：通过浏览器获取信息（深度）
3. **触发评估**：判断是否满足触发条件
4. **通知推送**：自动发送触发通知

**调度配置 / Scheduling:**
- 监控守护进程每30分钟执行一次
- 支持 Cron 表达式自定义频率
- 自动清理7天前的旧日志

### 脚本说明 / Script Descriptions

**核心脚本 / Core Scripts:**
- `scripts/cue.sh` - 主入口脚本，智能路由 / Main entry, intelligent routing
- `scripts/research.sh` - 深度研究执行（60分钟超时）/ Deep research execution (60min timeout)
- `scripts/notifier.sh` - 完成通知（含分享链接提取）/ Completion notification (with share link extraction)
- `scripts/cuecue-client.js` - 内置 API 客户端（Node.js，无额外依赖）/ Built-in API client (Node.js, no external deps)

**监控相关 / Monitoring:**
- `scripts/create-monitor.sh` - 监控项创建 / Monitor item creation
- `scripts/monitor-daemon.sh` - 监控守护进程（调度执行）/ Monitor daemon (scheduling)
- `scripts/monitor-notify.sh` - 监控触发通知 / Monitor trigger notification

**执行引擎 / Execution Engine:**
- `scripts/executor/monitor-engine.sh` - 监控执行主控 / Monitor execution controller
- `scripts/executor/search-executor.sh` - 搜索执行器 / Search executor
- `scripts/executor/browser-executor.sh` - 浏览器执行器 / Browser executor

---

## 环境变量与权限 / Environment Variables & Permissions

### 必需环境变量 / Required

| 变量名 | 说明 | 获取方式 |
|--------|------|---------|
| `CUECUE_API_KEY` | CueCue 深度研究 API 密钥 | https://cuecue.cn |

### 可选环境变量 / Optional

| 变量名 | 说明 | 用途 |
|--------|------|------|
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 | 监控功能的新闻搜索 |
| `FEISHU_APP_ID` | 飞书应用 ID | 飞书渠道通知 |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | 飞书渠道通知 |
| `OPENCLAW_CHANNEL` | OpenClaw 渠道标识 | 消息发送渠道选择 |
| `CHAT_ID` | 当前对话 ID | 用户识别和数据隔离 |

### 权限说明 / Permissions

**本 Skill 需要以下权限 / This Skill requires:**

1. **文件系统权限 / Filesystem**
   - 读写 `$HOME/.cuecue` 目录及其子目录
   - 创建用户数据、任务、监控配置和日志文件

2. **网络权限 / Network**
   - 出站访问 https://cuecue.cn (深度研究 API)
   - 出站访问 https://api.tavily.com (可选，监控搜索)

3. **定时任务权限 / Cron**
   - 安装 cron 作业（每30分钟执行监控检查）
   - 运行后台研究进程（60分钟超时）

4. **环境变量访问 / Environment**
   - 读取 OpenClaw 环境变量（如 FEISHU_APP_ID, CHAT_ID）
   - 读取用户配置的 API Key

**安装建议 / Installation Recommendation:**
- 初次安装请在测试环境验证
- 检查并批准 cron 作业和文件系统写入权限
- 确认 API Key 和网络访问策略
- 了解监控功能会定期产生外部 API 调用

---

*Cue - 让 AI 成为你的调研助理 / Let AI be your research assistant (Powered by CueCue)*

### 数据隔离 / Data Isolation

**多用户数据安全隔离**

每个用户的数据存储在独立目录：
```
~/.cuecue/users/${chat_id}/
├── .initialized     # 用户初始化标记
├── tasks/           # 用户专属研究任务
└── monitors/        # 用户专属监控配置
```

**安全特性**：
- ✅ 用户数据完全隔离
- ✅ 多用户共享实例时互不干扰
- ✅ 通过 chat_id 识别用户身份

---

## 版本历史 / Version History

### v1.0.4 (2026-02-25)
- 🔧 全面 Node.js 重构 - 基于 ES Module 的现代架构
- 🔧 模块化设计 - core/api/commands/utils 清晰分层
- 🔧 统一日志系统 - 支持多级别日志和文件持久化
- 🔧 改进错误处理 - 详细的错误信息和日志记录
- 🔧 Type hints - JSDoc 类型注解提升可维护性
- 🔧 依赖管理 - 使用 npm 管理 Node.js 依赖

### v1.0.3 (2026-02-25)
- ✨ 新增：自动角色匹配 - 根据主题关键词智能选择研究视角（trader/fund-manager/researcher/advisor）
- ✨ 新增：rewritten_mandate 提示词格式 - 结构化调研指令（目标/框架/信源/关注）
- ✨ 新增：/cn 命令 - 查看监控触发通知（默认最近3日）
- ✨ 新增：/key 命令 - 交互式 API Key 配置，自动识别服务类型
- ✨ 新增：智能状态检测 - 首次使用/版本更新/正常使用三种状态
- 🔧 修复：监控触发通知自动保存到用户目录
- 🔧 优化：trader 模式支持龙虎榜、资金流向等短线交易分析
- 📚 更新：SKILL.md 文档，添加新功能说明

### v1.0.2 (2026-02-24)
- 🔧 修复：API 调用错误（使用内置 cuecue-client.js）
- 🔧 修复：PID 获取污染问题
- 🔧 修复：输出文件分离导致的 notifier 错误
- 🔧 修复：退出码标记格式不一致
- ✨ 新增：内置 Node.js API 客户端（无额外依赖）

### v1.0.1 (2026-02-24)
- ✨ 产品定位："投研搭子" → "调研助理"
- 🏷️ 新增 7 个 Tags
- ⏱️ 优化：超时 30min → 60min
- 🔔 增强：5分钟进度推送
- 🔗 新增：自动提取分享链接
- 🤖 智能：回复 Y 自动创建监控
- 🌐 新增：多 Channel 支持
- 📝 新增：详细日志系统

### v1.0.0 (2026-02-23)
- 🎉 初始发布
- 深度研究功能
- 监控管理功能

