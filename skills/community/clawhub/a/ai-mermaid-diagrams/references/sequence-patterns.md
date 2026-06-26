# Mermaid Sequence Diagram Patterns

## Basic Syntax

```
sequenceDiagram
    participant A as Label A
    participant B as Label B
    A->>B: Message
    B-->>A: Response
    Note over A,B: Note text
```

Arrow types:
- `->>`  solid arrow (request/call)
- `-->>`  dashed arrow (response/return)
- `->`  solid line no arrowhead
- `-->`  dashed line no arrowhead
- `-x`  solid with X (async/fire-and-forget)
- `--x`  dashed with X

## OAuth 2.0 / Authentication Flow
```mermaid
sequenceDiagram
    participant User as 👤 User
    participant App as Client App
    participant Auth as Auth Server
    participant API as Resource API

    User->>App: Login request
    App->>Auth: Authorization request\n(client_id, scope, redirect_uri)
    Auth->>User: Login + consent screen
    User->>Auth: Credentials + approval
    Auth-->>App: Authorization code
    App->>Auth: Token request\n(code, client_secret)
    Auth-->>App: Access token + refresh token
    App->>API: API request\n(Bearer token)
    API->>Auth: Validate token
    Auth-->>API: Token valid + claims
    API-->>App: Protected resource
    App-->>User: Display result
```

## API Request Flow
```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant Auth as Auth Service
    participant Service as Backend Service
    participant DB as Database
    participant Cache as Redis Cache

    Client->>Gateway: HTTP Request + JWT
    Gateway->>Auth: Validate token
    Auth-->>Gateway: Token valid, user claims
    Gateway->>Service: Forward request + claims
    Service->>Cache: Check cache
    alt Cache hit
        Cache-->>Service: Cached response
    else Cache miss
        Service->>DB: Query data
        DB-->>Service: Result set
        Service->>Cache: Store in cache (TTL 5m)
    end
    Service-->>Gateway: Response payload
    Gateway-->>Client: HTTP 200 + JSON
```

## AI Prompt Processing Flow (DLP/Proxy)
```mermaid
sequenceDiagram
    participant User as 👤 Employee
    participant Ext as Browser Extension
    participant DLP as DLP / Webhook Ingest
    participant AI as AI Tool (Perplexity etc.)
    participant Alert as Alert Engine

    User->>Ext: Types prompt into AI tool
    Ext->>DLP: Send prompt event\n(user, prompt, site, timestamp)
    DLP->>DLP: Classify data sensitivity
    DLP->>DLP: Match against alert rules
    alt Policy violation detected
        DLP->>Alert: Trigger alert
        DLP->>Ext: Block instruction
        Ext->>User: ⛔ Blocked message
        Alert-->>DLP: Alert logged (triage_status=new)
    else Clean prompt
        DLP->>Ext: Allow instruction
        Ext->>AI: Forward prompt
        AI-->>User: AI response
        DLP->>DLP: Log event (blocked=0)
    end
```

## CI/CD Pipeline Flow
```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as GitHub
    participant CI as CI Pipeline
    participant Reg as Container Registry
    participant Stage as Staging
    participant Prod as Production

    Dev->>Git: git push (feature branch)
    Git->>CI: Webhook trigger
    CI->>CI: Run tests
    CI->>CI: Security scan (SAST/DAST)
    alt Tests pass
        CI->>Reg: Build + push Docker image
        CI->>Stage: Deploy to staging
        Stage-->>CI: Health check OK
        CI-->>Dev: ✅ Staging deploy success
        Dev->>Git: Merge PR to main
        Git->>CI: Trigger prod pipeline
        CI->>Prod: Deploy to production
        Prod-->>CI: Health check OK
        CI-->>Dev: ✅ Production deploy success
    else Tests fail
        CI-->>Dev: ❌ Build failed — see logs
    end
```

## Database Transaction Flow
```mermaid
sequenceDiagram
    participant App as Application
    participant DB as Database
    participant Cache as Cache

    App->>DB: BEGIN TRANSACTION
    App->>DB: INSERT record
    DB-->>App: Row inserted (id=123)
    App->>DB: UPDATE related record
    DB-->>App: 1 row updated
    App->>DB: COMMIT
    DB-->>App: Transaction committed
    App->>Cache: Invalidate cache key
    Cache-->>App: Cache cleared
```

## Useful Sequence Features

### Activation bars (show when participant is processing)
```
activate ServiceA
ServiceA->>ServiceB: call
deactivate ServiceA
```

### Loops
```
loop Every 30 seconds
    Monitor->>API: Health check
    API-->>Monitor: 200 OK
end
```

### Alt/Else blocks
```
alt Success
    API-->>Client: 200 OK
else Error
    API-->>Client: 500 Error
end
```

### Notes
```
Note right of Service: Processing takes\n~200ms average
Note over Client,Server: TLS 1.3 encrypted
```
