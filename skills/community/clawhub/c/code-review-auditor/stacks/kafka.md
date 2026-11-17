# Kafka Review Rules

Use for Kafka producers, consumers, streams, schemas, outbox/inbox patterns, event-driven architecture, and message contracts.

## Correctness And Reliability

- Check consumer group behavior, offset commits, retry topics, dead-letter handling, poison messages, ordering assumptions, and idempotency.
- Verify producer acknowledgement, key choice, partitioning, transactional/outbox guarantees, and duplicate handling.
- Look for schema evolution risks, incompatible payload changes, and missing contract tests.

## Security

- Check SASL/TLS config, topic ACLs, secrets, sensitive payload logging, and cross-tenant topic/key leakage.
- Verify PII retention, compaction, and access assumptions.

## Architecture

- Events should represent stable domain facts or clear integration messages, not leak internal persistence models casually.
- Avoid using Kafka as synchronous RPC unless timeout, retry, and failure semantics are explicit.
- Recommend outbox/inbox only when consistency, retries, or duplicate handling justify the operational cost.

## Performance

- Review batch size, linger, compression, consumer concurrency, max poll interval, backpressure, lag monitoring, and payload size.
- Check whether slow downstream calls block partition progress.

## Observability

- Require metrics for consumer lag, processing latency, failure rate, retry count, DLQ volume, and schema errors.
- Logs should include topic, partition, offset, key/correlation ID, and sanitized error context.
