# 人读报告排版规范（Output / Presentation 层 · v2.6.1）

> 定位：所有 Mode（Evaluation / IC / Portfolio 等）产出**人读 Artifact** 时的统一排版纪律。
> 原则一句话：**先给人结论，再给人证据；schema 名词留给机器，自然语言 + 表格留给 IC。**
> 与 Decision Object 的关系：机读 JSON 是 single source of truth，本规范管"同一份结论怎么呈现给人看"——两者分离，互不替代。

---

## 一、人读 vs 机读 分离（第一原则）

机读 schema 名词**只出现在**：
1. 独立机读 JSON（Decision Object，见 `decision-object.md` schema）
2. 报告「附录索引」的一句话指向（说明数据在哪个 JSON / 哪个独立文件）

人读正文**不得**用 schema 名词当标题或正文术语，一律用自然语言等价表述：

| schema 名词 | 人读写法 |
|---|---|
| gate_status | 决策闸状态 |
| 3A Valuation / 3B Return / 3C Exitability | 估值合理性 / 风险调整后回报 / 退出路径 |
| E1–E5 + Verification Status | 证据等级（已验证 / 部分验证 / 企业披露待验证）|
| Kill Factors | 关键风险与证伪 |
| Thesis Ledger | 投资命题账本（支持 vs 反证）|
| Assumption Register | 关键假设登记 |
| Evidence Objects | 证据清单 |
| Monitoring / Outcome / Learning Object | 投后跟踪 / 结果复盘 / 经验学习（一句话带过）|
| confidence_block / decision_confidence | 决策置信度（四层）与主要不确定性 |
| decision_critical_assumptions | 关键假设敏感性（Top3，敏感性 ≠ 风险）|
| evidence_conflicts | 证据冲突与调和 |
| dd_priority | 下一轮尽调优先级（P0/P1/P2）|
| memory_tier | 记忆分级（机构案例 / 决策记忆 / 初筛信号）|
| ic_resolution / decision_attribution | IC 决议与分歧记录 / 人机判定归因 |

## 二、排版八律（每次产出自检）

1. **结论前置** — 第一屏 = 一句话投资建议 + 建议参数（Recommendation over Report）
2. **一屏快照** — 紧跟「决策闸状态表」，PASS / WATCH / CONDITIONAL 一屏看清
3. **表格优先** — 状态 / 对比 / 参数用表格，不用长列表；每格一句话
4. **IC Package 不用代码块** — IC 决议页用表格 + 清单（Checkbox / 行动项），严禁用 ``` 包裹正文
5. **开发元信息不进正文** — REG-001 回归、版本对比、自检记录等 → 附录索引或独立文件
6. **层级 ≤3 级** — 标题不超过 ###；每节第一句给出该节结论
7. **短句 + 数字前置** — 每段 ≤3 行；金额 / 比例 / 日期直接给数字
8. **脱敏闸门** — 对外分享 / 演示 / 培训版本全泛化（XX公司 / ¥XX / X轮）；内部审议稿按授权

## 三、标准结构模板（IC 报告）

```
0. 执行摘要（一句话建议 + 建议参数）
1. 决策闸快照（一屏表）
2. 为什么是这个结论（3 Why）
3. 未解除的硬条件（每条：现在缺什么 / 解除条件）
4. 估值与回报（表格 + 标注"估算"）
5. 关键风险与证伪（Kill Factors + 反事实关键问）
6. 投后跟踪（简述，指向机读 JSON）
7. IC 决议页（建议参数 / 交易合规 Checkbox / 预判问答 / 行动项 / Vote·纪要）
8. 附录索引（证据清单 / 假设登记 / 机读 JSON / 开发交付物）
```

## 四、反模式（不得出现）

- ❌ schema 名词当标题（如"## Hard Gates 逐道（Gate-specific state）"）
- ❌ IC Package 塞进 ``` 代码块（黑底等宽，IC 委员难读）
- ❌ REG-001 回归表 / 版本对比表进 IC 正文
- ❌ 概率 / 权重不加"估算 / 假设"标注
- ❌ 机读字段直接平铺（evidence_objects 长 JSON 贴进正文）

---

## 五、Role Views 三视图（v2.6.2，同一 Decision Object，不加 Mode）

> 硬规则：**同源、只筛选、不产生第二份结论**。三个视图都由同一 Decision Object 推导，仅字段筛选与措辞不同；任何视图不得改写 Gate 结论。

| 视图 | 服务对象 | 关注点 | 内容块 |
|---|---|---|---|
| **Investment View** | 投资经理 | 下一步查什么 | 决策闸 / 估值与回报 / 关键风险与证伪 / DD 优先级 |
| **IC View** | 投委会成员 | 哪些事实足以投/不投 | 决策 / 为什么 / 为什么不投 / 硬闸 / 估值区间 / 关键风险 / 提问 |
| **Industrial View** | 地方招商领导 | 产业价值 & 招商机会 | 产业价值 / 地方契合 / 落地贡献 / 招商机会 / 投资结论 |

- 三视图同源即一致性验收项：不得出现"结论漂移"（同一次分析，三个视图说法打架）
- 措辞仍守人读机读分离：视图内不用 schema 名词，用自然语言

---

*本规范为呈现层增强，不改判定逻辑、不改 Decision Object schema、不改变任何 Gate 结论。*
