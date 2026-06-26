---
name: Filter
description: Create and manage reusable filter rules for email, news, search results, and structured task streams. Designed to reduce noise and preserve signal in OpenClaw workflows.
version: 1.1.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
      config:
        - ~/.openclaw/workspace/memory/filter/rules.json
---

# Filter

Filter is a rule-based skill for reducing noise and preserving signal.

It helps create and manage reusable filter rules for:
- email
- news
- search results
- structured task streams
- JSON-like data

## What this skill does
- creates filter rules
- stores reusable rules locally
- supports priority-based filtering
- supports allowlists and blocklists
- prepares rule sets for future filtering workflows

## Best use cases
- email triage
- news feed cleanup
- search result cleanup
- task stream narrowing
- structured data filtering

## Inputs
- content type
- filter criteria
- priority level

## Output
- saved filter rule
- reusable local rule set
- rule summary
