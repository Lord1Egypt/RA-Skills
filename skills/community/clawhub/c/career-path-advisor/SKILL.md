---
name: Career Path Advisor
slug: career-path-advisor
description: Map your career trajectory: skill gap analysis, role transitions, and personalized learning roadmaps based on market data.
tags: [career, job-search, skill-gap, learning-path, career-planning, china, professional-development]
version: 1.0.0
license: MIT-0
---

# Career Path Advisor (职业路径顾问)

Turn career anxiety into an actionable plan. Analyze your current skill stack against market demands, identify gaps, and generate personalized career roadmaps with concrete learning milestones — all grounded in real job market data, not generic advice.

## Prerequisites

The CLI script requires two common tools:

| Tool | Purpose | Install (macOS) | Install (Ubuntu/Debian) |
|------|---------|-----------------|-------------------------|
| **jq** | JSON processing (role matching, JSON output) | `brew install jq` | `sudo apt install jq` |
| **python3** | Dynamic role matching, gap analysis computation | Ships with macOS | `sudo apt install python3` |

Both are pre-installed on most development machines. Verify with:
```bash
jq --version
python3 --version
```

## Core Capabilities

- **Skill Radar Mapping**: Inventory your current skills and visualize strengths vs gaps with a structured radar chart
- **Market-Driven Gap Analysis**: Scrape target role JDs to extract real, current skill demands — not textbook lists
- **Multi-Path Generation**: Produce 2–4 viable career trajectories (lateral move / promotion / industry switch / functional pivot)
- **Learning Roadmaps**: Per-path timeline with milestones, recommended resources (courses, books, projects), and completion estimates
- **Offer Comparison Engine**: Decision matrix for evaluating multiple job offers across compensation, growth, culture, and risk
- **Industry Transition Planner**: Special handling for career changers — transferable skill mapping and bridge-role recommendations
- **Salary Benchmarking**: Market salary ranges by role, city, and experience level based on current job listings

## Workflow (9 Steps)

### Step 1: Current State Capture
**Input**: User provides:
- **Current role & title** (e.g., "Java后端开发, 高级工程师")
- **Years of experience** (e.g., 5 years)
- **Industry** (e.g., "互联网金融", "跨境电商")
- **Core skills** (free-form: "Spring Boot, MySQL, Redis, 微服务")
- **Education & certifications** (optional)
- **Location** (for salary benchmarking)
- **Target direction** (optional — e.g., "想转AI", "想做技术管理", "还在探索")

**Output**: Structured career profile.
**Logic**: If target is "还在探索", move to Step 2 exploration mode. Otherwise skip to Step 4 for gap analysis.

### Step 2: Career Exploration (if no target)
**Input**: Career profile with no target direction.
**Action**: Based on current skills + experience + industry trends, generate 5-7 possible directions:
- **Ladder-up**: Senior/Staff/Principal IC within same track
- **Management pivot**: Tech lead → Engineering Manager
- **Adjacent role**: Backend → SRE, Backend → Data Engineer
- **Industry switch**: Fintech → E-commerce, Gaming → Enterprise SaaS
- **Radical pivot**: Engineer → Product Manager, Developer → Technical Writer

**Output**: Exploration menu with:
- Direction name + title examples
- Estimated difficulty (Easy / Moderate / Hard)
- Time to transition (3m / 6m / 12m+)
- Salary impact (↑ / ≈ / ↓)
- Match score with current skills

**Logic**: Flag unrealistic directions (e.g., 2 years experience → CTO).

### Step 3: Target Role Selection
**Input**: Exploration menu (or user-provided target).
**Action**: User selects 1-3 target directions. Confirm with clarifying questions:
- Preferred company tier (大厂/中厂/创业公司)?
- Willing to relocate?
- Salary floor?
- Hard constraints (e.g., "不接受996", "必须在上海")?

**Output**: Confirmed target role(s) with user constraints.

### Step 4: Market Data Collection
**Input**: Target role(s) + location + company tier preference.
**Action**: Scrape current job listings (Lagou, BOSS Zhipin, LinkedIn) for target roles:
- Extract top 20 JDs per target role
- Aggregate: required skills, preferred skills, experience range, salary range
- Identify trending skills (skills appearing in 2026 JDs but not 2024 JDs)
- Note: certificates, tools, and domain knowledge frequently listed

**Output**: Market demand dataset:
```
Target: AI Engineer (Shanghai, 3-5yr exp)
Demand: 850+ open positions
Salary Range: ¥30K–60K/month
Top Required Skills: Python (98%), PyTorch (82%), Transformer (71%), MLOps (58%), CUDA (45%)
Trending (↑): LangChain (240% YoY), Vector DB (180% YoY)
```

### Step 5: Skill Gap Analysis
**Input**: Current skill stack + market demand dataset.
**Action**: Map current skills against market requirements:

| Skill | Your Level | Market Demand | Required Level | Gap |
|-------|-----------|---------------|----------------|-----|
| Python | ⭐⭐⭐⭐ | Critical | ⭐⭐⭐⭐ | ✅ No gap |
| PyTorch | ⭐⭐ | Critical | ⭐⭐⭐⭐ | 🔴 Large gap |
| MLOps | — | Important | ⭐⭐⭐ | 🔴 Missing |
| Docker | ⭐⭐⭐ | Nice-to-have | ⭐⭐ | ✅ Exceeds |

**Gap Score**: Weighted by demand criticality × gap size.
**Output**: Gap matrix + radar chart visualization (Mermaid/text).

### Step 6: Path Planning
**Input**: Confirmed target + gap matrix + user constraints.
**Action**: Generate 2–4 concrete paths:

**Path A: Direct Apply** (最快)
- Suitable when gap is small (<30% new skills needed)
- Timeline: 1–3 months (resume polish + interview prep)
- Action items: Update resume, practice system design, apply to 20+ positions

**Path B: Skill-Build then Apply** (最稳)
- Suitable when gap is moderate (30–60% new skills needed)
- Timeline: 3–6 months (learning + project building + apply)
- Action items: Complete 2 courses, build 1 portfolio project, network with target companies

**Path C: Bridge Role** (渐进)
- Suitable when gap is large (>60% new skills) or industry-switching
- Timeline: 6–12 months
- Action items: Take adjacent role first, learn on the job, internal transfer or re-apply

**Path D: Parallel Exploration** (探索)
- Try 2 directions simultaneously with low commitment
- Timeline: 2–4 months to decide
- Action items: Side projects, informational interviews, part-time consulting

**Output**: Per-path summary with timeline, milestones, effort estimate (hours/week), and success probability.

### Step 7: Learning Roadmap Generation
**Input**: Selected path + gap matrix.
**Action**: Generate a week-by-week or month-by-month learning plan:
- **Month 1**: Foundation courses (Coursera, B站, 极客时间)
- **Month 2**: Hands-on projects (build X, contribute to Y)
- **Month 3**: Advanced topics + interview prep
- Resources: Specific course names, book titles, GitHub repos, Chinese/English learning materials
- Checkpoints: "By end of Month 1, you should be able to..."

**Output**: Detailed learning roadmap with estimated hours per week and resource links.

### Step 8: Offer Decision Matrix (if applicable)
**Input**: 2+ job offers with details (salary, equity, team, growth, location, culture).
**Action**: Build a weighted decision matrix:

| Dimension | Weight | Offer A | Offer B | Offer C |
|-----------|--------|---------|---------|---------|
| Base Salary | 25% | ¥45K | ¥38K | ¥50K |
| Equity/Stock | 15% | Options | RSUs | None |
| Career Growth | 20% | Fast track | Stable | Unknown |
| Team & Culture | 15% | Strong | Risk | Good |
| Location/Commute | 10% | 30min | Remote | 60min |
| Work-Life Balance | 10% | 996 rumor | 1075 | Flexible |
| Company Stability | 5% | Series C | Public | Series A |

**Output**: Weighted scores + sensitivity analysis (how ranks change if you weight growth higher than salary). Risk flags per offer.

### Step 9: Final Report
**Input**: All analysis results.
**Action**: Compile the Career Development Plan:
1. **Current State**: Skill radar + strengths/weaknesses
2. **Target Analysis**: Market demand + salary benchmark
3. **Gap Analysis**: What you need to learn, ranked by priority
4. **Recommended Path**: Top pick with rationale
5. **Learning Roadmap**: Month-by-month plan with resources
6. **Action Items**: This week / this month / this quarter
7. **Progress Tracking**: Suggested monthly check-ins

**Output**: Complete career development plan in Markdown. Option to track progress in follow-up sessions.

## Sample Prompts

### Prompt 1: Career Exploration
**User**: "我是做Java后端的，5年经验，感觉遇到了瓶颈。帮我看看有哪些发展方向"
**Expected Output**: Exploration menu with 5-7 directions (Senior/Staff IC, Tech Lead/Manager, SRE/DevOps, Data Engineer, Solution Architect), each with difficulty, timeline, salary impact, and match score. Top 3 picks with rationale.

### Prompt 2: Specific Role Transition
**User**: "我想从后端开发转AI工程师，帮我分析需要学什么，大概要多久"
**Expected Output**: Market data for AI Engineer roles → gap matrix (Python: no gap, PyTorch: large gap, MLOps: missing) → 3 paths (Direct/6-month/12-month) → learning roadmap with specific courses and projects.

### Prompt 3: Offer Comparison
**User**: "收到3个offer：字节跳动45K、一家B轮创业公司50K+期权、外企38K但轻松。帮我分析怎么选"
**Expected Output**: Decision matrix with weighted dimensions → total scores → "If you prioritize growth: ByteDance (82). If you prioritize WLB: Foreign company (78). If you prioritize upside: Startup (75 but high variance)."

### Prompt 4: Industry Switch
**User**: "我在传统制造业做IT，想转互联网行业。应该怎么切入？"
**Expected Output**: Transferable skill mapping → bridge role recommendations (e.g., "先用制造业+IT的经验切入工业互联网/智能制造赛道") → learning gap analysis → 6-month transition plan.

### Prompt 5: First Job Planning
**User**: "应届生，计算机专业，不知道该选前端/后端/算法/测试。帮我分析一下"
**Expected Output**: Per-direction analysis: market demand (current + projected), salary curves, learning difficulty, career ceiling, remote work potential. Personalized recommendation based on user's interests (ask if unknown).

### Prompt 6: Career Plateau Check
**User**: "工作7年了还是高级工程师，感觉升不上去。帮我诊断一下问题"
**Expected Output**: "Career plateau diagnosis": ① Technical depth vs breadth analysis ② Visibility check (internal impact, external presence, mentoring) ③ Market comparison (do you have Staff-level skills?) ④ Action plan: specific changes to make in next 6 months.

## Real Task Examples

### Example 1: Mid-Career Pivot
**Scenario**: 30-year-old frontend developer, worried about AI replacing frontend work.
**Input**: "我做了6年前端，React/Vue/TypeScript都很熟。但AI写前端越来越强，我是不是该转行？如果要转，转什么？"
**Steps**:
1. Profile: 6yr Frontend, strong JS/TS, experienced in UI architecture.
2. Exploration: 5 directions generated.
3. Market data: Frontend demand still strong but shifting — "full-stack frontend" (Next.js, edge computing) growing. AI-assisted frontend engineering is new niche.
4. Gap analysis: To full-stack: need backend basics (Node.js already known → gap small). To AI: large gap.
5. Recommendation: Path A (evolve to Full-Stack/Architecture) 3-6 months vs Path B (pivot to AI Engineering) 12 months.
**Output**: "不建议完全转行。前端的终点不是被AI替代，而是成为'AI-Native前端架构师'。6个月学习计划: Next.js App Router → Edge Computing → AI SDK integration → 成为团队里最懂AI的前端。"

### Example 2: Offer Decision
**Scenario**: Senior engineer with competing offers, torn between growth and stability.
**Input**: Offer comparison with detailed numbers.
**Steps**:
1. Quantify each dimension with user-assigned weights.
2. Calculate total weighted scores.
3. Sensitivity analysis: "If you weight career growth at 30% instead of 20%, ranks change..."
4. Hidden factors: equity liquidity, company runway, team churn rate (ask user to research).
5. "Gut check" prompt: "Imagine you've been at Company A for 6 months. How do you feel?"
**Output**: Decision matrix with clear recommendation + key assumptions to verify before accepting.

### Example 3: Return-to-Work
**Scenario**: Parent returning to workforce after 2-year gap.
**Input**: "休息了2年带娃，之前做了4年的产品经理。现在想回去工作，但感觉脱节了。"
**Steps**:
1. Profile: 4yr PM experience, 2yr gap, target = PM again.
2. Market scan: PM landscape changes in 2 years (AI PM, Growth PM niches emerged).
3. Gap: General PM skills intact. Gaps in: AI/LLM product knowledge (new trend), latest tools (Figma, Notion are standard now).
4. Path: 2-month ramp-up → apply. Learning plan: AI PM fundamentals + build case study.
**Output**: "2年gap不是劣势，把它重新定义为'高强度项目管理经验'。2个月回归计划: Week 1-2行业更新阅读 → Week 3-4项目实战 → Week 5-8投递面试。建议先从B轮-C轮公司切入，比大厂更容易接受gap。"

## Scripts

| Path | Description |
|------|-------------|
| `scripts/advisor.sh` | Main CLI script — profile-based or interactive career analysis |
| `schemas/input.schema.json` | JSON Schema for workflow input (career profile) |
| `schemas/output.schema.json` | JSON Schema for workflow output (plan, gaps, paths) |
| `references/roles.json` | Role categories, transferable skills, and difficulty tiers |

### CLI Usage

```bash
# Gap analysis with target role
bash scripts/advisor.sh --profile '{"current_role":"Java后端","years":5,"skills":["Spring Boot","MySQL","Redis"],"target":"AI工程师","location":"上海"}'

# Exploration mode (no target specified)
bash scripts/advisor.sh --profile '{"current_role":"前端开发","years":3,"skills":["React","TypeScript"],"location":"北京"}'

# Interactive mode
bash scripts/advisor.sh --interactive

# JSON output for programmatic use
bash scripts/advisor.sh --profile '{"current_role":"Java后端","years":5,"target":"AI工程师","location":"上海"}' --output json
```

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `bash scripts/advisor.sh --profile '{"current_role":"Java后端","years":5,"location":"上海"}'` or `--interactive`
2. **Step 2**: Review the exploration menu and pick 1-2 target directions
3. **Step 3**: Run with `--target` to receive a detailed gap analysis and learning roadmap under 30 seconds

```bash
# Quick start
bash scripts/advisor.sh --profile '{"current_role":"Java后端","years":5,"target":"AI工程师","location":"上海"}'
```

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| User has <1 year experience | Switch to "entry-level" mode; focus on industry/market insights, not deep gap analysis |
| User has >15 years experience | Switch to "executive" mode; emphasize leadership, strategy, board roles over IC skills |
| Target role does not exist in market data | Flag as "emerging/niche role"; use adjacent role data + trend extrapolation |
| Salary expectations unrealistic (>90th percentile for experience) | Flag with market data; suggest negotiation tips or tier adjustment |
| User in non-tech field (e.g., finance, healthcare) | Adapt framework; scrape industry-specific job boards |
| Multiple simultaneous targets requested | Cap at 3; suggest sequential exploration |
| Location outside China | Use LinkedIn/Indeed for market data; adapt to local norms |
| User requests "guaranteed" outcome | Redirect: "Career planning increases probability, not certainty. Here's your best path forward." |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-MARKET-DATA-FAIL | Job boards inaccessible | Fall back to cached/general market knowledge; flag as "estimated" |
| E-TOO-VAGUE | Career profile too thin (<3 skills listed) | Ask probing questions; suggest self-assessment exercise |
| E-UNREALISTIC-TARGET | Target requires 10+ years of unaccounted experience | Flag politely; suggest bridge roles or longer timeline |
| E-OFFER-INCOMPLETE | Offer comparison missing key dimensions | Ask for missing info; note assumptions made |
| E-RAPID-CHANGE | Target field changing too fast (e.g., crypto 2025) | Warn of high uncertainty; suggest shorter planning cycles |
| E-REGION-MISMATCH | Salary benchmarks unavailable for small city | Use nearest Tier-1 city data with cost-of-living adjustment |

## Security Requirements

- **No identity storage**: Career profiles and skill data processed in-session only; not persisted across sessions
- **No PII collection**: Do not ask for real name, ID number, current employer name (use generic: "某大厂", "金融科技公司")
- **Market data attribution**: Cite data sources (e.g., "基于2026年6月BOSS直聘数据"). Note data freshness.
- **No guarantee of outcomes**: Always include disclaimer: career planning increases probability of success; it does NOT guarantee job offers, salary increases, or career satisfaction
- **Salary data privacy**: Salary benchmarks are aggregated anonymized market ranges, not individual data points
- **Avoid insider information**: Do not scrape or share non-public compensation data, internal promotion criteria, or proprietary company information