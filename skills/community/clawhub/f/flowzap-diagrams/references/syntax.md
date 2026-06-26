# FlowZap Code — Full DSL Specification

This reference contains the complete FlowZap Code syntax rules and advanced
multi-lane examples. Read this file when you need detailed syntax guidance
beyond the quick reference in SKILL.md.

## Table of Contents

- [Node definitions](#node-definitions)
- [Edge definitions](#edge-definitions)
- [Lanes](#lanes)
- [Cross-lane edges](#cross-lane-edges)
- [Loops](#loops)
- [Taskbox shape](#taskbox-shape)
- [Advanced example — multi-lane authentication flow](#advanced-example--multi-lane-authentication-flow)

## Node definitions

Nodes are declared inside a lane block. Each node has a globally unique ID
(`n1`, `n2`, …), a shape, and at least a `label` attribute.

```
n1: circle label:"Start"
n2: rectangle label:"Process Order"
n3: diamond label:"Approved?"
n4: taskbox label:"Review" owner:"Alice" description:"Check docs" system:"CRM"
```

**Rules:**
- IDs must be sequential with no gaps: `n1`, `n2`, `n3` (not `n1`, `n3`)
- IDs are globally unique across all lanes
- Attributes use **colon** syntax: `label:"Text"` (never `label="Text"`)
- Only 4 shapes: `circle`, `rectangle`, `diamond`, `taskbox`
- Labels should be max 50 characters (longer triggers a warning)

## Edge definitions

Edges connect nodes via handles. Every edge must specify source and target
handles with a direction.

```
n1.handle(right) -> n2.handle(left)
n2.handle(right) -> n3.handle(left) [label="Submit"]
```

**Rules:**
- Handle directions: `left`, `right`, `top`, `bottom`
- Edge labels use **equals inside brackets**: `[label="Text"]` (never `[label:"Text"]`)
- Prefer horizontal flow: `handle(right) -> handle(left)`
- Use `top`/`bottom` for cross-lane hops

## Lanes

Lanes group related nodes. Each lane has an identifier and an optional display
label as a comment on the same line as the opening brace.

```
OrderService { # Order Service
n1: circle label:"Start"
n2: rectangle label:"Create Order"
n1.handle(right) -> n2.handle(left)
}
```

**Rules:**
- Lane identifier: no spaces, used in cross-lane references
- Display label: `# Label Text` on the same line as `{`
- No nested lanes
- No emojis in labels or lane names

## Cross-lane edges

To connect a node in one lane to a node in another lane, prefix the target
with the lane identifier.

```
Frontend { # Frontend
n1: rectangle label:"Submit Form"
n1.handle(bottom) -> API.n2.handle(top) [label="POST /orders"]
}

API { # API Server
n2: rectangle label:"Process Request"
n3: rectangle label:"Return Response"
n2.handle(right) -> n3.handle(left)
n3.handle(top) -> Frontend.n1.handle(bottom) [label="Response: 200 OK"]
}
```

**Rules:**
- Format: `LaneName.nX.handle(direction)`
- The lane prefix must match the lane identifier exactly (case-sensitive)
- Cross-lane edges typically use `top`/`bottom` handles

## Loops

Loops define a repeating section within a lane. They are declared flat (not
nested) inside the lane block.

```
Processor { # Processor
n1: rectangle label:"Fetch Item"
n2: rectangle label:"Validate"
n3: diamond label:"Valid?"
loop [retry until all items processed] n1 n2 n3
}
```

**Rules:**
- Syntax: `loop [condition text] n1 n2 n3`
- Must be inside a lane's braces
- Lists the node IDs that participate in the loop
- Cannot be nested

## Taskbox shape

Taskboxes are specialized nodes for assigned tasks. Only use when the user
explicitly requests task assignment.

```
n5: taskbox label:"Review PR" owner:"Dev Team" description:"Check code quality" system:"GitHub"
```

**Properties:** `label`, `owner`, `description`, `system` — all use colon syntax.

## Advanced example — multi-lane authentication flow

This example demonstrates cross-lane communication, decision branching, loops,
and error handling across three participants.

```
User { # User
n1: circle label:"Start"
n2: rectangle label:"Enter username and password"
n3: rectangle label:"Submit form"
n4: rectangle label:"Receive confirmation"
n5: circle label:"Access granted"
n1.handle(right) -> n2.handle(left)
n2.handle(right) -> n3.handle(left)
n3.handle(bottom) -> Application.n6.handle(top) [label="Send credentials"]
n4.handle(right) -> n5.handle(left)
loop [retry until valid format] n2 n3 n7 n8
}

Application { # Application
n6: rectangle label:"Receive request"
n7: rectangle label:"Validate format"
n8: diamond label:"Valid format?"
n9: rectangle label:"Forward to server"
n14: rectangle label:"Forward confirmation to client"
n6.handle(right) -> n7.handle(left)
n7.handle(right) -> n8.handle(left)
n8.handle(right) -> n9.handle(left) [label="Yes"]
n9.handle(bottom) -> Server.n10.handle(top) [label="Authenticate"]
n8.handle(top) -> User.n2.handle(bottom) [label="No - Error"]
n14.handle(top) -> User.n4.handle(bottom) [label="Success"]
}

Server { # Server
n10: rectangle label:"Check database"
n11: diamond label:"Valid credentials?"
n12: rectangle label:"Generate session token"
n13: rectangle label:"Return error"
n10.handle(right) -> n11.handle(left)
n11.handle(right) -> n12.handle(left) [label="Yes"]
n11.handle(bottom) -> n13.handle(bottom) [label="No"]
n12.handle(top) -> Application.n14.handle(bottom) [label="Token"]
n13.handle(top) -> Application.n6.handle(bottom) [label="Error 401"]
}
```

### What this example demonstrates

- **3 lanes**: User, Application, Server — each with distinct responsibilities
- **Cross-lane edges**: `n3 → Application.n6`, `n9 → Server.n10`, responses back up
- **Decision diamonds**: `n8` (format check), `n11` (credential check)
- **Error paths**: Invalid format loops back to User, invalid credentials return 401
- **Loop**: Retry cycle on `n2 n3 n7 n8` until format is valid
- **Sequential IDs**: `n1` through `n14`, no gaps, globally unique
