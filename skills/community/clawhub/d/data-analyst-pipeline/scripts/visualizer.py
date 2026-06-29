"""
Chart generator for data analysis.
Produces distribution histograms, boxplots, correlation heatmaps, bar charts, and scatter plots.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from pathlib import Path


_font_initialized = False

def _init_font():
    """Initialize CJK font support. Called once before chart generation."""
    global _font_initialized
    if _font_initialized:
        return
    fm._load_fontmanager(try_read_cache=False)
    available = {f.name for f in fm.fontManager.ttflist}
    for font_name in ['Microsoft YaHei', 'SimHei', 'Noto Sans SC', 'KaiTi']:
        if font_name in available:
            plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans', 'Arial']
            plt.rcParams['font.family'] = 'sans-serif'
            _font_initialized = True
            return
    plt.rcParams['font.family'] = 'sans-serif'
    _font_initialized = True
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('whitegrid')
CHART_DIR = None  # Set by generate_all_charts


def generate_all_charts(df: pd.DataFrame, eda_results: dict, output_dir: str,
                        target_col: str = None) -> dict:
    """
    Generate all charts and save to output directory.

    Args:
        df: Cleaned DataFrame
        eda_results: Results from eda_runner.run_eda()
        output_dir: Directory to save charts
        target_col: Optional target column

    Returns:
        Dict mapping chart names to file paths
    """
    global CHART_DIR
    CHART_DIR = output_dir
    os.makedirs(output_dir, exist_ok=True)
    _init_font()

    charts = {}
    numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns]
    cat_cols = [c for c in df.select_dtypes(include=['object', 'category']).columns]

    # 1. Distribution histograms for top numeric columns
    charts['distributions'] = _plot_distributions(df, numeric_cols[:6])

    # 2. Box plots for detecting outliers
    if len(numeric_cols) >= 1:
        charts['boxplots'] = _plot_boxplots(df, numeric_cols[:8])

    # 3. Correlation heatmap
    if len(numeric_cols) >= 2:
        charts['correlation_heatmap'] = _plot_correlation_heatmap(df, numeric_cols)

    # 4. Missing value bar chart
    charts['missing_values'] = _plot_missing_values(df)

    # 5. Top categorical distributions
    if cat_cols:
        charts['categorical_top'] = _plot_categorical_top(df, cat_cols[:4])

    # 6. Pair plot (sample, for small datasets)
    if len(numeric_cols) >= 2 and len(numeric_cols) <= 5 and len(df) <= 5000:
        charts['pairplot'] = _plot_pairplot(df, numeric_cols, target_col)

    # 7. Numeric feature vs target
    if target_col and target_col in df.columns and numeric_cols:
        charts['target_vs_features'] = _plot_target_vs_features(df, target_col, numeric_cols[:4])

    print(f"[Visualizer] Generated {len(charts)} chart groups in {output_dir}")
    return charts


def _save_fig(name: str) -> str:
    """Save current figure and return path."""
    path = os.path.join(CHART_DIR, f'{name}.png')
    plt.tight_layout()
    plt.savefig(path, dpi=100, bbox_inches='tight')
    plt.close()
    return path


def _plot_distributions(df: pd.DataFrame, cols: list) -> list:
    """Histogram + KDE for top numeric columns."""
    paths = []
    n = len(cols)
    if n == 0:
        return paths

    cols_per_fig = min(3, n)
    figs_needed = (n + cols_per_fig - 1) // cols_per_fig

    for fig_idx in range(figs_needed):
        start = fig_idx * cols_per_fig
        end = min(start + cols_per_fig, n)
        current_cols = cols[start:end]
        fig, axes = plt.subplots(1, len(current_cols), figsize=(5 * len(current_cols), 4))
        if len(current_cols) == 1:
            axes = [axes]

        for ax, col in zip(axes, current_cols):
            series = df[col].dropna()
            ax.hist(series, bins=30, alpha=0.7, color='#3498db', edgecolor='white')
            ax.axvline(series.mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean={series.mean():.1f}')
            ax.axvline(series.median(), color='#2ecc71', linestyle='-', linewidth=1.5, label=f'Median={series.median():.1f}')
            ax.set_title(f'{col}', fontsize=12)
            ax.legend(fontsize=8)

        path = _save_fig(f'dist_{fig_idx+1}')
        paths.append(path)

    return paths


def _plot_boxplots(df: pd.DataFrame, cols: list) -> str:
    """Single figure with boxplots."""
    fig, ax = plt.subplots(figsize=(max(8, len(cols) * 1.2), 5))
    df_plot = df[cols].copy()

    # Normalize to 0-1 range for comparability
    df_norm = (df_plot - df_plot.min()) / (df_plot.max() - df_plot.min() + 1e-10)
    df_norm.boxplot(ax=ax, patch_artist=True,
                    boxprops=dict(facecolor='#3498db', alpha=0.6),
                    medianprops=dict(color='#e74c3c', linewidth=2))
    ax.set_title('Feature Distributions (Box Plot)', fontsize=14)
    ax.set_ylabel('Normalized Value')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    return _save_fig('boxplots')


def _plot_correlation_heatmap(df: pd.DataFrame, cols: list) -> str:
    """Correlation heatmap."""
    corr = df[cols].corr()
    figsize = max(6, len(cols) * 0.8)
    fig, ax = plt.subplots(figsize=(figsize, figsize))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, vmin=-1, vmax=1, square=True,
                linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
    ax.set_title('Correlation Heatmap', fontsize=14)
    return _save_fig('correlation_heatmap')


def _plot_missing_values(df: pd.DataFrame) -> str:
    """Missing value bar chart."""
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.text(0.5, 0.5, 'No missing values!', ha='center', va='center', fontsize=14)
        ax.set_axis_off()
        return _save_fig('missing_values')

    fig, ax = plt.subplots(figsize=(max(6, len(missing) * 0.5), 4))
    colors = ['#e74c3c' if v / len(df) > 0.2 else '#f39c12' if v / len(df) > 0.05 else '#3498db'
              for v in missing.values]
    bars = ax.bar(range(len(missing)), [v / len(df) * 100 for v in missing.values], color=colors)
    ax.set_xticks(range(len(missing)))
    ax.set_xticklabels(missing.index, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Missing (%)')
    ax.set_title('Missing Values by Column', fontsize=14)

    for bar, v in zip(bars, missing.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'{v}', ha='center', fontsize=8)

    return _save_fig('missing_values')


def _plot_categorical_top(df: pd.DataFrame, cols: list) -> list:
    """Top categories bar charts."""
    paths = []
    for col in cols:
        vc = df[col].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(range(len(vc)), vc.values, color='#3498db', alpha=0.8)
        ax.set_xticks(range(len(vc)))
        ax.set_xticklabels([str(v)[:20] for v in vc.index], rotation=45, ha='right', fontsize=8)
        ax.set_title(f'Top 10: {col}', fontsize=12)
        ax.set_ylabel('Count')
        for bar, v in zip(bars, vc.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(v), ha='center', fontsize=7)
        paths.append(_save_fig(f'cat_{col[:20]}'))
    return paths


def _plot_pairplot(df: pd.DataFrame, cols: list, target_col: str = None) -> str:
    """Pair plot for small datasets."""
    try:
        plot_cols = [c for c in cols if c in df.columns]
        if target_col and target_col in df.columns and target_col not in plot_cols:
            plot_cols.append(target_col)
        if len(plot_cols) < 2:
            return ''

        sample_df = df[plot_cols].sample(min(1000, len(df))).dropna()
        if len(sample_df) < 5:
            return ''

        hue = None
        if target_col and target_col in sample_df.columns:
            # Bin numeric target or use as-is for categorical
            if pd.api.types.is_numeric_dtype(sample_df[target_col]):
                if sample_df[target_col].nunique() <= 10:
                    sample_df[target_col] = sample_df[target_col].astype(str)
                    hue = target_col
                else:
                    # Skip hue for continuous target — too many categories
                    hue = None
            else:
                hue = target_col

        g = sns.pairplot(sample_df, hue=hue, diag_kind='kde',
                         plot_kws={'alpha': 0.5, 's': 20})
        g.fig.suptitle('Pair Plot Matrix', y=1.02, fontsize=14)
        return _save_fig('pairplot')
    except Exception as e:
        print(f"[Visualizer] Pairplot failed: {e}")
        return ''


def _plot_target_vs_features(df: pd.DataFrame, target_col: str, feature_cols: list) -> list:
    """Feature vs target scatter/box plots."""
    paths = []
    target_is_cat = df[target_col].nunique() <= 10

    for col in feature_cols:
        fig, ax = plt.subplots(figsize=(6, 4))
        if target_is_cat:
            # Box plot by class
            df.boxplot(column=col, by=target_col, ax=ax, patch_artist=True)
        else:
            # Scatter
            ax.scatter(df[col], df[target_col], alpha=0.3, s=10, color='#3498db')
            ax.set_xlabel(col)
            ax.set_ylabel(target_col)
        ax.set_title(f'{col} vs {target_col}', fontsize=11)
        plt.suptitle('')
        paths.append(_save_fig(f'target_{col[:20]}'))
    return paths


if __name__ == "__main__":
    print("Visualizer module — import and use generate_all_charts()")
