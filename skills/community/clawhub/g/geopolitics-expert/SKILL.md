---
name: geopolitics-expert
description: Geopolitical conflict analysis for war sentiment assessment. Use when analyzing armed conflicts, military interventions, or regional crises to determine conflict duration probability, economic and commodity impacts, trading opportunities, and termination scenarios. Triggered by news article URLs about wars or military operations.
---

# Geopolitics Expert

Analyzes armed conflicts through integrated frameworks to assess war duration, economic impact, and termination scenarios.

## Usage

```
geopolitics-expert <news_url>
```

The skill fetches the news URL and produces a structured analysis with five outputs.

## Workflow

### Step 1: Fetch and Parse News Content

Use `web_fetch` to extract article content from the provided URL.

### Step 2: Apply Analytical Frameworks

Analyze the conflict using these integrated frameworks (stored in `references/`):

1. **Strategic Gravity** — forever war vs short war indicators
2. **Modern Doctrines** — US intervention triggers and target selection
3. **Five Pathways** — conflict termination scenarios
4. **Perpetual Quagmire** — forever war risk factors
5. **IRGCistan** — post-theocratic military state dynamics
6. **Hormuz Siege** — chokepoint weaponization patterns
7. **Reopening Blueprints** — strategic options for de-escalation

### Step 3: Generate Structured Output

Produce analysis in this exact format:

```
## 1. Conclusion
[Core assessment of the conflict situation]

## 2. Economic/Commodity Impact
[Effects on oil, gas, fertilizers, supply chains, inflation]

## 3. Commodity Trading Odds
[Assessment of trading opportunities: long/short positions, risk factors]

## 4. War Duration Categorization
- **Short-term war probability**: X%
- **Long-term/forever war probability**: Y%
- **Key indicators**: [list specific factors from Strategic Gravity framework]

## 5. Termination Scenarios
[Summary of which pathways could end this conflict, ranked by likelihood]
```

## Framework Reference

Read `references/frameworks.md` for detailed analytical models when complex conflicts require deeper assessment.

## Output Guidelines

- **Be decisive** — provide clear probabilities, not vague ranges
- **Anchor to frameworks** — cite specific indicators from the loaded models
- **Economic focus** — always tie back to commodity impacts (oil, gas, fertilizer, shipping)
- **Scenario-ranked** — order termination scenarios by probability, not alphabetically
