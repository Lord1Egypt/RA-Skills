---
name: geelark-complete
version: 1.0.0
description: "All-in-one Skill fuer GeeLark: Setup, lokale API, nativer Sync-Transport, UI/RPA-Fallback, Posting-Flow, Verifikation und Troubleshooting in einem durchgaengigen Runbook."
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# GeeLark Complete

Dieser Skill ist der zentrale End-to-End Skill fuer GeeLark und deckt alle aktuell praktikablen Faehigkeiten im Workspace ab.

## Scope

- GeeLark Setup und Betriebsbereitschaft
- Lokale Agent-API auf `GEELARK_API_BASE`
- Nativer Desktop-Sync ueber `mssvr` (signierte Requests)
- UI-Automation als Fallback bei API-Limits
- Browser-/Profil-Start und URL-Navigation
- Asset-Transfer und Posting-Vorbereitung
- Strikte Verifikation und reproduzierbares Troubleshooting

## Voraussetzungen

- App: `/Applications/GeeLark.app`
- Env in `openclaw-config/.env`:
  - `GEELARK_API_BASE=http://localhost:40185`
  - `GEELARK_API_KEY=<bearer token>`
- Hilfsskripte:
  - `scripts/geelark/local_client.py`
  - `scripts/geelark/sync_client.mjs`
- Fuer Sync: GeeLark nativer `mssvr` muss aufloesbar/startbar sein

## Faehigkeiten (Capability Matrix)

1. Setup
- Team/Workspace-Basis pruefen
- Proxy/Phone/App-Basis dokumentieren
- `phone_id` Mapping aus Dashboard/Baserow festhalten

2. API Ops
- Agent-Liveness und Port-Info pruefen
- Endpunkt-Footprint (`probe`, `request`)
- Lesende Ersttests vor schreibenden Calls
- Upload-/Task-Routen vorbereiten, sofern Methode/Payload belegt

3. Native Sync Ops
- Signierte Requests mit `app-id` + `app-auth`
- Session-Lifecycle: `start -> config -> input/input_list -> stop`
- Preconditions pruefen (`sid`, Handle-Anzahl, Handle-Matching)

4. UI/RPA Ops
- App starten/fokussieren
- Sichtbare Profile/Browser oeffnen
- Klare, belegbare Klickpfade ausfuehren
- Bei Captcha/MFA bis zum belegbaren Blocker gehen und stoppen

5. Posting Ops
- Asset-Transfer bis GeeLark-Endstation
- Plattformspezifische Posting-Sequenz vorbereiten
- Timing/Line-Disziplin aus dem Workflow einhalten

6. Verification Ops
- Nach Aktionen immer dual pruefen:
  - Zustand A: richtige Vordergrund-App/Fenster
  - Zustand B: inhaltliche Zielpruefung (z. B. URL, Session-ID, API-Response)
- Ohne Gegencheck gilt eine Aktion als nicht abgeschlossen

7. Recovery/Triage
- API 404: Methode/Payload pruefen statt Endpunkt sofort verwerfen
- Sync-Fehler: erst `mssvr`-Port und Signaturpfad checken
- UI-Fehler: Fokusproblem von Logikproblem trennen
- Jede reproduzierbare Erkenntnis in Memory/Skill-Doku hinterlegen

## Standard-Runbook

1. Klasse bestimmen: Setup, API, Sync, UI, Posting.
2. API-first starten (harmloser Call zuerst).
3. Wenn Sync gebraucht wird: nur `sync_client.mjs` oder `local_client.py sync-*` nutzen.
4. Bei API-Blocker auf UI-Fallback wechseln.
5. Nach jedem Schritt verifizieren.
6. Nur bei validiertem Zustand weiter zum naechsten Schritt.

## Kommandos (sicherer Einstieg)

```bash
python3 scripts/geelark/local_client.py info
python3 scripts/geelark/local_client.py health
python3 scripts/geelark/local_client.py probe --endpoint /v1/browser/core/list --methods GET OPTIONS POST --json-body '{}'
python3 scripts/geelark/local_client.py sync-info
node scripts/geelark/sync_client.mjs info
```

## Kommandos (Sync-Lifecycle)

```bash
node scripts/geelark/sync_client.mjs start --main-hwnd 101 --hwnd 101 --hwnd 202
node scripts/geelark/sync_client.mjs config --sid abc --json-body '{"delay_range_before_click":[300,900]}'
node scripts/geelark/sync_client.mjs same-input --sid abc --text 'hello world' --input-interval 0,0
node scripts/geelark/sync_client.mjs stop --sid abc
```

## Kommandos (UI-Fallback)

```bash
open -a "GeeLark"
osascript -e 'tell application "GeeLark" to activate'
```

## Claw/OpenClaw Integration

- Lokale Nutzung: Skill liegt unter `skills/geelark-complete/` und ist damit im Workspace verfuegbar.
- Mit ClawHub CLI publizieren:

```bash
clawdhub publish ./skills/geelark-complete \
  --slug geelark-complete \
  --name "GeeLark Complete" \
  --version 1.0.0 \
  --changelog "Initial all-in-one GeeLark skill"
```

## Beziehungen zu vorhandenen Skills

- Nutzt und konsolidiert:
  - `geelark-ops`
  - `geelark-setup`
  - `geelark-api-ops`
  - `geelark-rpa-ops`
  - `geelark-posting-ops`
  - `geelark-sync-operational`
- Dieser Skill ist der zentrale Einstieg, die anderen bleiben als Deep-Dive erhalten.

## Grenzen

- Keine destruktiven Calls ohne belegte Route, Methode, Payload
- Keine externen Postings ohne explizite User-Absicht
- Keine erfundenen Endpunkte oder ungepruefte Automationsversprechen

## Zielbild

Ein einziger GeeLark Skill, der operative End-to-End Aufgaben von Diagnose bis Ausfuehrung mit Pflicht-Verifikation abdeckt und zugleich in ClawHub versionierbar ist.
