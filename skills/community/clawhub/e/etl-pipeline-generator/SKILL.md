---
name: etl_pipeline_generator
title: ETL Pipeline Generator
description: Generate automated ETL pipelines for transforming and loading data into graph databases or knowledge graphs.
category: data-ingestion
tags:
  - etl
  - pipeline-orchestration
  - data-workflow
  - data-ingestion
  - graph-loading
  - knowledge-graph
  - automation
  - data-transformation
  - data-quality
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"⚙️","homepage":"https://clawhub.com"}}
---

# ETL Pipeline Generator

**Design automated Extract-Transform-Load pipelines for knowledge graph construction.**

This skill generates structured ETL pipelines that move raw data from various sources into **graph-ready datasets** or **knowledge graph storage systems**. It orchestrates data ingestion, transformation, and loading steps so that messy input data becomes structured graph data.

## Quick Start

### Use When
- Building automated data ingestion workflows
- Designing Extract-Transform-Load pipelines
- Orchestrating multi-step data transformations
- Creating repeatable data pipeline architectures
- Integrating multiple data sources
- Automating knowledge graph population
- Building data quality and validation workflows

### Inputs
- Data source specifications (type, location, format)
- Transformation requirements and rules
- Target system definitions (database, format)
- Data quality requirements
- Pipeline scheduling and monitoring rules
- Error handling and recovery strategies

### Outputs
- Pipeline configuration (YAML)
- Directed Acyclic Graph (DAG) definitions
- Python/Scala/SQL implementation scripts
- Data flow diagrams
- Pipeline documentation
- Monitoring and alerting configurations

## Example

**Simple Customer Data Pipeline:**
```yaml
name: customer_graph_ingestion
description: Ingest customer data into knowledge graph

extract:
  source_type: csv
  source_path: data/customers.csv
  format: csv

transform:
  - normalize_entities
  - detect_relationships
  - validate_schema

load:
  target: neo4j
  database: customer_graph
  method: bulk_import
```

**Generated Pipeline Flow:**
```
Extract CSV → Normalize Entities → Detect Relationships → 
Validate Data → Load to Neo4j → Verify Load
```

## ETL Pipeline Architecture

### 1. Extract Stage

**Purpose:** Retrieve raw data from external sources

**Supported Sources:**
- CSV files
- JSON files
- REST APIs
- Databases (SQL, NoSQL)
- Text documents
- Streaming sources (Kafka, Pub/Sub)
- Data warehouses (Snowflake, BigQuery)

**Configuration:**
```yaml
extract:
  source_type: csv|json|api|database|text|stream
  location: /path/to/file or endpoint
  format: format_specifier
  authentication: credentials (if needed)
  filtering: (optional) filter criteria
```

### 2. Transform Stage

**Purpose:** Convert raw data into graph-ready structures

**Transformation Operations:**
- **Entity Detection** - Identify entity boundaries
- **Relationship Inference** - Discover relationships
- **Schema Mapping** - Map to target schema
- **Data Normalization** - Standardize values
- **Type Conversion** - Convert data types
- **Deduplication** - Remove duplicates
- **Enrichment** - Add contextual data
- **Validation** - Check data quality
- **Filtering** - Remove invalid records

**Example Transform:**
```yaml
transform:
  operations:
    - normalize_entity_names
    - infer_relationships_from_columns
    - convert_dates_to_iso8601
    - deduplicate_entities
    - validate_required_fields
    - enrich_with_external_data
```

### 3. Load Stage

**Purpose:** Load transformed data into target system

**Supported Targets:**
- **Neo4j** - Property graph database
- **RDF Triple Stores** - SPARQL endpoint
- **ArangoDB** - Multi-model database
- **TigerGraph** - Graph database
- **Property Graph Engines** - Generic property graphs
- **CSV/JSON** - File output

**Configuration:**
```yaml
load:
  target: neo4j|rdf|arangodb|tigergraph|property_graph|file
  connection_params:
    host: localhost
    port: 7687
    database: graph_database
  method: bulk_import|streaming|batch
  batch_size: 1000
```

## Pipeline Stages Explained

### Extract Stage Details

**Data Source Connectors:**
```
CSV Extractor
  - delimiter detection
  - header parsing
  - encoding handling
  - chunk processing

JSON Extractor
  - nested object handling
  - array flattening
  - schema inference
  - streaming JSON support

API Extractor
  - authentication handling
  - pagination support
  - rate limiting
  - response transformation

Database Extractor
  - SQL query execution
  - connection pooling
  - partition handling
  - transaction management
```

### Transform Stage Details

**Data Processing Operations:**
```
Normalization
  - case normalization
  - whitespace trimming
  - special character handling
  - URL encoding

Type Conversion
  - string → integer/float
  - string → datetime
  - string → boolean
  - safe type conversions

Deduplication
  - exact match detection
  - fuzzy matching
  - identity resolution
  - merge strategies

Validation
  - required field checks
  - data type validation
  - range validation
  - pattern matching
```

### Load Stage Details

**Data Loading Methods:**
```
Bulk Import
  - CSV nodes/edges files
  - Batch processing
  - High throughput
  - Transactional rollback

Streaming Load
  - Real-time ingestion
  - Event-based
  - Lower latency
  - Connection streaming

Batch Load
  - Scheduled runs
  - Configurable batch sizes
  - Progress tracking
  - Failure recovery
```

## Pipeline Execution Modes

### 1. Synchronous Execution
```
Sequential execution of all stages
Immediate feedback on success/failure
Best for: Small to medium datasets
```

### 2. Asynchronous Execution
```
Non-blocking pipeline execution
Async progress monitoring
Best for: Large datasets, scheduled runs
```

### 3. Streaming Mode
```
Continuous data flow
Real-time processing
Best for: Live data feeds, event streams
```

### 4. Scheduled Execution
```
Cron-based or scheduled triggers
Repeatable, idempotent operations
Best for: Regular data refreshes
```

## Pipeline Monitoring and Observability

### Monitoring Capabilities
- Step execution times
- Data volume metrics (rows in/out)
- Error tracking and logging
- Data quality metrics
- Performance profiling

### Alerting
```yaml
alerts:
  - condition: execution_time > 3600s
    action: notify_admin
  - condition: error_count > 10
    action: pause_pipeline
  - condition: data_quality_score < 0.9
    action: log_warning
```

## Error Handling and Recovery

### Error Handling Strategies
```
Fail Fast: Stop on first error
Fail Safe: Continue with logging
Retry: Exponential backoff retry
Skip: Skip failed records, continue
Dead Letter: Route to error queue
```

### Recovery Mechanisms
```
Checkpoint/Resume: Save state, resume from checkpoint
Rollback: Undo on failure
Compensation: Execute cleanup actions
Retry with Backoff: Automatic retry logic
```

## Output Formats

### YAML Pipeline Configuration
```yaml
name: pipeline_name
description: pipeline description

extract:
  source_type: csv
  location: data/file.csv

transform:
  operations:
    - normalize_entities
    - validate_data

load:
  target: neo4j
  database: my_graph
```

### DAG (Directed Acyclic Graph)
```
Extract(csv) → Parse → Normalize → 
Validate → Deduplicate → Load(Neo4j) → Verify
```

### Python Implementation
```python
def pipeline_execution():
    data = extract_from_csv('data.csv')
    data = normalize_entities(data)
    data = validate_data(data)
    load_to_neo4j(data)
    return verify_load()
```

### Execution Metrics
```json
{
  "pipeline_id": "customer_ingestion_001",
  "start_time": "2024-04-09T10:00:00Z",
  "end_time": "2024-04-09T10:05:30Z",
  "duration_seconds": 330,
  "stages": [
    {"name": "extract", "duration": 45, "records": 10000},
    {"name": "transform", "duration": 120, "records": 9900},
    {"name": "load", "duration": 150, "records": 9900}
  ],
  "status": "SUCCESS"
}
```

## Execution Steps

1. **Validate Pipeline Configuration** – Check all parameters
2. **Initialize Extractors** – Set up data source connections
3. **Execute Extract** – Retrieve raw data
4. **Initialize Transformers** – Prepare transformation engines
5. **Execute Transform** – Apply transformation operations
6. **Validate Transformed Data** – Check data quality
7. **Initialize Loaders** – Set up target connections
8. **Execute Load** – Load data to target system
9. **Verify Load** – Confirm successful loading
10. **Generate Metrics** – Collect execution statistics

## Integration with Other Skills

The ETL Pipeline Generator orchestrates these skills:
- **API Ingestion Connectors** → Extract from APIs
- **CSV Graph Loader Generator** → Transform and load CSVs
- **JSON to Triples Converter** → Transform JSON to RDF
- **Text Entity Relation Extractor** → Extract from text
- **Graph Schema Validation** → Validate loaded data
- **Graph Constraint Generator** → Apply constraints

## Recommended Libraries

- **Orchestration:** Apache Airflow, Prefect, Dagster
- **ETL Processing:** Apache Spark, Pandas, Polars
- **Data Validation:** Great Expectations, Pandera
- **Graph Loaders:** neo4j, rdflib, networkx
- **Scheduling:** APScheduler, Luigi, Celery
- **Monitoring:** Prometheus, Grafana, DataDog

## Best Practices

✓ **Idempotency** – Pipelines can be rerun safely
✓ **Data Validation** – Validate at each stage
✓ **Error Handling** – Graceful error management
✓ **Monitoring** – Track pipeline execution
✓ **Documentation** – Document data lineage
✓ **Testing** – Test with sample data first
✓ **Version Control** – Track pipeline changes
✓ **Scalability** – Design for data growth
✓ **Security** – Secure credentials and data
✓ **Performance** – Optimize transformation logic

## References

See [pipeline-patterns.md](references/pipeline-patterns.md) for detailed ETL pipeline patterns and [example-pipelines.md](examples/example-pipelines.md) for complete real-world pipeline examples.

---

**Version:** 1.0.0
