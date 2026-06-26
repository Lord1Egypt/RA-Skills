# Skill Domain Landscape - 研究摘要

## 目标

梳理当前主流 Agent Skill 生态里最常见的任务领域、高频任务形态，以及社区里已经形成的 Skill、CLI、API 或 MCP 最佳实践，为 `skill-factory` 后续扩展方向提供输入。

## 本次核实对象

- OpenAI 官方：
  - Codex Skills 文档
  - `openai/skills` 仓库
- Anthropic 官方：
  - Claude Skills 帮助文档
  - `anthropics/skills` 仓库
  - 《Writing effective tools for AI agents》
- Gemini 官方与社区：
  - Gemini CLI `activate_skill` 文档
  - Gemini CLI Extensions Gallery
- 开放标准：
  - Agent Skills 文档站

本次判断的“高频”，依据是这些领域是否在多个官方目录、示例仓库和社区扩展库里反复出现，不代表真实安装量排行。

## 研究结果

### 1. 重复出现最多的任务域有 8 类

#### A. 代码仓库与工程交付

高频任务：

- 修复 PR 评论
- 排查 CI 失败
- 创建或升级 Skill、MCP、CLI
- 生成或整理开发文档

重复证据：

- OpenAI `gh-address-comments`、`gh-fix-ci`、`yeet`、`cli-creator`
- Anthropic `skill-creator`、`mcp-builder`
- Gemini 社区的 `jules`、`self-command`

#### B. 前端、设计与设计到代码

高频任务：

- 落地页和应用 UI 生成
- Figma 写入、设计系统、设计稿实现
- 视觉稿到代码
- 页面美化和改版

重复证据：

- OpenAI `frontend-skill`、`figma-use`、`figma-implement-design`
- Anthropic `frontend-design`、`canvas-design`

#### C. 浏览器自动化与 UI 测试

高频任务：

- 本地页面验证
- 截图、快照、日志排查
- 浏览器交互自动化
- 持久会话 QA

重复证据：

- OpenAI `playwright`、`playwright-interactive`、`screenshot`
- Anthropic `webapp-testing`
- Gemini 社区 `browsermcp-extension`

#### D. 文档、文件与办公产物

高频任务：

- PDF、Word、PPT、Excel 处理
- 文档抽取、清洗、重组
- 生成正式交付物
- 表格和演示文稿自动化

重复证据：

- OpenAI `pdf`、`slides`、`spreadsheet`
- Anthropic `pdf`、`docx`、`pptx`、`xlsx`

#### E. 文档检索、知识问答与研究

高频任务：

- 官方文档检索
- 产品或 API 最新信息查询
- 知识沉淀到 Notion 或类似系统
- 长文档整理与引用

重复证据：

- OpenAI `openai-docs`、`notion-research-documentation`
- Gemini 社区 `developer-knowledge`、`gemini-api-docs-mcp-ext`
- Anthropic 官方文档明确把“组织知识流程”视作 Skill 典型场景

#### F. 项目协作与业务系统集成

高频任务：

- Linear、Notion、Jira、Slack 等系统联动
- 会议纪要结构化
- 任务创建与同步
- 品牌或内部沟通流程固化

重复证据：

- OpenAI `linear`、多个 Notion 技能
- Anthropic `internal-comms`、`brand-guidelines`
- Claude Skills 帮助文档把 JIRA、Asana、Linear 任务流列为典型示例

#### G. 部署、平台与云环境操作

高频任务：

- 一键部署
- 平台脚手架
- 环境配置
- 站点发布

重复证据：

- OpenAI `vercel-deploy`、`netlify-deploy`、`render-deploy`、`cloudflare-deploy`
- Gemini 社区里大量 MCP/命令扩展围绕数据库、云平台和开发工具展开

#### H. 安全、合规与风险检查

高频任务：

- 威胁建模
- 安全 ownership 梳理
- 安全调查和告警处理
- 代码与依赖风险排查

重复证据：

- OpenAI `security-best-practices`、`security-threat-model`、`security-ownership-map`
- Gemini 社区 `google-secops`
- Anthropic 工具设计文章把真实故障排查、日志调查作为强评测任务示例

### 2. Skill 的高频任务并不等于“所有动作都塞进 Skill”

当前社区更稳定的分层是：

- Skill 负责流程、边界、触发条件、策略约束
- CLI 负责本地可重复、可确定的执行动作
- API 或 MCP 负责外部系统访问和状态读写

这个分层在 OpenAI、Anthropic、Gemini 三侧都已经很明显。

### 3. 当前最稳定的 Skill 组合方式是“Skill + 执行面”

常见组合：

- Skill + `gh` / GitHub API
- Skill + Playwright / Browser MCP / 浏览器 CLI
- Skill + Figma MCP
- Skill + 文档脚本
- Skill + Notion / Linear / Slack API 或 MCP
- Skill + 部署平台 CLI

只写提示词、不绑定执行面，适合轻流程。
一旦进入真实生产任务，社区主流做法已经转向“技能描述 + 可调用执行面”。

### 4. 当前最值得优先建设的方向

对 `skill-factory` 来说，优先级建议如下：

#### 第一层

- 代码仓库与工程交付
- 浏览器自动化与 UI 测试
- 前端、设计与设计到代码
- 文档、文件与办公产物
- 文档检索、知识问答与研究

#### 第二层

- 项目协作与业务系统集成
- 部署、平台与云环境操作
- 安全、合规与风险检查

#### 第三层

- 音频、语音、视频、图像等多模态场景
- 强行业属性的企业内专用流程

## 研究结论

后续 `skill-factory` 适合把“任务域识别”提升成正式入口步骤。

在进入具体方案设计前，先判断：

- 当前需求属于哪一个主任务域
- 是否跨多个任务域
- 该任务更适合 Skill-only、Skill + CLI，还是 Skill + API/MCP
- 社区里是否已有成熟范式可直接复用

如果后续只做一轮扩展，最值得先做的是：

- 建立任务域目录
- 为每个任务域沉淀高频任务模板
- 为每个任务域绑定推荐的 Skill、CLI、API/MCP 执行面

## 主要来源

- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- OpenAI Skills Repo: https://github.com/openai/skills
- Claude Skills Overview: https://support.claude.com/en/articles/12512176-what-are-skills
- Anthropic Skills Repo: https://github.com/anthropics/skills
- Anthropic Tool Design: https://www.anthropic.com/engineering/writing-tools-for-agents
- Gemini CLI `activate_skill`: https://geminicli.com/docs/tools/activate-skill/
- Gemini Extensions Gallery: https://geminicli.com/extensions/
- Agent Skills Scripts Guide: https://agentskills.io/skill-creation/using-scripts
