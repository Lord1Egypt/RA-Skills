#!/usr/bin/env python3
"""
Slow SQL Analysis Script
Analyzes SQL statements and execution plans to identify performance issues.
"""

import argparse
import json
import re
from typing import Dict, List, Tuple


class SlowSQLAnalyzer:
    """Analyzes SQL statements for performance issues."""
    
    def __init__(self):
        self.issues = []
        self.recommendations = []
        
    def analyze_sql(self, sql: str, execution_plan: str = None) -> Dict:
        """
        Analyze SQL statement for performance issues.
        
        Args:
            sql: SQL statement to analyze
            execution_plan: Optional execution plan output
            
        Returns:
            Dictionary containing analysis results
        """
        self.issues = []
        self.recommendations = []
        
        # Check for common anti-patterns
        self._check_select_star(sql)
        self._check_where_clause(sql)
        self._check_like_pattern(sql)
        self._check_or_conditions(sql)
        self._check_functions_in_where(sql)
        self._check_distinct(sql)
        
        # Analyze execution plan if provided
        if execution_plan:
            self._analyze_execution_plan(execution_plan)
        
        return {
            'sql': sql,
            'issues': self.issues,
            'recommendations': self.recommendations,
            'severity': self._calculate_severity()
        }
    
    def _check_select_star(self, sql: str):
        """Check for SELECT * usage."""
        if re.search(r'\bSELECT\s+\*', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'SELECT_STAR',
                'message': 'SELECT * retrieves all columns, which may transfer unnecessary data',
                'severity': 'MEDIUM'
            })
            self.recommendations.append({
                'suggestion': 'Specify only required columns in SELECT clause',
                'example': 'Replace SELECT * with SELECT col1, col2, ...'
            })
    
    def _check_where_clause(self, sql: str):
        """Check for missing WHERE clause in SELECT/UPDATE/DELETE."""
        if re.search(r'\b(SELECT|UPDATE|DELETE)\b', sql, re.IGNORECASE):
            if not re.search(r'\bWHERE\b', sql, re.IGNORECASE):
                self.issues.append({
                    'type': 'MISSING_WHERE',
                    'message': 'Statement lacks WHERE clause, may affect entire table',
                    'severity': 'HIGH'
                })
                self.recommendations.append({
                    'suggestion': 'Add WHERE clause to limit affected rows',
                    'example': 'WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)'
                })
    
    def _check_like_pattern(self, sql: str):
        """Check for inefficient LIKE patterns."""
        if re.search(r"LIKE\s+['\"]%", sql, re.IGNORECASE):
            self.issues.append({
                'type': 'LEADING_WILDCARD',
                'message': 'LIKE with leading wildcard prevents index usage',
                'severity': 'HIGH'
            })
            self.recommendations.append({
                'suggestion': 'Avoid leading wildcard or use full-text search',
                'example': "LIKE 'prefix%' instead of LIKE '%pattern'"
            })
    
    def _check_or_conditions(self, sql: str):
        """Check for OR conditions that may prevent index usage."""
        if re.search(r'\bOR\b', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'OR_CONDITIONS',
                'message': 'OR conditions may prevent effective index usage',
                'severity': 'MEDIUM'
            })
            self.recommendations.append({
                'suggestion': 'Consider using UNION or IN clause instead',
                'example': 'SELECT ... WHERE id IN (1, 2, 3) instead of id=1 OR id=2 OR id=3'
            })
    
    def _check_functions_in_where(self, sql: str):
        """Check for functions in WHERE clause that prevent index usage."""
        if re.search(r'WHERE.*\w+\s*\([^)]*\)', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'FUNCTION_ON_COLUMN',
                'message': 'Function on column in WHERE clause may prevent index usage',
                'severity': 'MEDIUM'
            })
            self.recommendations.append({
                'suggestion': 'Rewrite condition to avoid function on indexed column',
                'example': 'WHERE date_col >= "2024-01-01" instead of WHERE DATE(date_col) = "2024-01-01"'
            })
    
    def _check_distinct(self, sql: str):
        """Check for DISTINCT that may indicate schema issues."""
        if re.search(r'\bDISTINCT\b', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'DISTINCT_USAGE',
                'message': 'DISTINCT may indicate duplicate data or missing JOIN conditions',
                'severity': 'LOW'
            })
            self.recommendations.append({
                'suggestion': 'Verify if DISTINCT is necessary, consider GROUP BY or improving JOIN logic',
                'example': 'Review schema and query logic to eliminate duplicates at source'
            })
    
    def _analyze_execution_plan(self, plan: str):
        """Analyze execution plan for performance issues."""
        # Check for full table scan
        if re.search(r'(type:\s*ALL|FULL TABLE SCAN|Seq Scan)', plan, re.IGNORECASE):
            self.issues.append({
                'type': 'FULL_TABLE_SCAN',
                'message': 'Query performs full table scan - no suitable index found',
                'severity': 'HIGH'
            })
            self.recommendations.append({
                'suggestion': 'Add index on columns used in WHERE/JOIN clauses',
                'example': 'CREATE INDEX idx_table_column ON table_name(column_name)'
            })
        
        # Check for temporary tables
        if re.search(r'Using temporary', plan, re.IGNORECASE):
            self.issues.append({
                'type': 'TEMPORARY_TABLE',
                'message': 'Query creates temporary table',
                'severity': 'MEDIUM'
            })
            self.recommendations.append({
                'suggestion': 'Consider optimizing GROUP BY or ORDER BY clauses',
                'example': 'Add composite index on GROUP BY/ORDER BY columns'
            })
        
        # Check for filesort
        if re.search(r'Using filesort', plan, re.IGNORECASE):
            self.issues.append({
                'type': 'FILESORT',
                'message': 'Query requires filesort operation',
                'severity': 'MEDIUM'
            })
            self.recommendations.append({
                'suggestion': 'Add index on ORDER BY columns',
                'example': 'CREATE INDEX idx_order ON table_name(order_column)'
            })
    
    def _calculate_severity(self) -> str:
        """Calculate overall severity based on issues found."""
        if not self.issues:
            return 'NONE'
        
        severity_scores = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        max_severity = max(severity_scores.get(issue['severity'], 0) for issue in self.issues)
        
        if max_severity >= 3:
            return 'HIGH'
        elif max_severity >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_index_suggestions(self, table_name: str, columns: List[str]) -> List[str]:
        """Generate index creation suggestions."""
        suggestions = []
        
        for col in columns:
            suggestions.append(
                f"CREATE INDEX idx_{table_name}_{col} ON {table_name}({col});"
            )
        
        return suggestions


def main():
    parser = argparse.ArgumentParser(description='Analyze SQL for performance issues')
    parser.add_argument('--sql', required=True, help='SQL statement to analyze')
    parser.add_argument('--plan', help='Execution plan output (optional)')
    parser.add_argument('--output', default='json', choices=['json', 'text'], 
                       help='Output format')
    
    args = parser.parse_args()
    
    analyzer = SlowSQLAnalyzer()
    result = analyzer.analyze_sql(args.sql, args.plan)
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(f"SQL Analysis Report")
        print("=" * 60)
        print(f"SQL: {result['sql']}")
        print(f"Severity: {result['severity']}")
        print("\nIssues Found:")
        for issue in result['issues']:
            print(f"  [{issue['severity']}] {issue['type']}: {issue['message']}")
        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  - {rec['suggestion']}")
            print(f"    Example: {rec['example']}")


if __name__ == '__main__':
    main()
