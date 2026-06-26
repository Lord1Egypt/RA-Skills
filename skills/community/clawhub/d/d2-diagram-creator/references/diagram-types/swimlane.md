# Swimlane Diagram

## Use Cases

- Cross-functional processes
- Multi-role workflows
- Inter-departmental collaboration
- Approval workflows

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Swimlane Container | `{}` | One container per role/department |
| Cross-lane Connection | `RoleA.Node -> RoleB.Node` | Cross-role interaction |
| Decision Node | `shape: diamond` | Branch decisions |

## Basic Example

```d2
direction: right

User: {
  Submit Request
  View Result
}

System: {
  Validate Request
  Process Data
}

User.Submit Request -> System.Validate Request
System.Validate Request -> System.Process Data
System.Process Data -> User.View Result
```

## E-commerce Order Processing Swimlane

```d2
direction: right

Customer: {
  Place Order
  Pay for Order
  Confirm Receipt
  Request Refund
}

Order System: {
  Validate Order
  Create Payment
  Update Inventory
  Generate Shipment
  Process Refund
}

Warehouse: {
  Pick Items
  Pack Items
  Ship Order
}

Logistics: {
  Transport
  Deliver
}

Finance System: {
  Confirm Payment
  Process Refund
}

Customer.Place Order -> Order System.Validate Order
Order System.Validate Order -> Order System.Create Payment
Order System.Create Payment -> Customer.Pay for Order
Customer.Pay for Order -> Finance System.Confirm Payment
Finance System.Confirm Payment -> Order System.Update Inventory
Order System.Update Inventory -> Order System.Generate Shipment
Order System.Generate Shipment -> Warehouse.Pick Items
Warehouse.Pick Items -> Warehouse.Pack Items
Warehouse.Pack Items -> Warehouse.Ship Order
Warehouse.Ship Order -> Logistics.Transport
Logistics.Transport -> Logistics.Deliver
Logistics.Deliver -> Customer.Confirm Receipt
Customer.Request Refund -> Order System.Process Refund
Order System.Process Refund -> Finance System.Process Refund
```

## Approval Workflow Swimlane

```d2
direction: right

Applicant: {
  Submit Application
  Provide Additional Info
  Receive Result
}

Department Manager: {
  Initial Review
  Approve: { shape: diamond }
  Reject
}

Finance Department: {
  Verify Amount
  Confirm Budget: { shape: diamond }
}

CEO: {
  Final Review
  Final Approval: { shape: diamond }
}

Applicant.Submit Application -> Department Manager.Initial Review
Department Manager.Initial Review -> Department Manager.Approve
Department Manager.Approve -> Department Manager.Reject: "Not approved"
Department Manager.Approve -> Finance Department.Verify Amount: "Approved"
Department Manager.Reject -> Applicant.Provide Additional Info
Applicant.Provide Additional Info -> Department Manager.Initial Review
Finance Department.Verify Amount -> Finance Department.Confirm Budget
Finance Department.Confirm Budget -> CEO.Final Review: "Over budget"
Finance Department.Confirm Budget -> Applicant.Receive Result: "Within budget"
CEO.Final Review -> CEO.Final Approval
CEO.Final Approval -> Applicant.Receive Result: "Approved"
CEO.Final Approval -> Applicant.Receive Result: "Rejected"
```

## Design Principles

1. **Clear Roles** - Each swimlane represents a role or department
2. **Horizontal Layout** - `direction: right` suits most swimlane diagrams
3. **Cross-lane Connections** - Use full paths `Role.Node`
4. **Concise Naming** - Keep swimlane names short and clear

## Vertical Swimlanes

Vertical layout may be more suitable in some scenarios:

```d2
direction: down

Frontend: {
  Page Render
  User Interaction
}

Backend: {
  API Processing
  Data Query
}

Frontend.Page Render -> Backend.API Processing
Backend.API Processing -> Backend.Data Query
Backend.Data Query -> Frontend.User Interaction
```
