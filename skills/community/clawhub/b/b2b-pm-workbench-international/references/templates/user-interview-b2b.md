# B2B User Interview Guide

## Core Differences: B2B vs B2C Interviews

| Dimension | B2C | B2B |
|------|-----|-----|
| Interviewee | Single user | Multiple roles (Decision Maker/Admin/End User) |
| Interview Goal | Understand individual behavior | Understand organizational operations and decision chain |
| Key Questions | Do you like it? Would you use it? | What are your KPIs? How does the existing process run? |
| Decision Factors | Personal preference | Organizational needs + Process + Compliance + ROI |
| Interview Difficulty | Easy to schedule | Requires relationships/business support |

---

## I. Pre-Interview Preparation

### 1.1 Identify Interview Roles

| Role Type | Why Important | Interview Focus |
|---------|-----------|---------|
| **Decision Maker (Economic Buyer)** | Controls budget, final approval | ROI, total cost, risk, integration with existing systems |
| **Manager (Technical Buyer)** | Evaluates product capabilities and feasibility | Features, security, integration, scalability |
| **Core End User** | Daily usage, directly impacts renewal | Operational efficiency, ease of use, fit with existing workflows |
| **IT/System Administrator** | Responsible for deployment and maintenance | Deployment method, permission management, data security, operational complexity |
| **End Affected Users** | Data input/viewing | Is operation simple? Is data accurate? |

### 1.2 Information Pre-Collection

Before the interview, collect as much as possible:
- [ ] Client company basic info (industry/size/IT maturity)
- [ ] Client's existing IT systems and tool stack
- [ ] Client organizational structure (especially departments related to the product)
- [ ] Known pain points and demands (provided by sales/pre-sales)
- [ ] Client's competitor product usage (if known)

### 1.3 Interview Outline Template

```
【Interview Information】
Client: [Company Name]
Interviewee: [Name/Position/Role Type]
Interview Method: On-site/Video/Phone
Interview Duration: 45-60 minutes
Interviewer: [Name]

【Interview Goals】
[Core questions to clarify in this interview, no more than 3]

【Question Outline】
1. Icebreaker & Background (5min)
2. Existing Process & Pain Points (20min, CORE!)
3. Needs & Expectations (15min)
4. Decision & Procurement Process (10min)
5. Wrap-up & Next Steps (5min)
```

---

## II. B2B Interview Question Bank

### 2.1 For Decision Makers

```
Background:
- Please describe your scope of responsibilities. Which business metrics are you accountable for?
- Current team size? Any changes in the past year?

Current State & Pain Points:
- How does this business process currently run? What are the steps from start to finish?
- What are the three most painful problems for you?
- How much impact do these problems have on the business? (Quantify: time/money/risk)
- What solutions have you tried before? Why didn't they succeed?

Needs & Expectations:
- In an ideal scenario, what would the process look like?
- If this problem were perfectly solved, how would it impact your business metrics?
- How would you measure whether this investment is successful?

Decision-Related:
- If you decide to purchase, who participates in the decision? What is the decision process?
- Where does the budget come from? What is the approximate range?
- What other alternatives are you considering?
```

### 2.2 For Core End Users

```
Daily Work:
- Please describe what a typical day/week looks like for you.
- What proportion of your work does [product-related task] occupy?
- When you perform [a specific task], what are the specific steps? Please demonstrate for me.

Pain Point Deep Dive:
- When doing [a specific task], what wastes the most time?
- What is most prone to errors? What do you do when errors occur?
- Are there any tasks you want to complete but current tools cannot do?

Expectations & Concerns:
- If the new system goes live, what change are you most looking forward to?
- What worries you most? (Learning curve? Data migration? Process changes?)
- Have you switched systems before? How was that experience?
```

### 2.3 For IT/Administrators

```
System Current State:
- What core business systems are currently in place? How does data flow between them?
- How is identity authentication handled? SSO/LDAP?
- Any special requirements for data security?

Technical Requirements:
- Deployment preference? SaaS/On-premise/Hybrid cloud? Why?
- What are the system integration requirements? Which systems need to be connected?
- What are the hard requirements for system performance and security?
- What are the data compliance requirements?
```

---

## III. Interview Techniques

### 3.1 SPIN Framework (B2B Classic)

```
S - Situation Questions: Understand the existing process
   "What is the monthly reconciliation process like right now?"

P - Problem Questions: Uncover pain points
   "What is the most error-prone step in this process?"

I - Implication Questions: Amplify the consequences of pain points
   "If this problem occurs, what impact would it have on the audit?"

N - Need-Payoff Questions: Stimulate demand
   "If reconciliation were fully automated, how much time could your team free up for analysis?"
```

### 3.2 The 5 Whys

```
User: "I need a bulk import feature"
1st Why: Why do you need bulk import?
     "Because we need to import hundreds of records each time"
2nd Why: Why do you have so much data to import?
     "We export from the ERP system each month and then re-enter it"
3rd Why: Why export from ERP and re-enter? Why not integrate directly?
     "IT says integrating the two systems is too complex"
4th Why: Why is integration complex? Where exactly is it stuck?
     "The ERP is a 10-year-old legacy system with no API"
5th Why: Are there plans to upgrade the ERP?
     "There are plans for next year, but it's uncertain"
→ Conclusion: Short-term, bulk import is a reasonable transitional solution,
         but plan for future direct integration capability
```

### 3.3 Avoid These Pitfalls

```
❌ Don't ask: "What do you think of this feature?"
✅ Ask instead: "If in [specific scenario], you could [specific action], would that be helpful?"

❌ Don't ask: "What features do you need?"
✅ Ask instead: "In [scenario], what task do you most want to accomplish?"

❌ Don't ask: "Would you use this product?"
✅ Ask instead: "If this product disappeared tomorrow, how much would your work be affected?"

❌ Don't promise any features or go-live timelines
✅ Say instead: "We'll record this requirement and get back to you after internal evaluation"

❌ Don't let sales/account managers conduct interviews for you
✅ Conduct them personally — you'll find the information filtered by sales is completely different from the real information
```

---

## IV. Interview Record Template

### Single Interview Record

```markdown
【Customer Interview Record】

Interview ID: IV-[YYYYMMDD]-[Sequence]
Date: YYYY-MM-DD
Duration: [X] minutes
Client: [Company Name]
Interviewee: [Name] | [Position] | [Role Type: Decision Maker/End User/IT]
Interviewer: [Name]

## Key Findings (Top 3)
1. [Most important finding]
2.
3.

## Detailed Record

### Existing Process
[Business process described by the user, focusing on bottlenecks and manual steps]

### Core Pain Points
| Pain Point | Frequency | Impact | Current Workaround |
|------|------|------|------------|
| | Daily/Weekly/Monthly | Time/Amount/Risk | |

### Explicit Needs
| Need | Priority (User Perspective) | Willingness to Pay | Notes |
|------|-----------------|--------------|------|
| | High/Medium/Low | Yes/No/Uncertain | |

### Competitor Information
[Were any competitors mentioned? What was the user experience like?]

### Procurement Information
- Decision Chain: [Who participates in the procurement decision?]
- Budget Range: [Approximate budget]
- Timeline: [Expected procurement timeline]
- Alternatives: [What other options are still being considered?]

### Quotes (Verbatim)
> "[User's exact words, especially the insightful ones]"

## Follow-up Actions
| Item | Owner | Deadline |
|------|--------|---------|
| | | |

## Interview Assessment
- Information Quality: High/Medium/Low
- Follow-up Interview Needed: Yes/No
- Reason for Follow-up:
```

---

## V. Post-Interview Analysis & Outputs

### 5.1 Cross-Interview Pattern Recognition

Lay multiple interview records side by side and look for patterns:
- Which pain points appear most frequently?
- Which needs are mentioned by everyone?
- Which are specific to certain roles/industries?

### 5.2 Deliverables

1. **User Persona Cards** (one per role type)
2. **User Journey Map** (mark pain points at each stage)
3. **JTBD Cards** (Jobs To Be Done for each user type)
4. **Requirement Classification List** (classified by KANO model)

---

## VI. Special B2B User Interview Scenarios

### Scenario 1: On-Site Interview + Observation at Client Location
- Beyond asking, observe: the user's actual workstation, screen, and operations
- Note "workarounds": the "hacks" users employ to complete tasks in non-standard ways

### Scenario 2: Competitor Replacement Interview
- Clarify: Why are they leaving the existing product? What was the trigger?
- Migration cost: How to migrate data? How many people need training? How long is the downtime?
- Decision chain: Who pushed for the replacement? Where does resistance come from?

### Scenario 3: 0-to-1 Exploratory Interview
- First confirm the problem exists, then confirm it needs a product solution
- Beware of "polite demand": users saying "sounds good, I'd use it" out of politeness
- The ultimate question to verify real demand: "Would you pay for this?"


---

## v1.1.0 Added: JTBD Interview Framework

### JTBD Core Questions
| Question | Purpose | Example |
|------|------|------|
| "When was the last time you did [task]?" | Recall a specific scenario | "Last Friday afternoon, I was preparing the monthly report" |
| "What triggered you to do this?" | Identify trigger conditions | "The boss suddenly needed it for a meeting tomorrow" |
| "What tools/methods did you use?" | Understand existing solutions | "Exported Excel from 3 systems, manually merged" |
| "What was the most painful part of the process?" | Discover pain points | "Data didn't match, spent 2 hours reconciling" |
| "If this could be automated, how would your work change?" | Quantify value | "Save 4 hours per week, reports would be more timely" |

### JTBD Analysis Template
| Dimension | Content |
|------|------|
| Job Statement | When [situation], I want to [motivation], so that [expected outcome] |
| Functional Needs | Specific functions needed to complete the job |
| Emotional Needs | Emotional desires when completing the job (security/achievement/control) |
| Social Needs | Social recognition after completing the job (being recognized/respected) |
| Existing Solutions | How the job is currently done |
| Switching Barriers | Resistance to switching from existing solutions to new ones |