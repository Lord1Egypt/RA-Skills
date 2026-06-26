# Plugin Integration Patterns

Diese Referenz beschreibt, wann welche fortgeschrittene Plugin-Art in Dify passt.

## Data Source Plugins

Offiziell dokumentiert:

- Dify kennt drei Data-Source-Plugin-Typen:
  - web crawler
  - online document
  - online drive
- typische Beispiele:
  - Web Crawler: Jina Reader, FireCrawl
  - Online Document: Notion, Confluence, GitHub
  - Online Drive: OneDrive, Google Drive, Box, AWS S3, Tencent COS
- `minimum_dify_version` fuer Data-Source-Plugins ist in der Doku mit `1.9.0` beschrieben

Quelle:

- `https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/datasource-plugin`

## Agent Strategy Plugins

Offiziell dokumentiert:

- Agent Strategy Plugins kapseln die Entscheidungs- und Tool-Nutzungslogik fuer Agenten
- typische Basisparameter sind:
  - `model`
  - `tools`
  - `query`
  - `maximum_iterations`
- Tool-Aufrufe laufen ueber `session.tool.invoke()`
- Logging ist ein ausdruecklicher Teil des Plugin-Musters

Quelle:

- `https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/agent-strategy-plugin`

## Trigger Plugins

Offiziell dokumentiert:

- Trigger wurden in Dify `v1.10.0` als neuer Start-Node-Typ eingefuehrt
- ihr Zweck ist nicht "ein weiterer Tool-Node", sondern das Normalisieren externer Event-Formate in Dify-kompatible Eingaben
- technisch basieren sie auf Webhooks

Quelle:

- `https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/trigger-plugin`

## Extensions

Offiziell dokumentiert:

- Extensions sind fuer Integrationen mit externen Services ueber HTTP Webhooks gedacht
- sie sind nicht dasselbe wie ein Tool oder Trigger, sondern eher ein externer Integrationspunkt

Quelle:

- `https://docs.dify.ai/en/develop-plugin/getting-started/getting-started-dify-plugin`

## Operative Auswahlregeln

- Externe Dokument-/Drive-/Crawler-Quellen fuer RAG eher als `datasource` denken.
- Neue Agent-Logik eher als `agent-strategy` denken, nicht als loses Tool.
- Event-Normalisierung fuer Workflow-Starts eher als `trigger` denken.
- Allgemeine HTTP-Integration ohne klassische Tool-Semantik eher als `extension` pruefen.
