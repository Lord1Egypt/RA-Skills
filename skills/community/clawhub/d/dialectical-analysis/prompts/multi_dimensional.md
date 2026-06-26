# Multi-Dimensional Analysis Framework

## Overview

This framework extends the dialectical analysis by adding multiple analytical dimensions. Instead of just Pro vs Con, each dimension is analyzed from both positive and negative perspectives.

## Supported Dimensions

### 1. Technology (技术)
- Technical feasibility
- Innovation capability
- Technical barriers
- R&D capability
- Technology lifecycle

### 2. Market (市场)
- Market size and growth
- Market access
- Customer needs
- Competitive landscape
- Market timing

### 3. Finance (财务)
- Investment requirements
- ROI projections
- Cash flow
- Cost structure
- Financial risks

### 4. Legal/Compliance (法律)
- Regulatory requirements
- Compliance risks
- Intellectual property
- Contractual risks
- Liability exposure

### 5. Operations (运营)
- Operational capability
- Supply chain
- Scalability
- Quality control
- Execution risks

### 6. Strategy (战略)
- Strategic fit
- Competitive positioning
- Long-term vision
- Synergies
- Strategic risks

## Output Format

### Multi-Dimensional Analysis (JSON)
```json
{
  "dimensions": {
    "technology": {
      "score": 7,
      "pro_arguments": [...],
      "con_arguments": [...],
      "summary": "..."
    },
    "market": {
      "score": 6,
      "pro_arguments": [...],
      "con_arguments": [...],
      "summary": "..."
    },
    "finance": {
      "score": 5,
      "pro_arguments": [...],
      "con_arguments": [...],
      "summary": "..."
    },
    "legal": {
      "score": 8,
      "pro_arguments": [...],
      "con_arguments": [...],
      "summary": "..."
    }
  },
  "overall_assessment": "...",
  "recommendations": [...]
}
```

## Dimension Scoring

Each dimension is scored 1-10:
- 1-3: High risk / Weak
- 4-6: Medium risk / Moderate
- 7-10: Low risk / Strong

## Weighted Scoring (Optional)

You can assign weights to dimensions based on importance:
```json
{
  "weights": {
    "technology": 0.2,
    "market": 0.3,
    "finance": 0.25,
    "legal": 0.15,
    "operations": 0.1
  }
}
```

## Language Adaptation

- **Output language MUST match the user's input language**
- Use the same language for dimension names as user's input

## Analysis Process

1. **Select dimensions**: Choose relevant dimensions for the topic
2. **Analyze each dimension**: Pro and Con arguments for each
3. **Score dimensions**: 1-10 scoring with rationale
4. **Calculate weighted score**: If weights provided
5. **Synthesize**: Overall assessment and recommendations

## Notes

- Not all dimensions are always relevant
- Scores are relative, not absolute
- Focus on key insights per dimension
- Prioritize actionable recommendations
