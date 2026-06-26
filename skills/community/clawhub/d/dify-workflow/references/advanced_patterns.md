# Advanced Workflow Patterns

Diese Referenz sammelt aktuelle, offiziell dokumentierte Muster fuer Human Input, Loop, Iteration und Agent-Nodes.

## Human Input

Offiziell dokumentiert:

- pausiert den Workflow fuer menschliche Freigabe, Review oder Entscheidung
- Zustellung aktuell per Web App oder Email
- die erste Antwort schliesst die Anfrage
- Entscheidungen koennen verschiedene Folgepfade ausloesen
- bei Timeout endet der Workflow standardmaessig, ausser ein Fallback-Branch ist definiert

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/human-input`

## Iteration

Offiziell dokumentiert:

- verarbeitet Arrays elementweise
- eignet sich fuer Batch-Operationen
- jedes Element bekommt eingebaute Variablen `item`/`items` und `index`
- kann sequentiell oder parallel laufen
- Parallelmodus verarbeitet bis zu 10 Items gleichzeitig
- Fehlerbehandlung kennt u.a. `Terminate`, `Continue on Error` und `Remove Failed Results`

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/iteration`

## Loop

Offiziell dokumentiert:

- ist fuer progressive Verfeinerung gedacht
- jede Runde baut auf dem Ergebnis der vorherigen auf
- Loop-Variablen persistieren ueber die Iterationen
- Abbruch per Condition, Max Count oder Exit Loop

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/loop`

## Agent

Offiziell dokumentiert:

- Agent-Nodes geben dem Modell autonome Tool-Kontrolle
- es gibt mindestens `Function Calling` und `ReAct`
- die Modellwahl muss zur Strategie passen
- Tool-Beschreibungen und Parameterqualitaet beeinflussen das Agent-Verhalten direkt
- `Maximum Iterations` begrenzt Kosten und Endlosschleifen
- Outputs enthalten u.a. Final Answer, Tool Outputs, Reasoning Trace, Iteration Count, Success Status und Logs

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/agent`

## Operative Skill-Regeln

- Human Input fuer echte Approval- oder Review-Gates nutzen, nicht nur als kosmetischen Halt.
- Iteration fuer unabhaengige Array-Verarbeitung, Loop fuer zustandsbehaftete Verfeinerung.
- Agent nur dann empfehlen, wenn Tool-Autonomie wirklich gebraucht wird; sonst oft lieber explizite Workflow-Node-Kette.
- Bei Agent-Strategien Modellfaehigkeiten, Kosten und Iterationslimit immer mitdenken.
