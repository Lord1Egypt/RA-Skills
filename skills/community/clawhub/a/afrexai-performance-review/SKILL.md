# Performance Review Engine

> Your AI-powered performance management system. Write reviews that develop people, not just evaluate them. From self-assessments to 360° feedback to calibration — complete frameworks for every review cycle.

---

## Quick Start

Tell your agent:
- "Write a performance review for [name] — they exceeded on delivery but need to improve communication"
- "Help me write my self-assessment for H2 2025"
- "Run a 360° feedback collection for my team of 6"
- "Prepare calibration notes for my 4 direct reports"

---

## 1. Review Cycle Setup

### Cycle Configuration Template

```yaml
cycle:
  name: "H2 2025 Performance Review"
  period: "2025-07-01 to 2025-12-31"
  type: annual | semi-annual | quarterly
  timeline:
    self_assessment_due: "2026-01-10"
    peer_feedback_due: "2026-01-17"
    manager_draft_due: "2026-01-24"
    calibration_session: "2026-01-28"
    delivery_window: "2026-01-29 to 2026-02-07"
  participants:
    - name: ""
      role: ""
      level: ""
      tenure_months: 0
      previous_rating: ""
      peer_reviewers: []
      skip_level_reviewer: ""
  rating_scale:
    1: "Does Not Meet Expectations"
    2: "Partially Meets Expectations"
    3: "Meets Expectations"
    4: "Exceeds Expectations"
    5: "Significantly Exceeds Expectations"
  competencies:
    - name: "Delivery & Execution"
      weight: 30
    - name: "Technical/Functional Expertise"
      weight: 25
    - name: "Communication & Collaboration"
      weight: 20
    - name: "Leadership & Influence"
      weight: 15
    - name: "Growth & Development"
      weight: 10
```

### Rating Distribution Guidelines

| Rating | Target % | Description |
|--------|----------|-------------|
| 5 - Significantly Exceeds | 5-10% | Transformational impact, raises the bar for everyone |
| 4 - Exceeds | 20-25% | Consistently above expectations, visible impact |
| 3 - Meets | 50-60% | Solid, reliable performer at level |
| 2 - Partially Meets | 10-15% | Gaps in key areas, needs focused improvement |
| 1 - Does Not Meet | 0-5% | Serious performance concerns, PIP candidate |

**Forced distribution warning:** These are guidelines, not quotas. If a team genuinely has 80% high performers, the distribution should reflect reality. Forcing bell curves creates distrust.

---

## 2. Self-Assessment Framework

### STAR-I Method (Situation → Task → Action → Result → Impact)

Guide employees to write self-assessments that actually demonstrate value:

```markdown
### Achievement: [Title]

**Situation:** What was the context or challenge?
**Task:** What was your specific responsibility?
**Action:** What did you do? (Be specific — tools, approaches, decisions)
**Result:** What was the measurable outcome?
**Impact:** How did this affect the team/org/company beyond the immediate result?

**Competency alignment:** [Which competency does this demonstrate?]
**Evidence:** [Links, metrics, Slack messages, PRs, customer feedback]
```

### Self-Assessment Prompts by Competency

**Delivery & Execution:**
- What were your top 3-5 deliverables this period?
- Which projects were on time/budget? Which weren't, and why?
- How did you handle blockers or scope changes?
- What did you ship that you're most proud of?

**Technical/Functional Expertise:**
- What new skills or knowledge did you develop?
- Where did you serve as the go-to expert?
- What technical decisions did you make and what was the outcome?
- How did you stay current in your field?

**Communication & Collaboration:**
- How did you contribute to team effectiveness?
- Give an example of resolving a disagreement productively
- How did you share knowledge with others?
- What cross-functional work did you do?

**Leadership & Influence:**
- How did you influence outcomes beyond your direct responsibilities?
- Did you mentor or develop others? How?
- What initiatives did you drive or champion?
- How did you contribute to team culture?

**Growth & Development:**
- What feedback did you receive and act on?
- What's your biggest area of growth this period?
- Where do you still want to improve?
- What are your goals for next period?

### Self-Assessment Quality Checklist

- [ ] Includes 5-8 concrete achievements with metrics
- [ ] Uses STAR-I format (not just "I did X")
- [ ] Covers all competency areas, not just delivery
- [ ] Acknowledges at least 1-2 growth areas honestly
- [ ] References specific feedback received and actions taken
- [ ] Includes forward-looking goals
- [ ] Avoids vague language ("helped with," "was involved in")
- [ ] Links to evidence where possible
- [ ] Appropriate length (1-2 pages, not 10)
- [ ] Written in first person, professional but human tone

---

## 3. Manager Review Writing

### The OBSERVE Framework

Structure every review around:

**O — Outcomes delivered:** What did they ship/achieve? Metrics and evidence.
**B — Behaviors demonstrated:** HOW they worked, not just what they produced.
**S — Strengths to leverage:** Their superpower — what should they do MORE of?
**E — Edges to develop:** Growth areas framed as opportunities, not failures.
**R — Relationships & impact:** How they affected team dynamics and culture.
**V — Vision forward:** Clear expectations and development plan for next period.
**E — Evidence cited:** Every claim backed by specific examples.

### Writing Rules

1. **Specific > Vague**
   - ❌ "Great job this quarter"
   - ✅ "Led the API migration affecting 12 services, completing 2 weeks ahead of schedule with zero customer-facing incidents"

2. **Behavior > Trait**
   - ❌ "Is a natural leader"
   - ✅ "Organized weekly knowledge-sharing sessions that improved team velocity by 15% and reduced onboarding time for 3 new hires"

3. **Pattern > Incident**
   - ❌ "Missed the Q3 deadline"
   - ✅ "Delivery timelines were missed on 3 of 5 projects, consistently by 1-2 weeks, suggesting estimation needs improvement"

4. **Forward > Backward**
   - ❌ "Failed to communicate effectively"
   - ✅ "Strengthening stakeholder communication — specifically proactive status updates — would multiply the impact of their strong technical work"

5. **Balanced always**
   - Even top performers need development feedback
   - Even struggling performers have strengths to acknowledge
   - Target ratio: 60% strengths / 40% development (adjust by rating)

### Review Templates by Rating

#### Rating 5 — Significantly Exceeds

```markdown
## Performance Review: [Name] — H2 2025
**Rating: Significantly Exceeds Expectations (5/5)**

### Summary
[Name] delivered exceptional results this period, consistently operating above their current level. Their impact extended well beyond their role, influencing [team/org/company] outcomes in measurable ways.

### Key Achievements
1. **[Achievement]** — [STAR-I summary with metrics]
2. **[Achievement]** — [STAR-I summary with metrics]
3. **[Achievement]** — [STAR-I summary with metrics]

### Competency Assessment
| Competency | Rating | Evidence |
|-----------|--------|----------|
| Delivery & Execution | 5 | [Specific examples] |
| Technical Expertise | [X] | [Specific examples] |
| Communication | [X] | [Specific examples] |
| Leadership | [X] | [Specific examples] |
| Growth | [X] | [Specific examples] |

### Strengths to Leverage
- [Strength 1] — this is a differentiator that should be amplified
- [Strength 2] — consider giving them a platform to share this more broadly

### Development Opportunities
Even at this exceptional level, continued growth in [area] would unlock [next-level impact]. Specifically:
- [Development area with actionable suggestion]
- [Stretch assignment or learning recommendation]

### Forward Look
[Name] is ready for [promotion/expanded scope/leadership opportunity]. Recommended next steps: [specific action].
```

#### Rating 3 — Meets Expectations

```markdown
## Performance Review: [Name] — H2 2025
**Rating: Meets Expectations (3/5)**

### Summary
[Name] delivered solid, reliable work this period, meeting the expectations of their role. They are a dependable contributor who [key positive theme].

### Key Achievements
1. **[Achievement]** — [Evidence]
2. **[Achievement]** — [Evidence]
3. **[Achievement]** — [Evidence]

### Competency Assessment
[Same table format]

### Strengths
- [Strength 1 with evidence]
- [Strength 2 with evidence]

### Development Areas
To move from "meets" to "exceeds," [Name] should focus on:
1. **[Area]** — Currently [current state]. The gap is [specific gap]. To close it: [actionable steps].
2. **[Area]** — [Same structure]

### Forward Look
Goals for next period:
1. [Measurable goal tied to development area]
2. [Stretch goal that would demonstrate growth]
3. [Continuation goal building on strengths]
```

#### Rating 1-2 — Below Expectations

```markdown
## Performance Review: [Name] — H2 2025
**Rating: [Partially Meets / Does Not Meet] Expectations ([1-2]/5)**

### Summary
[Name] struggled to meet expectations in key areas this period. While [acknowledge any positives], significant gaps in [areas] need to be addressed.

### Performance Gaps
1. **[Gap]** — Expected: [what was expected]. Actual: [what happened]. Impact: [business impact]. Examples: [2-3 specific instances].
2. **[Gap]** — [Same structure]

### What Was Done Well
- [Genuine positive — never skip this section]

### Context Considered
- [Any mitigating factors: reorg, unclear expectations, personal circumstances]
- [Whether support/coaching was provided and when]

### Improvement Plan
| Area | Current State | Target State | Actions | Timeline | Support Needed |
|------|--------------|-------------|---------|----------|----------------|
| [Gap 1] | [Specific] | [Specific] | [Steps] | [Date] | [Resources] |
| [Gap 2] | [Specific] | [Specific] | [Steps] | [Date] | [Resources] |

### Consequences
If improvement to [specific measurable standard] is not demonstrated by [date]:
- [Next step: PIP / role change / separation]

### Check-in Schedule
- Weekly 1:1s focused on [areas]
- 30-day checkpoint: [date]
- 60-day checkpoint: [date]
- Final assessment: [date]
```

---

## 4. 360° Feedback System

### Peer Feedback Request Template

```markdown
Hi [Peer Name],

You're invited to provide feedback on [Employee Name] for our [H2 2025] review cycle.

Please share your observations (10-15 min, ~200-400 words total):

1. **What does [Name] do well?** (Think: specific projects, behaviors, impact on you/the team)
2. **What could [Name] improve?** (Think: what would make them even more effective?)
3. **How would you describe working with [Name]?** (Collaboration style, communication, reliability)
4. **One thing [Name] should keep doing:** ___
5. **One thing [Name] should start or do more of:** ___

Your feedback will be anonymized and synthesized — [Name] will not see your individual responses verbatim.

Due by: [Date]
```

### Feedback Synthesis Method

When combining multiple peer reviews:

1. **Identify themes** — What do 2+ people mention? Those are patterns, not noise.
2. **Weight by proximity** — Feedback from close collaborators > occasional contacts.
3. **Separate fact from feeling** — "Missed 3 deadlines" is fact. "Seems disengaged" is perception (still valuable, but frame differently).
4. **Preserve outlier insights** — If one person noticed something unique, it may still be valuable. Include as "additionally noted."

### Synthesis Template

```markdown
### 360° Feedback Summary for [Name]

**Respondents:** [N] peers, [N] cross-functional, [N] skip-level

**Consistent Strengths (mentioned by 2+ reviewers):**
- [Theme] — "[Representative quote]" (paraphrased from [N] responses)
- [Theme] — "[Representative quote]"

**Consistent Development Areas:**
- [Theme] — "[Representative quote]"
- [Theme] — "[Representative quote]"

**Notable Individual Observations:**
- [Unique insight worth including]

**Overall Sentiment:** [Positive / Mixed / Concerning]
**Collaboration Rating (aggregated):** [Strong / Solid / Needs Improvement]
```

---

## 5. Calibration Session

### Pre-Calibration Prep

For each direct report, prepare:

```yaml
calibration_card:
  name: ""
  current_level: ""
  tenure: ""
  previous_rating: ""
  proposed_rating: ""
  rating_justification: "" # 2-3 sentences max
  top_achievement: ""
  biggest_gap: ""
  promotion_candidate: yes | no | not_yet
  flight_risk: low | medium | high
  key_question: "" # What you want the calibration group to weigh in on
```

### Calibration Discussion Framework

**Round 1 — Present (2 min per person)**
- Manager presents: proposed rating, top achievement, biggest gap
- No debate yet — just laying out the landscape

**Round 2 — Calibrate (5 min per person where needed)**
- Focus on: rating 4s and 5s (are they truly exceptional?), rating 1s and 2s (is this fair?), any rating that changed from last cycle
- Ask: "Would this person get the same rating on another team?"
- Ask: "Is this rating consistent with [comparable person]?"

**Round 3 — Decide**
- Finalize ratings
- Flag anyone who needs skip-level review
- Identify promotion candidates
- Identify flight risks needing retention action

### Calibration Bias Checklist

Before finalizing, check for:
- [ ] **Recency bias** — Are you over-weighting the last month vs. the full period?
- [ ] **Halo/horns effect** — Is one great/bad thing coloring the entire review?
- [ ] **Similarity bias** — Are you rating people like you higher?
- [ ] **Central tendency** — Are you avoiding extreme ratings when they're warranted?
- [ ] **Leniency/strictness** — Is your distribution shifted vs. the org?
- [ ] **Attribution error** — Are you blaming the person for systemic issues?
- [ ] **Contrast effect** — Are you comparing to the previous person reviewed rather than the standard?

---

## 6. Review Delivery Conversation

### Conversation Structure (45-60 min)

**Opening (5 min)**
- Set the tone: "This is a two-way conversation, not a verdict"
- Share the rating upfront — don't make them wait

**Achievements (10 min)**
- Walk through top 3-5 achievements
- Let them add context or achievements you missed
- Be genuinely appreciative — this isn't just preamble to criticism

**Development (15 min)**
- Present 1-2 development areas (not 10)
- Use the pattern: "I've observed [specific behavior] in [specific situations]. The impact was [what happened]. What I'd love to see is [desired behavior]."
- Ask: "Does this resonate? What's your perspective?"
- Listen. Actually listen.

**360° Themes (5 min)**
- Share synthesized peer feedback
- Highlight: "Your colleagues really value [X]"
- Development: "A theme that came up was [Y] — thoughts?"

**Goals & Development Plan (15 min)**
- Co-create 3-5 goals for next period
- At least 1 development goal, not just delivery goals
- Identify specific actions, resources, support needed
- Agree on check-in cadence

**Close (5 min)**
- Summarize key takeaways
- Ask: "What do you need from me to be successful?"
- End on forward-looking, supportive note

### Difficult Conversation Scripts

**For underperformers:**
"I want to be direct with you because I respect you and your potential here. Your performance this period was below what we need in [specific area]. Here's what I've observed... I want to work with you on a plan to get back on track. Are you willing to commit to that?"

**For strong performers who didn't get promoted:**
"Your work this period was excellent — [specific examples]. The reason you're rated [X] rather than promoted is [specific gap]. Here's what I think it would take: [concrete steps]. I'm committed to supporting you in getting there."

**For someone who disagrees with their rating:**
"I hear you, and I want to understand your perspective. Can you walk me through the specific areas where you see it differently? ... I appreciate you sharing that. Here's how I weighed [factors]. [Either: Let me take this back and reconsider / I understand the disagreement, but here's why the rating stands]."

---

## 7. Development Planning

### Development Plan Template

```yaml
development_plan:
  employee: ""
  manager: ""
  period: "H1 2026"
  review_date: ""
  
  strengths_to_leverage:
    - strength: ""
      leverage_action: "" # How to use this more
      
  development_areas:
    - area: ""
      current_state: ""
      target_state: ""
      actions:
        - type: "on_the_job" # 70% of development
          description: ""
          timeline: ""
        - type: "learning" # 20% — coaching, mentoring, peer learning
          description: ""
          timeline: ""
        - type: "formal" # 10% — courses, certifications, conferences
          description: ""
          timeline: ""
      success_metrics: ""
      check_in_dates: []
      
  career_goals:
    short_term: "" # 6-12 months
    medium_term: "" # 1-3 years
    long_term: "" # 3-5 years
    
  support_needed:
    from_manager: ""
    from_org: ""
    budget_required: ""
```

### The 70-20-10 Development Mix

| Type | % | Examples |
|------|---|----------|
| On-the-job | 70% | Stretch assignments, new projects, leading initiatives, cross-functional work, shadowing |
| Social learning | 20% | Mentoring, coaching, peer feedback, communities of practice, teaching others |
| Formal learning | 10% | Courses, certifications, conferences, books, structured programs |

**Common mistake:** Over-indexing on formal learning (sending someone to a course) when on-the-job stretch would be 5x more effective.

---

## 8. Continuous Feedback (Between Reviews)

### 1:1 Performance Check-in Template (Monthly)

```markdown
## Monthly Check-in: [Name] — [Month Year]

### Progress on Goals
| Goal | Status | Notes |
|------|--------|-------|
| [Goal 1] | 🟢 On track / 🟡 At risk / 🔴 Off track | [Brief update] |

### Recent Wins
- [What went well this month]

### Challenges
- [What's been difficult]

### Feedback Exchange
- **Manager → Employee:** [One specific piece of feedback]
- **Employee → Manager:** [Ask: "What can I do differently to support you?"]

### Action Items
- [ ] [Action] — Owner: [who] — By: [date]

### Overall Pulse: 😊 Great / 😐 Fine / 😟 Struggling
```

### Real-Time Feedback Formula (SBI)

**Situation:** "In yesterday's client presentation..."
**Behavior:** "...you handled the pricing objection by reframing around ROI rather than discounting..."
**Impact:** "...which kept us at full price and the client visibly shifted from skeptical to interested."

Deliver within 48 hours. Positive feedback publicly (if they're comfortable). Constructive feedback privately. Always.

---

## 9. Scoring & Analytics

### Individual Performance Score (0-100)

```
Score = Σ (competency_rating × competency_weight) × 20

Example:
Delivery (4/5 × 30%) + Technical (3/5 × 25%) + Communication (4/5 × 20%) 
+ Leadership (3/5 × 15%) + Growth (4/5 × 10%)
= (1.20 + 0.75 + 0.80 + 0.45 + 0.40) = 3.60 / 5 = 72/100
```

### Team Health Dashboard

Track quarterly:

```markdown
## Team Performance Dashboard — Q4 2025

**Team size:** [N]
**Rating distribution:** ⭐5: [N] | ⭐4: [N] | ⭐3: [N] | ⭐2: [N] | ⭐1: [N]
**Average score:** [X]/100
**vs. last period:** [↑/↓ X points]

**Promotion candidates:** [Names]
**Flight risks:** [Names + risk level]
**PIP/coaching:** [Names]

**Top team strengths:** [Competencies scoring highest]
**Team gaps:** [Competencies scoring lowest]
**Development budget used:** [X]% of [Y] allocated

**Engagement signals:**
- Voluntary turnover: [X]%
- Internal mobility: [X] transfers/promotions
- 1:1 completion rate: [X]%
- Goal completion rate: [X]%
```

---

## 10. Edge Cases & Advanced Scenarios

### New Hire (< 6 months)
- Evaluate against onboarding milestones, not full role expectations
- Weight learning speed and cultural integration higher
- Compare to "expected ramp" not to tenured peers
- Rating floor of 3 unless genuine performance issues (distinguish slow ramp from bad fit)

### Role Change Mid-Cycle
- Split the review: first half in old role, second half in new
- Weight the new role performance more heavily (it's the forward-looking signal)
- Acknowledge the transition tax — expect a temporary dip

### Remote/Hybrid Considerations
- Evaluate output and impact, not visibility or hours
- Seek feedback from async collaborators, not just people in the office
- Watch for proximity bias — don't rate in-office people higher by default

### High Performer Wanting to Leave
- Have the conversation: "I value you and want to understand what would make you want to stay"
- Don't inflate the rating as retention — it sets a precedent
- Document the conversation and retention actions taken

### Inherited Team Member
- Get context from previous manager (ask for their calibration card)
- Be transparent: "I'm still building my understanding of your work"
- Lean more on peer feedback and objective metrics
- Don't default to "meets" because you don't know — do the research

### Manager Reviewing Someone They Don't Like
- Stick to observable behaviors and measurable outcomes
- Have a peer manager gut-check your review for bias
- Ask yourself: "If my favorite team member did exactly this, what would I rate them?"

---

## 11. Legal & Compliance Notes

**Documentation rules:**
- Keep all review documents for minimum 3 years (7 in regulated industries)
- Feedback must reference specific, observable behaviors — not personality traits
- Never reference protected characteristics (age, gender, disability, etc.)
- PIP documentation should be reviewed by HR/legal before delivery
- Employee should sign acknowledging receipt (not agreement)

**Phrases to avoid:**
- "Cultural fit" (can mask bias) → Use "collaboration effectiveness"
- "Aggressive" (gendered connotation) → Use "assertive" or "direct"
- "Young/energetic" → Use specific behaviors
- "Not a team player" → Cite specific collaboration gaps with examples

---

## Commands Reference

| Command | What it does |
|---------|-------------|
| "Start review cycle for [team]" | Creates cycle config with timeline |
| "Write self-assessment for [achievements]" | Generates STAR-I formatted self-review |
| "Write review for [name] — rating [X]" | Full manager review using OBSERVE framework |
| "Collect 360 feedback for [name]" | Generates peer feedback requests |
| "Synthesize feedback from [sources]" | Combines multiple inputs into themes |
| "Prepare calibration for [team]" | Creates calibration cards for all reports |
| "Create development plan for [name]" | Builds 70-20-10 development plan |
| "Monthly check-in for [name]" | Generates 1:1 template with goal tracking |
| "Give feedback on [situation]" | Formats using SBI framework |
| "Score [name] across competencies" | Calculates weighted performance score |
| "Team health dashboard" | Generates full team analytics view |
