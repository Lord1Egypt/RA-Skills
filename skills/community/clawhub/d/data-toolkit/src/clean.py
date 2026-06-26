#!/usr/bin/env python3
"""
Data Toolkit - Data Cleaner
Remove duplicates, handle nulls, normalize data
"""

import argparse
import json
import csv
import sys
import re
from typing import Any, Dict, List, Set
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

try:
    import yaml
except ImportError:
    yaml = None


class DataCleaner:
    """Data cleaning utilities"""
    
    @staticmethod
    def remove_duplicates(data: List[Dict], key: str = None) -> List[Dict]:
        """Remove duplicate entries"""
        if not data:
            return data
        
        if key:
            # Remove duplicates based on specific key
            seen = set()
            result = []
            
            for item in data:
                if isinstance(item, dict):
                    key_value = item.get(key)
                    if key_value not in seen:
                        seen.add(key_value)
                        result.append(item)
                else:
                    result.append(item)
            
            return result
        else:
            # Remove exact duplicates (convert dict to JSON string for hashing)
            seen = set()
            result = []
            
            for item in data:
                item_str = json.dumps(item, sort_keys=True)
                if item_str not in seen:
                    seen.add(item_str)
                    result.append(item)
            
            return result
    
    @staticmethod
    def handle_nulls(data: Any, action: str = 'remove', replacement: Any = None) -> Any:
        """Handle null/empty values"""
        
        def process_value(value: Any) -> Any:
            is_null = value is None or (isinstance(value, str) and value.strip() in ('', 'null', 'NULL', 'None', 'NONE'))
            
            if is_null:
                if action == 'remove':
                    return None  # Will be filtered out
                elif action == 'replace':
                    return replacement
            
            return value
        
        def process_dict(obj: Dict) -> Dict:
            result = {}
            for key, value in obj.items():
                if isinstance(value, dict):
                    result[key] = process_dict(value)
                elif isinstance(value, list):
                    result[key] = process_list(value)
                else:
                    processed = process_value(value)
                    if action != 'remove' or processed is not None:
                        result[key] = processed
            return result
        
        def process_list(lst: List) -> List:
            result = []
            for item in lst:
                if isinstance(item, dict):
                    result.append(process_dict(item))
                elif isinstance(item, list):
                    result.append(process_list(item))
                else:
                    processed = process_value(item)
                    if action != 'remove' or processed is not None:
                        result.append(processed)
            return result
        
        if isinstance(data, dict):
            return process_dict(data)
        elif isinstance(data, list):
            return process_list(data)
        else:
            return process_value(data)
    
    @staticmethod
    def normalize_strings(data: Any, operations: List[str] = None) -> Any:
        """Normalize string values"""
        if operations is None:
            operations = ['trim', 'lowercase']
        
        def normalize_value(value: str) -> str:
            if not isinstance(value, str):
                return value
            
            result = value
            
            if 'trim' in operations:
                result = result.strip()
            
            if 'collapse_spaces' in operations:
                result = re.sub(r'\s+', ' ', result)
            
            if 'lowercase' in operations:
                result = result.lower()
            
            if 'uppercase' in operations:
                result = result.upper()
            
            if 'title' in operations:
                result = result.title()
            
            return result
        
        def process_structure(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: process_structure(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [process_structure(item) for item in obj]
            elif isinstance(obj, str):
                return normalize_value(obj)
            else:
                return obj
        
        return process_structure(data)
    
    @staticmethod
    def normalize_dates(data: Any, target_format: str = 'ISO8601') -> Any:
        """Normalize date strings to a standard format"""
        
        # Common date patterns to recognize
        patterns = [
            (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', '%Y-%m-%dT%H:%M:%S'),  # ISO8601
            (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),  # YYYY-MM-DD
            (r'\d{2}/\d{2}/\d{4}', '%m/%d/%Y'),  # MM/DD/YYYY
            (r'\d{2}-\d{2}-\d{4}', '%m-%d-%Y'),  # MM-DD-YYYY
        ]
        
        def normalize_date_string(value: str) -> str:
            if not isinstance(value, str):
                return value
            
            for pattern, format_str in patterns:
                if re.match(pattern, value.strip()):
                    try:
                        dt = datetime.strptime(value.strip(), format_str)
                        
                        if target_format == 'ISO8601':
                            return dt.strftime('%Y-%m-%dT%H:%M:%S')
                        elif target_format == 'YYYY-MM-DD':
                            return dt.strftime('%Y-%m-%d')
                        elif target_format == 'MM/DD/YYYY':
                            return dt.strftime('%m/%d/%Y')
                        else:
                            return dt.strftime(target_format)
                    except ValueError:
                        pass
            
            return value
        
        def process_structure(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: process_structure(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [process_structure(item) for item in obj]
            elif isinstance(obj, str):
                return normalize_date_string(obj)
            else:
                return obj
        
        return process_structure(data)
    
    @staticmethod
    def normalize_numbers(data: Any, precision: int = 2) -> Any:
        """Normalize number formatting"""
        
        def normalize_number(value: Any) -> Any:
            if isinstance(value, float):
                return round(value, precision)
            elif isinstance(value, str):
                # Try to parse as number
                try:
                    # Remove common formatting
                    cleaned = value.replace(',', '').strip()
                    if '.' in cleaned:
                        return round(float(cleaned), precision)
                    else:
                        return int(cleaned)
                except ValueError:
                    return value
            else:
                return value
        
        def process_structure(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: process_structure(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [process_structure(item) for item in obj]
            else:
                return normalize_number(obj)
        
        return process_structure(data)
    
    @staticmethod
    def remove_columns(data: List[Dict], columns: List[str]) -> List[Dict]:
        """Remove specified columns from data"""
        result = []
        
        for item in data:
            if isinstance(item, dict):
                new_item = {k: v for k, v in item.items() if k not in columns}
                result.append(new_item)
            else:
                result.append(item)
        
        return result
    
    @staticmethod
    def rename_columns(data: List[Dict], mapping: Dict[str, str]) -> List[Dict]:
        """Rename columns according to mapping"""
        result = []
        
        for item in data:
            if isinstance(item, dict):
                new_item = {}
                for key, value in item.items():
                    new_key = mapping.get(key, key)
                    new_item[new_key] = value
                result.append(new_item)
            else:
                result.append(item)
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description='Data Toolkit - Data Cleaner'
    )
    
    parser.add_argument('--input', '-i', required=True, help='Input file path')
    parser.add_argument('--output', '-o', help='Output file path (default: overwrites input)')
    
    # Deduplication
    parser.add_argument('--dedupe', action='store_true', help='Remove duplicates')
    parser.add_argument('--key', help='Key field for deduplication')
    
    # Null handling
    parser.add_argument('--remove-nulls', action='store_true', help='Remove null values')
    parser.add_argument('--replace-nulls', help='Replace nulls with this value')
    
    # Normalization
    parser.add_argument('--normalize', choices=['strings', 'dates', 'numbers', 'all'], help='Normalize data')
    parser.add_argument('--date-format', default='ISO8601', help='Target date format')
    parser.add_argument('--number-precision', type=int, default=2, help='Number decimal precision')
    parser.add_argument('--string-ops', default='trim,collapse_spaces', help='String operations (comma-separated)')
    
    # Column operations
    parser.add_argument('--remove-columns', help='Columns to remove (comma-separated)')
    parser.add_argument('--rename-columns', help='Rename columns (format: old1:new1,old2:new2)')
    
    args = parser.parse_args()
    
    cleaner = DataCleaner()
    
    try:
        # Load data
        ext = Path(args.input).suffix.lower()
        
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
            # Load CSV as list of dicts
            with open(args.input, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        else:
            print(f"Error: Unsupported file type: {ext}", file=sys.stderr)
            sys.exit(1)
        
        operations_performed = []
        
        # Remove duplicates
        if args.dedupe:
            if isinstance(data, list):
                original_count = len(data)
                data = cleaner.remove_duplicates(data, args.key)
                removed = original_count - len(data)
                operations_performed.append(f"Removed {removed} duplicates")
        
        # Handle nulls
        if args.remove_nulls:
            data = cleaner.handle_nulls(data, action='remove')
            operations_performed.append("Removed null values")
        elif args.replace_nulls:
            data = cleaner.handle_nulls(data, action='replace', replacement=args.replace_nulls)
            operations_performed.append(f"Replaced nulls with '{args.replace_nulls}'")
        
        # Normalize
        if args.normalize:
            if args.normalize in ('strings', 'all'):
                ops = args.string_ops.split(',')
                data = cleaner.normalize_strings(data, ops)
                operations_performed.append(f"Normalized strings ({', '.join(ops)})")
            
            if args.normalize in ('dates', 'all'):
                data = cleaner.normalize_dates(data, args.date_format)
                operations_performed.append(f"Normalized dates to {args.date_format}")
            
            if args.normalize in ('numbers', 'all'):
                data = cleaner.normalize_numbers(data, args.number_precision)
                operations_performed.append(f"Normalized numbers (precision: {args.number_precision})")
        
        # Column operations
        if args.remove_columns and isinstance(data, list):
            cols = args.remove_columns.split(',')
            data = cleaner.remove_columns(data, cols)
            operations_performed.append(f"Removed columns: {', '.join(cols)}")
        
        if args.rename_columns and isinstance(data, list):
            mapping = {}
            for pair in args.rename_columns.split(','):
                old, new = pair.split(':')
                mapping[old.strip()] = new.strip()
            data = cleaner.rename_columns(data, mapping)
            operations_performed.append(f"Renamed {len(mapping)} column(s)")
        
        # Save output
        output_path = args.output or args.input
        
        if ext == '.json' or output_path.endswith('.json'):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif ext in ('.yaml', '.yml') or output_path.endswith(('.yaml', '.yml')):
            if yaml is None:
                print("Error: PyYAML not installed", file=sys.stderr)
                sys.exit(1)
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        elif ext == '.csv' or output_path.endswith('.csv'):
            if data and isinstance(data, list) and isinstance(data[0], dict):
                keys = list(data[0].keys())
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
        
        print(f"✓ Cleaned {args.input} → {output_path}")
        if operations_performed:
            print("\nOperations performed:")
            for op in operations_performed:
                print(f"  - {op}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
