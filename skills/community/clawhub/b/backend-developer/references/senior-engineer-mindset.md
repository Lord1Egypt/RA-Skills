# Senior Backend Engineer Mindset

This reference defines how an expert senior backend engineer thinks and acts. Agents must internalize these principles — not just follow patterns mechanically.

---

## 1. Think Before You Code

**Ask these questions before touching a file:**

- What is the *actual* problem? Not the symptom.
- Who calls this? What are their expectations?
- What happens if this fails? Is it recoverable?
- Does this already exist somewhere? Don't duplicate.
- Will this be easy to change later?

**Red flags that signal incomplete understanding:**
- "I'll just add a field here"
- "I'll handle that edge case later"
- "This is a quick fix"

If you don't understand the business intent, **ask first. Code second.**

---

## 2. API Design Principles

### RESTful Resource Naming

```
✅ GET    /users              → list
✅ POST   /users              → create
✅ GET    /users/:id          → get one
✅ PUT    /users/:id          → replace
✅ PATCH  /users/:id          → partial update
✅ DELETE /users/:id          → delete

❌ GET    /getUsers
❌ POST   /createUser
❌ GET    /user/list
❌ DELETE /deleteUser/:id
```

### Nested Resources — Only When Necessary

```
✅ GET /users/:id/roles       → roles belonging to a user
✅ POST /orders/:id/items     → add item to order
❌ GET /users/:id/orders/:orderId/items/:itemId/reviews  → too deep (3 levels max)
```

### Query Parameters vs Path Parameters

```typescript
// Path params = resource identity (required, specific)
GET /users/:id          → specific user

// Query params = filtering, sorting, pagination (optional)
GET /users?search=john&role=admin&page=1&perPage=10
```

### Status Codes — Use Them Correctly

```
200 OK           → successful GET, PUT, PATCH
201 Created      → successful POST that created resource
204 No Content   → successful DELETE (no body)
400 Bad Request  → client sent invalid input
401 Unauthorized → not authenticated (no/invalid token)
403 Forbidden    → authenticated but no permission
404 Not Found    → resource doesn't exist
409 Conflict     → duplicate (email already exists)
422 Unprocessable→ valid format but business logic fails
429 Too Many     → rate limited
500 Server Error → our bug, not client's fault
```

---

## 3. Data Modeling Principles

### Always Include Audit Fields

```typescript
// Minimum fields on every entity
model User {
  id        String    @id @default(cuid())
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt
  deletedAt DateTime? // Soft delete — never hard delete in prod
}
```

### Soft Delete by Default

```typescript
// Never hard-delete in production unless explicitly required
// Hard delete = data loss, audit trail loss, foreign key chaos

// Repository: always filter
const where = { deletedAt: null };

// Soft delete = set timestamp
await prisma.user.update({
  where: { id },
  data: { deletedAt: new Date() }
});
```

### Naming Conventions for Database

```
Tables:     snake_case, plural         → users, role_permissions
Columns:    snake_case                 → created_at, is_active
Boolean:    is_ prefix                 → is_active, is_verified
Timestamps: created_at, updated_at, deleted_at
FKs:        entity_id format          → user_id, organization_id
```

---

## 4. Error Handling Philosophy

### Errors Are First-Class Citizens

Every function that can fail MUST communicate failure explicitly:

```typescript
// ❌ Bad — returns undefined, caller doesn't know why
async function findUser(id: string) {
  return prisma.user.findUnique({ where: { id } });
}

// ✅ Good — explicit error type, caller knows what happened
async function findUser(id: string): Promise<AppError | User> {
  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) return new AppError('NOT_FOUND', 'User not found');
  return user;
}
```

### Error Messages — Write for Humans

```typescript
// ❌ Bad — vague
new AppError('BAD_REQUEST', 'Invalid input')

// ✅ Good — specific, actionable
new AppError('BAD_REQUEST', 'email: must be a valid email address')
new AppError('CONFLICT', 'Email bayudsatriyo@gmail.com is already registered')
new AppError('NOT_FOUND', 'User with ID cmm1234 not found')
```

### Never Swallow Errors

```typescript
// ❌ Bad — silent failure
try {
  await service.doSomething();
} catch (error) {
  // silently ignored
}

// ✅ Good — log and propagate
try {
  await service.doSomething();
} catch (error) {
  console.error('[UserService.create]', error);
  throw error; // or return AppError
}
```

### Categorize Errors Properly

| Error Type | Who's Fault | Action |
|-----------|------------|--------|
| Validation | Client | 400 — tell them what's wrong |
| Auth | Client | 401/403 — don't expose details |
| Not Found | Client | 404 — confirm resource doesn't exist |
| Business Rule | Client | 409/422 — explain the constraint |
| Database | Server | 500 — log internally, generic message to client |
| External API | Server/External | 503 — retry logic, fallback |

---

## 5. Service Layer Best Practices

### Keep Services Pure and Testable

```typescript
// ✅ Good — pure function, easy to unit test
export const userService = {
  create: async (input: CreateUserRequest): Promise<AppError | UserDto> => {
    // 1. Business validation (not format — that's request layer)
    const exists = await userRepository.findByEmail(input.email);
    if (exists) return new AppError('CONFLICT', `${input.email} already registered`);

    // 2. Transform input to database shape if needed
    const hashedPassword = await bcrypt.hash(input.password, 10);

    // 3. Call repository
    const user = await userRepository.create({ ...input, password: hashedPassword });

    // 4. Transform to DTO (never return raw entity)
    return userMapper.toDto(user);
  },
};
```

### Never Mix Concerns in Service

```typescript
// ❌ Bad — service accessing request object
export const userService = {
  create: async (req: Request) => { // ← NEVER do this
    const { body } = req;
    // ...
  },
};

// ❌ Bad — service formatting HTTP response
export const userService = {
  create: async (input: any, res: Response) => { // ← NEVER
    res.json({ data: user }); // ← belongs in controller
  },
};
```

### Service Orchestration — Transactions for Multi-Step

```typescript
// ❌ Bad — two separate writes, no rollback
export const userService = {
  create: async (input: CreateUserRequest) => {
    const user = await userRepository.create(input);
    await auditRepository.log({ action: 'USER_CREATED', userId: user.id }); // if this fails?
    return user;
  },
};

// ✅ Good — atomic transaction
export const userService = {
  create: async (input: CreateUserRequest) => {
    return prisma.$transaction(async (tx) => {
      const user = await tx.user.create({ data: input });
      await tx.auditLog.create({ data: { action: 'USER_CREATED', userId: user.id } });
      return userMapper.toDto(user);
    });
  },
};
```

---

## 6. Performance Thinking

### N+1 Problem — Always Think About Queries

```typescript
// ❌ Bad — N+1 queries (1 for list + N for each user's role)
const users = await prisma.user.findMany();
for (const user of users) {
  user.role = await prisma.role.findUnique({ where: { id: user.roleId } });
}

// ✅ Good — single query with include
const users = await prisma.user.findMany({
  include: { role: true },
});
```

### Pagination Is Mandatory for Lists

```typescript
// ❌ Bad — returns entire table
const users = await prisma.user.findMany();

// ✅ Good — paginated with sane defaults
const users = await prisma.user.findMany({
  skip: (page - 1) * perPage,
  take: perPage, // Max 100 per page, never unlimited
  orderBy: { createdAt: 'desc' },
});
```

### Select Only What You Need

```typescript
// ❌ Bad — fetches all columns including sensitive ones
const user = await prisma.user.findUnique({ where: { id } });

// ✅ Good — explicit field selection
const user = await prisma.user.findUnique({
  where: { id },
  select: {
    id: true,
    name: true,
    email: true,
    role: true,
    // password: NEVER include this
    // internalNotes: NEVER expose internal fields
  },
});
```

### Parallel Queries When Possible

```typescript
// ❌ Bad — sequential: 200ms + 150ms = 350ms
const user = await prisma.user.findUnique({ where: { id } });
const posts = await prisma.post.findMany({ where: { userId: id } });

// ✅ Good — parallel: max(200ms, 150ms) = 200ms
const [user, posts] = await Promise.all([
  prisma.user.findUnique({ where: { id } }),
  prisma.post.findMany({ where: { userId: id } }),
]);
```

---

## 7. Security Principles

### Validate Everything, Trust Nothing

```typescript
// Even if frontend validates, backend MUST validate independently
// Clients can send anything — always validate at the boundary

// ✅ Always validate:
// - Types (is this actually a string? a number?)
// - Lengths (no 10MB strings in name fields)
// - Formats (email, phone, URL)
// - Ranges (age between 0 and 150)
// - Allowed values (enum validation)
```

### Sensitive Data Rules

```typescript
// NEVER expose in responses:
// - passwords (even hashed)
// - tokens / secrets
// - internal IDs that reveal business logic
// - audit/internal fields

// ALWAYS sanitize in logs:
console.log('Creating user:', { email: user.email }); // ✅
console.log('Creating user:', user); // ❌ might log password
```

### Authorization — Check at Service Level

```typescript
// Route middleware checks: "is user logged in?"
// Service checks: "does this user own this resource?"

export const postService = {
  delete: async (postId: string, requesterId: string): Promise<AppError | null> => {
    const post = await postRepository.findById(postId);
    if (!post) return new AppError('NOT_FOUND');

    // ← Service-level authorization
    if (post.userId !== requesterId) {
      return new AppError('FORBIDDEN', 'You cannot delete this post');
    }

    await postRepository.softDelete(postId);
    return null;
  },
};
```

---

## 8. Code Quality Standards

### Function Length — Max ~30 Lines

If a function is longer than 30 lines, it's doing too much. Extract sub-functions.

### Naming — Be Explicit

```typescript
// ❌ Bad — vague names
const d = new Date();
const u = await getUser(id);
const fn = async (x: any) => {};

// ✅ Good — self-documenting
const enrollmentDeadline = new Date();
const currentUser = await userRepository.findById(userId);
const sendWelcomeEmail = async (user: User): Promise<void> => {};
```

### Avoid Magic Numbers/Strings

```typescript
// ❌ Bad
if (user.role === 'a') { ... }
const timeout = 3600;

// ✅ Good
const ADMIN_ROLE = 'admin';
const SESSION_TIMEOUT_SECONDS = 60 * 60; // 1 hour

if (user.role === ADMIN_ROLE) { ... }
```

### Return Early to Reduce Nesting

```typescript
// ❌ Bad — deep nesting
async function processUser(id: string) {
  const user = await findUser(id);
  if (user) {
    if (user.isActive) {
      if (!user.isBanned) {
        // actual logic here
      }
    }
  }
}

// ✅ Good — guard clauses
async function processUser(id: string) {
  const user = await findUser(id);
  if (!user) return new AppError('NOT_FOUND');
  if (!user.isActive) return new AppError('FORBIDDEN', 'Account inactive');
  if (user.isBanned) return new AppError('FORBIDDEN', 'Account banned');

  // actual logic — clean and unindented
}
```

---

## 9. When to Add a New Layer or Pattern

### Add a middleware when:
- Logic needs to run on every request (auth, logging, rate limiting)
- Logic needs to run on groups of routes (role-based access)
- Concern is cross-cutting (CORS, security headers)

### Add an invoke layer when:
- Calling external APIs (SSO, payment, notification services)
- Need consistent retry logic
- Need to wrap external errors into AppError

### Add a query repository when:
- Same query is used in multiple services
- Query is complex enough to warrant its own named function
- Need to abstract database-specific implementation

### Split service when:
- Service file exceeds 200 lines
- Two concerns are emerging (e.g., user CRUD vs user authentication)
- Different consumers need different subsets of functionality

---

## 10. Things Senior Engineers Never Do

❌ `console.log` left in production code  
❌ Empty catch blocks that swallow errors  
❌ Hardcoded secrets/credentials in code  
❌ Unbounded queries (no pagination, no limit)  
❌ `any` type everywhere — type everything explicitly  
❌ `await` in a loop when Promise.all works  
❌ Return raw Prisma entities from services (always map to DTO)  
❌ Mix languages in naming (e.g., `getDataUser` mixing English/Indonesian)  
❌ Commit `node_modules/` or `.env`  
❌ "I'll add error handling later"

---

## 11. Code Review Checklist (Senior Lens)

Before marking any implementation complete:

**Architecture:**
- [ ] Correct layer for each piece of logic?
- [ ] Service returns `AppError | data`?
- [ ] Controller only formats response?
- [ ] Repository only does Prisma queries?

**Data Safety:**
- [ ] No sensitive fields exposed in DTO?
- [ ] Soft delete applied?
- [ ] Input validated at boundary?

**Performance:**
- [ ] No N+1 queries?
- [ ] Lists are paginated?
- [ ] Parallel queries where possible?

**Error Handling:**
- [ ] All errors have meaningful messages?
- [ ] Errors categorized correctly (400 vs 409 vs 500)?
- [ ] No silent failures?

**Code Quality:**
- [ ] No magic strings/numbers?
- [ ] Functions are focused and short?
- [ ] Naming is clear and consistent?
- [ ] No `console.log` left in?

**Security:**
- [ ] Authorization checked at service level?
- [ ] No secrets in code?
- [ ] Logs don't contain sensitive data?
