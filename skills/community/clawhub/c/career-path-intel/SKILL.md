---
name: Career Path & Education Intelligence
slug: career-path-intel
description: >
  AI-powered career development and education planning intelligence. Tracks job market shifts (BLS/LinkedIn/Burning Glass),
  emerging roles (7 career domains: AI, climate, cybersecurity, biotech, software, marketing, remote),
  salary benchmarks (Glassdoor/Levels.fyi), education ROI (bootcamps vs. degrees vs. certs),
  career transition roadmaps (6 validated pathways), and lifelong learning plans. Integrates 12 data sources
  covering 800+ occupations, salary data, university rankings, and real-time job posting analytics.
  Delivers personalized career plans, skills gap analysis, and education investment frameworks.
triggers:
  - "career change plan"
  - "job market trends"
  - "salary benchmark"
  - "skills gap analysis"
  - "education ROI"
  - "career transition"
  - "university ranking comparison"
  - "certification path"
  - "remote job opportunities"
  - "future of work"
  - "AI impact on jobs"
  - "career coaching"
  - "learning roadmap"
  - "professional development"
author: Marvis
version: "1.0"
metadata:
  emoji: "🎓"
  requires: "references/career_sources.json"
---

# Career Path & Education Intelligence

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | Job Market Trend Analysis | Role / industry / region | Hiring growth rate, salary trajectory, top employers, remote availability, geographic hotspots |
| 2 | Career Transition Roadmap | Current role → target role | Skills gap analysis, timeline, learning resources, portfolio projects, networking strategy, first-role expectations |
| 3 | Salary Benchmarking | Role + location + experience | Compensation bands (10th/50th/90th percentile), equity expectations, negotiation leverage points, total comp breakdown |
| 4 | Education Investment ROI | Education option (degree/bootcamp/cert) × career path | Total cost, opportunity cost, expected salary uplift, payback period, risk assessment |
| 5 | Skills Gap Analyzer | Target role + current skills inventory | Missing skills ranked by importance/difficulty, learning resources (courses/books/projects), proficiency benchmark |
| 6 | Emerging Career Radar | Domain (AI, climate, etc) | New job titles, required skills, entry pathways, growth projection, pioneer companies hiring |
| 7 | University & Program Comparator | Field + region + budget | Ranking, program specifics, placement rates, alumni salary, ROI, application difficulty |
| 8 | Certification Pathway Advisor | Field (cloud, security, PM, etc) | Certification hierarchy (entry → advanced), cost, study time, exam difficulty, employer demand, salary premium |
| 9 | Personal Brand Builder | Career stage + goals | LinkedIn profile optimization, portfolio strategy, content plan, networking outreach templates |
| 10 | Lifelong Learning Planner | Career goals + 5-year horizon | Skill acquisition timeline, learning format mix (courses/micro-credentials/projects/peer learning), renewal schedule |

## Workflow

```
User Query
  │
  ├─ [Step 1] Classify → career stage (student / early career / mid-career / executive) + domain + geography
  │
  ├─ [Step 2] Multi-source intelligence:
  │   └─ Labor market: BLS OOH, LinkedIn Workforce, Burning Glass/Lightcast, Indeed Hiring Lab
  │   └─ Compensation: Glassdoor, Levels.fyi
  │   └─ Education: QS/THE rankings, Coursera/edX course data, certification bodies
  │   └─ Trends: WEF Future of Jobs, O*NET skills evolution
  │
  ├─ [Step 3] Gap analysis: current vs. target skills matrix
  │
  ├─ [Step 4] Pathway generation with timeline, cost, and success probability
  │
  ├─ [Step 5] Output personalized plan with actionable steps
  │
  └─ [Step 6] ROI calculation: investment vs. expected salary uplift over 3-5 years
```

## Output Formats

### Career Transition Roadmap
| Phase | Timeline | Focus | Key Activities | Resources | Cost |
|-------|----------|-------|---------------|-----------|------|
| 1: Foundation | Months 1-2 | Core skills | [Courses, certifications] | [Links, providers] | $X |
| 2: Practice | Months 3-4 | Portfolio projects | [Project ideas, hackathons] | [GitHub, Kaggle] | $X |
| 3: Network | Months 5-6 | Industry connections | [Conferences, meetups, cold outreach] | [LinkedIn, Luma] | $X |
| 4: Apply | Month 7+ | Job search | [Resume, interviews, negotiation] | [Platforms, prep tools] | $0 |
| **Total** | **7 months** | | | | **$X total** |

### Salary Benchmark Table
| Percentile | Base Salary | Bonus | Equity (annual) | Total Comp | Notes |
|-----------|------------|-------|-----------------|------------|-------|
| 10th (Entry) | $XX,XXX | $X,XXX | $X,XXX | $XX,XXX | New grad / bootcamp |
| 50th (Mid) | $XX,XXX | $X,XXX | $XX,XXX | $XX,XXX | 3-5 years experience |
| 90th (Senior) | $XX,XXX | $X,XXX | $XX,XXX | $XX,XXX | Staff/Principal level |

### Education ROI Calculator
| Option | Duration | Total Cost | Opportunity Cost | Expected Salary Post | Payback Period | 5Y Net Gain |
|--------|----------|------------|-----------------|---------------------|----------------|-------------|
| Bootcamp | 4 months | $15,000 | $25,000 (no work) | $95,000 | 10 months | $315,000 |
| Master's | 2 years | $60,000 | $120,000 (no work) | $120,000 | 3 years | $190,000 |
| Self-Study | 8 months | $500 | $0 (keep job) | $95,000 | $0 | $375,000 |

## Usage Guidelines

1. **Data recency** — labor market data shifts rapidly; flag salary/job data >6 months old
2. **Location matters** — always normalize salaries for cost of living; NYC $150K ≠ Austin $150K
3. **No one-size-fits-all** — present multiple pathways; self-study / bootcamp / degree each have different risk-reward profiles
4. **AI impact assessment** — explicitly note automation risk and AI-augmentation opportunity for each role
5. **Motivational but honest** — celebrate achievable goals while being clear about competitive realities
6. **Global perspective** — support career planning across US, UK, EU, CN, IN, SG, AU, JP

## Examples

### Example 1: Career Transition
**User**: "I'm a high school teacher making $55K. Can I transition to instructional design?"
**Output**: Skills overlap analysis (curriculum design → instructional design mapping), 6-month transition plan with cost ($3K for certs), expected salary ($75K-$95K), remote work probability (high), portfolio project ideas.

### Example 2: AI Career Advice
**User**: "Which career is more future-proof: cybersecurity or data science?"
**Output**: Growth rate comparison (both >30%), AI augmentation vs. replacement risk for each, salary trajectories, barrier-to-entry analysis, personality-fit guide, 10-year outlook with automation risk assessment.

### Example 3: Salary Negotiation
**User**: "I got an offer for Senior Product Manager at a Series C startup in Berlin. Is €90K + 0.3% equity fair?"
**Output**: Berlin PM comp benchmarks (€75K-€120K base), equity value modeling (with exit scenarios), cost-of-living comparison (vs. London/SF), negotiation script, total comp vs. FAANG alternative.

---

**Data Base**: `references/career_sources.json` — 12 authoritative data sources, 7 career domains, 5 education pathways, 6 career transition matrices.
**Last Updated**: June 2026
**Free Tier**: Available. This skill aggregates public labor market data; no proprietary headhunter data accessed.
