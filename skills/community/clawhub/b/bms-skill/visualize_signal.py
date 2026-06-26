#!/usr/bin/env python3
"""
Signal visualization utility for BMS CAN analyzer skill.
Generates plots and formatted output for time series data.
"""

import sys
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import argparse
import os

def load_signal_data(json_file):
    """Load signal time series data from JSON file."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}", file=sys.stderr)
        return None

def create_plot(data, output_file=None):
    """Create a time series plot of the signal data."""
    if not data or 'signal_name' not in data or 'time_series' not in data:
        print("Invalid data format", file=sys.stderr)
        return False
    
    signal_name = data['signal_name']
    time_series = data['time_series']
    
    if not time_series:
        print("No time series data to plot", file=sys.stderr)
        return False
    
    # Extract timestamps and values
    timestamps = []
    values = []
    
    for point in time_series:
        if 'timestamp' in point and 'value' in point:
            timestamps.append(point['timestamp'])
            values.append(point['value'])
    
    if not timestamps:
        print("No valid timestamp/value pairs found", file=sys.stderr)
        return False
    
    # Convert timestamps to datetime objects if they're strings
    try:
        if isinstance(timestamps[0], str):
            datetime_stamps = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
        else:
            # Assume timestamps are already in seconds since epoch
            datetime_stamps = [datetime.fromtimestamp(ts) for ts in timestamps]
    except Exception as e:
        print(f"Error parsing timestamps: {e}", file=sys.stderr)
        datetime_stamps = list(range(len(timestamps)))
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(datetime_stamps, values, marker='o', linestyle='-', markersize=3)
    plt.title(f'Time Series: {signal_name}')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()
    return True

def format_output(data, format_type='json'):
    """Format the signal data for different output types."""
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'csv':
        if 'time_series' not in data:
            return "No time series data available"
        
        csv_lines = ['timestamp,value']
        for point in data['time_series']:
            if 'timestamp' in point and 'value' in point:
                csv_lines.append(f"{point['timestamp']},{point['value']}")
        return '\n'.join(csv_lines)
    elif format_type == 'summary':
        if 'time_series' not in data:
            return "No time series data available"
        
        values = [point['value'] for point in data['time_series'] if 'value' in point]
        if not values:
            return "No values found in time series"
        
        summary = f"Signal: {data.get('signal_name', 'Unknown')}\n"
        summary += f"Total samples: {len(values)}\n"
        summary += f"Min value: {min(values):.6f}\n"
        summary += f"Max value: {max(values):.6f}\n"
        summary += f"Average: {sum(values)/len(values):.6f}\n"
        return summary
    else:
        return "Unsupported format type"

def main():
    parser = argparse.ArgumentParser(description='Visualize BMS CAN signal time series data')
    parser.add_argument('input_file', help='Input JSON file with signal time series data')
    parser.add_argument('--output', '-o', help='Output file for plot (PNG)')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'summary'], 
                       default='json', help='Output format for data')
    parser.add_argument('--no-plot', action='store_true', help='Skip plotting, only output data')
    
    args = parser.parse_args()
    
    # Load the signal data
    data = load_signal_data(args.input_file)
    if data is None:
        sys.exit(1)
    
    # Output formatted data
    formatted_data = format_output(data, args.format)
    print(formatted_data)
    
    # Create plot if requested
    if not args.no_plot:
        plot_file = args.output or f"{data.get('signal_name', 'signal')}_timeseries.png"
        create_plot(data, plot_file)

if __name__ == '__main__':
    main()