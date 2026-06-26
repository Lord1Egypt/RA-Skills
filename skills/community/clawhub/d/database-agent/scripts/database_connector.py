#!/usr/bin/env python3
"""
Database Connector
Provides JDBC-like database connection utilities for Python.
"""

import argparse
import json
from typing import Dict, List, Any, Optional


class DatabaseConnector:
    """Database connection and query utilities."""
    
    def __init__(self, config: Dict):
        """
        Initialize database connector.
        
        Args:
            config: Database configuration dictionary
                {
                    'host': str,
                    'port': int,
                    'database': str,
                    'user': str,
                    'password': str,
                    'type': str (mysql, postgresql, etc.)
                }
        """
        self.config = config
        self.connection = None
        
    def connect(self):
        """Establish database connection."""
        try:
            import pymysql
            db_type = self.config.get('type', 'mysql')
            
            if db_type == 'mysql':
                self.connection = pymysql.connect(
                    host=self.config['host'],
                    port=self.config.get('port', 3306),
                    user=self.config['user'],
                    password=self.config['password'],
                    database=self.config['database'],
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                print(f"Connected to MySQL database: {self.config['database']}")
            
            elif db_type == 'postgresql':
                import psycopg2
                self.connection = psycopg2.connect(
                    host=self.config['host'],
                    port=self.config.get('port', 5432),
                    user=self.config['user'],
                    password=self.config['password'],
                    database=self.config['database']
                )
                print(f"Connected to PostgreSQL database: {self.config['database']}")
            
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
                
        except ImportError as e:
            print(f"Error: Required database driver not installed. {e}")
            print("For MySQL: pip install pymysql")
            print("For PostgreSQL: pip install psycopg2-binary")
            raise
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, sql: str, params: tuple = None) -> List[Dict]:
        """
        Execute a query and return results.
        
        Args:
            sql: SQL query
            params: Query parameters
            
        Returns:
            List of dictionaries representing rows
        """
        if not self.connection:
            raise RuntimeError("Not connected to database")
        
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def execute_update(self, sql: str, params: tuple = None) -> int:
        """
        Execute an UPDATE/INSERT/DELETE statement.
        
        Args:
            sql: SQL statement
            params: Statement parameters
            
        Returns:
            Number of affected rows
        """
        if not self.connection:
            raise RuntimeError("Not connected to database")
        
        with self.connection.cursor() as cursor:
            affected_rows = cursor.execute(sql, params)
            self.connection.commit()
            return affected_rows
    
    def get_table_schema(self, table_name: str) -> Dict:
        """
        Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table metadata
        """
        db_type = self.config.get('type', 'mysql')
        
        if db_type == 'mysql':
            return self._get_mysql_table_schema(table_name)
        elif db_type == 'postgresql':
            return self._get_postgresql_table_schema(table_name)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def _get_mysql_table_schema(self, table_name: str) -> Dict:
        """Get MySQL table schema."""
        # Get column information
        columns_sql = f"""
            SELECT 
                COLUMN_NAME as name,
                COLUMN_TYPE as type,
                IS_NULLABLE as nullable,
                COLUMN_KEY as key_type,
                COLUMN_DEFAULT as default_value,
                EXTRA as extra
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """
        
        columns = self.execute_query(
            columns_sql, 
            (self.config['database'], table_name)
        )
        
        # Get index information
        indexes_sql = f"""
            SELECT 
                INDEX_NAME as index_name,
                COLUMN_NAME as column_name,
                NON_UNIQUE as non_unique
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """
        
        indexes = self.execute_query(
            indexes_sql,
            (self.config['database'], table_name)
        )
        
        # Format columns
        formatted_columns = []
        for col in columns:
            formatted_columns.append({
                'name': col['name'],
                'type': col['type'],
                'nullable': col['nullable'] == 'YES',
                'is_primary_key': col['key_type'] == 'PRI',
                'default': col['default_value'],
                'auto_increment': 'auto_increment' in (col['extra'] or '').lower()
            })
        
        return {
            'table_name': table_name,
            'columns': formatted_columns,
            'indexes': indexes
        }
    
    def _get_postgresql_table_schema(self, table_name: str) -> Dict:
        """Get PostgreSQL table schema."""
        # Get column information
        columns_sql = f"""
            SELECT 
                column_name as name,
                data_type as type,
                is_nullable as nullable,
                column_default as default_value,
                character_maximum_length as max_length
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """
        
        columns = self.execute_query(columns_sql, (table_name,))
        
        # Get primary key
        pk_sql = f"""
            SELECT a.attname as column_name
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass AND i.indisprimary
        """
        
        primary_keys = self.execute_query(pk_sql, (table_name,))
        pk_columns = [pk['column_name'] for pk in primary_keys]
        
        # Format columns
        formatted_columns = []
        for col in columns:
            col_type = col['type']
            if col['max_length']:
                col_type = f"{col_type}({col['max_length']})"
            
            formatted_columns.append({
                'name': col['name'],
                'type': col_type,
                'nullable': col['nullable'] == 'YES',
                'is_primary_key': col['name'] in pk_columns,
                'default': col['default_value']
            })
        
        return {
            'table_name': table_name,
            'columns': formatted_columns
        }
    
    def get_all_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        db_type = self.config.get('type', 'mysql')
        
        if db_type == 'mysql':
            sql = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
            """
            result = self.execute_query(sql, (self.config['database'],))
        
        elif db_type == 'postgresql':
            sql = """
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """
            result = self.execute_query(sql)
        
        return [row['TABLE_NAME' if db_type == 'mysql' else 'tablename'] for row in result]
    
    def explain_query(self, sql: str) -> str:
        """Get execution plan for a query."""
        db_type = self.config.get('type', 'mysql')
        
        if db_type == 'mysql':
            explain_sql = f"EXPLAIN {sql}"
        elif db_type == 'postgresql':
            explain_sql = f"EXPLAIN ANALYZE {sql}"
        
        result = self.execute_query(explain_sql)
        return json.dumps(result, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Database connector utilities')
    parser.add_argument('--config', required=True, help='JSON file containing database config')
    parser.add_argument('--action', required=True, 
                       choices=['tables', 'schema', 'query', 'explain'],
                       help='Action to perform')
    parser.add_argument('--table', help='Table name (for schema action)')
    parser.add_argument('--sql', help='SQL query (for query/explain actions)')
    
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    connector = DatabaseConnector(config)
    
    try:
        connector.connect()
        
        if args.action == 'tables':
            tables = connector.get_all_tables()
            print("Tables in database:")
            for table in tables:
                print(f"  - {table}")
        
        elif args.action == 'schema':
            if not args.table:
                print("Error: --table required for schema action")
                return
            
            schema = connector.get_table_schema(args.table)
            print(json.dumps(schema, indent=2))
        
        elif args.action == 'query':
            if not args.sql:
                print("Error: --sql required for query action")
                return
            
            result = connector.execute_query(args.sql)
            print(json.dumps(result, indent=2))
        
        elif args.action == 'explain':
            if not args.sql:
                print("Error: --sql required for explain action")
                return
            
            plan = connector.explain_query(args.sql)
            print(plan)
    
    finally:
        connector.close()


if __name__ == '__main__':
    main()
