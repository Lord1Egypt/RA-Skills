# Customer Research Examples

This directory contains example personas and validation workflows.

## Example 1: FIRE Enthusiast Persona Validation

**Scenario:** Validate demand for FIRE Sim product before building marketing strategy

### Files
- `fire-enthusiast-persona.json` — Persona definition with assumptions and pain points

### Run the Example

1. **Mine Reddit for retirement calculator discussions:**
   ```bash
   cd /Users/clawdiri/.openclaw/workspace
   ./skills/customer-research/scripts/reddit-miner.sh \
     --subreddit "financialindependence" \
     --query "retirement calculator" \
     --limit 50
   ```

2. **Validate persona against research data:**
   ```bash
   ./skills/customer-research/scripts/persona-validator.sh \
     --persona-file skills/customer-research/examples/fire-enthusiast-persona.json
   ```

3. **Generate interview script:**
   ```bash
   ./skills/customer-research/scripts/interview-generator.sh \
     --persona "30-40 tech worker, $200K income, aiming FIRE by 45" \
     --problem "existing retirement tools too conservative or too complex"
   ```

### Expected Output

**Validation Report:**
- 4 assumptions validated (3 strong, 1 weak)
- 5 pain points confirmed with sample quotes
- Recommendations for next steps

**Key Findings:**
- ✅ Strong evidence for "too conservative" assumption
- ✅ Multiple pain points validated across 20+ Reddit threads
- ⚠️ Monte Carlo simulation need has weak support (needs more data)
- ✅ Side hustle income modeling is frequently requested

**Next Steps:**
1. Use validated pain points in content strategy
2. Run targeted interviews for weak-support items
3. Feed customer language into Ogilvy for marketing copy
4. Update product roadmap based on validated needs

## Creating Your Own Persona

Use this template:

```json
{
  "name": "Persona Name",
  "demographics": {
    "age_range": "X-Y",
    "income": "$X-$Y",
    "occupation": "role"
  },
  "assumptions": [
    {
      "id": "A1",
      "statement": "Clear, testable assumption",
      "confidence": "low|medium|high"
    }
  ],
  "pain_points": [
    "Specific pain point in customer language"
  ]
}
```

## Integration with Marketing Pipeline

```
Research → Validation → Strategy → Content
   ↓           ↓           ↓          ↓
Reddit    Persona    Content     Ogilvy
Mining    Validator  Pillars    Execution
```

**Workflow:**
1. Mine customer conversations (Reddit, reviews, forums)
2. Validate persona assumptions against real data
3. Extract validated pain points and customer language
4. Feed into content strategy (projects/davinci-enterprises/customer-insights.md)
5. Ogilvy creates content using real customer language
6. Track what resonates, iterate

## Quality Standards

- **Minimum sample:** 30+ sources per research question
- **Cross-validation:** Multiple sources (Reddit + reviews + interviews)
- **Real quotes:** Capture verbatim customer language for marketing
- **Document failures:** What you disproved is as valuable as what you proved
