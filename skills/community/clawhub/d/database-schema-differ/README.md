# Database Schema Differ

Compare database schemas across environments, generate migration scripts, and track schema evolution.

## Features

- Compare schemas between databases, SQL files, or schema snapshots
- Generate SQL migration scripts (up/down) for schema changes
- Detect schema drift between environments
- Support for PostgreSQL, MySQL, SQLite, and other databases via SQLAlchemy
- Multiple output formats (SQL, JSON, HTML visual diff)
- Schema snapshotting for historical comparison

## Quick Start

```bash
# Compare two databases
python3 scripts/main.py compare postgresql://user:pass@host1/db postgresql://user:pass@host2/db

# Generate migration from schema differences
python3 scripts/main.py diff schema_v1.sql schema_v2.sql --output migration.sql

# Create schema snapshot
python3 scripts/main.py snapshot postgresql://user:pass@host/db --save snapshot.json

# Check for schema drift in CI
python3 scripts/main.py check-drift --expected expected.json --actual actual.json --fail-on-drift
```

## Installation

This skill requires Python 3.x and SQLAlchemy:

```bash
pip3 install sqlalchemy alembic psycopg2-binary pymysql
```

Database-specific drivers:
- PostgreSQL: `psycopg2-binary`
- MySQL: `pymysql`
- SQLite: Built into Python
- SQL Server: `pyodbc`
- Oracle: `cx_oracle`

## Usage Examples

### Compare development and production
```bash
python3 scripts/main.py compare \
  postgresql://dev:pass@localhost/dev_db \
  postgresql://prod:pass@prod-host/prod_db \
  --output diff.json
```

### Generate visual HTML diff
```bash
python3 scripts/main.py visual-diff schema1.sql schema2.sql --html diff.html
```

### Track schema changes over time
```bash
python3 scripts/main.py history postgresql://user:pass@host/db --days 30 --format timeline
```

## Output Formats

- **Human-readable**: Color-coded terminal output
- **JSON**: Machine-readable for automation
- **SQL**: Ready-to-execute migration scripts
- **HTML**: Interactive visual diff in browser

## Limitations

- Requires database credentials for live comparisons
- Complex changes may need manual review
- Performance may vary with large schemas
- Limited to schema structure (not data comparison)

## License

This skill is part of the OpenClaw Skill Factory portfolio.