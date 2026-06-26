# Decision Dynamo — Criteria Reference

## The Five Criteria

| Key              | Label                        | Type     | Description                                              |
|------------------|------------------------------|----------|----------------------------------------------------------|
| skill_leverage   | Skill / Leverage Gain        | Positive | Does this grow your capabilities or create future value? |
| goal_alignment   | Long-term Goal Alignment     | Positive | Does this move you toward your larger goals?             |
| mental_drag      | Mental / Emotional Drag      | Negative | How much stress, dread, or cognitive load does it add?   |
| financial_cost   | Financial / Resource Cost    | Negative | How much does it cost in money or tangible resources?    |
| time_effort      | Time and Effort              | Negative | How much time and energy does it require?                |

## Scoring Scale (1–10)

- **1** = extremely low (e.g., skill gain: none / mental drag: none)
- **10** = extremely high (e.g., skill gain: transformative / mental drag: overwhelming)

## Weights (1–10)

Weights reflect how much each criterion matters *to you* for this specific decision.
A weight of 10 means "this is critical." A weight of 1 means "barely matters."

## Inversion Logic for Negative Criteria

Negative criteria are inverted so that a *lower* raw score (less drag/cost/effort) produces
a *higher* contribution to the total:

```
contribution = (11 - score) * weight
```

This means scoring mental_drag = 2 (low drag) is *better* than scoring it 9 (high drag).

## JSON Input Format

```json
{
  "weights": {
    "skill_leverage": 8,
    "goal_alignment": 9,
    "mental_drag": 6,
    "financial_cost": 5,
    "time_effort": 7
  },
  "options": [
    {
      "name": "Option A",
      "scores": {
        "skill_leverage": 8,
        "goal_alignment": 7,
        "mental_drag": 3,
        "financial_cost": 4,
        "time_effort": 5
      }
    },
    {
      "name": "Option B",
      "scores": {
        "skill_leverage": 5,
        "goal_alignment": 6,
        "mental_drag": 7,
        "financial_cost": 8,
        "time_effort": 9
      }
    }
  ]
}
```
