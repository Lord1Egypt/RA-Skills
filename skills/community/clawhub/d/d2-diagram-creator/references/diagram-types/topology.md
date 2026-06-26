# Service Topology

## Use Cases

- Cloud infrastructure planning
- Kubernetes cluster architecture
- Network topology design
- Resource dependency relationships

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Container Grouping | `{}` | Group by environment or type |
| Dashed Connection | `style.stroke-dash: 3` | Optional or indirect relationships |
| Database | `shape: cylinder` | Data storage |
| Cloud Service | `shape: cloud` | External services |

## Kubernetes Cluster Example

```d2
direction: right

Ingress Controller: {
  Nginx: { shape: rectangle }
}

Service Mesh: {
  API Service: {
    direction: down
    Pod1
    Pod2
    Pod3
  }
  User Service: {
    direction: down
    Pod1
    Pod2
  }
  Order Service: {
    direction: down
    Pod1
    Pod2
  }
}

Data Storage: {
  Redis Cluster: { shape: cylinder }
  PostgreSQL: { shape: cylinder }
}

Monitoring: {
  Prometheus
  Grafana
}

External Traffic -> Ingress Controller.Nginx
Ingress Controller.Nginx -> Service Mesh.API Service
Service Mesh.API Service -> Service Mesh.User Service
Service Mesh.API Service -> Service Mesh.Order Service
Service Mesh.User Service -> Data Storage.Redis Cluster
Service Mesh.Order Service -> Data Storage.PostgreSQL
Service Mesh -> Prometheus: Metrics
Prometheus -> Grafana
```

## Cloud Infrastructure Example

```d2
direction: right

VPC: {
  Public Subnet: {
    Load Balancer: { shape: rectangle }
    NAT Gateway: { shape: rectangle }
  }

  Private Subnet: {
    Web Servers: {
      direction: down
      Instance1
      Instance2
    }
    App Servers: {
      direction: down
      Instance1
      Instance2
      Instance3
    }
  }

  Data Subnet: {
    Primary DB: { shape: cylinder }
    Replica DB: { shape: cylinder }
  }
}

External Services: {
  CDN: { shape: cloud }
  Monitoring Service: { shape: cloud }
}

User Traffic -> CDN
CDN -> VPC.Public Subnet.Load Balancer
Load Balancer -> Private Subnet.Web Servers
Web Servers -> Private Subnet.App Servers
App Servers -> Data Subnet.Primary DB
Primary DB -> Data Subnet.Replica DB: Replication
Private Subnet.App Servers -> NAT Gateway
NAT Gateway -> External Services.Monitoring Service
```

## Network Topology Example

```d2
direction: right

Internet: { shape: cloud }

DMZ Zone: {
  Firewall
  Web Server
}

Internal Zone: {
  App Server
  DB Server: { shape: cylinder }
}

Management Zone: {
  Monitoring Server
  Log Server
}

Internet -> DMZ Zone.Firewall
DMZ Zone.Firewall -> DMZ Zone.Web Server
DMZ Zone.Web Server -> Internal Zone.App Server
Internal Zone.App Server -> Internal Zone.DB Server
DMZ Zone.Web Server -> Management Zone.Monitoring Server: Logs
Internal Zone.App Server -> Management Zone.Log Server
```

## Design Principles

1. **Group by Environment** - Use containers to distinguish production/test/development environments
2. **Label Dependencies** - Annotate protocols and purposes on connection lines
3. **Dashed for Optional** - Use dashed lines for non-essential connections
4. **Use Icons Wisely** - Use icons for cloud services to enhance recognition

## Class Style Reuse

Unify styles for the same type of resources:

```d2
class: server
server: {
  style.fill: "#e3f2fd"
  style.stroke: "#1976d2"
}

Web Server: {
  class: server
}
App Server: {
  class: server
}
```
