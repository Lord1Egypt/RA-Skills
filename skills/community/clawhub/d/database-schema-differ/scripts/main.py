#!/usr/bin/env python3
"""
Database Schema Differ
Compare database schemas, generate migration scripts, track schema evolution.
"""

import argparse
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import sys

def parse_sql_file(filename: str) -> Dict[str, List[str]]:
    """Parse SQL file into schema components."""
    if not os.path.exists(filename):
        return {"error": f"File not found: {filename}"}
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Simple SQL parser - extract CREATE statements
    schema = {
        "tables": [],
        "indexes": [],
        "constraints": [],
        "views": [],
        "triggers": [],
    }
    
    # Normalize SQL
    content = content.replace('\n', ' ').replace('\r', ' ')
    
    # Extract CREATE TABLE statements
    table_pattern = r'CREATE TABLE (\w+)\s*\((.*?)\);'
    for match in re.finditer(table_pattern, content, re.IGNORECASE | re.DOTALL):
        table_name = match.group(1)
        table_body = match.group(2)
        schema["tables"].append({
            "name": table_name,
            "definition": f"CREATE TABLE {table_name} ({table_body})",
            "columns": parse_table_columns(table_body)
        })
    
    # Extract CREATE INDEX statements
    index_pattern = r'CREATE (?:UNIQUE )?INDEX (\w+) ON (\w+)\s*\((.*?)\)'
    for match in re.finditer(index_pattern, content, re.IGNORECASE):
        schema["indexes"].append({
            "name": match.group(1),
            "table": match.group(2),
            "columns": match.group(3),
            "definition": match.group(0)
        })
    
    return schema

def parse_table_columns(table_body: str) -> List[Dict[str, str]]:
    """Parse table columns from CREATE TABLE body."""
    columns = []
    # Simple column parsing - split by commas, but handle nested parentheses
    lines = table_body.split(',')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('PRIMARY KEY') or line.startswith('FOREIGN KEY') or line.startswith('CONSTRAINT'):
            continue
        
        # Match column definition: column_name data_type [constraints]
        match = re.match(r'(\w+)\s+([\w\(\)\s]+)(?:\s+(.*))?', line)
        if match:
            columns.append({
                "name": match.group(1),
                "type": match.group(2).strip(),
                "constraints": match.group(3) if match.group(3) else ""
            })
    
    return columns

def compare_schemas(schema1: Dict[str, Any], schema2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two schemas and return differences."""
    differences = {
        "tables_added": [],
        "tables_removed": [],
        "tables_changed": [],
        "indexes_added": [],
        "indexes_removed": [],
        "columns_added": [],
        "columns_removed": [],
        "columns_changed": [],
    }
    
    # Compare tables
    tables1 = {t["name"]: t for t in schema1.get("tables", [])}
    tables2 = {t["name"]: t for t in schema2.get("tables", [])}
    
    # Find added/removed tables
    for table_name in tables2:
        if table_name not in tables1:
            differences["tables_added"].append(table_name)
    
    for table_name in tables1:
        if table_name not in tables2:
            differences["tables_removed"].append(table_name)
    
    # Find changed tables
    for table_name in set(tables1.keys()) & set(tables2.keys()):
        table1 = tables1[table_name]
        table2 = tables2[table_name]
        
        # Compare columns
        cols1 = {c["name"]: c for c in table1.get("columns", [])}
        cols2 = {c["name"]: c for c in table2.get("columns", [])}
        
        for col_name in cols2:
            if col_name not in cols1:
                differences["columns_added"].append(f"{table_name}.{col_name}")
        
        for col_name in cols1:
            if col_name not in cols2:
                differences["columns_removed"].append(f"{table_name}.{col_name}")
        
        for col_name in set(cols1.keys()) & set(cols2.keys()):
            col1 = cols1[col_name]
            col2 = cols2[col_name]
            if col1["type"] != col2["type"] or col1["constraints"] != col2["constraints"]:
                differences["columns_changed"].append(f"{table_name}.{col_name}")
    
    # Compare indexes
    indexes1 = {idx["name"]: idx for idx in schema1.get("indexes", [])}
    indexes2 = {idx["name"]: idx for idx in schema2.get("indexes", [])}
    
    for idx_name in indexes2:
        if idx_name not in indexes1:
            differences["indexes_added"].append(idx_name)
    
    for idx_name in indexes1:
        if idx_name not in indexes2:
            differences["indexes_removed"].append(idx_name)
    
    return differences

def generate_migration(differences: Dict[str, Any], output_format: str = "sql") -> str:
    """Generate migration script from differences."""
    migration = []
    migration.append(f"-- Generated: {datetime.now(timezone.utc).isoformat()}")
    migration.append(f"-- Differences: {sum(len(v) for v in differences.values())} changes")
    migration.append("")
    
    if output_format == "sql":
        migration.append("-- UP Migration")
        
        # Add tables
        for table in differences["tables_added"]:
            migration.append(f"-- TODO: Add CREATE TABLE statement for {table}")
            migration.append(f"CREATE TABLE {table} (")
            migration.append(f"  id SERIAL PRIMARY KEY,")
            migration.append(f"  -- Add columns here")
            migration.append(");")
            migration.append("")
        
        # Add columns
        for column in differences["columns_added"]:
            table, col = column.split('.')
            migration.append(f"-- TODO: Add column {col} to table {table}")
            migration.append(f"ALTER TABLE {table} ADD COLUMN {col} VARCHAR(255);")
            migration.append("")
        
        # Remove columns
        for column in differences["columns_removed"]:
            table, col = column.split('.')
            migration.append(f"-- TODO: Remove column {col} from table {table}")
            migration.append(f"ALTER TABLE {table} DROP COLUMN {col};")
            migration.append("")
        
        # Add indexes
        for index in differences["indexes_added"]:
            migration.append(f"-- TODO: Create index {index}")
            migration.append(f"CREATE INDEX {index} ON table_name(column_name);")
            migration.append("")
        
        migration.append("")
        migration.append("-- DOWN Migration (rollback)")
        
        # Rollback for added tables
        for table in differences["tables_added"]:
            migration.append(f"DROP TABLE IF EXISTS {table};")
        
        # Rollback for added columns
        for column in differences["columns_added"]:
            table, col = column.split('.')
            migration.append(f"ALTER TABLE {table} DROP COLUMN IF EXISTS {col};")
        
        # Rollback for removed columns would need to restore them
        # This is complex without knowing original definition
        for column in differences["columns_removed"]:
            migration.append(f"-- TODO: Restore column {column}")
        
        # Rollback for added indexes
        for index in differences["indexes_added"]:
            migration.append(f"DROP INDEX IF EXISTS {index};")
    
    elif output_format == "json":
        migration = [json.dumps(differences, indent=2)]
    
    return '\n'.join(migration)

def compare_command(args):
    """Handle compare command."""
    # Parse schemas
    if args.source1.endswith('.sql'):
        schema1 = parse_sql_file(args.source1)
    else:
        # Assume it's a database connection string (simplified)
        schema1 = {"tables": [], "indexes": [], "error": "Database connections not implemented in this version"}
    
    if args.source2.endswith('.sql'):
        schema2 = parse_sql_file(args.source2)
    else:
        schema2 = {"tables": [], "indexes": [], "error": "Database connections not implemented in this version"}
    
    # Check for errors
    if "error" in schema1:
        print(f"❌ Error parsing source1: {schema1['error']}")
        return
    if "error" in schema2:
        print(f"❌ Error parsing source2: {schema2['error']}")
        return
    
    # Compare schemas
    differences = compare_schemas(schema1, schema2)
    
    # Output
    if args.json:
        print(json.dumps(differences, indent=2))
        return
    
    # Human-readable output
    print(f"🔍 Comparing schemas: {args.source1} vs {args.source2}")
    print()
    
    total_changes = sum(len(v) for v in differences.values())
    if total_changes == 0:
        print("✅ Schemas are identical")
        return
    
    print(f"📊 Found {total_changes} differences:")
    print()
    
    if differences["tables_added"]:
        print(f"📈 Tables added ({len(differences['tables_added'])}):")
        for table in differences["tables_added"]:
            print(f"  + {table}")
        print()
    
    if differences["tables_removed"]:
        print(f"📉 Tables removed ({len(differences['tables_removed'])}):")
        for table in differences["tables_removed"]:
            print(f"  - {table}")
        print()
    
    if differences["columns_added"]:
        print(f"➕ Columns added ({len(differences['columns_added'])}):")
        for column in differences["columns_added"][:10]:  # Limit output
            print(f"  + {column}")
        if len(differences["columns_added"]) > 10:
            print(f"  ... and {len(differences['columns_added']) - 10} more")
        print()
    
    if differences["columns_removed"]:
        print(f"➖ Columns removed ({len(differences['columns_removed'])}):")
        for column in differences["columns_removed"][:10]:
            print(f"  - {column}")
        if len(differences["columns_removed"]) > 10:
            print(f"  ... and {len(differences['columns_removed']) - 10} more")
        print()
    
    if differences["columns_changed"]:
        print(f"🔄 Columns changed ({len(differences['columns_changed'])}):")
        for column in differences["columns_changed"][:10]:
            print(f"  ~ {column}")
        if len(differences["columns_changed"]) > 10:
            print(f"  ... and {len(differences['columns_changed']) - 10} more")
        print()
    
    if differences["indexes_added"]:
        print(f"📊 Indexes added ({len(differences['indexes_added'])}):")
        for index in differences["indexes_added"]:
            print(f"  + {index}")
        print()
    
    if differences["indexes_removed"]:
        print(f"📊 Indexes removed ({len(differences['indexes_removed'])}):")
        for index in differences["indexes_removed"]:
            print(f"  - {index}")
        print()
    
    # Generate migration if requested
    if args.output:
        migration = generate_migration(differences, args.format)
        with open(args.output, 'w') as f:
            f.write(migration)
        print(f"✅ Migration script generated: {args.output}")

def diff_command(args):
    """Handle diff command (alias for compare with migration generation)."""
    # Reuse compare logic
    compare_args = argparse.Namespace(
        source1=args.old_schema,
        source2=args.new_schema,
        json=False,
        output=args.output,
        format=args.format
    )
    compare_command(compare_args)

def snapshot_command(args):
    """Handle snapshot command."""
    if args.database.endswith('.sql'):
        schema = parse_sql_file(args.database)
    else:
        schema = {"tables": [], "indexes": [], "error": "Database connections not implemented"}
    
    if "error" in schema:
        print(f"❌ Error: {schema['error']}")
        return
    
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": args.database,
        "schema": schema,
        "metadata": {
            "tables_count": len(schema.get("tables", [])),
            "indexes_count": len(schema.get("indexes", [])),
        }
    }
    
    if args.save:
        with open(args.save, 'w') as f:
            json.dump(snapshot, f, indent=2)
        print(f"✅ Schema snapshot saved: {args.save}")
    else:
        print(json.dumps(snapshot, indent=2))

def check_drift_command(args):
    """Handle check-drift command."""
    # Load expected and actual schemas
    if not os.path.exists(args.expected):
        print(f"❌ Expected schema file not found: {args.expected}")
        return 1
    
    if not os.path.exists(args.actual):
        print(f"❌ Actual schema file not found: {args.actual}")
        return 1
    
    expected = parse_sql_file(args.expected)
    actual = parse_sql_file(args.actual)
    
    if "error" in expected:
        print(f"❌ Error parsing expected: {expected['error']}")
        return 1
    if "error" in actual:
        print(f"❌ Error parsing actual: {actual['error']}")
        return 1
    
    differences = compare_schemas(expected, actual)
    total_changes = sum(len(v) for v in differences.values())
    
    if total_changes == 0:
        print("✅ No schema drift detected")
        return 0
    
    print("❌ Schema drift detected!")
    print()
    print(f"Differences found: {total_changes}")
    
    # Show summary
    if differences["tables_added"]:
        print(f"- Unexpected tables: {', '.join(differences['tables_added'][:3])}")
        if len(differences["tables_added"]) > 3:
            print(f"  ... and {len(differences['tables_added']) - 3} more")
    
    if differences["tables_removed"]:
        print(f"- Missing tables: {', '.join(differences['tables_removed'][:3])}")
        if len(differences["tables_removed"]) > 3:
            print(f"  ... and {len(differences['tables_removed']) - 3} more")
    
    if differences["columns_added"]:
        print(f"- Unexpected columns: {len(differences['columns_added'])}")
    
    if differences["columns_removed"]:
        print(f"- Missing columns: {len(differences['columns_removed'])}")
    
    if args.fail_on_drift:
        print(f"\nExit code: 1 (failed due to --fail-on-drift)")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Database Schema Differ')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two schemas')
    compare_parser.add_argument('source1', help='First schema (SQL file or database URL)')
    compare_parser.add_argument('source2', help='Second schema (SQL file or database URL)')
    compare_parser.add_argument('--json', action='store_true', help='Output JSON')
    compare_parser.add_argument('--output', help='Generate migration to file')
    compare_parser.add_argument('--format', choices=['sql', 'json'], default='sql', help='Output format')
    compare_parser.set_defaults(func=compare_command)
    
    # Diff command (alias with different args)
    diff_parser = subparsers.add_parser('diff', help='Generate migration from schema differences')
    diff_parser.add_argument('old_schema', help='Old schema (SQL file)')
    diff_parser.add_argument('new_schema', help='New schema (SQL file)')
    diff_parser.add_argument('--output', required=True, help='Output migration file')
    diff_parser.add_argument('--format', choices=['sql', 'json'], default='sql', help='Output format')
    diff_parser.set_defaults(func=diff_command)
    
    # Snapshot command
    snapshot_parser = subparsers.add_parser('snapshot', help='Create schema snapshot')
    snapshot_parser.add_argument('database', help='Database URL or SQL file')
    snapshot_parser.add_argument('--save', help='Save snapshot to file')
    snapshot_parser.set_defaults(func=snapshot_command)
    
    # Check-drift command
    drift_parser = subparsers.add_parser('check-drift', help='Check for schema drift')
    drift_parser.add_argument('--expected', required=True, help='Expected schema file')
    drift_parser.add_argument('--actual', required=True, help='Actual schema file')
    drift_parser.add_argument('--fail-on-drift', action='store_true', help='Exit with error if drift detected')
    drift_parser.set_defaults(func=check_drift_command)
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        parser.print_help()
        return
    
    if args.command == 'check-drift':
        # Special handling for check-drift which returns exit code
        exit_code = args.func(args)
        sys.exit(exit_code)
    else:
        args.func(args)

if __name__ == '__main__':
    main()