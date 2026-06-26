#!/usr/bin/env python3
"""
Schema Compliance Checker
Validates database table structures against best practices and standards.
"""

import argparse
import json
import re
from typing import Dict, List


class SchemaComplianceChecker:
    """Validates table structures against database standards."""
    
    def __init__(self, rules_config: Dict = None):
        self.violations = []
        self.warnings = []
        self.rules = rules_config or self._default_rules()
        
    def _default_rules(self) -> Dict:
        """Default compliance rules."""
        return {
            'naming': {
                'table_pattern': r'^[a-z][a-z0-9_]*$',
                'column_pattern': r'^[a-z][a-z0-9_]*$',
                'reserved_keywords': ['order', 'group', 'select', 'index', 'key', 'value']
            },
            'primary_key': {
                'required': True,
                'naming_pattern': r'^id$|^[a-z_]+_id$'
            },
            'data_types': {
                'string_max_length': 255,
                'text_for_long_strings': True
            },
            'defaults': {
                'not_null_preferred': True,
                'explicit_defaults_required': False
            }
        }
    
    def check_table(self, table_schema: Dict) -> Dict:
        """
        Check table schema for compliance issues.
        
        Args:
            table_schema: Dictionary containing table metadata
                {
                    'table_name': str,
                    'columns': [
                        {
                            'name': str,
                            'type': str,
                            'nullable': bool,
                            'default': any,
                            'is_primary_key': bool
                        }
                    ],
                    'indexes': [...]
                }
        
        Returns:
            Dictionary with compliance results
        """
        self.violations = []
        self.warnings = []
        
        table_name = table_schema.get('table_name', '')
        columns = table_schema.get('columns', [])
        
        # Check table naming
        self._check_table_naming(table_name)
        
        # Check primary key
        self._check_primary_key(columns)
        
        # Check each column
        for column in columns:
            self._check_column_naming(table_name, column)
            self._check_column_type(table_name, column)
            self._check_column_nullable(table_name, column)
        
        return {
            'table_name': table_name,
            'violations': self.violations,
            'warnings': self.warnings,
            'compliance_score': self._calculate_compliance_score()
        }
    
    def _check_table_naming(self, table_name: str):
        """Check if table name follows naming conventions."""
        pattern = self.rules['naming']['table_pattern']
        
        if not re.match(pattern, table_name):
            self.violations.append({
                'type': 'TABLE_NAMING',
                'message': f"Table name '{table_name}' doesn't follow naming convention",
                'severity': 'HIGH',
                'suggestion': f"Use lowercase letters, numbers, and underscores only"
            })
        
        # Check reserved keywords
        if table_name.lower() in self.rules['naming']['reserved_keywords']:
            self.violations.append({
                'type': 'RESERVED_KEYWORD',
                'message': f"Table name '{table_name}' is a reserved keyword",
                'severity': 'HIGH',
                'suggestion': f"Prefix with 'tbl_' or use alternative name"
            })
    
    def _check_primary_key(self, columns: List[Dict]):
        """Check if table has proper primary key."""
        has_pk = any(col.get('is_primary_key', False) for col in columns)
        
        if not has_pk:
            self.violations.append({
                'type': 'MISSING_PRIMARY_KEY',
                'message': 'Table lacks primary key',
                'severity': 'HIGH',
                'suggestion': 'Add an auto-increment ID column as primary key'
            })
    
    def _check_column_naming(self, table_name: str, column: Dict):
        """Check column naming conventions."""
        col_name = column.get('name', '')
        pattern = self.rules['naming']['column_pattern']
        
        if not re.match(pattern, col_name):
            self.violations.append({
                'type': 'COLUMN_NAMING',
                'message': f"Column '{col_name}' in table '{table_name}' doesn't follow naming convention",
                'severity': 'MEDIUM',
                'suggestion': 'Use lowercase letters, numbers, and underscores only'
            })
        
        # Check reserved keywords
        if col_name.lower() in self.rules['naming']['reserved_keywords']:
            self.violations.append({
                'type': 'RESERVED_KEYWORD',
                'message': f"Column '{col_name}' is a reserved keyword",
                'severity': 'HIGH',
                'suggestion': f"Use alternative name like '{col_name}_value'"
            })
    
    def _check_column_type(self, table_name: str, column: Dict):
        """Check column data type appropriateness."""
        col_name = column.get('name', '')
        col_type = column.get('type', '').upper()
        
        # Check for VARCHAR length
        if 'VARCHAR' in col_type or 'CHAR' in col_type:
            match = re.search(r'\((\d+)\)', col_type)
            if match:
                length = int(match.group(1))
                if length > self.rules['data_types']['string_max_length']:
                    self.warnings.append({
                        'type': 'LONG_VARCHAR',
                        'message': f"Column '{col_name}' has VARCHAR({length}), consider using TEXT",
                        'severity': 'LOW',
                        'suggestion': 'Use TEXT type for strings longer than 255 characters'
                    })
    
    def _check_column_nullable(self, table_name: str, column: Dict):
        """Check nullable column practices."""
        col_name = column.get('name', '')
        nullable = column.get('nullable', True)
        default = column.get('default')
        
        # Recommend NOT NULL for critical columns
        if nullable and col_name.endswith(('_id', '_time', '_date', '_status')):
            self.warnings.append({
                'type': 'NULLABLE_COLUMN',
                'message': f"Column '{col_name}' should typically be NOT NULL",
                'severity': 'MEDIUM',
                'suggestion': 'Consider adding NOT NULL constraint with default value'
            })
    
    def _calculate_compliance_score(self) -> int:
        """Calculate compliance score (0-100)."""
        if not self.violations and not self.warnings:
            return 100
        
        # Each violation reduces score by 20, each warning by 5
        score = 100 - (len(self.violations) * 20) - (len(self.warnings) * 5)
        return max(0, score)
    
    def generate_fix_sql(self, violations: List[Dict], table_name: str) -> List[str]:
        """Generate SQL statements to fix violations."""
        fix_statements = []
        
        for violation in violations:
            if violation['type'] == 'MISSING_PRIMARY_KEY':
                fix_statements.append(
                    f"ALTER TABLE {table_name} ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;"
                )
        
        return fix_statements


def main():
    parser = argparse.ArgumentParser(description='Check database schema compliance')
    parser.add_argument('--schema', required=True, help='JSON file containing table schema')
    parser.add_argument('--rules', help='JSON file containing custom rules (optional)')
    parser.add_argument('--output', default='json', choices=['json', 'text'],
                       help='Output format')
    
    args = parser.parse_args()
    
    # Load table schema
    with open(args.schema, 'r') as f:
        table_schema = json.load(f)
    
    # Load custom rules if provided
    rules = None
    if args.rules:
        with open(args.rules, 'r') as f:
            rules = json.load(f)
    
    checker = SchemaComplianceChecker(rules)
    result = checker.check_table(table_schema)
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(f"Schema Compliance Report for '{result['table_name']}'")
        print("=" * 60)
        print(f"Compliance Score: {result['compliance_score']}/100")
        print("\nViolations:")
        for violation in result['violations']:
            print(f"  [{violation['severity']}] {violation['type']}")
            print(f"    {violation['message']}")
            print(f"    Suggestion: {violation['suggestion']}")
        print("\nWarnings:")
        for warning in result['warnings']:
            print(f"  [{warning['severity']}] {warning['type']}")
            print(f"    {warning['message']}")


if __name__ == '__main__':
    main()
