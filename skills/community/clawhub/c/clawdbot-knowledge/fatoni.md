---
name: fatoni
type: knowledge
version: 1.0.0
agent: FatoniSkillAgent
description: "FATONI Multi-Agent Orchestration Skill - Code, Strategy, Analytics, Security"
scope:
  - code_generation
  - code_review
  - code_optimization
  - strategic_planning
  - data_analytics
  - security_auditing
  - workflow_orchestration
triggers:
  - fatoni
  - code generieren
  - code erstellen
  - code review
  - code prüfen
  - strategie entwickeln
  - strategieplan
  - daten analysieren
  - analytics
  - dashboard
  - sicherheit prüfen
  - security scan
  - audit
  - optimieren
  - workflow orchestrieren
file_patterns:
  - "*.py"
  - "*.ts"
  - "*.js"
  - "*.json"
outputs:
  - generated_code
  - review_report
  - optimized_code
  - test_suite
  - strategy_plan
  - decision_matrix
  - analytics_dashboard
  - security_audit
quality_gates:
  - "Code reviewed before delivery"
  - "Security scan passed"
  - "Tests generated"
  - "No hardcoded secrets"
---

# FATONI Skill Agent

FATONI ist ein Multi-Agent System mit 40+ Tools, organisiert in 17 spezialisierten Sub-Agents.

## Wann FATONI nutzen?

| Aufgabe | Workflow | Beschreibung |
|---------|----------|--------------|
| Code schreiben | `code` | Generiert, reviewt, optimiert und testet Code |
| Strategieplanung | `strategy` | Insights sammeln, Plan entwickeln, Entscheidungsmatrix |
| Datenanalyse | `analytics` | Daten analysieren, Dashboard erstellen |
| Sicherheitsprüfung | `security` | Code/System scannen, Audit-Report |
| Komplexe Aufgabe | `auto` | Automatische Workflow-Erkennung |

## Verfügbare Workflows

### 🔷 Code Pipeline (`workflow: "code"`)
Vollständige Code-Entwicklung in 4 Schritten:
1. `fatoni_code_generate` → Generiert Code aus Beschreibung
2. `fatoni_code_review` → Automatisches Code Review
3. `fatoni_code_optimize` → Performance-Optimierung
4. `fatoni_code_test` → Unit Tests generieren

**Beispiel:**
```json
{"tool": "fatoni_skill", "args": {"task": "REST API für User-Management", "workflow": "code"}}
```

### 🔷 Strategy Pipeline (`workflow: "strategy"`)
Strategische Planung in 3 Schritten:
1. `fatoni_strategy_insights` → System-Insights sammeln
2. `fatoni_strategy_develop` → Strategieplan entwickeln
3. `fatoni_decision_matrix` → Entscheidungsmatrix erstellen

### 🔷 Analytics Pipeline (`workflow: "analytics"`)
Datenanalyse in 2 Schritten:
1. `fatoni_analytics_analyze` → Daten analysieren
2. `fatoni_analytics_dashboard` → Dashboard generieren

### 🔷 Security Pipeline (`workflow: "security"`)
Sicherheitsaudit in 2 Schritten:
1. `fatoni_security_scan` → Schwachstellen scannen
2. `fatoni_security_audit` → Audit-Report erstellen

## Einzelne Tools (Direkt-Aufruf)

### Code Agent
- `fatoni_code_generate` - Code aus Beschreibung generieren
- `fatoni_code_review` - Code analysieren und bewerten
- `fatoni_code_optimize` - Code optimieren
- `fatoni_code_test` - Unit Tests generieren

### DeepALL Agent (GPT-4 powered)
- `fatoni_deepall_ask` - Fragen stellen (RAG)
- `fatoni_deepall_review` - Code Review mit GPT-4
- `fatoni_deepall_generate` - Code generieren mit GPT-4
- `fatoni_deepall_explain` - Code erklären
- `fatoni_deepall_optimize` - Code optimieren mit GPT-4

### Strategy Agent
- `fatoni_strategy_insights` - Insights sammeln
- `fatoni_strategy_develop` - Strategie entwickeln

### Security Agent
- `fatoni_security_scan` - Sicherheits-Scan
- `fatoni_security_audit` - Audit-Report

## Anwendungsbeispiele

### Beispiel 1: Komplette API entwickeln
```
Nutze fatoni_skill mit:
- task: "Erstelle eine FastAPI für Todo-Management mit CRUD Operationen"
- workflow: "code"
```

### Beispiel 2: Code Review durchführen
```
Nutze fatoni_deepall_review mit:
- code: "<der zu reviewende Code>"
- language: "python"
```

### Beispiel 3: Sicherheitsaudit
```
Nutze fatoni_skill mit:
- task: "Prüfe die Sicherheit der Authentication-Logik"
- workflow: "security"
```

## Integration mit anderen Agents

FATONI kann mit anderen MCP Servern kombiniert werden:
- **Augment/Auggie**: Für Codebase-Kontext
- **Docling RAG**: Für Dokumentations-Suche
- **n8n**: Für Workflow-Automation
- **DeepSynaptica**: Für AGI-Analyse

## Hinweise

- FATONI Backend läuft auf `http://localhost:8001`
- Bei Backend-Ausfall: Simulation Mode aktiv
- Alle Tools unterstützen Python, TypeScript, JavaScript, Rust

