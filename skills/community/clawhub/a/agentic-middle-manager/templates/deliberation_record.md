# Deliberation Record Schema

## Purpose

A deliberation record is a structured account of an AI agent's reasoning process for a significant decision. It functions as a medical chart rather than a simple log entry, capturing the full context, alternatives, rationale, and outcome of every consequential agent action.

## Required Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `record_id` | UUID string | Unique identifier for this deliberation record |
| `timestamp` | ISO 8601 date-time | When the decision was made |
| `agent_id` | string | Identifier of the AI agent that made the decision |
| `provenance` | object | The provenance chain linking this action to human authorization |
| `context` | object | The situation and data available at the time of the decision |
| `alternatives` | array | The options the agent evaluated before making its decision |
| `rationale` | string | Why the chosen action was selected over the alternatives |
| `assumptions` | array of strings | Explicit list of assumptions the agent made |
| `confidence` | object | The agent's confidence assessment and routing action |
| `limitations` | array of strings | Known limitations of this analysis |
| `outcome` | object | The action taken and its observed result |

## Provenance Object

The provenance chain links every action to a human authorization.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `human_authorizer` | string | Yes | Name and role of the human who authorized this agent's scope of action |
| `authorization_scope` | string | Yes | Explicit description of what the agent is authorized to do |
| `authorization_date` | ISO 8601 date-time | No | When the authorization was granted |

## Context Object

The situation and data available at the time of the decision.

| Field | Type | Description |
| :--- | :--- | :--- |
| `situation_summary` | string | Concise description of the situation requiring a decision |
| `data_sources` | array of objects | Each with `source` (string), `type` ("internal" or "external"), `relevance` ("high", "medium", "low") |
| `cynefin_classification` | enum | One of: "clear", "complicated", "complex", "chaotic" |

## Alternatives Array

Each alternative the agent evaluated:

| Field | Type | Description |
| :--- | :--- | :--- |
| `option` | string | Name or description of the alternative |
| `pros` | array of strings | Key advantages |
| `cons` | array of strings | Key disadvantages |
| `risk_level` | enum | One of: "low", "medium", "high" |

## Confidence Object

| Field | Type | Description |
| :--- | :--- | :--- |
| `score` | number (0.0 - 1.0) | The agent's confidence in its decision |
| `factors` | array of strings | Factors contributing to the confidence level |
| `routing_action` | enum | One of: "auto-executed", "human-reviewed", "escalated" |

## Outcome Object

| Field | Type | Description |
| :--- | :--- | :--- |
| `action_taken` | string | Description of the action that was executed |
| `result` | string | The observed result of the action (filled in post-execution) |
| `post_mortem_required` | boolean | Whether this decision requires a post-mortem review |

## Quality Criteria

A deliberation record is considered adequate if a human reviewer can:

1. Understand the decision without additional context.
2. Identify the specific point where the reasoning might have gone wrong.
3. Determine whether the agent's assumptions were reasonable given the available data.

## Full JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Deliberation Record",
  "description": "A structured account of an AI agent's reasoning process for a significant decision.",
  "type": "object",
  "required": ["record_id", "timestamp", "agent_id", "provenance", "context", "alternatives", "rationale", "assumptions", "confidence", "limitations", "outcome"],
  "properties": {
    "record_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this deliberation record."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of when the decision was made."
    },
    "agent_id": {
      "type": "string",
      "description": "Identifier of the AI agent that made the decision."
    },
    "provenance": {
      "type": "object",
      "required": ["human_authorizer", "authorization_scope"],
      "properties": {
        "human_authorizer": { "type": "string" },
        "authorization_scope": { "type": "string" },
        "authorization_date": { "type": "string", "format": "date-time" }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "situation_summary": { "type": "string" },
        "data_sources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": { "type": "string" },
              "type": { "type": "string", "enum": ["internal", "external"] },
              "relevance": { "type": "string", "enum": ["high", "medium", "low"] }
            }
          }
        },
        "cynefin_classification": {
          "type": "string",
          "enum": ["clear", "complicated", "complex", "chaotic"]
        }
      }
    },
    "alternatives": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "option": { "type": "string" },
          "pros": { "type": "array", "items": { "type": "string" } },
          "cons": { "type": "array", "items": { "type": "string" } },
          "risk_level": { "type": "string", "enum": ["low", "medium", "high"] }
        }
      }
    },
    "rationale": { "type": "string" },
    "assumptions": { "type": "array", "items": { "type": "string" } },
    "confidence": {
      "type": "object",
      "properties": {
        "score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "factors": { "type": "array", "items": { "type": "string" } },
        "routing_action": { "type": "string", "enum": ["auto-executed", "human-reviewed", "escalated"] }
      }
    },
    "limitations": { "type": "array", "items": { "type": "string" } },
    "outcome": {
      "type": "object",
      "properties": {
        "action_taken": { "type": "string" },
        "result": { "type": "string" },
        "post_mortem_required": { "type": "boolean" }
      }
    }
  }
}
```
