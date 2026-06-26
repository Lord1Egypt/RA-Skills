# Sequence Diagram

## Use Cases

- Time-based interaction flows
- API call sequences
- Protocol flows
- Message passing

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Sequence Diagram Shape | `shape: sequence_diagram` | Top-level declaration |
| Participant | Node declaration | Interacting roles/systems |
| Message | `->` or `<-` | Call direction |
| Phase Grouping | Container `{}` | Logical grouping |

## Basic Example

```d2
shape: sequence_diagram

Client
Server
Database

Client -> Server: Request data
Server -> Database: Query
Database <- Server: Return result
Client <- Server: Response data
```

## User Login Sequence

```d2
shape: sequence_diagram

User Browser
Backend Service
Auth Service
Database
Cache Service

Login Request: {
  User Browser -> Backend Service: POST /login {username, password}
  Backend Service -> Cache Service: Check login limit
  Cache Service <- Backend Service: Return limit status
  Backend Service -> Auth Service: Verify credentials
  Auth Service -> Database: Query user info
  Database <- Auth Service: Return user data
  Auth Service <- Backend Service: Verification result
  Backend Service -> Cache Service: Store session
  Cache Service <- Backend Service: Store success
  User Browser <- Backend Service: Return JWT Token
}

Subsequent Request: {
  User Browser -> Backend Service: GET /api/resource {Authorization: Bearer}
  Backend Service -> Cache Service: Validate session
  Cache Service <- Backend Service: Session valid
  User Browser <- Backend Service: Return resource data
}
```

## Payment Flow Sequence

```d2
shape: sequence_diagram

User
Merchant System
Payment Platform
Bank System
Notification Service

Create Order: {
  User -> Merchant System: Place order
  Merchant System -> Payment Platform: Create payment order
  Merchant System <- Payment Platform: Return payment link
  User <- Merchant System: Redirect to payment page
}

User Payment: {
  User -> Payment Platform: Enter payment password
  Payment Platform -> Bank System: Deduct request
  Bank System <- Payment Platform: Deduction success
  User <- Payment Platform: Payment success page
}

Async Notification: {
  Payment Platform -> Notification Service: Payment result notification
  Notification Service -> Merchant System: Webhook callback
  Merchant System <- Notification Service: Acknowledge receipt
  Notification Service <- Merchant System: Return 200 OK
}
```

## API Call Sequence

```d2
shape: sequence_diagram

Client
API Gateway
User Service
Order Service
Message Queue

Client -> API Gateway: POST /orders
API Gateway -> User Service: Validate user
User Service <- API Gateway: User valid
API Gateway -> Order Service: Create order
Order Service -> Message Queue: Send order event
Message Queue <- Order Service: Acknowledge receipt
Order Service <- API Gateway: Order created successfully
Client <- API Gateway: Return order ID
```

## Styled Sequence Diagram

```d2
shape: sequence_diagram

Client
Server

Request Phase: {
  Client -> Server: Request data
  Server -> Server: Process data {
    style.stroke: blue
  }
  Client <- Server: Return result {
    style.stroke: green
  }
}
```

## Design Principles

1. **Declare Participants at Top** - List all roles before interactions
2. **Phase Grouping** - Use containers to group related messages
3. **Consistent Direction** - `->` for requests, `<-` for responses
4. **Clear Labels** - Message labels describe specific operations

## Message Direction Explanation

- `A -> B: message` - A sends message to B (request)
- `A <- B: message` - A receives message from B (response)
- Typically use `->` for requests and `<-` for responses

## Animation Effects

Add animation to key messages:

```d2
shape: sequence_diagram

Client
Server

Client -> Server: Normal request
Server -> Client: Important response {
  style.animated: true
}
```
