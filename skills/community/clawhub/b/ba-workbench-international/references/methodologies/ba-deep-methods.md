# Business Analysis Deep Methodology Library

> A collection of 50+ top-tier business analysis methodologies, from strategy to execution, from quantitative to qualitative, from MBB to Chinese enterprises.

---

## Methodology Index

| No. | Methodology | Domain | Source | Difficulty |
|------|--------|------|------|------|
| M-01 | MECE Principle | Structured Thinking | McKinsey | Beginner |
| M-02 | Pyramid Principle | Communication & Reporting | McKinsey | Beginner |
| M-03 | Porter's Five Forces + Complements | Industry Analysis | Porter | Intermediate |
| M-04 | VRIO Capability Analysis | Internal Capabilities | Barney | Intermediate |
| M-05 | BCG Growth-Share Matrix | Product Portfolio | BCG | Intermediate |
| M-06 | GE-McKinsey Matrix | Business Portfolio | McKinsey+GE | Intermediate |
| M-07 | Ansoff Growth Matrix | Growth Strategy | Ansoff | Beginner |
| M-08 | Blue Ocean Strategy ERRC | Differentiation & Innovation | Kim & Mauborgne | Intermediate |
| M-09 | JTBD Methodology | Needs Discovery | Christensen | Intermediate |
| M-10 | Unit Economics | Business Model | General | Beginner |
| M-11 | FMEA Failure Mode Analysis | Risk Management | General | Advanced |
| M-12 | Decision Tree Analysis | Decision Science | General | Intermediate |
| M-13 | SIPOC Process Analysis | Process Management | Six Sigma | Beginner |
| M-14 | Kotter's 8-Step Change Model | Change Management | Kotter | Intermediate |
| M-15 | MoSCoW Prioritization | Requirements Prioritization | DSDM | Beginner |
| M-16 | Kano Model | Requirements Classification & Satisfaction | Noriaki Kano | Beginner |
| M-17 | BDD Behavior-Driven Development | Requirements Engineering | Dan North | Intermediate |
| M-18 | EventStorming | Domain Modeling | Alberto Brandolini | Intermediate |
| M-19 | BABOK Agile Extension | Agile BA | IIBA | Intermediate |

---

## M-01: MECE Principle

### Source: McKinsey & Company

### Core Concepts
```
MECE = Mutually Exclusive + Collectively Exhaustive

Purpose: Ensure the analysis structure has no overlaps and no omissions
Application Scenarios: Any classification, grouping, or analysis framework design
```

### Common MECE Grouping Methods

| Grouping Logic | Example | Applicable Scenario |
|---------|------|---------|
| Chronological Order | Past → Present → Future / Plan → Do → Check → Act | Process Analysis |
| Structural Order | By Department/Region/Product Line | Organizational Analysis |
| Degree Order | Most Important → Least Important | Priority Ranking |
| Mathematical Formula | Profit = Revenue - Cost / Revenue = Volume × Price | Quantitative Analysis |
| Dichotomy | Internal/External, Online/Offline | General Classification |

### MECE Validation

```
Examples of non-MECE situations:
❌ New Customers + Existing Customers + Major Customers (Major customers may be both new/existing → not mutually exclusive)
✅ By Time: New Customers + Existing Customers (by first purchase time, <1 year = new)
✅ By Amount: Annual spend >1M customers + Annual spend ≤1M customers

❌ Revenue Sources: Products + Services + Software (may overlap)
✅ By Revenue Recognition Method: One-time Sales Revenue + Subscription Revenue + Service Revenue
```

---

## M-02: Pyramid Principle

### Source: Barbara Minto, McKinsey

### Core Principles
```
1. Conclusion First (Top-Down)
   Present the conclusion first, then expand on supporting arguments. Don't say "Because of A, B, C, therefore D"
   Instead say "D, for three reasons: A, B, C"

2. Upper Level Summarizes Lower Level
   The core idea of each level is a summary of the ideas at the level below

3. Same Level, Same Category
   Ideas at the same level must belong to the same logical category

4. Organize by Logical Order
   Chronological order / Structural order / Degree order
```

### Pyramid Structure Template

```
Recommendation/Conclusion
├── Argument 1 (Why 1)
│   ├── Supporting Point 1.1
│   └── Supporting Point 1.2
├── Argument 2 (Why 2)
│   ├── Supporting Point 2.1
│   └── Supporting Point 2.2
└── Argument 3 (Why 3)
    ├── Supporting Point 3.1
    └── Supporting Point 3.2
```

### Introduction Structure (SCQA)

```
S (Situation): Background / the stable state everyone knows
C (Complication): What changed / what problem emerged
Q (Question): What question does this raise
A (Answer): What is my answer/recommendation

Example:
S: Our company has maintained 20% annual growth over the past 3 years
C: But growth rate dropped to 8% in the last two quarters, and 3 major competitors have launched AI features
Q: How should we respond to the AI competitive threat?
A: Recommend investing 5M to launch an AI module before Q3, expected to recover 10% growth rate...
```

---

## M-03: Porter's Five Forces + Complements

### Source: Michael Porter, Harvard Business School

### Six Forces Framework (Five Forces + Complements)

| Force | Assessment | High Score Means | Low Score Means |
|------|------|----------|----------|
| Threat of New Entrants | 1-5 | Low entry barriers, profits will be eroded by new entrants | High entry barriers, incumbents are safe |
| Supplier Bargaining Power | 1-5 | Suppliers are strong, costs are uncontrollable | Suppliers are weak, procurement has the advantage |
| Buyer Bargaining Power | 1-5 | Customers are strong, high price pressure | Customers are weak, high pricing freedom |
| Threat of Substitutes | 1-5 | Easy to substitute, business model is fragile | Hard to substitute, model is stable |
| Industry Rivalry | 1-5 | Fierce competition, low profit margins | Mild competition, high profit margins |
| **Complements** | 1-5 | Weak complements, ecosystem immature | Strong complements, ecosystem thriving |

### Scoring Criteria

| Score | Standard |
|------|------|
| 1 | Very Weak — the force is almost non-existent |
| 2 | Relatively Weak — exists but impact is limited |
| 3 | Moderate — worth attention but not decisive |
| 4 | Relatively Strong — the force significantly affects industry profits |
| 5 | Very Strong — the force determines industry profit levels |

### Dynamic Perspective on Five Forces Analysis

```
Static Analysis: Current attractiveness of the industry
Dynamic Analysis: Future attractiveness of the industry

Ask:
- Which force is strengthening? Which is weakening?
- What events could change the balance of forces? (New technology? New regulations? New business models?)
- How can we proactively change the balance of forces? (e.g., reducing buyer bargaining power through branding)
```

---

## M-04: VRIO Capability Analysis

### Source: Jay Barney, Strategic Management

### VRIO Framework

```
V - Valuable: Can this capability create value for customers?
R - Rare: Do competitors generally possess this capability?
I - Inimitable: How costly is it for competitors to imitate this capability?
O - Organized: Does the organizational structure and system support leveraging this capability?

VRIO Decision Matrix:
V  R  I  O  →  Competitive Implication
✗  -  -  -  →  Competitive Disadvantage
✓  ✗  -  -  →  Competitive Parity
✓  ✓  ✗  -  →  Temporary Advantage
✓  ✓  ✓  ✗  →  Underutilized Advantage
✓  ✓  ✓  ✓  →  Sustainable Competitive Advantage ← Target!
```

### Capability Inventory Assessment

| Capability | V | R | I | O | Competitive Implication | Action |
|------|---|---|---|---|---------|------|
| Brand | ✓ | ✓ | ✓ | ✓ | Sustainable Advantage | Continue Investing |
| Technology | ✓ | ✓ | ✗ | - | Temporary Advantage | Accelerate Barrier Building |
| Customer Service | ✓ | ✗ | - | - | Competitive Parity | Raise Standards |

---

## M-05: BCG Growth-Share Matrix

### Source: Boston Consulting Group

### Matrix Structure

```
        Market Growth Rate
        High
        ↑
  ┌─────┼─────┐
  │ ★   │ ❓  │
  │Stars│Question Marks│
  ├─────┼─────┤
  │ 🐄  │ 🐕  │
  │Cash Cows│Dogs│
  └─────┼─────┘
        ↓
        Low
  High ← Relative Market Share → Low
```

### Strategies by Quadrant

| Type | Characteristics | Cash Flow | Strategy |
|------|------|--------|------|
| **Stars** | High Growth + High Share | Neutral | Continue investing, maintain leadership |
| **Cash Cows** | Low Growth + High Share | Strong Positive | Harvest profits, invest in Stars and Question Marks |
| **Question Marks (?)** | High Growth + Low Share | Strong Negative | Selective investment, double down on promising ones |
| **Dogs** | Low Growth + Low Share | Neutral/Negative | Harvest/Sell/Close |

### Limitations of the BCG Matrix

```
Note:
- Only focuses on market growth rate and share, ignoring profitability and competitive dynamics
- "Low growth ≠ unprofitable" — many Cash Cow industries still have ultra-high profits
- "High share ≠ sustainable" — technological disruption can wipe out share overnight
- Suitable for product portfolio VIEW, should not be the sole basis for decision-making
```

---

## M-08: Blue Ocean Strategy ERRC Framework

### Source: W. Chan Kim & Renée Mauborgne

### Four Actions Framework

```
Eliminate: Which factors that the industry takes for granted should be eliminated?
  → These factors are done by everyone, but customers actually no longer need them

Reduce: Which factors should be reduced well below the industry standard?
  → Factors that over-serve customers, can be reduced to save costs

Raise: Which factors should be raised well above the industry standard?
  → Factors that truly pain customers, should far exceed industry standards

Create: Which factors that the industry has never offered should be created?
  → Entirely new sources of value, creating new demand
```

### ERRC One-Page Worksheet

| Eliminate | Raise |
|-----------|-------|
| 1.  | 1. |
| 2.  | 2. |
|-----------|-------|
| Reduce    | Create |
| 1.  | 1. |
| 2.  | 2. |

### Three Characteristics of a Good Value Curve

```
1. Focus: Do not compete on all factors
2. Divergence: The value curve is significantly different from competitors'
3. Compelling Tagline: Can articulate the value proposition in one sentence
```

---

## M-09: JTBD (Jobs-to-Be-Done)

### Source: Clayton Christensen, Harvard

### Core Concepts

```
JTBD = The job that customers "hire" a product/service to get done

Not: What features do customers need?
But: In what context, what job does the customer need to get done?

Three Layers of Job:
├── Functional Job: The specific task that needs to be completed
├── Emotional Job: How do they want to feel? (Reassured/Confident/Recognized)
└── Social Job: How do they want others to perceive them? (Respectable/Smart/Tasteful)
```

### JTBD Perspective Shift

| Traditional Needs Perspective | JTBD Perspective |
|------------|---------|
| "Customers need a faster horse" | "Customers need to get from A to B faster" |
| "Customers need an Excel export feature" | "Customers need to present data to their boss" |
| "Customers need better search" | "Customers need to find XX information within 3 minutes to complete YY report" |

### JTBD Format

```
When [in what context]                           ← Context
I want to [get what job done]                     ← Functional Job
So that [achieve what purpose]                    ← Deeper Job
Instead of [current alternatives and their shortcomings]  ← Competitive Perspective
```

---

## M-10: Unit Economics

### Core Formulas

```
CAC (Customer Acquisition Cost) = Total Sales & Marketing Expenses / New Customers Acquired
LTV (Customer Lifetime Value) = Average Order Value × Gross Margin % × Average Lifetime (months)
LTV/CAC Ratio → >3 Healthy, >5 Excellent

CAC Payback Period (months) = CAC / (Monthly Contribution Margin)
→ <12 months Excellent, 12-18 months Acceptable, >18 months Dangerous

Contribution Margin = Revenue - Variable Costs
→ Equals the incremental profit from one additional customer
```

### Unit Economics Deterioration Signals

```
□ LTV/CAC < 3 → Growth is unsustainable
□ CAC Payback Period > 18 months → Cash flow pressure
□ CAC rising year over year → Intensifying competition / channel inefficiency
□ LTV declining year over year → Product value decay / rising churn rate
□ Paid conversion rate declining year over year → Weakening product-market fit
```

---

## M-11: FMEA Failure Mode Analysis

### Source: NASA / Six Sigma

### RPN Risk Priority

```
RPN = S (Severity) × O (Occurrence) × D (Detection Difficulty)
Each item scored 1-10

Thresholds:
RPN > 200 → Must take immediate action (unacceptable risk)
RPN 100-200 → Strongly recommend action (high risk)
RPN 50-100 → Consider action (moderate risk)
RPN < 50 → Acceptable risk

Improvement Directions:
1. Reduce S → Modify design / add redundancy / buffers
2. Reduce O → Preventive measures / Standardize / automatic checks
3. Reduce D → Early warning / Continuous Monitoring / periodic inspection
```

### FMEA Template

| Process/Function | Failure Mode | Failure Effect | S | Failure Cause | O | Current Controls | D | RPN | Improvement Actions |
|----------|---------|---------|---|---------|---|---------|---|-----|---------|
| | | | | | | | | | |

---

## M-15: MoSCoW Prioritization Method

### Source: DSDM (Dynamic Systems Development Method)

### Core Concepts

```
MoSCoW = Must Have + Should Have + Could Have + Won't Have

Purpose: Strictly prioritize requirements when resources are limited
Application Scenarios: Requirements management, release planning, Minimum Viable Product definition, project scope negotiation
```

### Four Priority Levels Explained

| Level | Meaning | Suggested Proportion | Consequence of Not Doing | Decision Criteria |
|------|------|---------|-----------|---------|
| **Must Have** | Must have, otherwise project fails | ≤60% | System unusable / project failure | Without this feature, does the solution still make sense? |
| **Should Have** | Should have, important but not fatal | ≤20% | Severely impacts experience but workaround exists | Without this feature, does it severely impact the core process? |
| **Could Have** | Could have, nice to have | ≤15% | Slightly impacts experience | Without this feature, would users barely notice? |
| **Won't Have** | Not this time | Explicitly excluded | No impact | Can it be done in the next release? |

### MoSCoW Prioritization Matrix

```
                High
                ↑
        Complexity  │  Should Have    │  Must Have (Do First)
        (Lower Priority) │  (Second Batch)  │  Must Have (Do Later)
                │                 │
        Low      │  Won't Have     │  Could Have
                │                 │
                └─────────────────┴──────→
                Low                High
                        Business Value
```

### MoSCoW Practical Notes

```
1. Must Have proportion must be ≤60%: If it exceeds 60%, the team's definition of "must" is too loose
2. Won't Have does not mean "unimportant": It means "not this time", may be implemented in the next release
3. Prioritization requires stakeholder consensus: BA facilitates discussion, but decision-making authority lies with the business side
4. Linkage with Kano Model: Must Have ≈ Must-be Quality + high-importance One-dimensional Quality
5. Dynamic adjustment: As the project progresses, priorities may change and need regular review
```

### MoSCoW vs Traditional Prioritization

| Traditional Prioritization (P0/P1/P2) | MoSCoW |
|---------------------|--------|
| Ambiguous levels, unclear boundary between P1 and P2 | Four clear levels, each with a clear definition |
| Easy to mark everything as P0 | Must Have proportion forced ≤60% |
| No "explicitly not doing" category | Won't Have explicitly excluded |
| Suitable for internal technical teams | Suitable for communicating with business stakeholders |

---

## M-16: Kano Model

### Source: Noriaki Kano, Tokyo Institute of Technology

### Core Concepts

```
The Kano Model classifies requirements into five types, based on the non-linear relationship between "degree of feature implementation" and "user satisfaction":

Requirement Types:
├── Must-be Quality: Not implementing → dissatisfied; implementing → not more satisfied
├── One-dimensional Quality: Better implementation → more satisfied; worse implementation → more dissatisfied
├── Attractive Quality: Not implementing → not dissatisfied; implementing → very satisfied
├── Indifferent Quality: Whether implemented or not has no impact on satisfaction
└── Reverse Quality: Implementing → dissatisfied
```

### Better-Worse Coefficient Calculation

```
Better Coefficient = (A+O)/(A+O+M+I)
  → Degree to which user satisfaction increases after implementing this feature (0~1)

Worse Coefficient = -(O+M)/(A+O+M+I)
  → Degree to which user satisfaction decreases after NOT implementing this feature (-1~0)

Where: A=Attractive, O=One-dimensional, M=Must-be, I=Indifferent
```

### Kano Classification Decision Table

| Requirement Type | Better Coefficient | Worse Coefficient | Strategy |
|---------|-----------|----------|------|
| **Attractive** | >0.5 | -0.3~0 | Prioritize: Low cost, high delight, differentiation |
| **One-dimensional** | 0.3~0.5 | -0.6~-0.3 | Must do: Linearly correlated with satisfaction, core competitiveness |
| **Must-be** | <0.3 | <-0.6 | Baseline must-do: Not doing causes severe dissatisfaction, but doing adds no bonus |
| **Indifferent** | ≈0 | ≈0 | Don't do: Waste of resources |
| **Reverse** | <0 | >0 | Absolutely don't do: Doing it actually reduces satisfaction |

### Kano Questionnaire Design

```
Ask two questions for each feature:
1. Functional question: If this feature IS implemented, how do you feel?
2. Dysfunctional question: If this feature is NOT implemented, how do you feel?

Options:
- I like it
- It must be
- Neutral
- I can tolerate it
- I dislike it

Based on the combination of answers to both questions, look up the table to determine the requirement type
```

### Kano Model Lifecycle

```
The same feature changes type over time:
Attractive → One-dimensional → Must-be

Example: Mobile phone fingerprint unlock
- 2013 (iPhone 5s debut): Attractive → Delight feature
- 2016: One-dimensional → "A phone at this price should have fingerprint"
- 2020: Must-be → "Won't buy a phone without fingerprint unlock"
```

### Kano and MoSCoW Linkage

| Kano Type | Corresponding MoSCoW | Priority Strategy |
|---------|-----------|----------|
| Must-be | Must Have | Must do, but don't over-invest |
| One-dimensional (High Worse) | Must Have / Should Have | Heavy investment, benchmark against competitors |
| Attractive | Could Have / Should Have | Prioritize low-cost high-delight items |
| Indifferent | Won't Have | Don't do |
| Reverse | Won't Have | Absolutely don't do |

---

## M-17: BDD Behavior-Driven Development

### Source: Dan North (introduced 2006)

### Core Concepts

```
BDD = Behavior-Driven Development

Core Idea: Describe system behavior in natural language, so BA+Dev+QA+business stakeholders can all understand
Essence: Express "requirements" as "behaviors", replace "abstract descriptions" with "examples"
```

### BDD Three Amigos

```
     BA (Business Analyst)          Developer               QA (Tester)
    "What does the business need?"  "How to implement technically?"  "What are the edge cases?"
          │                       │                        │
          └───────────────────────┼────────────────────────┘
                                  │
                           Jointly write Acceptance Criteria
                           (Gherkin scenarios)
```

### Gherkin Syntax Explained

```gherkin
Feature: [Feature Name]
  As a [Role]
  I want [Feature Description]
  So that [Business Value]

  Scenario: [Scenario Name - Happy Path]
    Given [Precondition]
    And [More Preconditions]
    When [User Action]
    And [More Actions]
    Then [Expected Result]
    And [More Expected Results]

  Scenario: [Scenario Name - Error Path]
    Given [Precondition]
    When [Error Action]
    Then [Error Handling Behavior]

  Scenario Outline: [Parameterized Scenario - Data-driven]
    Given the user is on the login page
    When the user enters email "<email>"
    And the user enters password "<password>"
    Then the system displays "<message>"

    Examples:
      | email              | password   | message         |
      | user@example.com   | correct123 | Login successful |
      | user@example.com   | wrong123   | Invalid email or password |
      | invalid@email      | correct123 | Invalid email format |
```

### BDD Core Principles

| Principle | Description |
|------|------|
| **Collaboration Discipline** | BA+Dev+QA jointly define Acceptance Criteria, eliminating understanding gaps |
| **Specification by Example** | Use concrete examples instead of abstract descriptions, "For example... Suppose..." |
| **Living Documentation** | Acceptance Tests are auto-executable, documentation and actual behavior are always in sync |
| **Business Language** | Describe behavior in business terms, not technical terms |
| **Just Enough** | No need to exhaustively cover all scenarios; cover core flows + key exceptions |

### BDD Tool Selection

| Tool | Language | Applicable Scenario |
|------|------|---------|
| Cucumber | Ruby/Java/JS | Cross-functional team collaboration, most mature |
| SpecFlow | .NET/C# | .NET ecosystem |
| Behave | Python | Python projects |
| JBehave | Java | Java projects |
| Gauge | Multi-language | Markdown format, more flexible |

### BDD in the BA Workflow

```
Requirements Elicitation → BDD Workshop (Three Amigos) → Gherkin Scenario Writing → Acceptance Criteria Confirmation → Living Documentation Maintenance
   ↑                                                                    ↓
   └──────────────── Automated Test Execution ←──────────────────────────────────┘
```

---

## M-18: EventStorming

### Source: Alberto Brandolini (DDD Community)

### Core Concepts

```
EventStorming = A collaborative domain modeling workshop method

Core Idea: Reverse-engineer business processes and system boundaries through "domain events"
Applicable Scenarios: Complex business domain modeling, microservice boundary identification, legacy system modernization
```

### Three Workshop Levels

| Level | Goal | Output | Duration | Participants |
|------|------|------|------|--------|
| **Big Picture** | Establish holistic domain understanding | End-to-end business process panorama | 2-4 hours | Business experts + BA + Architect |
| **Process Level** | Identify core processes and boundaries | Bounded context candidates | 4-8 hours | BA + Tech Lead + Domain experts |
| **Design Level** | Detailed design and implementation planning | Aggregates, Entities, Value Objects | 8-16 hours | Development team + BA |

### Six Core Elements

| Element | Color | Description | Example |
|------|------|------|------|
| **Domain Event** | 🟠 Orange | A fact that has already happened in the business (past tense) | "Order Submitted", "Payment Completed", "Goods Shipped" |
| **Command** | 🔵 Blue | An instruction issued by a user/system | "Submit Order", "Confirm Payment", "Ship" |
| **Aggregate** | 🟡 Yellow | The core entity that receives commands and produces events | Order, Payment, Inventory |
| **Policy** | 🟣 Purple | Rules automatically executed after an event is triggered | "Auto-notify warehouse after order payment succeeds" |
| **Read Model** | 🟢 Green | Data view optimized for queries | Order list, pending shipment report |
| **External System** | 🩷 Pink | External dependency systems | Payment gateway, logistics system, SMS gateway |

### EventStorming Workshop Flow

```
Step 1: Post Domain Events (Orange) — Post all business events along a timeline
Step 2: Add Commands (Blue) — What triggered these events?
Step 3: Identify Aggregates (Yellow) — Which entities are responsible for handling commands?
Step 4: Mark Policies (Purple) — What automatically happens after an event is triggered?
Step 5: Mark Read Models (Green) — What information does the user need to see?
Step 6: Mark External Systems (Pink) — Which external services need to be called?
Step 7: Identify Bounded Contexts — Natural clustering based on event flows
```

### Collaboration with DDD Bounded Contexts

```
EventStorming → Discover domain events and business rules
DDD Bounded Contexts → Partition microservices/modules based on event boundaries
BA + Tech Lead participate together, producing architecture boundaries that are both business-aligned and feasible

Bounded Context Identification Signals:
- Natural event clustering: A group of events revolves around the same business concept
- Terminology changes: The same thing has different names in different contexts
- Business rule boundaries: Rules in different contexts change independently
```

---

## M-19: BABOK Agile Extension

### Source: IIBA Agile Extension v2

### Core Concepts

```
BABOK Agile Extension = Application guide for BABOK V3 in agile environments

Core Idea: The BA's role in an agile team shifts from "document writer" to "collaboration facilitator"
```

### Seven Principles of Agile BA

| Principle | Meaning | Practical Application |
|------|------|---------|
| **See the Whole** | Understand end-to-end business context | Use Story Maps to connect strategy and details |
| **Think as a Customer** | Think from the user's perspective | User journey maps, personas, experience metrics |
| **Analyze to Determine What is Valuable** | Focus on value, not output | Impact Mapping, derive requirements backwards from goals |
| **Get Real Using Examples** | Use Specification by Example | Specification by Example, Gherkin scenarios |
| **Understand What is Doable** | Understand technical feasibility | Three Amigos collaboration (BA+Dev+QA) |
| **Stimulate Collaboration and Continuous Improvement** | Foster collaboration and continuous improvement | Retrospectives, communities of practice |
| **Avoid Waste** | Eliminate waste | Minimum viable requirements, don't over-analyze |

### Traditional BA vs Agile BA

| Dimension | Traditional BA | Agile BA |
|------|--------|--------|
| Requirements Documentation | Upfront complete requirements document | Continuous conversation, Just-in-time requirements |
| Working Style | Document-driven | Collaboration-driven |
| Team Position | BA as intermediary | BA embedded in development team |
| Confirmation Method | Signed confirmation | Continuous confirmation |
| Design Approach | Big Design Up Front (BDUF) | Emergent design |
| Requirements Granularity | Complete functional specification | User stories + Acceptance Criteria |
| Change Management | Formal change control process | Dynamic backlog priority adjustment |

### Agile BA Core Practices

```
1. User Story Splitting
   Epic → Feature → User Story → Task
   Splitting Principle: INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)

2. Backlog Refinement
   Frequency: 5-10% of each Sprint
   Output: Prioritized Ready Backlog

3. Acceptance Criteria Driven
   Every Story must have AC, AC must be testable
   Prefer Gherkin format

4. Continuous Elicitation
   Not one-time elicitation, but continuous conversation each Sprint
   Techniques: User interviews, observation, data analysis, A/B testing

5. Minimum Viable Product
   Use Story Map + MoSCoW to define Minimum Viable Product boundaries
   Minimum Viable Product = Minimum feature set × Verifiable hypothesis
```

### Agile BA Rhythm in Scrum

```
Sprint 0: Vision + Initial Backlog + Architecture overview
Sprint Planning: Explain Stories + Acceptance Criteria
Daily Standup: Answer Dev's business questions
During Sprint: Prepare next Sprint's Backlog (Refinement)
Sprint Review: Acceptance of completed Stories
Sprint Retro: Improve BA practices
```

### Agile BA vs Traditional BA Skills Comparison

| Skill | Traditional BA Weight | Agile BA Weight |
|------|----------|----------|
| Documentation Writing | High | Medium |
| Collaboration Facilitation | Medium | High |
| User Story Writing | Low | High |
| Acceptance Criteria Definition | Medium | High |
| Stakeholder Management | High | High |
| Data Analysis | Medium | High |
| Technical Understanding | Low | Medium-High |