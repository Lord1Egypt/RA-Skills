# Phase 1: Ingest

Normalize supplied interfaces into one complete operation inventory before modeling.

| Source        | Extract                                                                                             | Grain clues                                                           |
| ------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| REST/OpenAPI  | path+method operation; parameters/requestBody inputs; 2xx schema outputs                            | array element is often one row; object is often one resource snapshot |
| CLI           | subcommand operation; flags inputs; JSON/example output; classify read/write from observed contract | list often yields detail facts; show/get often yields snapshots       |
| table/DDL/CSV | table candidate; columns attributes/measures; PK business or degenerate key; FK dimension reference | unique-key combination suggests grain                                 |

Record operation name, source location/version, safety (`read` or `write`), inputs, output schema,
pagination, time fields, identifiers, enums, and evidence gaps. Do not infer undocumented response
fields from names or examples from another operation.

Classify a **fact** only when records measure a repeatable business process/event or an aggregatable
snapshot. Classify a **dimension lookup** when it translates stable codes or identifiers. Leave
ambiguous roles open with the evidence needed to decide.

Exit only when every supplied operation appears exactly once with source, read/write status, inputs,
outputs, and a supported role or explicit open decision.
