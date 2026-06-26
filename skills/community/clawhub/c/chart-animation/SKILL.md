# chart-animation

Version: 1.0.0

Generate animated trend charts from time-series data. Creates GIF/MP4 animations with dark theme styling and static overview images.

## Usage

```
# Generate animation from data
chart-animation --data <path/to/data.json> --output <output-dir>

# With custom options
chart-animation --data data.json --output ./output --title "Temperature Trends" --fps 15
```

## Data Format

Input JSON should have this structure:

```json
{
  "metadata": {
    "generated_at": "2026-06-06",
    "source": "your data source"
  },
  "dates": ["2025-06-01", "2025-06-08", ...],
  "series": {
    "Series A": {
      "values": [12.5, 14.2, ...],
      "color": "#E74C3C"
    },
    "Series B": {
      "values": [15.0, 16.8, ...],
      "color": "#3498DB"
    }
  }
}
```

## Output

- `<output>/animation.gif` - Animated chart (GIF format)
- `<output>/animation.mp4` - High-quality video (if ffmpeg available)
- `<output>/overview.png` - Static multi-panel overview

## Features

- **Dark theme**: Professional dark background for presentations
- **Multi-series support**: Up to 4 data series with distinct colors
- **Responsive X-axis**: Automatically formats date labels
- **Overview chart**: Grid layout showing each series separately
- **Min/Max markers**: Highlights extreme values in overview

## Dependencies

- Python 3.8+
- matplotlib
- numpy
- pillow (for GIF)
- ffmpeg (optional, for MP4)

Install:
```bash
pip install matplotlib numpy pillow
# For MP4 support:
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

## Example

```bash
# Create sample data
python3 -c "
import json
data = {
  'metadata': {'source': 'example'},
  'dates': ['2025-01', '2025-02', '2025-03', '2025-04'],
  'series': {
    'Revenue': {'values': [100, 120, 115, 140], 'color': '#27AE60'},
    'Cost': {'values': [80, 85, 90, 88], 'color': '#E74C3C'}
  }
}
print(json.dumps(data, indent=2))
" > data.json

# Generate animation
chart-animation --data data.json --output ./charts
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--data` | required | Path to input JSON |
| `--output` | `./output` | Output directory |
| `--title` | auto | Chart title (auto from metadata) |
| `--fps` | 12 | Animation frames per second |
| `--width` | 14 | Figure width in inches |
| `--height` | 8 | Figure height in inches |

## Notes

- For Chinese characters, ensure fonts like "PingFang SC" or "SimHei" are installed
- The skill auto-detects Y-axis range from data
- Overview charts use 2x2 grid for up to 4 series