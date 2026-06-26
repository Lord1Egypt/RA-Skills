# System Architecture

## Use Cases

- Software system component relationships
- Infrastructure planning
- Service interaction design
- Technical architecture documentation

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Database | `shape: cylinder` | Data storage |
| External System | `shape: cloud` | Third-party services, external APIs |
| Service Component | Default rectangle | Microservices, application services |

## Basic Example

```d2
direction: right

Frontend App
Backend Service: { shape: rectangle }
Database: { shape: cylinder }

Frontend App -> Backend Service: HTTP
Backend Service -> Database: SQL Query
```

## Cloud Architecture Example

```d2
direction: right

Load Balancer
Web Server: { shape: rectangle }
Database: { shape: cylinder }

Load Balancer -> Web Server: "Distribute traffic"
Web Server -> Database: "Query data"
```

## Microservices Architecture

```d2
direction: right

Frontend Layer: {
  Web App
  Mobile App
  Admin Console
}

Gateway Layer: {
  API Gateway: { shape: rectangle }
  Load Balancer: { shape: rectangle }
}

Service Layer: {
  User Service: { shape: rectangle }
  Order Service: { shape: rectangle }
  Payment Service: { shape: rectangle }
}

Data Layer: {
  User Database: { shape: cylinder }
  Order Database: { shape: cylinder }
  Cache: { shape: cylinder }
}

External Services: {
  Third-party Payment: { shape: cloud }
  Logistics Service: { shape: cloud }
}

Frontend Layer -> Gateway Layer: HTTPS
Gateway Layer -> Service Layer: gRPC
User Service -> User Database: SQL
Order Service -> Order Database: SQL
Service Layer -> Cache: Redis
Payment Service -> Third-party Payment: API
Order Service -> Logistics Service: API
```

## Multi-tier Application Architecture

```d2
direction: down

Presentation Layer: {
  Web Frontend
  Mobile Client
  Desktop App
}

Application Layer: {
  API Gateway
  Business Services: {
    direction: right
    Auth Service
    Data Service
    Report Service
  }
}

Middleware Layer: {
  Message Queue: { shape: queue }
  Cache Layer: { shape: cylinder }
}

Data Layer: {
  Primary Database: { shape: cylinder }
  Replica Database: { shape: cylinder }
  Data Warehouse: { shape: cylinder }
}

Presentation Layer -> API Gateway: HTTPS
API Gateway -> Business Services: REST
Business Services -> Cache Layer: Redis
Business Services -> Message Queue: AMQP
Business Services -> Primary Database: SQL
Primary Database -> Replica Database: Replication
```

## Design Principles

1. **Clear Layering** - Use containers to distinguish different tiers
2. **Label Protocols** - Annotate communication protocols on connection lines
3. **Proper Layout** - Use `direction` to control flow direction
4. **Complete Connections** - Every node must have at least one connection, avoid orphan nodes

## Common Mistakes

### ❌ Wrong: Orphan Nodes (Unconnected Modules)

```d2
# Problem: Logging System, Report Generator not connected to other components
Service Layer: {
  API Service
  Auth Service
}
Utility Layer: {
  Logging System      # Orphan!
  Report Generator    # Orphan!
}
API Service -> Auth Service
```

### ✅ Correct: Ensure All Nodes Are Connected

```d2
Service Layer: {
  API Service
  Auth Service
}
Utility Layer: {
  Logging System
  Report Generator
}
API Service -> Auth Service
API Service -> Logging System: "Log records"
Auth Service -> Logging System: "Log records"
API Service -> Report Generator: "Generate report"
```

### ✅ Better: Remove Non-core Dependencies, Keep It Simple

If a component (like logging) relates to all modules, consider omitting it and only keeping core data flows in the diagram:

```d2
Service Layer: {
  API Service
  Auth Service
}
Database: { shape: cylinder }

API Service -> Auth Service
API Service -> Database
Auth Service -> Database
# Auxiliary components like logging omitted to keep diagram clean
```
