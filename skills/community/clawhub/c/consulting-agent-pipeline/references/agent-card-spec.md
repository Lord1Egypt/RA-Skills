# Agent Card Spec — Agent 能力卡片格式

> 每个参与项目的 Agent 在 `AGENT_REGISTRY.yaml` 中注册。编排者通过查表知道谁能做什么，新 Agent 加入只需注册一行。

## AGENT_REGISTRY.yaml 格式

```yaml
schema_version: "1.0"
created: "2026-04-09"
updated: "2026-04-14"
agents:
  - id: orion
    name: Orion
    platform: minimax-openclaw
    role: orchestrator          # orchestrator | reviewer | researcher | executor | human
    capabilities:
      - task-planning
      - milestone-tracking
      - cross-agent-coordination
      - structured-handoff-writing
    tools: []                     # Agent 不直接调工具，通过 skill 调用
    status: active
    joined: "2026-04-09"
    handoff_read_path: null       # 编排者不读 handoff，写 PROJECT_STATE
    handoff_write_path: null

  - id: claude
    name: Claude
    platform: anthropic
    role: reviewer
    capabilities:
      - language-audit
      - compliance-check
      - structured-instruction-writing
      - presentation-script
      - forbidden-terms-scanning
    tools:
      - figma-remote
      - web-search
    status: active
    joined: "2026-04-09"
    handoff_read_path: "06_Claude审核与文稿任务/00_输入说明/"
    handoff_write_path: "06_Claude审核与文稿任务/01_Claude输出/"

  - id: codex
    name: Codex
    platform: openai-codex
    role: executor
    capabilities:
      - pptx-generation
      - html-generation
      - pdf-export
      - chart-generation
      - document-generation
    tools:
      - pptxgenjs
      - puppeteer
      - ffmpeg
    status: active
    joined: "2026-04-09"
    handoff_read_path: "03_PPT框架协作包/00_导航与协作/"
    handoff_write_path: "03_PPT框架协作包/"

  - id: gemini
    name: Gemini
    platform: google-gemini
    role: researcher
    capabilities:
      - deep-research
      - technical-analysis
      - policy-research
    tools:
      - web-search
    status: active
    joined: "2026-04-10"
    handoff_read_path: "07_Gemini调研资料/"
    handoff_write_path: "07_Gemini调研资料/"

  - id: leroy
    name: Leroy
    platform: human
    role: human
    capabilities:
      - strategic-decision
      - final-approval
      - expert-judgment
    tools: []
    status: active
    joined: "2026-04-09"
    handoff_read_path: null
    handoff_write_path: null
```

## Role 定义

| Role | 职责 | 读取 | 写入 |
|------|------|------|------|
| `orchestrator` | 任务分发、进度跟踪、阻塞上报 | PROJECT_STATE | PROJECT_STATE |
| `reviewer` | 多轮审核、内容合规、措辞把关 | handoff_doc | audit handoff |
| `researcher` | 专项深度调研 | research_prompt | research_output |
| `executor` | 产物生成、版本迭代 | audit handoff | deliverable + handoff |
| `human` | 战略决策、最终审批 | all | decision_log |

## Agent 能力卡片的使用场景

### 1. 新 Agent 加入项目
```bash
# 在 AGENT_REGISTRY.yaml 末尾追加一行
- id: liu-bowei
  name: 刘柏玮
  platform: human
  role: reviewer  # ESG专项审核
  capabilities: [...]
  status: active
  joined: "2026-04-12"
```

### 2. 编排者分发任务
编排者（Orion）读取 AGENT_REGISTRY，找到 `role: researcher` 且 `status: active` 的 Agent，分发调研任务。

### 3. 交接文档自动路由
交接文档的 `receiver.agent` 字段对应 AGENT_REGISTRY 的 `id`。可写脚本自动将交接文档推送到对应 Agent 的 `handoff_read_path`。

## 首钢吉泰安项目实际注册表

```yaml
agents:
  # 北水内部
  - id: orion
    name: Orion
    platform: minimax-openclaw
    role: orchestrator
    joined: "2026-04-09"

  - id: leroy
    name: Leroy
    platform: human
    role: human
    joined: "2026-04-09"

  # 外包 Agent
  - id: claude
    name: Claude
    platform: anthropic
    role: reviewer
    joined: "2026-04-09"

  - id: codex
    name: Codex
    platform: openai-codex
    role: executor
    joined: "2026-04-09"

  - id: gemini
    name: Gemini
    platform: google-gemini
    role: researcher
    joined: "2026-04-10"

  # 客户方（轻量注册）
  - id: chen-xin
    name: 陈鑫
    platform: human
    role: reviewer  # 热管理专项
    joined: "2026-04-09"

  - id: liu-bowei
    name: 刘柏玮
    platform: human
    role: reviewer  # ESG专项
    joined: "2026-04-09"

  - id: wang-yinghe
    name: 汪颖赫
    platform: human
    role: reviewer  # 卫星图专项
    joined: "2026-04-09"
```
