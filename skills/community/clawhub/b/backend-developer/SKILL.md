---
name: backend-developer
description: Standardized backend REST API development following layered architecture patterns (Route → Controller → Service → Repository). Use when building new REST APIs, implementing features, fixing bugs, or refactoring backend code. Enforces strict separation of concerns, centralized error handling, input validation, DTO/mapper patterns, and Prisma ORM usage.
---

# Backend API Architecture Skill

This skill provides a standardized, production-ready architecture for Node.js/TypeScript REST APIs following the **4-layer pattern** proven across multiple production systems.

## Core Architecture

```
Client Request
  ↓
[routes/] HTTP handlers + middleware
  ↓
[controller/] Request parsing + response formatting
  ↓
[service/] Business logic + orchestration
  ↓
[repository/] Database access (Prisma)
```

Each layer has a single responsibility and clear boundaries.

## Quick Start: The Standard Stack

**Runtime:** Node.js + TypeScript  
**Framework:** Express  
**ORM:** Prisma  
**Validation:** Joi + Zod (request validation)  
**Error Handling:** Custom `AppError` class + centralized middleware  
**Response Format:** Standardized JSON with `{status, data, meta, error}`

## File Organization

Each feature gets a **feature module** with 6 files:

```
src/
├── app/
│   └── [feature]/
│       ├── [feature].route.ts      ← HTTP routes + middleware
│       ├── [feature].controller.ts ← Request → response
│       ├── [feature].service.ts    ← Business logic
│       ├── [feature].repository.ts ← Database queries
│       ├── [feature].dto.ts        ← TypeScript types
│       ├── [feature].mapper.ts     ← Entity → DTO transformation
│       └── [feature].request.ts    ← Joi/Zod validation schemas
├── config/
│   └── config.ts                   ← Environment loading
├── interface/
│   └── index.ts                    ← Global types, ERROR_CODE, ApiResponse
├── middleware/
│   ├── auth-middleware.ts
│   ├── error-handler.ts            ← Centralized error handling
│   ├── validate-request.ts
│   ├── security.middleware.ts
│   └── index.ts
├── lib/
│   └── prisma.ts                   ← Prisma client singleton
├── utils/
│   ├── response-handler.ts         ← ResponseHandler utilities
│   ├── handle-prisma-error.ts
│   └── clean-joi-error-message.ts
├── routes/
│   └── index.ts                    ← Central route aggregator
└── index.ts                        ← Express app setup
```

## The 4 Layers Explained

### 1. Route Layer (`[feature].route.ts`)

**Responsibility:** HTTP method binding, middleware ordering, parameter extraction  
**Does:** Apply auth middleware → validate input → call controller → error handling  
**Does NOT:** Business logic, database access

```typescript
export const [feature]Routes = express.Router();

[feature]Routes.post(
  '/',
  auth('ACCESS', [Roles.Admin]),          // ← Auth middleware
  validate(createSchema, 'body'),         // ← Validation middleware
  catchAsync([feature]Controller.create), // ← Error wrapping
);

[feature]Routes.get(
  '/:id',
  auth('ACCESS', [Roles.User, Roles.Admin]),
  catchAsync([feature]Controller.findById),
);
```

**Key utilities:**
- `auth(tokenType, allowedRoles)` — JWT verification
- `validate(schema, 'body'|'query'|'params')` — Input validation
- `catchAsync(fn)` — Wrapper that catches promise rejections

### 2. Controller Layer (`[feature].controller.ts`)

**Responsibility:** Extract request data, call service, format response  
**Does:** `req.body`, `req.query`, `req.params` → service call → `ResponseHandler.ok()`  
**Does NOT:** Business logic, database queries

```typescript
export const [feature]Controller = {
  create: async (req: Request, res: Response, next: NextFunction) => {
    const { body } = req;
    const result = await [feature]Service.create(body);
    
    // Service returns AppError or data
    if (result instanceof AppError) {
      next(result);
      return;
    }
    
    ResponseHandler.created(res, result, 'Created successfully');
  },
  
  findAll: async (req: Request, res: Response, next: NextFunction) => {
    const { query } = req;
    const { data, meta } = await [feature]Service.findAll(query);
    if (data instanceof AppError) {
      next(data);
      return;
    }
    ResponseHandler.ok(res, data, 'Fetched successfully', meta);
  },
};
```

**Pattern:**
1. Extract `req` data
2. Call service (which returns `AppError | data`)
3. Check for `AppError` → `next(error)`
4. Otherwise → `ResponseHandler.ok()` or `.created()`

### 3. Service Layer (`[feature].service.ts`)

**Responsibility:** Business logic, data orchestration, mapper usage  
**Does:** Calls repository → transforms data (via mappers) → returns `AppError | data`  
**Does NOT:** Direct database queries, HTTP handling

```typescript
export const [feature]Service = {
  create: async (input: CreateDto): Promise<AppError | [Feature]Dto> => {
    // Validate business rules (not input format — that's the request layer)
    const existing = await [feature]Repository.findByEmail(input.email);
    if (existing) {
      return new AppError('CONFLICT', 'Email already exists');
    }
    
    // Call repository
    const entity = await [feature]Repository.create(input);
    
    // Transform entity to DTO via mapper
    return [feature]Mapper.toDtoArray([entity])[0];
  },
  
  findAll: async (query: QueryParams) => {
    const { page = 1, perPage = 10 } = query;
    const result = await [feature]Repository.findAll(page, perPage);
    
    return {
      data: [feature]Mapper.toDtoArray(result.data),
      meta: {
        currentPage: page,
        totalPages: Math.ceil(result.count / perPage),
        perPage,
        totalEntries: result.count,
      },
    };
  },
};
```

**Pattern:**
- Accept DTOs (validated input from request layer)
- Call repository for data access
- Use mapper to transform entities → DTOs
- Return `AppError | data` (union type)

### 4. Repository Layer (`[feature].repository.ts`)

**Responsibility:** Raw database access via Prisma  
**Does:** `prisma.model.query()` — nothing else  
**Does NOT:** Business logic, data transformation

```typescript
export const [feature]Repository = {
  create: async (input: CreateDto) => {
    return prisma.[feature].create({
      data: input,
    });
  },
  
  findAll: async (page: number, perPage: number) => {
    const skip = (page - 1) * perPage;
    const [data, count] = await Promise.all([
      prisma.[feature].findMany({
        skip,
        take: perPage,
        where: { deletedAt: null }, // Soft delete filter
      }),
      prisma.[feature].count({
        where: { deletedAt: null },
      }),
    ]);
    return { data, count };
  },
};
```

**Pattern:**
- Direct Prisma calls
- No business logic
- Return raw entity objects

## DTO & Mapper Pattern

**DTO** (Data Transfer Object) — TypeScript interface defining what data leaves the system:

```typescript
// [feature].dto.ts
export interface [Feature]Dto {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}
```

**Mapper** — Transform database entity to DTO:

```typescript
// [feature].mapper.ts
export const [feature]Mapper = {
  toDto(entity: [FeatureEntity]): [Feature]Dto {
    return {
      id: entity.id,
      name: entity.name,
      email: entity.email,
      createdAt: entity.createdAt,
    };
  },
  
  toDtoArray(entities: [FeatureEntity][]): [Feature]Dto[] {
    return entities.map(e => this.toDto(e));
  },
};
```

## Error Handling

**Central error class:**

```typescript
export class AppError extends Error {
  constructor(
    public readonly code: ErrorCode, // 'BAD_REQUEST', 'UNAUTHORIZED', etc.
    message?: string,
  ) {
    super(message);
  }
}
```

**Error codes (from `interface/index.ts`):**

```typescript
export const ERROR_CODE = {
  BAD_REQUEST: { code: 'BAD_REQUEST', message: 'Bad Request', httpStatus: 400 },
  UNAUTHORIZED: { code: 'UNAUTHORIZED', message: 'Unauthorized', httpStatus: 401 },
  FORBIDDEN: { code: 'FORBIDDEN', message: 'Forbidden', httpStatus: 403 },
  NOT_FOUND: { code: 'NOT_FOUND', message: 'Not Found', httpStatus: 404 },
  CONFLICT: { code: 'CONFLICT', message: 'Resource already exists', httpStatus: 409 },
  INTERNAL_SERVER_ERROR: { code: 'INTERNAL_SERVER_ERROR', httpStatus: 500 },
  // ... extend as needed
};
```

**Centralized error handler middleware:**

```typescript
export const errorHandler: ErrorRequestHandler = (
  err: AppError | Error,
  req: Request,
  res: Response,
) => {
  if (err instanceof AppError) {
    return res.status(err.httpStatus).json({
      status: 'error',
      error: {
        code: err.code,
        message: err.message,
      },
    });
  }
  
  // Fallback for unhandled errors
  console.error(err.stack);
  res.status(500).json({
    status: 'error',
    error: { code: 'INTERNAL_SERVER_ERROR', message: 'Internal Server Error' },
  });
};
```

## Response Format

**Success response:**
```json
{
  "status": "success",
  "message": "User created successfully",
  "data": { "id": "123", "name": "John", "email": "john@example.com" },
  "meta": null
}
```

**Paginated response:**
```json
{
  "status": "success",
  "data": [{ "id": "1" }, { "id": "2" }],
  "meta": {
    "currentPage": 1,
    "totalPages": 5,
    "perPage": 10,
    "totalEntries": 42
  }
}
```

**Error response:**
```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

## Validation Pattern

**Request file defines Joi schema + TypeScript type:**

```typescript
// [feature].request.ts
import Joi from 'joi';

export const createSchema = Joi.object({
  name: Joi.string().required(),
  email: Joi.string().email().required(),
  phone: Joi.string().optional(),
});

export type CreateRequest = {
  name: string;
  email: string;
  phone?: string;
};
```

**Route uses it:**
```typescript
[feature]Routes.post(
  '/',
  validate(createSchema, 'body'), // Validates against schema
  catchAsync([feature]Controller.create),
);
```

**Controller receives typed input:**
```typescript
create: async (req: Request, res: Response) => {
  const body = req.body as CreateRequest; // Already validated + typed
  // ...
};
```

## Middleware Stack

Standard middleware order in `index.ts`:

```typescript
app.use(express.json());
app.use(cors());
app.use(securityHeaders());
app.use(requestLogger());

app.use('/api', routes);

app.use(errorHandler); // Must be last
```

## Authentication Pattern

JWT middleware extracts and verifies token:

```typescript
export const auth = (tokenType: 'ACCESS' | 'REFRESH', roles?: Role[]) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return next(new AppError('UNAUTHORIZED'));
    }
    
    try {
      const payload = jwt.verify(token, process.env.JWT_SECRET!);
      if (roles && !roles.includes(payload.role)) {
        return next(new AppError('FORBIDDEN'));
      }
      (req as any).user = payload;
      next();
    } catch {
      next(new AppError('UNAUTHORIZED'));
    }
  };
};
```

## Key Utilities

See `references/utilities.md` for helper functions:
- `catchAsync(fn)` — Promise error wrapper
- `ResponseHandler` — Response formatting
- `validate(schema, field)` — Request validation middleware
- `handlePrismaError(err)` — Convert Prisma errors to AppError

## When Implementing Features

1. **Define request schema** — `[feature].request.ts`
2. **Define DTOs** — `[feature].dto.ts`
3. **Create repository** — `[feature].repository.ts` (Prisma queries only)
4. **Create service** — `[feature].service.ts` (business logic)
5. **Create controller** — `[feature].controller.ts` (request/response)
6. **Create mapper** — `[feature].mapper.ts` (entity → DTO)
7. **Create routes** — `[feature].route.ts` (HTTP endpoints)
8. **Register routes** — Add to `routes/index.ts`

## Checklist Before Merge

- [ ] All layers follow the pattern (route → controller → service → repository)
- [ ] Service returns `AppError | data` (union type)
- [ ] Controller checks for `AppError` before responding
- [ ] Validation happens in request layer, not service
- [ ] DTOs defined, mappers used for entity transformation
- [ ] Error codes added to `ERROR_CODE` if new errors introduced
- [ ] Prisma queries in repository layer only
- [ ] Business logic in service layer only
- [ ] No database access in controller
- [ ] Response uses `ResponseHandler`
- [ ] Auth middleware applied where needed
- [ ] Tests written for service layer (unit tests easy to write with pure functions)

## References

- See `references/senior-engineer-mindset.md` — **READ THIS FIRST** — Thinking patterns, API design, security, performance, code quality standards
- See `references/error-handling.md` — Error patterns and Prisma error conversion
- See `references/validation.md` — Joi + Zod usage
- See `references/utilities.md` — Helper functions explained
- See `assets/templates/` — Boilerplate code samples

## Senior Engineer Standard

Before implementing anything, read `references/senior-engineer-mindset.md`. It defines the quality bar expected of every implementation:

- **REST API design:** correct status codes, resource naming, nesting rules
- **Data modeling:** audit fields, soft delete, naming conventions
- **Error philosophy:** explicit errors, meaningful messages, no swallowing
- **Performance:** no N+1, always paginate, parallel queries, select only needed fields
- **Security:** validate everything, never expose sensitive data, service-level authorization
- **Code quality:** early return, no magic values, explicit naming, short focused functions

An implementation that passes functionality but violates these principles is **not complete**.
