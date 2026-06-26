#!/usr/bin/env python3
"""
BMS CAN Signal Extractor
Extract time series data for specific signals from BLF files using DBC definitions.
"""

import sys
import json
import argparse
from datetime import datetime
import can
import cantools

def load_dbc_file(dbc_path):
    """Load DBC file and return database object."""
    try:
        db = cantools.database.load_file(dbc_path)
        return db
    except Exception as e:
        print(f"Error loading DBC file: {e}", file=sys.stderr)
        sys.exit(1)

def parse_blf_file(blf_path, db):
    """Parse BLF file and return list of messages with decoded signals."""
    messages = []
    
    try:
        with can.BLFReader(blf_path) as reader:
            for msg in reader:
                if msg.is_error_frame or msg.is_remote_frame:
                    continue
                
                # Try to decode the message using DBC
                try:
                    decoded_msg = db.get_message_by_frame_id(msg.arbitration_id)
                    if decoded_msg:
                        # Decode all signals in this message
                        signal_values = db.decode_message(msg.arbitration_id, msg.data)
                        messages.append({
                            'timestamp': msg.timestamp,
                            'arbitration_id': msg.arbitration_id,
                            'message_name': decoded_msg.name,
                            'signals': signal_values
                        })
                except KeyError:
                    # Message not in DBC, skip it
                    continue
                except Exception as e:
                    # Skip messages that can't be decoded
                    continue
                    
    except Exception as e:
        print(f"Error reading BLF file: {e}", file=sys.stderr)
        sys.exit(1)
    
    return messages

def extract_signal_timeseries(messages, signal_name):
    """Extract time series for a specific signal."""
    timeseries = []
    
    for msg in messages:
        if signal_name in msg['signals']:
            timeseries.append({
                'timestamp': msg['timestamp'],
                'value': msg['signals'][signal_name]
            })
    
    # Sort by timestamp
    timeseries.sort(key=lambda x: x['timestamp'])
    return timeseries

def format_output(timeseries, signal_name, output_format='json'):
    """Format the time series output."""
    if output_format == 'json':
        result = {
            'signal_name': signal_name,
            'data_points': len(timeseries),
            'time_series': timeseries
        }
        return json.dumps(result, indent=2)
    
    elif output_format == 'csv':
        csv_lines = ['timestamp,value']
        for point in timeseries:
            csv_lines.append(f"{point['timestamp']},{point['value']}")
        return '\n'.join(csv_lines)
    
    elif output_format == 'simple':
        # Just the values, one per line
        return '\n'.join(str(point['value']) for point in timeseries)
    
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def main():
    parser = argparse.ArgumentParser(description='Extract signal time series from BLF files')
    parser.add_argument('blf_file', help='Path to BLF file')
    parser.add_argument('dbc_file', help='Path to DBC file')
    parser.add_argument('signal_name', help='Name of signal to extract')
    parser.add_argument('--format', choices=['json', 'csv', 'simple'], 
                       default='json', help='Output format (default: json)')
    parser.add_argument('--output', help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    # Load DBC
    db = load_dbc_file(args.dbc_file)
    
    # Parse BLF
    messages = parse_blf_file(args.blf_file, db)
    
    # Extract signal time series
    timeseries = extract_signal_timeseries(messages, args.signal_name)
    
    if not timeseries:
        print(f"Signal '{args.signal_name}' not found in the BLF file.", file=sys.stderr)
        sys.exit(1)
    
    # Format output
    output = format_output(timeseries, args.signal_name, args.format)
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output)

if __name__ == '__main__':
    main()