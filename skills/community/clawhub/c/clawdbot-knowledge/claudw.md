# Claudw.md: Universal AI-Orchestration Framework (SpeakMCP × Augment × ACP) — v2

## 1) Systemübersicht
Dieses Projekt nutzt ein hybrides Multi-Agenten-System, um Softwareentwicklung planbar, delegierbar und testbar zu automatisieren.

- **Orchestrator / UI:** SpeakMCP — https://github.com/aj47/SpeakMCP
- **Coding Agent (IDE/CLI):** Augment Code — https://www.augmentcode.com/
- **Bridge / Dispatch:** ACP (Agent Client Protocol) — https://github.com/agentclientprotocol/agent-client-protocol

**Zielzustand:** SpeakMCP kann Tasks via ACP an Augment delegieren; Augment implementiert im Repo; Tests/Build laufen; Ergebnis ist dokumentiert, auditierbar, rollbackfähig.

---

## 2) Setup & Installation

### Voraussetzungen
- **Node.js v18+** (SpeakMCP)
- **API Keys (nur lokal in `.env`):**
  - `OPENAI_API_KEY` oder `ANTHROPIC_API_KEY` (je nach Modellwahl in SpeakMCP)
- **Augment:** VS Code Extension installiert + CLI verfügbar
- **Git** installiert

### Schritte (Minimal)
1. `git clone https://github.com/aj47/SpeakMCP.git`
2. `cd SpeakMCP && npm install`
3. `npm run dev` (oder laut SpeakMCP-README)
4. In SpeakMCP: **Settings → ACP Agents**
   - Agent hinzufügen: **Augment**
   - **Command/Start-Befehl:** abhängig von Augment-CLI-Version
     → Verwende `augment --help` / `augment-cli --help` und setze den ACP-Startbefehl gemäß offizieller Doku.

> Hinweis: Keine ACP-/Augment-Flags raten. Wenn unklar: Doku/README/CLI-Help als Quelle verwenden.

---

## 3) Core Instruction: Augment Architect System Prompt (v3)

> **WICHTIG:** Den folgenden Block als **System Prompt / Custom Instruction** im Orchestrator-Modell verwenden.

--- START SYSTEM PROMPT ---

Du bist **Augment Architect**: die zentrale Orchestrierungsinstanz eines Multi-Agent Systems aus **SpeakMCP (Orchestrator)**, **ACP (Bridge)** und **Augment (Coding Agent)**.

### A) Fixe Rollen
- **SpeakMCP**: Nimmt Anforderungen entgegen, liest Kontext (Projektdateien), erstellt Plan, delegiert Tasks über ACP.
- **ACP**: Standardisierte Dispatch-Schicht (Agent-Registrierung, Routing, Request/Response, Status).
- **Augment**: Implementiert Code im Repo (VS Code/CLI), führt Checks aus, erzeugt PR/Commit-fähige Diffs.

### B) Nicht verhandelbare Regeln
1. **Nicht raten**: Keine erfundenen Commands, Flags, Endpoints, Config-Felder.
   Wenn etwas unklar ist: **README/Docs/CLI-Help** lokalisieren und daraus ableiten.
2. **Minimaler Diff**: Änderungen klein, reversibel, testbar.
3. **Backup-first** (bei Datei-Edits): vor Edit ein Backup erstellen (oder Git-Stash/Branch).
4. **Atomic Changes**: pro Task logisch abgeschlossene Einheit; keine "Nebenbei"-Refactors.
5. **Secrets**: niemals in Repo committen; `.env` + `.gitignore`; Logs redacted.

### C) Standard-Arbeitsablauf (immer)
**Phase 1 — Verifikation (keine Codeänderungen)**
- Prüfe: Startet SpeakMCP? Ist ein Modell/Key korrekt konfiguriert?
- Prüfe: ACP-Agent ist registriert und "reachable"?
- Prüfe: Augment CLI/Extension verfügbar? (Version/Health/Help)

**Phase 2 — Plan**
- Erzeuge einen Plan mit 6–12 Steps (abhängigkeitsbewusst).
- Markiere pro Step: *Owner* (SpeakMCP/ACP/Augment), *Input*, *Output*, *Check*.

**Phase 3 — Ausführung**
- Delegiere Codeaufgaben an **Augment**.
- Lasse Augment nach jeder Änderung mindestens einen Check ausführen (lint/test/build, je nach Repo).

**Phase 4 — Abschlussbericht**
- Liefere:
  - Was geändert wurde (Dateien + Kurzbegründung)
  - Wie verifiziert wurde (Commands + Ergebnis)
  - Wie man rollbackt (Git revert/checkout/Backup)
  - Offene Risiken/ToDos (max. 5 Punkte)

### D) Routing-Regeln (Task → Agent)
- **Code schreiben/refactoren/tests** → Augment
- **Agent-Wiring/ACP-Konfig/Runbooks** → SpeakMCP/ACP-nahe Schritte (mit Augment nur wenn Code betroffen)
- **Debugging** → zuerst Repro + Logs sammeln, dann isoliert fixen

### E) Quality Gate (Definition of Done je Task)
Ein Task ist DONE, wenn:
1. Anforderungen umgesetzt (nachweisbar im Diff)
2. Mindestens ein Smoke-Check erfolgreich (z. B. `test` oder `build` oder `lint`)
3. Änderungen dokumentiert (kurz, klar)
4. Keine Secrets geleakt
5. Rollback-Pfad benannt

### F) First-Response-Protokoll (deine erste Antwort auf einen neuen Task)
1. **Prereq-Checkliste**
2. **Plan (6–12 Steps)**
3. **Konkrete Commands/Actions pro Step** (nur aus Docs/CLI-Help abgeleitet)
4. **Minimaler E2E-Test** (wie man Delegation + Codechange + Check verifiziert)
5. **Pass/Fail Kriterien**

--- ENDE SYSTEM PROMPT ---

---

## 4) Troubleshooting & Flow (Kurzmatrix)

### Symptom: SpeakMCP findet Augment nicht
- **Ursache:** CLI nicht im PATH / falscher Startbefehl / Agent nicht registriert
- **Fix:**
  - `augment --version` oder `augment-cli --version`
  - `which augment` / `where augment`
  - In SpeakMCP ACP-Agent Command exakt nach Augment-Doku setzen
- **Verify:** Agent-Status in SpeakMCP zeigt "reachable/connected" + Test-Dispatch möglich

### Symptom: Modell-Fehler / Auth-Fehler
- **Ursache:** Key fehlt/ungültig; falsches Modell gewählt
- **Fix:** `.env` prüfen (`OPENAI_API_KEY`/`ANTHROPIC_API_KEY`), Modellkonfig in SpeakMCP prüfen
- **Verify:** einfache Testanfrage in SpeakMCP läuft ohne Auth-Error

### Symptom: Delegation klappt, aber Code ändert sich nicht
- **Ursache:** Augment hat keinen Repo-Kontext / falsches Working Directory / fehlende Rechte
- **Fix:** Augment in korrektem Projektordner starten; Repo in VS Code geöffnet; Zugriff prüfen
- **Verify:** Augment erzeugt einen sichtbaren Diff (Dateiänderung) + kann einen Check ausführen

---

## 5) Definition of Done (DoD) — Projekt-Ebene
Ein Task gilt als abgeschlossen, wenn:
1. SpeakMCP erfolgreich delegiert (ACP Request/Response nachvollziehbar)
2. Augment hat den Code geändert (Diff sichtbar)
3. Mindestens ein `test` oder `build` oder `lint` war erfolgreich
4. Änderung ist dokumentiert (kurz) + rollbackfähig

---

## 6) Multi-Agent Slot System

Das System hat **3 isolierte Arbeits-Slots** für parallele Agenten-Arbeit:

| Slot | Pfad | Wrapper |
|------|------|---------|
| Slot 1 | `C:\AI_Slots\SpeakMCP\slot-1` | `run-auggie.ps1` |
| Slot 2 | `C:\AI_Slots\SpeakMCP\slot-2` | `run-auggie.ps1` |
| Slot 3 | `C:\AI_Slots\SpeakMCP\slot-3` | `run-auggie.ps1` |

### Orchestrierung

**Aufgaben-Delegation:**

Wenn du mehrere parallele Aufgaben hast:
1. **Analysiere** die Aufgaben auf Unabhängigkeit
2. **Verteile** unabhängige Aufgaben auf verschiedene Slots
3. **Delegiere** an Auggie in jedem Slot via:

```powershell
# Slot 1
cd C:\AI_Slots\SpeakMCP\slot-1
.\run-auggie.ps1 "Implementiere Feature X"

# Slot 2
cd C:\AI_Slots\SpeakMCP\slot-2
.\run-auggie.ps1 "Fixe Bug Y"

# Slot 3
cd C:\AI_Slots\SpeakMCP\slot-3
.\run-auggie.ps1 "Schreibe Tests für Z"
```

### Auggie CLI Modi
- **`--print`** (Default): Automatisierungsmodus für Orchestrator
- **`-Interactive`**: Interaktiver Modus mit Echtzeit-Feedback

### Slot-Isolation
Jeder Slot ist ein vollständiger SpeakMCP-Klon mit:
- Eigenem `node_modules` (via `pnpm install`)
- Isoliertem Dateisystem
- Unabhängigem Git-Status

**WICHTIG:** Keine Dateikonflikte zwischen Slots möglich!

### Workflow-Beispiel
```
User: "Bearbeite Issues #1, #2 und #3 parallel"

Orchestrator:
1. Issue #1 → Slot 1: .\run-auggie.ps1 "Fix Issue #1: ..."
2. Issue #2 → Slot 2: .\run-auggie.ps1 "Fix Issue #2: ..."
3. Issue #3 → Slot 3: .\run-auggie.ps1 "Fix Issue #3: ..."

→ Alle 3 Agenten arbeiten gleichzeitig
→ Ergebnisse werden konsolidiert
→ PRs werden erstellt
```

### Status-Check
```powershell
# Alle Slots prüfen
1..3 | ForEach-Object {
    $path = "C:\AI_Slots\SpeakMCP\slot-$_"
    Write-Host "Slot $_: $(Test-Path $path)"
}
```

---

## 7) Evolutionary Workflow

**Diktat → Orchestrierung → Delegation → Review**

### Schritt 1: Diktat und Ideenfindung
- Voice-Input via SpeakMCP (Ctrl+Hold)
- Transkription mit Groq (sub-second)
- Post-Processing für Strukturierung

### Schritt 2: Orchestrierung und Analyse
- SpeakMCP analysiert Anforderung
- Nutzt MCP-Server (GitHub, Filesystem, etc.)
- Identifiziert Tasks für Delegation

### Schritt 3: Delegation an parallele Slots
- Tasks werden auf 3 Slots verteilt
- Jeder Slot erhält spezifische Aufgabe + Pfad
- Agenten arbeiten gleichzeitig

### Schritt 4: Review und Konsolidierung
- Agenten erstellen PRs (via GitHub MCP)
- Entwickler prüft Änderungen
- Integration in main branch

---

## 8) Remote-Steuerung & Sicherheit

### Cloudflare Tunnel
- Verschlüsselte Remote-Verbindung
- Zero Trust Richtlinien
- QR-Code für Smartphone-Kopplung
- Keine Ports am Router öffnen nötig

### Sicherheitsrisiken und Sandboxing
- Isolierte Workspaces pro Slot
- Eingeschränkte Berechtigungen (Principle of Least Privilege)
- Menschliche Aufsicht für kritische Aktionen
- Keine Secrets in Repo commiten

---

## 9) Wirtschaftlichkeit & Kostenoptimierung

### Modell-Mix
| Aufgabe | Modell | Grund |
|---------|--------|-------|
| Transkription | Groq (Llama-3-70b) | Unschlagbare Geschwindigkeit, geringe Kosten |
| Architekturplanung | Claude 3.5 Sonnet | Beste Reasoning-Fähigkeiten |
| Einfache Fixes | GPT-4o-mini | Kosteneffizient, zuverlässig |
| Lokale Tests | Llama 3 (Ollama) | Keine API-Kosten, maximale Privatsphäre |

### Effizientes Ressourcenmanagement
- `uv` für Python-Umgebungen
- `pnpm` für Node.js-Projekte
- Git Worktrees (shared .git, separate checkouts)

---

**Version:** 2.0.0
**Last Updated:** Januar 2026
**Based On:** SpeakMCP v1 + Augment Code + ACP
