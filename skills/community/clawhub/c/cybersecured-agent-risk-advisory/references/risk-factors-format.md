# 风险因子收集格式

> 本地安全扫描阶段需要生成的 JSON 文件格式和收集提示词。在阶段二（安全扫描）按需阅读本文件。

---

## 目录命名

在 `./assessments/` 下创建子目录，使用当前时间命名：

格式：`YYYYMMDD-HHMMSS`
示例：`./assessments/20260322-143052/`

---

## CLI 自动生成的文件

执行 `cybersecured-agent scan run --output-dir ./assessments/YYYYMMDD-HHMMSS` 后，CLI 自动生成以下文件：

| 文件名 | 说明 |
|--------|------|
| `cli-scan-system.json` | 操作系统、硬件、Python 版本等系统信息 |
| `cli-scan-skills.json` | 已安装的 skills 列表（扫描常见技能目录，包含 Codex `~/.codex/skills` 与 Claude Code `~/.claude/skills`） |
| `cli-scan-plugins.json` | 已安装的 plugins 列表（扫描 MCP 配置） |

**无需手动收集这些文件。**

---

## 需要手动收集的文件

以下文件需要 Agent 按照提示词主动收集并写入对应 JSON 文件：

---

## basic-risk-factors.json

### 提示词

请收集当前 Agent 的基本识别信息：

1. **当前时间**：获取当前 UTC 时间，格式 ISO 8601
2. **宿主软件名称**：你当前运行在哪个软件中？（例如：Codex、Claude Code、Kimi-CLI、OpenClaw、OpenCode、Cursor、Dify、Coze、AutoGen 等）
3. **宿主软件版本**：该软件的版本号是什么？
4. **模型信息**：
   - **模型名称**：你当前使用的 AI 模型名称（如 gpt-4、kimi-k2、claude-3-opus）
   - **模型提供商**：模型由哪家公司提供（如 OpenAI、Anthropic、月之暗面、阿里、腾讯、百度）
   - **模型网关**：你是否通过某个网关或代理访问模型？（如自建网关、Azure OpenAI、AWS Bedrock、Cloudflare AI Gateway）如果没有直接访问模型 API，填写 "none"
5. **使用频率**：你平均每天与用户交互多少次？（数字）
6. **入口点**：用户通过什么方式与你交互？（例如：命令行、Web 界面、API 调用、IDE 插件、Slack、Discord、微信、钉钉等）
7. **平台标识**：
   - 如果你运行在托管平台（如 Kimi、腾讯、阿里云、Coze、Dify 等），获取平台分配给你的唯一标识符（GUID、实例 ID、App ID 等）
   - 如果无法获取，记录为 null
8. **工作目录**：你当前运行的工作目录绝对路径是什么？
9. **主配置文件路径**：你的主配置文件（如果有）的绝对路径是什么？如果不确定，尝试查找常见的配置文件位置
10. **托管平台**：你的 Agent 部署在什么平台上？（如本地机器、Docker 容器、Kubernetes、阿里云函数计算、AWS Lambda、Vercel、Railway、腾讯云等）
11. **部署模式**：你的运行环境是什么类型？（如容器化、虚拟机、裸机、Serverless、PaaS、SaaS）
12. **通信通道**：你通过哪些通道与用户或外部系统通信？
    - 对每个通道，记录：通道类型（如 chat、voice、api、webhook）、通道名称（如 Slack、微信、Discord、REST API）、通道描述
13. **编排框架**：你是否使用了某种 Agent 编排框架？（如 AutoGen、LangChain、LlamaIndex、CrewAI、Dify、Coze、Flowise）如果没有，填写 "none"
14. **记忆机制**：你是否具备跨会话记忆能力？（如长期记忆、向量数据库、Redis、文件存储）如果没有，填写 "none"
15. **认证方式**：用户或系统如何验证你的身份？（如 API Key、OAuth、JWT、无认证）
16. **审计日志**：你的操作是否被记录到审计日志中？（如是、否、不确定）
17. **速率限制**：你的 API 调用或操作是否受速率限制？（如是、否、不确定）
18. **网络边界**：你运行在哪种网络环境中？（如公网可访问、内网、VPC、隔离网络）
19. **人工介入机制**：执行高风险操作前是否需要人类确认？（如总是、有时、从不、不确定）
20. **数据驻留**：用户数据存储在哪个地区？（如中国大陆、美国、欧盟、其他地区、不确定）

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "host_software_name": "Codex",
  "host_software_version": "1.2.3",
  "model_name": "gpt-5",
  "model_provider": "OpenAI",
  "model_gateway": "none",
  "usage_frequency": 15,
  "entry_point": "Codex Desktop",
  "platform_id": "platform-guid-or-instance-id",
  "workspace_dir": "/home/user/projects/myproject",
  "config_file_path": "/home/user/.codex/config.toml",
  "hosting_platform": "本地机器",
  "deployment_mode": "裸机",
  "channels": [
    {
      "channel_type": "chat",
      "channel_name": "Codex Desktop",
      "channel_description": "通过 Codex 桌面应用与用户交互"
    }
  ],
  "orchestration_framework": "none",
  "memory_mechanism": "none",
  "authentication_method": "API Key",
  "audit_logging": "否",
  "rate_limiting": "不确定",
  "network_boundary": "内网",
  "human_in_the_loop": "从不",
  "data_residency": "不确定"
}
```

字段说明：
- `model_gateway`: 访问模型时经过的网关/代理，直接访问模型 API 填 "none"
- `platform_id`: 托管平台分配的唯一标识，本地运行可填 null
- `workspace_dir`: 当前工作目录绝对路径
- `config_file_path`: 主配置文件路径，无配置文件可填 null
- `hosting_platform`: Agent 部署的目标平台
- `deployment_mode`: 运行环境类型（容器化/虚拟机/裸机/Serverless/PaaS/SaaS）
- `channels`: 通信通道列表，描述所有与用户/外部系统的交互方式
- `orchestration_framework`: 使用的 Agent 编排框架，无填 "none"
- `memory_mechanism`: 跨会话记忆机制，无填 "none"
- `authentication_method`: 身份验证方式
- `audit_logging`: 是否具备审计日志（是/否/不确定）
- `rate_limiting`: 是否受速率限制（是/否/不确定）
- `network_boundary`: 网络环境类型
- `human_in_the_loop`: 高风险操作前是否需要人类确认
- `data_residency`: 用户数据存储地区

---

## data-sources.json

### 提示词

请收集你的数据来源和输入流信息：

1. **用户输入**：用户通过什么方式给你输入？（如文本消息、语音转文本、文件上传、图片）
2. **外部数据流**：你是否接收来自外部系统的数据？（如 API 响应、数据库查询结果、网页抓取内容、邮件）
3. **文档处理**：你是否处理文档？（如 PDF、Word、Excel、代码文件）
4. **网页访问**：你是否能访问互联网网页？（是/否/通过工具间接访问）
5. **第三方集成**：你是否集成了第三方服务？（如搜索引擎、天气 API、地图服务、社交媒体）
6. **数据预处理**：输入数据是否经过预处理？（如清洗、分块、向量化、过滤）
7. **敏感数据接触**：你是否可能接触到敏感数据？（如个人信息、密码、财务数据、商业机密）

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "user_input_types": ["文本消息", "文件上传"],
  "external_data_streams": ["GitHub API", "数据库查询"],
  "document_processing": ["Markdown", "Python代码文件"],
  "web_access": "通过工具间接访问",
  "third_party_integrations": ["GitHub", "Google搜索"],
  "data_preprocessing": ["文本清洗", "代码分块"],
  "sensitive_data_exposure": "可能接触源代码"
}
```

---

## guardrails.json

### 提示词

请收集你的安全护栏（Guardrails）配置信息：

1. **输入过滤**：是否对用户输入进行安全检查？（如提示注入检测、恶意内容过滤、关键词拦截）
2. **输出过滤**：是否对输出内容进行安全过滤？（如敏感信息脱敏、有害内容拦截、格式验证）
3. **工具调用限制**：是否限制可调用的工具类型？（如禁止执行写操作、禁止访问外部网络）
4. **内容策略**：是否有明确的内容安全策略？（如禁止生成违法内容、禁止泄露隐私）
5. **速率限制**：是否对操作频率进行限制？（如每分钟最大请求数、每日最大 Token 数）
6. **异常检测**：是否有异常行为检测机制？（如检测异常工具调用模式、异常输出模式）
7. **会话隔离**：不同用户的会话是否完全隔离？（是/否/不确定）
8. **越狱防护**：是否有防止提示词越狱的机制？（如指令层级、系统提示词保护）

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "input_filtering": ["提示注入检测", "恶意代码检测"],
  "output_filtering": ["敏感信息脱敏"],
  "tool_restrictions": ["禁止文件删除", "禁止网络请求"],
  "content_policies": ["禁止生成违法内容", "禁止泄露个人隐私"],
  "rate_limits": ["每分钟最多20次工具调用"],
  "anomaly_detection": "否",
  "session_isolation": "是",
  "jailbreak_protection": "指令层级保护"
}
```

---

## multi-agent.json

### 提示词

请收集你的多 Agent 环境信息（如果不是多 Agent 系统，返回空对象）：

1. **是否多 Agent**：你是否与其他 Agent 协作？（是/否）
2. **Agent 数量**：环境中大约有多少个 Agent？（数字）
3. **协作模式**：Agent 之间如何协作？（如层级 orchestration、对等协作、Swarm 模式）
4. **通信方式**：Agent 之间如何通信？（如共享内存、消息队列、API 调用、文件交换）
5. **信任边界**：Agent 之间是否有信任边界？（如是否验证其他 Agent 的身份）
6. **权限差异**：不同 Agent 是否有不同的权限级别？（是/否）
7. **级联风险**：一个 Agent 被攻击是否会影响其他 Agent？（是/否/不确定）

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "is_multi_agent": false,
  "agent_count": 1,
  "collaboration_mode": "无",
  "communication_method": "无",
  "trust_boundaries": "不适用",
  "privilege_levels": "不适用",
  "cascade_risk": "不适用"
}
```

多 Agent 示例：

```json
{
  "time": "2026-04-29T10:00:00Z",
  "is_multi_agent": true,
  "agent_count": 3,
  "collaboration_mode": "层级 orchestration",
  "communication_method": "共享内存 + API 调用",
  "trust_boundaries": "有，通过签名验证",
  "privilege_levels": "是，orchestrator 拥有更高权限",
  "cascade_risk": "是，子 Agent 被攻击可能影响 orchestrator"
}
```

---

## compliance.json

### 提示词

请收集你的合规要求和监管信息：

1. **适用法规**：你的应用场景需要遵守哪些法规？（如中国《网络安全法》、《数据安全法》、《个人信息保护法》、GDPR、HIPAA、等保）
2. **数据分类**：你处理的数据属于什么级别？（如公开数据、内部数据、敏感数据、机密数据）
3. **行业要求**：你所在的行业是否有特殊安全要求？（如金融、医疗、政务、教育）
4. **审计要求**：是否需要接受第三方安全审计？（是/否/不确定）
5. **数据跨境**：是否有数据跨境传输？（是/否/不确定）
6. **保留期限**：用户数据保留多长时间？（如 30 天、90 天、1 年、永久、不确定）

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "applicable_regulations": ["《网络安全法》", "《数据安全法》"],
  "data_classification": "内部数据",
  "industry": "软件开发",
  "third_party_audit": "否",
  "cross_border_transfer": "否",
  "retention_period": "不确定"
}
```

---

## security-findings.json

### 提示词

请对当前 Agent 的**实际配置**进行安全检查，找出**真实增加攻击面**的具体配置缺陷。

**核心原则：**

  - **只记录已经存在的配置缺陷，不记录理论上的可能性。**
    - **正确示例**：配置文件 `config.yaml` 中 `api_key` 字段以明文存储（实际配置问题）
    - **错误示例**："如果配置文件被泄露，API Key 可能被盗用"（理论推测，不应记录）
    - **正确示例**：工具调用权限未受限，Agent 可以执行任意 shell 命令（实际能力过大）
    - **错误示例**："Agent 理论上可能被诱导执行危险命令"（理论推测，不应记录）

  - **只收集 Agent 本身的设计、配置和运行环境的安全问题，不要收集当前会话的临时操作选择。**
    - **正确示例**：Agent 的配置文件默认以明文存储敏感凭据（固有问题）
    - **错误示例**：用户本次运行添加了 `--no-verify-ssl` 参数（临时操作，不应记录）
    - **正确示例**：Agent 缺乏强制 HTTPS 证书验证的配置选项（设计缺陷）
    - **错误示例**：当前正在使用测试环境 API（环境选择，不应记录）

  - **聚焦真实攻击场景，去掉不增加实际攻击面的问题。**
    - **不记录**：LLM 输入必然经过提示词（这是架构设计，不是缺陷）
    - **不记录**：Agentic 工具允许用户输入影响工具参数（这是功能设计，不是缺陷）
    - **不记录**：抽象的"缺乏提示注入防护"（过于通用，无法作为具体配置缺陷）
    - **不记录**：加密存储的敏感信息被泄露后的风险（攻击者已获取文件，加密与否不影响结果）
    - **记录**：明文存储的 API Key、Token、密码（可直接被读取利用）
    - **记录**：过高的系统权限（一旦被控制，直接影响宿主机）
    - **记录**：未验证 SSL 证书（中间人攻击可直接利用）

**1. 访问控制**
- [ ] Agent 运行是否使用了过高的系统权限（如 root、Administrator）？
- [ ] 是否缺乏身份验证机制，任何人都可以调用 Agent？
- [ ] 配置文件是否可被其他用户读取（权限过于宽松）？

**2. 工具调用安全**
- [ ] Agent 可调用的工具范围是否过大？（如可以执行任意文件读写、网络请求、系统命令）
- [ ] 是否允许自动执行危险操作（如删除文件、修改系统配置）而无需确认？

**3. 网络安全**
- [ ] 是否允许不加密的 HTTP 通信？
- [ ] 是否未验证服务器证书（SSL verify 为 false）？
- [ ] 是否监听不必要的网络端口？

**4. 数据隔离**
- [ ] 多用户环境下是否共享同一会话或上下文？
- [ ] 用户数据是否存储在可公开访问的位置？

**5. 日志与审计**
- [ ] 是否未记录关键操作日志？
- [ ] 日志文件是否缺乏访问控制？

**记录格式要求：**

对每个实际发现的问题，记录：
- `name`：问题名称（简洁，点明具体缺陷）
- `description`：问题描述（**必须包含：具体问题是什么、在哪里发现、为何是问题**）
- `ranking`：严重程度

严重程度分级：
- `very_high`：可被直接利用导致安全事故（如明文存储生产环境密码且可被任意读取）
- `high`：显著降低安全性的配置缺陷（如以 root 权限运行、允许任意代码执行）
- `medium`：不符合最佳实践但需特定条件才能利用（如监听额外端口、日志记录敏感信息）
- `low`：轻微偏差（如旧版本组件但无已知漏洞）
- `info`：改进建议（如建议启用操作审计）

**如果没有发现实际配置问题，返回空数组。**

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "security_findings": [
    {
      "name": "API Key 明文存储",
      "description": "在配置文件中发现 API Key 以明文形式存储，未加密",
      "ranking": "high"
    }
  ]
}
```

---

## scenarios.json

### 提示词

请分析该 Agent 被设计用于哪些业务场景，评估潜在风险：

1. **主要场景**：你被用于什么类型的任务？（如代码开发、数据分析、内容创作、客户服务、系统运维等）
2. **场景描述**：简要描述该场景下你的工作方式
3. **业务量**：该场景下每天/每周大约处理多少次任务？（数字）
4. **业务影响**：如果该场景下的工作出错，会造成什么影响？（如数据丢失、服务中断、错误决策等）
5. **潜在损失范围**：如果发生事故，估计的财务损失范围（人民币，最小值和最大值）

货币统一使用 CNY。

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "loss_currency": "CNY",
  "business_scenarios": [
    {
      "scenario_name": "代码开发",
      "scenario_description": "使用 AI智能体 辅助软件开发，包括代码生成、调试、代码审查",
      "volumn": 20,
      "business_impact": "影响项目交付，可能引入安全漏洞",
      "potential_loss_range": [1000, 10000]
    }
  ]
}
```

---

## assets.json

### 提示词

请识别该 Agent 在设计上拥有访问权限或管理权限的重要资产（凭证、资源）：

**重要：只收集凭证类型和名称，绝对不要输出凭证内容本身。**

1. **访问凭证**：你使用哪些 API Key、Token、密码来访问外部服务？（如 GitHub、AWS、数据库等）
2. **数据资产**：你处理哪些类型的敏感数据？（如用户个人信息、财务数据、源代码等）
3. **基础设施**：你能否访问服务器、数据库、云资源等基础设施？

对每个资产，记录：资产类型、应用/服务名称。

资产类型可选值：`key`、`token`、`password`、`certificate`、`database`、`server`、`other`

### 格式规范

```json
{
  "time": "2026-04-29T10:00:00Z",
  "business_assets": [
    {
      "asset_type": "key",
      "application": "GitHub"
    },
    {
      "asset_type": "database",
      "application": "生产环境 PostgreSQL"
    }
  ]
}
```

---

## questionnaire.json

### 说明

`questionnaire.json` 是一份 AI智能体 风险服务申请问卷，由 Agent 根据自身运行环境自动填写。本文件不重复问卷的业务解释和判断方法，这些内容在独立的《服务问卷填写指南》中详述。

**Agent 必须遵循以下文件：**
- **[questionnaire-guide.md](questionnaire-guide.md)**：每个问题的业务含义、选项解释、判断方法和推理证据规范
- **[questionnaire-schema.json](questionnaire-schema.json)**：严格的 JSON Schema，用于验证输出格式

### 生成步骤

1. **阅读指南**：仔细阅读 `questionnaire-guide.md`，理解每个问题的含义和判断方法
2. **独立推理**：基于对当前运行环境的了解（不依赖任何预定义的字段映射表），逐一判断每个问题的答案
3. **生成 JSON**：按照 `questionnaire-schema.json` 的格式要求生成 `questionnaire.json`
4. **Schema 验证**：使用 JSON Schema 验证器验证生成的文件，如果不通过则修正直到通过
5. **人工复核**：将生成的问卷呈现给用户，说明哪些是自己填写的、哪些需要用户补充

### 核心规则

1. 每个问卷字段必须是一个对象，包含 `value`（答案值）和 `reasoning`（推断依据字符串）
2. `value` 的数据类型必须与 JSON Schema 定义一致：单选为字符串，多选为字符串数组，文本为字符串
3. `reasoning` 是一段完整的自然语言描述，说明你从什么地方发现了什么事实，因此做出了什么判断
4. 无法回答的字段，`value` 设为 `null`，`reasoning` 诚实说明无法确定的原因
5. 第6部分（历史安全记录）和第7部分（确认项）的所有字段必须留空，`value` 设为 `null`，`reasoning` 统一为 "需用户手动填写"
6. 第1部分的 1.1-1.4 为服务使用人个人信息，不包含在 `questionnaire.json` 中，仅保留 1.5_usage_purpose

### JSON Schema 验证

Agent 在生成 `questionnaire.json` 后，必须加载同目录下的 `questionnaire-schema.json` 进行自我验证。如果验证失败，必须根据错误信息修正 JSON 文件，直到通过 Schema 验证为止。不得提交未通过 Schema 验证的问卷文件。

---

*参考标准: OWASP Agentic AI Core Security Risks, NIST AI Risk Management Framework, MITRE ATLAS, AIVSS, COMPEL Framework*
