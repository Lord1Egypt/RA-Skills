#!/usr/bin/env python3
"""
Data Toolkit - Data Validator
Supports: JSON Schema, CSV structure, custom rules
"""

import argparse
import json
import csv
import sys
from typing import Any, Dict, List, Tuple
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_json_schema(data: Any, schema: Dict) -> Tuple[bool, List[str]]:
        """Validate JSON data against a schema (simplified)"""
        errors = []
        
        def validate_type(value: Any, expected_type: str, path: str = "") -> None:
            type_map = {
                'string': str,
                'number': (int, float),
                'integer': int,
                'boolean': bool,
                'array': list,
                'object': dict,
                'null': type(None)
            }
            
            expected_py_type = type_map.get(expected_type)
            if expected_py_type and not isinstance(value, expected_py_type):
                errors.append(f"{path}: Expected {expected_type}, got {type(value).__name__}")
        
        def validate_object(obj: Any, schema: Dict, path: str = "root") -> None:
            if not isinstance(obj, dict) and schema.get('type') == 'object':
                errors.append(f"{path}: Expected object, got {type(obj).__name__}")
                return
            
            # Check type
            if 'type' in schema:
                validate_type(obj, schema['type'], path)
            
            # Check required properties
            if 'required' in schema:
                for prop in schema['required']:
                    if prop not in obj:
                        errors.append(f"{path}: Missing required property '{prop}'")
            
            # Check properties
            if 'properties' in schema:
                for prop, prop_schema in schema['properties'].items():
                    if prop in obj:
                        validate_object(obj[prop], prop_schema, f"{path}.{prop}")
            
            # Check array items
            if schema.get('type') == 'array' and 'items' in schema:
                if isinstance(obj, list):
                    for i, item in enumerate(obj):
                        validate_object(item, schema['items'], f"{path}[{i}]")
        
        try:
            validate_object(data, schema)
            return len(errors) == 0, errors
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]
    
    @staticmethod
    def validate_csv_structure(file_path: str, expected_headers: List[str] = None) -> Tuple[bool, List[str]]:
        """Validate CSV file structure"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                if not headers:
                    errors.append("CSV file has no headers")
                    return False, errors
                
                # Check expected headers
                if expected_headers:
                    missing = set(expected_headers) - set(headers)
                    extra = set(headers) - set(expected_headers)
                    
                    if missing:
                        errors.append(f"Missing headers: {', '.join(missing)}")
                    if extra:
                        errors.append(f"Extra headers: {', '.join(extra)}")
                
                # Check for empty headers
                empty_headers = [h for h in headers if not h or not h.strip()]
                if empty_headers:
                    errors.append(f"Found {len(empty_headers)} empty header(s)")
                
                # Check rows
                row_count = 0
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                    row_count += 1
                    
                    # Check for completely empty rows
                    if all(not v or not v.strip() for v in row.values()):
                        errors.append(f"Row {row_num}: Completely empty")
                
                if row_count == 0:
                    errors.append("CSV file has no data rows")
                
                return len(errors) == 0, errors
                
        except Exception as e:
            return False, [f"Error reading CSV: {str(e)}"]
    
    @staticmethod
    def infer_column_types(file_path: str) -> Dict[str, str]:
        """Infer data types for CSV columns"""
        type_counts = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                for col, value in row.items():
                    if col not in type_counts:
                        type_counts[col] = {'int': 0, 'float': 0, 'bool': 0, 'string': 0, 'null': 0}
                    
                    if not value or value.strip().lower() in ('', 'null', 'none'):
                        type_counts[col]['null'] += 1
                    elif value.lower() in ('true', 'false'):
                        type_counts[col]['bool'] += 1
                    else:
                        try:
                            int(value)
                            type_counts[col]['int'] += 1
                        except ValueError:
                            try:
                                float(value)
                                type_counts[col]['float'] += 1
                            except ValueError:
                                type_counts[col]['string'] += 1
        
        # Determine dominant type for each column
        result = {}
        for col, counts in type_counts.items():
            # Remove null from consideration
            non_null_counts = {k: v for k, v in counts.items() if k != 'null'}
            if non_null_counts:
                dominant = max(non_null_counts, key=non_null_counts.get)
                result[col] = dominant
            else:
                result[col] = 'null'
        
        return result
    
    @staticmethod
    def validate_custom_rules(data: Any, rules: Dict) -> Tuple[bool, List[str]]:
        """Validate data against custom rules"""
        errors = []
        
        # Example rules format:
        # {
        #   "age": {"min": 0, "max": 150},
        #   "email": {"pattern": ".*@.*"},
        #   "status": {"enum": ["active", "inactive"]}
        # }
        
        if isinstance(data, list):
            for i, item in enumerate(data):
                item_errors = DataValidator._validate_item_rules(item, rules, f"item[{i}]")
                errors.extend(item_errors)
        else:
            errors = DataValidator._validate_item_rules(data, rules)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _validate_item_rules(item: Dict, rules: Dict, path: str = "") -> List[str]:
        """Validate a single item against rules"""
        errors = []
        
        for field, constraints in rules.items():
            if field not in item:
                continue
            
            value = item[field]
            prefix = f"{path}.{field}" if path else field
            
            # Min/max for numbers
            if 'min' in constraints:
                if isinstance(value, (int, float)) and value < constraints['min']:
                    errors.append(f"{prefix}: Value {value} is less than minimum {constraints['min']}")
            
            if 'max' in constraints:
                if isinstance(value, (int, float)) and value > constraints['max']:
                    errors.append(f"{prefix}: Value {value} exceeds maximum {constraints['max']}")
            
            # Enum values
            if 'enum' in constraints:
                if value not in constraints['enum']:
                    errors.append(f"{prefix}: Value '{value}' not in allowed values: {constraints['enum']}")
            
            # Pattern matching (simple)
            if 'pattern' in constraints:
                import re
                if not re.match(constraints['pattern'], str(value)):
                    errors.append(f"{prefix}: Value '{value}' does not match pattern '{constraints['pattern']}'")
            
            # Length constraints
            if 'minLength' in constraints:
                if len(str(value)) < constraints['minLength']:
                    errors.append(f"{prefix}: Length {len(str(value))} is less than minimum {constraints['minLength']}")
            
            if 'maxLength' in constraints:
                if len(str(value)) > constraints['maxLength']:
                    errors.append(f"{prefix}: Length {len(str(value))} exceeds maximum {constraints['maxLength']}")
        
        return errors


def main():
    parser = argparse.ArgumentParser(
        description='Data Toolkit - Data Validator'
    )
    
    parser.add_argument('--input', '-i', required=True, help='Input file path')
    parser.add_argument('--schema', '-s', help='JSON schema file')
    parser.add_argument('--rules', '-r', help='Custom rules file (YAML or JSON)')
    parser.add_argument('--check-headers', action='store_true', help='Validate CSV headers')
    parser.add_argument('--check-types', action='store_true', help='Infer and display column types')
    parser.add_argument('--expected-headers', help='Comma-separated list of expected headers')
    
    args = parser.parse_args()
    
    validator = DataValidator()
    all_valid = True
    
    try:
        # Detect file type
        ext = Path(args.input).suffix.lower()
        
        # Load data
        if ext == '.json':
            with open(args.input, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif ext in ('.yaml', '.yml'):
            if yaml is None:
                print("Error: PyYAML not installed", file=sys.stderr)
                sys.exit(1)
            with open(args.input, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif ext == '.csv':
            data = None  # CSV handled separately
        else:
            print(f"Error: Unsupported file type: {ext}", file=sys.stderr)
            sys.exit(1)
        
        # JSON Schema validation
        if args.schema:
            with open(args.schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            valid, errors = validator.validate_json_schema(data, schema)
            
            if valid:
                print("✓ JSON Schema validation passed")
            else:
                print("✗ JSON Schema validation failed:")
                for error in errors:
                    print(f"  - {error}")
                all_valid = False
        
        # CSV structure validation
        if ext == '.csv':
            expected = args.expected_headers.split(',') if args.expected_headers else None
            valid, errors = validator.validate_csv_structure(args.input, expected)
            
            if valid:
                print("✓ CSV structure validation passed")
            else:
                print("✗ CSV structure validation failed:")
                for error in errors:
                    print(f"  - {error}")
                all_valid = False
            
            # Type inference
            if args.check_types:
                types = validator.infer_column_types(args.input)
                print("\nInferred column types:")
                for col, dtype in types.items():
                    print(f"  {col}: {dtype}")
        
        # Custom rules validation
        if args.rules:
            with open(args.rules, 'r', encoding='utf-8') as f:
                if args.rules.endswith(('.yaml', '.yml')):
                    if yaml is None:
                        print("Error: PyYAML not installed", file=sys.stderr)
                        sys.exit(1)
                    rules = yaml.safe_load(f)
                else:
                    rules = json.load(f)
            
            valid, errors = validator.validate_custom_rules(data, rules)
            
            if valid:
                print("✓ Custom rules validation passed")
            else:
                print("✗ Custom rules validation failed:")
                for error in errors:
                    print(f"  - {error}")
                all_valid = False
        
        sys.exit(0 if all_valid else 1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
