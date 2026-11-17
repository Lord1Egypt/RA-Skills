# Deployment diagram

Map logical container instances to deployment nodes in one environment and show communication paths.

## Drawing approach

- This proposed production environment contains an ingress load balancer, two JVMs, and one database runtime.
- Each JVM runs one payment application instance. Both map to the L2 application, and the database instance maps to the L2 database.
- Provider callbacks pass through ingress. The application accesses the database and sends requests to the merchant and provider.
- Add availability zones, networks, and failover from evidence. Separate hosting location from logical ownership.

This is a fictional target design. The outer dashed boundary is the environment and inner boundaries are runtime nodes. Green marks application instances, purple the data instance, yellow infrastructure, and gray external systems. Solid lines represent communication.

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
flowchart TB
    Merchant("<b>Merchant order system</b><br/><small>External software system<br/>Manages orders and receives results</small>")
    Provider("<b>Payment provider</b><br/><small>External software system<br/>Charges and confirms results</small>")
    subgraph Production["☁ Proposed production"]
        direction TB
    Ingress("<b>Ingress load balancer</b><br/><small>Infrastructure | HTTPS</small>")
        subgraph NodeA["Runtime node A | JVM"]
    AppA("<b>Payment application instance A</b><br/><small>Container instance | Payment application</small>")
        end
        subgraph NodeB["Runtime node B | JVM"]
    AppB("<b>Payment application instance B</b><br/><small>Container instance | Payment application</small>")
        end
        subgraph NodeDB["Database runtime node"]
    Database[("<b>Payment database instance</b><br/><small>Container instance | Payment database | PostgreSQL</small>")]
        end
    Ingress -->|"Routes API and callbacks | HTTPS"| AppA
    Ingress -->|"Routes API and callbacks | HTTPS"| AppB
    AppA -->|"Reads and writes payments and tasks | SQL/TLS"| Database
    AppB -->|"Reads and writes payments and tasks | SQL/TLS"| Database
    end
    Merchant -->|"Initiates payment | HTTPS"| Ingress
    Provider -->|"Sends provider result | HTTPS"| Ingress
    AppA -->|"Charge and result query | HTTPS"| Provider
    AppB -->|"Charge and result query | HTTPS"| Provider
    AppA -->|"Notifies payment result | HTTPS"| Merchant
    AppB -->|"Notifies payment result | HTTPS"| Merchant
    classDef external fill:#101B2B,stroke:#66758A,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef infra fill:#28220E,stroke:#FACC15,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Ingress infra
    classDef service fill:#0B2B25,stroke:#34D399,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class AppA,AppB service
    classDef data fill:#211532,stroke:#C084FC,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Database data
    style Production fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeA fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeB fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeDB fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
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
flowchart TB
    Merchant("<b>Merchant order system</b><br/><small>External software system<br/>Manages orders and receives results</small>")
    Provider("<b>Payment provider</b><br/><small>External software system<br/>Charges and confirms results</small>")
    subgraph Production["☁ Proposed production"]
        direction TB
    Ingress("<b>Ingress load balancer</b><br/><small>Infrastructure | HTTPS</small>")
        subgraph NodeA["Runtime node A | JVM"]
    AppA("<b>Payment application instance A</b><br/><small>Container instance | Payment application</small>")
        end
        subgraph NodeB["Runtime node B | JVM"]
    AppB("<b>Payment application instance B</b><br/><small>Container instance | Payment application</small>")
        end
        subgraph NodeDB["Database runtime node"]
    Database[("<b>Payment database instance</b><br/><small>Container instance | Payment database | PostgreSQL</small>")]
        end
    Ingress -->|"Routes API and callbacks | HTTPS"| AppA
    Ingress -->|"Routes API and callbacks | HTTPS"| AppB
    AppA -->|"Reads and writes payments and tasks | SQL/TLS"| Database
    AppB -->|"Reads and writes payments and tasks | SQL/TLS"| Database
    end
    Merchant -->|"Initiates payment | HTTPS"| Ingress
    Provider -->|"Sends provider result | HTTPS"| Ingress
    AppA -->|"Charge and result query | HTTPS"| Provider
    AppB -->|"Charge and result query | HTTPS"| Provider
    AppA -->|"Notifies payment result | HTTPS"| Merchant
    AppB -->|"Notifies payment result | HTTPS"| Merchant
    classDef external fill:#F1F5F9,stroke:#8090A4,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef infra fill:#FFFBEB,stroke:#A16207,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Ingress infra
    classDef service fill:#ECFDF5,stroke:#047857,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class AppA,AppB service
    classDef data fill:#FAF5FF,stroke:#7E22CE,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Database data
    style Production fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeA fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeB fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeDB fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

Both application instances contain jobs. Claiming tasks requires a lease or equivalent concurrency control, with duplicate delivery handling. The single-database example makes no automatic failover or high-availability claim.

## Checks

- Support the environment, counts, and placement with evidence or an explicit target design. Map each instance to its L2 container.
- Check ingress, callback, outbound, and database paths, along with job coordination, state consistency, and recovery across instances.

See the [C4 deployment diagram definition](https://c4model.com/diagrams/deployment).
