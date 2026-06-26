---
name: backpressure-analyzer
description: Detect and resolve backpressure issues in data pipelines, message queues, and streaming systems. Identify bottleneck stages, measure queue depths and processing rates, and recommend flow control strategies.
---

# Backpressure Analyzer

Find where your pipeline is backing up. Measure processing rates at each stage, identify the bottleneck, detect growing queues, and recommend flow control strategies — bounded buffers, rate limiting, load shedding, or autoscaling.

Use when: "pipeline is slow", "queue keeps growing", "messages backing up", "consumer can't keep up", "producer faster than consumer", "backpressure", "flow control", "bottleneck analysis", or when processing delays increase over time.

## Commands

### 1. `detect` — Find Backpressure Points

#### Step 1: Measure Queue Depths

```bash
# Kafka consumer lag
kafka-consumer-groups --bootstrap-server $KAFKA_BROKER --describe --all-groups 2>/dev/null | \
  awk 'NR>1 && $6>0 {printf "%-30s %-20s lag=%s\n", $1, $4, $6}' | sort -t= -k2 -rn | head -20

# RabbitMQ queue depths
rabbitmqctl list_queues name messages consumers 2>/dev/null | \
  awk '$2>0 {print $2 "\t" $1 "\tconsumers=" $3}' | sort -rn | head -20

# AWS SQS
for queue_url in $(aws sqs list-queues --query 'QueueUrls[]' --output text); do
  attrs=$(aws sqs get-queue-attributes --queue-url "$queue_url" \
    --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible \
    --output json 2>/dev/null)
  visible=$(echo "$attrs" | python3 -c "import json,sys;print(json.load(sys.stdin)['Attributes'].get('ApproximateNumberOfMessages','0'))")
  inflight=$(echo "$attrs" | python3 -c "import json,sys;print(json.load(sys.stdin)['Attributes'].get('ApproximateNumberOfMessagesNotVisible','0'))")
  if [ "$visible" -gt 0 ] 2>/dev/null; then
    echo "Queue: $(basename $queue_url) — pending=$visible, in-flight=$inflight"
  fi
done

# Redis Streams
redis-cli XINFO STREAM mystream 2>/dev/null | grep -E "length|groups"
redis-cli XINFO GROUPS mystream 2>/dev/null
```

#### Step 2: Measure Processing Rates

```bash
# Measure throughput at each pipeline stage
# Take two snapshots 60s apart and calculate rate

# Kafka: messages produced vs consumed per second
kafka-consumer-groups --bootstrap-server $KAFKA_BROKER --describe --group mygroup 2>/dev/null | \
  awk 'NR>1 {lag+=$6; offset+=$4} END {print "Total lag:", lag, "Current offset:", offset}'

# Process-level: messages processed per second
# Check application metrics endpoint
curl -s http://localhost:9090/metrics | grep -E "messages_processed_total|items_processed_total"
```

#### Step 3: Identify Bottleneck

Map the pipeline stages and their rates:

```
Producer (1000 msg/s) → Queue A (depth: 5) → Stage 1 (800 msg/s) → Queue B (depth: 50000) → Stage 2 (200 msg/s) → Queue C (depth: 2) → Stage 3 (500 msg/s)
                                                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                        BOTTLENECK: Stage 2 can't keep up
```

The bottleneck is the stage with:
- **Growing queue depth** (input queue getting deeper over time)
- **Lowest throughput** relative to its input rate
- **Highest resource utilization** (CPU, memory, I/O at capacity)

#### Step 4: Generate Report

```markdown
# Backpressure Analysis Report

## Pipeline: Order Processing

## Flow Map
```
API (1000 req/s)
  → order-events (Kafka, lag: 45,000 ⚠️, growing +200/min)
    → order-validator (3 pods, 350 msg/s each = 1050 total)
      → validated-orders (Kafka, lag: 200, stable ✅)
        → payment-processor (2 pods, 150 msg/s each = 300 total)
          → payment-results (Kafka, lag: 85,000 🔴, growing +700/min)
            → notification-sender (1 pod, 500 msg/s)
```

## Bottleneck: payment-processor
- **Input rate:** 1050 msg/s (from validator)
- **Processing rate:** 300 msg/s (2 pods × 150 msg/s)
- **Deficit:** 750 msg/s accumulating in queue
- **Current backlog:** 85,000 messages (~4.7 hours to drain at current rate)
- **Resource utilization:** CPU 95%, memory 60%, network 20%
- **Root cause:** CPU-bound — payment validation is computationally expensive

## Recommendations (in order)
1. **Scale out:** Increase payment-processor to 7 pods (7 × 150 = 1050 msg/s)
   - Cost: +5 pods × $X/month
   - Time to drain backlog: ~2.5 hours after scaling

2. **Optimize processing:** Profile payment validation for optimization
   - Current: 6.7ms per message
   - Target: 1ms per message (would need only 2 pods)

3. **Add backpressure signal:** Have payment-processor signal order-validator to slow down
   - Reactive Streams-style demand signaling
   - Or: consumer pause when lag > threshold

4. **Load shedding (last resort):** Drop low-priority messages when queue > 100K
   - Only for non-critical notifications, never for payments
```

### 2. `strategies` — Recommend Flow Control

Based on the pipeline characteristics, recommend:

- **Bounded buffers:** Set max queue size, block producer when full
- **Rate limiting:** Limit producer rate to match slowest consumer
- **Autoscaling:** Scale consumers based on queue depth
- **Load shedding:** Drop low-priority messages under pressure
- **Batch processing:** Accumulate and process in batches for efficiency
- **Circuit breaker:** Stop sending to overwhelmed downstream
- **Priority queues:** Process critical messages first when backed up

### 3. `monitor` — Set Up Backpressure Alerts

Generate alerting rules:
```yaml
# Prometheus alert rules
groups:
  - name: backpressure
    rules:
      - alert: KafkaConsumerLagHigh
        expr: kafka_consumergroup_lag_sum > 10000
        for: 5m
        labels:
          severity: warning
      - alert: KafkaConsumerLagCritical
        expr: kafka_consumergroup_lag_sum > 100000
        for: 5m
        labels:
          severity: critical
      - alert: QueueDepthGrowing
        expr: rate(kafka_consumergroup_lag_sum[5m]) > 0
        for: 15m
        labels:
          severity: warning
```
