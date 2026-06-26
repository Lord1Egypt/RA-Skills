# Customer Onboarding Optimizer

Structured framework for designing, auditing, and optimizing B2B customer onboarding flows. Reduces time-to-value, increases activation rates, and prevents early churn.

## When to Use
- Designing onboarding for a new product or feature
- Auditing why activation rates are low
- Reducing time-to-first-value below industry benchmarks
- Building onboarding automation with agents

## Framework

### 1. Onboarding Health Score (0-100)

Score each dimension:

| Dimension | Weight | What to Measure |
|-----------|--------|----------------|
| Time-to-first-value | 25% | Days from signup to first meaningful outcome |
| Activation rate | 20% | % of signups completing core action within 7 days |
| Setup completion | 15% | % completing all onboarding steps |
| Support ticket rate | 15% | Tickets per new user in first 30 days (lower = better) |
| Day-30 retention | 15% | % still active at day 30 |
| NPS at day 14 | 10% | Net Promoter Score from onboarding survey |

**Scoring:**
- 80-100: Elite (top 10% of B2B SaaS)
- 60-79: Competitive
- 40-59: Leaking revenue — fix within 30 days
- Below 40: Emergency — onboarding is killing growth

### 2026 Benchmarks (B2B SaaS):
- Median time-to-first-value: 4.2 days
- Top quartile activation rate: 68%
- Median Day-30 retention: 72%
- Support tickets per new user (first 30 days): 2.1

### 2. Onboarding Stage Map

Design onboarding in 5 stages:

**Stage 1: Welcome (Minutes 0-5)**
- Personalized welcome based on signup data
- Set expectations: what they will accomplish today
- Single clear CTA — not a tour, not a video, an ACTION

**Stage 2: Quick Win (Minutes 5-30)**
- Guide user to ONE meaningful outcome
- Pre-populate with sample data if possible
- Celebrate completion (dopamine hit matters)

**Stage 3: Core Setup (Days 1-3)**
- Integrations, team invites, data import
- Progress bar showing completion %
- Automated nudges for incomplete steps (email + in-app)

**Stage 4: Habit Formation (Days 3-14)**
- Daily/weekly triggers tied to their workflow
- Show value metrics ("You saved 3.2 hours this week")
- Introduce advanced features gradually

**Stage 5: Expansion (Days 14-30)**
- Cross-sell / upsell based on usage patterns
- Team expansion prompts
- Success milestone celebration + case study request

### 3. Onboarding Automation Map

| Task | Automate? | Agent Capability |
|------|-----------|-----------------|
| Welcome email sequence | Yes — fully | Personalized based on company size, industry, role |
| Account setup checklist | Yes — fully | Track completion, send reminders |
| Integration assistance | Partial | Agent handles common integrations, escalate edge cases |
| Data migration | Partial | Agent runs migration scripts, human validates |
| Training / walkthrough | Yes — fully | Interactive agent-guided tours |
| Check-in calls | Partial | Agent schedules, human conducts for enterprise |
| Health score monitoring | Yes — fully | Daily scoring, alert on drops |

### 4. Churn Risk Signals (First 30 Days)

Flag immediately if:
- [ ] No login within 48 hours of signup
- [ ] Setup incomplete after 5 days
- [ ] Zero core actions in first 7 days
- [ ] Support ticket within first 24 hours (bad UX signal)
- [ ] Team invite sent but not accepted after 3 days
- [ ] Usage declining week-over-week in first month
- [ ] NPS response below 6

### 5. Onboarding Cost Framework

| Company Stage | Monthly New Users | Onboarding Cost/User | Automation Target |
|--------------|-------------------|---------------------|-------------------|
| Early (0-100 users) | 10-30 | $150-$300 (high-touch) | 40% automated |
| Growth (100-1K) | 50-200 | $50-$150 (guided) | 70% automated |
| Scale (1K-10K) | 200-2K | $15-$50 (self-serve + agent) | 90% automated |
| Enterprise (10K+) | 1K+ | $5-$20 (fully automated) | 95% automated |

### 6. Email Sequence Template

**Day 0:** Welcome + quick win CTA
**Day 1:** "Did you try [core feature]?" + 1-click deep link
**Day 3:** Setup completion reminder (if incomplete)
**Day 5:** Value proof ("Companies like yours saved $X")
**Day 7:** Feature spotlight (based on usage)
**Day 14:** NPS survey + expansion offer
**Day 21:** Case study request (if active) OR re-engagement (if inactive)
**Day 30:** Renewal/upgrade prompt + ROI summary

### 7. Industry Adjustments

| Industry | Key Onboarding Challenge | Recommended Focus |
|----------|------------------------|-------------------|
| SaaS | Feature overload | Single quick win, progressive disclosure |
| Fintech | Compliance requirements | KYC/AML flow optimization, parallel processing |
| Healthcare | Integration complexity | Pre-built EHR connectors, dedicated migration support |
| Legal | Data sensitivity | Security walkthrough first, then value demo |
| E-commerce | Time pressure | Same-day value delivery, pre-configured templates |
| Construction | Low tech literacy | Mobile-first, video tutorials, phone support option |
| Real Estate | Seasonal urgency | Fast setup for listing season, batch import |
| Recruitment | Data migration volume | Bulk candidate import, ATS integration priority |
| Manufacturing | Multi-stakeholder | Role-based onboarding paths, champion enablement |
| Professional Services | Customization needs | Template library, white-label setup |

## Output Format

Deliver results as:
1. Onboarding Health Score (current state)
2. Stage-by-stage gap analysis
3. Top 3 quick fixes (implement this week)
4. 30-day optimization roadmap
5. Automation opportunities with ROI estimates

## Resources

- [AI Revenue Leak Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/) — Find where onboarding waste hides
- [Industry Context Packs](https://afrexai-cto.github.io/context-packs/) — $47 each, 10 industries
- [Agent Setup Wizard](https://afrexai-cto.github.io/agent-setup/) — Deploy your onboarding agent in 5 minutes
- Bundles: Pick 3 ($97) | All 10 ($197) | Everything ($247)
