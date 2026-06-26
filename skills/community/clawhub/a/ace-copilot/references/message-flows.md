# IBM ACE Message Flows

## What is a Message Flow?

A message flow is a directed acyclic graph of nodes that processes messages. Each message travels through the nodes sequentially, being transformed or routed at each step.

```
[MQInput] → [Compute] → [Filter] → [MQOutput]
                              ↓
                         [MQOutput2]  (alternate route)
```

---

## Node Types

### Input Nodes (Entry Points)
| Node | Purpose |
|------|---------|
| `MQInput` | Reads from an MQ queue |
| `HTTPInput` | Receives HTTP/REST requests |
| `SOAPInput` | Receives SOAP web service calls |
| `FileInput` | Reads from a file system directory |
| `JMSInput` | Reads from a JMS queue/topic |
| `KafkaConsumer` | Consumes from a Kafka topic |
| `DatabaseInput` | Polls a database table |
| `TimeoutNotification` | Timer-triggered input |
| `SCADAInput` | Industrial sensor data |

### Processing Nodes
| Node | Purpose |
|------|---------|
| `Compute` | ESQL-based message transformation |
| `JavaCompute` | Java-based transformation |
| `Filter` | ESQL-based conditional routing |
| `Route` | XPath/pattern-based routing to multiple outputs |
| `RouteToLabel` | Dynamic routing using label names |
| `Label` | Target for RouteToLabel |
| `Mapping` | Graphical mapping (no ESQL) |
| `DatabaseRetrieve` | Lookup data from a database |
| `DatabaseInsert` | Insert record into database |
| `DatabaseUpdate` | Update records in database |
| `DatabaseDelete` | Delete records from database |
| `XMLTransformation` | XSLT transformation |
| `DataDelete` | Remove elements from message |
| `Validate` | Validate message against schema |
| `Parse` | Parse a specific message domain |
| `ResetContentDescriptor` | Change message domain/format |
| `Aggregation` | Scatter-gather pattern |
| `Collector` | Collect multiple responses |
| `Sequence` | Enforce message ordering |
| `TryCatch` | Error handling within a flow |
| `Throw` | Raise a flow exception |

### Output Nodes (Exit Points)
| Node | Purpose |
|------|---------|
| `MQOutput` | Write to an MQ queue |
| `HTTPReply` | Send HTTP response |
| `HTTPRequest` | Call external HTTP endpoint |
| `SOAPReply` | Send SOAP response |
| `SOAPRequest` | Call external SOAP service |
| `FileOutput` | Write to a file |
| `JMSOutput` | Write to JMS queue/topic |
| `KafkaProducer` | Produce to Kafka topic |
| `MQGet` | Synchronous MQ get |

---

## Node Terminals

Each node has **input terminals** and **output terminals**:

- **In** — receives the message
- **Out** — normal processing path
- **Failure** — error path (unhandled exceptions)
- **Alternate** — additional conditional output (Filter node)

Connections between terminals form the flow graph.

---

## Message Domains

ACE parses messages into a logical tree using domains:

| Domain | Format |
|--------|--------|
| `XMLNSC` | XML (namespace-aware, recommended) |
| `XML` | XML (legacy) |
| `JSON` | JSON |
| `DFDL` | Custom binary/text formats via DFDL schema |
| `BLOB` | Raw binary (no parsing) |
| `MRM` | Message Repository Manager (legacy) |
| `MIME` | MIME multipart |

Set domain in:
- Input node properties → Message Domain
- `ResetContentDescriptor` node
- ESQL: `SET OutputRoot.Properties.ContentType = 'application/json';`

---

## Common Flow Patterns

### Request-Reply (MQ)
```
MQInput → Compute (transform) → MQOutput (reply-to queue)
```

### HTTP REST API
```
HTTPInput → Compute (build response body) → HTTPReply
```

### Content-Based Routing
```
MQInput → Filter → [route A] MQOutput
                ↓ [alternate]
               MQOutput2
```

### Database Enrichment
```
MQInput → DatabaseRetrieve → Compute (merge data) → MQOutput
```

### Error Handling Pattern
```
MQInput → TryCatch → Compute
              ↓ [Catch]
            Compute (build error) → MQOutput (error queue)
```

### Scatter-Gather (Fan-out/Fan-in)
```
HTTPInput → Compute → [fan-out]
                 ├── HTTPRequest (service A)
                 └── HTTPRequest (service B)
                           ↓ [Collector]
                      Compute (merge) → HTTPReply
```

---

## Subflows

Reusable flow fragments extracted into `.subflow` files:
- Defined in Library projects
- Included via `Flow Order` or directly as a sub-flow node
- Common uses: error handling logic, logging, security checks

```
MainFlow: MQInput → [SubflowNode: LoggingSubflow] → Compute → MQOutput
```

---

## Message Flow Properties

Key properties configurable on any flow:
- **Additional Instances** — parallel execution threads (default 1)
- **Commit Mode** — transaction commit behavior
- **Coordinator** — transaction coordinator type
- **Monitoring** — enable/disable flow monitoring events

---

## .msgflow File Format

Message flows are stored as XML:
```xml
<ecore:EPackage xmlns:ecore="..." name="MyFlow">
  <composition>
    <nodes xsi:type="MQInput" .../>
    <nodes xsi:type="ComputeNode" .../>
    <connections sourceNode="..." targetNode="..." .../>
  </composition>
</ecore:EPackage>
```

Best practice: use ACE Toolkit GUI to edit flows, not raw XML.
