# Council v2 JSON Schemas

## Reviewer Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CouncilV2ReviewerOutput",
  "type": "object",
  "required": ["reviewer", "model", "verdict", "confidence", "findings", "summary"],
  "additionalProperties": false,
  "properties": {
    "reviewer": {"type": "string"},
    "model": {"type": "string"},
    "verdict": {
      "type": "string",
      "enum": ["approve", "approve_with_conditions", "reject"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["severity", "title", "detail", "recommendation"],
        "additionalProperties": false,
        "properties": {
          "severity": {
            "type": "string",
            "enum": ["critical", "warning", "note"]
          },
          "title": {"type": "string"},
          "detail": {"type": "string"},
          "recommendation": {"type": "string"}
        }
      }
    },
    "summary": {"type": "string"}
  }
}
```

### Reviewer Example

```json
{
  "reviewer": "Security & Risk",
  "model": "grok4",
  "verdict": "approve_with_conditions",
  "confidence": 0.86,
  "findings": [
    {
      "severity": "warning",
      "title": "Missing rollback gate",
      "detail": "The plan changes auth flow without a tested rollback path.",
      "recommendation": "Add explicit rollback steps and exit criteria."
    }
  ],
  "summary": "Directionally sound, but not safe to ship without rollback controls."
}
```

## Synthesis Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CouncilV2SynthesisOutput",
  "type": "object",
  "required": [
    "verdicts",
    "mechanical_result",
    "vote_count",
    "critical_blocks",
    "minority_report",
    "anti_consensus_check",
    "conditions"
  ],
  "additionalProperties": false,
  "properties": {
    "verdicts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["reviewer", "model", "verdict", "confidence", "summary"],
        "properties": {
          "reviewer": {"type": "string"},
          "model": {"type": "string"},
          "verdict": {
            "type": "string",
            "enum": ["approve", "approve_with_conditions", "reject"]
          },
          "confidence": {"type": "number"},
          "summary": {"type": "string"}
        }
      }
    },
    "mechanical_result": {
      "type": "string",
      "enum": ["approve", "approve_with_conditions", "reject", "blocked"]
    },
    "vote_count": {
      "type": "object",
      "required": ["approve_points", "reviewer_count", "thresholds"],
      "properties": {
        "approve_points": {"type": "number"},
        "reviewer_count": {"type": "integer"},
        "thresholds": {"type": "object"}
      }
    },
    "critical_blocks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["reviewer", "title", "detail"],
        "properties": {
          "reviewer": {"type": "string"},
          "title": {"type": "string"},
          "detail": {"type": "string"}
        }
      }
    },
    "minority_report": {
      "type": ["object", "null"],
      "properties": {
        "reviewer": {"type": "string"},
        "verdict": {"type": "string"},
        "summary": {"type": "string"}
      }
    },
    "anti_consensus_check": {
      "type": "object",
      "required": ["triggered", "note", "strongest_counterargument"],
      "properties": {
        "triggered": {"type": "boolean"},
        "note": {"type": "string"},
        "strongest_counterargument": {"type": "string"}
      }
    },
    "conditions": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```
