# Data Pipeline Toolkit

Build ETL pipelines in minutes.

## Features

- **Extract** - APIs, databases, files, streams
- **Transform** - Clean, filter, aggregate, join
- **Load** - Data warehouses, databases, APIs
- **Scheduling** - Cron-based or event-driven
- **Monitoring** - Alerts on failures

## Quick Start

```bash
# Create pipeline
./pipeline.sh create my-pipeline

# Add extract step
./pipeline.sh extract my-pipeline api --url https://api.example.com

# Add transform
./pipeline.sh transform my-pipeline filter "age > 18"

# Add load
./pipeline.sh load my-pipeline postgres --connection $DB_URL

# Run
./pipeline.sh run my-pipeline
```

## Sources

- REST APIs
- GraphQL
- SQL Databases
- CSV/JSON/Parquet files
- S3/Google Cloud Storage
- Kafka/SQS

## Destinations

- PostgreSQL/MySQL
- Snowflake/BigQuery
- S3
- APIs
- Data warehouses

## Requirements

- Python 3.8+
- Docker (optional)

## Author

Sunshine-del-ux
