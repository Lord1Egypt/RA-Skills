# Backend Stacks

Patterns and defaults for the major backend runtimes.

## Choosing a backend

| If you need... | Pick |
|---|---|
| Fast iteration, same-repo as Next.js, moderate load | **Next.js route handlers / API routes** |
| Standalone Node service, serious throughput | **Fastify** or **NestJS** |
| Python ecosystem (ML, data, scientific) | **FastAPI** |
| Full-featured framework with ORM and admin | **Django** or **Ruby on Rails** |
| High concurrency, low memory, strict typing | **Go** (stdlib + chi or Gin) |
| Maximum performance, strong type safety | **Rust** (axum or actix-web) |
| Real-time / WebSocket-heavy | Node with Socket.IO, or Elixir/Phoenix for truly massive scale |

Default: **Next.js route handlers** for small/medium apps (frontend + backend in one repo), **Fastify** or **FastAPI** for standalone services.

## Universal backend principles

- **Input validation at the boundary.** Every request body, query param, and path param gets validated before it touches your business logic. Use Zod (Node/TS), Pydantic (Python), or struct tags + validator (Go).
- **Structured errors.** Return JSON like `{"error": {"code": "USER_NOT_FOUND", "message": "..."}}`. Never leak stack traces or raw DB errors to clients.
- **Don't put business logic in the route handler.** Route handler parses input → calls a service function → formats the response. The service is what you unit-test.
- **Database connection pooling.** Instantiate the pool once; never `new Client()` per request.
- **Transactions around multi-step writes.** Partial writes cause data corruption nightmares.
- **Idempotency for destructive or billable operations.** Use idempotency keys on payment creation, emails, etc.
- **Rate limiting** on auth endpoints at minimum. `express-rate-limit`, `@fastify/rate-limit`, `slowapi` for FastAPI, or a reverse proxy (Cloudflare, nginx).
- **CORS** configured explicitly. Default-deny, allow specific origins.
- **Secrets via environment variables**, loaded through a validated config module. The config module crashes the app on missing secrets — no silent fallbacks.

## Node.js — Fastify (recommended for standalone)

### Why Fastify over Express
- 2–3× faster under load
- Native schema validation (no extra middleware)
- Better TypeScript support
- Plugin-based architecture that scales to large codebases
- Active maintenance

Express is fine for legacy reasons but don't start new projects with it in 2026.

### Project structure
```
src/
  server.ts              # Fastify instance, register plugins
  config.ts              # env var validation (Zod)
  plugins/               # auth, DB, rate limiting
  modules/
    users/
      users.routes.ts    # HTTP layer
      users.service.ts   # business logic
      users.repo.ts      # DB access
      users.schema.ts    # Zod schemas
      users.test.ts
    orders/
      ...
  lib/
    db.ts                # Prisma or Drizzle client singleton
    logger.ts            # pino instance
```

### Example route (Fastify + Zod + Prisma)
```ts
// users.routes.ts
import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';
import { createUser } from './users.service';

const CreateUserBody = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export const usersRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.post('/users', async (req, reply) => {
    const body = CreateUserBody.parse(req.body);
    const user = await createUser(body);
    return reply.code(201).send(user);
  });
};
```

### Logging
Use `pino` (comes with Fastify). Log structured JSON. Include request ID, user ID, timing.

## Node.js — NestJS

Pick NestJS when:
- Team has Angular / strong OOP background
- App is large and benefits from opinionated module structure
- You want DI out of the box

Don't pick NestJS for a small app — the overhead doesn't pay off until the codebase is large.

## Python — FastAPI (recommended for Python)

### Why FastAPI
- Async-first, fast under load
- Pydantic for validation — best-in-class
- Automatic OpenAPI docs
- Type hints throughout

### Project structure
```
app/
  main.py                # FastAPI app, router registration
  config.py              # pydantic-settings
  db.py                  # SQLAlchemy engine + session
  deps.py                # FastAPI dependencies (auth, DB session)
  modules/
    users/
      router.py
      service.py
      schemas.py         # Pydantic models
      models.py          # SQLAlchemy models
      repo.py
  middleware/
  tests/
pyproject.toml           # use Poetry or uv
```

### Example endpoint
```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from .service import create_user
from ..deps import get_db

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    email: EmailStr
    name: str

@router.post("", status_code=201)
def create(body: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, body)
```

### Testing
`pytest` + `httpx.AsyncClient` for integration tests. Use an in-memory SQLite or a dedicated test Postgres.

## Python — Django

Pick Django when:
- Content-heavy app with lots of CRUD
- You want an admin interface for free
- Team is Python-first and already knows Django

Don't pick Django if you need async performance or the app is primarily an API — FastAPI is a better fit.

## Go

### Why Go
- Best-in-class concurrency (goroutines)
- Low memory footprint
- Fast compile, fast startup
- Great for services that scale horizontally

### Project structure
```
cmd/
  server/main.go
internal/
  users/
    handler.go
    service.go
    repo.go
    model.go
  config/
  db/
  middleware/
pkg/                    # only for code you'd actually share
go.mod
```

Use `chi` (idiomatic, small) or `Gin` (familiar to Express users). Skip the debates — both are fine.

Use `sqlc` to generate type-safe Go from SQL. It's better than any ORM for Go.

### Testing
Go's built-in `testing` package. Table-driven tests. `testify` for nicer assertions if the team likes it.

## API layering pattern (all languages)

```
┌────────────────────────────┐
│  HTTP layer (routes/       │  parse input, auth check, call service
│  handlers/controllers)     │
├────────────────────────────┤
│  Service layer             │  business logic, orchestration
│                            │  <-- this is what you unit test
├────────────────────────────┤
│  Repository / data layer   │  DB access, external API calls
└────────────────────────────┘
```

This separation becomes worth it around 5–10 endpoints. Below that, keeping everything in the route handler is fine.

## Background jobs & async work

If the user's app needs to send emails, process images, call slow third-party APIs, or do anything that shouldn't block an HTTP request:

- **Small Node apps**: [BullMQ](https://bullmq.io) (Redis-backed) is the default.
- **Python**: [Celery](https://docs.celeryq.dev) with Redis or RabbitMQ; [RQ](https://python-rq.org) is simpler and often enough.
- **Go**: [asynq](https://github.com/hibiken/asynq) or [River](https://riverqueue.com) (Postgres-backed — no extra infra).
- **Postgres-first**: [pg-boss](https://github.com/timgit/pg-boss) (Node) or River (Go). If you're already on Postgres and don't have heavy volume, skipping Redis is a real simplification.
- **Serverless**: cloud-native (AWS SQS + Lambda, GCP Pub/Sub + Cloud Functions, Inngest, Trigger.dev).

Never send emails, hit Stripe, or do anything slow inside the HTTP request handler. Queue the work, return fast, let the job system handle retries.

## Real-time / WebSockets

- **Simple broadcast / rooms**: Socket.IO (Node), or native WebSocket with a thin wrapper.
- **Scalable pub/sub**: Redis pub/sub adapter for Socket.IO, or a dedicated service (Pusher, Ably, Supabase Realtime).
- **Truly massive concurrent connections**: Elixir/Phoenix — the BEAM VM is built for this.

Server-Sent Events (SSE) is underrated. If you only need server → client push (notifications, streaming AI responses, live updates), SSE is simpler than WebSocket and works through proxies that mangle WS.

## Common mistakes to avoid

- **N+1 queries.** Load related data with `include` / `join` / eager loading, not in a loop.
- **Sync work inside request handlers.** Emails, image processing, third-party calls → background jobs.
- **No timeouts on outbound calls.** Always set a timeout on `fetch` / `httpx` / HTTP clients, or one hanging call will exhaust your connection pool.
- **Trusting the frontend.** Re-validate permissions on every write. "The UI doesn't let them do X" is not access control.
- **Logging secrets.** Scrub tokens, passwords, card numbers from logs. Use a logger middleware that redacts known sensitive fields.
