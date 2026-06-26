# Mermaid Architecture Diagram Patterns

## System Architecture (flowchart LR/TD)

Use `flowchart` for system and network architecture diagrams.

### Basic System Architecture
```mermaid
flowchart LR
    User["👤 User"] --> LB["Load Balancer"]
    LB --> API1["API Server 1"]
    LB --> API2["API Server 2"]
    API1 & API2 --> Cache["Redis Cache"]
    API1 & API2 --> DB[(PostgreSQL)]
    API1 & API2 --> Queue["Message Queue"]
    Queue --> Worker["Worker Service"]
    Worker --> DB
```

### Network Architecture
```mermaid
flowchart TD
    Internet["🌐 Internet"] --> FW["Firewall"]
    FW --> DMZ["DMZ\n192.168.1.0/24"]
    DMZ --> WAF["Web App Firewall"]
    WAF --> LB["Load Balancer"]
    LB --> INT["Internal Network\n10.0.0.0/8"]
    INT --> APP["App Servers\n10.0.1.x"]
    INT --> DB[(Database\n10.0.2.x)]
    INT --> AUTH["Auth Service\n10.0.3.x"]
```

### Cloud Architecture (AWS style)
```mermaid
flowchart LR
    subgraph AWS["AWS us-east-1"]
        subgraph VPC["VPC 10.0.0.0/16"]
            subgraph Public["Public Subnet"]
                ALB["ALB"]
                NAT["NAT Gateway"]
            end
            subgraph Private["Private Subnet"]
                ECS["ECS Cluster"]
                RDS[(RDS Aurora)]
                Redis["ElastiCache"]
            end
        end
        S3["S3 Bucket"]
        CF["CloudFront"]
        R53["Route 53"]
    end
    User["👤 User"] --> R53 --> CF --> ALB --> ECS
    ECS --> RDS & Redis & S3
    ECS --> NAT --> Internet["🌐 Internet"]
```

### Microservices Architecture
```mermaid
flowchart LR
    Client["Client App"] --> GW["API Gateway"]
    GW --> Auth["Auth Service"]
    GW --> User["User Service"]
    GW --> Order["Order Service"]
    GW --> Product["Product Service"]
    Auth --> UserDB[(User DB)]
    User --> UserDB
    Order --> OrderDB[(Order DB)]
    Order --> Product
    Order --> MQ["Message Bus"]
    MQ --> Notify["Notification Service"]
    MQ --> Billing["Billing Service"]
    Product --> ProductDB[(Product DB)]
```

## C4 Architecture Diagrams

Use `C4Context` for high-level system context diagrams.

### C4 Context Diagram
```
C4Context
    title System Context — ISAI Platform

    Person(user, "ISAI Analyst", "Security analyst reviewing AI usage")
    Person(admin, "ISAI Admin", "Configures rules and policies")

    System(openclaw, "OpenClaw", "AI security agent and reporting platform")
    System(webhook, "Webhook Ingest", "Captures AI tool usage events firm-wide")

    System_Ext(ai_tools, "AI Tools", "Perplexity, ChatGPT, Copilot, etc.")
    System_Ext(llm, "Anthropic Claude API", "LLM provider for OpenClaw")
    System_Ext(lms, "LMS", "Training completion records")
    System_Ext(iam, "IAM / Active Directory", "User identity and access")

    Rel(user, openclaw, "Queries, reviews reports")
    Rel(admin, openclaw, "Configures rules")
    Rel(ai_tools, webhook, "Sends usage events via browser extension")
    Rel(openclaw, webhook, "Reads telemetry data")
    Rel(openclaw, llm, "Sends prompts, receives responses")
    Rel(openclaw, lms, "Reads training completions")
    Rel(openclaw, iam, "Reads user directory")
```

## Subgraph Styling Tips
- Use `subgraph` to group related components (VPCs, networks, services)
- Use `[(name)]` for databases
- Use `[/name/]` for processes/tasks
- Use `{{name}}` for decision points
- Icons: 👤 🌐 🔒 ☁️ 🗄️ can be embedded in node labels
- Direction: `LR` (left-right) for pipelines, `TD` (top-down) for hierarchies

## Node Shapes Quick Reference
| Shape | Syntax | Use for |
|---|---|---|
| Rectangle | `[text]` | Services, components |
| Rounded | `(text)` | Start/end, soft components |
| Stadium | `([text])` | Terminals |
| Cylinder | `[(text)]` | Databases |
| Diamond | `{text}` | Decisions |
| Parallelogram | `[/text/]` | I/O, processes |
| Hexagon | `{{text}}` | Preparation steps |
| Circle | `((text))` | Events |
