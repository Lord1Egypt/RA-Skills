---
name: DeepSynaptica AGI
type: knowledge
version: 1.0
agent: deepsynaptica
triggers:
  - deepsynaptica
  - synaptica
  - agi
  - kognition
  - cognition
  - semantic
  - reflection
  - knowledge map
  - wissenskarte
---

# DeepSynaptica AGI System

DeepSynaptica ist ein fortschrittliches Artificial General Intelligence System mit kognitiver Verarbeitung, semantischer Analyse und Meta-Reflexion.

## MCP Tools (deepsynaptica Server)

### synaptica_process
Verarbeitet eine Anfrage durch die komplette AGI Pipeline.
```
synaptica_process(query="Analysiere dieses Problem", documentation="optional context")
```
Rückgabe: antwort, kontext, score, meta_feedback, entscheidung, phasen, rolle

### analyze_cognition_phases
Erkennt kognitive Phasen im Text (Exploration, Verbindung, Struktur, Präzisierung, Forderung, Abschluss).
```
analyze_cognition_phases(text="Ich denke, wir brauchen eine Verbindung...")
```

### gpt_agent_query
GPT-Abfrage mit rollenbasiertem Prompting.
Rollen: analyst, reflektor, docwriter, strategist
```
gpt_agent_query(query="Frage", context="Kontext", role="analyst")
```

### evaluate_meta_trend
Bewertet Score und berechnet Systemtrend.
```
evaluate_meta_trend(score=0.75)
```

### build_knowledge_map
Erstellt Wissensgraph aus Dokumentation.
```
build_knowledge_map(documentation="Modulbeschreibung...")
```

### semantic_document_analysis
Semantische Dokumentanalyse mit Modul-Extraktion.
```
semantic_document_analysis(documentation="...", query="optional search")
```

### deep_reflect
Bewertet Inhaltsqualität mit Verbesserungsvorschlägen.
```
deep_reflect(content="Zu bewertender Text")
```

### get_vault_history
Holt Analyse-Historie aus dem Vault.
```
get_vault_history(limit=10)
```

### system_health_check
Prüft DeepSynaptica System-Gesundheit.
```
system_health_check()
```

## API Endpoints (Port 8000)

Starte das Backend mit: `python api_backend.py`

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| /health | GET | System-Status |
| /api/analyze | POST | Dokument analysieren |
| /api/analyze/{id} | GET | Analyse-Status |
| /api/vault/analyses | GET | Alle Analysen |
| /api/gpt/query | POST | GPT Query |
| /api/system/info | GET | System Info |
| /api/monitor/metrics | GET | Metriken |

## Kognitive Phasen

1. **Exploration** - Offenes Denken ("ich denke", "vielleicht")
2. **Verbindung** - Zusammenhänge erkennen
3. **Struktur** - Ordnung schaffen
4. **Präzisierung** - Konkretisieren
5. **Forderung** - Aktionen anfordern
6. **Abschluss** - Zusammenfassen

## Rollen

- **analyst** - Präzise Systemanalyse
- **reflektor** - Kritische Reflexion, Schwächen finden
- **docwriter** - Klare, strukturierte Zusammenfassungen
- **strategist** - Zusammenhänge erkennen, Strategien vorschlagen

## Beispiel-Workflow

1. Text mit `analyze_cognition_phases` analysieren
2. Phase bestimmt die Rolle für `gpt_agent_query`
3. Antwort mit `deep_reflect` bewerten
4. Score mit `evaluate_meta_trend` tracken
5. Optional: `build_knowledge_map` für Visualisierung
