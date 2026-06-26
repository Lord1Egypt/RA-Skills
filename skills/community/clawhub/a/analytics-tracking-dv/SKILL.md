---
id: 'analytics-tracking'
name: 'Analytics Tracking'
description: 'Track events and user behavior using Segment.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Analytics Tracking

Track events and user behavior using Segment.

## Usage

### Track an event

```bash
analytics-tracking track \
  --event "Signed Up" \
  --user-id "user-123" \
  --properties '{"plan":"Pro"}'
```

### Identify a user

```bash
analytics-tracking identify \
  --user-id "user-123" \
  --traits '{"name":"John Doe","email":"john.doe@example.com"}'
```

### Create a group

```bash
analytics-tracking group \
  --user-id "user-123" \
  --group-id "group-abc" \
  --traits '{"name":"Acme Inc."}'
```
