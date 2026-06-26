# D365 F&O Security

## XDS (Extensible Data Security)

**Purpose:** Row-level security policies that filter what data a role/user can see.

### Policy structure:
- **Entity**: The data entity or table to secure
- **Constraint**: A query that defines which rows are accessible
- **Operation**: Create, Read, Update, Delete, or All
- **Context**: Role, User, or Organization

### Example — Sales order by customer group:
Query constraint: `SalesTable.CustGroup == "DOMESTIC"`
This shows only domestic sales orders.

### Common patterns:
- **Organization-based**: Filter by legal entity
- **Role-based**: Different access for Sales vs. Finance roles
- **User-based**: `CurrentUserId` in constraint query
- **Date-based**: Only current/active records visible

### Implementation:
1. Go to System administration → Security → Extensible data security policies
2. Create new policy → Select entity → Define constraint
3. Assign to roles

## Record Level Security

Similar to XDS but applied at individual record level per user.

## Duties & Privileges

**Duty**: A collection of privileges (e.g., Maintain customers)
**Privilege**: Access to a specific entry point (menu item, service operation)

### Security hierarchy:
Role → Duties → Privileges → Entry Points (Menu items, Service ops, Tables)

### Security for integrations:
- OData entities require `Read` privilege on the service operation
- Custom services require `Invoke` privilege on the service operation
- DMF requires `DMFAdministration` or `DMFOperations` duty

### Best practices:
- Never assign privileges directly to users — always through roles
- Use XDS over custom code for data filtering (maintainable, no code change)
- Test with a non-admin account before deploying security changes
