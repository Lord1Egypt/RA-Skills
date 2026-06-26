# Autonomous Cascade - Plan→Act→Evaluate Loop

Inspiriert von MCP-God-Mode/autonomous_cascade.ts, angepasst für OpenClaw.

## Wann nutzen

Wenn eine Aufgabe mehrere Schritte braucht und kein User-Ping nötig ist.
Beispiel: "Optimiere Bot-Params bis WR > 55%", "Diagnostiziere Gateway-Problem", "Update Workspace nach OC-Reset"

## Loop-Struktur

```
PLAN:
  goal: <Ziel in einem Satz>
  max_rounds: <3-10>
  budget_seconds: <60-600>
  risk: read_only | write_fs | networked
  stop_when: <klare Bedingung>

ROUND N:
  THINK: Was ist der aktuelle Stand?
  ACT: <Tool-Call>
  EVALUATE: Bin ich naehergekommen? Neue Erkenntnisse?
  CONTINUE oder HALT:SOFT (done) oder HALT:HARD (budget/blocked)
```

## Stop-Signale

- `HALT:SOFT` - Ziel erreicht, sauber abschliessen
- `HALT:HARD` - Budget, Fehler oder User needed - sofort stoppen
- `HALT:BLOCKED` - Weiterarbeit benoetigt User-Input

## Beispiel: Gateway diagnostizieren

```
PLAN:
  goal: Gateway auf Port 18789 zum Laufen bringen
  max_rounds: 5
  risk: write_fs
  stop_when: netstat zeigt 18789 LISTENING + /health antwortet

ROUND 1: THINK: Port pruefen
  ACT: netstat -ano | findstr :18789
  EVALUATE: Port down → weiter

ROUND 2: THINK: tmp-Dateien und doppelte Instanzen
  ACT: taskkill /F /IM node.exe
  EVALUATE: gekillt → neu starten

ROUND 3: THINK: Gateway neu starten
  ACT: Start gateway.cmd
  EVALUATE: 18789 LISTENING → HALT:SOFT
```

## Kontext-Budget

- max_rounds gilt pro Cascade
- Nie mehr als 3 Tool-Calls pro Round
- Bei HALT:HARD: User informieren was blockiert ist

## Octopaminergic Override (2024 FlyWire)

Falls System-Stress-Level hoch (USDT < $5, EPERM, Loop dead):
- Risk downgrade: write_fs → read_only
- max_rounds halbieren
- User sofort informieren bevor ACT
