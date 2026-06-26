#!/usr/bin/env python3
"""
CSV Data Explorer CLI
Explore, analyze, and visualize CSV data from terminal.
"""

import argparse
import csv
import json
import os
import sys
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

try:
    import pandas as pd
    import numpy as np
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: 'pandas' library not found. Install with: pip3 install pandas")
    print("Basic CSV reading will use Python's built-in csv module.")

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def detect_delimiter(filepath: str) -> str:
    """Detect CSV delimiter by analyzing first few lines."""
    delimiters = [',', ';', '\t', '|']
    try:
        with open(filepath, 'r') as f:
            sample = f.read(4096)
        
        # Count occurrences of each delimiter
        counts = {}
        for delim in delimiters:
            counts[delim] = sample.count(delim)
        
        # Return delimiter with highest count
        return max(counts.items(), key=lambda x: x[1])[0]
    except:
        return ','  # Default to comma


def load_csv_pandas(filepath: str, limit: Optional[int] = None) -> 'pd.DataFrame':
    """Load CSV using pandas (preferred)."""
    if not HAS_PANDAS:
        raise ImportError("pandas is required for this operation")
    
    try:
        # Try to detect delimiter
        delimiter = detect_delimiter(filepath)
        
        # Load CSV
        df = pd.read_csv(filepath, delimiter=delimiter, nrows=limit)
        return df
    except Exception as e:
        print(f"Error loading CSV with pandas: {e}")
        # Fall back to basic CSV reader
        raise


def load_csv_basic(filepath: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
    """Load CSV using Python's built-in csv module."""
    delimiter = detect_delimiter(filepath)
    data = []
    
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for i, row in enumerate(reader):
                if limit and i >= limit:
                    break
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []


def print_preview(df: 'pd.DataFrame', limit: int = 10) -> None:
    """Print preview of DataFrame."""
    print(f"\nCSV File Preview ({len(df)} rows × {len(df.columns)} columns)")
    print("=" * 80)
    
    # Show first few rows
    print(f"First {min(limit, len(df))} rows:")
    print(df.head(limit).to_string())
    
    print(f"\nLast {min(limit, len(df))} rows:")
    print(df.tail(limit).to_string())
    
    # Column information
    print(f"\nColumn Information:")
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        total = len(df)
        null_percent = ((total - non_null) / total * 100) if total > 0 else 0
        
        # Get unique values count for object/string columns
        if dtype == 'object':
            unique_count = df[col].nunique()
            print(f"  - {col}: {dtype}, {non_null}/{total} non-null ({null_percent:.1f}% null), {unique_count} unique values")
        else:
            print(f"  - {col}: {dtype}, {non_null}/{total} non-null ({null_percent:.1f}% null)")


def print_statistics(df: 'pd.DataFrame') -> None:
    """Print statistics for DataFrame."""
    print(f"\nStatistics Summary")
    print("=" * 80)
    
    # Overall statistics
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns):,}")
    
    # Memory usage (pandas only)
    if HAS_PANDAS:
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        print(f"Memory usage: {memory_mb:.2f} MB")
    
    print(f"\nColumn Statistics:")
    
    for col in df.columns:
        print(f"\n  {col}:")
        
        # Data type
        dtype = str(df[col].dtype)
        print(f"    Type: {dtype}")
        
        # Non-null count
        non_null = df[col].count()
        total = len(df)
        null_count = total - non_null
        null_percent = (null_count / total * 100) if total > 0 else 0
        print(f"    Non-null: {non_null}/{total} ({null_percent:.1f}% null)")
        
        # For numeric columns
        if dtype in ['int64', 'float64', 'int32', 'float32']:
            try:
                print(f"    Mean: {df[col].mean():.2f}")
                print(f"    Median: {df[col].median():.2f}")
                print(f"    Std: {df[col].std():.2f}")
                print(f"    Min: {df[col].min():.2f}")
                print(f"    Max: {df[col].max():.2f}")
                print(f"    25%: {df[col].quantile(0.25):.2f}")
                print(f"    50%: {df[col].quantile(0.50):.2f}")
                print(f"    75%: {df[col].quantile(0.75):.2f}")
            except:
                pass
        
        # For object/string columns
        elif dtype == 'object':
            unique_count = df[col].nunique()
            print(f"    Unique values: {unique_count}")
            
            if unique_count <= 10:
                # Show value counts for columns with few unique values
                value_counts = df[col].value_counts().head(5)
                print(f"    Top values:")
                for value, count in value_counts.items():
                    percent = (count / total * 100) if total > 0 else 0
                    print(f"      '{value}': {count} ({percent:.1f}%)")


def filter_dataframe(df: 'pd.DataFrame', condition: str) -> 'pd.DataFrame':
    """Filter DataFrame based on condition string."""
    if not HAS_PANDAS:
        print("Error: pandas required for filtering")
        return df
    
    try:
        # Simple condition parsing
        # Support basic conditions: column == value, column > value, column < value
        # For now, use pandas query (but be careful with security)
        # In production, would need proper parsing/sanitization
        if condition:
            # Basic safety check
            if any(op in condition for op in ['import', 'exec', 'eval', '__']):
                print("Error: Invalid condition - contains unsafe operations")
                return df
            
            try:
                filtered = df.query(condition, engine='python')
                print(f"Filtered from {len(df)} to {len(filtered)} rows")
                return filtered
            except:
                print(f"Error parsing condition: {condition}")
                print("Try format: 'column > value' or 'column == \"string\"'")
                return df
        else:
            return df
    except Exception as e:
        print(f"Error filtering data: {e}")
        return df


def select_columns(df: 'pd.DataFrame', columns: List[str]) -> 'pd.DataFrame':
    """Select specific columns from DataFrame."""
    if not HAS_PANDAS:
        print("Error: pandas required for column selection")
        return df
    
    try:
        # Check if columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            print(f"Warning: Columns not found: {missing_cols}")
            print(f"Available columns: {list(df.columns)}")
            columns = [col for col in columns if col in df.columns]
        
        if columns:
            selected = df[columns]
            print(f"Selected {len(columns)} columns: {columns}")
            return selected
        else:
            print("No valid columns selected")
            return df
    except Exception as e:
        print(f"Error selecting columns: {e}")
        return df


def create_histogram_ascii(values: List[float], bins: int = 10) -> None:
    """Create ASCII histogram for terminal display."""
    if not values:
        print("No numeric data for histogram")
        return
    
    # Calculate histogram
    min_val = min(values)
    max_val = max(values)
    bin_width = (max_val - min_val) / bins
    
    # Create bins
    histogram = [0] * bins
    for value in values:
        if bin_width > 0:
            bin_idx = min(int((value - min_val) / bin_width), bins - 1)
            histogram[bin_idx] += 1
    
    # Print histogram
    max_count = max(histogram) if histogram else 1
    scale = 50 / max_count if max_count > 0 else 1
    
    print(f"\nHistogram ({len(values)} values, {bins} bins)")
    print("-" * 60)
    
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        count = histogram[i]
        bar = '█' * int(count * scale)
        print(f"[{bin_start:7.2f} - {bin_end:7.2f}] {bar} {count}")


def create_histogram_matplotlib(df: 'pd.DataFrame', column: str, bins: int = 10) -> None:
    """Create histogram using matplotlib."""
    if not HAS_MATPLOTLIB:
        print("matplotlib not available, using ASCII histogram")
        # Fall back to ASCII
        if column in df.columns and HAS_PANDAS:
            numeric_data = pd.to_numeric(df[column], errors='coerce').dropna()
            create_histogram_ascii(numeric_data.tolist(), bins)
        return
    
    try:
        plt.figure(figsize=(10, 6))
        df[column].hist(bins=bins, edgecolor='black')
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        # Save to file or show
        output_file = f"histogram_{column}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(output_file)
        print(f"Histogram saved to: {output_file}")
        plt.close()
    except Exception as e:
        print(f"Error creating matplotlib histogram: {e}")
        # Fall back to ASCII
        if column in df.columns and HAS_PANDAS:
            numeric_data = pd.to_numeric(df[column], errors='coerce').dropna()
            create_histogram_ascii(numeric_data.tolist(), bins)


def show_unique_values(df: 'pd.DataFrame', column: str, limit: int = 20) -> None:
    """Show unique values in a column."""
    if not HAS_PANDAS:
        print("Error: pandas required for unique value analysis")
        return
    
    if column not in df.columns:
        print(f"Column '{column}' not found")
        print(f"Available columns: {list(df.columns)}")
        return
    
    value_counts = df[column].value_counts()
    total = len(df)
    
    print(f"\nUnique values in '{column}' ({len(value_counts)} unique, {total} total)")
    print("-" * 60)
    
    for i, (value, count) in enumerate(value_counts.head(limit).items()):
        percent = (count / total * 100) if total > 0 else 0
        print(f"{i+1:3}. '{value}' - {count:6} ({percent:5.1f}%)")
    
    if len(value_counts) > limit:
        print(f"... and {len(value_counts) - limit} more unique values")


def export_data(df: 'pd.DataFrame', output_path: str, format: str = 'csv') -> None:
    """Export DataFrame to file."""
    if not HAS_PANDAS:
        print("Error: pandas required for export")
        return
    
    try:
        if format.lower() == 'csv':
            df.to_csv(output_path, index=False)
            print(f"Exported {len(df)} rows to CSV: {output_path}")
        elif format.lower() == 'json':
            df.to_json(output_path, orient='records', indent=2)
            print(f"Exported {len(df)} rows to JSON: {output_path}")
        else:
            print(f"Unsupported format: {format}")
    except Exception as e:
        print(f"Error exporting data: {e}")


def handle_preview(args):
    """Handle preview command."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    try:
        if HAS_PANDAS:
            df = load_csv_pandas(args.file, args.limit)
            print_preview(df, args.limit)
        else:
            data = load_csv_basic(args.file, args.limit)
            if data:
                print(f"CSV File: {args.file} ({len(data)} rows)")
                print("First few rows:")
                for i, row in enumerate(data[:min(args.limit, len(data))]):
                    print(f"Row {i+1}: {row}")
    except Exception as e:
        print(f"Error previewing file: {e}")


def handle_stats(args):
    """Handle stats command."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    if not HAS_PANDAS:
        print("Error: pandas required for statistics")
        print("Install with: pip3 install pandas")
        return
    
    try:
        df = load_csv_pandas(args.file)
        print_statistics(df)
    except Exception as e:
        print(f"Error calculating statistics: {e}")


def handle_filter(args):
    """Handle filter command."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    if not HAS_PANDAS:
        print("Error: pandas required for filtering")
        print("Install with: pip3 install pandas")
        return
    
    try:
        df = load_csv_pandas(args.file)
        
        # Apply filter if condition provided
        if args.where:
            df = filter_dataframe(df, args.where)
        
        # Select columns if specified
        if args.columns:
            columns = [col.strip() for col in args.columns.split(',')]
            df = select_columns(df, columns)
        
        # Show preview if requested
        if args.preview:
            print_preview(df, args.preview_limit)
        
        # Show statistics if requested
        if args.stats:
            print_statistics(df)
        
        # Export if output specified
        if args.output:
            export_data(df, args.output)
        
    except Exception as e:
        print(f"Error filtering data: {e}")


def handle_select(args):
    """Handle select command."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    if not HAS_PANDAS:
        print("Error: pandas required for column selection")
        print("Install with: pip3 install pandas")
        return
    
    try:
        df = load_csv_pandas(args.file)
        
        # Select columns
        columns = [col.strip() for col in args.columns.split(',')]
        df = select_columns(df, columns)
        
        # Show preview
        print_preview(df, args.limit)
        
        # Export if output specified
        if args.output:
            export_data(df, args.output)
        
    except Exception as e:
        print(f"Error selecting columns: {e}")


def handle_histogram(args):
    """Handle histogram command."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    if not HAS_PANDAS:
        print("Error: pandas required for histograms")
        print("Install with: pip3 install pandas")
        return
    
    try:
        df = load_csv_pandas(args.file)
        
        if args.column not in df.columns:
            print(f"Column '{args.column}' not found")
            print(f"Available columns: {list(df.columns)}")
            return
        
        # Check if column is numeric
        try:
            numeric_data = pd.to_numeric(df[args.column], errors='coerce').dropna()
            if len(numeric_data) == 0:
                print(f"Column '{args.column}' contains no numeric data")
                return
            
            # Create histogram
            if HAS_MATPLOTLIB and args.matplotlib:
                create_histogram_matplotlib(df, args.column, args.bins)
            else:
                create_histogram_ascii(numeric_data.tolist(), args.bins)
                
        except Exception as e:
            print(f"Error creating histogram: {e}")
            
    except Exception as e:
        print(f"Error loading file: {e}")


def handle_unique(args):
    """Handle unique command."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    if not HAS_PANDAS:
        print("Error: pandas required for unique value analysis")
        print("Install with: pip3 install pandas")
        return
    
    try:
        df = load_csv_pandas(args.file)
        show_unique_values(df, args.column, args.limit)
    except Exception as e:
        print(f"Error analyzing unique values: {e}")


def handle_interactive(args):
    """Handle interactive mode."""
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return
    
    if not HAS_PANDAS:
        print("Error: pandas required for interactive mode")
        print("Install with: pip3 install pandas")
        return
    
    print("CSV Data Explorer - Interactive Mode")
    print("=" * 50)
    
    try:
        df = load_csv_pandas(args.file)
        print(f"Loaded: {args.file} ({len(df)} rows × {len(df.columns)} columns)")
        
        while True:
            print(f"\nOptions:")
            print("  1. Preview data")
            print("  2. Show statistics")
            print("  3. Filter rows")
            print("  4. Select columns")
            print("  5. Create histogram")
            print("  6. Show unique values")
            print("  7. Export data")
            print("  8. Exit")
            
            try:
                choice = input("\nSelect option (1-8): ").strip()
                
                if choice == '1':
                    limit = input("Number of rows to show (default 10): ").strip()
                    limit = int(limit) if limit else 10
                    print_preview(df, limit)
                
                elif choice == '2':
                    print_statistics(df)
                
                elif choice == '3':
                    condition = input("Filter condition (e.g., 'age > 30'): ").strip()
                    if condition:
                        df = filter_dataframe(df, condition)
                
                elif choice == '4':
                    columns_input = input("Columns to select (comma-separated): ").strip()
                    if columns_input:
                        columns = [col.strip() for col in columns_input.split(',')]
                        df = select_columns(df, columns)
                
                elif choice == '5':
                    column = input("Column for histogram: ").strip()
                    if column and column in df.columns:
                        bins = input("Number of bins (default 10): ").strip()
                        bins = int(bins) if bins else 10
                        use_matplotlib = input("Use matplotlib? (y/n, default n): ").strip().lower() == 'y'
                        
                        # Create histogram
                        try:
                            numeric_data = pd.to_numeric(df[column], errors='coerce').dropna()
                            if use_matplotlib and HAS_MATPLOTLIB:
                                create_histogram_matplotlib(df, column, bins)
                            else:
                                create_histogram_ascii(numeric_data.tolist(), bins)
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        print(f"Column '{column}' not found")
                
                elif choice == '6':
                    column = input("Column for unique values: ").strip()
                    if column and column in df.columns:
                        limit = input("Limit (default 20): ").strip()
                        limit = int(limit) if limit else 20
                        show_unique_values(df, column, limit)
                    else:
                        print(f"Column '{column}' not found")
                
                elif choice == '7':
                    format_choice = input("Export format (csv/json, default csv): ").strip().lower() or 'csv'
                    if format_choice in ['csv', 'json']:
                        default_name = f"export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.{format_choice}"
                        output_path = input(f"Output path (default {default_name}): ").strip() or default_name
                        export_data(df, output_path, format_choice)
                    else:
                        print("Invalid format. Use 'csv' or 'json'")
                
                elif choice == '8':
                    print("Exiting interactive mode")
                    break
                
                else:
                    print("Invalid choice. Please select 1-8.")
                    
            except (KeyboardInterrupt, EOFError):
                print("\nExiting interactive mode")
                break
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Error in interactive mode: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="CSV Data Explorer - Analyze CSV files in terminal"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview CSV file")
    preview_parser.add_argument("file", help="CSV file path")
    preview_parser.add_argument("--limit", type=int, default=10, help="Number of rows to show (default: 10)")
    preview_parser.set_defaults(func=handle_preview)
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics for CSV file")
    stats_parser.add_argument("file", help="CSV file path")
    stats_parser.set_defaults(func=handle_stats)
    
    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Filter CSV rows")
    filter_parser.add_argument("file", help="CSV file path")
    filter_parser.add_argument("--where", help="Filter condition (e.g., 'age > 30')")
    filter_parser.add_argument("--columns", help="Columns to select (comma-separated)")
    filter_parser.add_argument("--preview", action="store_true", help="Show preview after filtering")
    filter_parser.add_argument("--preview-limit", type=int, default=10, help="Preview row limit (default: 10)")
    filter_parser.add_argument("--stats", action="store_true", help="Show statistics after filtering")
    filter_parser.add_argument("--output", help="Output file for filtered data")
    filter_parser.set_defaults(func=handle_filter)
    
    # Select command
    select_parser = subparsers.add_parser("select", help="Select specific columns")
    select_parser.add_argument("file", help="CSV file path")
    select_parser.add_argument("--columns", required=True, help="Columns to select (comma-separated)")
    select_parser.add_argument("--limit", type=int, default=10, help="Preview row limit (default: 10)")
    select_parser.add_argument("--output", help="Output file for selected data")
    select_parser.set_defaults(func=handle_select)
    
    # Histogram command
    hist_parser = subparsers.add_parser("histogram", help="Create histogram for a column")
    hist_parser.add_argument("file", help="CSV file path")
    hist_parser.add_argument("--column", required=True, help="Column for histogram")
    hist_parser.add_argument("--bins", type=int, default=10, help="Number of bins (default: 10)")
    hist_parser.add_argument("--matplotlib", action="store_true", help="Use matplotlib for visualization")
    hist_parser.set_defaults(func=handle_histogram)
    
    # Unique command
    unique_parser = subparsers.add_parser("unique", help="Show unique values in a column")
    unique_parser.add_argument("file", help="CSV file path")
    unique_parser.add_argument("--column", required=True, help="Column for unique values")
    unique_parser.add_argument("--limit", type=int, default=20, help="Limit number of values shown (default: 20)")
    unique_parser.set_defaults(func=handle_unique)
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive exploration mode")
    interactive_parser.add_argument("file", help="CSV file path")
    interactive_parser.set_defaults(func=handle_interactive)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check for pandas
    if args.command not in ['preview'] and not HAS_PANDAS:
        print(f"Error: Command '{args.command}' requires pandas library")
        print("Install with: pip3 install pandas")
        if args.command in ['histogram']:
            print("For matplotlib visualizations, also install: pip3 install matplotlib")
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()