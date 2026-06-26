# Knowledge Retrieval (Self-Hosted Dify)

Diese Referenz sammelt belastbare Regeln fuer RAG- und Retrieval-Fragen in Dify.

## Grundlogik

Die `Knowledge Retrieval`-Node kann bestehende Knowledge Bases in Chatflows oder Workflows einbinden und ihre Treffer als Kontext fuer nachgelagerte Nodes wie LLMs ausgeben.

Offiziell dokumentiert:

1. Query eingeben
2. Knowledge Base(s) waehlen
3. Node-Level Retrieval Settings konfigurieren
4. `result` als Kontext in spaetere Nodes geben

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/knowledge-retrieval`

## Wichtige self-hosted Details

### Query Images

Offiziell dokumentiert:

- Bildbasierte Suche ist moeglich, wenn mindestens eine multimodale Knowledge Base eingebunden ist.
- Das Image-Limit kann bei self-hosted ueber `ATTACHMENT_IMAGE_FILE_SIZE_LIMIT` angepasst werden.

### Mehrere Knowledge Bases

Offiziell dokumentiert:

- Mehrere Knowledge Bases werden zuerst parallel durchsucht.
- Danach greifen Node-Level Settings wie Rerank, Top K und Threshold.

### Retrieval Settings

Offiziell dokumentiert:

- es gibt Knowledge-Base-Level und Node-Level Retrieval Settings
- Weighted Score mischt semantische und keyword-basierte Relevanz
- `Top K` begrenzt die finalen Treffer
- `Score Threshold` filtert zu schwache Treffer
- Metadaten koennen fuer praeziseres Filtern genutzt werden

## Outputs

Die Node liefert laut Doku eine Variable `result`.

Diese enthaelt:

- Treffer-Chunks
- Content
- Metadaten
- Titel
- ggf. `files` bei Bildtreffern

## Operative Skill-Regel

- Bei Retrieval-Problemen nicht nur pauschal "mehr Daten hochladen" sagen.
- Immer Query, Knowledge-Auswahl, Node-Level Settings und Metadatenfilter getrennt denken.
- Bei self-hosted Bild-Retrieval den Vision-/Embedding-Kontext und die Instanzlimits mitpruefen.
