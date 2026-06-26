#!/usr/bin/env python3
"""
Chart Animation Generator
Creates animated trend charts from time-series data.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime
import os
import sys
import argparse

# Default color palette
DEFAULT_COLORS = ['#E74C3C', '#3498DB', '#27AE60', '#F39C12', '#9B59B6', '#1ABC9C']

def load_data(data_path):
    """Load time-series data from JSON file."""
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_data(data):
    """Validate data structure."""
    if 'dates' not in data:
        raise ValueError("Data must contain 'dates' array")
    if 'series' not in data:
        raise ValueError("Data must contain 'series' object")
    
    for name, series in data['series'].items():
        if 'values' not in series:
            raise ValueError(f"Series '{name}' must contain 'values' array")
        if len(series['values']) != len(data['dates']):
            raise ValueError(f"Series '{name}' values count must match dates count")

def create_animation(data, output_dir, options):
    """Create animated chart."""
    print("🎬 Creating animated chart...")
    
    dates = data['dates']
    series_names = list(data['series'].keys())
    num_series = len(series_names)
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(options.width, options.height))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    # Y-axis range
    all_values = []
    for name in series_names:
        all_values.extend(data['series'][name]['values'])
    min_val = min(all_values) - 3
    max_val = max(all_values) + 3
    ax.set_ylim(min_val, max_val)
    ax.set_xlim(-1, len(dates) + 1)
    
    # Title
    title = ax.set_title("", fontsize=20, fontweight='bold', color='white', pad=20)
    
    # X-axis labels
    tick_positions = list(range(0, len(dates), max(1, len(dates) // 10)))
    tick_labels = [dates[i].split('-')[1] + '/' + dates[i].split('-')[2] 
                   if '-' in dates[i] else dates[i] for i in tick_positions]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right', color='white', fontsize=10)
    
    # Y-axis
    ylabel = data.get('ylabel', 'Value')
    ax.set_ylabel(ylabel, fontsize=14, color='white')
    ax.tick_params(axis='y', colors='white')
    ax.grid(True, alpha=0.2, color='white')
    
    # Lines
    lines = {}
    for idx, name in enumerate(series_names):
        color = data['series'][name].get('color', DEFAULT_COLORS[idx % len(DEFAULT_COLORS)])
        line, = ax.plot([], [], color=color, linewidth=3, label=name, alpha=0.9)
        lines[name] = line
    
    # Legend
    ax.legend(loc='upper right', fontsize=12, 
              facecolor='#16213e', edgecolor='white', labelcolor='white')
    
    def init():
        for name in series_names:
            lines[name].set_data([], [])
        title.set_text("")
        return list(lines.values()) + [title]
    
    def animate(frame):
        current_idx = frame + 1
        for name in series_names:
            values = data['series'][name]['values'][:current_idx]
            x = list(range(len(values)))
            lines[name].set_data(x, values)
        
        title_text = options.title if options.title else data.get('metadata', {}).get('title', 'Trend Chart')
        current_date = dates[min(frame, len(dates)-1)]
        title.set_text(f"{title_text}\n{current_date} — {dates[-1]}")
        
        return list(lines.values()) + [title]
    
    anim = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=len(dates),
        interval=80,
        blit=True,
        repeat=True
    )
    
    # Save GIF
    gif_path = os.path.join(output_dir, 'animation.gif')
    print(f"💾 Saving GIF...")
    anim.save(gif_path, writer='pillow', fps=options.fps, dpi=100)
    print(f"✅ GIF saved: {gif_path}")
    
    # Try MP4
    try:
        mp4_path = os.path.join(output_dir, 'animation.mp4')
        print(f"💾 Saving MP4...")
        anim.save(mp4_path, writer='ffmpeg', fps=options.fps, dpi=150)
        print(f"✅ MP4 saved: {mp4_path}")
    except Exception as e:
        print(f"⚠️  MP4 skipped (ffmpeg not available): {e}")
    
    plt.close()
    return gif_path

def create_overview(data, output_dir, options):
    """Create static overview chart."""
    print("\n📊 Creating overview chart...")
    
    dates = data['dates']
    series_names = list(data['series'].keys())
    num_series = len(series_names)
    
    # Grid layout
    if num_series == 1:
        rows, cols = 1, 1
    elif num_series <= 2:
        rows, cols = 1, 2
    elif num_series <= 4:
        rows, cols = 2, 2
    else:
        rows = (num_series + 1) // 2
        cols = 2
    
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    fig.patch.set_facecolor('#1a1a2e')
    
    if num_series == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
    
    for idx, name in enumerate(series_names):
        ax = axes[idx]
        ax.set_facecolor('#16213e')
        
        values = data['series'][name]['values']
        color = data['series'][name].get('color', DEFAULT_COLORS[idx % len(DEFAULT_COLORS)])
        
        ax.fill_between(range(len(dates)), values, alpha=0.3, color=color)
        ax.plot(range(len(dates)), values, color=color, linewidth=2)
        
        # Min/max markers
        max_idx = values.index(max(values))
        min_idx = values.index(min(values))
        
        ax.scatter([max_idx], [values[max_idx]], color='red', s=100, zorder=5)
        ax.scatter([min_idx], [values[min_idx]], color='blue', s=100, zorder=5)
        
        ax.annotate(f'Max: {values[max_idx]:.1f}', 
                   xy=(max_idx, values[max_idx]),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=10, color='white')
        ax.annotate(f'Min: {values[min_idx]:.1f}',
                   xy=(min_idx, values[min_idx]),
                   xytext=(10, -15), textcoords='offset points',
                   fontsize=10, color='white')
        
        mean_val = np.mean(values)
        ax.set_title(f"{name}\nAvg: {mean_val:.1f}", fontsize=14, fontweight='bold', color='white')
        ax.set_ylabel(data.get('ylabel', 'Value'), color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        month_ticks = list(range(0, len(dates), max(1, len(dates) // 6)))
        month_labels = [dates[i].split('-')[1] if '-' in dates[i] else dates[i][:3] for i in month_ticks]
        ax.set_xticks(month_ticks)
        ax.set_xticklabels(month_labels, color='white', fontsize=9)
    
    # Hide unused axes
    for idx in range(num_series, len(axes)):
        axes[idx].set_visible(False)
    
    title_text = options.title if options.title else data.get('metadata', {}).get('title', 'Trend Overview')
    fig.suptitle(title_text, fontsize=18, fontweight='bold', color='white', y=0.98)
    
    plt.tight_layout()
    
    overview_path = os.path.join(output_dir, 'overview.png')
    plt.savefig(overview_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    print(f"✅ Overview saved: {overview_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate animated trend charts')
    parser.add_argument('--data', required=True, help='Path to input JSON data')
    parser.add_argument('--output', default='./output', help='Output directory')
    parser.add_argument('--title', default=None, help='Chart title')
    parser.add_argument('--fps', type=int, default=12, help='Animation FPS')
    parser.add_argument('--width', type=int, default=14, help='Figure width (inches)')
    parser.add_argument('--height', type=int, default=8, help='Figure height (inches)')
    
    options = parser.parse_args()
    
    # Create output directory
    os.makedirs(options.output, exist_ok=True)
    
    # Load and validate data
    data = load_data(options.data)
    validate_data(data)
    
    # Set Chinese font support
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'STHeiti', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # Generate outputs
    create_animation(data, options.output, options)
    create_overview(data, options.output, options)
    
    print("\n" + "=" * 50)
    print("🎉 Chart animation complete!")
    print(f"📁 Output directory: {options.output}")

if __name__ == '__main__':
    main()