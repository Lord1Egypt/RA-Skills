# Scoring Framework

Scores are decision aids, not objective truth. Always explain tradeoffs.

## Candidate Score Fields

Each candidate may be rated 0-10 on:

- sound
- anc
- transparency
- mic
- comfort
- battery
- codec
- latency
- multipoint
- app
- water_resistance
- ecosystem
- reliability
- value

Unknown fields should be null, not guessed.

## Default Weights

### Balanced

```json
{
  "sound": 0.15,
  "anc": 0.15,
  "mic": 0.12,
  "comfort": 0.15,
  "battery": 0.10,
  "codec": 0.05,
  "latency": 0.03,
  "multipoint": 0.05,
  "app": 0.05,
  "water_resistance": 0.03,
  "ecosystem": 0.05,
  "reliability": 0.07,
  "value": 0.10
}
```

### Commuting + Calls

```json
{
  "anc": 0.25,
  "mic": 0.22,
  "comfort": 0.15,
  "battery": 0.10,
  "sound": 0.08,
  "multipoint": 0.05,
  "reliability": 0.07,
  "value": 0.08
}
```

### Music First

```json
{
  "sound": 0.35,
  "comfort": 0.15,
  "codec": 0.10,
  "app": 0.10,
  "anc": 0.08,
  "battery": 0.07,
  "reliability": 0.07,
  "value": 0.08
}
```

### Gym

```json
{
  "comfort": 0.22,
  "water_resistance": 0.20,
  "battery": 0.12,
  "reliability": 0.12,
  "sound": 0.10,
  "mic": 0.08,
  "value": 0.16
}
```

## Hard Constraints

Remove candidates before scoring if they violate hard constraints:

- above maximum budget unless user allows stretch picks
- unavailable in target region
- excluded brand
- missing must-have feature
- known deal breaker

## Handling Unknowns

If a score field is unknown:

- Do not invent it.
- Exclude that weight from the denominator for the numeric score.
- Mention lower confidence in the report.
