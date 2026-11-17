# CDISC 2026 AI 创新挑战：AI 自动生成临床试验数据/文档 情报参考

> 类型：外部竞赛结果 + 开源实现源码级分析（参考文献 / intelligence reference）
> 入库日期：2026-10-18 ｜ 关联规范：ct-base §22（AI 生成资产治理）· §21（论文评估与改进纳入）
> 置信度：高（6 个获奖方案新闻稿 + 唯一开源投稿 Appsilon 的仓库已 `git clone` 逐文件读源码）

---

## 1. 来源清单（可溯源）

| 类型 | 出处 | 链接 |
|---|---|---|
| 官方结果 | CDISC 2026 AI Innovation Challenge | https://www.cdisc.org/events/ai-innovation-challenge |
| 赛果详述 | LinkedIn 长文（含 6 方案描述） | https://www.linkedin.com/pulse/cdisc-ai-innovation-challenge-2026-cdisc-71lse |
| 公众号二次解读 | 老白的AI实践《CDISC 2026 AI 挑战结果出炉…》（2026-10-15） | 搜狗微信 type=2（链接已过期，以官方页+开源仓库为准） |
| 开源投稿（赛道1/3） | Appsilon `cdisc-case-1`（含 `synthsdtm` R 包 + `build-config` 技能） | https://github.com/Appsilon/cdisc-case-1 |
| 开源编排平台 | Appsilon `mediforce`（Apache 2.0，Control Mode + ALCOA+ 审计） | https://github.com/Appsilon/mediforce |
| 案例文档 | Synthetic SDTM / Traceable TFLs | https://mediforce.ai/case-studies/synthetic-sdtm ｜ /traceable-tfls |
| 技能安装 | `npx skills add https://github.com/Appsilon/cdisc-case-1 --skill build-config` | — |

> 本仓已克隆到本地 `WorkBuddy/2026-10-13-10-11-50/src_analysis/{cdisc-case-1,mediforce}/`（含 `synthsdtm` R 包全量源码），源码级结论以此为准。

---

## 2. 赛果全景（30 家组织 · 50 份作品 · 三赛道）

| 赛道 | 冠军（组织） | 方案 | 亚军（组织） | 方案 | 开源可见 |
|---|---|---|---|---|---|
| 1 合成测试数据 | Novartis + AWS | Syn2Real（USDM→SDTM/ADaM） | BioInformatiCo | Leova（协议→USDM→可重复场景） | 闭源 / 闭源 |
| 2 生成 SAP | Saama | Smart ClinSAP（协议→可执行 SAS/R，SADM 蓝图） | Jazz | SAP-Genie（ARS 一致 SAP + 可溯源 CDISC 包） | 闭源 / 计划中 |
| 3 生成 TFL | Novartis + AWS | PAIR（SAP+ADaM 规格→报告包） | Zifo | TLFGenix（六 agent 流水线） | 闭源 / 闭源 |

**关键看点**：6 方案的真正高价值不在"生成得多快"，而在 **"AI 知道什么时候该停下来"**——口径含糊就提交人工确认，缺变量/方法就停止流程，产物必须带 **追溯矩阵 + 执行日志 + 生成代码 + 审批记录**。

---

## 3. 唯一开源可深挖方案（Appsilon）的架构与源码发现

### 3.1 端到端架构（赛道1：NCT id → 合成 SDTM）

| 步 | 动作 | 执行者 | AI? |
|---|---|---|---|
| 1 | 输入 NCT id | 人类 | 否 |
| 2 | `fetch.py` 拉 CT.gov v2 → `study.json` | 脚本（确定性，无 key） | 否 |
| 3 | `scaffold_config.py` 机械映射 → `study_config.json` 骨架 | 脚本（确定性） | 否 |
| 3 | agent + `build-config` 技能：补"条件域 + 检测面板" | **Agent（LLM）** | **仅此步** |
| 4 | `generate.R`：`build_spec→simulate→write→check→export→CORE` | 脚本（R，确定性） | 否 |
| 5 | 人类审查生成数据：approve 或 revise（≤5 轮回到步3） | 人类（review gate） | 否 |

题眼：*"A fixed subject count or a fixed domain list is a bug, not a simplification."*（固定受试者数或固定域列表是 bug，不是简化。）

### 3.2 `scaffold_config.py`（机械映射，确定性，零 AI）
*"There is one right answer and no judgement, so an LLM adds latency and a chance of drift, not value."* —— 协议字段→结构化配置的映射必须是确定性脚本，不该让 LLM 做（避免漂移、省 token）。

### 3.3 `build-config/SKILL.md`（AI 只做"配置"——判断域范围）
纪律：① 机械映射不是 LLM 的活（禁重写 scaffold 字段）；② 域范围才是交付物（每张触发表=可校验规则，如 `EG` 仅 QTc/ECG 为终点或计划评估时加）；③ revise 模式只改最小差异、绝不可从零重建；④ 强制用 CDISC 受控术语 submission value。

### 3.4 `synthsdtm` R 包（真正的生成引擎，确定性 + seed）
`simulate_sdtm(config, spec, ct, seed)`：`set.seed(seed)` 后 `build_subjects()` 造骨架；`builders` 分发（dm/ie/mh/ex/cm/ae/ds 各自 bespoke；`build_findings()` 通用通吃 VS/EG/LB/QS… 变量名由域前缀推导）；**seed 默认 = studyId 哈希 → 同试验逐字节可复现**；`--LOBXFL`/`--NRIND` 自动算；`trace_one()` 记 lineage（cell→USDM activity→BC NCIt→protocol page）。
⚠️ 局限：`AEDECOD` 无 MedDRA 直接透传原词（stopgap），层级变量空位待接；**抄架构，别抄 AE 编码 stopgap**。

### 3.5 `study_config.schema.json`（契约）
`additionalProperties:false` + `required` 强约束 + 未知键即失败（fail-fast）；`build_spec()` 从官方 `SDTMIG v3.4 Classes and Columns.xlsx` 生成变量模板并 **pin `ct_package()="sdtmct-2026-03-27"`**（受控术语离线快照）。

### 3.6 `check.R` 三层合规 + 追溯 + 可复现（"AI 何时该停"硬保障）
- **T1 形态**：行数、SEQ 唯一无间隙、覆盖域==配置域、表头==spec、`可复现性`（同输入+seed 重生成逐 CSV diff）。
- **T2 合规**：CT 成员资格、数值可解析、Required 必填、ISO-8601 日期、结果在区间、**LINEAGE**（每个追溯样本须指向 activity + protocol page）。
- **T3 跨域**：USUBJID 参照完整性、DY 无 day-0 且由 RFSTDTC 重算、DM 的 RF* 与 EX/DS 对账、EPOCH∈CT C99079、PLACEBO 规则、OPEN-AE 规则。
- `export.R` 的 `digest_core()` 把 CORE 报告按 `data_bug / tabulation_gap / harness` 分类——诚实区分真 bug / 未实现推导 / 校验假阳性。

### 3.7 Mediforce 编排层
- **Control Mode（CM0–CM4，每步独立）**：CM0 纯人/脚本 → CM2 人机协作 → **CM3 人工审**（agent 完成、人工批准才推进，监管甜区）→ CM4 自治事后审计。cdisc-case-1 把"生成配置"设 CM3、"确定性生成/校验"设 CM0。
- **AuditEventSchema（ALCOA+）**：`actorId/actorType/actorRole`（Attributable）、`timestamp`（Contemporaneous）、`inputSnapshot/outputSnapshot`（Original）、`basis`（Accurate："基于什么做的决定"）、`processDefinitionVersion`（Consistent：追溯到工作流定义版本）、`entity/namespace/stepId`（Complete）。

---

## 4. 对 ct- 技能系列的可借鉴点（P0/P1/P2 落地清单）

| 优先级 | 借鉴点 | 落地到 | 具体做法 |
|---|---|---|---|
| **P0** | "歧义即停"HITL 闸门 | ct-sdtm / ct-adam / ct-tlf / ct-csr | 确定性脚本出骨架 → LLM 补判断域 → **生成前**人工 gate（非生成后）；禁止 AI 自行补全口径 |
| **P0** | 确定性生成 + 固定 seed | ct-sdtm（合成）/ ct-adam | "LLM 出配置 → 确定性引擎生成 → seed 固定 → 同输入输出一致" |
| **P1** | 三层合规（T1/T2/T3）+ LINEAGE + 可复现 | ct-datacheck / ct-sdtm | 对齐 `check_sdtm`：形态/合规/跨域三档；必带 cell→activity→BC→page 追溯与重生成 diff |
| **P1** | 标准工件 pin 版本 + CT 离线快照 | ct-sdtm / ct-adam / ct-base | 变量级元数据从权威 xlsx 生成并 pin `SDTMIG`/`ADaMIG`/`sdtmct` 版本；产物侧车标注 |
| **P1** | ALCOA+ 审计 + 工作流版本锁定 | ct-advisor / ct-statrev / ct-csr | 每次 AI 动作落审计记录（重点 `basis`）；输出带 `processDefinitionVersion` |
| **P1** | Control Mode 自治阶梯（CM0–CM4） | ct-advisor 路由 | 风险点默认 CM3，确定性步骤 CM0；自治级显式配置 |
| **P2** | 通用 findings builder（前缀推导变量名） | ct-sdtm | VS/EG/LB/QS… 共用 builder，新域只加 `.emit_perm` + 面板，零新代码 |
| **P2** | 标准资料索引 + CT 版本字段 | ct-base / 各技能 | 标准材料组织成索引文件（source/sheet/生成时间/源列/条数 + CT 版本）喂 LLM 检索 |

---

## 5. 警示与边界（不要把原型当生产）

1. `synthsdtm` 非生产级合规：`digest_core` 自曝 `data_bug`/`tabulation_gap`/`harness` 三类问题（AEDECOD 无 MedDRA 透传原词、层级变量空位）。**抄架构，别抄 AE 编码 stopgap**。
2. 闭源方案（Novartis/AWS、Saama）能力描述领先于开源可见代码，但看不到实现；"AI 做到了哪一步"的乐观叙述部分来自商业稿。
3. "做到了"是协作非自治：三个赛道冠军都是 agent + 确定性代码 + 人工 gate 的组合，任何"AI 全自动出 SDTM/TFL"表述须打折。
4. 开源仅覆盖 SDTM 合成 + TFL 追溯；SAP 生成（赛道2）开源参照是 Jazz 的 SAP-Genie（计划开源，截至挖掘时未见仓库），ct-sap 方向可等其落地再对标。

---

*结论：文章是入口，开源代码才是真料。最该抄的不是"AI 生成数据"炫技表述，而是工程纪律——确定性引擎 + 固定种子 + LLM 只喂受约束配置 + 风险点人工 gate + ALCOA+ 审计。全套纪律固化于 ct-base §22，叶子技能按 §22 对齐。*
