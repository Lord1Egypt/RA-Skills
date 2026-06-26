# Workflow Retrieval Patterns

Diese Referenz beschreibt `Knowledge Retrieval` als echtes Workflow-Muster statt nur als einzelne Node.

## Grundmuster

Die `Knowledge Retrieval`-Node liefert ihre Treffer in der Variable `result`.

Diese `result`-Variable ist typischerweise der Uebergabepunkt an:

- eine nachgelagerte LLM-Node fuer Antwortgenerierung
- einen `Variable Aggregator`, wenn mehrere Retrieval-Pfade wieder zusammengefuehrt werden
- weitere Filter- oder Routing-Logik

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/knowledge-retrieval`

## Retrieval in mehreren Pfaden

Ein typisches Expertenmuster:

1. Frage zuerst klassifizieren, z. B. per `Question Classifier`
2. Je Kategorie eine spezialisierte Knowledge Base oder Retrieval-Node nutzen
3. Die verschiedenen Retrieval-Ergebnisse wieder zusammenfuehren
4. Erst danach eine gemeinsame LLM-Node benutzen

Warum:

- ohne Aggregation braucht jeder Pfad eigene nachgelagerte LLM- oder Antwort-Logik
- mit Aggregation wird der gemeinsame Teil des Workflows deutlich einfacher

Quellen:

- `https://docs.dify.ai/en/guides/workflow/node/variable-aggregator`
- `https://docs.dify.ai/en/guides/workflow/node/question-classifier`

## Wichtige Retrieval-Hebel

### Knowledge-Base-Level vs Node-Level

Die Doku beschreibt zwei Filterebenen:

1. Knowledge-Base-Level-Einstellungen
2. Node-Level-Einstellungen der Retrieval-Node

Das ist wichtig, weil schlechte Ergebnisse nicht immer am Prompt oder an der Query liegen.

### Node-Level-Hebel

- `Rerank Model`
- `Top K`
- `Score Threshold`
- `Metadata Filtering`

### Multimodale Faelle

Wenn multimodale Knowledge Bases beteiligt sind:

- fuer Rerank braucht man einen passenden multimodalen Rerank-Ansatz
- sonst koennen Bilder aus dem finalen Ergebnis herausfallen

## Variable Aggregator als Merge-Pattern

`Variable Aggregator` ist das Standardmittel, um Ergebnisse aus verschiedenen Branches wieder auf einen einheitlichen Downstream-Pfad zu bringen.

Wichtige Regeln:

1. Alle aggregierten Variablen muessen denselben Typ haben.
2. Die Node gibt den Wert aus dem Branch weiter, der tatsaechlich gelaufen ist.
3. Das vermeidet doppelte LLM- oder Antwort-Nodes nach mehreren Branches.

## Dokument- und Datei-Faelle

`Document Extractor` ist ein vorgeschaltetes Muster fuer Dokumentdateien:

1. Datei hochladen
2. Dokumenttext extrahieren
3. Text an LLM oder andere Folgeschritte geben

Bei `Array[File]`-Faellen gilt:

- haeufig erst per `List Operator` oder Routing auftrennen
- nicht alles blind in denselben Extraktionspfad schicken
- Bilder und Dokumente nicht alles ueber denselben Document-Extractor-Pfad behandeln

Quellen:

- `https://docs.dify.ai/en/use-dify/nodes/doc-extractor`
- `https://docs.dify.ai/versions/3-0-x/en/user-guide/workflow/file-upload`

## Operative Skill-Regeln

- Retrieval nicht nur als "Node einfuegen" denken, sondern als abgestuften RAG-Pfad.
- Bei Mehrfach-Retrieval frueh an `Variable Aggregator` denken.
- `Document Extractor` nicht fuer Bilder, Audio oder Video missbrauchen.
- Bei Re-Import darauf achten, dass `result`-Folgepfade, Aggregation und Downstream-Variablen weiter zum Export passen.
