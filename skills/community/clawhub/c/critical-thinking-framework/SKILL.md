---
name: critical-thinking-framework
version: 1.0.0
description: 基于津巴多心理学六问法，对任何新观点、主张或信息进行系统性、结构化的批判性审视。通过六个递进维度的分析，识别潜在偏差、验证逻辑有效性，并形成经过多重检验的审慎结论。适用于评估新闻报道、科学主张、政策建议及日常决策。
---

### Parameters
| Parameter            | Type   | Required | Description                                                  |
| -------------------- | ------ | -------- | ------------------------------------------------------------ |
| `claim`              | string | Yes      | 待分析的具体观点或主张（如"糖会导致儿童亢奋"）               |
| `source_info`        | object | No       | 观点来源信息，包含`author`（作者）、`credentials`（资质）、`affiliation`（所属机构）、`potential_interests`（潜在利益） |
| `evidence_available` | array  | No       | 当前可获取的支持性证据列表（轶事、统计数据、实验结果等）     |
| `domain`             | string | No       | 观点所属领域（医学/心理学/社会学/政策等），用于选择专业视角  |

### Execution Steps

**Step 1: 权威溯源与利益审查 (Source & Interest Verification)**
- 核查提出者是否具备相关领域的实际专业资质（非自封专家）
- 识别利益冲突：是否存在政治资本、经济利益或媒体曝光动机？
- **输出标记**: `source_credibility` (high/medium/low), `conflict_of_interest` (boolean)

**Step 2: 主张合理性校准 (Claim Plausibility Calibration)**
- 应用"卡尔·萨根原则"：不寻常的主张需要不寻常的证据
- 评估与现有科学共识的兼容性，警惕"突破/革命"式宣传
- 质疑"快速解决复杂问题"的承诺（如简单方法解决青少年犯罪）
- **输出标记**: `claim_plausibility` (plausible/suspicious/extreme), `evidence_barrier` (high/low)

**Step 3: 证据质量分级 (Evidence Hierarchy Evaluation)**
- 区分轶事证据（个人证词、精心挑选的案例）与实证证据（可重复实验、大样本研究）
- 检查是否存在"将适合少数人的事物推断为适合所有人"的风险
- **输出标记**: `evidence_type` (anecdotal/correlational/experimental), `generalizability_risk` (high/medium/low)

**Step 4: 认知偏差识别 (Cognitive Bias Detection)**
- **情感偏差**：是否存在绝望、恐惧等强烈情绪影响判断？（如绝望父母 grab any straw）
- **证实性偏差**：是否只记住支持信念的证据而忽略反证？（如占星术信徒的选择性记忆）
- **期望偏差**：观察者是否因预期而看到"想看到的结果"？（如预期糖导致亢奋而高估活跃程度）
- **输出标记**: `detected_biases` (array: [emotional_bias, confirmation_bias, expectancy_bias])

**Step 5: 逻辑谬误规避 (Logical Fallacy Avoidance)**
- **相关-因果谬误检查**：是否将时间先后或统计关联等同于因果关系？
- 考虑第三变量解释（C变量）：是否存在同时影响A和B的隐藏因素？
- 警惕"常识替代科学"（如"物以类聚"与"异性相吸"的矛盾常识）
- **输出标记**: `causal_validity` (valid/suspected_fallacy), `third_variables` (array)

**Step 6: 多元视角整合 (Multi-perspective Integration)**
- 强制要求至少3个不同学科视角：
  - **生物/心理视角**：遗传、神经机制、人格特质（如糖代谢对大脑的影响）
  - **社会/情境视角**：环境压力、群体规范、文化背景（如聚会氛围对儿童行为的影响）
  - **经济/系统视角**：成本收益、结构性因素、激励机制
- **输出标记**: `perspectives_considered` (array), `complexity_level` (simple/complex)

### Output Format
```json
{
  "analysis_summary": {
    "overall_trustworthiness": "low/medium/high",
    "key_risks": ["利益冲突", "相关-因果谬误", "情感偏差"],
    "recommended_action": "reject/suspend_judgment/accept_with_caution"
  },
  "detailed_assessment": {
    "source": {"credibility": "...", "conflicts": "..."},
    "claim": {"plausibility": "...", "required_evidence_level": "..."},
    "evidence": {"quality": "...", "generalizability": "..."},
    "biases": ["emotional_bias", "confirmation_bias"],
    "logic": {"causal_validity": "...", "alternative_explanations": ["..."]},
    "perspectives": ["biological", "social", "economic"]
  }
}