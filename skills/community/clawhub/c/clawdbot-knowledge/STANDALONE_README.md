# 🎙️ SpeakMCP Standalone System

Vollständig selbstständige SpeakMCP-Installation mit allen MCP-Servern lokal.

## 📁 Projektstruktur

```
SpeakMCP/
├── apps/desktop/                  # Electron Desktop App
├── mcp-servers/                   # Alle MCP Server (lokal)
│   ├── fatoni-bridge/             # 33 Tools - 16 FATONI AI Agents
│   ├── n8n-mcp-bidirectional/     # 🔄 Bidirektional - n8n API
│   ├── n8n-mcp/                   # Generator-only Version
│   ├── kadis-control/             # 7 Tools - Desktop Automation
│   ├── deepsynaptica/             # 9 Tools - AGI System
│   ├── docling-mcp/               # 19 Tools - Pinecone RAG
│   ├── docling-rag/               # 6 Tools - RAG Search API
│   ├── knowledge/                 # FATONI Knowledge Files
│   ├── .env                       # API Keys (erstellen!)
│   ├── requirements.txt           # Python Dependencies
│   ├── standalone-config.json
│   └── apply_standalone_config.py
├── setup_standalone.ps1           # Setup Script
├── start_standalone.ps1           # Start Script
└── STANDALONE_README.md           # Diese Datei
```

## 🚀 Quick Start

### 1. Setup (einmalig)
```powershell
.\setup_standalone.ps1
```

### 2. Starten
```powershell
.\start_standalone.ps1
```

## 🖥️ MCP Server (20+)

### Lokale Server (im Projekt)
| Server | Tools | Beschreibung |
|--------|-------|--------------|
| fatoni-bridge | 33 | 16 FATONI AI Agents |
| **n8n-mcp** | 15+ | 🔄 **Bidirektional** - n8n API Integration |
| n8n-generator | 9 | Workflow-Generierung (disabled) |
| kadis-control | 7 | Desktop Automation (Maus/Tastatur) |
| deepsynaptica | 9 | AGI System (Cognition/Semantic) |
| docling-mcp | 19 | Pinecone RAG |
| docling-rag | 6 | RAG Search API |

### NPX Server (automatisch geladen)
| Server | Beschreibung |
|--------|--------------|
| exa | AI Web Search (7 Tools) |
| playwright | Browser Automation |
| context7 | Code Documentation |
| filesystem | File Operations |
| fetch | Web Fetching |
| memory | Persistent Memory |
| sequential-thinking | Step Reasoning |
| github | GitHub API |
| brave-search | Web Search |
| notion | Notion API |
| figma | Design System |
| supabase | Database/Auth |

## 📋 Voraussetzungen

- **Node.js 18+** mit pnpm
- **Python 3.10+**
- **Git**
- **n8n** (lokal oder cloud) für bidirektionale Workflows

## 🔧 Manuelle Konfiguration

Die Konfiguration wird automatisch angewendet. Falls nötig:

```powershell
cd mcp-servers
python apply_standalone_config.py
```

---

## 🔄 n8n Bidirektionale Integration

### Was ist bidirektional?

| Modus | Beschreibung |
|-------|--------------|
| **Unidirektional** | Nur Workflows generieren (JSON erstellen) |
| **Bidirektional** | Workflows generieren UND mit n8n-Instanz kommunizieren |

### Bidirektionale Funktionen

- ✅ Workflows von n8n abrufen (`GET /api/v1/workflows`)
- ✅ Workflows direkt in n8n erstellen (`POST /api/v1/workflows`)
- ✅ Workflows aktivieren/deaktivieren
- ✅ Workflow-Ausführung triggern
- ✅ Webhooks empfangen und verarbeiten
- ✅ Credential-Management

### Konfiguration

**1. `.env` Datei erstellen:**

```bash
# mcp-servers/.env
N8N_API_KEY=n8n_api_xxxxxxxxxxxxxxxxxxxxx
N8N_BASE_URL=http://localhost:5678
```

**2. n8n API Key erstellen:**

1. n8n öffnen → Settings → API
2. "Create API Key" klicken
3. Key kopieren und in `.env` einfügen

**3. n8n Cloud:**

```bash
N8N_BASE_URL=https://your-instance.app.n8n.cloud
```

### Ohne Credentials

Wenn keine Credentials gesetzt sind, funktioniert der Server im **Generator-Modus**:
- Workflows werden als JSON generiert
- Können manuell in n8n importiert werden
- Keine API-Kommunikation

---

## 🎤 Voice Commands

Nach dem Start kannst du per Spracheingabe:

| Command | Server | Aktion |
|---------|--------|--------|
| "Analysiere diese Datei" | FATONI/DeepSynaptica | Dateianalyse |
| "Erstelle einen n8n Workflow für..." | n8n-mcp | Workflow generieren + deployen |
| "Liste meine n8n Workflows" | n8n-mcp | Workflows von n8n abrufen |
| "Aktiviere Workflow XY" | n8n-mcp | Workflow aktivieren |
| "Klicke auf den Button" | kadis-control | Desktop Automation |
| "Suche im Web nach..." | exa/brave-search | Web-Suche |
| "Öffne die Webseite..." | playwright | Browser öffnen |

---

## 📦 Portabilität

Das gesamte Projekt kann kopiert/verschoben werden:
1. Ordner kopieren
2. `.\setup_standalone.ps1` ausführen
3. `.\start_standalone.ps1` starten

Die Konfiguration wird automatisch auf den neuen Pfad angepasst.

---

## 🔐 Credentials Übersicht

| Server | Env Variable | Beschreibung |
|--------|--------------|--------------|
| n8n-mcp | `N8N_API_KEY` | n8n API Key |
| n8n-mcp | `N8N_BASE_URL` | n8n URL (default: localhost:5678) |
| exa | `EXA_API_KEY` | Exa Search API |
| brave-search | `BRAVE_API_KEY` | Brave Search API |
| github | `GITHUB_TOKEN` | GitHub Personal Access Token |
| notion | `NOTION_API_KEY` | Notion Integration Token |
| supabase | `SUPABASE_URL` | Supabase Project URL |
| supabase | `SUPABASE_KEY` | Supabase API Key |
| docling-mcp | `PINECONE_API_KEY` | Pinecone API Key |
| deepsynaptica | `OPENAI_API_KEY` | OpenAI API Key |

---
**Version:** 2.0 | **Erstellt:** 2025-12-27 | **Bidirektional:** ✅

