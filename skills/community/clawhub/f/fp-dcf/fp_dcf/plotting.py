from __future__ import annotations

from pathlib import Path

import numpy as np

from .schemas import SensitivityHeatmapOutput

try:  # pragma: no cover - optional dependency path
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.patches import Rectangle
except ImportError:  # pragma: no cover - exercised when viz deps are missing
    plt = None
    LinearSegmentedColormap = None
    Rectangle = None


def _require_matplotlib() -> None:
    if plt is None or LinearSegmentedColormap is None or Rectangle is None:
        raise RuntimeError(
            "Heatmap rendering requires matplotlib. Install the optional viz dependencies first, "
            "for example with `python3 -m pip install .[viz]`."
        )


def _format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def _get_text_color(bg_rgb: tuple[float, float, float, float]) -> str:
    # Use luminance to pick a legible foreground color for heatmap annotations.
    luminance = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
    return "#FFFFFF" if luminance < 0.5 else "#132A13"


def _format_metric(
    value: float | None,
    metric: str,
    currency: str | None,
    market_price: float | None = None,
) -> str:
    if value is None:
        return "N/A"

    main_text = ""
    if metric == "per_share_value":
        prefix = f"{currency} " if currency else ""
        if abs(value) >= 1000:
            main_text = f"{prefix}{value:,.0f}"
        elif abs(value) >= 100:
            main_text = f"{prefix}{value:,.1f}"
        else:
            main_text = f"{prefix}{value:,.2f}"
    else:
        scale = 1.0
        suffix = ""
        if abs(value) >= 1_000_000_000_000:
            scale = 1_000_000_000_000
            suffix = "T"
        elif abs(value) >= 1_000_000_000:
            scale = 1_000_000_000
            suffix = "B"
        elif abs(value) >= 1_000_000:
            scale = 1_000_000
            suffix = "M"

        prefix = f"{currency} " if currency else ""
        main_text = f"{prefix}{value / scale:,.1f}{suffix}"

    if market_price and market_price > 0:
        upside = (value / market_price) - 1.0
        sign = "+" if upside > 0 else ""
        return f"{main_text}\n({sign}{upside:.1%})"

    return main_text


def render_wacc_terminal_growth_heatmap(
    heatmap: SensitivityHeatmapOutput,
    output_path: str | Path,
    *,
    title: str | None = None,
) -> Path:
    _require_matplotlib()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    display_rows = list(reversed(heatmap.matrix))
    display_wacc_values = list(reversed(heatmap.wacc_values))
    data = np.array([[np.nan if value is None else value for value in row] for row in display_rows], dtype=float)
    masked = np.ma.masked_invalid(data)

    cmap = plt.get_cmap("Spectral_r")
    cmap.set_bad(color="#F4F4F9")

    cell_size = 1.2
    fig_width = max(8.0, cell_size * len(heatmap.terminal_growth_values) + 3.5)
    fig_height = max(6.0, cell_size * len(heatmap.wacc_values) + 2.5)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=200)

    image = ax.imshow(masked, cmap=cmap, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(heatmap.terminal_growth_values)))
    ax.set_xticklabels([_format_percent(value) for value in heatmap.terminal_growth_values], fontsize=10)
    ax.set_yticks(range(len(display_wacc_values)))
    ax.set_yticklabels([_format_percent(value) for value in display_wacc_values], fontsize=10)
    ax.set_xlabel("Terminal Growth Rate", fontsize=11, labelpad=10, fontweight="bold")
    ax.set_ylabel("WACC", fontsize=11, labelpad=10, fontweight="bold")

    chart_title = title or f"{heatmap.ticker} Sensitivity Analysis"
    ax.set_title(
        f"{chart_title}\n{heatmap.metric_label} across WACC x Terminal Growth",
        loc="left",
        fontsize=14,
        pad=20,
        fontweight="bold",
    )

    ax.set_xticks(np.arange(-0.5, len(heatmap.terminal_growth_values), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(display_wacc_values), 1), minor=True)
    ax.grid(which="minor", color="#FFFFFF", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(display_rows):
        for col_index, value in enumerate(row):
            if value is not None:
                masked_min = float(masked.min())
                masked_max = float(masked.max())
                norm_val = (value - masked_min) / (masked_max - masked_min) if masked_max != masked_min else 0.5
                text_color = _get_text_color(cmap(norm_val))
            else:
                text_color = "#9BA4B0"

            text = _format_metric(value, heatmap.metric, heatmap.currency, heatmap.market_price)
            ax.text(
                col_index,
                row_index,
                text,
                ha="center",
                va="center",
                fontsize=9,
                color=text_color,
                fontweight="medium" if value is not None else "normal",
            )

    if heatmap.base_wacc in heatmap.wacc_values and heatmap.base_terminal_growth_rate in heatmap.terminal_growth_values:
        base_row = display_wacc_values.index(heatmap.base_wacc)
        base_col = heatmap.terminal_growth_values.index(heatmap.base_terminal_growth_rate)
        ax.add_patch(
            Rectangle(
                (base_col - 0.48, base_row - 0.48),
                0.96,
                0.96,
                fill=False,
                linewidth=3.0,
                edgecolor="#2D3436",
                zorder=10,
            )
        )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.outline.set_visible(False)
    colorbar.ax.set_ylabel(heatmap.metric_label, rotation=270, labelpad=20, fontsize=10)

    note = "Base case (Current assumptions) is outlined in dark charcoal."
    if heatmap.market_price:
        note += f"\nParentheses show upside/downside vs market price ({heatmap.currency} {heatmap.market_price:,.2f})."
    note += "\nGrey cells indicate Terminal Growth >= WACC (Invalid models)."
    fig.text(
        0.01,
        -0.02,
        note,
        fontsize=9,
        color="#4A5568",
        ha="left",
    )

    plt.tight_layout()
    fig.savefig(path, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)
    return path
