#!/usr/bin/env python3
"""
Data Analysis for Feishu - Main entry point
Unified interface for all chart generation requests
Version: 1.0.0
Repository: https://github.com/openclaw/data-analysis-for-feishu
License: MIT
"""
import argparse
import json
import asyncio
import sys
import os
from typing import List, Dict, Any

# Read version
VERSION = "1.0.0"
try:
    with open(os.path.join(os.path.dirname(__file__), "..", "VERSION"), "r") as f:
        VERSION = f.read().strip()
except:
    pass

from generate_echarts_screenshot import generate_chart_option, render_echarts_to_image
from data_parser import parse_excel, parse_bitable_records, parse_sheet_data, parse_csv
from auto_analyzer import analyze_data, generate_auto_analysis

def print_error(message: str):
    """Print error message in red color"""
    print(f"\033[91m❌ Error: {message}\033[0m", file=sys.stderr)

def print_success(message: str):
    """Print success message in green color"""
    print(f"\033[92m✅ Success: {message}\033[0m")

def print_info(message: str):
    """Print info message in blue color"""
    print(f"\033[94mℹ️ Info: {message}\033[0m")

def main():
    parser = argparse.ArgumentParser(description=f"Data Analysis for Feishu v{VERSION} - Generate ECharts visualizations optimized for Feishu")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--type", choices=["auto", "line", "area", "bar", "stack_bar", "pie", "donut", "gauge", "radar", "scatter", "funnel", "waterfall", "dual_axis"], default="auto", help="Chart type, 'auto' for automatic recommendation")
    parser.add_argument("--title", help="Chart title (auto-generated if not provided)")
    parser.add_argument("--output", required=True, help="Output PNG file path")
    parser.add_argument("--auto-analyze", action="store_true", default=True, help="Enable automatic data analysis and conclusion generation")
    
    # Data source options
    parser.add_argument("--excel", help="Excel file path")
    parser.add_argument("--csv", help="CSV file path")
    parser.add_argument("--sheet", help="Excel sheet name (optional)")
    parser.add_argument("--bitable-records", type=json.loads, help="Feishu Bitable records JSON")
    parser.add_argument("--sheet-data", type=json.loads, help="Feishu Sheet values JSON")
    parser.add_argument("--markdown-table", help="Markdown format table string")
    
    # Data mapping options
    parser.add_argument("--x-axis-field", help="Field name for X-axis (line/bar chart)")
    parser.add_argument("--y-axis-field", help="Field name(s) for Y-axis, comma-separated for multiple series")
    parser.add_argument("--label-field", help="Field name for labels (pie/funnel chart)")
    parser.add_argument("--value-field", help="Field name for values (pie/funnel chart)")
    parser.add_argument("--y-name", default="", help="Y-axis name")
    
    # Raw data options
    parser.add_argument("--x-axis", nargs="+", help="Raw X-axis data")
    parser.add_argument("--y-axis", nargs="+", type=float, help="Raw Y-axis data")
    parser.add_argument("--labels", nargs="+", help="Raw labels data")
    parser.add_argument("--values", nargs="+", type=float, help="Raw values data")
    parser.add_argument("--value", type=float, help="Single value for gauge chart")
    parser.add_argument("--max", type=float, default=100, help="Max value for gauge chart")
    parser.add_argument("--unit", default="%", help="Unit for gauge chart")
    parser.add_argument("--indicators", type=json.loads, help="Radar chart indicators JSON")
    parser.add_argument("--series-name", default="", help="Series name for radar chart")
    
    # Multi-series parameters
    parser.add_argument("--series-names", default="", help="Comma-separated series names")
    parser.add_argument("--stack", action="store_true", help="Enable stacked chart")
    parser.add_argument("--area", action="store_true", help="Enable area fill for line chart")
    
    # Dual axis parameters
    parser.add_argument("--y1-axis", nargs="+", type=float, help="Left Y-axis data (dual_axis)")
    parser.add_argument("--y2-axis", nargs="+", type=float, help="Right Y-axis data (dual_axis)")
    parser.add_argument("--y1-name", default="", help="Left Y-axis name")
    parser.add_argument("--y2-name", default="", help="Right Y-axis name")
    
    # Output options
    parser.add_argument("--width", type=int, default=1200, help="Chart width")
    parser.add_argument("--height", type=int, default=750, help="Chart height")
    parser.add_argument("--analysis-output", help="Path to save analysis conclusion text file")
    
    args = parser.parse_args()
    
    try:
        # Parse data from source
        data = None
        if args.excel:
            print_info(f"Parsing Excel file: {args.excel}")
            data = parse_excel(args.excel, args.sheet)
            print_success(f"Parsed {len(data)} rows of data")
        elif args.csv:
            print_info(f"Parsing CSV file: {args.csv}")
            data = parse_csv(args.csv)
            print_success(f"Parsed {len(data)} rows of data")
        elif args.bitable_records:
            print_info(f"Parsing Feishu Bitable records")
            data = parse_bitable_records(args.bitable_records)
            print_success(f"Parsed {len(data)} rows of data")
        elif args.sheet_data:
            print_info(f"Parsing Feishu Sheet data")
            data = parse_sheet_data(args.sheet_data)
            print_success(f"Parsed {len(data)} rows of data")
        elif args.markdown_table:
            print_info(f"Parsing Markdown table")
            # Simple markdown table parsing
            lines = args.markdown_table.strip().split("\n")
            lines = [line.strip() for line in lines if line.strip() and not line.startswith("|---")]
            headers = [h.strip() for h in lines[0].strip("|").split("|")]
            data = []
            for line in lines[1:]:
                values = [v.strip() for v in line.strip("|").split("|")]
                data.append(dict(zip(headers, values)))
            print_success(f"Parsed {len(data)} rows of data")
        
        # Auto analysis if enabled
        analysis_result = None
        if args.auto_analyze and data:
            print_info("Analyzing data characteristics...")
            analysis_result = analyze_data(data)
            print_info(f"Recommended chart type: {analysis_result['recommended_chart']}")
            print_info(f"Recommendation reason: {analysis_result['recommendation_reason']}")
            
            # Auto fill parameters if not provided
            if args.type == "auto":
                args.type = analysis_result["recommended_chart"]
                if "recommended_fields" in analysis_result:
                    for field, value in analysis_result["recommended_fields"].items():
                        if not getattr(args, field, None):
                            setattr(args, field, value)
            
            # Auto generate title if not provided
            if not args.title:
                args.title = f"Data Analysis Chart"
        
        # Extract data fields if using data source
        fields_used = {}
        if data:
            if args.type in ["line", "area", "bar", "stack_bar", "scatter", "waterfall"]:
                if not args.x_axis_field or not args.y_axis_field:
                    print_error("Please specify --x-axis-field and --y-axis-field")
                    sys.exit(1)
                
                # Support multiple y-axis fields
                y_fields = [f.strip() for f in args.y_axis_field.split(",")]
                args.multi_series = len(y_fields) > 1
                
                args.x_axis = [item[args.x_axis_field] for item in data if item.get(args.x_axis_field) is not None]
                y_axis_data = []
                for y_field in y_fields:
                    y_data = [float(item[y_field]) for item in data if item.get(y_field) is not None]
                    y_axis_data.append(y_data)
                
                if args.multi_series:
                    args.y_axis = y_axis_data
                    if not args.series_names:
                        args.series_names = ",".join(y_fields)
                else:
                    args.y_axis = y_axis_data[0]
                
                fields_used["x_axis"] = args.x_axis_field
                fields_used["y_axis"] = args.y_axis_field
                print_info(f"Extracted X-axis: {len(args.x_axis)} items, Y-axis: {len(y_axis_data)} series")
            
            elif args.type in ["pie", "donut", "funnel"]:
                if not args.label_field or not args.value_field:
                    print_error("Please specify --label-field and --value-field")
                    sys.exit(1)
                args.labels = [str(item[args.label_field]) for item in data if item.get(args.label_field) is not None]
                args.values = [float(item[args.value_field]) for item in data if item.get(args.value_field) is not None]
                fields_used["label_field"] = args.label_field
                fields_used["value_field"] = args.value_field
                print_info(f"Extracted labels: {len(args.labels)} items, values: {len(args.values)} items")
        
        # Handle stacked bar
        if args.stack and args.type == "bar":
            args.type = "stack_bar"
        
        # Handle area line
        if args.area and args.type == "line":
            args.type = "area"
        
        # Validate data
        if args.type in ["line", "area", "bar", "stack_bar"]:
            if not args.x_axis or not args.y_axis:
                print_error("Missing X-axis or Y-axis data")
                sys.exit(1)
        
        elif args.type in ["pie", "donut", "funnel"]:
            if not args.labels or not args.values or len(args.labels) != len(args.values):
                print_error("Labels and values must have the same length")
                sys.exit(1)
        
        elif args.type == "gauge":
            if args.value is None:
                print_error("Please provide --value for gauge chart")
                sys.exit(1)
            fields_used["value"] = args.value
            fields_used["max"] = args.max
        
        # Generate chart option
        print_info(f"Generating {args.type} chart: {args.title}")
        option = generate_chart_option(args)
        
        # Render to image
        asyncio.run(render_echarts_to_image(option, args.output, args.width, args.height))
        print_success(f"Chart saved to: {args.output}")
        
        # Generate and save analysis conclusion
        if args.auto_analyze:
            if data:
                analysis_text = generate_auto_analysis(data, args.type, fields_used)
            else:
                analysis_text = "📊 **Chart generated successfully**"
            
            if args.analysis_output:
                with open(args.analysis_output, "w", encoding="utf-8") as f:
                    f.write(analysis_text)
                print_success(f"Analysis conclusion saved to: {args.analysis_output}")
            
            # Print analysis
            print("\n" + analysis_text + "\n")
        
    except Exception as e:
        print_error(f"Generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
