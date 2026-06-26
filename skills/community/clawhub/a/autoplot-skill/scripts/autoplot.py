#!/usr/bin/env python3
"""
AutoPlot - Automatic Data Visualization
Main entry point
"""

import sys
import os

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)

from pathlib import Path
import argparse
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

__version__ = "1.0.0"

class AutoPlot:
    """Main class for automatic data visualization"""
    
    def __init__(self):
        self.data = None
        self.file_path = None
        self.columns_info = {}
        
    def load_data(self, file_path: Path) -> Dict:
        """Load data from various file formats"""
        file_path = Path(file_path).expanduser().resolve()
        
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        self.file_path = file_path
        suffix = file_path.suffix.lower()
        
        try:
            if suffix == '.csv':
                import pandas as pd
                self.data = pd.read_csv(file_path)
            elif suffix in ['.xlsx', '.xls']:
                import pandas as pd
                self.data = pd.read_excel(file_path)
            elif suffix == '.json':
                import pandas as pd
                self.data = pd.read_json(file_path)
            else:
                return {"error": f"Unsupported file format: {suffix}"}
            
            self._analyze_columns()
            return {
                "success": True,
                "rows": len(self.data),
                "columns": len(self.data.columns),
                "column_info": self.columns_info
            }
        except Exception as e:
            return {"error": f"Failed to load data: {str(e)}"}
    
    def _analyze_columns(self):
        """Analyze column types and characteristics"""
        import pandas as pd
        
        for col in self.data.columns:
            dtype = self.data[col].dtype
            sample = self.data[col].dropna().head(10)
            
            info = {
                "dtype": str(dtype),
                "null_count": int(self.data[col].isnull().sum()),
                "unique_count": int(self.data[col].nunique())
            }
            
            # Detect type
            if pd.api.types.is_datetime64_any_dtype(dtype):
                info["type"] = "datetime"
            elif pd.api.types.is_numeric_dtype(dtype):
                info["type"] = "numeric"
                info["min"] = float(self.data[col].min()) if not self.data[col].isnull().all() else None
                info["max"] = float(self.data[col].max()) if not self.data[col].isnull().all() else None
                info["mean"] = float(self.data[col].mean()) if not self.data[col].isnull().all() else None
            elif info["unique_count"] <= 20:
                info["type"] = "categorical"
                info["categories"] = self.data[col].value_counts().head(10).to_dict()
            else:
                info["type"] = "text"
            
            self.columns_info[col] = info
    
    def suggest_charts(self) -> List[Dict]:
        """Suggest appropriate chart types based on data"""
        suggestions = []
        
        # Get column types
        numeric_cols = [c for c, i in self.columns_info.items() if i["type"] == "numeric"]
        categorical_cols = [c for c, i in self.columns_info.items() if i["type"] == "categorical"]
        datetime_cols = [c for c, i in self.columns_info.items() if i["type"] == "datetime"]
        
        # Time series
        if datetime_cols and numeric_cols:
            suggestions.append({
                "type": "line",
                "title": f"Trend over time",
                "x": datetime_cols[0],
                "y": numeric_cols[0],
                "reason": "Time series data detected"
            })
        
        # Bar chart for categories
        if categorical_cols and numeric_cols:
            suggestions.append({
                "type": "bar",
                "title": f"{numeric_cols[0]} by {categorical_cols[0]}",
                "x": categorical_cols[0],
                "y": numeric_cols[0],
                "reason": "Categorical comparison"
            })
        
        # Distribution
        if numeric_cols:
            suggestions.append({
                "type": "histogram",
                "title": f"Distribution of {numeric_cols[0]}",
                "column": numeric_cols[0],
                "reason": "Numeric distribution"
            })
        
        # Correlation
        if len(numeric_cols) >= 2:
            suggestions.append({
                "type": "scatter",
                "title": f"{numeric_cols[0]} vs {numeric_cols[1]}",
                "x": numeric_cols[0],
                "y": numeric_cols[1],
                "reason": "Correlation analysis"
            })
        
        # Pie chart for single categorical
        if categorical_cols:
            suggestions.append({
                "type": "pie",
                "title": f"Distribution of {categorical_cols[0]}",
                "column": categorical_cols[0],
                "reason": "Proportion visualization"
            })
        
        return suggestions
    
    def create_chart(self, chart_type: str, x: str = None, y: str = None, 
                     title: str = None, output: str = None, **kwargs) -> Dict:
        """Create a chart"""
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            
            if self.data is None:
                return {"error": "No data loaded"}
            
            # Default title
            if not title:
                title = f"{chart_type.title()} Chart"
            
            fig = None
            
            # Create appropriate chart
            if chart_type == "line":
                if x and y:
                    fig = px.line(self.data, x=x, y=y, title=title)
                elif y:
                    fig = px.line(self.data, y=y, title=title)
            
            elif chart_type == "bar":
                if x and y:
                    fig = px.bar(self.data, x=x, y=y, title=title)
                elif x:
                    value_counts = self.data[x].value_counts().head(20)
                    fig = px.bar(x=value_counts.index, y=value_counts.values, 
                                title=title, labels={'x': x, 'y': 'Count'})
            
            elif chart_type == "scatter":
                if x and y:
                    fig = px.scatter(self.data, x=x, y=y, title=title, trendline="ols")
            
            elif chart_type == "pie":
                column = x or y or list(self.data.columns)[0]
                value_counts = self.data[column].value_counts().head(10)
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=title)
            
            elif chart_type == "histogram":
                column = x or y or [c for c, i in self.columns_info.items() if i["type"] == "numeric"][0]
                fig = px.histogram(self.data, x=column, title=title)
            
            elif chart_type == "box":
                column = x or y or [c for c, i in self.columns_info.items() if i["type"] == "numeric"][0]
                fig = px.box(self.data, y=column, title=title)
            
            if fig is None:
                return {"error": f"Could not create {chart_type} chart with provided parameters"}
            
            # Update layout
            fig.update_layout(
                template="plotly_white",
                width=kwargs.get('width', 1200),
                height=kwargs.get('height', 800)
            )
            
            # Save output
            if not output:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output = f"chart_{chart_type}_{timestamp}.html"
            
            output_path = Path(output)
            
            # Export based on format
            if output_path.suffix == '.html':
                fig.write_html(str(output_path))
            elif output_path.suffix == '.png':
                fig.write_image(str(output_path))
            elif output_path.suffix == '.svg':
                fig.write_image(str(output_path))
            elif output_path.suffix == '.pdf':
                fig.write_image(str(output_path))
            else:
                # Default to HTML
                output_path = output_path.with_suffix('.html')
                fig.write_html(str(output_path))
            
            return {
                "success": True,
                "chart_type": chart_type,
                "output": str(output_path.absolute()),
                "title": title
            }
            
        except Exception as e:
            return {"error": f"Failed to create chart: {str(e)}"}
    
    def analyze_data(self, detailed: bool = False) -> Dict:
        """Analyze data and return insights"""
        if self.data is None:
            return {"error": "No data loaded"}
        
        import pandas as pd
        
        result = {
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "column_info": self.columns_info,
            "suggested_charts": self.suggest_charts()
        }
        
        if detailed:
            # Add detailed statistics
            numeric_data = self.data.select_dtypes(include=['number'])
            if not numeric_data.empty:
                result["statistics"] = numeric_data.describe().to_dict()
        
        return result

def main():
    parser = argparse.ArgumentParser(
        description="AutoPlot - Automatic Data Visualization",
        prog="autoplot"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Visualize command
    viz_parser = subparsers.add_parser("visualize", help="Create visualization from data file")
    viz_parser.add_argument("file", help="Data file (CSV, Excel, JSON)")
    viz_parser.add_argument("--chart-type", choices=["line", "bar", "scatter", "pie", "histogram", "box"],
                          help="Chart type (auto-detected if not specified)")
    viz_parser.add_argument("--x-column", help="X-axis column name")
    viz_parser.add_argument("--y-column", help="Y-axis column name")
    viz_parser.add_argument("--title", help="Chart title")
    viz_parser.add_argument("--theme", default="default", choices=["default", "minimal", "dark"],
                          help="Visual theme")
    viz_parser.add_argument("--format", choices=["html", "png", "svg", "pdf"],
                          help="Output format (default: html)")
    viz_parser.add_argument("--output", help="Output file path")
    viz_parser.add_argument("--width", type=int, default=1200, help="Chart width")
    viz_parser.add_argument("--height", type=int, default=800, help="Chart height")
    
    # Analyze command
    ana_parser = subparsers.add_parser("analyze", help="Analyze data structure")
    ana_parser.add_argument("file", help="Data file to analyze")
    ana_parser.add_argument("--detailed", action="store_true", help="Show detailed statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    plotter = AutoPlot()
    
    if args.command == "visualize":
        # Load data
        result = plotter.load_data(Path(args.file))
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        # Determine chart type
        chart_type = args.chart_type
        if not chart_type:
            suggestions = plotter.suggest_charts()
            if suggestions:
                chart_type = suggestions[0]["type"]
                print(f"Auto-selected chart type: {chart_type}")
            else:
                chart_type = "bar"
        
        # Determine columns
        x_col = args.x_column
        y_col = args.y_column
        
        if not x_col and not y_col:
            suggestions = plotter.suggest_charts()
            if suggestions:
                x_col = suggestions[0].get("x")
                y_col = suggestions[0].get("y")
        
        # Create output filename
        if args.output:
            output = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = args.format or "html"
            output = f"chart_{chart_type}_{timestamp}.{ext}"
        
        # Create chart
        result = plotter.create_chart(
            chart_type=chart_type,
            x=x_col,
            y=y_col,
            title=args.title,
            output=output,
            width=args.width,
            height=args.height
        )
        
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        print(f"[SUCCESS] Chart created: {result['output']}")
        print(f"  Type: {result['chart_type']}")
        print(f"  Title: {result['title']}")
    
    elif args.command == "analyze":
        result = plotter.load_data(Path(args.file))
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        analysis = plotter.analyze_data(detailed=args.detailed)
        
        print(f"\nData Analysis: {args.file}")
        print(f"Shape: {analysis['shape'][0]} rows x {analysis['shape'][1]} columns")
        print(f"\nColumns:")
        for col, info in analysis['column_info'].items():
            print(f"  {col} ({info['type']}): {info['unique_count']} unique, {info['null_count']} nulls")
        
        print(f"\nSuggested Charts:")
        for i, chart in enumerate(analysis['suggested_charts'][:5], 1):
            print(f"  {i}. {chart['type']}: {chart['title']} ({chart['reason']})")

if __name__ == "__main__":
    main()
