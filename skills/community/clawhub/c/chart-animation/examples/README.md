# Chart Animation Examples

## Example 1: Temperature Trends

```json
{
  "metadata": {
    "generated_at": "2026-06-06",
    "source": "weather API",
    "title": "Temperature Trends"
  },
  "ylabel": "Temperature (°C)",
  "dates": [
    "2025-06-01", "2025-06-08", "2025-06-15", "2025-06-22",
    "2025-06-29", "2025-07-06", "2025-07-13", "2025-07-20"
  ],
  "series": {
    "Beijing": {
      "values": [22, 25, 28, 30, 29, 31, 30, 28],
      "color": "#E74C3C"
    },
    "Shanghai": {
      "values": [24, 26, 28, 30, 31, 32, 31, 30],
      "color": "#3498DB"
    },
    "Guangzhou": {
      "values": [28, 29, 30, 31, 32, 33, 32, 31],
      "color": "#27AE60"
    }
  }
}
```

## Example 2: Revenue vs Cost

```json
{
  "metadata": {
    "title": "Quarterly Financials"
  },
  "ylabel": "Amount ($K)",
  "dates": ["Q1", "Q2", "Q3", "Q4"],
  "series": {
    "Revenue": {
      "values": [150, 180, 165, 200],
      "color": "#27AE60"
    },
    "Cost": {
      "values": [100, 110, 105, 120],
      "color": "#E74C3C"
    }
  }
}
```

## Example 3: Website Traffic

```json
{
  "metadata": {
    "title": "Monthly Website Traffic"
  },
  "ylabel": "Visitors (K)",
  "dates": [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ],
  "series": {
    "Organic": {
      "values": [45, 52, 58, 63, 70, 85, 92, 88, 75, 68, 72, 80],
      "color": "#27AE60"
    },
    "Social": {
      "values": [20, 25, 30, 28, 35, 40, 45, 42, 38, 32, 35, 42],
      "color": "#3498DB"
    },
    "Direct": {
      "values": [15, 18, 20, 22, 25, 28, 30, 28, 25, 23, 25, 28],
      "color": "#F39C12"
    }
  }
}
```

## Usage

```bash
# Generate from example file
python3 scripts/chart_animation.py --data examples/temperature.json --output ./output

# With custom title
python3 scripts/chart_animation.py --data examples/revenue.json --output ./charts --title "Revenue Trends 2025"

# Adjust size and FPS
python3 scripts/chart_animation.py --data examples/traffic.json --output ./output --width 16 --height 10 --fps 15
```