#!/usr/bin/env python3
"""
Test Data Generator
Intelligently generates test data based on table structures and business rules.
"""

import argparse
import json
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any
import hashlib


class TestDataGenerator:
    """Generates intelligent test data based on table schema."""
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.generated_ids = {}  # Track generated IDs for foreign keys
        
    def _default_config(self) -> Dict:
        """Default test data generation configuration."""
        return {
            'string_patterns': {
                'email': lambda: f"user{random.randint(1, 10000)}@test.com",
                'phone': lambda: f"1{random.randint(3000000000, 9999999999)}",
                'name': lambda: random.choice(['张三', '李四', '王五', '赵六', '钱七']),
                'address': lambda: f"测试地址{random.randint(1, 999)}号",
                'uuid': lambda: hashlib.md5(str(random.random()).encode()).hexdigest()
            },
            'number_ranges': {
                'age': (18, 70),
                'price': (1, 10000),
                'quantity': (1, 100),
                'status': (0, 1)
            },
            'date_ranges': {
                'past_days': 365,
                'future_days': 30
            }
        }
    
    def generate_for_table(self, table_schema: Dict, count: int = 100) -> List[Dict]:
        """
        Generate test data for a table.
        
        Args:
            table_schema: Table metadata including columns
            count: Number of rows to generate
            
        Returns:
            List of dictionaries representing test data rows
        """
        rows = []
        table_name = table_schema.get('table_name', '')
        columns = table_schema.get('columns', [])
        
        for i in range(count):
            row = {}
            for column in columns:
                col_name = column.get('name', '')
                col_type = column.get('type', '').upper()
                is_pk = column.get('is_primary_key', False)
                
                # Generate value for this column
                value = self._generate_column_value(
                    col_name, col_type, is_pk, table_name
                )
                row[col_name] = value
            
            rows.append(row)
        
        return rows
    
    def _generate_column_value(self, col_name: str, col_type: str, 
                               is_pk: bool, table_name: str) -> Any:
        """Generate a value for a specific column."""
        col_lower = col_name.lower()
        
        # Primary key handling
        if is_pk:
            if 'AUTO_INCREMENT' in col_type.upper():
                return None  # Will be auto-generated
        
        # Pattern-based generation
        if 'email' in col_lower:
            return self.config['string_patterns']['email']()
        elif 'phone' in col_lower or 'mobile' in col_lower:
            return self.config['string_patterns']['phone']()
        elif 'name' in col_lower and 'user' in col_lower:
            return self.config['string_patterns']['name']()
        elif 'address' in col_lower:
            return self.config['string_patterns']['address']()
        elif col_lower.endswith('_id') and not is_pk:
            # Foreign key - return a valid reference
            return self._generate_foreign_key_reference(col_lower)
        
        # Type-based generation
        if 'INT' in col_type:
            if 'age' in col_lower:
                return random.randint(*self.config['number_ranges']['age'])
            elif 'status' in col_lower:
                return random.randint(*self.config['number_ranges']['status'])
            elif 'price' in col_lower or 'amount' in col_lower:
                return random.randint(*self.config['number_ranges']['price'])
            else:
                return random.randint(1, 10000)
        
        elif 'VARCHAR' in col_type or 'CHAR' in col_type:
            # Extract length from type
            match = re.search(r'\((\d+)\)', col_type)
            max_length = int(match.group(1)) if match else 255
            
            # Generate appropriate string
            if max_length <= 10:
                return f"TEST{random.randint(1, 999):03d}"
            else:
                return f"测试数据_{random.randint(1, 9999)}"
        
        elif 'TEXT' in col_type:
            return f"测试文本内容_{random.randint(1, 100)}: 这是自动生成的测试数据"
        
        elif 'DATE' in col_type:
            days_ago = random.randint(0, self.config['date_ranges']['past_days'])
            return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        elif 'DATETIME' in col_type or 'TIMESTAMP' in col_type:
            days_ago = random.randint(0, self.config['date_ranges']['past_days'])
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            dt = datetime.now() - timedelta(days=days_ago, hours=hours, minutes=minutes)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        
        elif 'DECIMAL' in col_type or 'FLOAT' in col_type or 'DOUBLE' in col_type:
            return round(random.uniform(1, 10000), 2)
        
        elif 'BOOLEAN' in col_type or 'TINYINT' in col_type:
            return random.choice([0, 1])
        
        else:
            # Default: generate a string
            return f"test_value_{random.randint(1, 1000)}"
    
    def _generate_foreign_key_reference(self, col_name: str) -> int:
        """Generate a valid foreign key reference."""
        # Extract table name from column name (e.g., user_id -> user)
        ref_table = col_name.replace('_id', '')
        
        # If we haven't generated IDs for this table, generate some
        if ref_table not in self.generated_ids:
            self.generated_ids[ref_table] = list(range(1, 101))
        
        # Return a random ID from the generated set
        return random.choice(self.generated_ids[ref_table])
    
    def generate_insert_statements(self, table_name: str, rows: List[Dict]) -> List[str]:
        """Generate INSERT SQL statements from test data."""
        statements = []
        
        for row in rows:
            columns = ', '.join(row.keys())
            values = []
            
            for value in row.values():
                if value is None:
                    values.append('NULL')
                elif isinstance(value, str):
                    # Escape quotes
                    escaped = value.replace("'", "''")
                    values.append(f"'{escaped}'")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    values.append(f"'{value}'")
            
            values_str = ', '.join(values)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values_str});"
            statements.append(sql)
        
        return statements
    
    def generate_batch_insert(self, table_name: str, rows: List[Dict], 
                             batch_size: int = 100) -> List[str]:
        """Generate batch INSERT statements for better performance."""
        statements = []
        
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            
            if not batch:
                continue
            
            columns = ', '.join(batch[0].keys())
            all_values = []
            
            for row in batch:
                values = []
                for value in row.values():
                    if value is None:
                        values.append('NULL')
                    elif isinstance(value, str):
                        escaped = value.replace("'", "''")
                        values.append(f"'{escaped}'")
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    else:
                        values.append(f"'{value}'")
                all_values.append(f"({', '.join(values)})")
            
            values_str = ',\n'.join(all_values)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES\n{values_str};"
            statements.append(sql)
        
        return statements


def main():
    parser = argparse.ArgumentParser(description='Generate test data for database tables')
    parser.add_argument('--schema', required=True, help='JSON file containing table schema')
    parser.add_argument('--count', type=int, default=100, help='Number of rows to generate')
    parser.add_argument('--output', default='sql', choices=['sql', 'json'],
                       help='Output format')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Batch size for INSERT statements')
    parser.add_argument('--config', help='JSON file containing generation config')
    
    args = parser.parse_args()
    
    # Load table schema
    with open(args.schema, 'r') as f:
        table_schema = json.load(f)
    
    # Load config if provided
    config = None
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    generator = TestDataGenerator(config)
    rows = generator.generate_for_table(table_schema, args.count)
    
    if args.output == 'json':
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        table_name = table_schema.get('table_name', 'table')
        statements = generator.generate_batch_insert(
            table_name, rows, args.batch_size
        )
        
        print(f"-- Generated {len(rows)} test records for table '{table_name}'")
        print(f"-- Generated at: {datetime.now().isoformat()}\n")
        
        for stmt in statements:
            print(stmt)
            print()


if __name__ == '__main__':
    main()
