# Travel Mapify (flyai-travelmapify)

Turn travel plans into interactive route maps: parse screenshots or comma-separated place names, geocode with Amap, and emit a self-contained HTML map with optional **FlyAI** hotel search.

**License:** MIT · **Author:** rudy2steiner

## Features

- **Image mode** — POI extraction from travel-plan images (AI vision–assisted workflow; see `SKILL.md` for agent steps).
- **Text mode** — Comma-separated locations with automatic city detection (defaults to Shanghai when unclear).
- **Interactive HTML** — Edit / view modes, reorder POIs, route on the map, unique per-map `localStorage` IDs.
- **Hotels** — Real hotel search via FlyAI when the hotel server is running (see `SKILL.md`).

## Requirements

- Python 3.7+
- [FlyAI CLI](https://www.npmjs.com/package/@openclaw/flyai): `npm install -g @openclaw/flyai`
- Valid **Amap** Web API access (typically via a local proxy; default `http://localhost:8769`)
- Modern browser; serve the HTML over **HTTP** (not `file://`) for full behavior

Full setup, env overrides, and troubleshooting: **[INSTALL.md](INSTALL.md)**.

## Quick start

From this directory:

```bash
# Text input
python3 flyai-travelmapify.py --locations "上海外滩,上海迪士尼乐园,豫园" --output-html shanghai-trip.html

# Image input
python3 flyai-travelmapify.py --image /path/to/plan.jpg --output-html my-trip.html

# Custom ports (HTTP + hotel server)
python3 flyai-travelmapify.py --locations "Tokyo Tower,Shibuya Crossing" --output-html tokyo.html --http-port 8080 --hotel-port 9000
```

The enhanced pipeline may start a local HTTP server (default **9000**) and hotel search server (default **8770**); URLs are printed when applicable.

```bash
python3 flyai-travelmapify.py --help
```

## Project layout

| Path | Role |
|------|------|
| `flyai-travelmapify.py` | Portable CLI entry (delegates to `scripts/main_travel_mapify_enhanced.py`) |
| `scripts/` | Geocoding, template generation, hotel server, vision helpers |
| `assets/templates/` | HTML template(s) for generated maps |
| `references/` | Amap notes, POI rules, troubleshooting |
| `SKILL.md` | **OpenClaw / agent workflow** — when to use, full steps, UX details |
| `INSTALL.md` | Installation and configuration |
| `DEPLOYMENT.md` | Deployment notes |

## Documentation

- Agents using this skill should follow **[SKILL.md](SKILL.md)** (version **2.2.0** in that file).
- Operators: **[INSTALL.md](INSTALL.md)**, **[DEPLOYMENT.md](DEPLOYMENT.md)**, **[references/troubleshooting-guide.md](references/troubleshooting-guide.md)**.
