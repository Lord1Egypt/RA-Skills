# brightdata-research

基于 BrightData + 飞书 lark-cli 的批量调研 skill，为 Claude Code 提供"搜索 → 抓取 → 验证 → 去重 → 风险分层 → 飞书写入"一站式研究流水线。

## 链接

- GitHub：https://github.com/16Miku/brightdata-research-skill
- ClawHub：https://clawhub.ai/16miku/brightdata-research

## 功能概览

- **批量搜索**：通过 BrightData MCP 或 CLI 并行搜索多组关键词，发现候选平台
- **网页抓取**：自动抓取官网、文档、定价、条款等公开页面，提取结构化字段
- **智能去重**：域名规范化 + 品牌别名识别 + 历史文档交叉比对，避免重复写入
- **风险分层**：6 维度 checklist 打分（A/B/C 三级），替代纯主观判断
- **飞书写入**：通过 lark-cli 串行追加到飞书文档，格式稳定
- **环境自适应**：自动检测环境能力，缺失项可自动修复或明确降级

## 快速安装

### 1. 安装 skill

```bash
npx skills add https://github.com/16Miku/brightdata-research-skill -y -g
```

### 2. 配置 BrightData（搜索和抓取能力）

**方式一：MCP 服务器（推荐）**
```bash
claude mcp add --transport sse brightdata "https://mcp.brightdata.com/sse?token=<your-api-token>"
```

**方式二：BrightData CLI**
```bash
npm install -g @brightdata/cli
brightdata login
```

### 3. 配置 lark-cli（飞书写入能力）

```bash
npm install -g @larksuite/cli
npx skills add https://github.com/larksuite/cli -y -g
lark-cli config init
lark-cli auth login --recommend
```

### 4. 验证

```bash
claude mcp list                    # 检查 BrightData MCP
lark-cli auth status               # 检查飞书认证
```

## 使用方式

安装完成后，在 Claude Code 中直接用自然语言触发：

```
帮我批量找一批大模型 API 中转站，搜索+抓取+整理后追加到飞书文档
```

```
继续扩展候选池，找 5-8 个新的 OpenAI-compatible API gateway
```

```
检查飞书文档里有没有重复的中转站
```

Skill 会自动识别意图并执行完整流程。

## 执行模式

| 模式 | 条件 | 行为 |
|------|------|------|
| **Mode A** | 搜索、抓取、飞书写入均就绪 | 直接执行研究流程 |
| **Mode B** | 首次使用或缺少关键能力 | 先检查环境并自动修复，再执行 |
| **降级模式** | 缺少无法自动修复的能力 | 执行可用步骤，明确告知缺失项 |

## 标准工作流

```
Step 0. 明确目标 → Step 1. Preflight 检查 → Step 2. 制定搜索批次
    → Step 3. 并行搜索 → Step 4. 去重 → Step 5. 结构化提取
    → Step 6. 风险分层 → Step 7. 主代理收口 → Step 8. 写入飞书
```

## 风险评分体系

| 维度 | 有=1分 | 无=0分 |
|------|--------|--------|
| 可访问的官网 | 1 | 0 |
| 公开 API 文档 | 1 | 0 |
| 定价页或价格信息 | 1 | 0 |
| Terms / Privacy | 1 | 0 |
| 可查证的公司主体 | 1 | 0 |
| OpenAI-compatible 兼容证据 | 1 | 0 |

- **A 级**（5-6 分）：较低风险，资料完整
- **B 级**（3-4 分）：中风险，部分需补验
- **C 级**（0-2 分）：高风险，证据不足

## 项目结构

```
brightdata-research/
├── SKILL.md                                    # 主 skill 文件（agent 读取）
├── README.md                                   # 项目说明（人类阅读）
├── evals/
│   └── evals.json                              # 9 个场景评测用例
└── references/
    ├── brightdata-mcp-setup.md                 # BrightData MCP + CLI 配置
    ├── lark-cli-install-and-auth.md            # lark-cli 安装与认证
    ├── environment-checklist.md                # 环境 Preflight 检查清单
    ├── feishu-setup.md                         # 飞书写入规则
    ├── known-failures-and-fallbacks.md         # 失败场景与降级策略
    ├── subagent-git-prerequisites.md           # subagent 前置条件
    └── smoke-tests.md                          # 能力验证命令
```

## 前置依赖

| 组件 | 必需 | 用途 |
|------|------|------|
| Claude Code | 是 | 执行环境 |
| BrightData 账户 + API Key | 是 | 搜索和网页抓取 |
| lark-cli | 是（写飞书时） | 飞书文档读写 |
| Node.js / npm | 是 | 安装 CLI 工具 |
| git | 否 | subagent worktree 隔离（可选） |

## 评测

包含 9 个场景评测用例，覆盖：

| ID | 场景 |
|----|------|
| 0 | 标准批量搜索 + 飞书追加 |
| 1 | subagent 并行搜索 + 串行收口 |
| 2 | 指定数量候选 + 先结论后写入 |
| 3 | 新环境首次使用（Mode B） |
| 4 | 飞书不可写的降级场景 |
| 5 | 文档去重清理 |
| 6 | 用户提供历史名单去重 |
| 7 | 上下文复用续写 |
| 8 | 简短请求触发识别 |

## 许可证

MIT
