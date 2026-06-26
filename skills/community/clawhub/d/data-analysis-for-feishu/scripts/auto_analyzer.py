#!/usr/bin/env python3
"""
Auto chart recommendation and analysis module
"""
import pandas as pd
from typing import List, Dict, Any, Tuple

def analyze_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze data characteristics to recommend chart type and insights"""
    df = pd.DataFrame(data)
    analysis = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "column_types": {},
        "recommended_chart": None,
        "insights": []
    }
    
    # Analyze column types
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            analysis["column_types"][col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            analysis["column_types"][col] = "datetime"
        else:
            analysis["column_types"][col] = "categorical"
    
    numeric_cols = [c for c, t in analysis["column_types"].items() if t == "numeric"]
    categorical_cols = [c for c, t in analysis["column_types"].items() if t == "categorical"]
    datetime_cols = [c for c, t in analysis["column_types"].items() if t == "datetime"]
    
    # Generate insights
    for col in numeric_cols:
        mean_val = df[col].mean()
        max_val = df[col].max()
        min_val = df[col].min()
        analysis["insights"].append(f"Column '{col}': average={mean_val:.2f}, max={max_val}, min={min_val}")
    
    # Recommend chart type
    if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
        analysis["recommended_chart"] = "line"
        analysis["recommended_fields"] = {
            "x_axis": datetime_cols[0],
            "y_axis": numeric_cols[0]
        }
        analysis["recommendation_reason"] = "Time series data detected, line chart is best for showing trends"
    
    elif len(categorical_cols) >= 1 and len(numeric_cols) == 1:
        unique_cats = df[categorical_cols[0]].nunique()
        if unique_cats <= 10:
            analysis["recommended_chart"] = "pie"
            analysis["recommended_fields"] = {
                "label_field": categorical_cols[0],
                "value_field": numeric_cols[0]
            }
            analysis["recommendation_reason"] = "Single numeric column with few categories, pie chart shows proportion well"
        else:
            analysis["recommended_chart"] = "bar"
            analysis["recommended_fields"] = {
                "x_axis": categorical_cols[0],
                "y_axis": numeric_cols[0]
            }
            analysis["recommendation_reason"] = "Single numeric column with many categories, bar chart is easier to compare"
    
    elif len(categorical_cols) >= 1 and len(numeric_cols) >= 2:
        analysis["recommended_chart"] = "bar"
        analysis["recommended_fields"] = {
            "x_axis": categorical_cols[0],
            "y_axis": numeric_cols
        }
        analysis["recommendation_reason"] = "Multiple numeric columns, bar chart supports multi-series comparison"
    
    elif len(numeric_cols) >= 3:
        analysis["recommended_chart"] = "radar"
        analysis["recommendation_reason"] = "3+ numeric columns, radar chart shows multi-dimensional comparison"
    
    else:
        analysis["recommended_chart"] = "bar"
        analysis["recommendation_reason"] = "Default to bar chart for general data"
    
    return analysis

def generate_auto_analysis(data: List[Dict[str, Any]], chart_type: str, fields: Dict[str, str]) -> str:
    """Generate natural language analysis conclusion for the chart"""
    df = pd.DataFrame(data)
    analysis_lines = ["📊 **Data Analysis Conclusion:**"]
    
    if chart_type == "line" and "x_axis" in fields and "y_axis" in fields:
        x_col = fields["x_axis"]
        y_col = fields["y_axis"]
        if isinstance(y_col, list):
            y_col = y_col[0]
        
        # Calculate growth rate
        first_val = df[y_col].iloc[0]
        last_val = df[y_col].iloc[-1]
        growth_rate = (last_val - first_val) / first_val * 100 if first_val != 0 else 0
        
        max_val = df[y_col].max()
        min_val = df[y_col].min()
        max_point = df[df[y_col] == max_val].iloc[0]
        min_point = df[df[y_col] == min_val].iloc[0]
        
        analysis_lines.append(f"- Overall trend: {'Growth' if growth_rate > 0 else 'Decline'} of {abs(growth_rate):.1f}% from {df[x_col].iloc[0]} to {df[x_col].iloc[-1]}")
        analysis_lines.append(f"- Highest point: {max_point[x_col]} with value {max_val:.2f}")
        analysis_lines.append(f"- Lowest point: {min_point[x_col]} with value {min_val:.2f}")
    
    elif chart_type == "bar" and "x_axis" in fields and "y_axis" in fields:
        x_col = fields["x_axis"]
        y_cols = fields["y_axis"] if isinstance(fields["y_axis"], list) else [fields["y_axis"]]
        
        for y_col in y_cols:
            max_val = df[y_col].max()
            min_val = df[y_col].min()
            max_cat = df[df[y_col] == max_val].iloc[0][x_col]
            min_cat = df[df[y_col] == min_val].iloc[0][x_col]
            analysis_lines.append(f"- For {y_col}: Highest is '{max_cat}' ({max_val:.2f}), Lowest is '{min_cat}' ({min_val:.2f})")
    
    elif chart_type == "pie" and "label_field" in fields and "value_field" in fields:
        label_col = fields["label_field"]
        value_col = fields["value_field"]
        total = df[value_col].sum()
        top_item = df.sort_values(value_col, ascending=False).iloc[0]
        analysis_lines.append(f"- Total value: {total:.2f}")
        analysis_lines.append(f"- Largest proportion: '{top_item[label_col]}' accounts for {top_item[value_col]/total*100:.1f}%")
    
    elif chart_type == "gauge":
        value = fields.get("value", 0)
        max_val = fields.get("max", 100)
        completion_rate = value / max_val * 100
        status = "✅ Exceeded target" if completion_rate >= 100 else "⏳ In progress" if completion_rate >= 60 else "⚠️ Behind target"
        analysis_lines.append(f"- Completion rate: {completion_rate:.1f}% ({value}/{max_val})")
        analysis_lines.append(f"- Status: {status}")
    
    return "\n".join(analysis_lines)
