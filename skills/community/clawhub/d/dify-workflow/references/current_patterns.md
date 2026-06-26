# Current Workflow Patterns

Diese Referenz sammelt aktuelle, offiziell dokumentierte Muster fuer Dify-Workflows.

## Chatflow vs Workflow Output Nodes

Offiziell dokumentiert:

- `Answer` ist die typische Antwort-Node in Chatflow.
- `End` ist die Abschluss-Node in Workflow.
- Chatflow ist auf mehrturnige Interaktion ausgelegt.
- Workflow ist eher fuer einmalige Prozessausfuehrung gedacht.

Quellen:

- `https://docs.dify.ai/en/use-dify/getting-started/key-concepts#workflow`
- `https://docs.dify.ai/versions/legacy/en/user-guide/build-app/flow-app/create-flow-app`

## Trigger-Startpunkte sind versions- und deployment-sensitiv

Im aktuellen Dify-Umfeld sind Trigger ein offizieller Workflow-Einstiegspunkt. Trigger-Verhalten ist aber besonders versions- und self-hosted-sensitiv.

Wichtige Regeln:

1. Trigger nicht stillschweigend als immer verfuegbar annehmen.
2. Trigger-Fragen gegen Doku und Release Notes pruefen.
3. Bei self-hosted Trigger-Plugins an Domain, Callback und `TRIGGER_URL` denken.

Quellen:

- `https://docs.dify.ai/en/use-dify/nodes/trigger/plugin-trigger`
- `https://github.com/langgenius/dify/releases`

## Fehlerpfade nicht nur theoretisch modellieren

Bei riskanten Flows:

1. `fail-branch` nur dann nutzen, wenn Export und Node-Typ das hergeben.
2. nach Fehlerpfaden haeufig Aggregation oder saubere End-/Answer-Verdrahtung planen.
3. Fehlerpfade immer gegen Re-Import und echte Outputs pruefen.

Praktische Folge:

- nicht nur "Recovery-Branch" sagen,
- sondern Outputs, Handles und nachgelagerte Nodes explizit mitdenken.

## Operator- und Hilfsnodes nur mit Quellenkontext behaupten

Nodes wie `if-else`, `list-operator`, `parameter-extractor` oder Dokument-/Datei-bezogene Nodes sollten im Skill nur dann stark behauptet werden, wenn:

1. die Zielversion sie dokumentiert oder exportbasiert bestaetigt,
2. Inputs/Outputs zum Export passen,
3. Import und Re-Import fuer die Zielinstanz realistisch bleiben.

## Operative Skill-Regel

- Neue Workflow-Muster immer zuerst als exportbasierte Minimaledits denken.
- Node-Tricks ohne Re-Import-Pfad sind nur Theorie.
- Bei self-hosted Triggern und Plugin-Nodes immer die Betriebsrealitaet mitpruefen, nicht nur die DSL-Form.
