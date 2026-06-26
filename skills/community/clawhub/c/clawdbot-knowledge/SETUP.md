# Orchestrator Skill - Setup Guide

Komplette Anleitung zum Einrichten des Augment Orchestrator Skills für Multi-Agent Voice Development.

---

## Voraussetzungen

**Software:**
- ✅ SpeakMCP installiert und läuft
- ✅ Node.js 18+ installiert
- ✅ Git installiert
- ✅ Auggie CLI installiert: `npm install -g @augmentcode/cli`

**API Keys:**
- ✅ OpenAI oder Anthropic API Key (für SpeakMCP)
- ✅ Supabase URL + Key (für Skill-Registrierung)

---

## Setup in 3 Schritten

### Schritt 1: Skill registrieren

**1.1 Environment konfigurieren**

Erstelle/bearbeite `.claude/skills/deepallspeak/scripts/.env`:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ...your-key...
```

**1.2 Skill registrieren**

```powershell
cd .claude/skills/orchestrator/scripts
.\register-skill.ps1
```

**Output:**
```
🎯 Registering Orchestrator Skill
==================================
✓ Node.js installed
✓ Skill creation script found
✓ Dependencies installed
🚀 Creating Orchestrator Skill...
✅ Skill created successfully!
```

---

### Schritt 2: Slots einrichten

**2.1 Slots erstellen**

```powershell
cd .claude/skills/orchestrator/scripts
.\setup-slots.ps1
```

**Was passiert:**
- Erstellt 3 Git Worktrees unter `C:\AI_Slots\SpeakMCP\`
- Jeder Slot bekommt `run-auggie.ps1` Wrapper
- Dependencies werden installiert (npm/pnpm)

**Output:**
```
🚀 Augment Orchestrator - Multi-Agent Slot Setup
==================================================
✓ Git installiert
✓ Auggie CLI installiert
✓ Repository gefunden
📦 Erstelle 3 Slots...

Slot 1: C:\AI_Slots\SpeakMCP\slot-1
  → Erstelle Git Worktree...
  ✓ Worktree erstellt
  ✓ run-auggie.ps1 erstellt
  ✓ Dependencies installiert
✓ Slot 1 bereit!

[... Slot 2 und 3 analog ...]

🎉 Setup abgeschlossen!
```

**2.2 Slots verifizieren**

```powershell
# Status prüfen
1..3 | ForEach-Object {
    Write-Host "Slot $_: $(Test-Path "C:\AI_Slots\SpeakMCP\slot-$_")"
}

# Output:
# Slot 1: True
# Slot 2: True
# Slot 3: True
```

---

### Schritt 3: ACP-Agent konfigurieren

**3.1 In SpeakMCP:**
1. Öffne **Settings** (⚙️)
2. Navigiere zu **ACP Agents**
3. Klicke **Add Agent**

**3.2 Agent-Konfiguration:**
```
Name: Augment
Command: auggie --acp
(oder: augment --acp, je nach CLI-Version)
```

**3.3 Test Connection:**
- Klicke **Test Connection**
- Status sollte zeigen: ✅ **Reachable**

---

## Verwendung

### Voice Commands (Ctrl+Hold)

**Einfacher Bug Fix:**
```
"Fix the null pointer in auth.ts line 42"
```

**Parallele Issues:**
```
"Bearbeite Issues 23, 45 und 67 parallel"
```

**Sequential mit Dependencies:**
```
"Implementiere User Authentication, dann Tests, dann Deployment"
```

**Explizite Slot-Wahl:**
```
"Slot 2 soll Dashboard Widget für Umsatzstatistiken erstellen mit Chart.js"
```

---

## Verifizierung

### Test 1: Single Slot
```powershell
cd C:\AI_Slots\SpeakMCP\slot-1
.\run-auggie.ps1 "Get status and list available tools"
```

**Erwartetes Ergebnis:**
- Auggie startet
- Zeigt Status und Tools
- Exit code 0

### Test 2: Voice Command
**In SpeakMCP (Ctrl+Hold):**
```
"Slot 1, get status"
```

**Erwartetes Ergebnis:**
- Orchestrator analysiert Task
- Delegiert an Slot 1
- Auggie führt aus
- Ergebnis wird präsentiert

### Test 3: Parallele Ausführung
**Voice:**
```
"Fixe Bug in file A, file B und file C parallel"
```

**Erwartetes Ergebnis:**
- Orchestrator erkennt 3 unabhängige Tasks
- Verteilt auf Slot 1, 2, 3
- Alle 3 Auggie-Instanzen arbeiten gleichzeitig
- Ergebnisse werden konsolidiert

---

## Troubleshooting

### Problem: "Auggie not found"
**Lösung:**
```powershell
# Installation prüfen
auggie --version

# Neuinstallation
npm install -g @augmentcode/cli

# PATH prüfen
where auggie
```

### Problem: "ACP-Agent not reachable"
**Lösung:**
1. SpeakMCP → Settings → ACP Agents
2. Prüfe Command: `auggie --acp` oder `augment --acp`
3. Test Connection
4. Logs prüfen: `~/.speakmcp/logs/acp.log`

### Problem: "Skill not found"
**Lösung:**
```powershell
# Skill-Registrierung wiederholen
cd .claude/skills/orchestrator/scripts
.\register-skill.ps1

# In SpeakMCP:
"List skills"
# Sollte zeigen: augment-orchestrator
```

### Problem: "Slot conflicts"
**Lösung:**
```powershell
# Prüfe, ob Slots isoliert sind
ls C:\AI_Slots\SpeakMCP\

# Sollte zeigen:
# slot-1/
# slot-2/
# slot-3/

# Neu erstellen bei Problemen:
cd .claude/skills/orchestrator/scripts
.\setup-slots.ps1
```

### Problem: "Tests fail in Auggie"
**Lösung:**
```powershell
# Manuell Tests laufen lassen
cd C:\AI_Slots\SpeakMCP\slot-1
npm test

# Output prüfen, Fehler fixen
# Auggie erneut mit "fix tests" instruieren
```

---

## Erweiterte Konfiguration

### Custom Slot-Pfad
```powershell
.\setup-slots.ps1 -SlotBasePath "D:\MySlots"
```

### Ohne Worktrees (volle Klone)
```powershell
.\setup-slots.ps1 -UseWorktrees:$false
```

### Auggie mit Custom Model
In jedem Slot, edit `.augment/config.json`:
```json
{
  "model": "claude-3.5-sonnet",
  "temperature": 0.7
}
```

### MCP Server für Auggie
In jedem Slot, edit Augment settings:
```json
{
  "augment.advanced": {
    "mcpServers": [
      {
        "name": "filesystem",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\AI_Slots\\SpeakMCP\\slot-1"]
      },
      {
        "name": "github",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
      }
    ]
  }
}
```

---

## Nächste Schritte

1. ✅ **Skill registriert** → Kann in SpeakMCP aktiviert werden
2. ✅ **Slots eingerichtet** → 3 parallele Workspaces bereit
3. ✅ **ACP konfiguriert** → Auggie erreichbar
4. 🚀 **Loslegen:** Voice Commands ausprobieren!

### Empfohlene erste Tasks:
1. **Simple Bug Fix:** "Fix typo in README.md"
2. **Parallel Test:** "Fixe 3 kleine Bugs parallel"
3. **Full Workflow:** "Implementiere Feature X mit Tests und Docs"

---

## Performance & Best Practices

### Model-Mix für Effizienz
- **Transkription:** Groq (sub-second, günstig)
- **Task-Analyse:** GPT-4o-mini (schnell)
- **Code-Gen (Auggie):** Claude 3.5 Sonnet (beste Qualität)

### Voice-First Tipps
✅ **DO:**
- Klare, präzise Anweisungen sprechen
- Dateipfade und Libraries explizit nennen
- "Parallel" oder "Sequential" spezifizieren wenn nötig

❌ **DON'T:**
- Vage Formulierungen ("irgendwie besser")
- Zu schnell sprechen (Transkriptionsfehler)
- Zu viele Tasks in einer Anfrage (max. 3-5)

### Definition of Done (DoD)
Jeder Task ist DONE wenn:
1. ✓ Code geändert (Diff sichtbar)
2. ✓ Tests/Build erfolgreich
3. ✓ Dokumentiert
4. ✓ Keine Secrets geleakt
5. ✓ Rollback-Pfad bekannt

---

## Support & Dokumentation

**Dokumentation:**
- `.claude/skills/orchestrator/skill.md` - Vollständige Referenz
- `.claude/skills/orchestrator/README.md` - Quick Start
- `.claude/skills/orchestrator/references/claudw.md` - Framework

**Links:**
- Auggie CLI: https://docs.augmentcode.com/cli
- SpeakMCP: https://github.com/aj47/SpeakMCP
- ACP Protocol: https://github.com/agentclientprotocol/agent-client-protocol

---

**Version:** 2.0.0
**Last Updated:** Januar 2026

**Ready for voice-controlled multi-agent development with 3x speedup!** 🎤🤖
