# ETL Pipeline Design Patterns

This guide provides patterns for designing and implementing ETL pipelines for knowledge graph construction.

## Extract Stage Patterns

### CSV File Extraction Pattern

```yaml
Pattern: Read CSV files and prepare for transformation

Configuration:
  source_type: csv
  location: /path/to/file.csv
  delimiter: ","
  encoding: utf-8
  header_row: 1

Features:
  - Automatic delimiter detection
  - Header parsing
  - Chunk processing for large files
  - Type inference

When to use:
  ✓ Static CSV files
  ✓ Scheduled batch imports
  ✓ Small to medium datasets
```

### JSON API Extraction Pattern

```yaml
Pattern: Fetch JSON data from REST API with pagination

Configuration:
  source_type: api
  endpoint: https://api.example.com/data
  method: GET
  pagination:
    type: page
    param: page
    page_size: 100
  authentication:
    type: bearer
    token: ${API_TOKEN}

Features:
  - Automatic pagination handling
  - Rate limit respect
  - Connection pooling
  - Response validation

When to use:
  ✓ REST API data sources
  ✓ Regular API polling
  ✓ Real-time data feeds
```

### Database Query Extraction Pattern

```yaml
Pattern: Extract data from SQL/NoSQL databases

Configuration:
  source_type: database
  connection:
    type: postgresql
    host: db.example.com
    port: 5432
    database: source_db
  query: |
    SELECT id, name, email, created_at
    FROM users
    WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
  batch_size: 5000

Features:
  - Connection pooling
  - Query optimization
  - Batch fetching
  - Transaction management

When to use:
  ✓ Database sources
  ✓ Large datasets
  ✓ Complex data requirements
```

### Streaming Data Extraction Pattern

```yaml
Pattern: Consume data from message queues/streams

Configuration:
  source_type: stream
  protocol: kafka|mqtt|pubsub
  broker: kafka.example.com:9092
  topic: events.users
  consumer_group: etl_pipeline
  batch_timeout: 30_seconds

Features:
  - Real-time data consumption
  - Offset tracking
  - Auto-commit handling
  - Backpressure management

When to use:
  ✓ Real-time data
  ✓ Event-driven pipelines
  ✓ Continuous data flows
```

---

## Transform Stage Patterns

### Entity Normalization Pattern

```
Pattern: Standardize entity representations

Operations:
  - name: trim_whitespace
    input: string_field
    output: cleaned_name
  
  - name: case_normalize
    input: name
    case: title_case
  
  - name: special_char_remove
    input: identifier
    chars: ['@', '#', '$']

Example:
  Input:  "  JOHN DOE  "
  Output: "John Doe"
```

### Data Type Conversion Pattern

```yaml
Pattern: Convert data to correct types

Operations:
  - field: birth_date
    from: string (MM/DD/YYYY)
    to: datetime (ISO8601)
    format: "%m/%d/%Y"
  
  - field: age
    from: string
    to: integer
    validation: "0-150"
  
  - field: is_active
    from: string ("Y"/"N")
    to: boolean
    mapping: {"Y": true, "N": false}
```

### Deduplication Pattern

```yaml
Pattern: Remove or merge duplicate records

Strategy: Merge duplicates by ID
  key_field: user_id
  on_duplicate:
    action: merge
    strategy: keep_latest
    timestamp_field: updated_at

Strategy: Exact match deduplication
  fields: [email, phone]
  action: keep_first

Strategy: Fuzzy deduplication
  fields: [name]
  similarity_threshold: 0.95
  algorithm: levenshtein
```

### Schema Mapping Pattern

```yaml
Pattern: Map source schema to target schema

Mappings:
  - source: customer_id
    target: id
    type: string
  
  - source: full_name
    target: name
    transformations:
      - split_on: " "
      - map: 
          index_0: first_name
          index_1: last_name
  
  - source: contact_email
    target: email
    validation: email_format
  
  - source: DOB
    target: birth_date
    format: "MM/DD/YYYY"
    type: date
```

### Enrichment Pattern

```yaml
Pattern: Add contextual data during transformation

Enrichment sources:
  - lookup_external_api:
      field: customer_id
      endpoint: https://api.example.com/customer/{id}
      cache: true
      cache_ttl: 86400
  
  - lookup_reference_table:
      field: country_code
      table: country_lookup
      join_on: code
      fields_to_add: [country_name, region]
  
  - calculate_derived:
      field: customer_tier
      calculation: |
        if lifetime_value >= 10000 then "GOLD"
        elif lifetime_value >= 5000 then "SILVER"
        else "BRONZE"
```

### Validation Pattern

```yaml
Pattern: Validate data quality and consistency

Validations:
  - type: required_fields
    fields: [id, name, email]
    on_failure: skip_record
  
  - type: data_type
    field: age
    expected_type: integer
    on_failure: attempt_conversion
  
  - type: range_validation
    field: price
    min: 0
    max: 999999
    on_failure: log_error
  
  - type: format_validation
    field: email
    pattern: "^[^@]+@[^@]+\\.[^@]+$"
    on_failure: skip_record
  
  - type: referential_integrity
    field: customer_id
    reference_table: customers
    on_failure: flag_orphan
```

---

## Load Stage Patterns

### Bulk Import Pattern

```yaml
Pattern: High-throughput batch loading

Configuration:
  method: bulk_import
  batch_size: 10000
  transaction_size: 50000
  parallelism: 4

Process:
  1. Stage data in intermediate format
  2. Validate batch
  3. Begin transaction
  4. Load batch
  5. Commit transaction
  6. Verify load count
  7. Generate metrics

Advantages:
  - High throughput
  - Low memory usage
  - Transactional guarantee
```

### Streaming Load Pattern

```yaml
Pattern: Real-time incremental loading

Configuration:
  method: streaming
  connection_pool_size: 10
  queue_size: 1000
  flush_interval: 5_seconds

Process:
  1. Open connection
  2. For each record:
     - Queue write operation
     - If queue full: flush
     - If timeout: flush
  3. On pipeline end: flush remaining

Advantages:
  - Low latency
  - Continuous updates
  - Real-time visibility
```

### Merge Pattern

```yaml
Pattern: Update existing data or insert new (UPSERT)

Configuration:
  method: merge
  merge_keys: [id, email]
  on_match:
    - update_properties: true
    - update_timestamp: true
  on_create:
    - set_initial_properties: true
    - set_created_timestamp: true

Example Cypher:
  MERGE (n:Person {email: row.email})
  ON CREATE SET
    n.id = row.id,
    n.created_at = timestamp()
  ON MATCH SET
    n.name = row.name,
    n.updated_at = timestamp()
```

### Delete/Update Pattern

```yaml
Pattern: Handle data deletion and updates

Strategies:
  - soft_delete:
      flag_field: is_deleted
      value_on_delete: true
      restoration: restore by setting false
  
  - hard_delete:
      condition: WHERE record_status = 'ARCHIVED'
      action: DELETE entity
  
  - versioning:
      archive_old: true
      create_version: true
      keep_history: true
```

---

## Error Handling Patterns

### Fail Fast Pattern

```yaml
Pattern: Stop pipeline on first error

Configuration:
  error_handling: fail_fast
  on_error:
    action: stop
    log_level: error
    rollback: true

Use case: Data quality critical, no partial loads acceptable
```

### Fail Safe Pattern

```yaml
Pattern: Continue processing, log errors

Configuration:
  error_handling: fail_safe
  on_error:
    action: log_and_continue
    error_log: /var/log/etl/errors.log
    track_error_records: true
    quarantine_location: /var/data/quarantine/

Post-processing:
  - Review error log
  - Retry failed records
  - Manual intervention if needed
```

### Skip Invalid Records Pattern

```yaml
Pattern: Skip records that fail validation

Configuration:
  on_validation_error:
    action: skip
    log_location: dead_letter_queue.csv
    continue_processing: true

Validation:
  - Check required fields
  - Validate data types
  - Check business rules
  - Skip if any validation fails
```

### Dead Letter Queue Pattern

```yaml
Pattern: Route failed records for later analysis

Configuration:
  dead_letter_queue:
    enabled: true
    location: dlq/failed_records.csv
    fields_to_include:
      - original_record
      - error_message
      - error_timestamp
      - pipeline_run_id
    retention_days: 90

Post-processing:
  1. Analyze DLQ records
  2. Fix data quality issues
  3. Re-process through pipeline
```

---

## Monitoring and Observability Patterns

### Metrics Collection Pattern

```yaml
Pattern: Track pipeline execution metrics

Metrics:
  - extract_stage:
      records_read: counter
      bytes_read: counter
      duration: timer
      errors: counter
  
  - transform_stage:
      records_input: counter
      records_output: counter
      records_skipped: counter
      duration: timer
  
  - load_stage:
      records_loaded: counter
      nodes_created: counter
      edges_created: counter
      duration: timer
  
  - overall:
      success_rate: gauge
      data_quality_score: gauge
      total_duration: timer
```

### Alerting Pattern

```yaml
Pattern: Alert on anomalies

Rules:
  - name: slow_extract
    condition: extract_duration > 300_seconds
    severity: warning
    action: notify_ops
  
  - name: high_error_rate
    condition: error_count/total_records > 0.01
    severity: critical
    action: pause_and_alert
  
  - name: low_data_quality
    condition: validation_failures > 100
    severity: warning
    action: log_and_notify
  
  - name: load_failure
    condition: load_status = FAILED
    severity: critical
    action: immediate_alert
```

### Logging Pattern

```yaml
Pattern: Comprehensive pipeline logging

Log Levels:
  DEBUG:
    - Record-level details
    - Transformation steps
    - Connection info
  
  INFO:
    - Stage completion
    - Record counts
    - Metrics
  
  WARN:
    - Validation failures
    - Skipped records
    - Retries
  
  ERROR:
    - Load failures
    - Connection errors
    - Critical issues

Log Structure:
  timestamp: ISO8601
  pipeline_id: string
  stage: string
  level: string
  message: string
  context: object (additional fields)
```

---

## Performance Optimization Patterns

### Parallelization Pattern

```yaml
Pattern: Process data in parallel

Configuration:
  parallelism: 8
  partition_by: customer_id
  partition_count: 8

Benefits:
  - Increased throughput
  - Better CPU utilization
  - Reduced total runtime

Trade-offs:
  - Increased memory usage
  - Potential ordering issues
  - Complexity in monitoring
```

### Caching Pattern

```yaml
Pattern: Cache expensive lookups

Configuration:
  cache_type: in_memory|redis
  ttl: 86400  # 24 hours
  size_limit: 100000_records

Use cases:
  - Lookup table joins
  - Reference data enrichment
  - API response caching
  - Calculated field caching
```

### Incremental Load Pattern

```yaml
Pattern: Load only changed data

Tracking:
  - delta_method: timestamp
    timestamp_field: modified_at
    last_sync: 2024-04-08T23:59:59Z
  
  - delta_method: change_data_capture
    source: database_cdc_table
    track_operations: [INSERT, UPDATE, DELETE]

Benefits:
  - Reduced data transfer
  - Faster processing
  - Lower resource usage
```

---

## Best Practices

✓ **Idempotency** – Pipelines can be safely rerun  
✓ **Data Lineage** – Track data origins and transformations  
✓ **Quality Gates** – Validate at each stage  
✓ **Monitoring** – Comprehensive visibility  
✓ **Error Handling** – Graceful degradation  
✓ **Documentation** – Clear pipeline specifications  
✓ **Testing** – Test with sample data first  
✓ **Scalability** – Design for growth  
✓ **Security** – Protect credentials and sensitive data  
✓ **Performance** – Optimize resource usage  

---

See [example-pipelines.md](../examples/example-pipelines.md) for complete ETL pipeline implementation examples.


