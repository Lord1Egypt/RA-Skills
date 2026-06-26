#!/usr/bin/env python3
"""
Data Visualization Studio - Core visualization script

This script provides comprehensive data visualization capabilities
for various data formats and chart types.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional, List
import json
import os

def create_visualization(data_source: str, chart_type: str, output_path: str, 
                        title: str = "", config: Dict[str, Any] = None) -> str:
    """
    Create a visualization from the given data source.
    
    Args:
        data_source: Path to data file or JSON string
        chart_type: Type of chart to create (bar, line, scatter, pie, heatmap, etc.)
        output_path: Path where the visualization should be saved
        title: Title for the chart
        config: Additional configuration parameters
        
    Returns:
        Path to the generated visualization file
    """
    config = config or {}
    
    # Load data
    df = load_data(data_source)
    
    # Create visualization based on chart type
    if chart_type == "bar":
        fig = create_bar_chart(df, title, config)
    elif chart_type == "line":
        fig = create_line_chart(df, title, config)
    elif chart_type == "scatter":
        fig = create_scatter_plot(df, title, config)
    elif chart_type == "pie":
        fig = create_pie_chart(df, title, config)
    elif chart_type == "heatmap":
        fig = create_heatmap(df, title, config)
    elif chart_type == "histogram":
        fig = create_histogram(df, title, config)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
    
    # Save visualization
    if output_path.endswith('.html'):
        fig.write_html(output_path)
    else:
        fig.write_image(output_path)
    
    return output_path

def load_data(data_source: str) -> pd.DataFrame:
    """Load data from various sources."""
    if data_source.startswith('{') or data_source.startswith('['):
        # JSON string
        data = json.loads(data_source)
        return pd.DataFrame(data)
    elif data_source.endswith('.csv'):
        return pd.read_csv(data_source)
    elif data_source.endswith('.json'):
        return pd.read_json(data_source)
    elif data_source.endswith('.xlsx') or data_source.endswith('.xls'):
        return pd.read_excel(data_source)
    else:
        raise ValueError(f"Unsupported data format: {data_source}")

def create_bar_chart(df: pd.DataFrame, title: str, config: Dict[str, Any]) -> go.Figure:
    """Create a bar chart."""
    x_col = config.get('x_column', df.columns[0])
    y_col = config.get('y_column', df.columns[1])
    color_col = config.get('color_column')
    
    fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=title)
    return fig

def create_line_chart(df: pd.DataFrame, title: str, config: Dict[str, Any]) -> go.Figure:
    """Create a line chart."""
    x_col = config.get('x_column', df.columns[0])
    y_col = config.get('y_column', df.columns[1])
    color_col = config.get('color_column')
    
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    return fig

def create_scatter_plot(df: pd.DataFrame, title: str, config: Dict[str, Any]) -> go.Figure:
    """Create a scatter plot."""
    x_col = config.get('x_column', df.columns[0])
    y_col = config.get('y_column', df.columns[1])
    color_col = config.get('color_column')
    size_col = config.get('size_column')
    
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col, title=title)
    return fig

def create_pie_chart(df: pd.DataFrame, title: str, config: Dict[str, Any]) -> go.Figure:
    """Create a pie chart."""
    names_col = config.get('names_column', df.columns[0])
    values_col = config.get('values_column', df.columns[1])
    
    fig = px.pie(df, names=names_col, values=values_col, title=title)
    return fig

def create_heatmap(df: pd.DataFrame, title: str, config: Dict[str, Any]) -> go.Figure:
    """Create a heatmap."""
    fig = px.imshow(df.corr(), title=title)
    return fig

def create_histogram(df: pd.DataFrame, title: str, config: Dict[str, Any]) -> go.Figure:
    """Create a histogram."""
    x_col = config.get('x_column', df.columns[0])
    fig = px.histogram(df, x=x_col, title=title)
    return fig

def get_supported_formats() -> List[str]:
    """Get list of supported data formats."""
    return ['csv', 'json', 'xlsx', 'xls']

def get_supported_charts() -> List[str]:
    """Get list of supported chart types."""
    return ['bar', 'line', 'scatter', 'pie', 'heatmap', 'histogram']

if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) != 5:
        print("Usage: visualize_data.py <data_source> <chart_type> <output_path> <title>")
        sys.exit(1)
    
    data_source = sys.argv[1]
    chart_type = sys.argv[2]
    output_path = sys.argv[3]
    title = sys.argv[4]
    
    result = create_visualization(data_source, chart_type, output_path, title)
    print(f"Visualization created: {result}")