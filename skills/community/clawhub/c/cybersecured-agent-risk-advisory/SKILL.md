---
name: cybersecured-agent-risk-advisory
description: 为 AI智能体配置龙行无忧风险管家服务。协助用户完成认证、智能体绑定、安全扫描、风险评估、服务申请和事故信息提交；生效后继续围绕保障与事故协助处理。当用户提及"配置龙行无忧"、"给我的 AI智能体 买保险/申请服务"、"查看申请/服务状态"、"我要报案/提交事故信息"、"查看保障"时调用。
---

# 龙行无忧 - AI智能体风险管家服务

## 概述

龙行无忧是厚锋科技面向AI智能体推出的风险管家服务，具体内涵包括对AI智能体的持续风险监测、定期风险分析、风险处置建议和损失事件响应。用户通过云端管理平台完成服务申请、信息核实与服务方案选择，随后进入服务开通流程。生效后的对象继续以保障视图展示，事故处理则保留事故语义，并通过协助处理机制支持用户提交信息、补充材料和联系服务人员。服务覆盖AI智能体使用过程中的核心风险：通用网络安全事故、敏感信息泄漏和恶意教唆行为责任。

厚锋科技通过与合作方协同，为用户提供风险保障服务。当风险事件发生时，协调相关流程按照保障条款进行处理。

## 触发条件

- 用户提及"配置龙行无忧"、"开启服务"、"买保险"、"申请服务"
- 用户提及"给我的 AI智能体 申请服务"、"给我的 AI智能体 买保险"
- 用户提及"查看申请状态"、"我的申请进度"、"服务状态"
- 用户提及"我要报案"、"报告事故"、"提交事故信息"、"Token被盗"、"密钥泄露"
- 用户提及"查看保障"、"查看保单"、"下载电子凭证"、"我的保障"
- 用户提及"放弃报案"
- 用户提及"检查更新"、"刷新状态"

## 工具依赖

| 工具 | 用途 | 说明 |
|-----|------|------|
| `cybersecured-agent` | CLI 工具 | `uv tool install cybersecured-agent-cli`，Codex/Claude Code 需 `>= 2.1.0` |
| `uv` | Python 包管理器 | 安装 CLI 及依赖（https://docs.astral.sh/uv） |
| `python` | 执行环境 | Python 3.8+ |

## 兼容智能体框架

CLI `2.1.0` 起支持以下框架的自动识别、指纹生成与本地环境采集：

| 框架 | 典型识别信号 |
|------|--------------|
| OpenClaw | `OPENCLAW_WORKSPACE`、`~/.openclaw` |
| Hermes | `HERMES_HOME`、`~/.hermes` |
| Kimi CLI | `KIMI_WORK_DIR`、`~/.kimi` |
| OpenCode | `OPENCODE*` 环境变量、`~/.config/opencode` |
| Codex / Codex Desktop | `CODEX_THREAD_ID`、`CODEX_SHELL`、`~/.codex`、Codex 进程链 |
| Claude Code | `CLAUDE_CONFIG_DIR`、`CLAUDE_CODE_*`、`~/.claude`、Claude Code 进程链 |

## CLI 命令速查

```bash
# 认证（生产环境）
cybersecured-agent auth login --api-key cds-aiai-xxxxxx

# 认证（指定后端地址，开发/测试环境使用）
cybersecured-agent --api-base-url http://<API_BASE_URL>/trope auth login --api-key cds-aiai-xxxxxx

# 认证（测试环境，自签名证书）
cybersecured-agent --api-base-url https://<API_BASE_URL>/trope --no-verify-ssl auth login --api-key cds-aiai-xxxxxx

# 认证（测试环境）
cybersecured-agent --api-base-url https://<API_BASE_URL>/trope auth login --api-key cds-aiai-xxxxxx

cybersecured-agent auth logout
cybersecured-agent auth whoami

# 智能体绑定
cybersecured-agent agent bind --nickname "My Agent"
# 了解本agent的信息
cybersecured-agent agent info

# 安全扫描
cybersecured-agent scan run --output-dir ./assessments/$(date +%Y%m%d-%H%M%S)

# 风险评估提交
cybersecured-agent assessment submit --assessment-dir ./assessments/20260322-120000

# 服务申请
cybersecured-agent application create --assessment-id xxx
cybersecured-agent application status <application_id>

# 保障查询
cybersecured-agent coverage list

# 事故信息提交
cybersecured-agent incident create \
  --policy-id <policy_id> \
  --type <general_security|data_leakage|other> \
  --time "2026-04-30T14:30:00+08:00" \
  --description "事故描述..." \
  --amount 5000 \
  [--details '{"discovery_method":"...","impact_scope":"..."}']
cybersecured-agent incident confirm --claim-id <claim_id>
cybersecured-agent incident abandon --claim-id <claim_id>
cybersecured-agent incident list
cybersecured-agent incident status <claim_id>

# 状态查询
cybersecured-agent status
```

## 运行前检查

每次启动服务前，先检查 CLI 是否有更新：

```bash
uv tool upgrade cybersecured-agent-cli
```

检查 CLI 版本，确认输出不低于 `2.1.0`：

```bash
cybersecured-agent --version
```

如果尚未安装 CLI：

```bash
uv tool install cybersecured-agent-cli
```

> **说明**：`uv tool install` 会为 CLI 创建独立的虚拟环境并自动暴露命令到 PATH，无需手动激活虚拟环境，也不会污染系统 Python。

---

## 核心工作流程

### 阶段零：认证

首次使用前，需要用户提供 API Key 并完成认证：

1. 引导用户访问 https://ai.cybersecured.cn 登录并获取 API Key
2. 执行认证命令：

```bash
cybersecured-agent auth login --api-key cds-aiai-xxxxxx
```

**测试环境**：如果连接测试后端，需在命令前添加 `--api-base-url` 参数（注意必须包含 `/trope` 路径后缀）：

```bash
cybersecured-agent --api-base-url https://<API_BASE_URL>/trope auth login --api-key cds-aiai-xxxxxx
```

**测试环境（自签名证书）**：如果测试环境使用自签名 HTTPS 证书，添加 `--no-verify-ssl` 参数跳过证书验证：

```bash
cybersecured-agent --api-base-url https://<API_BASE_URL>/trope --no-verify-ssl auth login --api-key cds-aiai-xxxxxx
```

`--api-base-url` 是全局选项，需放在子命令之前。设置一次后，所有后续命令（agent bind、assessment submit、application create 等）都会使用同一地址。

认证成功后，CLI 保存配置到本地，后续命令无需重复输入 API Key。

### 阶段一：智能体绑定

1. Agent 根据用户喜好、自身的功能特点、运行环境，生成一个容易被客户识别且有辨识度的昵称（如"Python开发助手"、"数据分析Agent"）
2. **必须向用户展示生成的昵称并询问用户是否确认或需要修改**
3. 用户确认后，执行绑定命令：

```bash
cybersecured-agent agent bind --nickname "用户确认的昵称"
```

CLI 自动处理：配置检查 → 验证 → 智能体绑定 → 本地保存。

如果绑定、扫描或状态查询提示“framework is not yet supported”，先执行：

```bash
cybersecured-agent diagnose --output diagnose.json
```

确认 `framework_detection.matched` 是否为 `codex`、`claude-code` 或其他支持框架；若仍为 `unsupported`，提示用户升级 CLI 到 `2.1.0+` 后重试。

绑定完成后，继续执行后续阶段。

### 阶段二：安全扫描

在 `./assessments/` 目录下，创建以当前时间命名的子目录，格式为 `YYYYMMDD-HHMMSS`（例如 `20260322-143052`）。


1. 运行系统扫描 → `cybersecured-agent scan run`
2. 在该目录中根据要求收集风险因子信息，生成不同的 json 文件。具体要求参见 references/risk-factors-format.md。
3. 填写服务问卷：生成 `questionnaire.json` 文件。

   步骤：
   - 阅读 references/questionnaire-guide.md，理解每个问题的业务含义、选项解释和判断方法
   - 根据自身运行环境逐一推理判断每个答案，为每个答案提供完整的推理证据
   - 按照 references/questionnaire-schema.json 的格式要求生成 JSON 文件
   - 使用 JSON Schema 验证输出。验证命令示例：

     ```python
     import json
     import jsonschema

     with open('questionnaire.json') as f:
         data = json.load(f)
     with open('references/questionnaire-schema.json') as f:
         schema = json.load(f)

     jsonschema.validate(data, schema)
     ```

     如果验证失败，根据错误信息修正 questionnaire.json，直到通过验证。不得提交未通过验证的问卷。
   - 将问卷呈现给用户，告知用户可以在移动端进行后续的确认和修改。


### 阶段三：风险评估

提交本地收集的安全信息到后端：

```bash
cybersecured-agent assessment submit --assessment-dir ./assessments/YYYYMMDD-HHMMSS
```

提交成功后，CLI 返回 `assessment_id`。评估完成后自动进入阶段四，无需提示用户中断。

### 阶段四：创建服务申请

```bash
cybersecured-agent application create --assessment-id <assessment_id>
```

创建成功后，提示用户到厚锋科技的网页端（https://ai.cybersecured.cn）完成信息核实和服务方案选择。

### 阶段五：状态查询

查询申请状态：

```bash
cybersecured-agent application status <application_id>
```

**重要：服务方案状态展示规则**

当状态查询返回 `plan_code` 时，必须将其转换为中文名称展示给用户，**绝不允许直接显示代码**。

| 方案代码 | 中文名称 | 适用场景 |
|---------|---------|---------|
| `basic` | 基础计划 | 日常办公提效、个人学习 |
| `standard` | 专业计划 | 辅助客户服务、商业运营、企业内部管理 |
| `premium` | 高端计划 | 直接对客户提供服务、深度参与商业运营 |
| `enterprise` | 企业定制计划 | 高度定制业务流程、深度使用AI智能体 |

展示示例：
- 正确："您当前选择的服务方案是：**基础计划**"
- 错误："您当前选择的服务方案是：basic"

根据返回的状态给出对应指引。完整状态说明参见 references/status-guide.md。

### 阶段六：事故信息提交

当用户说"我要报案"、"报告事故"、"提交事故信息"、"Token被盗"等时，进入引导式事故信息提交流程。

**重要原则**：
- Skill 与 CLI 是同一渠道（Skill → CLI → Backend）
- Token 盗刷/密钥泄露属于保障范围，应主动引导
- 服务中断**不在**保障范围内，不要引导询问

#### 步骤 1：确认生效保障

```bash
cybersecured-agent coverage list
```

- **无生效保障** → 告知"提交事故信息需要一份生效中的保障，请先完成服务申请"，结束
- **有生效保障** → 展示保障信息（保单号、保障类型、生效/到期时间），继续
- **多份生效保障** → 引导选择具体保障 → 确定 `policy_id`

#### 步骤 2：事故类型识别

**引导话术**："请告诉我这次事故大致属于哪种情况？"

| 选项 | 代码 | 引导说明 |
|------|------|---------|
| 通用网络安全事故 | `general_security` | 系统被入侵、恶意软件感染、DDoS攻击、服务被破坏等 |
| 敏感信息泄露 | `data_leakage` | API Key被盗用、Token被盗刷、数据外泄、隐私数据暴露、凭证泄露等 |
| 其他安全事件 | `other` | 不属于以上类型的安全事件 |

**特色引导**：当用户描述涉及"Token被盗刷"、"API Key泄露"等场景时，应主动说明这些属于保障范围。

#### 步骤 3：事故时间线

**引导话术**："请回忆一下："

1. **事故发生时间**（必填）："这个安全事件是什么时候发生的？（大致时间即可）"
   - 约束：必须在保障生效期内，不能晚于当前时间
2. **事故发现时间**（选填）："您是什么时候发现这个事件的？（如果与发生时间不同）"
3. **发现方式**（选填）："您是如何发现的？"
   - 选项：自行发现 / 安全工具告警 / 第三方通知 / 审计检查 / 其他

#### 步骤 4：事故经过描述（结构化引导）

**引导话术**："请详细描述事故的经过。以下问题可能帮助您组织描述："

| 维度 | 引导问题 | 存储位置 |
|------|---------|---------|
| 事件经过 | "发生了什么？系统被入侵？数据被泄露？Token被盗用？" | incident_description |
| 影响范围 | "影响到了哪些系统、数据或服务？" | incident_details.impact_scope |
| 受影响资源 | "具体哪些资源受影响？（如代码仓库、数据库、API服务等）" | incident_details.affected_resources |
| 原因假设 | "您怀疑的根本原因是什么？" | incident_details.root_cause_hypothesis |

通过对话方式引导用户完整描述，然后整理为 20-500 字的 `incident_description`，同时将结构化信息存入 `incident_details`。

#### 步骤 5：影响与损失评估

**引导话术**："让我们评估一下事故的影响和损失："

1. **影响程度**：
   - "是否有数据丢失或损坏？" → incident_details.data_loss
   - "是否有第三方受到损害？" → incident_details.third_party_affected
   - "影响范围是什么？（仅本机 / 局部网络 / 云服务 / 第三方系统）" → incident_details.impact_level
- "是否有 Token/密钥被盗用？" → incident_details.token_compromised（特色引导，此为可支持项）

2. **经济损失估算**（必填）：
   - "您估计的经济损失大约是多少？"
   - 引导考虑：系统恢复费用、数据恢复费用、应急响应费用、Token盗刷损失、第三方赔偿
   - 约束：不能超过保障剩余限额

#### 步骤 6：已采取的措施

**引导话术**："事故发生后，您已经采取了哪些应对措施？如果需要，也可以联系服务人员协助处理。"

| 措施 | 引导 |
|------|------|
| 隔离 | "是否已隔离受影响的系统或网络？" |
| 凭证更换 | "是否已更换泄露的密钥、Token 或凭证？" |
| 通知 | "是否已通知可能受影响的第三方？" |
| 修复 | "是否已进行修复或打补丁？" |
| 专家协助 | "是否已联系安全专家或应急响应团队？" |

存储到 `incident_details.mitigation_actions`（数组）

#### 步骤 7：确认信息摘要

汇总所有收集到的信息，向用户展示完整摘要，询问是否需要修改或确认提交。

#### 步骤 8：创建草稿事故信息

用户确认信息无误后，执行：

```bash
cybersecured-agent incident create \
  --policy-id <policy_id> \
  --type data_leakage \
  --time "2026-04-30T14:30:00+08:00" \
  --description "事故描述..." \
  --amount 5000 \
  --details '{"discovered_at":"...","discovery_method":"...","impact_scope":"...","mitigation_actions":[...]}'
```

→ 返回 `claim_id`，状态为 `draft`

#### 步骤 9：用户确认提交

向用户展示事故信息摘要，询问：
"请确认以上事故信息是否准确。确认正式提交事故信息？（提交后后台审核人员将开始处理）"

用户确认后：

```bash
cybersecured-agent incident confirm --claim-id <claim_id>
```

→ 状态变为 `reported`，事故信息提交完成。告知用户案件号。

#### 放弃提交

用户可在 `draft`/`reported`/`pending_info` 状态下放弃提交（`approved`/`paid` 状态不支持）：

```bash
cybersecured-agent incident abandon --claim-id <claim_id>
```

## 状态速查

| 状态 | 用户端显示 | Skill 响应 |
|------|-----------|-----------|
| `risk_assessed` | 风险评估完成 | 提示到网页端完成信息核实 |
| `questionnaire_filled` | 信息已预填 | 提示到网页端确认信息 |
| `plan_selected` | 服务方案已选择 | 展示服务方案中文名称，提示确认并支付技术服务费 |
| `awaiting_payment` | 待支付 | 提示尽快完成技术服务费支付 |
| `paid` | 已支付 | 提示等待后台处理 |
| `underwriting` | 处理中 | 告知后台正在协同处理 |
| `policy_uploaded` | 处理中 | 提示等待保障生效 |
| `activated` | 保障已生效 | 显示保障信息（含服务方案中文名称）与后续事故协助入口 |
| `refunding` | 退款中 | 提示后台正在处理退款 |
| `refunded` | 已退款 | 说明退款已完成，可重新发起服务申请 |
| `expired` | 已过期 | 提示重新申请 |
| `abandoned` | 已放弃 | 提示重新申请 |

## 参考文档

- 状态处理指南：references/status-guide.md
- 风险因子收集：references/risk-factors-format.md
- 服务问卷填写指南：references/questionnaire-guide.md
- 服务问卷 JSON Schema：references/questionnaire-schema.json
- 数据存储规范：references/data-storage.md

---

*厚锋科技 - 让每个 AI智能体 都有服务保障*
