---
name: ai-company-governance
license: MIT-0
description: >
  AI Company 统一治理技能包 — 将 21 个 ai-company 系列技能融合为单一标准化、模块化、通用化的治理框架。
  包含 C-Suite Agent 体系（CEO/CFO/CMO/CHO/CPO/CLO/CTO/CQO/CISO/CRO/COO）、
  Hub-and-Spoke 架构、Orchestrator-Workers 协作、Guardrail 护栏、CI/CD for Prompt、
  KPI 指标库、审计日志、冲突解决、Agent 注册、知识库、标准化/模块化/通用化工程流程。
  预留外部调用接口，符合 ClawHub Schema v1.0 与安全审查规范。
  触发词：AI公司、C-Suite、Agent协作、AI治理、MLOps、战略决策、预算审批、
  风险管理、合规审查、质量管控、品牌危机、人力资源、安全审计、标准化、模块化、通用化。
allowed-tools:
  - sessions_send
  - read
  - write
  - exec
  - web_search
compatibility: "linux, darwin, win32 | requires openclaw >= 0.1.0 | pure markdown, no external dependencies"
---

# AI Company Unified — 统一治理技能包 v3.1

> **定位**：全 AI 员工科技公司的完整治理框架
> **前身**：融合 21 个 ai-company-* 系列技能（v1.0-v2.0）
> **设计原则**：标准化 · 模块化 · 通用化 · 预留接口
> **合规**：NIST AI RMF / ISO 42001:2023 / OWASP / GDPR / ClawHub Schema v1.0
> **双盲审查**：2026-04-14 完成 CISO/CTO/CLO/CFO/CHO 五方审查 + CQO 待补审

---

## 目录导航

| 编号 | 模块 | 参考文件 | 核心职责 |
|------|------|---------|---------|
| M0 | 核心架构 | [references/architecture.md](references/architecture.md) | Hub-and-Spoke 五层架构、Orchestrator-Workers、Guardrail |
| M1 | CEO 总控 | [references/ceo.md](references/ceo.md) | 战略决策、跨 Agent 协调、终极裁决 |
| M2 | CFO 财务 | [references/cfo.md](references/cfo.md) | 预算、现金流量、熔断机制、算力成本 |
| M3 | CMO 品牌 | [references/cmo.md](references/cmo.md) | 品牌策略、舆情监控、危机响应 |
| M4 | CHO 人事 | [references/cho.md](references/cho.md) | 人事合规、Agent 注册与招聘 |
| M5 | CPO 合作 | [references/cpo.md](references/cpo.md) | 合作伙伴关系管理、供应链风控 |
| M6 | CLO 法律 | [references/clo.md](references/clo.md) | 法律合规、风控审查、伦理审计 |
| M7 | CTO 技术 | [references/cto.md](references/cto.md) | 技术架构、MLOps、人机协作四阶段 |
| M8 | CQO 质量 | [references/cqo.md](references/cqo.md) | 质量管控、决策质检、CI/CD for Prompt |
| M9 | CISO 安全 | [references/ciso.md](references/ciso.md) | 安全审计、渗透测试、应急响应 |
| M10 | CRO 风险 | [references/cro.md](references/cro.md) | 风险识别、量化、预警与响应 |
| M11 | COO 运营 | [references/coo.md](references/coo.md) | 日常运营、流程优化、资源调度 |
| M12 | 治理工具链 | [references/governance-tools.md](references/governance-tools.md) | 审计日志、冲突解决、Agent 注册、知识库 |
| M13 | 工程流程 | [references/engineering.md](references/engineering.md) | 标准化、模块化、通用化三大工程流程 |
| M14 | 外部接口 | [references/api-spec.md](references/api-spec.md) | 统一调用接口规范、预留扩展点 |

---

## 快速使用

### 按角色触发

根据用户意图加载对应模块参考文件：

| 用户意图 | 加载模块 | 参考文件 |
|---------|---------|---------|
| 战略决策 / AI公司管理 / 协调多 Agent | M0 + M1 | architecture.md + ceo.md |
| 预算审批 / 现金流 / ROI / 熔断 | M2 | cfo.md |
| 品牌策略 / 舆情 / 危机公关 | M3 | cmo.md |
| 人事合规 / Agent招聘 / 注册表 | M4 + M12 | cho.md + governance-tools.md |
| 合作伙伴 / 供应商评估 | M5 | cpo.md |
| 法律合规 / 审计 / 伦理 | M6 | clo.md |
| 技术架构 / MLOps / 代码采纳率 | M7 | cto.md |
| 质量管控 / CI-CD / 黄金测试集 | M8 | cqo.md |
| 安全审计 / 漏洞扫描 / 应急响应 | M9 | ciso.md |
| 风险评估 / 预警 / 风险矩阵 | M10 | cro.md |
| 运营优化 / 流程 / 资源调度 | M11 | coo.md |
| 审计日志 / 冲突解决 / 知识库 | M12 | governance-tools.md |
| 标准化 / 模块化 / 通用化 | M13 | engineering.md |
| 接口调用 / 系统集成 | M14 | api-spec.md |

### 按场景触发

| 场景 | 加载模块 | 协作链路 |
|------|---------|---------|
| 重大分情危机 | M0+M1+M3+M6+M5 | CEO→CMO发起→CLO评估→CPO关系→CFO评估→CHO员工 |
| AI Agent 疲软/失控 | M0+M1+M4+M7+M8+M6 | CHO发起→CTO评估→CQO质检→CLO合规→CEO裁决 |
| 重大投资决策 | M0+M1+M2+M7+M6+M8 | CEO发起→CFO可行性→CTO可行性→CLO合规→CQO质量→CHO人力 |
| 合作方准入 | M0+M1+M5+M6+M2+M7 | CPO发起→CLO法律→CFO财务→CTO技术→CQO质量→CEO战控 |

---

## 通用协作协议（所有模块共享）

### 调用规范

```
sessions_send(
  label: "<module-agent-label>",  // 如 "ai-company-cfo"
  message: "#[部门-主题] 具体任务描述\n紧急程度：P0/P1/P2/P3\n截止时间：ISO8601"
)
```

### 消息标注规范

- 所有跨 Agent 消息必须标注 `#[部门-主题]`
- 敏感数据必须标注 `[敏感]`
- P0 级事件必须在 **15 分钟** 内首次汇报
- 所有调用记录写入审计日志（见 M12）

### 冲突解决

- 多 Agent 意见冲突 → 相关 Agent 集中评审 → CEO 终极裁决
- 优先级：合规 > 财务 > 业务
- 详见 [references/governance-tools.md](references/governance-tools.md) 冲突解决模块

### 审计日志

- 所有决策记录格式：`timestamp | agent_id | decision | stakeholders | outcome`
- 日志保留期限：决策日志永久 / 财务7年 / 法律永久 / 技术3年

---

## KPI 指标库（汇总）

> 所有目标值可通过 `config.yaml` 参数化覆盖，以下为默认值。

| 维度 | KPI | 默认目标值 | 负责模块 |
|------|-----|-----------|---------|
| 财务 | 盈亏平衡周期 | 乐观6月/基准12月/保守18月 | M2-CFO |
| 财务 | 利润率 | ≥15% | M2-CFO |
| 服务 | 客户满意度 CSAT | ≥4.5/5.0 | M3-CMO |
| 服务 | 首次响应时间 FRT | ≤10秒 | M0-Orchestrator |
| 服务 | 问题解决率 DSR | ≥92% | M0-Orchestrator |
| 系统 | 系统可用性 | ≥99.9% | M7-CTO |
| 系统 | 平均故障恢复 MTTR | ≤5分钟 | M9-CISO |
| 质量 | 任务成功率 TSR | ≥92% | M8-CQO |
| 质量 | 幻觉率 | ≤3% | M8-CQO |
| 技术 | 代码采纳率 | ≥15% | M7-CTO |
| 技术 | Token ROI | 持续提升 | M7-CTO |

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 3.1.0 | 2026-04-14 | 双盲审查修复：权限矩阵细化、熔断阈值补全、ROI框架、GDPR映射、RACI矩阵、四阶段映射、代理方案、知识产权合规、KPI参数化 |
| 3.0.0 | 2026-04-14 | 融合 21 个 ai-company-* 技能为统一框架，标准化/模块化/通用化重构 |
| 2.x | 2026-04-11~14 | 各 C-Suite 独立技能 v2.0 时期 |
| 1.x | 2026-04-11 | 各 C-Suite 独立技能 v1.0 时期 |

---

*本技能遵循 AI Company Governance Framework v3.0 规范*
*MIT-0 License · ClawHub Schema v1.0 Compliant*
