#!/usr/bin/env python3
"""
Data Analysis Script

Usage:
    python data_analysis.py --query "QUERY" --file data.xlsx
    python data_analysis.py --query "QUERY" --json '[{"col1": 1, "col2": 2}]'
    python data_analysis.py --query "QUERY" --json data.json

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
        description='Data Analysis - Execute precise data retrieval and analysis through natural language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze from file
    python data_analysis.py --query "Calculate total sales by product" --file sales.xlsx
    
    # Analyze from JSON string
    python data_analysis.py --query "Calculate average" --json '[{"name":"A","value":10},{"name":"B","value":20}]'
    
    # Analyze from JSON file
    python data_analysis.py --query "Filter data greater than 15" --json data.json
        """
    )
    parser.add_argument('--query', required=True, help='Analysis query statement')
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
        
        result = api.analyze(
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
