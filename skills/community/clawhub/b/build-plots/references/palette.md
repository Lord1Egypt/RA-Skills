# Restrained, accessible plot palette

Use one accent plus neutrals by default. Add categorical colors only when category identity is essential and cannot be carried by position or labels.

## Core colors

| Role | Hex | Use |
|---|---|---|
| Ink | `#222222` | Titles, primary labels, total bars |
| Muted text | `#626A73` | Secondary labels, source notes |
| Context gray | `#B8BEC6` | Non-focal bars and lines |
| Grid | `#E3E6EA` | Sparse guide lines |
| Primary blue | `#0072B2` | Default focal series, positive change |
| Orange | `#E69F00` | Second focal series or warning |
| Bluish green | `#009E73` | Positive status when blue is occupied |
| Vermillion | `#D55E00` | Negative change or exception |
| Sky blue | `#56B4E9` | Supporting categorical series |
| Purple | `#CC79A7` | Supporting categorical series |
| Yellow | `#F0E442` | Sparse highlight only; never small text on white |

The categorical hues follow the Okabe-Ito colorblind-safe family. Do not use all colors merely because they are available.

## Ordered palettes

Sequential blue, low to high:

```python
["#E8F1F8", "#C7DDEB", "#93BED5", "#5599C2", "#1976AD", "#084A72"]
```

Diverging exception-to-positive, centered on a meaningful reference:

```python
["#B2182B", "#D6604D", "#F4A582", "#F7F7F7", "#92C5DE", "#4393C3", "#2166AC"]
```

Ordered survey responses:

```python
{
    "Strongly disagree": "#B2182B",
    "Disagree": "#EF8A62",
    "Neutral": "#D9D9D9",
    "Agree": "#67A9CF",
    "Strongly agree": "#2166AC",
}
```

## Application rules

1. Map meaning to color before writing plotting code.
2. Keep unchanged context gray.
3. Use the primary blue for the statement in the title.
4. Reserve vermillion for losses, failures, or exceptions; do not use red and green as the only distinction.
5. Use identical mappings in Matplotlib, Seaborn, and Bokeh outputs.
6. Check grayscale legibility and add direct labels, shapes, or line styles where needed.
7. Avoid rainbow and jet palettes because they introduce false visual boundaries and unordered hue changes.
