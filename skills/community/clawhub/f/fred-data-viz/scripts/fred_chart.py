import pandas as pd
import matplotlib.pyplot as plt
import argparse
import json
import sys

def fetch_fred_data(series_id, start_date='1959-01-01', end_date='2026-12-31'):
    """Fetch FRED data via CSV API."""
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start_date}&coed={end_date}'
    df = pd.read_csv(url, parse_dates=['observation_date'])
    df.columns = ['date', 'value']
    return df

def index_data(df, base_date=None):
    """Index data to a base date (default: first observation)."""
    if base_date:
        base_value = df.loc[df['date'] >= base_date, 'value'].iloc[0]
    else:
        base_value = df['value'].iloc[0]
    df['index'] = (df['value'] / base_value) * 100
    return df

def create_chart(series_list, title, output_path, annotations=None, start_date=None, end_date=None, fill_gap=True):
    """
    Create an economic comparison chart.
    
    series_list: list of dicts with 'id', 'label', 'color'
    annotations: list of dicts with 'date', 'label', 'position', 'y'
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    indexed_data = []
    
    for s in series_list:
        df = fetch_fred_data(s['id'], start_date or '1959-01-01', end_date or '2026-12-31')
        df = index_data(df)
        
        if start_date:
            df = df[df['date'] >= start_date]
        if end_date:
            df = df[df['date'] <= end_date]
        
        ax.plot(df['date'], df['index'], label=s['label'], linewidth=2.5, color=s.get('color', None))
        indexed_data.append(df)
    
    # Fill gap between first two series if requested
    if fill_gap and len(indexed_data) >= 2:
        df1 = indexed_data[0]
        df2 = indexed_data[1]
        merged = pd.merge(df1[['date', 'index']], df2[['date', 'index']], on='date', suffixes=('_1', '_2'))
        ax.fill_between(merged['date'], merged['index_2'], merged['index_1'], alpha=0.15, color='red', label='Gap')
    
    ax.axhline(y=100, color='black', linestyle='--', linewidth=0.8, alpha=0.4)
    
    # Add annotations
    if annotations:
        for ann in annotations:
            date = pd.Timestamp(ann['date'])
            ax.axvline(x=date, color='gray', linestyle=':', linewidth=0.6, alpha=0.5)
            y_pos = ann.get('y', 150)
            pos = ann.get('position', 'top')
            va = 'bottom' if pos == 'top' else 'top'
            y_target = y_pos + 10 if pos == 'top' else y_pos - 10
            ax.annotate(ann['label'], xy=(date, y_target), xytext=(date, y_pos),
                       fontsize=8, ha='center', va=va,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='gray'),
                       arrowprops=dict(arrowstyle='->', color='gray', lw=0.6))
    
    ax.set_title(title, fontsize=15, fontweight='bold', pad=15)
    ax.set_ylabel('Index (Start = 100)', fontsize=12)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create economic comparison charts from FRED data')
    parser.add_argument('--config', required=True, help='JSON config file with series, title, annotations')
    parser.add_argument('--output', default='/tmp/fred_chart.png', help='Output path for chart')
    
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = json.load(f)
    
    create_chart(
        series_list=config['series'],
        title=config['title'],
        output_path=args.output,
        annotations=config.get('annotations'),
        start_date=config.get('start_date'),
        end_date=config.get('end_date'),
        fill_gap=config.get('fill_gap', True)
    )
