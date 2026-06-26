---
name: dead-letter-queue-analyzer
description: Analyze dead letter queue (DLQ) messages to identify failure patterns, root causes, and remediation strategies. Supports AWS SQS, RabbitMQ, Kafka, Azure Service Bus, and generic message queues.
---

# Dead Letter Queue Analyzer

Stop ignoring your dead letter queue. Analyze DLQ messages to find failure patterns, identify root causes, determine which messages are replayable, and generate remediation plans — turning your DLQ from a black hole into an actionable error stream.

Use when: "analyze DLQ", "dead letter queue growing", "why are messages failing", "replay failed messages", "DLQ backlog", "message processing failures", or when unprocessed messages accumulate.

## Commands

### 1. `analyze` — Categorize DLQ Messages

#### Step 1: Read DLQ Messages

**AWS SQS:**
```bash
aws sqs receive-message \
  --queue-url "$DLQ_URL" \
  --max-number-of-messages 10 \
  --attribute-names All \
  --message-attribute-names All | python3 -c "
import json, sys
msgs = json.load(sys.stdin).get('Messages', [])
for m in msgs:
    body = json.loads(m['Body']) if m['Body'].startswith('{') else m['Body']
    attrs = m.get('Attributes', {})
    print(f'ID: {m[\"MessageId\"]}')
    print(f'  Received count: {attrs.get(\"ApproximateReceiveCount\", \"?\")}')
    print(f'  First received: {attrs.get(\"ApproximateFirstReceiveTimestamp\", \"?\")}')
    print(f'  Body preview: {str(body)[:200]}')
    print()
"

# Count total DLQ depth
aws sqs get-queue-attributes --queue-url "$DLQ_URL" \
  --attribute-names ApproximateNumberOfMessages | python3 -c "
import json, sys
attrs = json.load(sys.stdin)['Attributes']
print(f'DLQ depth: {attrs[\"ApproximateNumberOfMessages\"]} messages')
"
```

**RabbitMQ:**
```bash
# List DLQ queues
rabbitmqctl list_queues name messages | grep -i "dead\|dlq\|error"

# Peek at messages
rabbitmqadmin get queue="dead_letter_queue" count=10 2>/dev/null
```

**Kafka:**
```bash
# Read from DLT (dead letter topic)
kafka-console-consumer --bootstrap-server $KAFKA_BROKER \
  --topic "$DLT_TOPIC" --from-beginning --max-messages 20 \
  --property print.headers=true --property print.timestamp=true
```

#### Step 2: Classify Failure Causes

Group DLQ messages by failure reason:

| Category | Signal | Replayable? | Action |
|----------|--------|------------|--------|
| **Schema error** | Validation failure, missing field | After fix | Fix producer or consumer schema |
| **Timeout** | Processing exceeded deadline | Yes | Increase timeout or optimize processing |
| **Dependency down** | Connection refused, 503 | Yes | Wait for recovery, then replay |
| **Poison message** | Crash/exception on processing | No | Fix handler, then replay |
| **Data integrity** | FK violation, duplicate key | Maybe | Fix data, then replay |
| **Permission** | Auth error, access denied | After fix | Fix credentials, then replay |
| **Deserialization** | Invalid JSON/Protobuf/Avro | No | Discard or fix producer |

```python
# Group messages by error pattern
from collections import Counter
errors = Counter()
for msg in dlq_messages:
    # Extract error reason from message attributes or headers
    error = msg.get('error_reason', msg.get('x-death-reason', 'unknown'))
    errors[error] += 1

for error, count in errors.most_common(10):
    print(f'{count:>5}x  {error}')
```

#### Step 3: Generate Report

```markdown
# DLQ Analysis Report

## Summary
- Queue: orders-processing-dlq
- Total messages: 1,247
- Oldest message: 3 days ago
- Growth rate: ~400/day (increasing)

## Failure Categories
| Category | Count | % | Replayable | Root Cause |
|----------|-------|---|------------|------------|
| Timeout | 823 | 66% | ✅ | DB slow queries since Tuesday deploy |
| Schema error | 312 | 25% | ✅ (after fix) | New field `currency` not in consumer schema |
| Poison message | 67 | 5% | ❌ | NullPointer in price calculation |
| Permission | 45 | 4% | ✅ (after fix) | Expired service account token |

## Root Cause
Primary: DB slow queries causing processing timeouts (66% of failures)
- Started: Tuesday 14:30 UTC (correlates with deploy)
- Impact: 823 orders stuck in DLQ

## Remediation Plan
1. **Fix DB performance** — add missing index on orders.status (immediate)
2. **Replay timeout messages** (823) — safe, operations are idempotent
3. **Update consumer schema** to accept `currency` field (312 messages)
4. **Rotate service account token** (45 messages)
5. **Fix NullPointer** in OrderPriceCalculator.java:67 (67 messages — investigate first)
6. Set up DLQ depth alerting (threshold: 50 messages)
```

### 2. `replay` — Generate Replay Script

```bash
# SQS: move messages from DLQ back to main queue
aws sqs start-message-move-task \
  --source-arn "$DLQ_ARN" \
  --destination-arn "$MAIN_QUEUE_ARN" \
  --max-number-of-messages-per-second 10

# Or selective replay (only timeout errors)
# Read, filter, re-send
```

### 3. `monitor` — Set Up DLQ Alerting

Generate CloudWatch alarm / Prometheus alert for DLQ depth:
- Alert when DLQ depth > 0 (any message is a signal)
- Alert when growth rate > N/hour (active problem)
- Alert when oldest message > 24h (messages going stale)
- Dashboard showing DLQ depth over time + categorization

### 4. `prevent` — Improve Message Handling

Recommend changes to prevent future DLQ accumulation:
- Add retry with backoff before sending to DLQ
- Add idempotency keys for safe replay
- Add dead letter reason headers for faster triage
- Add message TTL to prevent infinite accumulation
- Add schema validation before publishing (catch at source)
