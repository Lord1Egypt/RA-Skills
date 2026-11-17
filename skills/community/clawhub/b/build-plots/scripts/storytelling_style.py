"""Shared styling and export helpers for publication-ready plots."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#222222"
MUTED = "#626A73"
CONTEXT = "#B8BEC6"
GRID = "#E3E6EA"
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERMILLION = "#D55E00"
SKY = "#56B4E9"
PURPLE = "#CC79A7"
YELLOW = "#F0E442"

CATEGORICAL = [BLUE, ORANGE, GREEN, VERMILLION, SKY, PURPLE]
SEQUENTIAL_BLUE = ["#E8F1F8", "#C7DDEB", "#93BED5", "#5599C2", "#1976AD", "#084A72"]
DIVERGING = ["#B2182B", "#D6604D", "#F4A582", "#F7F7F7", "#92C5DE", "#4393C3", "#2166AC"]


def apply_style() -> None:
    """Apply restrained defaults while preserving vector text in PDF/SVG."""
    mpl.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.edgecolor": GRID,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "grid.alpha": 1.0,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def clean_axes(ax: plt.Axes, *, grid: str | None = "x") -> None:
    """Remove chart furniture and retain only useful guide lines."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(False)
    if grid:
        ax.grid(axis=grid)
        ax.set_axisbelow(True)


def add_source(fig: plt.Figure, text: str) -> None:
    """Add a quiet source note below the plotting area."""
    fig.text(0.01, 0.01, text, ha="left", va="bottom", fontsize=7.5, color=MUTED)


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> list[Path]:
    """Save review PNG plus vector PDF and SVG from one Matplotlib figure."""
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for suffix, kwargs in (
        ("png", {"dpi": 220}),
        ("pdf", {}),
        ("svg", {}),
    ):
        path = output_dir / f"{stem}.{suffix}"
        fig.savefig(path, bbox_inches="tight", pad_inches=0.12, **kwargs)
        outputs.append(path)
    plt.close(fig)
    return outputs
