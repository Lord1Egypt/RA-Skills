# 投标模拟评标 · 魔鬼评委 — 测试用例

## 用例 L：评标表解析 + 模拟打分端到端

**目标**：验证 `parse_score_table.py` 能从《评标表》docx 准确抽取评分项（因素/分值/类型/证据要求），并产出可供 LLM 核定打分的 `criteria.json`。

**输入**：
- `demo/eval_table.docx`（含 5 项评分表：企业资质/类似业绩/技术方案/项目团队/售后服务）
- `demo/response.docx`（我方响应，含部分证据、部分缺失）

**步骤**：
```bash
$VENV scripts/parse_score_table.py demo/eval_table.docx --out demo/criteria.json
$VENV scripts/parse_score_table.py --mode response demo/response.docx --out demo/response.txt
```

**预期（断言）**：
1. `criteria.json` 含 **5** 项，`score` 分别为 6/10/15/9/10。
2. `type` 判定：企业资质=objective、类似业绩=objective、技术方案=subjective、项目团队=objective、售后服务=subjective。
3. `evidence_required=true` 应出现在企业资质、类似业绩、项目团队三项。
4. `needs_review` 全为 false（抽取完整）。
5. `response.txt` 非空（>150 字符），含「电子与智能化」「ISO」未出现等可供 LLM 对照的关键词。

**LLM 模拟打分验证（人工核对样例）**：
- 企业资质：一级资质证据在→3；ISO 未在响应出现→0 → 模拟 3/6（客观·高）
- 类似业绩：响应 2 项→4/10（客观·高）
- 模拟总分 26/50，与 `demo/mock_eval_report.md` 一致。

**回归红线**：若 `criteria.json` 项数 ≠ 5 或 `type` 全为 unknown，判定解析回归，需检查表格表头识别逻辑。

## 用例 M：评标表合规审查（模式 C，问题表）

**目标**：验证解析能标出 `is_knockout` 否决项，且 LLM 能对照六维度产出可质疑点清单。

**输入**：`demo/eval_table_noncompliant.docx`（含：①企业资质「须提供 XX 品牌原厂授权，否则否决投标」②价格分占比 20% ③技术方案「优者得满分，无档位描述」④业绩「单项合同金额≥5000 万元」⑤本地服务「须本地常驻网点」）

**步骤**：`$VENV scripts/parse_score_table.py demo/eval_table_noncompliant.docx --out demo/criteria_noncompliant.json`

**预期（断言）**：
1. `is_knockout=true` 至少出现在 **2** 项：企业资质（否则否决投标）、本地服务（否则不得分）。
2. LLM 对照 `references/compliance-review.md` 六维度，至少识别：
   - Q1 歧视性（限定品牌原厂授权）→ 招投标法第 18/20 条、政府采购法第 22 条
   - Q2 价格分占比 20% < 法定 30% 下限 → 87 号令第 55 条
   - Q3 主观不可量化（无档位）→ 87 号令第 55 条
   - Q4 业绩门槛 5000 万过高变相排斥 → 政府采购法第 22 条
   - Q5 本地网点限定地域 → 政府采购法第 22 条 / 中小企业扶持例外
3. 每条含「条款原文 + 违规类型 + 法条方向 + 风险等级（🔴/🟡/⚪）」。

**回归红线**：若 `is_knockout` 全为 false，判定否决项识别回归。

## 用例 N：响应覆盖审计（模式 B）

**目标**：验证 `--mode audit` 覆盖初判 + LLM 精修流程。

**输入**：`demo/criteria.json` + `demo/response.docx`

**步骤**：
```bash
$VENV scripts/parse_score_table.py demo/eval_table.docx --out demo/criteria.json
$VENV scripts/parse_score_table.py --mode audit --criteria demo/criteria.json demo/response.docx --out demo/coverage_hints.json
```

**预期（断言）**：
1. `coverage_hints.json` 含 **5** 项，`coverage_hint ∈ {covered, partial, missing}`。
2. 脚本初判可能因「关键词命中 ≠ 真实覆盖」而偏乐观（如企业资质 hit 到「企业资质」但 ISO 实际缺失）；**LLM 精修须纠正**：企业资质=partial（ISO 缺），不得直接判 covered。
3. LLM 产出：得分点地图（按分值降序，否决项置顶）+ 覆盖审计表（✅/⚠️/❌/▶）+ 评分索引表。

**回归红线**：若 `coverage_hints.json` 项数 ≠ 5，判定 audit 回归。
