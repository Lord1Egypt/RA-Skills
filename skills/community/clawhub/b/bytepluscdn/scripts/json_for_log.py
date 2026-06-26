import json
import argparse
import sys
import os

def escape_json_file(input_file, output_file=None):
    """
    Reads a JSON file, parses it, and serializes it into a single-line compact JSON string.
    This is useful for passing large JSON credentials (like GCP Service Accounts) 
    as command-line arguments without running into length or newline issues.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Serialize to JSON string, then serialize THAT string to get the escaped format BigQuery needs
        # e.g., {"type":"..."} -> "{\"type\":\"...\"}"
        escaped_json = json.dumps(json.dumps(data))
        # Remove the outer quotes
        escaped_json = escaped_json[1:-1]
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(escaped_json)
            print(f"Successfully escaped JSON to '{output_file}'")
        else:
            # Print to stdout so it can be captured or copied
            print(escaped_json)
            
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{input_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Escape a JSON file into a single-line compact string.")
    parser.add_argument("input_file", help="Path to the original JSON file (e.g., GCP credentials)")
    parser.add_argument("-o", "--output", help="Optional path to save the escaped JSON string. If omitted, prints to stdout.")
    
    args = parser.parse_args()
    escape_json_file(args.input_file, args.output)
