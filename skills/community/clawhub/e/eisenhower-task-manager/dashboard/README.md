# Eisenhower Task Dashboard

Dynamic task dashboard for the eisenhower-task-manager skill with real-time Web interface.

## Features

- 📊 **Real-time Statistics** - Task counts by quadrant, customers, delegation, and maybe list
- 🔥 **Four-Quadrant Matrix** - Visual Q1-Q4 task distribution
- 🏢 **Customer Projects** - View all customers and their project status
- 👑 **Delegation** - Track tasks assigned to others
- 🌱 **Maybe List** - Manage "might do later" ideas
- ⚡ **Real-time Updates** - WebSocket pushes file changes instantly
- 🎨 **Dark Theme** - Modern dark UI design
- 🌐 **Bilingual** - English/Chinese language support

## Quick Start

### Auto-install & Run (Recommended)

```bash
cd dashboard
./start.sh              # Auto-installs deps on first run, then starts server
```

The script will:
1. Check if `node_modules` exists (install if missing)
2. Read your saved port (or use default 8080)
3. Start the server
4. Open `http://localhost:8080` in your browser

### Manual Setup

```bash
cd dashboard
npm install             # One-time setup
./start.sh              # Start server

# Or use custom port
./start.sh --port 3000
```

## Scripts

| Script | Description |
|--------|-------------|
| `./start.sh` | Start server with auto-install and port memory |
| `./check-and-install.sh` | Check and install dependencies only |
| `npm start` | Start server directly (requires deps installed) |

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/tasks` - Get all task data
- `WS /` - WebSocket real-time updates

## File Structure

```
dashboard/
├── server.js                # Express + WebSocket server
├── parser.js                # Markdown parser
├── package.json             # Dependencies
├── start.sh                 # Auto-install & start script ⭐
├── check-and-install.sh     # Dependency checker ⭐
├── port.conf                # Saved port config (auto-generated)
├── .gitignore               # Excludes node_modules
└── public/                  # Frontend files
    ├── index.html
    ├── style.css
    ├── app.js
    ├── i18n.js              # Bilingual support
    └── favicon.svg          # App icon
```

## Tech Stack

- **Backend**: Node.js, Express, WebSocket (ws), chokidar
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Real-time**: WebSocket

## Data Source

Automatically reads from `../tasks/` directory:
- `tasks.md` - Four-quadrant tasks
- `customer-projects.md` - Customer projects
- `delegation.md` - Delegated tasks
- `maybe.md` - Future ideas

## Port Configuration

The dashboard remembers your last used port:

```bash
# First run with custom port
./start.sh --port 3000

# Subsequent runs will use port 3000 automatically
./start.sh
```

Default port: `8080`
