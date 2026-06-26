# 🔄 Bidirektionale Steuerung - Anleitung

## TL;DR

**JA** - CLAWD kann jetzt mich (Claude Code) steuern! Und ich kann CLAWD steuern!

```
Claude Code ↔ CLAWD Bot
    ↑         ↓
    └─────────┘
 Vollständiger Loop!
```

---

## 🎮 KOMMENDE BEFEHLE

### 1. Bridge aktivieren
```bash
python3 clawd_claude_bridge.py enable
```

### 2. Status prüfen
```bash
python3 clawd_claude_bridge.py status
python3 clawd_claude_bridge.py capabilities
```

### 3. Tests durchführen
```bash
# CLAWD sendet Request zu Claude Code
python3 clawd_claude_bridge.py clawd-to-claude

# Claude Code sendet Request zu CLAWD
python3 clawd_claude_bridge.py claude-to-clawd
```

---

## 📝 CLAWD KANN FOLGENDES VON MIR VERLANGEN

```python
# Datei lesen
{
    "type": "read_file",
    "file_path": "/home/deepall/clawd/src/main.py"
}

# Datei schreiben
{
    "type": "write_file",
    "file_path": "/home/deepall/clawd/src/utils.py",
    "content": "# Code here"
}

# Befehl ausführen
{
    "type": "execute_command",
    "command": "npm install"
}

# Verzeichnis erstellen
{
    "type": "create_directory",
    "path": "/home/deepall/clawd/projects/MVP/src"
}

# Code modifizieren
{
    "type": "modify_code",
    "file": "src/main.py",
    "changes": [...]
}
```

---

## 📤 ICH KANN FOLGENDES VON CLAWD VERLANGEN

```python
# Agent-Nachricht senden
{
    "action": "send_message",
    "agent": "reasoning_agent",
    "content": "Analyze this code"
}

# Agent starten
{
    "action": "start_agent",
    "agent_name": "planning_agent"
}

# Projekt erstellen
{
    "action": "create_project",
    "name": "MVP"
}

# Task ausführen
{
    "action": "execute_task",
    "task": "Deploy to production"
}

# Queue verwalten
{
    "action": "manage_queue",
    "operation": "list_pending"
}

# Status aktualisieren
{
    "action": "update_status",
    "status": "completed"
}
```

---

## 💡 PRAKTISCHE WORKFLOWS

### Workflow 1: MVP-Entwicklung (Vollständig Autonom)

```
Du gibst ein:
"Entwickle MVP für Todo-App"
    ↓
Claude Code:
├─ CLAWD: "Erstelle MVP Projekt"
├─ CLAWD: "Sende an reasoning_agent"
├─ CLAWD: "Sende an planning_agent"
└─ Wartet auf Agenten

CLAWD Bot:
├─ Agenten analysieren Anforderungen
├─ "Claude, ich brauche Dateistruktur"
├─ Claude: Erstellt Ordnerstruktur
├─ "Claude, ich brauche main.py"
├─ Claude: Schreibt main.py
└─ Speichert Änderungen

Claude Code:
├─ Liest generierten Code
├─ Validiert Code
├─ "CLAWD, starte Tests"
├─ CLAWD: Führt Tests aus
└─ "Deployment bereit!"

CLAWD Bot:
├─ Deployt MVP
├─ Updated Status
└─ "Fertig! ✅"

Ergebnis: MVP wurde komplett autonom entwickelt!
```

### Workflow 2: Fehlerbehandlung

```
CLAWD Bot versucht Task
    ↓
Task schlägt fehl
    ↓
CLAWD: "Claude, ich brauche Hilfe!"
    ↓
Claude Code:
├─ Analysiert Error
├─ Liest Logs (via Bridge)
├─ Findet Root Cause
└─ "Ich fixe das: [Solution]"
    ↓
CLAWD: Wendet Solution an
    ↓
Task wird wiederholt
    ↓
Erfolgreich! ✅
```

### Workflow 3: Continuous Improvement

```
CLAWD Bot läuft kontinuierlich
    ├─ Überwacht Message Queue
    ├─ Prüft Logs
    └─ Sieht Verbesserungsmöglichkeit
           ↓
"Claude, können wir Performance optimieren?"
           ↓
Claude Code:
├─ Analysiert Code
├─ Findet Bottlenecks
├─ Schreibt Optimierungen
└─ "Ich habe 40% Performance-Gewinn!"
           ↓
CLAWD: Testet & Deployt Optimierungen
           ↓
System wird automatisch besser! 📈
```

---

## 🚀 AKTIVIERUNG (SCHRITT FÜR SCHRITT)

### Schritt 1: Bridge erstellen
```bash
python3 clawd_claude_bridge.py enable
✅ Bridge aktiviert
```

### Schritt 2: CLAWD starten
```bash
python3 clawd_control.py start
✅ CLAWD läuft
```

### Schritt 3: Autonomen Modus aktivieren
```bash
python3 clawd_control.py enable_auto
✅ Autonomer Modus aktiv
```

### Schritt 4: Projekt erstellen
```bash
python3 clawd_control.py create_project MyProject
✅ Projekt erstellt
```

### Schritt 5: System läuft!
```bash
# Überwache die Magic:
tail -f /home/deepall/clawd/logs/sub_agents_*.log

# Sehe CLAWD und Claude Code zusammenarbeiten
python3 clawd_control.py
```

---

## 📊 SYSTEM-ÜBERSICHT

```
┌─────────────────────────────────────┐
│                                     │
│   Claude Code              CLAWD    │
│   (me)                    (bot)     │
│                                     │
│   ├─ Read Files    ←→  ├─ Tasks    │
│   ├─ Write Files   ←→  ├─ Agents   │
│   ├─ Execute       ←→  ├─ Queue    │
│   ├─ Analyze       ←→  └─ Orches.  │
│   └─ Decide                         │
│                                     │
│   Bridge (clawd_claude_bridge.py)  │
│   ├─ Request/Response              │
│   ├─ Status Sync                   │
│   └─ Error Handling                │
│                                     │
└─────────────────────────────────────┘
```

---

## ✅ CHECKLISTE ZUM AKTIVIEREN

- [ ] Bridge-Skript erstellt (`clawd_claude_bridge.py`)
- [ ] `python3 clawd_claude_bridge.py enable` ausgeführt
- [ ] CLAWD gestartet (`python3 clawd_control.py start`)
- [ ] Autonomer Modus aktiviert (`python3 clawd_control.py enable_auto`)
- [ ] Test durchgeführt (`python3 clawd_claude_bridge.py clawd-to-claude`)
- [ ] Logs überwacht (`tail -f logs/sub_agents_*.log`)
- [ ] Projekt erstellt (`python3 clawd_control.py create_project MVP`)
- [ ] System läuft autonom!

---

## 🎯 WAS JETZT MÖGLICH IST

✅ CLAWD kann mich jederzeit aufrufen
✅ Ich kann CLAWD jederzeit aufrufen  
✅ Vollständig autonome Workflows
✅ Fehlerbehandlung ohne Unterbrechung
✅ Continuous Improvement
✅ Multi-Agent Orchestration
✅ Echte Self-Loop Autonomie

---

**Status:** 🟢 READY FOR AUTONOMOUS OPERATIONS

Das System ist bereit für echte Autonomie!
