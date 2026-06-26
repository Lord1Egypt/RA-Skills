---
name: cm-avro-schema-manager
description: Manage Apache Avro schemas — validate structure, check forward/backward compatibility, plan schema evolution, audit namespace conventions, and generate code stubs. Works with Confluent Schema Registry, AWS Glue Schema Registry, or standalone .avsc files. Use when asked to review Avro schemas, check schema compatibility, plan schema migration, validate .avsc files, audit schema registry, or generate Avro code. Triggers on "avro", "avro schema", "schema registry", "schema compatibility", "schema evolution", ".avsc", "avsc", "confluent schema registry", "schema migration", "backward compatible", "forward compatible", "avro namespace", "serialization schema".
metadata:
  tags: ["avro", "schema", "schema-registry", "data-engineering", "serialization", "kafka", "compatibility", "data-contracts", "streaming", "data-governance"]
---

# Avro Schema Manager

Manage Apache Avro schemas across your data platform. Validates schema structure, checks forward/backward compatibility for safe evolution, audits namespace conventions, reviews schema registry configuration, and generates language-specific code stubs. Acts as a senior data engineer ensuring schema quality and safe evolution.

## Usage

**Basic:** `Validate the Avro schemas in /path/to/schemas/`
**Focused:** `Check compatibility between schema v3 and v4` | `Review namespace conventions` | `Generate Java POJOs from this schema` | `Plan migration for adding a field`

## How It Works

### Step 1: Discover Schema Files

```bash
find /path/to/project -name "*.avsc" -o -name "*.avdl" -o -name "*.avpr"
grep -r "schema.registry.url" /path/to/project --include="*.properties"
grep -rl "avro.schema\|AvroSchema\|fastavro" /path/to/project --include="*.py" --include="*.java"
```

Parses schema type (record, enum, fixed), namespace/name, fields with types/defaults/docs, logical types (date, timestamp, decimal, uuid), complex types (unions, arrays, maps), and cross-schema references.

### Step 2: Validate Schema Structure

```
Schema Validation: UserEvent (com.company.events.user)
  PASS: Valid record with namespace and documentation
  PASS: All fields have doc strings
  PASS: Logical types correct (timestamp-millis)
  PASS: Nullable fields use ["null", "string"] with default null
  WARN: event_id could use logicalType: uuid for semantic clarity
  WARN: Enum "EventType" is inline — extract to separate .avsc for reuse

Schema Validation: OrderCreated (com.company.events.order)
  FAIL: Nullable field wrong union order
    "discount_code": ["string", "null"]
    FIX: ["null", "string"], default: null (null-first convention)

  FAIL: Missing default on nullable field "referral_source"
    Type ["null", "string"] but no default — old producers cause errors
    FIX: Add "default": null

  FAIL: "amount" is bytes without logical type
    FIX: {"type": "bytes", "logicalType": "decimal", "precision": 10, "scale": 2}

  FAIL: Mixed naming — "firstName" vs snake_case elsewhere
    FIX: "first_name" with alias: {"aliases": ["firstName"]}

  WARN: 4/8 fields missing documentation
```

### Step 3: Check Schema Compatibility

```
Compatibility Analysis: UserEvent v3 -> v4 (mode: BACKWARD)

  1. ADD "device_type" (string, default: "unknown")
     BACKWARD: YES | FORWARD: YES | FULL: YES

  2. REMOVE "legacy_flag"
     BACKWARD: YES (consumers use default) | FORWARD: NO
     RISK: Consumers still reading legacy_flag get default/null
     ACTION: Verify no consumer depends on this field

  3. MODIFY "user_id": int -> long
     BACKWARD: NO | FORWARD: NO | FULL: NO
     BREAKING CHANGE — deserialization failures guaranteed
     FIX: Two-phase migration:
       Phase 1: Add "user_id_v2" (long), keep "user_id" (int)
       Phase 2: Migrate all consumers to user_id_v2
       Phase 3: Remove "user_id" in future version

  4. ADD enum symbol "REFUND" to EventType
     BACKWARD: YES | FORWARD: NO
     RISK: Consumers without default case in switch/match will throw

  VERDICT: FAIL — Schema Registry will REJECT under BACKWARD mode
  BLOCKING: Change 3 (type widening) must be resolved first
```

### Step 4: Audit Namespace Conventions

```
  8 namespaces found

  FAIL: "UserActivity" has no namespace — collision risk, default package
    FIX: Add namespace "com.company.events.user"

  FAIL: Inconsistent prefix: "events.user" vs "com.company.events.user"
    FIX: Standardize to com.company.<domain>.<subdomain>

  FAIL: "Config" uses too-broad "com.company"
    FIX: Use "com.company.common" or "com.company.config"

  FAIL: Schema "OrderItem" references "com.company.model.Product"
    but no .avsc file defines it — unversioned dependency
    FIX: Keep all schema files in repository

  RECOMMEND: Document namespace convention:
    com.company.events.*  (event schemas)
    com.company.model.*   (data model schemas)
    com.company.common    (shared types)
```

### Step 5: Review Schema Registry

```
  Confluent Schema Registry | 34 subjects | 127 versions
  Global compatibility: BACKWARD

  WARN: "internal-logs-value" set to NONE — any change accepted
    RISK: Breaking changes reach prod. FIX: Set BACKWARD minimum

  PASS: "payment-events-value" uses BACKWARD_TRANSITIVE
    Checks against ALL prior versions — good for critical data

  FAIL: 3 subjects with non-standard naming
    "UserEvent" (no -value suffix), "order.created.v2" (dots + version)
    FIX: Standardize to TopicNameStrategy: <topic>-key, <topic>-value

  WARN: "order-events-value" has 8 versions — review if all consumed
    Soft-delete unused versions after consumer migration

  FAIL: No schema validation in CI/CD
    FIX: Add PR gate check:
      curl -X POST schema-registry/compatibility/subjects/<sub>/versions/latest
      Block merge if compatibility fails
```

### Step 6: Plan Schema Evolution

```
  Safe path for adding "payment_method" to OrderCreated:

  Step 1: Add as nullable with default
    {"name": "payment_method", "type": ["null", "string"], "default": null}
    Compatible in ALL modes. Old producers: consumers get null.

  Step 2: Register new version — compatibility check passes
  Step 3: Deploy producers that populate the field
  Step 4: (Optional future) Make required — ONLY after all producers send it

  DANGEROUS changes requiring special handling:
    Rename field: NEVER directly — use aliases instead
    Change type: Add new field with new type, deprecate old
    Remove enum symbol: NEVER — prefix with DEPRECATED_ instead
    Reorder fields: SAFE in Avro (name-based), may break raw byte consumers
```

### Step 7: Code Generation Guidance

```
  Java: avro-maven-plugin generates SpecificRecord classes
  Python: fastavro parse_schema() + writer/reader
  TypeScript: avsc.Type.forSchema() for encoder/decoder
  Go: github.com/linkedin/goavro/v2 codec from schema JSON

  RECOMMEND: Automate in CI/CD build step
    avro-tools compile schema src/main/avro target/generated
    Never hand-edit generated classes
```

### Step 8: Final Report

```
# Avro Schema Management Report

## Overall Health Score: 61/100
  Schema structure: 7/10     Field conventions: 5/10
  Compatibility: 6/10        Namespaces: 4/10
  Registry config: 6/10      Evolution practices: 5/10
  CI/CD integration: 3/10    Documentation: 5/10

## Critical Issues
  1. int->long type change on user_id — BREAKING, registry rejects
  2. "UserActivity" has no namespace — collision risk
  3. No CI/CD compatibility validation
  4. Referenced schema "Product" not in repository
  5. Nullable field with wrong union order — deserialization risk

## High Priority
  6. Non-standard subject naming (3 subjects)
  7. "internal-logs" compatibility set to NONE
  8. No code generation automation
  9. Inline enums preventing cross-schema reuse
  10. 30% of fields missing documentation
```

## Output

- **Per-schema validation** with field-level checks and fixes
- **Compatibility matrix** for forward/backward/full between versions
- **Namespace audit** for organizational consistency
- **Registry review** covering config, naming, per-subject policies
- **Evolution plan** with safe migration steps for requested changes
- **Code generation** guidance for Java, Python, TypeScript, Go
- **Health score** 0-100 with per-category breakdown

## Tips for Best Results

- Point the agent at your schema directory (where .avsc files live)
- Provide both old and new schema versions for compatibility checks
- Specify compatibility mode needed (BACKWARD, FORWARD, FULL)
- Include consumer/producer code for skew detection
- Run before any schema change deployment as a gate check
