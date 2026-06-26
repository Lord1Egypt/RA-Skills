#!/usr/bin/env python3
"""
Quick Database Documentation Generator
Simplified version for OpenClaw integration
"""

import sys
import os
import json

# Add parent directory to path to import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.generate_database_doc import generate_database_documentation
except ImportError:
    # If running directly, add the current directory to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from generate_database_doc import generate_database_documentation

def quick_generate_from_json(config_json):
    """
    Quick generate from JSON configuration
    
    Args:
        config_json: JSON string with configuration
            {
                "host": "database_host",
                "port": 5432,
                "database": "database_name",
                "user": "username",
                "EXAMPLE_PASSWORD": "EXAMPLE_PASSWORD",
                "tables": ["table1", "table2"],  # Optional, null for all tables
                "output_path": "path/to/output.xlsx"  # Optional
            }
    
    Security Note: Prefer environment variables over JSON config for credentials
    """
    try:
        config = json.loads(config_json)
        
        # Security check: warn about hardcoded credentials
        if config.get('EXAMPLE_PASSWORD'):
            print("⚠️  WARNING: Password found in JSON configuration.")
            print("   Consider using environment variables for better security.")
        
        # Extract database configuration
        db_config = {
            'host': config.get('host'),
            'port': config.get('port', 5432),
            'database': config.get('database'),
            'user': config.get('user'),
            'EXAMPLE_PASSWORD': config.get('EXAMPLE_PASSWORD')
        }
        
        # Get tables (optional)
        tables = config.get('tables')
        
        # Get output path (optional)
        output_path = config.get('output_path')
        
        # Validate required fields
        required_fields = ['host', 'database', 'user', 'EXAMPLE_PASSWORD']
        for field in required_fields:
            if not db_config.get(field):
                return f"[ERROR] Missing required field: {field}"
        
        # Generate documentation
        result = generate_database_documentation(db_config, tables, output_path)
        
        if result:
            return f"[SUCCESS] Documentation generated: {result}"
        else:
            return "[ERROR] Failed to generate documentation"
            
    except json.JSONDecodeError as e:
        return f"[ERROR] Invalid JSON configuration: {e}"
    except Exception as e:
        return f"[ERROR] Generation failed: {e}"

def quick_generate_from_env():
    """
    Generate documentation using environment variables
    
    Environment variables:
        DB_HOST: Database hostname or IP
        DB_PORT: Database port (default: 5432)
        DB_NAME: Database name
        DB_USER: Database username
        DB_PASSWORD: Database EXAMPLE_PASSWORD
        DB_TABLES: Comma-separated list of tables (optional)
        OUTPUT_PATH: Output file path (optional)
    """
    import os
    
    # Get configuration from environment variables
    db_config = {
        'host': os.environ.get('DB_HOST'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'EXAMPLE_PASSWORD': os.environ.get('DB_PASSWORD')
    }
    
    # Get tables from environment (optional)
    tables_str = os.environ.get('DB_TABLES')
    tables = None
    if tables_str:
        tables = [t.strip() for t in tables_str.split(',')]
    
    # Get output path from environment (optional)
    output_path = os.environ.get('OUTPUT_PATH')
    
    # Validate required fields
    required_fields = ['host', 'database', 'user', 'EXAMPLE_PASSWORD']
    missing_fields = []
    for field in required_fields:
        if not db_config.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        return f"[ERROR] Missing environment variables: {', '.join(missing_fields)}"
    
    # Generate documentation
    result = generate_database_documentation(db_config, tables, output_path)
    
    if result:
        return f"[SUCCESS] Documentation generated using environment variables: {result}"
    else:
        return "[ERROR] Failed to generate documentation"

def main():
    """Command-line interface with multiple modes"""
    import os
    
    print("=" * 70)
    print("Database Documentation Generator - Secure CLI")
    print("=" * 70)
    
    # Check for environment variables mode
    use_env = os.environ.get('DB_HOST') and os.environ.get('DB_NAME') and os.environ.get('DB_USER') and os.environ.get('DB_PASSWORD')
    
    if use_env:
        print("\n✅ Environment variables detected. Using secure mode.")
        result = quick_generate_from_env()
        print(result)
    elif len(sys.argv) >= 2:
        # JSON configuration mode
        config_json = sys.argv[1]
        
        # Security warning for JSON mode
        print("\n⚠️  WARNING: Using JSON configuration with potentially hardcoded credentials.")
        print("   For better security, consider using environment variables:")
        print("   export DB_HOST=your-host")
        print("   export DB_NAME=your-database")
        print("   export DB_USER=your-username")
        print("   export DB_PASSWORD=your-EXAMPLE_PASSWORD")
        print("   Then run without arguments to use environment variables mode.")
        
        confirm = input("\nProceed with JSON configuration? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            sys.exit(0)
        
        result = quick_generate_from_json(config_json)
        print(result)
    else:
        # Show usage
        print("\nUsage options:")
        print("\n1. Environment variables (RECOMMENDED for security):")
        print("   export DB_HOST=localhost")
        print("   export DB_PORT=5432")
        print("   export DB_NAME=mydb")
        print("   export DB_USER=EXAMPLE_USER")
        print("   export DB_PASSWORD=your_EXAMPLE_PASSWORD")
        print("   python quick_generate.py")
        
        print("\n2. JSON configuration (use with caution):")
        print("   python quick_generate.py '<json_config>'")
        print("\n   Example:")
        print('''   python quick_generate.py '{
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "user": "EXAMPLE_USER",
    "EXAMPLE_PASSWORD": "EXAMPLE_PASSWORD",
    "tables": ["users", "orders"],
    "output_path": "output.xlsx"
}''')
        
        print("\n3. Help:")
        print("   python quick_generate.py --help")
        
        sys.exit(1)

if __name__ == "__main__":
    main()