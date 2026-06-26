#!/usr/bin/env python3
"""
Data Interpretation Script

Usage:
    python data_interpretation.py --query "QUERY" --file data.xlsx
    python data_interpretation.py --query "QUERY" --json '[{"col1": 1, "col2": 2}]'
    python data_interpretation.py --query "QUERY" --json data.json

Environment Variables:
    CHARTGEN_API_KEY: API key
"""
import argparse
import sys
import os
import json

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chartgen_api import ChartGenAPI


def parse_json_arg(json_arg: str) -> any:
    """
    Parse JSON argument (supports string or file path)
    
    Args:
        json_arg: JSON string or JSON file path
        
    Returns:
        Parsed Python object
    """
    if os.path.exists(json_arg):
        with open(json_arg, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return json.loads(json_arg)


def main():
    parser = argparse.ArgumentParser(
        description='Data Interpretation - Automatically generate data analysis conclusions and insights',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interpret from file
    python data_interpretation.py --query "Analyze sales trends" --file sales.xlsx
    
    # Interpret from JSON string
    python data_interpretation.py --query "Interpret the pattern of this data" --json '[{"month":"Jan","sales":100},{"month":"Feb","sales":150}]'
    
    # Interpret from JSON file
    python data_interpretation.py --query "Find anomalies" --json data.json
        """
    )
    parser.add_argument('--query', required=True, help='Interpretation query statement')
    parser.add_argument('--file', help='Input file path (.xlsx/.xls/.csv)')
    parser.add_argument('--json', help='JSON data (string or file path)')
    
    args = parser.parse_args()
    
    # Parameter validation
    if not args.file and not args.json:
        parser.error("Either --file or --json parameter must be provided")
    
    if args.file and args.json:
        print("Warning: Both --file and --json provided, will use --file", file=sys.stderr)
    
    try:
        api = ChartGenAPI()  # Read API Key from environment variable
        
        json_data = None
        if args.json and not args.file:
            json_data = parse_json_arg(args.json)
        
        result = api.interpret(
            query=args.query,
            file_path=args.file,
            json_data=json_data
        )
        
        print(result)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
