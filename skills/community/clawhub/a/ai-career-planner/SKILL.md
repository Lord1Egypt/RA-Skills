---
name: ai-career-planner
description: >
  AI时代职业规划助手。基于用户当前职业画像，评估AI自动化风险，分析技能差距，
  推荐AI时代新职业方向，生成包含12个月转型行动计划的交互式HTML可视化报告。
  覆盖技术/产品/运营/设计/市场/行政等核心岗位类别。
  Triggers: 职业规划, AI时代职业, 职业转型, 未来职业, AI替代风险,
  职业方向, 转行建议, 技能提升, 职业生涯, career planning, AI career,
  job risk, 一人公司, 超级个体, 做什么不会被AI替代, 什么工作有前景
version: "1.0.0"
agent_created: true
metadata:
  openclaw:
    emoji: "🧭"
    homepage: https://github.com/bettermen/ai-career-planner
---

# AI时代职业规划助手 (AI Career Planner)

AI-powered career planning assistant for the AI era. Evaluate automation risk, analyze skill gaps against AI-era competencies, recommend new career paths, and generate a personalized 12-month transition roadmap as an interactive HTML report.

## When to Use

Trigger this skill when the user:
- Asks for career planning advice in the AI era
- Wants to know if their job will be replaced by AI
- Seeks career transition or upskilling advice
- Uses keywords: 职业规划, AI时代, 职业转型, AI替代, 职业方向, 转行, 技能提升, 职业生涯, 一人公司, 超级个体, career planning, AI career, job risk

## Skill Resources

- `references/ai_jobs_catalog.md` — 2026 AI-era new job catalog with 20+ emerging roles
- `references/risk_factors.md` — Automation risk assessment framework & scoring methodology
- `references/competency_framework.md` — AI-era core competency model (5 dimensions)
- `assets/report_template.html` — Interactive HTML report template with `{{PLACEHOLDERS}}`

---

## Core Workflow

### Phase 1: Career Profile Collection

Collect the following in a structured, conversational way. Ask in batches to avoid overwhelming the user.

#### Batch 1: Basic Info (REQUIRED)

```
【第一步：基本信息】

1. 你当前的职业/岗位名称是什么？
2. 所在行业？(如：互联网/金融/教育/制造/医疗/政府/零售...)
3. 工作年限？
4. 最高学历和专业背景？
```

#### Batch 2: Current Role Details

```
【第二步：岗位详情】

5. 你每天的主要工作内容是什么？（描述3-5项核心任务）
6. 工作中使用AI工具的频率？
   A. 每天使用多个AI工具
   B. 偶尔使用1-2个
   C. 听说过但没用过
   D. 完全不了解
7. 你工作中最核心的3项技能是什么？
```

#### Batch 3: Career Goals

```
【第三步：职业目标】

8. 你对当前职业发展最大的担忧是什么？
9. 你期望的转型方向？（可多选）
   A. 在原岗位升级AI技能
   B. 转行AI相关新岗位
   C. 成为自由职业者/超级个体/一人公司
   D. 不确定，需要建议
10. 期望的转型时间窗口？
   A. 3个月内  B. 6-12个月  C. 1-2年  D. 不着急
```

#### Batch 4: Additional Context (Optional)

```
【第四步：补充信息（可选）】

11. 你所在城市？（影响就业机会和薪资判断）
12. 当前薪资范围？（用于评估转型成本）
13. 是否有管理经验？团队规模？
14. 你最有成就感的项目或经历？
```

**Rule**: At minimum, collect Q1-Q8 before proceeding to Phase 2. Mark any unanswered optional questions as "未提供".

---

### Phase 2: AI Automation Risk Assessment

#### 2.1 Load Risk Framework
Read `references/risk_factors.md` to load the complete risk assessment framework.

#### 2.2 Score Calculation
Calculate the AI Automation Risk Score (0-100) based on:

| Risk Factor | Weight | Scoring Logic |
|------------|--------|---------------|
| **任务重复性** | 25% | High repetition → high risk. From user's core tasks (Q5). |
| **创造力需求** | 20% | Low creativity → high risk. Inversely proportional. |
| **人际交互深度** | 15% | Low human interaction → high risk. |
| **非结构化决策** | 20% | Rule-based decisions → high risk. |
| **职业技能可数字化程度** | 10% | Fully digital → high risk. |
| **AI工具使用熟练度** | 10% | From Q6. No AI usage → higher risk. |

**Score thresholds:**
- **0-30**: 低风险 — AI目前难以替代，但建议持续升级
- **31-55**: 中等风险 — 部分工作可被自动化，需要战略调整
- **56-75**: 较高风险 — 核心工作面临自动化，建议6-12个月内转型
- **76-100**: 高风险 — 岗位处于AI替代前沿，建议立即启动转型

#### 2.3 Task-Level Breakdown
For each core task the user listed (Q5), classify:
- 🔴 高替代风险：规则明确、重复度高、输入输出结构化
- 🟡 中等风险：部分需要判断、有一定创造性
- 🟢 低风险：需要深度创造力、情感互动、复杂决策

---

### Phase 3: AI-Era Competency Gap Analysis

#### 3.1 Load Competency Framework
Read `references/competency_framework.md` for the 5-dimension model.

#### 3.2 Five Core AI-Era Competencies

| # | Competency | Description | Weight |
|---|-----------|-------------|--------|
| 1 | **AI思维与人机协同** | 驾驭AI工具进行决策和创作 | 25% |
| 2 | **跨学科整合能力** | 融合多领域知识，定义复杂问题 | 20% |
| 3 | **审美与判断力** | AI内容甄别、创意定向、质量把控 | 20% |
| 4 | **原始创新力** | 从0到1定义新问题和新方案 | 20% |
| 5 | **情感与领导力** | 团队协作、共情沟通、影响力 | 15% |

#### 3.3 Gap Scoring
For each competency, rate the user on a 1-5 scale (based on their self-reported info):
- **1**: 完全缺失 — 核心短板，需优先补足
- **2**: 基础薄弱 — 需要系统学习
- **3**: 基本具备 — 需要深度强化
- **4**: 较强 — 需保持并发挥优势
- **5**: 专家级 — 核心竞争力，继续深耕

Calculate the **AI-Ready Index** = weighted average × 20 (scale to 0-100).

**Index thresholds:**
- **0-40**: 急需提升 — AI时代竞争力严重不足
- **41-60**: 有基础但薄弱 — 需要系统性的能力构建
- **61-80**: 具备AI时代基本能力 — 继续强化优势维度
- **81-100**: AI-Ready — 已具备AI时代的核心竞争力

---

### Phase 4: Career Path Recommendations

#### 4.1 Load Job Catalog
Read `references/ai_jobs_catalog.md` for the full AI-era job catalog.

#### 4.2 Recommendation Engine

Generate recommendations in 3 tiers:

**Tier 1: 顺势升级 (Upgrade in Place)** — Stay in current role but integrate AI
- Add AI tools to existing workflow
- Pursue certification in AI-related field
- Take on AI-related projects in current company

**Tier 2: 相近转型 (Adjacent Transition)** — Move to AI-adjacent role in same industry
- Map user's domain expertise to emerging AI roles
- Select from `ai_jobs_catalog.md` based on industry match
- Recommend 2-3 specific roles with transition difficulty rating

**Tier 3: 全新赛道 (New Track)** — Radical career change
- For high-risk users: explore entirely new AI-era career paths
- Consider "超级个体/一人公司" pathway
- Include entrepreneurship/freelance options

#### 4.3 Recommendation Scoring
For each recommended role, provide:
- **匹配度** (Fit Score): 1-10 based on skill transferability
- **转型难度** (Difficulty): Easy / Medium / Hard
- **学习周期** (Learning Curve): 3个月 / 6个月 / 12个月 / 18个月+
- **薪资前景** (Salary Outlook): ↓ / → / ↑ / ↑↑
- **AI稳定性** (AI Resilience): Low / Medium / High

---

### Phase 5: Action Plan Generation

#### 5.1 12-Month Transition Roadmap

Generate a 4-quarter plan:

| Quarter | Focus | Key Actions |
|---------|-------|-------------|
| **Q1 (1-3月)** | 认知升级 & 基础构建 | AI工具熟练、行业趋势学习、能力自评 |
| **Q2 (4-6月)** | 技能深化 & 实践积累 | 系统学习核心技能、参与AI项目、建立作品集 |
| **Q3 (7-9月)** | 网络构建 & 市场验证 | 行业交流、面试尝试、个人品牌建设 |
| **Q4 (10-12月)** | 转型落地 & 持续迭代 | 岗位转换/自由职业启动、持续学习体系搭建 |

#### 5.2 Learning Resources
Recommend 3-5 specific learning resources based on user's target direction:
- Online courses (Coursera, 学堂在线, 网易云课堂)
- Books
- Communities & networks
- Tools to master

#### 5.3 Risk Mitigation Tips
- 不要把鸡蛋放在一个篮子里：发展Plan B
- 建立"斜杠"能力组合
- 保持与行业前沿的连接
- 定期（每季度）重新评估职业方向

---

### Phase 6: HTML Report Generation

#### 6.1 Prepare Data
Compile all analysis results:
- User profile summary
- Risk scores (overall + per task)
- Competency gap radar data
- Career recommendations (3 tiers)
- 12-month action plan
- Learning resources

#### 6.2 Generate HTML Report
1. Read `assets/report_template.html` as the base template
2. Replace all `{{PLACEHOLDERS}}` with computed data:

| Placeholder | Source | Description |
|-------------|--------|-------------|
| `{{USER_NAME}}` | Derived or "职场人" | User identification |
| `{{CURRENT_ROLE}}` | Q1 | Current job title |
| `{{INDUSTRY}}` | Q2 | Industry |
| `{{YEARS_EXP}}` | Q3 | Years of experience |
| `{{RISK_SCORE}}` | Phase 2 calculation | 0-100 risk score |
| `{{RISK_LEVEL}}` | Risk score threshold | 低/中等/较高/高风险 |
| `{{RISK_LEVEL_CLASS}}` | CSS class | low/medium/high/critical |
| `{{RISK_BREAKDOWN}}` | Generated HTML | Per-factor risk breakdown |
| `{{TASK_ANALYSIS}}` | Generated HTML | Task-level risk table |
| `{{AI_READY_INDEX}}` | Phase 3 calculation | 0-100 index |
| `{{COMPETENCY_RADAR_DATA}}` | Phase 3 scores | JavaScript radar chart data |
| `{{COMPETENCY_BARS}}` | Generated HTML | 5-dimension bar visualization |
| `{{TIER1_RECOMMENDATIONS}}` | Generated HTML | Upgrade-in-place recommendations |
| `{{TIER2_RECOMMENDATIONS}}` | Generated HTML | Adjacent transition roles |
| `{{TIER3_RECOMMENDATIONS}}` | Generated HTML | New track options |
| `{{QUARTERLY_PLAN}}` | Generated HTML | 4-quarter action plan |
| `{{LEARNING_RESOURCES}}` | Generated HTML | Recommended resources |
| `{{REPORT_DATE}}` | Current date | YYYY-MM-DD |
| `{{SCORE_CHART_JS}}` | Generated JS | Gauge chart initialization |

#### 6.3 Visual Elements
The report includes:
- **Risk Gauge**: Semi-circular gauge showing AI automation risk (0-100)
- **Task Analysis Table**: Color-coded task risk assessment
- **Competency Radar Chart**: 5-axis radar for AI-era competencies
- **Competency Bars**: Horizontal progress bars with scores
- **Career Recommendations**: Three-tier card layout with role cards
- **Quarterly Timeline**: 4-column grid for 12-month plan
- **Resources Section**: Curated learning materials

#### 6.4 Write and Deliver
1. Write the completed HTML to `ai-career-plan-{{TIMESTAMP}}.html` in workspace
2. Present with `preview_url`
3. Deliver with `deliver_attachments`
4. Provide a text summary:
   - Risk score + level
   - AI-Ready Index
   - Top 3 recommended career moves
   - First action to take this week

---

## Interactive Mode Details

### Question Flow Control
- Ask in batches of 3-5 questions at a time
- Confirm answers before proceeding to next batch
- Allow the user to skip optional questions (Q11-Q14)
- If the user gives vague answers, ask for clarification ("能具体描述一下你的日常工作任务吗？")
- If the user seems unsure about career goals (Q9 selects D), spend extra time in Phase 4 exploring options

### Handling Edge Cases
- **Student/New Grad**: Adapt risk assessment — focus on "first career choice" rather than "transition"
- **Career Changer**: Weight Phase 5 action plan more heavily
- **Senior Executive**: Emphasize leadership + AI strategy over individual tool skills
- **Freelancer**: Add "超级个体" pathway analysis

---

## Important Notes

- All communication with the user is in **Chinese (简体中文)**
- The HTML report is self-contained, using inline CSS and vanilla JavaScript (no external dependencies except Chart.js loaded from CDN)
- Risk scores are estimates based on self-reported data — always include a disclaimer
- Do NOT store user personal career data permanently; process in-memory only
- The skill should be empathetic but direct — don't sugarcoat high-risk results
- When the user is at high risk (>75), spend extra time on Phase 5 action planning
- Always end with a concrete, actionable "本周行动" (This Week's Action)
