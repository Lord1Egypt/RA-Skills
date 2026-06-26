# Citywalk Map Generator 🗺️

> Generate beautiful walking route maps with a single command, based on real OSM maps with horizontal full-width design.

---

## ✨ Features

- 🌏 **Real Maps** - OpenStreetMap data, routes never go through buildings
- 🚶 **Real Routes** - OSRM walking navigation, actual road geometry
- 🖥️ **Horizontal Full-Width** - Perfect on both desktop and mobile
- 🎨 **Custom Themes** - Change accent color with one env var (supports country colors)
- ⚡ **Zero Dependencies** - Pure Python + HTML + curl, no build tools

---

## 🚀 Quick Start

```bash
# Basic usage
python3 scripts/generate.py "My Route" "lat1,lon1,Start,desc|lat2,lon2,End,desc"

# Custom theme color
COLOR=#0055A4 python3 scripts/generate.py "Paris Walk" "..."

# View result
open /tmp/citywalk_map.html
```

---

## 📖 Usage

### Input Format

```
lat,lon,name,description
```

- `lat,lon` - Required, coordinates
- `name` - Required, display name
- `description` - Optional, shown in popup

Separate multiple waypoints with `|`.

### Getting Coordinates

Use [Nominatim](https://nominatim.openstreetmap.org/ui/search.html) to search for places, click "details" for exact coordinates.

### Common Theme Colors

| Country | Color Code | Description |
|--------|-----------|-------------|
| China | `#DE2910` | Chinese Red |
| France | `#0055A4` | French Blue |
| UK | `#012169` | British Blue |
| Japan | `#BC002D` | Japanese Red |
| USA | `#3C3B6E` | American Blue |
| Default | `#e94560` | Vibrant Pink |

### Screenshot Flow

```bash
# 1. Start HTTP server
python3 -m http.server 18767 --directory /tmp &

# 2. Open http://localhost:18767/citywalk_map.html in browser
# 3. Wait 20 seconds for OSM tiles to load
# 4. Screenshot
# 5. Stop server
pkill -f "http.server 18767"
```

---

## 🌍 Paris Example

```bash
COLOR=#0055A4 python3 scripts/generate.py \
  "Paris Louvre Citywalk" \
  "48.8606,2.3376,Louvre Pyramid|48.8641,2.3276,Tuileries Garden|48.8656,2.3211,Place de la Concorde|48.8637,2.3130,Pont Alexandre III|48.8738,2.2950,Arc de Triomphe|48.8595,2.3122,Les Invalides|48.8584,2.2945,Eiffel Tower"
```

---

## 🔧 Tech Stack

- **Map**: Leaflet.js + OpenStreetMap
- **Routing**: OSRM Walking Routing (router.project-osrm.org)
- **Geocoding**: Nominatim (OpenStreetMap)
- **Generation**: Python 3 (no pip dependencies, uses curl for OSRM)

---

## 📄 License

MIT License
