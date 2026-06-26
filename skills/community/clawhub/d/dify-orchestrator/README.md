# Dify Skill

Projekt-Skill fuer self-hosted Dify-Orchestrierung.

## Zweck

Dieser Skill deckt den operativen Teil von Dify ab:

- Apps verwalten
- Datasets anlegen und verknuepfen
- Prompts aktualisieren
- Dokumente in Datasets hochladen
- Retrieval und Health-Checks ausfuehren
- Feature-Machbarkeit gegen Doku und Release Notes absichern

Das Ziel ist nicht nur sichere Orchestrierung, sondern belastbare self-hosted-Dify-Expertise fuer App-Typen, RAG-Ablaufe, Provider-/Plugin-Aussagen und Betriebsgrenzen.

Workflow-DSL gehoert bewusst **nicht** mehr hier hinein. Dafuer gibt es jetzt den separaten Skill [`../dify-workflow/SKILL.md`](../dify-workflow/SKILL.md).

## Paketstruktur

```text
dify/
├── SKILL.md
├── README.md
├── VERSION
├── references/
└── examples.md
```

## MCP Server

Kanonischer Pfad:

```text
/Users/alexanderschneider/mcp-servers/dify-manager
```

## Beispielkonfiguration

```json
{
  "mcpServers": {
    "dify-manager": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/Users/alexanderschneider/mcp-servers/dify-manager",
      "env": {
        "DIFY_MGMT_API_URL": "https://deine-dify-instanz.example/mgmt-api",
        "DIFY_MGMT_API_KEY": "nur-als-local-secret-setzen",
        "DIFY_API_URL": "https://deine-dify-instanz.example/v1",
        "DIFY_API_KEY": "nur-als-local-secret-setzen",
        "DIFY_CONSOLE_API_URL": "https://deine-dify-instanz.example/console/api",
        "DIFY_CONSOLE_EMAIL": "admin@example.com",
        "DIFY_CONSOLE_PASSWORD": "nur-als-local-secret-setzen"
      }
    }
  }
}
```

## Arbeitsweise

1. Bestehenden Zustand lesen
2. Ziele und Risiken klaeren
3. Preflight fuer Endpunkt, App-Typ und IDs machen
3. Kleine Management-Operationen ausfuehren
4. Ergebnis verifizieren
5. Bei Workflow-DSL-Fragen an `dify-workflow` uebergeben

## Preflight vor Schreiboperationen

Vor `create`, `update`, `link`, Upload oder Delete kurz pruefen:

1. Welche API ist gemeint: Management, Runtime oder Console?
2. Ist der App-Typ kompatibel mit der geplanten Aenderung?
3. Stimmen IDs und Namen mit dem gelesenen Ist-Zustand ueberein?
4. Ist nach der Aenderung ein lesender Folge-Check definiert?

## Validierung im Workspace

```bash
# Skill-Paket pruefen
python3 scripts/validate_skills.py .codex/skills
```

Nach inhaltlichen Aenderungen sollte mindestens geprueft werden:

1. Trigger und Scope sind noch eindeutig.
2. Relative Referenzen zeigen auf existierende Dateien.
3. Beispiel-Calls passen weiter zum `dify-manager` MCP-Server.

## Typische Tool-Calls

```javascript
dify-manager:list_dify_apps({limit: 20})
dify-manager:create_dify_app({name: "support-bot", mode: "chat"})
dify-manager:create_dify_dataset({name: "support-kb", indexing_technique: "high_quality"})
dify-manager:link_dataset_to_app({app_id: "app-id", dataset_id: "dataset-id"})
dify-manager:update_dify_prompt({app_id: "app-id", system_prompt: "..."})
dify-manager:search_knowledge_base({query: "Docker Volumes", dataset_names: ["support-kb"]})
```

Der typische Support-Bot-Fall ist eine New Chat Assistant Management-Operation mit `create_dify_app(...)`, `create_dify_dataset(...)` und `link_dataset_to_app(...)`, nicht Workflow-DSL.

## Fachliche Referenzen

- [`references/app_types.md`](references/app_types.md)
- [`references/plugins_and_providers.md`](references/plugins_and_providers.md)

## Hinweise

- Vor versionskritischen Aussagen offizielle Dify-Doku und Release Notes pruefen.
- Keine Secrets in Prompts, Beispielen oder Commit-Historie hinterlegen.
- Workflow-JSON/YAML nicht hier dokumentieren oder pflegen.
- Quellen- und Themenausbau werden unter `../../../research/` gepflegt.
