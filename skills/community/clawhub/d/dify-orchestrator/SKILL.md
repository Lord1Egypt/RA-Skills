---
name: dify
description: Use when managing a self-hosted Dify instance, checking feature feasibility, or orchestrating apps, prompts, datasets, and knowledge-base operations via the dify-manager MCP server.
---

# Dify Orchestrator (Self-Hosted)

Fokussierter Skill fuer den operativen Umgang mit einer self-hosted Dify-Instanz: Apps, Datasets, Prompts, Uploads, Retrieval-Checks und Machbarkeitsbewertung.

**Arbeitsbereich:** Instanzbetrieb und Dify-Management
**Nicht zustaendig:** Workflow-DSL authoring oder Import-Editing. Dafuer den Skill [`../dify-workflow/SKILL.md`](../dify-workflow/SKILL.md) verwenden.

## Trigger Conditions

Use when:
- Creating, listing, inspecting, or deleting Dify apps
- Updating prompts for chat/completion style apps
- Creating or linking datasets
- Uploading files into datasets
- Searching an existing knowledge base
- Running a health check on a self-hosted Dify setup
- Checking whether a requested Dify feature is supported on the deployed version

## Scope Boundaries

Nutze **diesen** Skill fuer:
- App-Orchestrierung
- Prompt- und Dataset-Operationen
- Knowledge-Base-Management
- Management-API und Console-API Ablaufe
- Betriebsnahe Entscheidungen und Machbarkeitspruefung

Nutze **`dify-workflow`** fuer:
- Workflow-DSL schreiben oder editieren
- Node-/Edge-Strukturen aendern
- Import-/Export-basierte Workflow-Migration
- YAML-Validierung fuer Workflow-Dateien

## Expert Domains

Dieser Skill soll langfristig ein echter self-hosted-Dify-Experte fuer diese Bereiche werden:

- App-Typen und ihre Einsatzgrenzen
- Prompt-, Dataset- und Knowledge-Base-Operationen
- self-hosted API-/Console-/Management-Abgrenzung
- Feature-Machbarkeit gegen aktuelle Docs und Releases
- Plugin-/Provider-Aussagen nur mit belastbarer Quelle oder Instanztest

## Rapid Triage

Bleibe in **`dify`**, wenn der User vor allem nach diesen Dingen fragt:

- "Erstelle oder aendere eine App"
- "Verknuepfe ein Dataset"
- "Passe den Prompt an"
- "Pruefe Retrieval oder die Knowledge Base"
- "Ist Feature X in meiner Dify-Version verfuegbar?"

Das sind in der Regel **Management-Operationen** an App, Prompt oder Dataset, nicht Workflow-DSL-Aenderungen.

Wechsle zu **`dify-workflow`**, sobald mindestens eines davon zutrifft:

- der User liefert exportiertes Workflow-JSON/YAML
- es geht um Nodes, Edges, Handles, Branches oder Variablen-Syntax
- der Fehler liegt beim Import oder in der DSL-Struktur
- der Wunsch laesst sich nur per Workflow-Edit statt per Management-Operation loesen

## Operating Principles

1. **Version first**: Vor riskanten Aussagen Release Notes und offizielle Dify-Doku pruefen.
2. **Management before DSL**: Wenn das Ziel per App-/Dataset-/Prompt-Operation loesbar ist, nicht unnötig in Workflow-DSL abtauchen.
3. **Export before workflow edits**: Sobald die Anfrage Workflow-JSON/YAML betrifft, an `dify-workflow` uebergeben.
4. **Secrets stay out of content**: Keine API-Keys in Prompts, Beispielen, Logs oder Skill-Doku.
5. **Least surprise**: Vor destruktiven Schritten den Impact klar benennen.

## Available MCP Tools

Der kanonische MCP-Server liegt unter `/Users/alexanderschneider/mcp-servers/dify-manager`.

### App Management

```javascript
dify-manager:list_dify_apps({limit: 20})
dify-manager:create_dify_app({name, mode, description, icon})
dify-manager:get_dify_app({app_id})
dify-manager:update_dify_prompt({app_id, system_prompt, opening_statement})
dify-manager:delete_dify_app({app_id})
```

### Dataset And Knowledge Base

```javascript
dify-manager:list_dify_datasets({limit: 20})
dify-manager:create_dify_dataset({name, description, indexing_technique, doc_form})
dify-manager:link_dataset_to_app({app_id, dataset_id})
dify-manager:add_document_to_dataset({dataset_id, file_path, indexing_technique, doc_form})
dify-manager:search_knowledge_base({query, dataset_names, limit, score_threshold})
```

### Monitoring

```javascript
dify-manager:get_dify_stats()
```

## Expert References

- [`references/app_types.md`](references/app_types.md): belastbare Regeln fuer Chatbot, Text Generator, Agent, Chatflow und Workflow
- [`references/app_type_decision_guide.md`](references/app_type_decision_guide.md): Entscheidungslogik und Anti-Patterns fuer die App-Typ-Auswahl
- [`references/plugins_and_providers.md`](references/plugins_and_providers.md): workspace-scoped Plugins, Provider-Logik, self-hosted OAuth und Trigger-Besonderheiten
- [`references/version_notes.md`](references/version_notes.md): aktuelle Versionssignale fuer Plugin-System, Trigger und Workflow-Engine
- [`references/knowledge_retrieval.md`](references/knowledge_retrieval.md): aktuelle Retrieval-Regeln fuer Knowledge Bases, Rerank, Top K und self-hosted Bildsuche
- [`references/self_hosted_operations.md`](references/self_hosted_operations.md): Betriebsregeln fuer API-/Console-Trennung, Secrets, Smoke-Checks und Trigger-/OAuth-Realitaet
- [`references/plugin_integration_patterns.md`](references/plugin_integration_patterns.md): Datasources, Agent Strategies, Trigger und Extensions als Integrationsmuster

## Preflight Checklist

Vor jeder Schreib- oder Loeschoperation kurz verifizieren:

1. Ist klar, welcher Endpunkt betroffen ist: `DIFY_MGMT_API_URL`, `DIFY_API_URL` oder `DIFY_CONSOLE_API_URL`?
2. Passt die geplante Operation zum App-Typ und zur API-Oberflaeche?
3. Sind App-ID, Dataset-ID oder Dateipfad gegen den Ist-Zustand geprueft?
4. Ist bei potenziell destruktiven Schritten wie `delete_dify_app(...)` der Impact klar benannt?
5. Gibt es direkt danach einen lesenden Check oder Smoke-Check?

Loeschoperationen nie sofort ausfuehren: erst Impact benennen, dann ausdrueckliche Bestaetigung einholen, danach den Smoke-Check planen.

## Self-Hosted Operations Discipline

1. Management-, Runtime- und Console-Pfade nicht vermischen.
2. Secrets nur als lokale Konfiguration oder Secret-Store denken, nie als Skill-Inhalt.
3. Nach App-, Prompt-, Dataset- oder Trigger-Aenderungen immer einen lesenden Folge-Check oder Smoke-Check nennen.
4. Cloud-Komfort nie stillschweigend fuer self-hosted annehmen.

## External Verification

Bei unsicheren oder versionsabhaengigen Fragen:

1. Offizielle Dify-Doku pruefen
2. GitHub Releases von `langgenius/dify` pruefen
3. Erst dann konkrete Aussage oder Umsetzungsplan geben

Typische Kandidaten fuer Verifikation:
- neue Features
- Limits oder Storage-Verhalten
- Plugin-/Provider-Support
- Console-API-Verhalten
- Unterschiede zwischen Chat, Completion, Workflow, Advanced Chat

Primaerquellen und Ausbau-Backlog liegen unter `../../../research/`.

## Recommended Interaction Pattern

### Phase 1: Request Triage

Frueh unterscheiden:
- Geht es um App-/Dataset-Verwaltung? Dann hier bleiben.
- Geht es um Workflow-DSL? Dann zu `dify-workflow`.
- Geht es um Versions-/Feature-Fragen? Erst Docs/Release Notes pruefen.

Praktische Handover-Formulierung:

```text
Das ist keine reine App- oder Dataset-Operation mehr. Ich wechsle auf `dify-workflow`, weil hier eine Workflow-DSL-Aenderung mit export-first, minimalem Edit und erfolgreichem Re-Import auf derselben Zielinstanz noetig ist.
```

### Phase 2: Current State Check

Vor Aenderungen nach Bedarf:

```text
1. list_dify_apps()
2. list_dify_datasets()
3. get_dify_stats()
4. get_dify_app(app_id) bei bestehenden Apps
```

### Phase 3: Safe Execution

- Kleine Schritte statt Massenmutation
- IDs und Namen vor Schreiboperationen verifizieren
- Bei Batch-Operationen Fortschritt und Anzahl nennen
- Bei potenziell destruktiven Schritten explizit warnen

### Phase 4: Verification

Nach Aenderungen:
- App-/Dataset-Zustand erneut lesen
- Falls Prompt geaendert wurde: App-Details oder UI-Test empfehlen
- Falls Uploads erfolgt sind: Retrieval oder UI-Pruefung empfehlen

Minimaler Abschluss pro Schreiboperation:

1. Zielobjekt erneut lesen
2. IDs/Namen gegen Erwartung pruefen
3. naechsten operativen Smoke-Check nennen

## Common Tasks

### New Chat Assistant

1. Anwendungsfall klaeren
2. Als **New Chat Assistant** behandeln und `create_dify_app(...)` ausfuehren
3. optional `create_dify_dataset(...)`
4. `link_dataset_to_app(...)`
5. `update_dify_prompt(...)`
6. Upload- und Testschritte nennen

### Health Check

1. `get_dify_stats()`
2. `list_dify_apps()`
3. `list_dify_datasets()`
4. Probleme benennen:
   - leere Datasets
   - unverknuepfte Datasets
   - alte oder inaktive Apps
   - Prompt-Duplikate

### Knowledge Base Check

1. Ziel-Dataset identifizieren
2. optional Datei per `add_document_to_dataset(...)` hochladen
3. `search_knowledge_base(...)` mit realistischen Queries ausfuehren
4. Retrieval-Qualitaet und naechste Schritte zusammenfassen

### Retrieval Triage

1. Query, Ziel-Knowledge-Base und Retrieval-Settings getrennt betrachten.
2. Bei mehreren Knowledge Bases nicht blind eine einzige Ursache annehmen.
3. Top K, Score Threshold, Rerank und Metadatenfilter als eigene Hebel behandeln.
4. Bei bildbasiertem Retrieval self-hosted Limits und multimodale Knowledge Bases mitdenken.

### Feature Feasibility Check

1. Gewuenschtes Feature konkret benennen
2. App-Typ und Dify-Bereich klaeren: Chatbot, Text Generator, Agent, Chatflow, Workflow, Plugin oder Provider
3. Offizielle Doku und Releases pruefen
4. Keine blinde Zusage machen, bevor die Quellenlage klar ist
5. Aussage klar markieren:
   - bestaetigt
   - nicht bestaetigt
   - aus Quellen nur indirekt ableitbar

### Self-Hosted Operations Triage

1. Vor jeder risikohaften Aussage erst klaeren, welche Oberflaeche wirklich betroffen ist.
2. Trigger-/OAuth-Themen immer mit Domain, Callback, `TRIGGER_URL` und Admin-Rechten denken.
3. Secrets, Delete-Impact und Smoke-Checks in jeder operativen Antwort mitfuehren.

### App-Type Triage

1. Mehrturnige, speichernde, dialogische Logik eher als `Chatflow` denken.
2. Einmalige Automation oder Batch-Logik eher als `Workflow` denken.
3. Chatbot, Text Generator und Agent gegen die aktuelle Produktlogik pruefen, statt sie reflexartig als beste Wahl anzunehmen.
4. Unterschiede fuer Memory, Startvariablen, `Answer` und `End` aus `references/app_types.md` ziehen.
5. Anti-Patterns und vereinfachte Oberflaechen mit `references/app_type_decision_guide.md` abfedern.

### Plugin And Provider Triage

1. Plugins als workspace-scoped Komponenten denken.
2. Nicht so tun, als seien Provider fest eingebaut; Modelle und Tools sind plugin-basiert.
3. Bei self-hosted Trigger- oder OAuth-Fragen aktiv nach Admin-Rechten, Domain und Callback-Setup denken.
4. Vor Aussagen zu Plugin-Verfuegbarkeit oder Upgrade-Verhalten Doku, Releases und offizielle Plugin-Quellen pruefen.
5. Datasources, Agent Strategies, Trigger und Extensions bewusst auseinanderhalten.

### Version-Sensitive Feature Triage

1. Trigger, Event-Driven-Workflows und neue Engine-/Knowledge-Funktionen nicht pauschal als ueberall vorhanden zusagen.
2. Release-Kontext aktiv nennen, wenn ein Feature juenger oder besonders aenderungsanfällig ist.
3. Bei self-hosted immer zwischen "in Dify-Doku beschrieben" und "auf deiner Instanz sicher verfuegbar" unterscheiden.

## Prompt Guidance

Wenn ein Prompt neu erstellt oder ueberarbeitet wird, strukturiere ihn mindestens nach:

- Rolle
- Geltungsbereich
- Antwortstil
- Sicherheitsregeln
- Fallback-Verhalten

Kurzes Muster:

```text
Du bist [Rolle].
Antworte nur im Rahmen von [Scope].
Stil: [kurz/praezise/freundlich/...].
Wenn Informationen fehlen oder die Antwort unsicher ist, sage das klar.
```

## Safety Notes

- `update_dify_prompt(...)` funktioniert nicht fuer alle App-Typen gleich; bei Workflow-/Advanced-Chat-Faellen keine falsche Sicherheit suggerieren.
- Keine geheimen Zugangsdaten in Skill-Beispielen oder Testdaten verwenden.
- Grosse Dataset-Uploads schrittweise angehen und danach Retrieval pruefen.
- Loeschoperationen nur nach klarer Bestatigung ausfuehren.
- Loeschoperationen immer mit Impact-Hinweis und nachfolgendem Smoke-Check rahmen.
- Keine Workflow-Loesungen vorschlagen, wenn eine reine Management-Operation ausreicht.

## Useful References

- Dify Docs: `https://docs.dify.ai/`
- GitHub Repository: `https://github.com/langgenius/dify`
- Releases: `https://github.com/langgenius/dify/releases`
