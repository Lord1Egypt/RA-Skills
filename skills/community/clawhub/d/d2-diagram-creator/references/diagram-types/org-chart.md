# Organization Chart

## Use Cases

- Company organizational structure
- Team composition display
- Reporting relationships
- Department structure diagrams

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Person Node | `shape: person` | Employees, roles |
| Department Container | `{}` nested | Organizational units |
| Hierarchical Relationship | `->` connection | Reporting, management relationships |

## Basic Example

```d2
direction: down

CEO: { shape: person }

Tech Department: {
  CTO: { shape: person }
  Frontend Team: {
    Frontend Lead: { shape: person }
    Frontend Engineer: { shape: person }
  }
  Backend Team: {
    Backend Lead: { shape: person }
    Backend Engineer: { shape: person }
  }
}

Marketing Department: {
  Marketing Director: { shape: person }
  Marketing Specialist: { shape: person }
}

CEO -> CTO
CEO -> Marketing Director
CTO -> Frontend Team.Frontend Lead
CTO -> Backend Team.Backend Lead
```

## Complete Company Organization Structure

```d2
direction: down

Board: {
  Chairman
}

Executive Team: {
  CEO
  CFO
  CTO
}

Tech Department: {
  Frontend Team: {
    direction: right
    Frontend Lead
    Frontend Engineer1: { shape: person }
    Frontend Engineer2: { shape: person }
  }
  Backend Team: {
    direction: right
    Backend Lead
    Backend Engineer1: { shape: person }
    Backend Engineer2: { shape: person }
  }
  DevOps Team: {
    direction: right
    DevOps Lead
    DevOps Engineer: { shape: person }
  }
}

Business Department: {
  Product Manager: { shape: person }
  Operations Team: {
    direction: right
    Operations Lead
    Operations Specialist: { shape: person }
  }
}

Finance Department: {
  Finance Lead
  Accountant: { shape: person }
  Cashier: { shape: person }
}

Board -> CEO: "Appoint"
CEO -> CFO
CEO -> CTO
CTO -> Tech Department
CEO -> Business Department
CFO -> Finance Department
```

## Design Principles

1. **Vertical Layout Preferred** - `direction: down` works best
2. **Container Nesting** - Use containers to represent department hierarchy
3. **Person Shape** - Use `shape: person` to identify person nodes
4. **Clear Role Labels** - Include position information in node names

## Team Internal Layout

Members within the same team can use horizontal layout:

```d2
Frontend Team: {
  direction: right
  Frontend Lead
  Frontend Engineer1: { shape: person }
  Frontend Engineer2: { shape: person }
}
```
