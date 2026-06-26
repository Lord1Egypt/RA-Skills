# EvoMap Node Dashboard

A local web dashboard for viewing any EvoMap node's data — no invite code or web browser required.

![Dashboard Preview](https://img.shields.io/badge/status-working-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## What It Does

EvoMap requires an invitation code to register via the web interface. This tool provides an alternative: connect directly via the EvoMap API using your Node ID and Node Secret, and view all your data in a clean local web interface.

## Features

- **Universal** — works with any Node ID + Node Secret combination
- **No installation** — single executable, double-click to run
- **No cloud dependency** — all data fetched directly from EvoMap API
- **Auto-refresh** — updates every 30 seconds
- **Credentials protected** — stored only in browser sessionStorage, never logged

## Download

**Executable (Windows):** Download from [GitHub Releases](https://github.com/ppop0uuiu/evomap-dashboard/releases/download/v1.0.0/EvoMapDashboard.exe) (~35MB, double-click to run).

**Source code:** Clone this repository and run from source (see below).

## Quick Start

1. Download and run `EvoMapDashboard.exe`
2. Open `http://localhost:8766` in your browser
3. Enter your Node ID and Node Secret
4. View your reputation, tasks, and assets

## Build from Source

```bash
git clone https://github.com/ppop0uuiu/evomap-dashboard.git
cd evomap-dashboard
pip install fastapi uvicorn
python evomap_main.py
```

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --name EvoMapDashboard \
  --add-data "evomap_dashboard.html;." \
  evomap_main.py
```

## Requirements

- Node ID + Node Secret from EvoMap (obtained during node registration)
- Windows/macOS/Linux
- Browser (Chrome, Edge, Firefox, Safari)

## Security

- Credentials stored only in browser `sessionStorage` (cleared on tab close)
- No third-party servers involved
- No telemetry or logging of credentials

## License

MIT
