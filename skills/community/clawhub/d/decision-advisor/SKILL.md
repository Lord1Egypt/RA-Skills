---
name: decision-advisor
description: Decision-making advisor using Tree of Thoughts for exploring options, analyzing trade-offs, and providing data-driven recommendations.
---

# Decision Advisor

AI-powered decision advisor that uses Tree of Thoughts to explore multiple options, analyze trade-offs, and provide structured recommendations for complex decisions.

---

## Use Cases

### 🎯 Technical Decisions

- Technology stack selection
- Architecture patterns
- Build vs buy decisions
- Tool evaluation

### 💼 Business Decisions

- Product feature prioritization
- Investment analysis
- Strategic planning
- Risk assessment

### 👥 Personal Decisions

- Career choices
- Education paths
- Major purchases

---

## Features

### 🌳 Option Exploration

- Generate multiple alternatives
- Consider non-obvious options
- Explore different perspectives

### ⚖️ Trade-off Analysis

- Pros and cons for each option
- Risk assessment
- Cost-benefit analysis
- Long-term implications

### 📊 Structured Framework

- Decision criteria definition
- Weighted scoring
- Sensitivity analysis
- Recommendation with confidence level

---

## Usage

```javascript
const advisor = new DecisionAdvisor();

const decision = await advisor.advise({
  decision: 'Choose frontend framework for enterprise app',
  options: ['React', 'Vue', 'Angular'],
  criteria: [
    { name: 'Performance', weight: 0.3 },
    { name: 'Developer Experience', weight: 0.25 },
    { name: 'Ecosystem', weight: 0.25 },
    { name: 'Long-term Support', weight: 0.2 }
  ],
  context: 'Team of 20 developers, 5-year project lifespan'
});

console.log(decision.recommendation);
console.log(decision.analysis);
```

---

## Example Output

```markdown
## Decision Analysis: Frontend Framework Selection

### Options Evaluated
1. React
2. Vue
3. Angular

### Scoring Matrix

| Criteria              | Weight | React | Vue | Angular |
|-----------------------|--------|-------|-----|---------|
| Performance           | 30%    | 8.5   | 8.0 | 7.5     |
| Developer Experience  | 25%    | 9.0   | 8.5 | 7.0     |
| Ecosystem             | 25%    | 9.5   | 7.5 | 8.5     |
| Long-term Support     | 20%    | 9.0   | 7.0 | 9.0     |
| **Weighted Score**    |        | **8.95** | 7.85 | 7.95 |

### Recommendation

**React** is recommended with a weighted score of 8.95/10.

### Key Reasons
1. Largest ecosystem and community
2. Excellent developer experience
3. Strong corporate backing (Meta)
4. Proven at scale

### Risks & Mitigations
- **Risk**: Frequent breaking changes
- **Mitigation**: Use stable LTS versions, invest in testing

### Confidence Level: High (85%)
```

---

## Architecture

```
Decision Request
    ↓
Tree of Thoughts Agent
    ├─ Generate options
    ├─ Explore variations
    └─ Identify criteria
    ↓
Evaluation Phase
    ├─ Score each option
    ├─ Analyze trade-offs
    └─ Assess risks
    ↓
Recommendation Engine
    ├─ Weighted scoring
    ├─ Sensitivity analysis
    └─ Confidence calculation
    ↓
Structured Report
```

---

## Installation

```bash
clawhub install decision-advisor
```

---

## License

MIT

---

## Version

1.0.0

---

## Created

2026-04-02
