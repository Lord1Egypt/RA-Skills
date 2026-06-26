# Skill Domain Landscape - 参考 Skill 与执行面分析

## 分析口径

本次不追求把所有 Skill 全量展开，而是抽样核对三类对象：

- 官方 Skill 目录里的代表性 Skill
- 官方文档里明确提到的使用场景
- 社区扩展里已经成型的执行面

## 1. 代码仓库与工程交付

### 代表对象

- OpenAI `gh-address-comments`
- OpenAI `gh-fix-ci`
- Anthropic `skill-creator`
- Anthropic `mcp-builder`
- Gemini 社区 `jules`

### 值得复用的能力

- 明确触发条件，避免误触发
- 把“先分析、再改动”的节奏写进 Skill
- 把 GitHub、MCP、CLI 等外部执行面当成正式依赖
- 对审批、认证、风险边界做前置约束

### 设计要点

- 这类 Skill 很少独立工作，几乎都要接 GitHub CLI、GitHub API、MCP SDK 或本地脚本
- 说明文案都很具体，触发场景边界清楚
- 高价值任务集中在 PR、CI、代码生成、MCP/Skill 创建这几个环节

### 适合 `skill-factory` 复用的抽象

- Repo workflow
- Review and repair
- Builder workflow
- Eval and benchmark

## 2. 前端、设计与设计到代码

### 代表对象

- OpenAI `frontend-skill`
- OpenAI `figma-use`
- OpenAI `figma-implement-design`
- Anthropic `frontend-design`
- Anthropic `canvas-design`

### 值得复用的能力

- 明确区分“做视觉设计”和“实现代码”
- 把 Figma 写入、设计系统、设计稿实现拆成不同 Skill
- 对视觉方向、组件复用、移动端适配给出硬约束

### 设计要点

- 这一类 Skill 的价值不只是生成界面，更重要的是固定设计决策方式
- 社区已经形成“设计 Skill + Figma 执行面 + 前端实现 Skill”的组合
- 风格要求、品牌要求、设计系统依赖需要写进 Skill，而不是临时补充

### 适合 `skill-factory` 复用的抽象

- Visual design
- Design-to-code
- Design system operations
- Frontend polish

## 3. 浏览器自动化与 UI 测试

### 代表对象

- OpenAI `playwright-interactive`
- OpenAI `playwright`
- Anthropic `webapp-testing`
- Gemini 社区 `browsermcp-extension`

### 值得复用的能力

- 持久浏览器会话
- 结构化截图、日志、快照
- 本地页面验证
- 浏览器执行和 Skill 指南分层

### 设计要点

- 这一类场景天然依赖执行面，单纯 Skill 文本远远不够
- 社区分成三种稳定路线：Playwright、本地 Browser CLI、Browser MCP
- 适合把“截图、快照、日志、等待、表单操作”做成通用检查清单

### 适合 `skill-factory` 复用的抽象

- Browser automation routing
- UI regression checklist
- Login-state decision
- Visual QA

## 4. 文档、文件与办公产物

### 代表对象

- OpenAI `pdf`
- OpenAI `slides`
- Anthropic `pdf`
- Anthropic `docx`
- Anthropic `pptx`
- Anthropic `xlsx`

### 值得复用的能力

- 触发条件极清楚，通常按文件类型触发
- 工具链稳定，输入输出契约也稳定
- 文档处理从读取、重排、抽取到生成都有成熟套路

### 设计要点

- 这是最适合沉淀为“文件型 Skill”的方向之一
- Skill 负责识别任务和组织步骤，脚本负责具体文件变换
- 用户常常只描述交付物，不会主动说文件格式，所以 Skill 需要把触发词写足

### 适合 `skill-factory` 复用的抽象

- File-type skill template
- Document transform flow
- Office artifact generation

## 5. 文档检索、知识问答与研究

### 代表对象

- OpenAI `openai-docs`
- OpenAI `notion-research-documentation`
- Gemini 社区 `developer-knowledge`
- Gemini 社区 `gemini-api-docs-mcp-ext`

### 值得复用的能力

- 优先查官方文档
- 限定来源范围
- 把引用和链接作为结果的一部分
- 用 MCP 或文档索引降低“知识过时”风险

### 设计要点

- 这是最适合“Skill + 检索执行面”的方向
- 当问题涉及时效性、规范或 SDK 细节时，必须优先官方来源
- 如果已有官方 MCP 或结构化文档接口，优先用它，而不是泛搜索

### 适合 `skill-factory` 复用的抽象

- Docs-first research
- Source restriction policy
- Citation-required workflow

## 6. 项目协作与业务系统集成

### 代表对象

- OpenAI `linear`
- OpenAI 多个 Notion 技能
- Anthropic `internal-comms`
- Anthropic `brand-guidelines`

### 值得复用的能力

- 把组织规则、品牌规则、会议和任务流写成可复用流程
- 结合 Notion、Linear、Jira、Slack 等业务系统
- 让 Skill 承载团队共识，而不是只承载操作步骤

### 设计要点

- 这一类 Skill 更偏“组织知识封装”
- 通常需要连接器、API 或 MCP 才能真正执行
- 任务频率高，但组织差异很大，适合做模板，不适合写死

### 适合 `skill-factory` 复用的抽象

- Team workflow
- Knowledge capture
- Branded writing
- Meeting-to-task flow

## 7. 部署、平台与云环境操作

### 代表对象

- OpenAI `vercel-deploy`
- OpenAI `netlify-deploy`
- OpenAI `render-deploy`
- OpenAI `cloudflare-deploy`

### 值得复用的能力

- 把平台差异收敛到 Skill 内部
- 结合平台 CLI 或 API 做确定性发布
- 用 Skill 约束发布前检查和参数准备

### 设计要点

- 这类方向很适合“平台模板 + CLI 约束”
- 如果目标平台足够明确，Skill 的触发精度会很高
- 风险在凭据、环境变量和误发布，需要显式安全步骤

### 适合 `skill-factory` 复用的抽象

- Platform-specific template
- Deploy checklist
- Credential gate

## 8. 安全、合规与风险检查

### 代表对象

- OpenAI `security-best-practices`
- OpenAI `security-threat-model`
- OpenAI `security-ownership-map`
- Gemini 社区 `google-secops`

### 值得复用的能力

- 风险识别框架
- 责任归属梳理
- 调查流程模板
- 安全任务的证据化输出

### 设计要点

- 这类 Skill 更像专业流程框架
- 通常要和日志系统、告警系统、代码仓库、工单系统联动
- 输出需要保留结构化证据，方便复核

### 适合 `skill-factory` 复用的抽象

- Risk review
- Threat model checklist
- Incident investigation flow

## 汇总结论

当前社区里已经很清楚的模式有三条：

1. Skill 用来固化任务分解、触发边界、判断规则和输出要求。
2. CLI 用来承接本地确定性动作，特别适合文件、部署、Git、浏览器、脚本场景。
3. API 或 MCP 用来连接真实外部系统，特别适合文档、业务系统、平台服务和知识检索。

对 `skill-factory` 来说，后续更值得沉淀的是这三类内容：

- 每个任务域的高频任务模板
- 每个任务域的推荐执行面
- 每个任务域的风险边界和触发提示
