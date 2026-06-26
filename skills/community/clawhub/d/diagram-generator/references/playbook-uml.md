# UML And Data Model Playbook

Use this playbook for sequence diagrams, class diagrams, ER diagrams, and other UML-style documentation.

## Default Choice

- Default format: Mermaid
- Default direction: automatic
- Use Draw.io only when the user needs custom visual placement or presentation-grade styling.
- Excalidraw is not recommended unless the user explicitly wants a whiteboard sketch.

## Sequence Diagrams

Use sequence diagrams for interactions over time.

Rules:
- Participant order follows first message appearance.
- Remaining declared nodes appear after first-seen participants.
- Use edge labels for message names and return values.
- Use `relation` to distinguish message type:
  - `sync`: synchronous call, rendered as a normal request.
  - `async`: asynchronous message.
  - `return`: return message.

Example relation mapping:

```json
[
  { "type": "edge", "source": "browser", "target": "api", "label": "Submit order", "relation": "sync" },
  { "type": "edge", "source": "api", "target": "queue", "label": "Publish event", "relation": "async" },
  { "type": "edge", "source": "db", "target": "api", "label": "Order ID", "relation": "return" }
]
```

Quality check:
- Participants appear in a natural left-to-right order.
- Returns use `relation: "return"`.
- Fire-and-forget messages use `relation: "async"`.

## Class Diagrams

Use class diagrams for classes, interfaces, fields, methods, inheritance, composition, aggregation, and dependencies.

Node fields:
- Use `fields` for attributes.
- Use `methods` for operations.
- Keep signatures concise.

Relation mapping:

| Meaning | `relation` |
| --- | --- |
| Association | `association` |
| Inheritance | `inheritance` |
| Composition | `composition` |
| Aggregation | `aggregation` |
| Dependency | `dependency` |
| Realization | `realization` |

Example:

```json
[
  { "id": "entity", "type": "node", "name": "Entity", "fields": ["+String id"], "methods": ["+validate()"] },
  { "id": "order", "type": "node", "name": "Order", "fields": ["+String orderNo"], "methods": ["+pay()"] },
  { "type": "edge", "source": "entity", "target": "order", "relation": "inheritance" }
]
```

Quality check:
- Inheritance, composition, aggregation, and dependency are not all collapsed into association.
- Fields and methods are expressed on nodes instead of being hidden in labels.

## ER Diagrams

Use ER diagrams for database entities, fields, keys, and cardinality.

Field rules:
- Use `fields` for attributes.
- Include type and key markers when known.
- Prefer concise field strings such as `int id PK`, `int user_id FK`, or `datetime created_at`.

Cardinality mapping:

| Meaning | `relation` |
| --- | --- |
| One to one | `oneToOne` |
| One to many | `oneToMany` |
| Many to one | `manyToOne` |
| Many to many | `manyToMany` |
| Zero or one to many | `zeroOrOneToMany` |

Example:

```json
[
  { "id": "customer", "type": "node", "name": "CUSTOMER", "fields": ["int id PK", "string name"] },
  { "id": "orders", "type": "node", "name": "ORDERS", "fields": ["int id PK", "int customer_id FK"] },
  { "type": "edge", "source": "customer", "target": "orders", "relation": "oneToMany", "label": "places" }
]
```

Quality check:
- Cardinality is explicit.
- Primary and foreign keys are marked when available.
- Field types are preserved when provided by the user.
