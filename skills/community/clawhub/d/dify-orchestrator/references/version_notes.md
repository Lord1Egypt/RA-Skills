# Version Notes (Self-Hosted Dify)

Diese Referenz sammelt einige aktuelle, offizielle Versionssignale, die fuer self-hosted Dify besonders wichtig sind.

## Plugin-Umstellung ab Dify v1.0.0

Offiziell dokumentiert:

- Seit Dify `v1.0.0` wurden Modelle und Tools in Plugins ausgelagert.
- Das offizielle Plugin-Repository ist seitdem die primaere Quelle fuer offizielle Plugins.

Quelle:

- `https://github.com/langgenius/dify-official-plugins`

## Dify 1.9.0

Offiziell kommuniziert:

- Knowledge Pipeline eingefuehrt
- Queue-based Graph Engine eingefuehrt
- Worker- und Ausfuehrungsparameter fuer Workflows dokumentiert
- Data Source Plugins sind in der offiziellen Plugin-Doku mit `minimum_dify_version = 1.9.0` beschrieben

Quellen:

- `https://github.com/langgenius/dify/releases`
- `https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/datasource-plugin`

## Dify 1.10.0

Offiziell kommuniziert:

- Event-driven Workflows wurden als zentrales Thema hervorgehoben
- Trigger bilden die Grundlage dieser Event-Driven-Workflows

Quellen:

- `https://github.com/langgenius/dify/releases`
- `https://github.com/langgenius/dify/discussions/28192`

## Operative Skill-Regel

- Trigger-, Plugin- und Workflow-Aussagen aktiv gegen den Versionskontext pruefen.
- Bei self-hosted Deployments keine Features pauschal als vorhanden annehmen, nur weil sie in juengerer Doku oder juengeren Releases existieren.
- Bei Upgrade-Empfehlungen den Zielstand und betroffene Integrationen zuerst klaeren.
- Konkrete Mindestversionen wie `Data Source Plugin = 1.9.0` und `Trigger = 1.10.0` aktiv nennen, wenn sie fuer die Antwort relevant sind.
