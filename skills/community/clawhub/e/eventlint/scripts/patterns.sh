#!/usr/bin/env bash
# EventLint -- Event & Message Queue Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Immediate reliability risk (message loss, infinite redelivery, dual-write)
#   high     -- Significant event-driven problem requiring prompt attention
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   PP (Producer Patterns)       -- 15 patterns (PP-001 to PP-015)
#   CP (Consumer Patterns)       -- 15 patterns (CP-001 to CP-015)
#   MS (Message Schema)          -- 15 patterns (MS-001 to MS-015)
#   ED (Error & Dead Letter)     -- 15 patterns (ED-001 to ED-015)
#   OD (Ordering & Delivery)     -- 15 patterns (OD-001 to OD-015)
#   EO (Event Observability)     -- 15 patterns (EO-001 to EO-015)

set -euo pipefail

# ============================================================================
# 1. PRODUCER PATTERNS (PP-001 through PP-015)
#    Detects fire-and-forget publish, missing message keys, oversized payloads,
#    no schema validation before publish, hardcoded topic names.
# ============================================================================

declare -a EVENTLINT_PP_PATTERNS=()

EVENTLINT_PP_PATTERNS+=(
  # PP-001: Fire-and-forget publish (no callback/await on send/publish)
  '\.publish\([^)]*\)[[:space:]]*;[[:space:]]*$|critical|PP-001|Fire-and-forget publish without callback or await|Add await or callback to confirm message delivery before proceeding'

  # PP-002: Missing message key / partition key on produce
  'produce\([[:space:]]*\{[^}]*message[^}]*\}|high|PP-002|Producer send without partition key or message key|Include a partition key to ensure message ordering within a partition'

  # PP-003: Oversized message payload (>1MB literal or large JSON.stringify)
  'JSON\.stringify\([^)]*\)[[:space:]]*\.[[:space:]]*length[[:space:]]*>[[:space:]]*1[0-9]{6}|medium|PP-003|Oversized message payload check detected (>1MB threshold)|Keep messages small; use claim-check pattern for large payloads'

  # PP-004: No schema validation before publish
  'publish\([[:space:]]*\{[[:space:]]*topic|medium|PP-004|Message published without schema validation step|Validate message against schema registry before publishing to prevent poison messages'

  # PP-005: Hardcoded topic/queue name string in publish
  'publish\([[:space:]]*["\x27][a-z][a-z._-]+["\x27]|medium|PP-005|Hardcoded topic or queue name in publish call|Use configuration or constants for topic names to enable environment portability'

  # PP-006: Missing correlation ID in message payload
  'publish\([[:space:]]*\{[^}]*body[[:space:]]*:|medium|PP-006|Message published without correlation ID field|Include correlationId in message headers for distributed tracing and debugging'

  # PP-007: No retry on publish failure
  '\.send\([^)]*\)[[:space:]]*\.catch\([[:space:]]*\(\)|high|PP-007|Publish failure caught but no retry logic implemented|Add retry with exponential backoff for transient publish failures'

  # PP-008: Publish without message ID field
  'emit\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*\{|medium|PP-008|Event emitted without unique message ID|Include a unique messageId (UUID) for deduplication and traceability'

  # PP-009: Missing timestamp in event payload
  'publish\([[:space:]]*\{[^}]*type[[:space:]]*:[^}]*\}[[:space:]]*\)|medium|PP-009|Event published without timestamp field|Add a timestamp (ISO 8601) to every event for ordering and debugging'

  # PP-010: No error handling on send/produce call
  '\.send\([^)]*\)[[:space:]]*$|high|PP-010|Message send call without error handling|Wrap send in try/catch or attach error callback to handle delivery failures'

  # PP-011: Synchronous publish inside async handler
  'async[[:space:]].*\.publishSync\(|medium|PP-011|Synchronous publish call inside async handler|Use async publish to avoid blocking the event loop in async contexts'

  # PP-012: Publish without content-type or serialization format
  'sendMessage\([[:space:]]*\{[^}]*Body[[:space:]]*:|low|PP-012|Message sent without explicit content-type header|Set content-type header (application/json, avro, protobuf) for consumer deserialization'

  # PP-013: Missing event type field in published message
  'channel\.sendToQueue\([^,]*,[[:space:]]*Buffer\.from|medium|PP-013|Message sent to queue without event type field|Include an eventType field for consumers to route and filter messages correctly'

  # PP-014: No publish confirmation (acks=0 or no waitForAck)
  'acks[[:space:]]*:[[:space:]]*0|critical|PP-014|Producer acknowledgment disabled (acks=0) -- messages may be lost|Set acks to 1 or all to ensure broker confirms message receipt'

  # PP-015: Batch publish without per-message error handling
  'sendBatch\([[:space:]]*\[[^]]*\]\)|high|PP-015|Batch publish without per-message error handling|Handle errors individually per message in batch to identify failed deliveries'
)

# ============================================================================
# 2. CONSUMER PATTERNS (CP-001 through CP-015)
#    Detects missing idempotency, auto-ack without processing, unbounded
#    batch sizes, missing consumer group, blocking handlers.
# ============================================================================

declare -a EVENTLINT_CP_PATTERNS=()

EVENTLINT_CP_PATTERNS+=(
  # CP-001: No idempotency check on message consume
  'on\([[:space:]]*["\x27]message["\x27][[:space:]]*,[[:space:]]*async[[:space:]]*\(|high|CP-001|Consumer handler without idempotency check|Add idempotency check using messageId or deduplication key before processing'

  # CP-002: Missing offset commit strategy (auto.commit without explicit config)
  'autoCommit[[:space:]]*:[[:space:]]*true|high|CP-002|Auto-commit enabled without explicit offset strategy|Use manual commit after successful processing to prevent message loss on failure'

  # CP-003: Auto-ack without processing confirmation
  'noAck[[:space:]]*:[[:space:]]*true|critical|CP-003|Auto-acknowledge enabled -- messages acknowledged before processing|Set noAck to false and manually ack after successful processing'

  # CP-004: Unbounded consumer prefetch/batch size
  'prefetchCount[[:space:]]*:[[:space:]]*0|high|CP-004|Unbounded prefetch count (0 means unlimited)|Set prefetchCount to a reasonable limit (10-100) to prevent memory exhaustion'

  # CP-005: Missing consumer group ID
  'subscribe\([[:space:]]*\{[^}]*topic|medium|CP-005|Consumer subscribing without explicit consumer group configuration|Set groupId to enable load balancing and offset tracking across consumer instances'

  # CP-006: No graceful shutdown handler for consumer
  'consumer\.run\([[:space:]]*\{|medium|CP-006|Consumer started without graceful shutdown handler|Add SIGTERM/SIGINT handlers to disconnect consumer and commit offsets before exit'

  # CP-007: Blocking synchronous operation in consumer handler
  'readFileSync\([^)]*\).*on\([[:space:]]*["\x27]message|high|CP-007|Blocking synchronous I/O in consumer message handler|Use async I/O in message handlers to avoid blocking the consumer event loop'

  # CP-008: No consumer heartbeat configuration
  'new[[:space:]]Kafka\([[:space:]]*\{[^}]*brokers|low|CP-008|Kafka consumer created without explicit heartbeat configuration|Configure heartbeatInterval and sessionTimeout for consumer group stability'

  # CP-009: Missing consumer error handler
  'consumer\.run\([[:space:]]*\{[[:space:]]*eachMessage|medium|CP-009|Consumer run without error handler callback|Add error handling via consumer.on(CRASH) or try/catch in eachMessage handler'

  # CP-010: Single-threaded consumer bottleneck
  'eachMessage[[:space:]]*:[[:space:]]*async[[:space:]]*\([[:space:]]*\{[[:space:]]*message[[:space:]]*\}|low|CP-010|Single-threaded message processing may be a bottleneck|Consider eachBatch or parallel processing with concurrency limit for throughput'

  # CP-011: No consumer concurrency limit
  'eachBatch[[:space:]]*:[[:space:]]*async[[:space:]]*\(|low|CP-011|Batch consumer without visible concurrency limit|Configure partitionsConsumedConcurrently to control parallel processing'

  # CP-012: Missing message deserialization error handling
  'JSON\.parse\([[:space:]]*message\.value|high|CP-012|Message deserialization without error handling|Wrap JSON.parse in try/catch to handle malformed messages gracefully'

  # CP-013: Consumer without retry policy
  'channel\.consume\([^,]*,[[:space:]]*async[[:space:]]*\(|medium|CP-013|Consumer handler without retry policy for failed messages|Implement retry with backoff before sending failed messages to dead letter queue'

  # CP-014: No consumer lag alerting configuration
  'groupId[[:space:]]*:[[:space:]]*["\x27][^"]*["\x27]|low|CP-014|Consumer group configured without lag monitoring mention|Set up consumer lag alerting to detect processing delays before they become critical'

  # CP-015: Processing without transaction or atomicity guarantee
  'eachMessage.*await[[:space:]]db\.|medium|CP-015|Message processing with database write lacks transactional guarantee|Use transactional processing: commit offset only after DB transaction succeeds'
)

# ============================================================================
# 3. MESSAGE SCHEMA (MS-001 through MS-015)
#    Detects missing schema registry, unversioned schemas, raw string
#    serialization, loose typing, no backward compatibility.
# ============================================================================

declare -a EVENTLINT_MS_PATTERNS=()

EVENTLINT_MS_PATTERNS+=(
  # MS-001: No schema registry integration (publish raw JSON)
  'JSON\.stringify\([^)]*\)[[:space:]]*\)[[:space:]]*;|medium|MS-001|Message serialized as raw JSON without schema registry validation|Integrate schema registry (Confluent, AWS Glue) to enforce message contracts'

  # MS-002: Breaking schema change -- removing a required field
  'delete[[:space:]][[:alnum:]_]*\.required[[:alnum:]_]*|critical|MS-002|Potential breaking schema change -- deleting a required field|Use schema evolution: deprecate fields instead of removing to maintain backward compat'

  # MS-003: Unversioned event schema (no version field in message)
  'eventType[[:space:]]*:[[:space:]]*["\x27][^"]*["\x27][[:space:]]*[,}]|medium|MS-003|Event type defined without schema version field|Add schemaVersion field to every event for forward and backward compatibility'

  # MS-004: Raw string message body (not structured format)
  'Buffer\.from\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*\)|medium|MS-004|Raw string serialized to buffer (not structured format)|Use structured serialization (JSON, Avro, Protobuf) for schema evolution support'

  # MS-005: Missing event type or version field in message constructor
  'new[[:space:]][A-Z][[:alnum:]]*Event\([[:space:]]*\{[^}]*\}|low|MS-005|Event constructor without visible type and version fields|Include eventType and version in every event for routing and compatibility'

  # MS-006: Loose typing with any/unknown in event payload type
  'payload[[:space:]]*:[[:space:]]*any|high|MS-006|Event payload typed as any -- no compile-time schema enforcement|Define strict TypeScript interfaces or use code-generated types from schema registry'

  # MS-007: Schema validation explicitly disabled
  'schemaValidation[[:space:]]*:[[:space:]]*false|critical|MS-007|Schema validation explicitly disabled -- poison messages may propagate|Enable schema validation to prevent malformed messages from entering the pipeline'

  # MS-008: No backward compatibility check in schema evolution
  'compatibility[[:space:]]*:[[:space:]]*["\x27]NONE["\x27]|high|MS-008|Schema compatibility set to NONE -- breaking changes will not be caught|Set compatibility to BACKWARD or FULL to prevent consumer failures on schema changes'

  # MS-009: Hardcoded schema version number
  'schemaVersion[[:space:]]*:[[:space:]]*[0-9]+|low|MS-009|Hardcoded schema version number in code|Reference schema version from registry or config to centralize version management'

  # MS-010: Missing schema documentation (no description field)
  'avsc[[:space:]]*=[[:space:]]*\{[^}]*name[[:space:]]*:|low|MS-010|Avro schema defined without description or documentation field|Add doc field to Avro schemas for developer discoverability and documentation'

  # MS-011: Schema defined inline in code instead of registry
  'schema[[:space:]]*=[[:space:]]*\{[[:space:]]*type[[:space:]]*:[[:space:]]*["\x27]record["\x27]|medium|MS-011|Schema defined inline in code instead of external schema registry|Move schema definitions to schema registry for centralized governance and versioning'

  # MS-012: No schema evolution strategy defined
  'avro\.Type\.forSchema\([[:space:]]*\{|low|MS-012|Avro schema loaded without evolution strategy configuration|Define schema compatibility strategy (BACKWARD, FORWARD, FULL) for safe evolution'

  # MS-013: Breaking change -- new required field without default
  'required[[:space:]]*:[[:space:]]*\[[^\]]*["\x27][a-z][[:alnum:]_]*["\x27]|medium|MS-013|Required fields list may include new fields without defaults (breaking)|New required fields must have default values for backward compatibility'

  # MS-014: JSON message without JSON Schema validation
  'JSON\.parse\([[:space:]]*message|medium|MS-014|JSON message consumed without JSON Schema validation step|Validate incoming JSON messages against schema before processing'

  # MS-015: Mixed serialization formats across topics
  'protobuf.*JSON\.stringify|high|MS-015|Mixed serialization formats detected (protobuf and JSON)|Standardize on a single serialization format per topic or use schema registry'
)

# ============================================================================
# 4. ERROR & DEAD LETTER (ED-001 through ED-015)
#    Detects missing DLQ configuration, no poison message handling, infinite
#    redelivery, DLQ without alerting, swallowed consumer exceptions.
# ============================================================================

declare -a EVENTLINT_ED_PATTERNS=()

EVENTLINT_ED_PATTERNS+=(
  # ED-001: Missing dead letter queue configuration
  'channel\.consume\([^)]*\)[[:space:]]*;[[:space:]]*$|high|ED-001|Consumer configured without dead letter queue|Configure a dead letter queue for messages that fail processing after max retries'

  # ED-002: No poison message handling (parse error ignored)
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*console\.log|high|ED-002|Poison message error logged but not handled (no DLQ routing)|Route unparseable messages to dead letter queue instead of just logging'

  # ED-003: Infinite redelivery loop (no max retry count)
  'channel\.nack\([^,]*,[[:space:]]*false,[[:space:]]*true|critical|ED-003|Message nack with requeue=true but no max retry limit|Track retry count in headers; route to DLQ after max retries to prevent infinite loop'

  # ED-004: DLQ without alerting or monitoring
  'deadLetter[[:space:]]*:[[:space:]]*["\x27][^"]*["\x27]|medium|ED-004|Dead letter queue configured without alerting mention|Set up alerts on DLQ depth to detect processing failures before they accumulate'

  # ED-005: No error event publication on processing failure
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*channel\.ack|high|ED-005|Processing error caught but message acked without error event|Publish error event or route to DLQ before acknowledging failed message'

  # ED-006: Swallowed consumer exception (empty catch)
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|critical|ED-006|Consumer exception swallowed in empty catch block|Log error, increment failure metric, and route message to DLQ on failure'

  # ED-007: Missing max retry count on message consumption
  'retryCount[[:space:]]*<[[:space:]]*[0-9]{3,}|high|ED-007|Excessive retry count on consume (100+ retries)|Limit retries to 3-5 attempts then route to DLQ for investigation'

  # ED-008: No DLQ consumer for reprocessing failed messages
  'deadLetterQueue[[:space:]]*=[[:space:]]*["\x27][^"]*["\x27]|low|ED-008|Dead letter queue defined but no reprocessing consumer visible|Implement a DLQ consumer to inspect, fix, and replay failed messages'

  # ED-009: Error without original message context
  'catch.*throw[[:space:]]new[[:space:]]Error\([[:space:]]*["\x27]|medium|ED-009|Error thrown without original message context or metadata|Include original message ID, topic, and partition in error for debugging'

  # ED-010: Missing error classification (transient vs permanent)
  'catch.*retry\(\)|medium|ED-010|Error handling without classifying transient vs permanent failures|Classify errors: retry transient (network, timeout); DLQ permanent (validation, schema)'

  # ED-011: No circuit breaker on consumer external calls
  'eachMessage.*await[[:space:]]fetch\(|high|ED-011|Consumer calls external service without circuit breaker|Add circuit breaker to prevent cascading failures when downstream services are down'

  # ED-012: Failed message processing without logging
  'channel\.nack\([^)]*\)[[:space:]]*;[[:space:]]*$|medium|ED-012|Message nacked without logging failure details|Log message ID, error details, and retry count before nacking for debugging'

  # ED-013: Missing DLQ TTL or cleanup policy
  'x-dead-letter-exchange[[:space:]]*:[[:space:]]*["\x27]|low|ED-013|Dead letter exchange configured without TTL or cleanup policy|Set message TTL and queue length limit on DLQ to prevent unbounded growth'

  # ED-014: No manual retry mechanism for DLQ messages
  'dlq[[:space:]]*=[[:space:]]*new[[:space:]]|low|ED-014|DLQ instantiated without manual retry or replay mechanism|Implement DLQ dashboard or CLI tool for inspecting and replaying failed messages'

  # ED-015: Error handler silently drops message
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]*;|critical|ED-015|Error handler silently drops message without logging or DLQ|Never silently drop messages; log, metric, and route to DLQ on unrecoverable failure'
)

# ============================================================================
# 5. ORDERING & DELIVERY (OD-001 through OD-015)
#    Detects missing ordering guarantees, no deduplication, dual-write
#    problems, missing outbox pattern, no exactly-once semantics.
# ============================================================================

declare -a EVENTLINT_OD_PATTERNS=()

EVENTLINT_OD_PATTERNS+=(
  # OD-001: No ordering guarantee on dependent events
  'publish\([[:space:]]*["\x27][[:alnum:]_.]*["\x27][[:space:]]*,[[:space:]]*\{[^}]*\}[[:space:]]*\)[[:space:]]*;[[:space:]]*publish\(|high|OD-001|Multiple events published without ordering guarantee|Use partition key or sequence number to ensure dependent events are processed in order'

  # OD-002: Missing deduplication mechanism on consumer
  'eachMessage[[:space:]]*:[[:space:]]*async[[:space:]]*\([[:space:]]*\{|medium|OD-002|Message consumer without deduplication mechanism|Implement idempotency using messageId-based deduplication cache or database constraint'

  # OD-003: Eventual consistency without compensation logic
  'publish.*await[[:space:]]db\.save|medium|OD-003|Event published after DB save without compensation for publish failure|Implement saga pattern with compensating transactions for consistency on failure'

  # OD-004: Saga without timeout or deadline
  'saga[[:space:]]*=[[:space:]]*new[[:space:]]|high|OD-004|Saga orchestration without visible timeout or deadline|Set saga timeout to prevent indefinitely hanging distributed transactions'

  # OD-005: Missing event sourcing snapshot strategy
  'eventStore\.append\(|low|OD-005|Event store append without snapshot strategy mention|Implement periodic snapshots to prevent unbounded event replay on aggregate load'

  # OD-006: Out-of-order timestamp handling
  'createdAt[[:space:]]*>[[:space:]]*message\.timestamp|medium|OD-006|Timestamp comparison suggests out-of-order message handling|Use vector clocks or sequence numbers instead of timestamps for ordering'

  # OD-007: No idempotency key in published message
  'send\([[:space:]]*\{[^}]*topic[[:space:]]*:[^}]*\}|medium|OD-007|Message sent without idempotency key for consumer deduplication|Include unique idempotencyKey in message headers for exactly-once processing'

  # OD-008: Missing sequence number in event payload
  'emit\([[:space:]]*["\x27]event["\x27]|low|OD-008|Event emitted without sequence number for ordering|Add monotonic sequence number to events for gap detection and ordering'

  # OD-009: Publish before DB commit (dual-write problem)
  'publish\([^)]*\)[[:space:]]*;[[:space:]]*await[[:space:]]db\.|critical|OD-009|Event published before database commit (dual-write problem)|Use transactional outbox pattern: write event to outbox table then publish from outbox'

  # OD-010: No transactional outbox pattern
  'await[[:space:]]db\.save.*publish\(|high|OD-010|DB save and event publish without transactional outbox pattern|Implement outbox pattern: save event to DB in same transaction, publish from outbox relay'

  # OD-011: Missing exactly-once semantics configuration
  'enable\.idempotence[[:space:]]*:[[:space:]]*false|high|OD-011|Kafka idempotence disabled -- duplicate messages may occur|Set enable.idempotence to true for exactly-once producer semantics'

  # OD-012: Event replay without idempotency guard
  'replay\([[:space:]]*events|medium|OD-012|Event replay function without idempotency guard|Ensure replay consumer checks for already-processed events to prevent side-effect duplication'

  # OD-013: Race condition on concurrent event processing
  'Promise\.all\([[:space:]]*\[.*eachMessage|high|OD-013|Concurrent message processing without ordering or lock mechanism|Use partition-based ordering or distributed lock for messages requiring sequential processing'

  # OD-014: Missing causation ID chain in published event
  'publish\([[:space:]]*\{[^}]*eventType[[:space:]]*:|low|OD-014|Published event without causationId or parentEventId|Include causationId linking to triggering event for full event lineage tracking'

  # OD-015: Concurrent consumers on ordered topic without partition awareness
  'consumer\.run.*partitionsConsumedConcurrently[[:space:]]*:[[:space:]]*[2-9]|medium|OD-015|Multiple concurrent consumers without partition-based ordering guarantee|Ensure ordering-sensitive topics use single consumer per partition or ordering key'
)

# ============================================================================
# 6. EVENT OBSERVABILITY (EO-001 through EO-015)
#    Detects missing tracing, no consumer lag monitoring, missing metrics,
#    no event catalog, missing audit trail.
# ============================================================================

declare -a EVENTLINT_EO_PATTERNS=()

EVENTLINT_EO_PATTERNS+=(
  # EO-001: Missing event tracing (no trace/span ID in message)
  'publish\([[:space:]]*\{[^}]*body[[:space:]]*:[^}]*\}[[:space:]]*\)|medium|EO-001|Event published without trace ID or span ID in headers|Propagate trace context (W3C traceparent) in message headers for distributed tracing'

  # EO-002: No consumer lag monitoring setup
  'consumer\.connect\(\)|low|EO-002|Consumer connection without lag monitoring configuration|Set up consumer lag monitoring (Burrow, Kafka Exporter) to detect processing delays'

  # EO-003: Missing publish/consume metrics
  'eachMessage[[:space:]]*:[[:space:]]*async|low|EO-003|Message processing without publish/consume metrics instrumentation|Add metrics: messages_published_total, messages_consumed_total, processing_duration_ms'

  # EO-004: No event flow documentation
  'subscribe\([[:space:]]*\{[[:space:]]*topics[[:space:]]*:|low|EO-004|Topic subscription without event flow documentation reference|Document event flows with AsyncAPI spec or event catalog for team discoverability'

  # EO-005: Missing event catalog or registry reference
  'new[[:space:]]Kafka\([[:space:]]*\{[^}]*clientId|low|EO-005|Kafka client without event catalog or registry reference|Maintain an event catalog documenting all topics, schemas, producers, and consumers'

  # EO-006: No schema compatibility check in CI pipeline
  'register[[:space:]]*Schema\(|low|EO-006|Schema registration without CI-level compatibility check|Add schema compatibility check in CI pipeline before deploying schema changes'

  # EO-007: Missing event audit trail
  'channel\.ack\([^)]*\)[[:space:]]*;[[:space:]]*$|medium|EO-007|Message acknowledged without audit trail or processing log|Log message processing outcome (success/failure, duration, messageId) for audit compliance'

  # EO-008: No dead letter queue dashboard or visibility
  'x-dead-letter-routing-key|low|EO-008|Dead letter routing configured without dashboard or monitoring mention|Create DLQ dashboard showing failed messages, error types, and retry history'

  # EO-009: Consumer group without monitoring
  'groupId[[:space:]]*:[[:space:]]*["\x27][[:alnum:]_-]+["\x27]|low|EO-009|Consumer group defined without monitoring or alerting reference|Monitor consumer group health: rebalances, lag, member count, and error rates'

  # EO-010: Missing end-to-end latency tracking
  'producer\.send\([[:space:]]*\{|medium|EO-010|Producer send without end-to-end latency tracking mechanism|Record publish timestamp in message headers and measure consumer-side processing latency'

  # EO-011: No message throughput metrics
  'consumer\.run\([[:space:]]*\{[[:space:]]*eachBatch|low|EO-011|Batch consumer without throughput metrics instrumentation|Track messages_per_second, batch_size, and batch_processing_duration metrics'

  # EO-012: Event processing without structured logging
  'console\.log\([^)]*message|medium|EO-012|Event processing uses console.log instead of structured logging|Use structured logging (JSON format) with messageId, topic, partition, and offset fields'

  # EO-013: Missing event lineage tracking
  'publish\([[:space:]]*\{[^}]*source[[:space:]]*:|low|EO-013|Event source field present but no full lineage tracking|Track full event lineage: source, causationId, correlationId for end-to-end traceability'

  # EO-014: No alerting on processing failures
  'catch[[:space:]]*\([[:space:]]*err[[:space:]]*\)[[:space:]]*\{[[:space:]]*console\.error|medium|EO-014|Processing failure logged to console without alerting integration|Integrate error alerting (PagerDuty, OpsGenie, Slack) for consumer processing failures'

  # EO-015: Missing event replay capability
  'consumer\.seek\(|low|EO-015|Consumer seek used without documented replay capability|Document event replay procedures and test replay with idempotency guards regularly'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
eventlint_pattern_count() {
  local count=0
  count=$((count + ${#EVENTLINT_PP_PATTERNS[@]}))
  count=$((count + ${#EVENTLINT_CP_PATTERNS[@]}))
  count=$((count + ${#EVENTLINT_MS_PATTERNS[@]}))
  count=$((count + ${#EVENTLINT_ED_PATTERNS[@]}))
  count=$((count + ${#EVENTLINT_OD_PATTERNS[@]}))
  count=$((count + ${#EVENTLINT_EO_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
eventlint_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_eventlint_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_eventlint_patterns_for_category() {
  local category="$1"
  case "$category" in
    PP|pp) echo "EVENTLINT_PP_PATTERNS" ;;
    CP|cp) echo "EVENTLINT_CP_PATTERNS" ;;
    MS|ms) echo "EVENTLINT_MS_PATTERNS" ;;
    ED|ed) echo "EVENTLINT_ED_PATTERNS" ;;
    OD|od) echo "EVENTLINT_OD_PATTERNS" ;;
    EO|eo) echo "EVENTLINT_EO_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_eventlint_category_label() {
  local category="$1"
  case "$category" in
    PP|pp) echo "Producer Patterns" ;;
    CP|cp) echo "Consumer Patterns" ;;
    MS|ms) echo "Message Schema" ;;
    ED|ed) echo "Error & Dead Letter" ;;
    OD|od) echo "Ordering & Delivery" ;;
    EO|eo) echo "Event Observability" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_eventlint_categories() {
  echo "PP CP MS ED OD EO"
}

# Get categories available for a given tier level
# free=0 -> PP, CP (30 patterns)
# pro=1  -> PP, CP, MS, ED (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_eventlint_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "PP CP MS ED OD EO"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "PP CP MS ED"
  else
    echo "PP CP"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
eventlint_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in PP CP MS ED OD EO; do
      eventlint_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_eventlint_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_eventlint_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_eventlint_category() {
  local category="$1"
  case "$category" in
    PP|pp|CP|cp|MS|ms|ED|ed|OD|od|EO|eo) return 0 ;;
    *) return 1 ;;
  esac
}
