# CLAIM-GATE 结论勾稽闸 · 通用框架模板（L2 子类）

> 2026-08-16 泛化成族（GENERALIZE-GATE 立即泛化档执行产物）。
> 本源实证：post_gate_audit（复核）；已克隆：council_reverify（会诊）、acceptance_verdict（验收）。
> 定位：锚点闸的姊妹闸——锚点闸管"证据真不真"，本闸管"结论对不对得上证据"。

## 一、适用判定（什么时候用本框架）

- 产出物是**结论型**：复核报告 / 会诊结论 / 验收结论 / 评估打分……含数值断言、定级、充分性、遗漏判定
- 已有或将有证据锚点机制，但"锚点真 ≠ 结论对"：数字可以是编的、结论可以与数据矛盾、定级可以随口
- **不适用**：纯语义解读本体（留软层，禁止勾稽化）；无数值/枚举可勾稽的自由文本

## 二、冻结契约（骨架 · 四枚举逐字冻结）

`claim` 为**可选**字段：不带不罚，出现即强校验。`claim_type` 未知即违例（防自由发挥）。

| claim_type | 必填字段 | 机械勾稽规则 |
|---|---|---|
| `coverage_verdict` | actual/threshold（数值）、direction（gte\|lte）、verdict（pass\|fail） | verdict 必须与数值比较结果一致；actual 必须可追溯（锚点行原文包含，或对数据源字段严格相等） |
| `severity_rating` | severity、critical\|high\|medium\|low、rationale ≥10 字 | 与宿主条目 severity（若存在）必须一致（自洽） |
| `evidence_sufficiency` | required_refs（正整数） | 实际证据/锚点数 ≥ required_refs |
| `boundary_omission` | — | 报遗漏即宿主 verdict 不得为 pass 等价集 |

## 三、接入五步法（实例化）

1. **定挂载点**：结论数组字段（findings[] / details[] / verdict 条目[]）
2. **定追溯源**：锚点行取数 or 数据源点路径取数（二选一，写死进 checker）
3. **克隆 checker**：从既有 checker 脚本（如复核报告校验器）的 `check_claims` 复制，只改取数与字段映射；exit 0=A / 1=B / 3=CLARIFY，单行 JSON 输出
4. **spec 接线**：gate-switch spec 加 script_exit 包装，desc/label 同步
5. **实证三件套**：pytest ≥5 用例（正向 A + 各勾稽矛盾 B + 无 claim 兼容）→ 真闸端到端 A/B 各扳一次 → 存量真实样本兼容实证

## 四、适配点白名单（仅此两类，其余改动即新原语，须回 REFORM-GATE）

1. 锚点/取数方式（file:line 锚点行原文 / 数据源字段点路径）
2. 字段名映射（findings→details、verdict 的 pass 等价集、severity 宿主字段等）

## 五、反例（禁止勾稽化，留软层）

- "分析是否到位""建议是否合理"等解读本体
- 给骨架加第五条枚举——先举证 ≥2 个独立场景现有四枚举表达不了，过 REFORM-GATE 再说

## 六、已入族实例

| 实例 | 闸 | 挂载点 | 追溯源 |
|---|---|---|---|
| 本源 | post_gate_audit | findings[].claim | file:line 锚点行原文 |
| 克隆 | council_reverify | verdict 条目.claim | verdict 文本内联 file:line |
| 克隆 | acceptance_verdict | details[].claim | test-master-report.json 点路径 |
