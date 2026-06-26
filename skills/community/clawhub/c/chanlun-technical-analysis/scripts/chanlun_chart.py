#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChanLun Chart Generator - K-line + Fractal + Stroke + Segment + Pivot + MACD
Generate intuitive ChanLun technical chart PNG images with English labels
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import os
from datetime import datetime

# Use default font settings (no Chinese font dependency)
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150


class ChanLunChart:
    """ChanLun Chart Generator"""
    
    def __init__(self, df: pd.DataFrame, analyzer, output_dir: str = './outputs'):
        """
        Initialize chart generator
        
        Args:
            df: DataFrame with OHLCV data
            analyzer: ChanLunCore analyzer instance
            output_dir: Output directory
        """
        self.df = df.reset_index(drop=True)
        self.analyzer = analyzer
        self.output_dir = output_dir
        
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_full_chart(self, stock_code: str, save: bool = True, show_macd: bool = True) -> str:
        """
        Plot complete ChanLun chart (main chart + sub charts)
        
        Args:
            stock_code: Stock code
            save: Whether to save file
            show_macd: Whether to show MACD sub chart
        
        Returns:
            File path
        """
        if show_macd:
            fig = plt.figure(figsize=(16, 10))
            gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 1], hspace=0.08)
        else:
            fig = plt.figure(figsize=(16, 8))
            gs = fig.add_gridspec(2, 1, height_ratios=[4, 1], hspace=0.08)
        
        # K-line chart + strokes + segments + pivots
        ax_kline = fig.add_subplot(gs[0])
        self._plot_kline(ax_kline)
        self._plot_fractals(ax_kline)
        self._plot_strokes(ax_kline)
        self._plot_segments(ax_kline)
        self._plot_pivots(ax_kline)
        
        # Set title
        trend = self.analyzer.get_current_trend()
        trend_en = {'uptrend': 'Uptrend', 'downtrend': 'Downtrend', 'consolidation': 'Consolidation'}.get(trend, 'Unknown')
        
        latest_price = self.df.iloc[-1]['close']
        price_change = (latest_price - self.df.iloc[-2]['close']) / self.df.iloc[-2]['close'] * 100
        
        title = f'{stock_code} ChanLun Technical Analysis - {trend_en}'
        subtitle = f'Latest: {latest_price:.2f} Change: {price_change:+.2f}%'
        
        ax_kline.set_title(title, fontsize=14, fontweight='bold', pad=10)
        ax_kline.text(0.02, 0.98, subtitle, transform=ax_kline.transAxes, 
                     fontsize=10, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax_kline.set_ylabel('Price', fontsize=10)
        ax_kline.grid(True, alpha=0.3, linestyle='--')
        
        self._add_legend(ax_kline)
        
        if show_macd:
            ax_macd = fig.add_subplot(gs[1], sharex=ax_kline)
            self._plot_macd(ax_macd)
            
            ax_volume = fig.add_subplot(gs[2], sharex=ax_kline)
            self._plot_volume(ax_volume)
        else:
            ax_volume = fig.add_subplot(gs[1], sharex=ax_kline)
            self._plot_volume(ax_volume)
        
        if save:
            filepath = os.path.join(self.output_dir, f'{stock_code}_chanlun_chart.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            return filepath
        else:
            plt.show()
            return None
    
    def _plot_kline(self, ax):
        """Plot K-line chart"""
        df = self.df
        
        # Red for up, green for down (Chinese convention)
        colors = ['red' if df.iloc[i]['close'] >= df.iloc[i]['open'] else 'green' 
                  for i in range(len(df))]
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Draw shadow
            ax.plot([i, i], [row['low'], row['high']], color=colors[i], linewidth=1, alpha=0.8)
            
            # Draw body
            body_top = max(row['open'], row['close'])
            body_bottom = min(row['open'], row['close'])
            body_height = body_top - body_bottom
            
            if body_height > 0:
                rect = Rectangle((i-0.3, body_bottom), 0.6, body_height, 
                                facecolor=colors[i], edgecolor=colors[i], 
                                linewidth=1, alpha=0.9)
                ax.add_patch(rect)
        
        ax.set_ylim(df['low'].min() * 0.95, df['high'].max() * 1.05)
        
        # Add date labels on x-axis
        if 'datetime' in df.columns:
            dates = df['datetime'].dt.strftime('%m-%d')
            step = max(1, len(dates) // 10)
            ax.set_xticks(range(0, len(dates), step))
            ax.set_xticklabels([dates.iloc[i] for i in range(0, len(dates), step)], rotation=45, ha='right')
    
    def _plot_fractals(self, ax):
        """Plot fractal markers"""
        fractals = self.analyzer.fractals
        
        # Top fractals - down arrow (green)
        for top in fractals.get('tops', []):
            ax.annotate('T', xy=(top['index'], top['price']), 
                       xytext=(0, 12), textcoords='offset points',
                       color='green', fontsize=10, ha='center', fontweight='bold',
                       bbox=dict(boxstyle='circle', facecolor='white', alpha=0.8, edgecolor='green'))
        
        # Bottom fractals - up arrow (red)
        for bottom in fractals.get('bottoms', []):
            ax.annotate('B', xy=(bottom['index'], bottom['price']), 
                       xytext=(0, -12), textcoords='offset points',
                       color='red', fontsize=10, ha='center', fontweight='bold',
                       bbox=dict(boxstyle='circle', facecolor='white', alpha=0.8, edgecolor='red'))
    
    def _plot_strokes(self, ax):
        """Plot stroke connections"""
        strokes = self.analyzer.strokes
        
        for stroke in strokes:
            color = 'blue' if stroke['direction'] == 'up' else 'purple'
            linestyle = '-' if stroke['direction'] == 'up' else '--'
            linewidth = 2.5
            
            ax.plot([stroke['start'], stroke['end']], 
                   [stroke['start_price'], stroke['end_price']], 
                   color=color, linestyle=linestyle, linewidth=linewidth, 
                   alpha=0.8, zorder=5)
            
            # Add direction marker at midpoint
            mid_idx = (stroke['start'] + stroke['end']) / 2
            mid_price = (stroke['start_price'] + stroke['end_price']) / 2
            direction = 'UP' if stroke['direction'] == 'up' else 'DN'
            ax.annotate(direction, xy=(mid_idx, mid_price),
                       color=color, fontsize=8, ha='center', va='center',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    def _plot_segments(self, ax):
        """Plot segments"""
        segments = self.analyzer.segments
        
        for i, segment in enumerate(segments):
            color = 'lightblue' if segment['direction'] == 'up' else 'lightcoral'
            alpha = 0.15
            
            ax.axvspan(segment['start'], segment['end'], 
                      alpha=alpha, color=color)
            
            ax.annotate(f'Seg{i+1}', xy=(segment['start'], 
                                         self.df.iloc[segment['start']]['low'] * 0.98),
                       xytext=(0, -30), textcoords='offset points',
                       color='darkblue' if segment['direction'] == 'up' else 'darkred', 
                       fontsize=8, ha='center',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    def _plot_pivots(self, ax):
        """Plot pivot zones"""
        pivots = self.analyzer.identify_pivots()
        
        for i, pivot in enumerate(pivots):
            rect = Rectangle((pivot['start_index'], pivot['low']), 
                            pivot['end_index'] - pivot['start_index'],
                            pivot['high'] - pivot['low'],
                            facecolor='yellow', alpha=0.25, 
                            edgecolor='orange', linewidth=2, 
                            linestyle='--', zorder=3)
            ax.add_patch(rect)
            
            ax.annotate(f'Pivot{i+1}', 
                       xy=((pivot['start_index'] + pivot['end_index']) / 2, pivot['high']),
                       xytext=(0, 15), textcoords='offset points',
                       color='darkorange', fontsize=10, ha='center', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def _plot_macd(self, ax):
        """Plot MACD indicator"""
        from chanlun_divergence import DivergenceDetector
        
        detector = DivergenceDetector(self.analyzer.processed_klines, self.analyzer.strokes)
        macd = detector.macd
        
        x = range(len(macd))
        
        colors = ['red' if v >= 0 else 'green' for v in macd['hist']]
        ax.bar(x, macd['hist'], color=colors, alpha=0.7, width=1.0, label='MACD Hist')
        
        ax.plot(x, macd['macd'], color='blue', linewidth=1.5, label='DIF')
        ax.plot(x, macd['signal'], color='orange', linewidth=1.5, label='DEA')
        
        ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='-')
        
        ax.set_ylabel('MACD', fontsize=9)
        ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(macd['hist'].min() * 1.2, macd['hist'].max() * 1.2)
    
    def _plot_volume(self, ax):
        """Plot volume"""
        df = self.df
        
        colors = ['red' if df.iloc[i]['close'] >= df.iloc[i]['open'] else 'green' 
                  for i in range(len(df))]
        
        ax.bar(range(len(df)), df['volume'], color=colors, alpha=0.7, width=1.0)
        ax.set_ylabel('Volume', fontsize=9)
        ax.set_xlabel('Date', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
    
    def _add_legend(self, ax):
        """Add legend"""
        from matplotlib.lines import Line2D
        
        legend_elements = [
            Line2D([0], [0], color='red', linewidth=2, label='Bullish Candle'),
            Line2D([0], [0], color='green', linewidth=2, label='Bearish Candle'),
            Line2D([0], [0], color='blue', linewidth=2, linestyle='-', label='Up Stroke'),
            Line2D([0], [0], color='purple', linewidth=2, linestyle='--', label='Down Stroke'),
            Line2D([0], [0], marker='o', color='green', linestyle='None', 
                  markersize=8, label='Top Fractal (T)'),
            Line2D([0], [0], marker='o', color='red', linestyle='None', 
                  markersize=8, label='Bottom Fractal (B)'),
            Rectangle((0, 0), 1, 1, facecolor='yellow', alpha=0.25, 
                     edgecolor='orange', linestyle='--', label='Pivot Zone')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', fontsize=8, 
                 framealpha=0.9, bbox_to_anchor=(0, 1.02))


def plot_chanlun_chart(stock_code: str, analyzer, output_dir: str = './outputs', 
                       show_macd: bool = True) -> str:
    """
    Convenience function: Generate ChanLun chart
    
    Args:
        stock_code: Stock code
        analyzer: ChanLunCore analyzer instance
        output_dir: Output directory
        show_macd: Whether to show MACD
    
    Returns:
        Chart file path
    """
    chart = ChanLunChart(analyzer.df, analyzer, output_dir)
    filepath = chart.plot_full_chart(stock_code, save=True, show_macd=show_macd)
    return filepath