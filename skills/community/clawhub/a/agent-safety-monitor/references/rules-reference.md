# Safety Rules Reference

## YAML Schema

```yaml
# Rate limits (actions per minute)
rate_limits:
  exec: 30
  message: 20
  file_write: 10
  api_call: 60

# Tool allowlist (omit to allow all)
allowlisted_tools:
  - read
  - write
  - search
  - exec

# Blocked target patterns
blocked_targets:
  - /etc/shadow
  - .env
  - private_key
  - password

# Budget cap (USD)
budget_cap: 5.00

# Token budget per hour
max_tokens_per_hour: 100000

# File scope restrictions
scope:
  allowed_paths:
    - /home/agent/workspace
  blocked_paths:
    - /etc
    - /root
    - ~/.ssh
```

## Alert Levels

| Level | Description | Auto-Action |
|-------|------------|-------------|
| warn | Suspicious but not dangerous | Log only |
| critical | Policy violation | Pause agent |
| fatal | Severe violation | Kill agent immediately |

## Anomaly Detection Thresholds

- **Frequency spike**: >3x baseline average (min 5 occurrences)
- **Loop detection**: Same action+target repeated >10x in 5 min
- **Token spike**: >5x recent average (min 1000 tokens)
