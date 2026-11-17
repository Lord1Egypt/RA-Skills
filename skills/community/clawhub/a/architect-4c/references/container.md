# L2 Container diagram

Expand one system to show applications and data stores, their responsibilities, technologies, and communication.

## Drawing approach

- Expand the payment platform into the payment application and database. Retain external system names and types.
- Jobs run inside the payment application as components. Use a separate container if evidence shows an independently started and deployed worker.
- Use execution boundaries to distinguish a SPA, API, or job process. Libraries and source folders alone cannot establish container boundaries.
- Separate logical data ownership from hosting location. Put machines, replicas, and load balancers in deployment views.

This is a fictional target design. The dashed boundary is the system. Green marks the application container, purple the data container, and gray external systems. Solid lines represent communication.

Use the shared [diagram and visual guidelines](diagram-guidelines.md).

## Complete templates

### Dark

```mermaid
---
config:
  theme: "base"
  look: "classic"
  fontFamily: "\"PingFang SC\", \"Helvetica Neue\", Arial, sans-serif"
  flowchart: {nodeSpacing: 28, rankSpacing: 40, padding: 14, curve: basis}
  sequence: {mirrorActors: false, actorMargin: 42, messageMargin: 28, boxMargin: 10}
  themeVariables: {darkMode: true, background: '#07111F', fontFamily: '"PingFang SC", "Helvetica Neue", Arial, sans-serif', fontSize: 15px,
      primaryColor: '#0B2B25', primaryTextColor: '#E6EDF3', primaryBorderColor: '#34D399', lineColor: '#B8C4D4',
      textColor: '#E6EDF3', secondaryColor: '#211532', tertiaryColor: '#101B2B', clusterBkg: '#101B2B', clusterBorder: '#66758A',
      edgeLabelBackground: '#07111F', actorBkg: '#101B2B', actorBorder: '#34D399', actorTextColor: '#E6EDF3', actorLineColor: '#66758A',
      signalColor: '#B8C4D4', signalTextColor: '#E6EDF3', labelBoxBkgColor: '#101B2B', labelBoxBorderColor: '#66758A',
      labelTextColor: '#E6EDF3', loopTextColor: '#E6EDF3', noteBkgColor: '#28220E', noteBorderColor: '#FACC15',
      noteTextColor: '#E6EDF3', activationBkgColor: '#0B2B25', activationBorderColor: '#34D399', sequenceNumberColor: '#07111F'}
  themeCSS: |
    .nodeLabel small { color: #9AA9BC; font-size: 12px; }
    .nodeLabel b { font-weight: 600; }
    .cluster-label { font-weight: 600; }
    .edgeLabel { background-color: #07111F; color: #9AA9BC; }
    .cluster rect { rx: 10; ry: 10; }
    .actor { rx: 8; ry: 8; }
---
flowchart LR
    Merchant("<b>Merchant order system</b><br/><small>External software system<br/>Manages orders and receives results</small>")
    Provider("<b>Payment provider</b><br/><small>External software system<br/>Charges and confirms results</small>")
    subgraph Platform["◈ Payment platform | L2"]
        direction TB
    PayApp("<b>Payment application</b><br/><small>Application container | Java 21 / Spring Boot<br/>Accepts, reconciles, notifies</small>")
    PayDB[("<b>Payment database</b><br/><small>Data container | PostgreSQL<br/>Payment state and delivery tasks</small>")]
    PayApp -->|"Reads and writes payments and tasks | SQL/TLS"| PayDB
    end
    Merchant -->|"Initiates payment | JSON/HTTPS"| PayApp
    PayApp -->|"Notifies payment result | JSON/HTTPS"| Merchant
    PayApp -->|"Requests charge and queries result | JSON/HTTPS"| Provider
    Provider -->|"Sends provider result | JSON/HTTPS"| PayApp
    classDef external fill:#101B2B,stroke:#66758A,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef service fill:#0B2B25,stroke:#34D399,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class PayApp service
    classDef data fill:#211532,stroke:#C084FC,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class PayDB data
    style Platform fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

### Light

```mermaid
---
config:
  theme: "base"
  look: "classic"
  fontFamily: "\"PingFang SC\", \"Helvetica Neue\", Arial, sans-serif"
  flowchart: {nodeSpacing: 28, rankSpacing: 40, padding: 14, curve: basis}
  sequence: {mirrorActors: false, actorMargin: 42, messageMargin: 28, boxMargin: 10}
  themeVariables: {darkMode: false, background: '#F8FAFC', fontFamily: '"PingFang SC", "Helvetica Neue", Arial, sans-serif',
      fontSize: 15px, primaryColor: '#ECFDF5', primaryTextColor: '#142238', primaryBorderColor: '#047857', lineColor: '#52657D',
      textColor: '#142238', secondaryColor: '#FAF5FF', tertiaryColor: '#F1F5F9', clusterBkg: '#F1F5F9', clusterBorder: '#8090A4',
      edgeLabelBackground: '#F8FAFC', actorBkg: '#F1F5F9', actorBorder: '#047857', actorTextColor: '#142238', actorLineColor: '#8090A4',
      signalColor: '#52657D', signalTextColor: '#142238', labelBoxBkgColor: '#F1F5F9', labelBoxBorderColor: '#8090A4',
      labelTextColor: '#142238', loopTextColor: '#142238', noteBkgColor: '#FFFBEB', noteBorderColor: '#92400E',
      noteTextColor: '#142238', activationBkgColor: '#ECFDF5', activationBorderColor: '#047857', sequenceNumberColor: '#F8FAFC'}
  themeCSS: |
    .nodeLabel small { color: #53647A; font-size: 12px; }
    .nodeLabel b { font-weight: 600; }
    .cluster-label { font-weight: 600; }
    .edgeLabel { background-color: #F8FAFC; color: #53647A; }
    .cluster rect { rx: 10; ry: 10; }
    .actor { rx: 8; ry: 8; }
---
flowchart LR
    Merchant("<b>Merchant order system</b><br/><small>External software system<br/>Manages orders and receives results</small>")
    Provider("<b>Payment provider</b><br/><small>External software system<br/>Charges and confirms results</small>")
    subgraph Platform["◈ Payment platform | L2"]
        direction TB
    PayApp("<b>Payment application</b><br/><small>Application container | Java 21 / Spring Boot<br/>Accepts, reconciles, notifies</small>")
    PayDB[("<b>Payment database</b><br/><small>Data container | PostgreSQL<br/>Payment state and delivery tasks</small>")]
    PayApp -->|"Reads and writes payments and tasks | SQL/TLS"| PayDB
    end
    Merchant -->|"Initiates payment | JSON/HTTPS"| PayApp
    PayApp -->|"Notifies payment result | JSON/HTTPS"| Merchant
    PayApp -->|"Requests charge and queries result | JSON/HTTPS"| Provider
    Provider -->|"Sends provider result | JSON/HTTPS"| PayApp
    classDef external fill:#F1F5F9,stroke:#8090A4,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef service fill:#ECFDF5,stroke:#047857,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class PayApp service
    classDef data fill:#FAF5FF,stroke:#7E22CE,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class PayDB data
    style Platform fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

The payment application exclusively accesses the database, which stores payment state and delivery tasks. Atomic persistence of final state and delivery task is an example design decision. Component and dynamic views must assign its implementation.

## Checks

- Confirm each internal node is an application or data store, with explicit responsibility, technology, protocol, and data ownership.
- Map L1's external relationships to containers and expand the same payment application at L3.

See the [C4 container diagram](https://c4model.com/diagrams/container) and [container abstraction](https://c4model.com/abstractions/container).
