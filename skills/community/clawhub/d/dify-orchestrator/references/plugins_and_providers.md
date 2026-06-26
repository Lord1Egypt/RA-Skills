# Plugins And Providers (Self-Hosted Dify)

Diese Referenz sammelt belastbare Grundregeln zu Plugins, Providern und self-hosted Besonderheiten.

## Grundmodell

Plugins sind in Dify der modulare Weg, um Modelle, Tools und Integrationen in einen Workspace zu bringen.

Offiziell dokumentiert:

- Plugins sind workspace-scoped.
- Einmal installierte Plugins koennen in allen Apps des Workspaces genutzt werden.
- Installation ist ueber Marketplace, GitHub-URL plus Version oder Local Upload moeglich.
- Jeder LLM-Provider in Dify ist selbst ein Plugin.

Quelle:

- `https://docs.dify.ai/en/use-dify/workspace/plugins`

## Self-Hosted Relevanz

Bei self-hosted Dify darf man nicht automatisch Cloud-Komfort annehmen.

### OAuth

Offiziell dokumentiert:

- Auf Dify Cloud richtet das Dify-Team fuer populaere Plugins OAuth-Clients vor.
- Bei self-hosted Dify muessen Admins diese OAuth-Client-Einrichtung selbst erledigen.
- Die Redirect-URI fuer Plugin-OAuth haengt am Dify-Domain-/Console-Setup.

Quellen:

- `https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-oauth`
- `https://docs.dify.ai/en/use-dify/nodes/trigger/plugin-trigger`

### Trigger Plugins

Offiziell dokumentiert:

- Trigger koennen als Start-Node fuer Workflows genutzt werden.
- In self-hosted Deployments ist dafuer typischerweise ein eigener OAuth-Client noetig.
- Fuer oeffentlich erreichbare Trigger-Callbacks ist `TRIGGER_URL` relevant.

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/trigger/plugin-trigger`

## Offizielles Plugin-Repository

Seit Dify `v1.0.0` wurden Modelle und Tools aus dem Haupt-Repository in das offizielle Plugin-Repository ausgelagert.

Dieses Repository ist deshalb eine primaere Quelle fuer aktuelle Plugin-Arten und offizielle Marktplaetze.

Es enthaelt u.a.:

- `models`
- `tools`
- `triggers`
- `datasources`
- `agent-strategies`
- `extensions`

Quelle:

- `https://github.com/langgenius/dify-official-plugins`

## Plugin-Typen praktisch einordnen

### Models

Nutze diesen Typ, wenn ein Modellanbieter oder eine Modellfamilie eingebunden werden soll.

### Tools

Nutze diesen Typ, wenn Apps oder Agents eine gezielte Faehigkeit wie Analyse, Uebersetzung oder externe Aktion brauchen.

### Triggers

Nutze diesen Typ, wenn ein Workflow von einem externen Ereignis gestartet werden soll.

### Datasources

Nutze diesen Typ, wenn externe Datenquellen strukturiert in Dify eingebunden werden sollen.

### Agent Strategies

Nutze diesen Typ, wenn eine neue Reasoning- oder Tool-Selection-Strategie fuer Agent-Nodes gebraucht wird.

### Extensions

Nutze diesen Typ, wenn ueber HTTP-Webhooks oder aehnliche Integrationspunkte ein externer Dienst angeschlossen werden soll.

## Operative Auswahlregel

- Nicht jede Integration ist ein `tool`.
- Event-getriebene Starts eher als `trigger` denken.
- reasoning-spezifische Agent-Logik eher als `agent-strategy` denken.
- webhook-/plattformnahe Integrationen eher als `extension` denken.

## Operative Skill-Regel

- Plugin-, Provider- und OAuth-Aussagen immer als versions- und deployment-sensitiv behandeln.
- Bei self-hosted niemals stillschweigend Cloud-Defaults annehmen.
- Bei Trigger- oder OAuth-Plugins immer pruefen, ob Domain, Callback und Admin-Rechte im self-hosted Setup passen.
