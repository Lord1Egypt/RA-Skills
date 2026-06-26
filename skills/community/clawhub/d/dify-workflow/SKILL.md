---
name: dify-workflow
description: Use when creating, editing, debugging, or validating Dify workflow DSL for self-hosted Dify. Start from an exported workflow of the target instance, edit minimally, and verify by re-importing.
---

# Dify Workflow DSL (Self-Hosted)

Ein konsolidierter Skill fuer Dify-Workflow-DSL: Authoring, Editing, Debugging, Referenzen, Templates und lokale Validierung in einem Paket.

**Arbeitsbereich:** Workflow-DSL, Import-/Export-nahe Aenderungen und YAML-Validierung
**Nicht zustaendig:** App-, Prompt-, Dataset- oder Knowledge-Base-Orchestrierung. Dafuer den Skill [`../dify/SKILL.md`](../dify/SKILL.md) verwenden.

## Trigger Conditions

Use when:
- Creating a new Dify workflow
- Editing or debugging an existing workflow DSL file
- Adding or removing nodes, edges, or branches
- Migrating workflows between Dify instances
- Validating import errors or suspicious DSL behavior

## Scope Boundaries

Nutze **diesen** Skill fuer:
- Workflow-DSL schreiben oder editieren
- Node-/Edge-Strukturen aendern
- Import-/Export-basierte Workflow-Migration
- YAML-Validierung fuer Workflow-Dateien
- Fehlersuche bei Import- oder Schema-Problemen

Nutze **`dify`** fuer:
- App-Orchestrierung
- Prompt- und Dataset-Operationen
- Knowledge-Base-Management
- Management-API und Console-API Ablaufe
- Betriebsnahe Health-Checks

## Expert Domains

Dieser Skill soll langfristig ein echter self-hosted-Dify-Workflow-Experte fuer diese Bereiche werden:

- Node-Typen, Handles und Variablen-Syntax
- Import-, Re-Import- und Schema-Fallen
- Minimaledits auf Basis realer Exporte
- versions- und plugin-sensitive Workflow-Aussagen
- sichere Draft-/Backup-/Rollback-Pfade vor riskanten Ueberschreibungen

## Rapid Triage

Bleibe in **`dify-workflow`**, wenn der User eines davon liefert oder verlangt:

- exportierte Workflow-DSL
- neue oder geaenderte Nodes, Edges oder Branches
- Importfehler oder Schemafehler
- Variablen-Syntax, Handles, Outputs oder Node-Abhaengigkeiten
- konkrete Minimaledits fuer Re-Import oder erfolgreichen Re-Import auf derselben Zielinstanz

Bleibe **nicht** hier, wenn das Problem per App-, Prompt- oder Dataset-Operation loesbar ist. Dann an `dify` zurueckgeben.

App-, Prompt- oder Dataset-Aufgaben sind in der Regel **Management-Operationen** und gehoeren deshalb zu `dify`, nicht zu `dify-workflow`.

## Operating Principles

1. **Export first**: Ein Export der Zielinstanz ist immer die Quelle der Wahrheit.
2. **Minimal edits**: Nur gezielte Aenderungen, keine Voll-Neuschreibung ohne Not.
3. **Version aware**: Versions- und Plugin-Unterschiede explizit pruefen.
4. **Secrets stay out of content**: Keine API-Keys in YAML, Prompts oder Beispielen.
5. **Validate before import**: Lokal pruefen, dann auf derselben Zielinstanz importieren.

## Recommended Workflow

1. Exportiere einen bekannten, funktionierenden Workflow aus der Zielinstanz.
2. Leite Struktur, Version und Feldnamen aus diesem Export ab.
3. Nutze Templates und Referenzen aus diesem Skill nur als Hilfestellung, nicht als starre Wahrheit.
4. Bearbeite die DSL minimal statt sie komplett neu zu erfinden.
5. Validiere lokal und pruefe danach den Import in derselben Zielinstanz.

Wenn **kein Export** vorliegt:

1. klar sagen: kein Export vorhanden,
2. nicht so tun, als sei ein Template schon produktionsreif,
3. die Antwort explizit als unverified draft markieren,
4. klar sagen, dass der Workflow ohne Export nicht direkt importierbar ist,
5. vor jeder riskanten Ueberschreibung einen bestehenden Export oder ein anderes belastbares Backup fuer Rollback verlangen,
6. auf Export der Zielinstanz bestehen, sobald echte Importfaehigkeit gefordert ist.

## Critical Rules

### Rule 1: Export First

- **Always export** a workflow from the target instance first.
- **Never assume** DSL version, node schema, dependency format, or feature flags.
- Keep edits minimal and aligned to the exported shape.

### Rule 2: Variable Syntax Must Be Exact

```text
{{#NODE_ID.VARIABLE_NAME#}}
```

Wrong examples:
- `{{NODE_ID.VARIABLE_NAME}}`
- `{{#NODE_ID.VARIABLE_NAME}}`
- `{{{#NODE_ID.VARIABLE_NAME#}}}`

### Rule 3: Code Node Outputs Must Match

Wenn ein Code-Node `{"result": ...}` oder andere Felder zurueckgibt, muessen diese Felder im `outputs`-Schema deklariert sein.

### Rule 4: Secrets Stay Outside the DSL

- **Never embed API keys** in node code, prompts, or exported YAML.
- Nutze Dify-Environment-Variablen oder die Server-/Instanzkonfiguration.

### Rule 5: Validate Changed Paths, Not Just Theory

Nach jeder relevanten Aenderung:

1. lokale YAML-Pruefung ausfuehren,
2. betroffene Outputs und Variablen-Verweise gegen die geaenderte Struktur lesen,
3. Re-Import in derselben Zielinstanz empfehlen oder durchfuehren, wenn moeglich.

## Package Contents

- `references/`: DSL-Struktur, Node-Typen, Edge-Regeln und haeufige Fehler
- `templates/`: kompakte Ausgangspunkte fuer neue Workflows
- `assets/`: umfassendere Beispiel-Workflows fuer wiederkehrende Muster
- `scripts/`: lokale Hilfsmittel fuer IDs und Validierung

## Available References

- [`references/workflow_structure.md`](references/workflow_structure.md): Gesamtstruktur der DSL
- [`references/node_types.md`](references/node_types.md): Node-Typen und Einsatzzwecke
- [`references/edge_types.md`](references/edge_types.md): Handles, Kanten und Routing
- [`references/node_positioning.md`](references/node_positioning.md): Layout- und Positionierungsregeln
- [`references/variable-syntax.md`](references/variable-syntax.md): Variablen-Syntax und typische Fehler
- [`references/common-gotchas.md`](references/common-gotchas.md): Import-/Node-/Schema-Fallen
- [`references/node-templates.md`](references/node-templates.md): YAML-Patterns fuer wichtige Nodes
- [`references/current_patterns.md`](references/current_patterns.md): aktuelle Chatflow/Workflow-, Trigger- und Fehlerpfad-Muster
- [`references/advanced_patterns.md`](references/advanced_patterns.md): Human Input, Loop, Iteration und Agent in produktionsnahen Mustern
- [`references/retrieval_patterns.md`](references/retrieval_patterns.md): Knowledge Retrieval, Aggregator, Question Classifier und Document Extractor als Workflow-Muster

Das uebergeordnete Themen- und Quellen-Backlog liegt unter `../../../research/`.

## Templates And Assets

- [`templates/minimal-workflow.yaml`](templates/minimal-workflow.yaml): Minimaler Startpunkt
- [`templates/llm-chain-workflow.yaml`](templates/llm-chain-workflow.yaml): Lineare LLM-Chain
- [`templates/http-llm-workflow.yaml`](templates/http-llm-workflow.yaml): HTTP + LLM Flow
- [`assets/simple_llm_workflow.yml`](assets/simple_llm_workflow.yml): Beispiel fuer einfachen Flow
- [`assets/conditional_workflow.yml`](assets/conditional_workflow.yml): Beispiel fuer IF/ELSE-Routing
- [`assets/error_handling_workflow.yml`](assets/error_handling_workflow.yml): Beispiel fuer Fehlerbehandlung

## Local Scripts

- [`scripts/generate_id.py`](scripts/generate_id.py): Erzeugt eindeutige Node-IDs
- [`scripts/validate_workflow.py`](scripts/validate_workflow.py): Prueft YAML-Struktur und Grundintegritaet

Beispiele:

```bash
# Node-IDs erzeugen
python3 scripts/generate_id.py 5

# Workflow lokal validieren
python3 scripts/validate_workflow.py /absolute/path/to/workflow.yaml
```

## Safety Notes

- Nicht blind auf Templates vertrauen, wenn ein realer Export verfuegbar ist.
- Provider-, Plugin- und Feldnamen immer gegen die Zielinstanz verifizieren.
- Bei Importfehlern zuerst Syntax und Abhaengigkeiten pruefen, nicht sofort die gesamte DSL umbauen.
- Keine Workflow-Aenderungen als bestaetigt betrachten, bevor der Import auf der Zielinstanz erfolgreich war.
- Ohne Export: unverified draft statt direkt importierbar, bis die Zielinstanz einen passenden Export geliefert hat.

## Practical Editing Checklist

1. Start-/End-Nodes vorhanden?
2. Sind alle Node-IDs eindeutig?
3. Referenzieren alle Edges existierende Nodes?
4. Stimmen `sourceHandle` und `targetHandle` zum Node-Typ?
5. Ist die Variablen-Syntax exakt?
6. Stimmen Code-Outputs mit `outputs` ueberein?
7. Sind Provider-/Plugin-Abhaengigkeiten und Versionen zur Zielinstanz passend?
8. Wurde der Import in der Zielinstanz getestet?
9. Ist ohne Export klar markiert, dass es nur ein Draft ist?
10. Gibt es vor riskanten Ersetzungen einen belastbaren Backup- oder Rollback-Pfad?

## Import Error Triage

Wenn ein Re-Import scheitert, in dieser Reihenfolge pruefen:

1. `validate_workflow.py` zuerst laufen lassen.
2. Node-IDs und Edge-Referenzen pruefen.
3. `sourceHandle` und `targetHandle` gegen den betroffenen Node-Typ pruefen.
4. `outputs` von Code-Nodes gegen ihre Rueckgabefelder pruefen.
5. Variable-Syntax und abgeleitete Verweise erneut lesen.
6. Minimalen Fix statt Full Rewrite vorbereiten.
7. Erst danach groessere Strukturfehler oder Versionsunterschiede vermuten.

## Recommended Response Pattern

Wenn ein User eine Workflow-Aenderung will:

1. Frage nach Export oder bestehender DSL-Datei.
2. Klaere Zielinstanz und Dify-Version, falls unklar.
3. Schlage minimale Aenderungen statt Full Rewrite vor.
4. Verweise fuer Details gezielt auf Templates, Referenzen oder Validator.
5. Schliesse mit Re-Import-/Smoke-Check-Schritten auf derselben Zielinstanz ab.

Praktische Rueckgabe an `dify`, falls die Anfrage falsch gelandet ist:

```text
Das ist wahrscheinlich keine DSL-Aenderung, sondern eine Management-Operation an App, Prompt oder Dataset. Ich wechsle dafuer auf `dify`, damit die Management-Operation ohne unnötige Workflow-Komplexitaet umgesetzt wird.
```

## Useful References

- Dify Docs: `https://docs.dify.ai/`
- GitHub Repository: `https://github.com/langgenius/dify`
- Releases: `https://github.com/langgenius/dify/releases`
