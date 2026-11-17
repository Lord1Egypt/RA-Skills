# Convbox-DiagClaw

**Your Marketing Doctor**

由 [RTOAI](https://www.rto.ai/) 维护。

[English](README.md)

Convbox-DiagClaw 是一套轻量、开放的 DTC 电商营销诊断 Agent Skill。它把自然语言
业务问题路由到对应分析方案，基于 Convbox 第一方归因数据输出量化诊断、优先处理
建议，以及日报、周报或自定义周期报告。

> **当前状态：Preview。** Convbox-DiagClaw 是迈向“诊断即服务”的起点，适合能力
> 验证和分析师辅助流程。所有涉及预算、出价、广告和店铺调整的建议仍需人工审核。

## 先诊断，再优化

仪表盘告诉你“发生了什么”，Convbox-DiagClaw 更关注“为什么发生”和“下一步应该
先查什么”。

```text
自然语言问题
    -> 自动场景路由
    -> 第一方数据取数
    -> 诊断与对比
    -> 按优先级给出建议
    -> 日报 / 周报 / 自定义报告
```

使用者无需记忆分析方案名称。Skill 会识别意图、选择对应诊断流程、保持指标口径
一致，并在数据不足时明确说明不能可靠判断的原因。

## 三层能力

| 层级 | 覆盖内容 | 代表性输出 |
|---|---|---|
| 盯盘与诊断 | 增长异常、ROAS/CPA 变化、归因差异、追踪健康、素材与 Campaign、漏斗、利润质量 | 根因判断、量化差异、问题排序 |
| 优化 | 预算分配、扩量决策、出价策略、受众效率、再营销增量 | 有证据支撑的优先行动建议 |
| 报告 | 每日脉冲、周度复盘、月报、自定义周期与角色报告 | 营销团队可直接用于决策的摘要 |

“盯盘”需要由宿主 Agent 调用或定时触发，当前不是实时流式告警服务。

## 为什么选择 Convbox-DiagClaw

- **以第一方数据为决策基础：** 诊断优先使用 Convbox 归因指标；Meta、Google 等
  平台自报数据用于比较，而不是直接替代第一方口径。
- **自然语言自动路由：** 用户只需提出业务问题，Skill 会选择相关分析方案或方案链。
- **量化归因偏差：** 不只判断“平台数据对不上”，还可计算并排序平台高报比例和
  转化价值差额。
- **多 Agent 生态兼容：** 同一套开放 Skill 面向 Claude Code、Codex、OpenClaw、
  Hermes、WorkBuddy、GitHub Copilot，以及其他支持 `SKILL.md` 和 HTTPS 的宿主。
- **开放且可调整：** 客户和贡献者可以审查规则、修改分析方案或补充诊断场景。
- **人工掌控执行：** Skill 负责诊断、解释和建议，不会静默修改 Campaign、预算、
  出价或店铺页面。

## 可以这样提问

```text
上周 Meta ROAS 降低了，能帮我分析原因吗？
为什么 Meta 和 Google 报告的转化高于第一方数据？
哪些渠道可以安全增加预算？
用户主要流失在站内漏斗的哪一步？
生成本周付费媒体复盘，并告诉我应该先处理什么。
```

代表性场景包括：

- 增长健康、Campaign 异常、ROAS 下降和 CPA 上升诊断
- 广告平台自报数据与第一方归因差异分析
- 追踪健康和匹配率检查
- 渠道、Campaign、受众和素材表现分析
- 站内漏斗、落地页承接和加购异常诊断
- 预算分配、扩量和出价策略建议
- 利润质量和再营销增量分析

## 安装

### 直接告诉你的 Agent

```text
先检查 https://github.com/RTOAI/Convbox-DiagClaw 及其 SKILL.md，确认来源和
运行要求，然后为我安装 convbox-diagclaw。安装后，帮助我通过安全的环境变量方式
配置 CONVBOX_API_KEY；不要打印 Key，也不要把它写入仓库、Prompt 或日志。
```

### 一条命令安装

使用开放的 Agent Skills CLI 全局安装（需要 Node.js 18+）：

```bash
npx skills add RTOAI/Convbox-DiagClaw --skill convbox-diagclaw -g
```

安装程序会检测支持的 Agent，并提示选择安装目标。如需为 Codex 手动安装：

```bash
git clone https://github.com/RTOAI/Convbox-DiagClaw.git \
  ~/.codex/skills/convbox-diagclaw
```

其他 Agent 可按其文档把仓库克隆到技能目录，或将技能根目录指向本仓库。

## 使用条件

- 支持读取 `SKILL.md` 并发起 HTTPS 请求的 AI Agent
- 已开通 Convbox 并获得有效 API Key
- 仅运行健康检查工具时需要 Python 3.10+ 和 PyYAML 6.x

本仓库许可证只覆盖 Skill 文件和工具代码。托管的 Convbox API 是独立服务，仍需
有效账户和 API Key，并受相应服务条款约束。

请通过进程环境配置 API Key，不要把真实 Key 写入可能提交的 `.env` 文件。

macOS 或 Linux：

```bash
export CONVBOX_API_KEY="your-key"
```

Windows PowerShell：

```powershell
$env:CONVBOX_API_KEY = "your-key"
```

## 验证安装

```bash
python -m pip install -r requirements.txt
python utilities/config-health-check/config_health_check.py --config-only
python utilities/config-health-check/config_health_check.py \
  --recent-window 7 --strict
```

健康检查不会打印 API Key，只报告 `OK`、`WARN`、`FAIL` 或 `SKIP`。

## 分析如何路由

1. `SKILL.md` 识别用户意图和业务前置条件。
2. `functions.md` 确定场景、接口、权限和开发状态。
3. `access.yaml` 定义精确的接口请求、响应字段和指标口径。
4. `plans/` 中对应方案完成数据准备、比较、诊断和行动建议。
5. 输出列出实际调用的 Plans，并明确数据或业务输入限制。

## 目录结构

```text
.
|-- SKILL.md                 # Agent 入口、路由和安全边界
|-- functions.md             # 数据契约和场景目录
|-- access.yaml              # Convbox API 请求与响应字典
|-- plans/                   # 原子分析方案
|-- utilities/
|   `-- config-health-check/ # 配置、连通性和 Schema 自检
|-- CONTRIBUTING.md
|-- SECURITY.md
`-- LICENSE
```

## 数据与安全边界

- 只消费 Convbox API 返回的聚合数据，不执行用户级 ETL。
- 平台透传数据只用于差异比较，不能直接与第一方归因指标相加。
- 利润分析需要成本配置；精确出价建议需要确认毛利率或用户明确授权的假设。
- 空数据或不可用数据必须报告为限制，不能据此编造结论。
- 模型输出可能存在差异，高影响建议必须由人工和相关广告平台共同复核。
- Issue 和 Pull Request 中禁止提交客户数据、API 响应、账户 ID 或验证证据。

## 演进方向

当前版本聚焦诊断、行动建议和报告。后续可能演进统一严重度分级、人工审批后执行、
客户上下文持久记忆、建议反馈学习和可分享报告产物。这些是方向，不是当前版本承诺。

场景是否可用以 [`functions.md`](functions.md) 的 **Development status** 为准；存在
Plan 文件不代表该场景已经达到生产稳定状态。

## 参与贡献与安全

修改指标口径、接口字段或判断阈值前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
凭证泄露、未授权数据访问和鉴权问题请按照 [SECURITY.md](SECURITY.md) 私下报告，
不要创建公开 Issue。

## 许可证

技能文件和工具代码采用 [MIT-0](LICENSE) 许可证。托管的 Convbox API 需单独授权。
该许可证不授予 Convbox 名称或 Logo 的商标使用权。
