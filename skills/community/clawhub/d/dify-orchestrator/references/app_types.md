# App Types (Self-Hosted Dify)

Diese Referenz sammelt belastbare Grundregeln zu Dify-App-Typen fuer self-hosted Umgebungen.

## Offiziell bestaetigte App-Typen

Laut offizieller Dify-Doku gibt es fuenf App-Typen:

1. Chatbot
2. Text Generator
3. Agent
4. Chatflow
5. Workflow

Quelle:

- `https://docs.dify.ai/versions/3-0-x/en/user-guide/application-orchestrate/readme`

## Aktuelle Produktlogik

Die aktuelle Doku empfiehlt, bevorzugt **Workflow** oder **Chatflow** als App-Typ zu waehlen. Chatbot, Agent und Text Generator laufen auf derselben Workflow-Engine, bringen aber vereinfachte, aeltere Interfaces mit.

Quelle:

- `https://docs.dify.ai/en/use-dify/getting-started/key-concepts#workflow`

## Chatflow vs Workflow

### Chatflow

Nutze Chatflow fuer:

- mehrstufige dialogische Ablaufe
- mehrmalige Rueckfragen und Kontextfortschreibung
- Memory-gestuetzte Konversation
- Streaming-Antworten ueber `Answer`-Nodes innerhalb des Flows

### Workflow

Nutze Workflow fuer:

- Single-run Automation
- Batch- und Backend-Ablaufe
- lineare oder verzweigte Prozesslogik ohne mehrturnige Chat-Memory
- klassische Endpunkte mit `End`-Node als Abschluss

## Dokumentierte Unterschiede

Offiziell dokumentiert:

1. `End` gehoert zu Workflow.
2. `Answer` gehoert zu Chatflow.
3. Chatflow hat eingebaute Memory-Faehigkeiten.
4. Workflow hat diese Memory-Konfiguration nicht.
5. Chatflow und Workflow haben unterschiedliche eingebaute Startvariablen.

Quellen:

- `https://docs.dify.ai/versions/legacy/en/user-guide/build-app/flow-app/create-flow-app`
- `https://docs.dify.ai/en/use-dify/getting-started/key-concepts#workflow`

## Operative Skill-Regel

- Wenn der User eine mehrturnige, speichernde, interaktive Orchestrierung will, ist `Chatflow` meist der richtige Denkrahmen.
- Wenn der User einen einmaligen, automatisierten Prozess oder Batch-Ablauf will, ist `Workflow` meist der richtige Denkrahmen.
- Wenn nur ein klassischer Chatbot/Text-Generator/Agent gemeint ist, trotzdem gegen die aktuelle Doku denken: viele moderne Faelle sind in Wahrheit Chatflow- oder Workflow-Designfragen.
