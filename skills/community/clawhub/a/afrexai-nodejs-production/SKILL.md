# Node.js & TypeScript Production Engineering

Complete methodology for building production-grade Node.js backends with TypeScript. Covers architecture, frameworks, error handling, database patterns, security, testing, observability, and deployment.

---

## Quick Health Check (/16)

Run through these 8 signals — score 0 (missing) or 2 (present):

| # | Signal | Check |
|---|--------|-------|
| 1 | Strict TypeScript | `"strict": true` in tsconfig, no `any` escape hatches |
| 2 | Structured errors | Custom error classes with codes, not string throws |
| 3 | Input validation | Zod/Valibot on every external boundary |
| 4 | Database migrations | Version-controlled, reversible, CI-enforced |
| 5 | Health endpoints | `/health` (liveness) + `/ready` (readiness) with dependency checks |
| 6 | Structured logging | JSON logs with request IDs, no `console.log` in prod |
| 7 | Test coverage | >80% unit, integration tests for critical paths |
| 8 | Graceful shutdown | SIGTERM handler drains connections before exit |

**Score interpretation:** 0-6 = critical gaps, 8-10 = needs work, 12-14 = solid, 16 = production-grade.

---

## Phase 1: Architecture & Project Structure

### Framework Selection Matrix

| Framework | Best For | Throughput | Ecosystem | Learning Curve | TypeScript |
|-----------|----------|-----------|-----------|----------------|------------|
| **Hono** | Edge/serverless, lightweight APIs | ⭐⭐⭐⭐⭐ | Growing fast | Low | Native |
| **Fastify** | High-perf monoliths, JSON APIs | ⭐⭐⭐⭐⭐ | Mature | Medium | Excellent |
| **Express** | Legacy, max middleware ecosystem | ⭐⭐⭐ | Massive | Low | Via @types |
| **NestJS** | Enterprise, large teams, DI-heavy | ⭐⭐⭐⭐ | Large | High | Native |
| **Elysia** | Bun-first, type-safe APIs | ⭐⭐⭐⭐⭐ | Small | Low | Native |
| **tRPC** | Full-stack TS, type-safe RPC | N/A (layer) | Growing | Medium | Native |

**Decision rules:**
- New project, small team → **Hono** (portable, fast, minimal)
- High throughput JSON API → **Fastify** (proven, benchmarked)
- Enterprise, 10+ developers → **NestJS** (structure enforced)
- Full-stack TypeScript monorepo → **tRPC** (end-to-end types)
- Existing Express codebase → Stay on Express, migrate incrementally
- Bun runtime → **Elysia** or **Hono**

### Recommended Project Structure

```
src/
├── index.ts              # Entry point — bootstrap only
├── app.ts                # App factory (createApp)
├── config/
│   ├── env.ts            # Environment validation (Zod)
│   └── database.ts       # DB connection config
├── routes/
│   ├── index.ts          # Route registry
│   ├── users.ts          # /users routes
│   └── orders.ts         # /orders routes
├── services/
│   ├── user.service.ts   # Business logic
│   └── order.service.ts
├── repositories/
│   ├── user.repo.ts      # Data access (Drizzle/Prisma)
│   └── order.repo.ts
├── middleware/
│   ├── auth.ts           # Authentication
│   ├── validate.ts       # Request validation
│   ├── error-handler.ts  # Global error handler
│   └── request-id.ts     # Correlation ID
├── errors/
│   └── index.ts          # Custom error classes
├── types/
│   └── index.ts          # Shared types
├── utils/
│   └── index.ts          # Pure utility functions
├── jobs/                 # Background jobs/queues
│   └── email.job.ts
└── __tests__/            # Tests mirror src/ structure
    ├── services/
    └── routes/
drizzle/                  # Database migrations
├── 0001_create_users.sql
└── meta/
tsconfig.json
package.json
Dockerfile
docker-compose.yml
.env.example
```

### 7 Architecture Rules

1. **Routes → Services → Repositories** — never skip layers
2. **Services contain business logic** — routes are thin (validate + call service + respond)
3. **Repositories own data access** — services never import DB client directly
4. **No circular dependencies** — dependency flow is strictly downward
5. **One export per file** — makes imports predictable, testing easy
6. **Config validated at startup** — fail fast, not at runtime
7. **≤50 lines per function, ≤300 lines per file** — split when exceeded

---

## Phase 2: TypeScript Configuration

### Production tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "skipLibCheck": true,
    "esModuleInterop": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### 8 TypeScript Rules

1. **Never use `any`** — use `unknown` and narrow, or define proper types
2. **`noUncheckedIndexedAccess: true`** — forces null checks on array/object access
3. **Branded types for IDs** — `type UserId = string & { __brand: 'UserId' }`
4. **Zod schemas derive types** — `type User = z.infer<typeof UserSchema>`
5. **Discriminated unions for states** — `{ status: 'active'; data: T } | { status: 'error'; error: E }`
6. **`satisfies` over `as`** — preserves narrowed types: `config satisfies Config`
7. **Enums → const objects** — `const Status = { ACTIVE: 'active', INACTIVE: 'inactive' } as const`
8. **Return types on public APIs** — explicit return types on exported functions

### Branded Types Pattern

```typescript
// types/branded.ts
declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { [__brand]: B };

export type UserId = Brand<string, 'UserId'>;
export type OrderId = Brand<string, 'OrderId'>;
export type Email = Brand<string, 'Email'>;

export function UserId(id: string): UserId { return id as UserId; }
export function Email(email: string): Email {
  if (!email.includes('@')) throw new ValidationError('Invalid email');
  return email as Email;
}
```

---

## Phase 3: Environment & Configuration

### Validated Configuration with Zod

```typescript
// config/env.ts
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url().optional(),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('15m'),
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace']).default('info'),
  CORS_ORIGINS: z.string().transform(s => s.split(',')).default('*'),
  RATE_LIMIT_MAX: z.coerce.number().default(100),
  RATE_LIMIT_WINDOW_MS: z.coerce.number().default(60_000),
});

export type Env = z.infer<typeof EnvSchema>;

// Validate at import time — fail fast
const parsed = EnvSchema.safeParse(process.env);
if (!parsed.success) {
  console.error('❌ Invalid environment variables:', parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const env = parsed.data;
```

### 5 Configuration Rules

1. **Validate ALL env vars at startup** — never read `process.env` directly elsewhere
2. **Type-safe access only** — import `env` object, not `process.env`
3. **Secrets via vault/env** — never hardcoded, never committed
4. **`.env.example` always current** — document every var with description + default
5. **Different configs per environment** — use `NODE_ENV` for branching, never feature flags in env

---

## Phase 4: Error Handling Architecture

### Custom Error Hierarchy

```typescript
// errors/index.ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number,
    public readonly details?: Record<string, unknown>,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404, { resource, id });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(message, 'FORBIDDEN', 403);
  }
}

export class ConflictError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'CONFLICT', 409, details);
  }
}

export class RateLimitError extends AppError {
  constructor(retryAfterMs: number) {
    super('Too many requests', 'RATE_LIMITED', 429, { retryAfterMs });
  }
}
```

### Global Error Handler

```typescript
// middleware/error-handler.ts
import type { ErrorHandler } from 'hono';
import { AppError } from '../errors/index.js';
import { logger } from '../utils/logger.js';

export const errorHandler: ErrorHandler = (err, c) => {
  const requestId = c.get('requestId');

  if (err instanceof AppError) {
    if (err.statusCode >= 500) {
      logger.error({ err, requestId }, 'Server error');
    } else {
      logger.warn({ err, requestId }, 'Client error');
    }

    return c.json({
      error: { code: err.code, message: err.message, details: err.details },
    }, err.statusCode as any);
  }

  // Unexpected errors — don't leak internals
  logger.error({ err, requestId }, 'Unhandled error');
  return c.json({
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
  }, 500);
};
```

### 6 Error Handling Rules

1. **Throw custom errors, catch at boundary** — services throw, routes/middleware catch
2. **Never throw strings** — always `throw new SomeError(message)`
3. **Don't leak internals** — 5xx returns generic message, log the real error
4. **Include error codes** — machine-readable codes for client handling
5. **Validate early, fail fast** — Zod at route level before business logic
6. **Async errors auto-caught** — use frameworks that handle rejected promises (Hono/Fastify do this natively)

---

## Phase 5: Input Validation

### Zod Schema Patterns

```typescript
// routes/users.ts
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';

const CreateUserSchema = z.object({
  email: z.string().email().max(255).toLowerCase(),
  name: z.string().min(1).max(100).trim(),
  role: z.enum(['user', 'admin']).default('user'),
});

const PaginationSchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

const UserIdParamSchema = z.object({
  id: z.string().uuid(),
});

// Usage with Hono
app.post('/users', zValidator('json', CreateUserSchema), async (c) => {
  const body = c.req.valid('json'); // Fully typed!
  const user = await userService.create(body);
  return c.json({ data: user }, 201);
});

app.get('/users', zValidator('query', PaginationSchema), async (c) => {
  const { cursor, limit } = c.req.valid('query');
  const result = await userService.list({ cursor, limit });
  return c.json({ data: result.items, nextCursor: result.nextCursor });
});
```

### Validation Rules

1. **Validate at the edge** — every route handler validates input before calling services
2. **Schemas define the contract** — derive TypeScript types from Zod, not the other way around
3. **Transform in schemas** — `.trim()`, `.toLowerCase()`, `.default()` in Zod, not in services
4. **Reuse common schemas** — `PaginationSchema`, `DateRangeSchema`, `SortSchema`
5. **Validate path params too** — UUIDs, slugs, numeric IDs

---

## Phase 6: Database Patterns

### ORM Selection Guide

| ORM | Best For | Type Safety | Migration | Query Builder | Learning Curve |
|-----|----------|-------------|-----------|---------------|----------------|
| **Drizzle** | SQL-first, edge, performance | ⭐⭐⭐⭐⭐ | Built-in | SQL-like | Low |
| **Prisma** | Rapid dev, schema-first | ⭐⭐⭐⭐ | Built-in | Custom DSL | Low |
| **Kysely** | SQL purists, complex queries | ⭐⭐⭐⭐⭐ | External | Type-safe SQL | Medium |
| **TypeORM** | Legacy, decorator-style | ⭐⭐⭐ | Built-in | ORM-style | Medium |

**Decision:** Drizzle for new projects (matches SQL mental model, best TypeScript inference, edge-compatible).

### Drizzle Schema Example

```typescript
// drizzle/schema.ts
import { pgTable, text, timestamp, uuid, varchar, boolean, index } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  role: text('role', { enum: ['user', 'admin'] }).notNull().default('user'),
  isActive: boolean('is_active').notNull().default(true),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index('idx_users_email').on(table.email),
  index('idx_users_created').on(table.createdAt),
]);
```

### Repository Pattern

```typescript
// repositories/user.repo.ts
import { eq, desc, gt } from 'drizzle-orm';
import { db } from '../config/database.js';
import { users } from '../../drizzle/schema.js';
import type { UserId } from '../types/branded.js';
import { NotFoundError } from '../errors/index.js';

export class UserRepository {
  async findById(id: UserId) {
    const [user] = await db.select().from(users).where(eq(users.id, id)).limit(1);
    if (!user) throw new NotFoundError('User', id);
    return user;
  }

  async list(opts: { cursor?: string; limit: number }) {
    const query = db.select().from(users).orderBy(desc(users.createdAt)).limit(opts.limit + 1);
    if (opts.cursor) query.where(gt(users.id, opts.cursor));
    const rows = await query;
    const hasMore = rows.length > opts.limit;
    return { items: rows.slice(0, opts.limit), nextCursor: hasMore ? rows[opts.limit - 1].id : undefined };
  }

  async create(data: { email: string; name: string; role?: string }) {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  }

  async update(id: UserId, data: Partial<{ name: string; role: string; isActive: boolean }>) {
    const [user] = await db.update(users).set({ ...data, updatedAt: new Date() }).where(eq(users.id, id)).returning();
    if (!user) throw new NotFoundError('User', id);
    return user;
  }
}
```

### Database Rules

1. **Cursor-based pagination** — never OFFSET for user-facing lists
2. **Migrations in version control** — `drizzle-kit generate` → commit → `drizzle-kit migrate` in CI
3. **Connection pooling** — use `pg` pool (min: 2, max: 10 per process) or serverless driver for edge
4. **Transactions for multi-write** — `db.transaction(async (tx) => { ... })`
5. **Index query patterns** — add indexes for WHERE + ORDER BY columns, monitor slow queries
6. **SQLite for dev, Postgres for prod** — Drizzle supports both with same schema (use `better-sqlite3` locally)

---

## Phase 7: Authentication & Authorization

### JWT Auth Middleware (Hono)

```typescript
// middleware/auth.ts
import { jwt } from 'hono/jwt';
import { env } from '../config/env.js';
import type { UserId } from '../types/branded.js';

type JwtPayload = { sub: UserId; role: 'user' | 'admin'; iat: number; exp: number };

export const authenticate = jwt({ secret: env.JWT_SECRET });

export const requireRole = (...roles: string[]) => {
  return async (c: any, next: any) => {
    const payload = c.get('jwtPayload') as JwtPayload;
    if (!roles.includes(payload.role)) {
      throw new ForbiddenError(`Required role: ${roles.join(' or ')}`);
    }
    await next();
  };
};
```

### Security Checklist

| # | Item | Priority |
|---|------|----------|
| 1 | Helmet/security headers (CSP, HSTS, X-Frame) | P0 |
| 2 | Rate limiting per IP + per user | P0 |
| 3 | Input validation on every endpoint | P0 |
| 4 | CORS configured (not `*` in prod) | P0 |
| 5 | JWT short-lived (15m) + refresh token rotation | P0 |
| 6 | Password hashing (argon2id, cost ≥ 3) | P0 |
| 7 | SQL injection prevention (parameterized queries) | P0 |
| 8 | Request size limits (1MB default) | P1 |
| 9 | Dependency audit (`npm audit`, Snyk) | P1 |
| 10 | API key scoping (read-only, write, admin) | P1 |

---

## Phase 8: Structured Logging & Observability

### Pino Logger Setup

```typescript
// utils/logger.ts
import pino from 'pino';
import { env } from '../config/env.js';

export const logger = pino({
  level: env.LOG_LEVEL,
  ...(env.NODE_ENV === 'development' && { transport: { target: 'pino-pretty' } }),
  serializers: { err: pino.stdSerializers.err },
  redact: ['req.headers.authorization', '*.password', '*.token', '*.secret'],
  formatters: {
    level: (label) => ({ level: label }),
  },
});
```

### Request ID Middleware

```typescript
// middleware/request-id.ts
import { randomUUID } from 'node:crypto';

export const requestId = () => {
  return async (c: any, next: any) => {
    const id = c.req.header('x-request-id') || randomUUID();
    c.set('requestId', id);
    c.header('x-request-id', id);
    await next();
  };
};
```

### Request Logging Middleware

```typescript
// middleware/request-logger.ts
import { logger } from '../utils/logger.js';

export const requestLogger = () => {
  return async (c: any, next: any) => {
    const start = performance.now();
    const requestId = c.get('requestId');

    await next();

    const duration = Math.round(performance.now() - start);
    const level = c.res.status >= 500 ? 'error' : c.res.status >= 400 ? 'warn' : 'info';

    logger[level]({
      requestId,
      method: c.req.method,
      path: c.req.path,
      status: c.res.status,
      durationMs: duration,
      userAgent: c.req.header('user-agent'),
    }, `${c.req.method} ${c.req.path} ${c.res.status} ${duration}ms`);
  };
};
```

### Health Endpoints

```typescript
// routes/health.ts
app.get('/health', (c) => c.json({ status: 'ok', timestamp: new Date().toISOString() }));

app.get('/ready', async (c) => {
  const checks = {
    database: false,
    redis: false,
  };

  try {
    await db.execute(sql`SELECT 1`);
    checks.database = true;
  } catch {}

  try {
    await redis.ping();
    checks.redis = true;
  } catch {}

  const ready = Object.values(checks).every(Boolean);
  return c.json({ status: ready ? 'ready' : 'degraded', checks }, ready ? 200 : 503);
});
```

---

## Phase 9: Testing Strategy

### Test Pyramid

| Level | Coverage Target | Tools | What to Test |
|-------|----------------|-------|-------------|
| **Unit** | >80% | Vitest | Services, utils, pure logic |
| **Integration** | Critical paths | Vitest + testcontainers | Routes → DB round-trip |
| **E2E** | Happy paths | Vitest + supertest | Full HTTP request cycle |
| **Contract** | API boundaries | Vitest | Request/response shapes |

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts'],
    coverage: { provider: 'v8', reporter: ['text', 'lcov'], thresholds: { lines: 80, branches: 75 } },
    setupFiles: ['./src/__tests__/setup.ts'],
    pool: 'forks', // Isolation for DB tests
  },
});
```

### Service Unit Test Pattern

```typescript
// __tests__/services/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from '../../services/user.service.js';
import type { UserRepository } from '../../repositories/user.repo.js';

describe('UserService', () => {
  let service: UserService;
  let repo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    repo = { findById: vi.fn(), create: vi.fn(), update: vi.fn(), list: vi.fn() } as any;
    service = new UserService(repo);
  });

  it('creates user with normalized email', async () => {
    repo.create.mockResolvedValue({ id: '1', email: 'test@example.com', name: 'Test' } as any);
    const result = await service.create({ email: 'Test@Example.COM', name: 'Test' });
    expect(repo.create).toHaveBeenCalledWith(expect.objectContaining({ email: 'test@example.com' }));
    expect(result.email).toBe('test@example.com');
  });
});
```

### Integration Test Pattern

```typescript
// __tests__/routes/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createApp } from '../../app.js';
import { testDb, migrate, cleanup } from '../helpers/db.js';

describe('POST /users', () => {
  let app: any;

  beforeAll(async () => {
    await migrate(testDb);
    app = createApp({ db: testDb });
  });

  afterAll(async () => { await cleanup(testDb); });

  it('creates user and returns 201', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'new@example.com', name: 'New User' }),
    });

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.data.email).toBe('new@example.com');
  });

  it('rejects invalid email with 400', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'not-an-email', name: 'Bad' }),
    });

    expect(res.status).toBe(400);
  });
});
```

### 7 Testing Rules

1. **Test behavior, not implementation** — assert outputs, not internal method calls
2. **Each test is independent** — no shared mutable state between tests
3. **Name tests as specifications** — `it('rejects expired JWT with 401')`
4. **Fast unit tests, isolated integration tests** — use `pool: 'forks'` for DB tests
5. **Mock at boundaries** — mock repositories in service tests, real DB in integration tests
6. **Test error paths** — 400s, 404s, 409s, 500s, not just happy paths
7. **CI enforces coverage** — fail build if coverage drops below threshold

---

## Phase 10: Graceful Shutdown & Process Management

### Shutdown Handler

```typescript
// index.ts
import { serve } from '@hono/node-server';
import { createApp } from './app.js';
import { logger } from './utils/logger.js';
import { env } from './config/env.js';
import { db } from './config/database.js';

const app = createApp();
const server = serve({ fetch: app.fetch, port: env.PORT });

logger.info({ port: env.PORT }, 'Server started');

const shutdown = async (signal: string) => {
  logger.info({ signal }, 'Shutdown signal received');

  // Stop accepting new connections
  server.close(() => { logger.info('HTTP server closed'); });

  // Drain existing work (give 10s)
  const timeout = setTimeout(() => {
    logger.error('Forced shutdown after timeout');
    process.exit(1);
  }, 10_000);

  try {
    // Close DB pool, Redis, queues, etc.
    await db.$client.end();
    logger.info('Database pool closed');
    clearTimeout(timeout);
    process.exit(0);
  } catch (err) {
    logger.error({ err }, 'Error during shutdown');
    process.exit(1);
  }
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// Catch unhandled errors
process.on('unhandledRejection', (err) => {
  logger.fatal({ err }, 'Unhandled rejection');
  process.exit(1);
});
```

---

## Phase 11: Production Deployment

### Multi-Stage Dockerfile

```dockerfile
# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --ignore-scripts
COPY tsconfig.json ./
COPY src/ src/
COPY drizzle/ drizzle/
RUN npm run build
RUN npm ci --omit=dev --ignore-scripts

# Production stage
FROM node:22-alpine
RUN apk add --no-cache tini dumb-init
WORKDIR /app
COPY --from=builder /app/dist dist/
COPY --from=builder /app/drizzle drizzle/
COPY --from=builder /app/node_modules node_modules/
COPY --from=builder /app/package.json .

ENV NODE_ENV=production
USER node
EXPOSE 3000
ENTRYPOINT ["tini", "--"]
CMD ["node", "dist/index.js"]
```

### GitHub Actions CI

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_DB: test, POSTGRES_PASSWORD: test }
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
        env: { DATABASE_URL: 'postgresql://postgres:test@localhost:5432/test' }
      - run: npm run build
```

### Production Checklist

**P0 — Mandatory:**
- [ ] `NODE_ENV=production`
- [ ] Strict TypeScript (`tsc --noEmit` passes)
- [ ] All env vars validated at startup
- [ ] Health + readiness endpoints
- [ ] Graceful shutdown handles SIGTERM
- [ ] Structured JSON logging (no console.log)
- [ ] Error handler doesn't leak stack traces
- [ ] Rate limiting enabled
- [ ] CORS configured (not wildcard)
- [ ] Security headers set

**P1 — Recommended:**
- [ ] Request ID tracing through all logs
- [ ] Database connection pooling configured
- [ ] Dependency audit clean (`npm audit`)
- [ ] Docker image < 200MB
- [ ] Response compression (gzip/brotli)
- [ ] API versioning strategy decided
- [ ] Monitoring/alerting configured

---

## Phase 12: Performance Optimization

### Priority Stack

| # | Technique | Impact | Effort |
|---|-----------|--------|--------|
| 1 | Connection pooling (DB + Redis) | High | Low |
| 2 | Response caching (Redis/in-memory) | High | Medium |
| 3 | Query optimization (indexes, N+1) | High | Medium |
| 4 | JSON serialization (fast-json-stringify) | Medium | Low |
| 5 | Compression middleware | Medium | Low |
| 6 | Streaming responses for large payloads | Medium | Medium |
| 7 | Worker threads for CPU-bound work | High | High |
| 8 | HTTP/2 + keep-alive | Low | Low |

### Common Optimizations

```typescript
// N+1 prevention — batch with dataloader or SQL JOIN
// ❌ Bad: for loop with individual queries
for (const order of orders) {
  order.user = await db.query.users.findFirst({ where: eq(users.id, order.userId) });
}

// ✅ Good: single query with join
const ordersWithUsers = await db
  .select()
  .from(orders)
  .leftJoin(users, eq(orders.userId, users.id))
  .where(inArray(orders.id, orderIds));

// In-memory caching for hot data
import { LRUCache } from 'lru-cache';
const cache = new LRUCache<string, any>({ max: 1000, ttl: 60_000 });

async function getCachedUser(id: string) {
  const cached = cache.get(id);
  if (cached) return cached;
  const user = await userRepo.findById(id);
  cache.set(id, user);
  return user;
}
```

---

## Phase 13: Background Jobs & Queues

### BullMQ Pattern

```typescript
// jobs/email.job.ts
import { Queue, Worker } from 'bullmq';
import { env } from '../config/env.js';
import { logger } from '../utils/logger.js';

const connection = { url: env.REDIS_URL };

export const emailQueue = new Queue('email', { connection });

export const emailWorker = new Worker('email', async (job) => {
  const { to, subject, body } = job.data;
  logger.info({ jobId: job.id, to }, 'Sending email');
  // Send via provider
  await sendEmail({ to, subject, body });
}, {
  connection,
  concurrency: 5,
  limiter: { max: 10, duration: 1000 }, // 10 per second
});

emailWorker.on('failed', (job, err) => {
  logger.error({ jobId: job?.id, err }, 'Email job failed');
});
```

### Job Rules

1. **Idempotent jobs** — same job ID running twice produces same result
2. **Retry with backoff** — exponential backoff for transient failures
3. **Dead letter queue** — failed jobs after max retries go to DLQ for inspection
4. **Job timeout** — set `removeOnComplete` and `removeOnFail` TTLs
5. **Monitor queue health** — queue length, processing time, failure rate

---

## Phase 14: Advanced Patterns

### Dependency Injection (Manual)

```typescript
// app.ts — compose dependencies explicitly
export function createApp(deps?: { db?: Database; redis?: Redis }) {
  const database = deps?.db ?? defaultDb;
  const app = new Hono();

  // Compose service graph
  const userRepo = new UserRepository(database);
  const userService = new UserService(userRepo);

  // Mount routes with injected services
  app.route('/users', createUserRoutes(userService));

  return app;
}
```

### Rate Limiting

```typescript
// middleware/rate-limit.ts (using hono-rate-limiter)
import { rateLimiter } from 'hono-rate-limiter';

export const apiRateLimit = rateLimiter({
  windowMs: 60_000,
  limit: 100,
  keyGenerator: (c) => c.get('jwtPayload')?.sub || c.req.header('x-forwarded-for') || 'anonymous',
  message: { error: { code: 'RATE_LIMITED', message: 'Too many requests' } },
});
```

### WebSocket Pattern (Hono + @hono/node-ws)

```typescript
import { createNodeWebSocket } from '@hono/node-ws';

const { injectWebSocket, upgradeWebSocket } = createNodeWebSocket({ app });

app.get('/ws', upgradeWebSocket((c) => ({
  onOpen(evt, ws) { logger.info('WebSocket connected'); },
  onMessage(evt, ws) {
    const data = JSON.parse(evt.data.toString());
    // Handle message
    ws.send(JSON.stringify({ type: 'ack', id: data.id }));
  },
  onClose() { logger.info('WebSocket disconnected'); },
})));
```

---

## 2025+ Recommended Stack

| Layer | Recommended | Alternative |
|-------|-------------|-------------|
| **Runtime** | Node.js 22 LTS | Bun |
| **Framework** | Hono | Fastify |
| **Language** | TypeScript (strict) | — |
| **Validation** | Zod | Valibot |
| **ORM** | Drizzle | Prisma |
| **Database** | PostgreSQL | SQLite (dev) |
| **Cache** | Redis / Upstash | LRU in-memory |
| **Auth** | JWT + refresh | Lucia, Better Auth |
| **Queue** | BullMQ | pg-boss |
| **Testing** | Vitest | — |
| **Logging** | Pino | — |
| **Linting** | Biome | ESLint + Prettier |
| **CI/CD** | GitHub Actions | — |
| **Deploy** | Docker + Railway/Fly | Vercel (serverless) |

---

## 10 Commandments

1. **Validate everything at the boundary** — Zod on every route
2. **Fail fast at startup** — env vars, DB connection, migrations
3. **Structured logging everywhere** — JSON, request IDs, no console.log
4. **Custom errors with codes** — never throw strings
5. **Cursor pagination** — never OFFSET
6. **Graceful shutdown** — drain connections on SIGTERM
7. **Test error paths** — 4xx/5xx matter more than happy paths
8. **Type everything** — no `any`, branded IDs, Zod-derived types
9. **Security by default** — rate limit, helmet, CORS, audit deps
10. **Keep it simple** — 50 lines/function, 300 lines/file, flat is better than nested

---

## 10 Common Mistakes

| # | Mistake | Fix |
|---|---------|-----|
| 1 | `console.log` in production | Use Pino with JSON output |
| 2 | `any` type everywhere | `unknown` + type narrowing |
| 3 | No input validation | Zod middleware on every route |
| 4 | OFFSET pagination | Cursor-based with keyset |
| 5 | No graceful shutdown | SIGTERM handler with drain timeout |
| 6 | Hardcoded config | Zod-validated env at startup |
| 7 | Fat controllers | Thin routes → services → repositories |
| 8 | No error hierarchy | Custom AppError with codes |
| 9 | Testing only happy paths | Test 400/401/404/409/500 explicitly |
| 10 | No request tracing | Request ID middleware + propagation |

---

## Quality Scoring (0-100)

| Dimension | Weight | What to Assess |
|-----------|--------|----------------|
| Type safety | 20% | Strict TS, no `any`, branded types |
| Error handling | 15% | Custom errors, global handler, no leaks |
| Testing | 15% | Coverage >80%, integration tests, error paths |
| Security | 15% | Auth, validation, rate limiting, headers |
| Observability | 10% | Structured logging, health checks, metrics |
| Performance | 10% | Connection pooling, caching, N+1 prevention |
| Code structure | 10% | Layer separation, file size limits, DI |
| Deployment | 5% | Docker, CI/CD, graceful shutdown |

---

## Edge Cases

### Startup/MVP
- Start with Hono + SQLite (Drizzle) + Vitest — ship in hours
- Add Postgres when you need concurrent writes
- Skip Redis until you need caching or queues

### Monorepo (Turborepo/Nx)
- Shared packages: `@org/types`, `@org/db`, `@org/validation`
- Each service is its own package with independent build/test
- Use workspace protocol: `"@org/types": "workspace:*"`

### Serverless (Vercel/Cloudflare Workers)
- Hono runs everywhere — same code, different adapters
- Use serverless DB drivers (Neon, PlanetScale, Turso)
- No graceful shutdown needed — stateless by design

### Legacy Express Migration
- Add TypeScript incrementally (`.ts` files alongside `.js`)
- Wrap Express routes with Zod validation middleware
- Replace `console.log` with Pino one file at a time
- Migrate to Hono/Fastify route-by-route using adapter

---

## Natural Language Commands

- "Set up a new TypeScript API project" → Phase 1-3 (structure + config + env)
- "Add authentication to my API" → Phase 7 (JWT + RBAC)
- "Review my error handling" → Phase 4 (error hierarchy + handler)
- "Add database with Drizzle" → Phase 6 (schema + repository + migrations)
- "Set up testing" → Phase 9 (Vitest + unit + integration patterns)
- "Prepare for production deployment" → Phase 11 (Docker + CI + checklist)
- "Optimize API performance" → Phase 12 (priority stack + patterns)
- "Add background jobs" → Phase 13 (BullMQ + patterns)
- "Audit my API security" → Phase 7 security checklist
- "Set up logging and monitoring" → Phase 8 (Pino + request ID + health)
- "Review my project structure" → Phase 1 (structure + rules)
- "Full health check" → Quick Health Check + Quality Scoring

---

⚡ Built by [AfrexAI](https://afrexai-cto.github.io/context-packs/) — AI-powered business automation.
