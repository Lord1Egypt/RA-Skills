# State Machine

## Use Cases

- Object state transitions
- Workflow state management
- Lifecycle diagrams
- Business process states

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| State Node | `shape: circle` or rectangle | Represents state |
| Transition Arrow | `->` with label | State change |
| Initial State | Style distinction | Starting state |
| Final State | Style distinction | Ending state |

## Basic Example

```d2
direction: right

Pending -> Processing: "Start processing"
Processing -> Completed: "Success"
Processing -> Cancelled: "Failed"
```

## Order State Machine

```d2
direction: right

Awaiting Payment: {
  style.stroke-width: 3
}
Paid
Processing
Shipped
Completed: {
  style.stroke-width: 3
}
Cancelled: {
  style.stroke-width: 3
}
Refunding
Refunded: {
  style.stroke-width: 3
}

Awaiting Payment -> Paid: "Payment success"
Awaiting Payment -> Cancelled: "Timeout/Cancel"
Paid -> Processing: "Confirm order"
Processing -> Shipped: "Warehouse ships"
Shipped -> Completed: "Confirm receipt"
Paid -> Cancelled: "User cancel"
Processing -> Cancelled: "Cancel order"
Shipped -> Refunding: "Request refund"
Refunding -> Refunded: "Refund complete"
Completed -> Refunding: "After-sale request"
```

## User Session State Machine

```d2
direction: right

Not Logged In: {
  style.stroke-width: 3
}
Logging In
Logged In
Session Expired
Locked
Logged Out

Not Logged In -> Logging In: "Submit credentials"
Logging In -> Logged In: "Auth success"
Logging In -> Locked: "Multiple failures"
Logging In -> Not Logged In: "Auth failed"
Logged In -> Session Expired: "Timeout"
Logged In -> Logged Out: "Active logout"
Session Expired -> Not Logged In: "Re-login"
Logged Out -> Not Logged In
Locked -> Not Logged In: "Admin unlock"
```

## Styled State Machine

Use colors to distinguish state types:

```d2
direction: right

# Initial state - Green
Initial State: {
  shape: circle
  style.fill: "#c8e6c9"
  style.stroke: "#2e7d32"
}

# Intermediate state - Blue
Processing: {
  style.fill: "#bbdefb"
}

# Final state - Red
Final State: {
  shape: circle
  style.fill: "#ffcdd2"
  style.stroke: "#c62828"
}

Initial State -> Processing: "Event A"
Processing -> Final State: "Event B"
```

## Bidirectional State Toggle

```d2
direction: right

On <-> Off: "Toggle"

# Or use two one-way arrows
# On -> Off: "Turn off"
# Off -> On: "Turn on"
```

## Design Principles

1. **Label Transitions Clearly** - Every transition arrow should have a trigger condition
2. **Distinguish State Types** - Use styles to differentiate initial/final states
3. **Avoid Over-complexity** - Consider splitting if more than 10 states
4. **Horizontal Layout** - `direction: right` usually works better
