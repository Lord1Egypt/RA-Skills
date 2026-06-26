# 🦅 Context-Hawk

> **KI-Kontext-Gedächtnis-Wächter** — Hör auf, den Faden zu verlieren, und fang an, dich an das Wichtige zu erinnern.

*Gib jedem KI-Agenten ein Gedächtnis, das wirklich funktioniert — über Sessions, Themen und Zeit hinweg.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## Was es macht

Die meisten KI-Agenten leiden an **Amnesie** — jede neue Sitzung beginnt bei Null. Context-Hawk löst das mit einem produktionsreifen Gedächtnisverwaltungssystem, das automatisch erfasst, was wichtig ist, Rauschen verblassen lässt und die richtige Erinnerung zum richtigen Zeitpunkt abruft.

**Ohne Context-Hawk:**
> "Ich habe es dir schon gesagt — ich mag kurze Antworten!"
> (nächste Sitzung, der Agent vergisst es wieder)

**Mit Context-Hawk:**
> (wendet stillschweigend deine Kommunikationspräferenzen aus Sitzung 1 an)
> ✅ Liefert jedes Mal eine präzise, direkte Antwort

---

## ❌ Without vs ✅ With Context-Hawk (TODO: translate)

| Scenario | ❌ Without Context-Hawk | ✅ With Context-Hawk |
|----------|------------------------|---------------------|
| **New session starts** | Blank — knows nothing about you | ✅ Injects relevant memories automatically |
| **User repeats a preference** | "I told you before..." | Remembers from day 1 |
| **Long task runs for days** | Restart = start over | Task state persists via `hawk resume` |
| **Context gets large** | Token bill skyrockets | 5 compression strategies keep it lean |
| **Duplicate info** | Same fact stored 10 times | SimHash dedup — stored once |
| **Memory recall** | All similar, redundant injection | MMR diverse recall — no repetition |
| **Memory management** | Everything piles up forever | 4-tier decay — noise fades, signal stays |
| **Self-improvement** | Repeats the same mistakes | importance + access_count tracking → smart promotion |
| **Multi-agent team** | Each agent starts fresh | Shared memory via LanceDB |

---

## 😰 Pain Points & Solutions (TODO: translate)

| Pain Point | Impact | Context-Hawk Solution |
|------------|--------|----------------------|
| AI forgets every session | Users repeat themselves | 4-tier memory decay |
| Long tasks lost on restart | Work wasted | `hawk resume` |
| Context overflow | Token costs spike | 5 injection + 5 compression strategies |
| Memory noise | Important info buried | AI importance scoring |
| Preferences ignored | User re-explains rules | importance ≥ 0.9 = permanent |

---

## 🎯 5 Core Problems (TODO: translate)

**Problem 1: Session context window limits**
Context has token limit (e.g. 32k). Long history crowds out important content.
→ Context-Hawk compresses/archives, injects only the most relevant.

**Problem 2: AI forgets across sessions**
Session ends → context disappears. Next conversation starts fresh.
→ `hawk recall` retrieves relevant memories for the next session.

**Problem 3: Multiple agents share nothing**
Agent A doesn't know Agent B's context.
→ Shared LanceDB (with hawk-bridge): all agents read/write the same store.

**Problem 4: Context grows too large before LLM**
Recall without optimization = large, repetitive context.
→ Compression + SimHash dedup + MMR: context is much smaller before LLM.

**Problem 5: Memory never self-manages**
No management: messages pile up until overflow.
→ Auto-extraction → importance scoring → 4-tier decay.

---

## ✨ 12 Kernfunktionen

---

## ✨ 12 Kernfunktionen

| # | Funktion | Beschreibung |
|---|---------|-------|
| 1 | **Aufgabenstatus-Persistenz** | `hawk resume` — Status speichern, nach Neustart fortsetzen |
| 2 | **4-stufiges Gedächtnis** | Working → Short → Long → Archive mit Weibull-Abfall |
| 3 | **Strukturiertes JSON** | Wichtigkeitsbewertung (0-10), Kategorie, Ebene, L0/L1/L2-Schichten |
| 4 | **KI-Wichtigkeitsbewertung** | Erinnerungen automatisch bewerten, minderwertige Inhalte verwerfen |
| 5 | **5 Injektionsstrategien** | A(high-imp) / B(aufgabenbezogen) / C(rezent) / D(top5) / E(voll) |
| 6 | **5 Kompressionsstrategien** | summarize / extract / delete / promote / archive |
| 7 | **Selbst-Introspektion** | Prüft Aufgabenklarheit, fehlende Informationen, Schleifenerkennung |
| 8 | **LanceDB-Vektorsuche** | Optional — hybride Vektor + BM25-Suche |
| 9 | **Reines Gedächtnis-Fallback** | Funktioniert ohne LanceDB, JSONL-Datei-Persistenz |
| 10 | **Auto-Deduplizierung** | Führt doppelte Erinnerungen automatisch zusammen |
| 11 | **MMR-Abruf** | Maximale Randrelevanz — vielfältiger Abruf, keine Wiederholung |
| 12 | **6-Kategorie-Extraktion** | KI-gestützte Kategorisierung: Tatsache / Präferenz / Entscheidung / Entität / Aufgabe / Sonstiges |

---

## 🚀 Schnellstart

```bash
# Einzeilige Installation (empfohlen)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# Oder direkt via pip
pip install context-hawk

# Mit allen Funktionen (inkl. sentence-transformers)
pip install "context-hawk[all]"
```

---

## 🏗️ Architektur

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Aktuelle Sitzung (letzte 5-10 Runden)  │
│       ↓ Weibull-Abfall                                        │
│  Short-term      ←── 24h Inhalt, zusammengefasst            │
│       ↓ access_count ≥ 10 + Wichtigkeit ≥ 0.7             │
│  Long-term       ←── Permanentes Wissen, vektorindiziert   │
│       ↓ >90 Tage oder decay_score < 0.15                    │
│  Archive          ←── Historie, bei Bedarf geladen         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Über Neustarts hinweg persistent (Schlüssel!)│
│  - Aktuelle Aufgabe / nächste Schritte / Fortschritt / Ausgaben│
├──────────────────────────────────────────────────────────────┤
│  Injektions-Engine  ←── Strategie A/B/C/D/E bestimmt Abruf │
│  Selbst-Introspektion ←── Jede Antwort prüft Kontext       │
│  Auto-Trigger        ←── Alle 10 Runden (konfigurierbar)    │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Aufgabenstatus-Gedächtnis (Wertvollste Funktion)

Selbst nach Neustart, Stromausfall oder Sitzungswechsel setzt Context-Hawk genau dort fort, wo es aufgehört hat.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "API-Dokumentation abschließen",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Architekturvorlage überprüfen", "Benutzer Bericht erstatten"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Abdeckung muss 98% erreichen", "APIs müssen versioniert sein"],
  "resumed_count": 3
}
```

```bash
hawk task "Dokumentation abschließen"  # Aufgabe erstellen
hawk task --step 1 done             # Schritt als erledigt markieren
hawk resume                           # Nach Neustart fortsetzen ← KERN!
```

---

## 🧠 Strukturiertes Gedächtnis

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Vollständiger Originalinhalt",
  "summary": "Einzeilige Zusammenfassung",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Wichtigkeitsbewertung

| Bewertung | Typ | Aktion |
|-------|------|--------|
| 0.9-1.0 | Entscheidungen/Regeln/Fehler | Permanent, langsamster Abfall |
| 0.7-0.9 | Aufgaben/Präferenzen/Wissen | Langzeitgedächtnis |
| 0.4-0.7 | Dialog/Diskussion | Kurzzeit, Abfall zu Archiv |
| 0.0-0.4 | Chat/Begrüßungen | **Verwerfen, niemals speichern** |

---

## 🎯 5 Kontextinjektionsstrategien

| Strategie | Auslöser | Einsparung |
|----------|---------|-----------|
| **A: Hohe Wichtigkeit** | `Wichtigkeit ≥ 0.7` | 60-70% |
| **B: Aufgabenbezogen** | Scope-Treffer | 30-40% ← Standard |
| **C: Aktuell** | letzte 10 Runden | 50% |
| **D: Top5 Abruf** | Top 5 `access_count` | 70% |
| **E: Voll** | kein Filter | 100% |

---

## 🗜️ 5 Kompressionsstrategien

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4-stufiges Alarm-System

| Stufe | Schwellenwert | Aktion |
|-------|---------|--------|
| ✅ Normal | < 60% | Still |
| 🟡 Beobachten | 60-79% | Kompression vorschlagen |
| 🔴 Kritisch | 80-94% | Auto-Schreiben pausieren, Vorschlag erzwingen |
| 🚨 Gefahr | ≥ 95% | Schreiben blockieren, Kompression Pflicht |

---

## 🚀 Schnellstart

```bash
# LanceDB-Plugin installieren (empfohlen)
openclaw plugins install memory-lancedb-pro@beta

# Skill aktivieren
openclaw skills install ./context-hawk.skill

# Initialisieren
hawk init

# Kernbefehle
hawk task "Meine Aufgabe"    # Aufgabe erstellen
hawk resume             # Letzte Aufgabe fortsetzen ← SEHR WICHTIG
hawk status            # Kontextnutzung anzeigen
hawk compress          # Gedächtnis komprimieren
hawk strategy B        # Zum aufgabenbezogenen Modus wechseln
hawk introspect         # Selbst-Introspektionsbericht
```

---

## Auto-Trigger: Alle N Runden

Alle **10 Runden** (Standard, konfigurierbar) führt Context-Hawk automatisch aus:

1. Kontext-Wasserstand prüfen
2. Gedächtniswichtigkeit bewerten
3. Status an Benutzer melden
4. Kompression vorschlagen, wenn nötig

```bash
# Konfiguration (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # alle N Runden prüfen
  "keep_recent": 5,                 # letzte N Runden bewahren
  "auto_compress_threshold": 70      # komprimieren wenn > 70%
}
```

---

## Dateistruktur

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI-Werkzeug
└── references/
    ├── memory-system.md           # 4-Ebenen-Architektur
    ├── structured-memory.md      # Gedächtnisformat und Wichtigkeit
    ├── task-state.md           # Aufgabenstatus-Persistenz
    ├── injection-strategies.md  # 5 Injektionsstrategien
    ├── compression-strategies.md # 5 Kompressionsstrategien
    ├── alerting.md             # Alarmsystem
    ├── self-introspection.md   # Selbst-Introspektion
    ├── lancedb-integration.md  # LanceDB-Integration
    └── cli.md                  # CLI-Referenz
```

---

## Technische Daten

| | |
|---|---|
| **Persistenz** | JSONL lokale Dateien, keine Datenbank erforderlich |
| **Vektorsuche** | LanceDB (optional) + sentence-transformers local embedding, automatisches Fallback auf Dateien |
| **Suche** | BM25 + ANN Vektorsuche + RRF-Fusion |
| **Embedding-Anbieter** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | Universell, keine Geschäftslogik, funktioniert mit jedem KI-Agenten |
| **Null-Konfiguration** | Sofort einsatzbereit mit intelligenten Standardwerten (BM25-only Modus) |
| **Python** | 3.12+ |

---

## Lizenz

MIT — frei verwendbar, änderbar und verteilbar.
