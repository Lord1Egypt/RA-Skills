import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import json
import sys
from pathlib import Path

def load_data(source, type='csv'):
    """Load data from various sources."""
    if type == 'csv':
        if source.startswith('http'):
            return pd.read_csv(source, parse_dates=True)
        return pd.read_csv(source, parse_dates=True)
    elif type == 'json':
        return pd.read_json(source)
    elif type == 'fred':
        url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={source}&cosd=1950-01-01'
        df = pd.read_csv(url, parse_dates=['observation_date'])
        df.columns = ['date', 'value']
        return df
    return None

def index_series(df, date_col='date', value_col='value', base_date=None):
    """Index series to 100 at base_date (or first observation)."""
    if base_date:
        base = df.loc[df[date_col] >= base_date, value_col].iloc[0]
    else:
        base = df[value_col].iloc[0]
    df['index'] = (df[value_col] / base) * 100
    return df

def create_chart(config):
    """Create chart from config dict."""
    fig, ax = plt.subplots(figsize=config.get('figsize', [12, 7]))
    
    series_data = []
    
    for s in config['series']:
        # Load data
        if 'data' in s:
            df = pd.DataFrame(s['data'])
        elif 'csv' in s:
            df = pd.read_csv(s['csv'], parse_dates=[s.get('date_col', 'date')])
        elif 'fred' in s:
            df = load_data(s['fred'], type='fred')
        else:
            raise ValueError(f"No data source for series: {s.get('label', 'unknown')}")
        
        date_col = s.get('date_col', 'date')
        value_col = s.get('value_col', 'value')
        
        # Filter date range
        if 'start_date' in config:
            df = df[df[date_col] >= config['start_date']]
        if 'end_date' in config:
            df = df[df[date_col] <= config['end_date']]
        
        # Index if requested
        if s.get('index', False) or config.get('index_all', False):
            df = index_series(df, date_col, value_col, s.get('base_date'))
            plot_col = 'index'
            ylabel = 'Index (Base = 100)'
        else:
            plot_col = value_col
            ylabel = value_col
        
        # Plot
        plot_type = s.get('type', 'line')
        if plot_type == 'line':
            ax.plot(df[date_col], df[plot_col], label=s['label'], 
                   linewidth=s.get('width', 2.5), color=s.get('color'), 
                   linestyle=s.get('style', '-'), zorder=3)
        elif plot_type == 'bar':
            ax.bar(df[date_col], df[plot_col], label=s['label'], 
                   color=s.get('color'), alpha=s.get('alpha', 0.7))
        elif plot_type == 'scatter':
            ax.scatter(df[date_col], df[plot_col], label=s['label'], 
                      color=s.get('color'), s=s.get('size', 20))
        
        series_data.append(df)
    
    # Fill between two series
    if config.get('fill') and len(series_data) >= 2:
        df1 = series_data[0][[date_col, plot_col]].rename(columns={plot_col: 'v1'})
        df2 = series_data[1][[date_col, plot_col]].rename(columns={plot_col: 'v2'})
        merged = pd.merge(df1, df2, on=date_col)
        ax.fill_between(merged[date_col], merged['v1'], merged['v2'], 
                       alpha=config.get('fill_alpha', 0.15), 
                       color=config.get('fill_color', 'red'),
                       label=config.get('fill_label', 'Gap'))
    
    # Reference line
    if config.get('hline'):
        ax.axhline(y=config['hline'], color='black', linestyle='--', 
                  linewidth=0.8, alpha=0.4, zorder=1)
    
    # Annotations
    for ann in config.get('annotations', []):
        date = pd.Timestamp(ann['date'])
        ax.axvline(x=date, color=ann.get('line_color', 'gray'), 
                  linestyle=':', linewidth=0.6, alpha=0.5, zorder=1)
        
        y_pos = ann.get('y', 150)
        pos = ann.get('position', 'top')
        
        ax.annotate(ann['label'], xy=(date, y_pos),
                   fontsize=ann.get('fontsize', 8), 
                   ha='center', va='bottom' if pos == 'top' else 'top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            alpha=0.9, edgecolor='gray'),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=0.6))
    
    # Title and labels
    ax.set_title(config.get('title', 'Chart'), fontsize=config.get('title_size', 15), 
                fontweight='bold', pad=15)
    ax.set_ylabel(config.get('ylabel', ylabel), fontsize=12)
    if config.get('xlabel'):
        ax.set_xlabel(config['xlabel'], fontsize=12)
    
    # Legend
    ax.legend(loc=config.get('legend_pos', 'upper left'), 
             fontsize=config.get('legend_size', 11),
             framealpha=config.get('legend_alpha', 0.95))
    
    # Grid
    ax.grid(config.get('grid', True), alpha=config.get('grid_alpha', 0.3))
    
    # Y limits
    if 'ylim' in config:
        ax.set_ylim(config['ylim'])
    
    plt.tight_layout()
    
    output = config.get('output', '/tmp/chart.png')
    plt.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight')
    print(f"Chart saved: {output}")
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='General-purpose chart builder')
    parser.add_argument('--config', required=True, help='JSON config file')
    
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = json.load(f)
    
    create_chart(config)
