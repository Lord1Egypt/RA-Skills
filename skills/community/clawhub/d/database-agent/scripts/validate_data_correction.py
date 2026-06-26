#!/usr/bin/env python3
"""
Data Correction Safety Validator
Validates UPDATE/DELETE operations to prevent unsafe data modifications.
"""

import argparse
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple


class DataCorrectionValidator:
    """Validates data modification operations for safety."""
    
    def __init__(self):
        self.risks = []
        self.is_safe = True
        
    def validate_sql(self, sql: str, affected_rows_estimate: int = None) -> Dict:
        """
        Validate UPDATE/DELETE SQL for safety risks.
        
        Args:
            sql: SQL statement to validate
            affected_rows_estimate: Optional estimate of affected rows
            
        Returns:
            Dictionary containing validation results
        """
        self.risks = []
        self.is_safe = True
        
        sql_upper = sql.upper()
        
        # Determine operation type
        operation = self._get_operation_type(sql_upper)
        
        # Perform safety checks
        self._check_where_clause(sql, operation)
        self._check_limit_clause(sql, operation)
        self._check_dangerous_patterns(sql, operation)
        self._check_primary_key_modification(sql, operation)
        
        # Check affected rows estimate if provided
        if affected_rows_estimate is not None:
            self._check_affected_rows(affected_rows_estimate)
        
        return {
            'sql': sql,
            'operation': operation,
            'is_safe': self.is_safe,
            'risks': self.risks,
            'requires_backup': len(self.risks) > 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_operation_type(self, sql_upper: str) -> str:
        """Determine the type of SQL operation."""
        if 'UPDATE' in sql_upper:
            return 'UPDATE'
        elif 'DELETE' in sql_upper:
            return 'DELETE'
        elif 'INSERT' in sql_upper:
            return 'INSERT'
        return 'UNKNOWN'
    
    def _check_where_clause(self, sql: str, operation: str):
        """Check for missing WHERE clause."""
        if operation in ['UPDATE', 'DELETE']:
            if not re.search(r'\bWHERE\b', sql, re.IGNORECASE):
                self.risks.append({
                    'type': 'MISSING_WHERE',
                    'severity': 'CRITICAL',
                    'message': f'{operation} without WHERE clause affects entire table',
                    'recommendation': 'Add WHERE clause to limit affected rows'
                })
                self.is_safe = False
    
    def _check_limit_clause(self, sql: str, operation: str):
        """Check for missing LIMIT clause on DELETE."""
        if operation == 'DELETE':
            if not re.search(r'\bLIMIT\b', sql, re.IGNORECASE):
                self.risks.append({
                    'type': 'NO_LIMIT',
                    'severity': 'HIGH',
                    'message': 'DELETE without LIMIT may affect more rows than expected',
                    'recommendation': 'Consider adding LIMIT clause or use transactions'
                })
    
    def _check_dangerous_patterns(self, sql: str, operation: str):
        """Check for dangerous SQL patterns."""
        sql_upper = sql.upper()
        
        # Check for TRUE conditions
        if re.search(r'\bWHERE\s+(TRUE|1\s*=\s*1)\b', sql, re.IGNORECASE):
            self.risks.append({
                'type': 'ALWAYS_TRUE_WHERE',
                'severity': 'CRITICAL',
                'message': 'WHERE clause is always true - affects all rows',
                'recommendation': 'Review WHERE clause logic'
            })
            self.is_safe = False
        
        # Check for OR 1=1 injection pattern
        if re.search(r'\bOR\s+1\s*=\s*1\b', sql, re.IGNORECASE):
            self.risks.append({
                'type': 'SQL_INJECTION_PATTERN',
                'severity': 'CRITICAL',
                'message': 'Detected potential SQL injection pattern: OR 1=1',
                'recommendation': 'Review query construction'
            })
            self.is_safe = False
        
        # Check for UPDATE with id in SET clause
        if operation == 'UPDATE':
            if re.search(r'\bSET\b.*\bid\s*=', sql, re.IGNORECASE):
                self.risks.append({
                    'type': 'UPDATING_PRIMARY_KEY',
                    'severity': 'HIGH',
                    'message': 'Attempting to update primary key column',
                    'recommendation': 'Primary key updates may break referential integrity'
                })
    
    def _check_primary_key_modification(self, sql: str, operation: str):
        """Check if operation modifies primary key or unique constraints."""
        sql_upper = sql.upper()
        
        # Check for deleting by non-primary key
        if operation == 'DELETE':
            # If WHERE doesn't contain id or primary key columns
            if not re.search(r'\bWHERE\b.*\bid\b', sql, re.IGNORECASE):
                self.risks.append({
                    'type': 'DELETE_BY_NON_PK',
                    'severity': 'MEDIUM',
                    'message': 'DELETE by non-primary key may be slower on large tables',
                    'recommendation': 'Consider deleting by primary key for better performance'
                })
    
    def _check_affected_rows(self, affected_rows: int):
        """Check if affected rows count exceeds safety threshold."""
        WARNING_THRESHOLD = 1000
        CRITICAL_THRESHOLD = 10000
        
        if affected_rows >= CRITICAL_THRESHOLD:
            self.risks.append({
                'type': 'MASS_OPERATION',
                'severity': 'CRITICAL',
                'message': f'Operation affects {affected_rows} rows (>= {CRITICAL_THRESHOLD})',
                'recommendation': 'Requires explicit confirmation and approval'
            })
            self.is_safe = False
        elif affected_rows >= WARNING_THRESHOLD:
            self.risks.append({
                'type': 'LARGE_OPERATION',
                'severity': 'HIGH',
                'message': f'Operation affects {affected_rows} rows (>= {WARNING_THRESHOLD})',
                'recommendation': 'Consider batch processing with LIMIT'
            })
    
    def generate_backup_sql(self, sql: str, table_name: str = None) -> str:
        """Generate backup SQL statement."""
        # Extract table name from SQL if not provided
        if not table_name:
            table_match = re.search(r'\bFROM\s+(\w+)', sql, re.IGNORECASE)
            if table_match:
                table_name = table_match.group(1)
            else:
                table_name = 'unknown_table'
        
        # Extract WHERE clause
        where_match = re.search(r'\bWHERE\s+(.+)', sql, re.IGNORECASE)
        where_clause = where_match.group(1) if where_match else '1=1'
        
        # Generate backup table name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_table = f"{table_name}_backup_{timestamp}"
        
        return f"CREATE TABLE {backup_table} AS SELECT * FROM {table_name} WHERE {where_clause};"
    
    def generate_rollback_sql(self, sql: str, table_name: str = None) -> List[str]:
        """Generate rollback SQL statements."""
        rollback_statements = []
        
        # Extract table name
        if not table_name:
            table_match = re.search(r'\bFROM\s+(\w+)', sql, re.IGNORECASE)
            table_name = table_match.group(1) if table_match else 'unknown_table'
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_table = f"{table_name}_backup_{timestamp}"
        
        # Generate rollback based on operation type
        if 'DELETE' in sql.upper():
            rollback_statements.append(
                f"-- Rollback: Restore deleted records\n"
                f"INSERT INTO {table_name} SELECT * FROM {backup_table};"
            )
        elif 'UPDATE' in sql.upper():
            # This is simplified - real rollback would need to know original values
            rollback_statements.append(
                f"-- Rollback: Restore updated records\n"
                f"-- Requires backup table with original values\n"
                f"UPDATE {table_name} t SET ... FROM {backup_table} b WHERE t.id = b.id;"
            )
        
        return rollback_statements


def main():
    parser = argparse.ArgumentParser(description='Validate data correction SQL for safety')
    parser.add_argument('--sql', required=True, help='SQL statement to validate')
    parser.add_argument('--affected-rows', type=int, help='Estimated affected rows (optional)')
    parser.add_argument('--output', default='json', choices=['json', 'text'],
                       help='Output format')
    
    args = parser.parse_args()
    
    validator = DataCorrectionValidator()
    result = validator.validate_sql(args.sql, args.affected_rows)
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(f"Data Correction Safety Report")
        print("=" * 60)
        print(f"Operation: {result['operation']}")
        print(f"Safe: {'YES' if result['is_safe'] else 'NO'}")
        print(f"\nRisks Identified: {len(result['risks'])}")
        for risk in result['risks']:
            print(f"  [{risk['severity']}] {risk['type']}")
            print(f"    {risk['message']}")
            print(f"    Recommendation: {risk['recommendation']}")
        
        if result['requires_backup']:
            print("\n⚠️  BACKUP REQUIRED")
            backup_sql = validator.generate_backup_sql(args.sql)
            print(f"\nBackup SQL:\n{backup_sql}")


if __name__ == '__main__':
    main()
