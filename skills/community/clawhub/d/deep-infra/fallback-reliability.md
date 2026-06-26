# Fallback Reliability — Deep Infra

## Failure Modes to Plan For

- Rate limit responses during traffic spikes.
- Provider-side outages or degraded regions.
- Latency spikes that breach user expectations.
- Quality regressions after model updates.

## Fallback Policy Design

| Trigger | Immediate Action | Follow-up |
|---------|------------------|-----------|
| Rate limit | Retry once with jitter, then fallback | Log event and adjust burst policy |
| Timeout | Fallback to lower-latency model | Record latency threshold breach |
| Repeated format failure | Switch to more deterministic model | Tighten prompt constraints |
| Model outage | Route to different model family | Mark incident and recovery time |

## Reliability Rules

1. Avoid infinite retries; cap attempts and fail forward.
2. Keep at least two independent routing paths for critical workloads.
3. Separate reliability fallback from cost optimization fallback.
4. Record incident fingerprints so repeated outages are recognized quickly.
5. Use models from different families in fallback chains (e.g., DeepSeek primary with GLM fallback).

## Quick Health Check

```bash
curl -sS https://api.deepinfra.com/v1/openai/models | jq '.data[0].id'
```

If this fails consistently, avoid changing routing policy until connectivity and auth are confirmed.
