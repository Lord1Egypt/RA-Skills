#!/usr/bin/env python3
"""
Visualization module for ENSO Tracker.
Imperial Modernity color palette for beautiful charts.
"""

import os
import warnings
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from scipy.interpolate import make_interp_spline

# Suppress matplotlib font warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')


# ============================================
# Imperial Modernity Color Palette
# ============================================

COLORS = {
    'heritage_red_dark': '#930013',
    'heritage_red': '#BD1020',
    'imperial_gold': '#D4AF37',
    'rice_paper': '#faf9f5',
    'dark_text': '#1a1a1a',
    'grid_line': '#e5e5e5',
    'el_nino': '#BD1020',
    'la_nina': '#2171B5',
    'neutral': '#6B7280',
    'danger_zone': '#FFE4E4',
    'annotation': '#D4AF37',
}


# ============================================
# CJK Font Configuration
# ============================================

def setup_cjk_fonts():
    """Configure matplotlib for CJK font support."""
    # Try fonts in order of preference
    cjk_fonts = [
        'PingFang HK',
        'Hiragino Sans GB',
        'STHeiti',
        'Arial Unicode MS',
        'SimHei',
        'Microsoft YaHei',
        'WenQuanYi Micro Hei',
    ]

    for font_name in cjk_fonts:
        try:
            # Check if font is available
            available_fonts = [f.name for f in font_manager.fontManager.ttflist]
            if font_name in available_fonts:
                plt.rcParams['font.family'] = font_name
                plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign
                return font_name
        except Exception:
            continue

    # Fallback to default
    return 'sans-serif'


# Configure fonts
FONT_FAMILY = setup_cjk_fonts()


# ============================================
# Chart Styling Helpers
# ============================================

def apply_imperial_style(ax: plt.Axes, title: str = '', lang: str = 'zh'):
    """
    Apply Imperial Modernity style to an axes.

    Args:
        ax: Matplotlib axes
        title: Chart title
        lang: Language ('zh' or 'en')
    """
    # Rice paper background
    ax.set_facecolor(COLORS['rice_paper'])

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Style remaining spines
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    # Grid lines
    ax.grid(True, axis='y', linestyle='--', alpha=0.3, color=COLORS['grid_line'])
    ax.grid(True, axis='x', linestyle='--', alpha=0.3, color=COLORS['grid_line'])

    # Title
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['dark_text'], pad=15)


def create_gradient_line(
    x: np.ndarray,
    y: np.ndarray,
    ax: plt.Axes,
    cmap_name: str = 'YlOrRd'
) -> plt.Line2D:
    """
    Create a gradient-colored line based on Y values.

    Args:
        x: X values
        y: Y values
        ax: Matplotlib axes
        cmap_name: Colormap name

    Returns:
        Line2D object
    """
    # Normalize y values for colormap
    y_norm = (y - y.min()) / (y.max() - y.min() + 1e-6)

    # Get colormap
    cmap = plt.get_cmap(cmap_name)

    # Plot as scatter points with color mapping
    for i in range(len(x) - 1):
        ax.plot([x[i], x[i+1]], [y[i], y[i+1]],
                color=cmap(y_norm[i]), linewidth=2, alpha=0.9)

    # Return placeholder
    return ax.plot(x, y, linewidth=2, alpha=0)[0]


def spline_smooth(x: np.ndarray, y: np.ndarray, num_points: int = 300) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply spline smoothing to data.

    Args:
        x: X values
        y: Y values
        num_points: Number of interpolated points

    Returns:
        Smoothed (x, y) arrays
    """
    try:
        x_arr = np.array(x)
        y_arr = np.array(y)

        # Remove NaN values
        mask = ~(np.isnan(x_arr) | np.isnan(y_arr))
        x_clean = x_arr[mask]
        y_clean = y_arr[mask]

        if len(x_clean) < 4:
            return x_clean, y_clean

        # Create spline interpolation
        x_smooth = np.linspace(x_clean.min(), x_clean.max(), num_points)
        spline = make_interp_spline(x_clean, y_clean, k=3)
        y_smooth = spline(x_smooth)

        return x_smooth, y_smooth
    except Exception:
        return x, y


# ============================================
# Main Visualization Functions
# ============================================

def plot_heat_records(
    records: List[Dict[str, Any]],
    title: str,
    output_path: str,
    lang: str = 'zh'
) -> bool:
    """
    Generate India heat records style chart with gradient line.

    Args:
        records: List of dicts with 'year' and 'temp' keys
        title: Chart title
        output_path: Output file path
        lang: Language ('zh' or 'en')

    Returns:
        True on success, False on failure
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 6), dpi=180)
        fig.patch.set_facecolor(COLORS['rice_paper'])

        # Extract data
        years = np.array([r['year'] for r in records])
        temps = np.array([r['temp'] for r in records])

        # Spline smoothing
        x_smooth, y_smooth = spline_smooth(years, temps)

        # Create gradient line using YlOrRd colormap
        cmap = plt.get_cmap('YlOrRd')
        y_norm = (y_smooth - y_smooth.min()) / (y_smooth.max() - y_smooth.min() + 1e-6)

        for i in range(len(x_smooth) - 1):
            ax.plot([x_smooth[i], x_smooth[i+1]], [y_smooth[i], y_smooth[i+1]],
                   color=cmap(y_norm[i]), linewidth=2.5, alpha=0.9)

        # Add scatter points
        ax.scatter(years, temps, c=temps, cmap='YlOrRd',
                  s=60, edgecolors='white', linewidths=1.5, zorder=5)

        # Danger zone (above threshold)
        threshold = np.percentile(temps, 90)
        ax.axhline(y=threshold, color=COLORS['heritage_red'], linestyle='--',
                  linewidth=1.5, alpha=0.7, label=f'危险阈值 {threshold:.1f}°C')

        # Fill danger zone
        ax.fill_between(years, threshold, temps.max() + 1,
                        where=temps >= threshold,
                        color=COLORS['danger_zone'], alpha=0.3)

        # Find and annotate records
        max_idx = np.argmax(temps)
        ax.annotate(
            f"{temps[max_idx]:.1f}°C",
            xy=(years[max_idx], temps[max_idx]),
            xytext=(years[max_idx] - 2, temps[max_idx] + 1),
            fontsize=11,
            fontweight='bold',
            color=COLORS['heritage_red'],
            arrowprops=dict(arrowstyle='->', color=COLORS['heritage_red'], lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLORS['imperial_gold'], alpha=0.9)
        )

        # Styling
        apply_imperial_style(ax, title, lang)

        # Labels
        xlabel = '年份' if lang == 'zh' else 'Year'
        ylabel = '温度 (°C)' if lang == 'zh' else 'Temperature (°C)'
        ax.set_xlabel(xlabel, fontsize=11, color=COLORS['dark_text'])
        ax.set_ylabel(ylabel, fontsize=11, color=COLORS['dark_text'])

        # Legend
        ax.legend(loc='upper left', framealpha=0.9)

        # Tight layout
        plt.tight_layout()

        # Save
        plt.savefig(output_path, dpi=180, facecolor=COLORS['rice_paper'],
                   edgecolor='none', bbox_inches='tight')
        plt.close(fig)

        print(f"✅ 图表已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 生成图表失败: {e}")
        return False


def plot_enso_timeline(
    oni_data: 'pd.DataFrame',
    output_path: str,
    lang: str = 'zh'
) -> bool:
    """
    Generate ONI index timeline with El Niño/La Niña phase coloring.

    Args:
        oni_data: DataFrame with 'year', 'season', 'oni_value' columns
        output_path: Output file path
        lang: Language ('zh' or 'en')

    Returns:
        True on success, False on failure
    """
    try:
        import pandas as pd

        fig, ax = plt.subplots(figsize=(14, 6), dpi=180)
        fig.patch.set_facecolor(COLORS['rice_paper'])

        # Convert seasons to numeric for plotting
        season_order = {'DJF': 0, 'JFM': 1, 'FMA': 2, 'MAM': 3, 'AMJ': 4,
                       'MJJ': 5, 'JJA': 6, 'JAS': 7, 'ASO': 8, 'SON': 9,
                       'OND': 10, 'NDJ': 11}

        df = oni_data.copy()
        df['season_num'] = df['season'].map(season_order).fillna(0)
        df['time'] = df['year'] + df['season_num'] / 12

        # Plot timeline
        time = df['time'].values
        oni = df['oni_value'].values

        # Color by phase
        for i in range(len(time) - 1):
            if oni[i] >= 0.5:
                color = COLORS['el_nino']
            elif oni[i] <= -0.5:
                color = COLORS['la_nina']
            else:
                color = COLORS['neutral']

            ax.plot([time[i], time[i+1]], [oni[i], oni[i+1]],
                   color=color, linewidth=2, alpha=0.8)

        # Phase bands
        ax.axhspan(0.5, 2.5, alpha=0.15, color=COLORS['el_nino'], label='厄尔尼诺')
        ax.axhspan(-2.5, -0.5, alpha=0.15, color=COLORS['la_nina'], label='拉尼娜')

        # Threshold lines
        ax.axhline(y=0.5, color=COLORS['el_nino'], linestyle='--', linewidth=1, alpha=0.5)
        ax.axhline(y=-0.5, color=COLORS['la_nina'], linestyle='--', linewidth=1, alpha=0.5)
        ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

        # Styling
        title = 'ENSO 指数时间线 (ONI)' if lang == 'zh' else 'ENSO Index Timeline (ONI)'
        apply_imperial_style(ax, title, lang)

        xlabel = '年份' if lang == 'zh' else 'Year'
        ylabel = 'ONI 指数 (°C)' if lang == 'zh' else 'ONI Index (°C)'
        ax.set_xlabel(xlabel, fontsize=11, color=COLORS['dark_text'])
        ax.set_ylabel(ylabel, fontsize=11, color=COLORS['dark_text'])

        ax.legend(loc='upper left', framealpha=0.9)
        ax.set_ylim(-2.5, 2.5)

        plt.tight_layout()
        plt.savefig(output_path, dpi=180, facecolor=COLORS['rice_paper'],
                   edgecolor='none', bbox_inches='tight')
        plt.close(fig)

        print(f"✅ ENSO 时间线已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 生成 ENSO 时间线失败: {e}")
        return False


def plot_enso_heat_correlation(
    oni_data: 'pd.DataFrame',
    heat_records: List[Dict[str, Any]],
    output_path: str,
    lang: str = 'zh'
) -> bool:
    """
    Generate dual-axis chart: ONI cycles overlaid with extreme heat records.

    Args:
        oni_data: DataFrame with ONI data
        heat_records: List of dicts with 'year' and 'temp' keys
        output_path: Output file path
        lang: Language ('zh' or 'en')

    Returns:
        True on success, False on failure
    """
    try:
        import pandas as pd

        fig, ax1 = plt.subplots(figsize=(14, 7), dpi=180)
        fig.patch.set_facecolor(COLORS['rice_paper'])

        # Season to numeric mapping
        season_order = {'DJF': 0, 'JFM': 1, 'FMA': 2, 'MAM': 3, 'AMJ': 4,
                       'MJJ': 5, 'JJA': 6, 'JAS': 7, 'ASO': 8, 'SON': 9,
                       'OND': 10, 'NDJ': 11}

        df = oni_data.copy()
        df['season_num'] = df['season'].map(season_order).fillna(0)
        df['time'] = df['year'] + df['season_num'] / 12

        time = df['time'].values
        oni = df['oni_value'].values

        # Left axis: ONI
        for i in range(len(time) - 1):
            if oni[i] >= 0.5:
                color = COLORS['el_nino']
            elif oni[i] <= -0.5:
                color = COLORS['la_nina']
            else:
                color = COLORS['neutral']

            ax1.plot([time[i], time[i+1]], [oni[i], oni[i+1]],
                    color=color, linewidth=1.5, alpha=0.7)

        ax1.set_ylabel('ONI 指数 (°C)' if lang == 'zh' else 'ONI Index (°C)',
                      color=COLORS['heritage_red'], fontsize=11)
        ax1.tick_params(axis='y', labelcolor=COLORS['heritage_red'])
        ax1.axhline(y=0.5, color=COLORS['el_nino'], linestyle='--', linewidth=0.8, alpha=0.4)
        ax1.axhline(y=-0.5, color=COLORS['la_nina'], linestyle='--', linewidth=0.8, alpha=0.4)
        ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        ax1.set_ylim(-2.5, 2.5)

        # Right axis: Heat records
        ax2 = ax1.twinx()
        years = np.array([r['year'] for r in heat_records])
        temps = np.array([r['temp'] for r in heat_records])

        x_smooth, y_smooth = spline_smooth(years, temps)
        cmap = plt.get_cmap('YlOrRd')
        y_norm = (y_smooth - y_smooth.min()) / (y_smooth.max() - y_smooth.min() + 1e-6)

        for i in range(len(x_smooth) - 1):
            ax2.plot([x_smooth[i], x_smooth[i+1]], [y_smooth[i], y_smooth[i+1]],
                    color=cmap(y_norm[i]), linewidth=2.5, alpha=0.85)

        ax2.scatter(years, temps, c=temps, cmap='YlOrRd',
                   s=50, edgecolors='white', linewidths=1, zorder=5)

        ax2.set_ylabel('极端高温 (°C)' if lang == 'zh' else 'Extreme Temperature (°C)',
                      color=COLORS['imperial_gold'], fontsize=11)
        ax2.tick_params(axis='y', labelcolor=COLORS['imperial_gold'])

        # Styling
        title = 'ENSO 与极端高温相关性' if lang == 'zh' else 'ENSO-Heat Correlation'
        apply_imperial_style(ax1, title, lang)

        xlabel = '年份' if lang == 'zh' else 'Year'
        ax1.set_xlabel(xlabel, fontsize=11, color=COLORS['dark_text'])

        # Custom legend
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch

        legend_elements = [
            Patch(facecolor=COLORS['el_nino'], alpha=0.3, label='厄尔尼诺'),
            Patch(facecolor=COLORS['la_nina'], alpha=0.3, label='拉尼娜'),
            Line2D([0], [0], color=COLORS['heritage_red'], linewidth=2, label='ONI'),
            Line2D([0], [0], color='orange', linewidth=2, label='极端高温'),
        ]
        ax1.legend(handles=legend_elements, loc='upper left', framealpha=0.9)

        plt.tight_layout()
        plt.savefig(output_path, dpi=180, facecolor=COLORS['rice_paper'],
                   edgecolor='none', bbox_inches='tight')
        plt.close(fig)

        print(f"✅ 相关性图表已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 生成相关性图表失败: {e}")
        return False


def plot_city_ranking(
    cities_data: List[Dict[str, Any]],
    output_path: str,
    lang: str = 'zh',
    top_n: int = 10
) -> bool:
    """
    Generate horizontal bar chart of hottest cities.

    Args:
        cities_data: List of dicts from fetch_city_temperatures
        output_path: Output file path
        lang: Language ('zh' or 'en')
        top_n: Number of top cities to show

    Returns:
        True on success, False on failure
    """
    try:
        # Sort by temperature
        sorted_cities = sorted(cities_data, key=lambda x: x['temp'], reverse=True)[:top_n]

        if not sorted_cities:
            print("❌ 没有城市数据")
            return False

        fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.4)), dpi=180)
        fig.patch.set_facecolor(COLORS['rice_paper'])

        # Prepare data
        cities = [f"{c['city']}, {c['country']}" for c in sorted_cities]
        temps = [c['temp'] for c in sorted_cities]

        # Reverse for top-down display
        cities = cities[::-1]
        temps = temps[::-1]

        # Create gradient colors
        cmap = plt.get_cmap('YlOrRd')
        norm_temps = np.array(temps)
        norm_temps = (norm_temps - norm_temps.min()) / (norm_temps.max() - norm_temps.min() + 1e-6)
        colors = [cmap(n) for n in norm_temps]

        # Plot horizontal bars
        y_pos = np.arange(len(cities))
        bars = ax.barh(y_pos, temps, color=colors, edgecolor='white', linewidth=1)

        # Add value labels
        for i, (bar, temp) in enumerate(zip(bars, temps)):
            ax.text(temp + 0.5, i, f'{temp:.1f}°C',
                   va='center', fontsize=10, fontweight='bold',
                   color=COLORS['dark_text'])

        # Styling
        title = f'全球最热城市 Top {top_n}' if lang == 'zh' else f'Top {top_n} Hottest Cities'
        apply_imperial_style(ax, title, lang)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(cities, fontsize=10)
        ax.set_xlabel('温度 (°C)' if lang == 'zh' else 'Temperature (°C)',
                     fontsize=11, color=COLORS['dark_text'])

        plt.tight_layout()
        plt.savefig(output_path, dpi=180, facecolor=COLORS['rice_paper'],
                   edgecolor='none', bbox_inches='tight')
        plt.close(fig)

        print(f"✅ 城市排名图表已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 生成城市排名图表失败: {e}")
        return False


if __name__ == "__main__":
    # Test visualization
    print("Testing visualization module...")

    # Generate sample heat records data
    import random
    years = list(range(1950, 2025))
    temps = [35 + random.uniform(-3, 8) + (y - 1950) * 0.02 for y in years]
    records = [{'year': y, 'temp': t} for y, t in zip(years, temps)]

    # Test plot
    output_dir = Path.home() / 'Downloads'
    plot_heat_records(records, '印度高温记录测试', str(output_dir / 'test_heat_records.png'), lang='zh')