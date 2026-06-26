---
name: augment-orchestrator
description: Augment Architect - Multi-Agent Orchestrierung mit SpeakMCP × Auggie × ACP für parallele Softwareentwicklung
version: 2.0.0
author: SpeakMCP Community
category: orchestration
tags:
  - augment
  - auggie
  - acp
  - multi-agent
  - slots
  - voice-first
  - speakmcp
dependencies:
  - augment-cli
  - speakmcp
  - acp-protocol
related_skills:
  - speak-mcp
  - augment-code
capabilities:
  - Multi-Agent Slot Management (3 Slots)
  - Parallele Task-Ausführung via Auggie
  - Voice-First Development
  - ACP-basierte Agent-Delegation
  - Definition of Done Enforcement
  - Git Worktree Isolation
---

# Augment Orchestrator - Multi-Agent Slot System

Intelligente Orchestrierung von 3 parallelen Auggie-Agenten für voice-gesteuerte Softwareentwicklung mit SpeakMCP.

## Systemübersicht

**Architektur:** SpeakMCP (Orchestrator) × Auggie CLI (Coding Agent) × ACP (Bridge)

```
┌─────────────────────────────────────────────────┐
│           SpeakMCP (Voice-First UI)             │
│  - Spracheingabe (Groq/Whisper)                 │
│  - Task-Analyse & Dekomposition                 │
│  - ACP-Delegation                                │
└──────────────┬──────────────────────────────────┘
               │ ACP Protocol
      ┌────────┼────────┬────────────┐
      │        │        │            │
   Slot 1   Slot 2   Slot 3     (isolierte Workspaces)
      │        │        │
   Auggie   Auggie   Auggie   (Augment CLI Worker)
      │        │        │
   ┌──┴────┬──┴────┬──┴────┐
   Git     Git     Git      (Worktrees/Klone)
   Repo 1  Repo 2  Repo 3
```

## Slot-Infrastruktur

**3 isolierte Arbeits-Slots** für parallele Code-Arbeit:

| Slot | Pfad | Wrapper | Isolation |
|------|------|---------|-----------|
| Slot 1 | `C:\AI_Slots\SpeakMCP\slot-1` | `run-auggie.ps1` | Eigenes node_modules + Git |
| Slot 2 | `C:\AI_Slots\SpeakMCP\slot-2` | `run-auggie.ps1` | Eigenes node_modules + Git |
| Slot 3 | `C:\AI_Slots\SpeakMCP\slot-3` | `run-auggie.ps1` | Eigenes node_modules + Git |

**Wrapper-Aufruf:**
```powershell
cd C:\AI_Slots\SpeakMCP\slot-1
.\run-auggie.ps1 "Implementiere Feature X"  # --print Mode (non-interactive)
```

## Augment Architect System Prompt (Core Logic)

**Rolle:** Zentrale Orchestrierungsinstanz für Multi-Agent System

### Fixe Rollen
- **SpeakMCP**: Anforderungen aufnehmen, Kontext lesen, Plan erstellen, delegieren (ACP)
- **ACP**: Standardisierte Dispatch-Schicht (Agent-Registrierung, Routing, Status)
- **Auggie**: Code implementieren (VS Code/CLI), Checks ausführen, PR-fähige Diffs erzeugen

### Nicht verhandelbare Regeln
1. **Nicht raten**: Keine erfundenen Commands/Flags → Nur aus Docs/CLI-Help
2. **Minimaler Diff**: Änderungen klein, reversibel, testbar
3. **Backup-first**: Vor Edit ein Backup (Git-Stash/Branch)
4. **Atomic Changes**: Pro Task logisch abgeschlossen, keine Nebenbei-Refactors
5. **Secrets**: Niemals committen; `.env` + `.gitignore`; Logs redacted

### Standard-Arbeitsablauf (IMMER)

**Phase 1 — Verifikation (keine Codeänderungen)**
- ✓ SpeakMCP läuft? Modell/Key korrekt?
- ✓ ACP-Agent registriert und "reachable"?
- ✓ Auggie CLI/Extension verfügbar? (Version/Health)

**Phase 2 — Plan**
- Erstelle Plan mit 6–12 Steps (abhängigkeitsbewusst)
- Markiere pro Step: *Owner*, *Input*, *Output*, *Check*

**Phase 3 — Ausführung**
- Delegiere Code-Aufgaben an **Auggie** (per Slot)
- Auggie führt nach jeder Änderung Check aus (lint/test/build)

**Phase 4 — Abschlussbericht**
- Was geändert (Dateien + Begründung)
- Wie verifiziert (Commands + Ergebnis)
- Wie rollbackt man (Git revert/checkout/Backup)
- Offene Risiken/ToDos (max. 5 Punkte)

### Routing-Regeln (Task → Agent)
- **Code schreiben/refactoren/tests** → Auggie
- **Agent-Wiring/ACP-Konfig/Runbooks** → SpeakMCP/ACP (mit Auggie nur wenn Code betroffen)
- **Debugging** → Repro + Logs sammeln, dann isoliert fixen

### Quality Gate (Definition of Done)
Ein Task ist **DONE**, wenn:
1. ✓ Anforderungen umgesetzt (nachweisbar im Diff)
2. ✓ Mindestens ein Smoke-Check erfolgreich (`test` / `build` / `lint`)
3. ✓ Änderungen dokumentiert (kurz, klar)
4. ✓ Keine Secrets geleakt
5. ✓ Rollback-Pfad benannt

## Orchestrierungs-Workflows

### Workflow 1: Einfacher Task (Single Slot)

```
User (Voice): "Fix the null pointer in auth.ts line 42"

Orchestrator:
  ↓ Analysiert: Bug Fix, Komplexität LOW, 1 Datei
  ↓ Wählt: Slot 1
  ↓ Delegiert:
    cd C:\AI_Slots\SpeakMCP\slot-1
    .\run-auggie.ps1 "Fix null pointer in auth.ts:42. Add null check before property access. Run tests after fix."

Auggie (Slot 1):
  1. Liest auth.ts Zeile 42
  2. Generiert Patch (null check)
  3. Führt Tests aus
  4. Erstellt Commit

Result: Patch in ~2 min, Tests passed ✓
```

### Workflow 2: Parallele Tasks (Multi-Slot)

```
User (Voice): "Bearbeite Issues #23, #45 und #67 parallel"

Orchestrator:
  ↓ Analysiert: 3 unabhängige Issues
  ↓ Prüft Abhängigkeiten: Keine
  ↓ Verteilt auf 3 Slots:

  PARALLEL:
    Slot 1: Issue #23 (UI Bug in Dashboard)
    Slot 2: Issue #45 (API Rate Limiting)
    Slot 3: Issue #67 (Test Coverage für User Service)

  Execution:
    cd C:\AI_Slots\SpeakMCP\slot-1
    .\run-auggie.ps1 "Fix Issue #23: Dashboard layout bug on mobile. File: src/components/Dashboard.tsx"

    cd C:\AI_Slots\SpeakMCP\slot-2
    .\run-auggie.ps1 "Implement Issue #45: Add rate limiting middleware to API. File: src/middleware/rateLimit.ts"

    cd C:\AI_Slots\SpeakMCP\slot-3
    .\run-auggie.ps1 "Write tests for Issue #67: User service test coverage. File: tests/services/user.test.ts"

  → Alle 3 Auggie-Instanzen arbeiten gleichzeitig
  → Slot-Isolation verhindert Dateikonflikte

Aggregation:
  ↓ Wartet auf alle 3 Slots
  ↓ Konsolidiert Ergebnisse
  ↓ Erstellt 3 separate PRs (via GitHub MCP)

Result: 3 Issues gelöst in ~8 min (statt 24 min sequentiell)
```

### Workflow 3: Sequential mit Dependency

```
User (Voice): "Implementiere User Authentication mit Tests und Deployment"

Orchestrator:
  ↓ Analysiert: Komplexität HIGH, Abhängigkeiten: JA
  ↓ Plan erstellt:

  Phase 1: Auth Implementation (Slot 1)
    .\run-auggie.ps1 "Implement JWT authentication in src/auth. Include login, register, token refresh."

  Phase 2: Wait for Phase 1 ✓

  Phase 3: Tests (Slot 2 parallel mit Documentation)
    Slot 2: .\run-auggie.ps1 "Write integration tests for auth endpoints in tests/auth"
    Slot 3: .\run-auggie.ps1 "Update API documentation for new auth endpoints in docs/api"

  Phase 4: Wait for Phase 3 ✓

  Phase 5: Deployment Prep (Slot 1)
    .\run-auggie.ps1 "Create migration script for auth tables. Update docker-compose with env vars."

Result: Vollständiges Auth-System in ~20 min
```

### Workflow 4: Voice-First Development

**Diktat → Orchestrierung → Delegation → Review**

```
User (spricht via Ctrl+Hold):
  "Ich brauche ein neues Dashboard-Widget für Umsatzstatistiken.
   Es soll die letzten 30 Tage zeigen, als Liniendiagramm,
   mit Filter für verschiedene Produkte.
   Verwende Chart.js und TypeScript.
   Slot 2 kann das machen."

SpeakMCP:
  ↓ Transkription (Groq - sub-second)
  ↓ Post-Processing (Grammatik fix, Strukturierung)
  ↓ Analyse:
      - Feature: Dashboard Widget
      - Technologien: Chart.js, TypeScript
      - Slot: 2 (explizit gewählt)
  ↓ Delegiert an Slot 2:

cd C:\AI_Slots\SpeakMCP\slot-2
.\run-auggie.ps1 @"
Create a new dashboard widget for revenue statistics.
Requirements:
- Display last 30 days of data
- Line chart using Chart.js
- Filter dropdown for different products
- TypeScript with proper types
- File location: src/components/widgets/RevenueChart.tsx
- Include unit tests
- Run build after implementation
"@

Auggie (Slot 2):
  1. Erstellt RevenueChart.tsx
  2. Implementiert Chart.js Integration
  3. Fügt TypeScript Types hinzu
  4. Erstellt Tests
  5. Führt `npm run build` aus

User (spricht nach 5 min):
  "Status von Slot 2?"

SpeakMCP:
  "Slot 2: RevenueChart implementiert. Build erfolgreich. 87% Test Coverage. Bereit für Review."

User (spricht):
  "Erstelle PR für Slot 2"

SpeakMCP → GitHub MCP:
  Creates PR with title: "feat: Add revenue statistics dashboard widget"
```

## Task-Analyse Framework

### Intent Recognition
```python
def analyze_task(voice_input: str) -> TaskAnalysis:
    """Analysiert gesprochene Anforderung"""

    # Intent erkennen
    if "fix" or "bug" in voice_input:
        intent = "BUG_FIX"
    elif "implement" or "add" or "create" in voice_input:
        intent = "FEATURE"
    elif "test" in voice_input:
        intent = "TESTING"
    elif "refactor" in voice_input:
        intent = "REFACTOR"

    # Komplexität schätzen
    complexity = estimate_complexity(voice_input)

    # Slot-Anforderung prüfen
    if "parallel" or mentions_multiple_issues(voice_input):
        slots_needed = count_independent_tasks(voice_input)
    else:
        slots_needed = 1

    # Abhängigkeiten identifizieren
    dependencies = detect_dependencies(voice_input)

    return TaskAnalysis(
        intent=intent,
        complexity=complexity,
        slots_needed=slots_needed,
        dependencies=dependencies,
        estimated_time=calculate_time(complexity, slots_needed)
    )
```

### Slot-Auswahl Logik
```
IF task.independent AND other_tasks.exist:
    → Nutze freien Slot (1, 2 oder 3)

ELIF task.has_dependencies:
    → Sequential auf Slot 1 (oder explicit gewähltem Slot)

ELIF user.specified_slot:
    → Nutze explizit genannten Slot

ELSE:
    → Default: Slot 1
```

## MCP Integration

**Verfügbare MCP Server für Auggie-Delegation:**

### Filesystem Server
```powershell
# Auggie kann auf Dateien zugreifen
MCP: filesystem → C:\AI_Slots\SpeakMCP\slot-X
```

### GitHub Server
```powershell
# Auggie kann PRs erstellen, Issues lesen
MCP: github → Create PR after code changes
```

### Context7 Server
```powershell
# Auggie erhält aktuelle Docs/APIs
MCP: context7 → Latest Chart.js documentation
```

**Konfiguration in Auggie:**
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

## Voice Commands

### Slot-Management
```
"Starte Slot 1 mit [task]"
"Welche Slots sind aktiv?"
"Status von Slot 2"
"Stoppe Slot 3"
"Zeige Ergebnisse aller Slots"
```

### Parallele Ausführung
```
"Bearbeite Issues 1, 2 und 3 parallel"
"Fixe alle Bugs in [component] mit 3 Slots"
"Implementiere [feature A], [feature B] und [feature C] gleichzeitig"
```

### Sequential mit Dependencies
```
"Implementiere [A], dann teste [A], dann deploye [A]"
"Erst [B], warte auf Completion, dann [C]"
```

### Explicit Slot Selection
```
"Slot 1 soll [task A] machen"
"Verwende Slot 2 für [task B]"
"[task C] auf Slot 3"
```

### Review & Merge
```
"Zeige Diffs von allen Slots"
"Erstelle PRs für alle abgeschlossenen Slots"
"Merge PR von Slot 1"
```

## Troubleshooting

### Problem: Auggie nicht erreichbar
**Symptom:** `run-auggie.ps1` findet Auggie CLI nicht

**Lösung:**
```powershell
# Prüfe Installation
auggie --version  # oder augment --version

# Prüfe PATH
where auggie  # oder where augment

# Neuinstallation
npm install -g @augmentcode/cli
```

### Problem: Slot-Konflikte
**Symptom:** "File already locked" oder Git-Merge-Conflicts

**Lösung:**
- Slots sind isoliert → sollte nicht passieren
- Prüfe: Sind wirklich separate Verzeichnisse?
  ```powershell
  ls C:\AI_Slots\SpeakMCP\
  # Sollte zeigen: slot-1, slot-2, slot-3
  ```

### Problem: ACP-Agent nicht registriert
**Symptom:** SpeakMCP findet Auggie nicht

**Lösung:**
1. SpeakMCP → Settings → ACP Agents
2. Add Agent: "Augment"
3. Command: `auggie --acp` (oder gemäß Auggie-Doku)
4. Test Connection

### Problem: Tests schlagen fehl
**Symptom:** Auggie meldet "Tests failed"

**Lösung:**
- Review Auggie Output
- Manuell Tests laufen lassen:
  ```powershell
  cd C:\AI_Slots\SpeakMCP\slot-1
  npm test
  ```
- Auggie erneut mit "fix tests" instruieren

## Best Practices

### 1. Slot-Isolation
✅ **DO:** Immer separate Verzeichnisse für Slots
✅ **DO:** Git Worktrees verwenden (shared .git, separate checkouts)
❌ **DON'T:** Denselben Ordner für mehrere Slots nutzen

### 2. Task-Dekomposition
✅ **DO:** Große Tasks in 3-5 unabhängige Subtasks zerlegen
✅ **DO:** Abhängigkeiten explizit dokumentieren
❌ **DON'T:** Zu granular (Overhead) oder zu grob (Parallelisierung unmöglich)

### 3. Voice-First Ergonomie
✅ **DO:** Klare, präzise Anweisungen sprechen
✅ **DO:** Technische Details explizit nennen (Dateipfade, Libraries)
❌ **DON'T:** Vage Formulierungen wie "irgendwie besser machen"

### 4. Quality Gates
✅ **DO:** Nach jedem Slot-Task DoD prüfen
✅ **DO:** Minimale Smoke-Tests (build/lint/test) laufen lassen
❌ **DON'T:** Ohne Verifikation mergen

### 5. Backup-First
✅ **DO:** Vor größeren Changes Git-Branch/Stash erstellen
✅ **DO:** Rollback-Pfad dokumentieren
❌ **DON'T:** Blind auf main/master commiten

## Performance & Kosten

**Model-Mix für Effizienz:**
- **Transkription:** Groq (sub-second, günstig)
- **Task-Analyse:** GPT-4o-mini (schnell, günstig)
- **Code-Generation (Auggie):** Claude 3.5 Sonnet (beste Qualität)

**Parallele Slots:**
- **1 Slot:** ~10-15 min pro Task
- **3 Slots:** ~10-15 min für 3 Tasks (3x Speedup)

**Kosten-Beispiel:**
```
Single Task (1 Slot):
  - Transkription: ~$0.001 (Groq)
  - Analyse: ~$0.01 (GPT-4o-mini)
  - Code: ~$0.15 (Claude Sonnet)
  Total: ~$0.16

3 Parallel Tasks (3 Slots):
  - Transkription: ~$0.003
  - Analyse: ~$0.03
  - Code: ~$0.45 (3x Claude)
  Total: ~$0.48
  Time: Same as 1 Task (~10 min)
```

## Resources

- **Auggie CLI Docs:** https://docs.augmentcode.com/cli
- **ACP Protocol:** https://github.com/agentclientprotocol/agent-client-protocol
- **SpeakMCP:** https://github.com/aj47/SpeakMCP
- **MCP Protocol:** https://modelcontextprotocol.io

## Version

**Version:** 2.0.0
**Last Updated:** Januar 2026
**Based On:** SpeakMCP v1 + Augment Code + ACP
**License:** AGPL-3.0

---

**Voice-gesteuerte Multi-Agent Softwareentwicklung mit 3x Speedup!**

Speak: "Bearbeite Issues 1, 2 und 3 parallel mit allen Slots"
