# Decision Memory（决策记忆 · v2.6.0 P1 Institutional Learning）

## 定位
机构的决策资产。记住的不是"IC 说了什么"，而是"每一次决策为什么发生、后来结果如何、改变了什么认知"。属于整个 Agent，不属于某个 Mode。

## 核心原则：Capture / Recall 分离
- **Capture（捕获）**：从 Mode 1 就开始。每次决策（含 Screening 的 NO）都生成 Decision Object 并存储。被筛掉的项目是最值钱的学习数据。
- **Capture（v2.6.0 扩展）**：Portfolio Mode 追加捕获 **Monitoring / Outcome / Learning Object**（四件套），`outcome_id` / `learning_id` 挂回 `decision_id`。
- **Recall（激活）**：Evaluation / IC / Portfolio 阶段自动检索历史同类决策，融入输出。

## 存储方案
- 格式：**JSONL**（每行一个 Object：Decision / Monitoring / Outcome / Learning），可直接被代码查询，也可被 LLM 读取做 Recall
- 路径：`decision_memory.jsonl`（工作区根目录）+ `outcome_memory.jsonl`（Outcome/Learning，按 decision_id 关联）
- Phase 1：零外部依赖，线性扫描即可工作

## Memory Qualification（记忆质量分级，v2.6.2）

> "Capture 太容易 → 记忆垃圾"的反效果。原则：**全部 Capture，分级入 Recall**——不违背"从 Screening 起 Capture"铁律，但防止低质量负样本污染主要记忆。

每个 Decision Object 带 `memory_tier`：
- **Level A — Institutional Case**：完整 DD / IC / Outcome（进入主要 Recall + Calibration）
- **Level B — Decision Memory**：有明确 reason + 关键 evidence（进入主要 Recall）
- **Level C — Screening Signal**：仅结构化标签（**不进入主要 Recall 通道**，仅作去重 / 结构化信号统计）

写入与升级规则：
- 所有决策**仍全部 Capture**（含 Screening 的 NO，负样本有价值）
- 默认 Recall 只检索 **A + B**；C 仅在"去重 / 信号统计"时使用
- 升级路径：C →（完成 DD）→ B →（完成 IC + Outcome）→ A；**事实完整度只触发"升级建议"，Agent 不得自主升级为 A**——升级由专家治理确认（延续 Calibration 只报告不改规则的哲学）

## Capture 流程
```
每个 Mode 决策完成
  ↓
按 decision-object.md Schema 生成对应 Object（Decision / Monitoring / Outcome / Learning）
  ↓
追加写入 decision_memory.jsonl / outcome_memory.jsonl
  ↓
（IC 模式）决议回填 ic_resolution；（Portfolio）Outcome 回填后派生 Learning
```

## Recall 流程（v2.6.0 P1：Semantic + Structured + Outcome 三类召回）

> **Memory 复利 = 机构学习，不是 RAG。** 向量检索只解决"哪些案例语义相似"，CIO 真正需要的是"**历史上类似项目中，什么判断最终被事实证明是错的**"。

```
接收项目（sector / stage / 商业模式 / 估值区间 / 当前 Thesis 要点）
  ↓
① Semantic Recall（语义相似）：与当前项目表述相近的历史案例
② Structured Recall（结构化同类）：同行业 / 同商业模式 / 同估值区间 / 同 stage
③ Outcome Recall（结果反例）——v2.6.0 新增，最有价值：
   - 历史 Outcome 与当前 Thesis 相反的案例（当初看好后来低于预期 / 当初 Pass 后来爆发）
   - 历史 Kill Factor 命中案例（哪些 Trigger 真的应验了）
   - 历史 Forecast Error 最大案例（哪些维度长期高估/低估）
  ↓
融入当前输出（统计口径，不是文档堆）：
  "过去 12 个相似项目：7 个进入 IC，4 个投资，3 个最终低于预期。
   最常见失败原因不是客户获取，而是回款周期与估值压缩。
   当前项目存在同类信号：XX。"
  ↓
在当前 Decision Object 写入 linked_decisions（含 outcome_id / learning_id）
```

## 典型 Recall 场景（v2.6.0）
| 问题 | Recall 逻辑 |
|------|-----------|
| 为什么去年 Pass 这个项目？ | Structured：按 project_id / sector 检索历史 NO 决策 + reason |
| 这个赛道我们投过吗？结果如何？ | Outcome：按 sector 检索所有决策 + 关联 Outcome（IRR/营收/退出 vs 预期） |
| 历史上类似项目什么判断被证明是错的？ | Outcome Recall：Thesis 相反案例 + Kill Factor 命中 + Forecast Error |
| 现在还能投吗？ | 对比历史 reason + Outcome 与当前变化，给重评建议 |
| 这个判断我们曾经错在哪？ | Learning Recall：failed_assumptions / misleading_evidence |
| Agent 与 IC 在什么类型问题上更准？（v2.6.2） | 按 `decision_attribution` 聚合，输出"历史上 Agent 在估值类判断偏乐观、IC 在退出时点判断更准"这类**人机分工洞察** |

## Why-Not Memory（Why Not ≠ Pass，v2.6.0）

> 保存 **Decision + Why + Why Not + Outcome** 四条信息，其中投资决策与产业合作是**两条独立轨道**——投资未通过 ≠ 产业无价值。

三角色各取所需：
- **投资经理**："这个项目我们以前为什么没投？"（Why Not + reason）
- **IC**："我们过去是不是已经看过类似项目？"（Structured 去重）
- **招商领导**："投资没过，但产业上有没有合作价值？"（产业合作建议轨道）

示意（⚠️ 占位）：
```
投资未通过：估值过高（Why Not）
产业合作建议：继续推进（独立轨道）
后续 Outcome：企业估值下降 30% → 重新进入投资池（Outcome 回填，反哺下次 Recall）
```

### Missed Opportunity（漏投复盘，v2.6.2）
- Pass 项目后续 Outcome 显著上行（估值 / 收入 / 退出超预期）→ 标记 `missed_opportunity = true`，回写 Learning Object 的 `what_was_wrong`
- 纳入 Calibration 的 **False Negative 倾向统计**（我们是否系统性漏投某类项目）
- 标记必须基于**预定义 Outcome Criterion**，不得事后倒推归因（与 decision_attribution 同规则，防 hindsight bias）

## Decision Memory ≠ Market Intelligence Memory（v2.6.2）

| 存储 | 内容 | Recall 用途 |
|---|---|---|
| **Decision Memory**（`decision_memory.jsonl` + `outcome_memory.jsonl`）| 项目级决策 + 结果（Screening/Evaluation/IC/Portfolio 漏斗内）| 只服务"我们自己的决策校准" |
| **Market Intelligence Memory**（`benchmark_cases.jsonl` + `标杆案例库.md`）| 市场 / 标杆范式情报（Radar 维护）| 只服务"横向借鉴 / 赛道锚点"，**不作 Decision 证据** |

硬规则：**Recall 不跨类**——"别人投了机器人"不得作为"我们过去判断过类似项目"的依据写入决策逻辑；Market 情报只作 context 输入，不进入 Decision 的证据链。

## Calibration Ledger（校准账本，v2.6.0 P1）

> 原则：**没有 Outcome 就没有 Calibration；没有 Calibration，Score 永远只是主观意见。** Soft Score 要从"规则分数"变成"经过历史校准的预测工具"。

由 Outcome / Learning Object 累计统计，周期输出校准报告，回答五个问题：
1. **哪个维度长期高估？**（Forecast vs Actual 分维度偏差：营收 / ARPU / 毛利 / 估值）
2. **哪类项目最易误判？**（按行业 / 商业模式 / 估值区间分组）
3. **哪个评分偏乐观？**（Decision Outcome = wrong 的项目，当初 Soft Score 分布）
4. **哪个 Evidence 产生虚假信号？**（misleading_evidence 累计）
5. **哪个 Kill Factor 真有预测力？**（kill_factor_outcome 命中率统计）

校准报告（**Agent 只报告，不自动改规则——规则与方法论由专家治理**）：
- 输出"历史上该类项目 Revenue Forecast 平均高估 17%"这类**报告**
- 建议项（供专家决策，不自动执行）：`calibrate_soft_score`（建议下调某维度）/ `adjust_comparable_weight`（建议修正可比权重）/ `update_assumption_prior`（建议更新假设先验）
- **Agent 不自动修改评分权重、不自主改写规则**——专家确认后才由人调整

## Phase 2（存储升级，数据量大时）
- 向量 + 结构化混合存储（Semantic Recall 生效前提）
- 统计报表（月度决策分布、Pass 重评提醒、Calibration 季报）
- 自然语言问答（"去年我们为什么没看人形机器人"、"我们的 Base Case 平均高估多少"）

## 隐私边界
- Decision / Outcome / Learning Memory 含基金保密数据，本地存储，不外发、不上第三方训练
- 导出 / 共享需 IC 秘书人工审批
