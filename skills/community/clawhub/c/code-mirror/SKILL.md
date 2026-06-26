---
name: code-mirror
description: "Mirror frontend and backend code across the stack. Invoke when user wants to generate backend from frontend code, generate frontend from backend code, sync existing code across stack, or scaffold full-stack features from one side."

---

# Code Mirror - Frontend-Backend Code Mirroring

Code Mirror analyzes existing frontend or backend code and generates the corresponding counterpart on the other side. It understands the structural semantics — API contracts, data models, routing, validation, state management — and produces idiomatic, production-ready code that perfectly mirrors the source.

---

## When to Use This Skill

Activate Code Mirror when the user:

- Provides frontend code and asks for the backend implementation
- Provides backend code and asks for the frontend integration
- Wants to scaffold a full-stack feature from one side of the stack
- Asks to sync types or API calls between existing frontend and backend
- Says "mirror", "bridge", "generate counterpart", "sync types", "scaffold API", "generate client"
- Has a backend change and wants frontend types updated (or vice versa)

---

## Core Workflow

### Phase 1: Identify Source and Target

First, understand what the user has and what they want.

**Source side detection** (read the code the user provides):

| Clues                                                        | Side         |
| ------------------------------------------------------------ | ------------ |
| `useState`, `useEffect`, `useCallback`, `axios`, `fetch`, `onClick`, `ref`, `component`, `template`, `v-for`, `v-if`, `ngIf`, `ngFor`, `queryClient`, `useQuery`, `useMutation`, `.tsx`, `.jsx`, `.vue`, `.svelte` | **Frontend** |
| `@app.route`, `router.`, `req.body`, `res.json`, `@Controller`, `@GetMapping`, `@PostMapping`, `@RestController`, `Model.find`, `Schema`, `prisma`, `entity`, `repository`, `BaseModel`, `Depends`, `HTTPException`, `.go`, `.java`, `.py` with `fastapi`/`django` | **Backend**  |

If ambiguous, ask: "Is this frontend or backend code? What framework are you using?"

**Target stack detection** (infer from existing project or ask the user):

Check the user's project files in the workspace:

| File                                  | Stack                                                       |
| ------------------------------------- | ----------------------------------------------------------- |
| `package.json`                        | Check dependencies for React, Vue, Angular, Express, NestJS |
| `requirements.txt` / `pyproject.toml` | Python with FastAPI, Django, Flask                          |
| `go.mod`                              | Go with Gin, Echo, net/http                                 |
| `pom.xml` / `build.gradle`            | Java with Spring Boot                                       |
| `Cargo.toml`                          | Rust with Actix, Rocket                                     |
| `*.csproj`                            | C# with ASP.NET Core                                        |

If no existing project, ask: "What stack do you want me to generate for? (e.g., Express + TypeScript, FastAPI, Go Gin, Spring Boot)"

### Phase 2: Analyze Source Code

Read and deeply understand the source code. Extract the following based on side:

#### When analyzing FRONTEND code, extract:

**1. API Calls** — all endpoints the frontend hits

```typescript
// For each API call, record:
// - HTTP method (GET, POST, PUT, PATCH, DELETE)
// - URL path (/api/users, /api/users/:id)
// - Request body shape (from the data being sent)
// - Response shape (from how the response is used)
// - Query parameters (from URL params)
// - Path parameters (from template strings like `/users/${id}`)

axios.get('/api/users')                           // GET /api/users → User[]
axios.post('/api/users', { name, email })         // POST /api/users → User
axios.put(`/api/users/${id}`, { name })           // PUT /api/users/:id → User
axios.delete(`/api/users/${id}`)                  // DELETE /api/users/:id
fetch('/api/users?page=1&limit=20')               // GET with query params
```

**2. Data Models** — TypeScript interfaces, PropTypes, Zod schemas

```typescript
// Extract: name, all fields, field types, optional/required markers, enums, default values

interface User {
  id: string;                    // required string
  name: string;                  // required string
  email: string;                 // required string
  role: 'admin' | 'user';        // enum
  age?: number;                  // optional number
  createdAt: Date;               // date
}
```

**3. Form Validation Rules** — Zod, Yup, or manual validation

```typescript
// Extract: field name, validation type (required, email, min, max, pattern, custom)

const schema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().min(18).optional(),
  password: z.string().min(8),
});
```

**4. State Management Patterns** (optional, for complex apps)

```typescript
// Extract: store structure, state shape, actions that modify state

const useUserStore = create((set) => ({
  users: [],
  loading: false,
  error: null,
  fetchUsers: async () => { ... },
  addUser: (user) => set((state) => ({ users: [...state.users, user] })),
}));
```

#### When analyzing BACKEND code, extract:

**1. Route Definitions** — every endpoint the backend exposes

```python
# For each route, record:
# - Path (including path parameters like /users/{user_id})
# - HTTP method
# - Request body schema (from Pydantic model or DTO)
# - Query parameters (from function arguments)
# - Response model (from response_model or return type)
# - Status codes (especially 201, 204)

@router.get("/users")                              # GET /users → List[UserOut]
@router.get("/users/{user_id}")                    # GET /users/:id → UserOut
@router.post("/users")                             # POST /users → UserOut
@router.put("/users/{user_id}")                    # PUT /users/:id → UserOut
@router.delete("/users/{user_id}", status_code=204) # DELETE /users/:id → 204
```

**2. Data Models / Schemas** — database models and API schemas

```python
# Extract: name, fields, types, required/optional, validators, relationships

class User(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: Literal["admin", "user"] = "user"
    age: Optional[int] = Field(None, ge=0, le=120)
    created_at: datetime
```

**3. Business Logic** (for more complete generation)

```python
# Extract: operations, side effects (email sending, logging), error handling patterns

def create_user(db: Session, user: UserCreate):
    # hash password
    # check if email exists
    # send welcome email
    # return created user
    pass
```

**4. Authentication/Authorization**

```python
# Extract: auth method (JWT, session, API key), protected routes, role requirements

@router.get("/admin/users", dependencies=[Depends(require_admin)])
async def get_admin_users(...):
    pass
```

### Phase 3: Generate Target Code

Generate code following the target stack's best practices. Always produce code that fits naturally into the existing project structure.

#### Frontend → Backend (generate in this order):

1. **Data models** — ORM schema (Prisma, Mongoose, SQLAlchemy, TypeORM)
2. **Validation schemas** — matching frontend form rules (Zod, Pydantic, Joi, class-validator)
3. **Route definitions** — covering all endpoints frontend calls
4. **Controller/Handler functions** — implementing each route
5. **Service layer** — if the project uses services
6. **Middleware** — auth, error handling, CORS, logging
7. **Database configuration** — connection setup, migrations

#### Backend → Frontend (generate in this order):

1. **TypeScript types** — from backend response/request models
2. **API client** — typed fetch/axios functions for all endpoints
3. **React Query hooks** or Vue composables or Angular services
4. **State management** — stores/slices for complex data flows
5. **UI components** — forms, lists, detail views
6. **Client-side routes** — if generating full pages

### Phase 4: Validate and Output

After generation, verify consistency and present the code clearly.

**Consistency Checklist:**

- [ ] Every frontend API call has a corresponding backend route
- [ ] Every backend route is called by the frontend (if generating from backend)
- [ ] Request/response types match on both sides
- [ ] Validation rules are consistent (same required fields, same formats)
- [ ] Error responses have consistent shapes (status codes, error message fields)
- [ ] Authentication headers/tokens are handled correctly
- [ ] No placeholder comments like `// TODO: implement`

**Output Format:**

For each generated file, show:

1. **File path as a heading** — so user knows exactly where to put it
2. **Brief explanation** (optional, for complex files)
3. **Complete file content** — no snippets, no placeholders

Example:

```
I'll generate the Express backend for your React todo form.

`src/models/Todo.ts`
```typescript
// full file content
```

`src/validators/todoValidator.ts`

```typescript
// full file content
```

`src/routes/todos.ts`

```typescript
// full file content
```

The routes match the frontend calls: `POST /api/todos` expects `{ title, description }` and returns a todo with an `id`. All validation rules from your frontend form are mirrored in the backend Zod schema.
---

## Stack-Specific Generation Templates

### For Express + TypeScript Backend

**Model (Mongoose):**

```typescript
import mongoose, { Schema, Document } from 'mongoose';

export interface I{{Resource}} extends Document {
  {{#each fields}}
  {{name}}: {{mongooseType}};
  {{/each}}
  createdAt: Date;
  updatedAt: Date;
}

const {{resource}}Schema = new Schema<I{{Resource}}>(
  {
    {{#each fields}}
    {{name}}: { 
      type: {{mongooseType}}, 
      required: {{required}}{{#if unique}}, unique: true{{/if}}
    },
    {{/each}}
  },
  { timestamps: true }
);

export const {{Resource}}Model = mongoose.model<I{{Resource}}>('{{Resource}}', {{resource}}Schema);
```

**Validator (Zod):**

```typescript
import { z } from 'zod';

export const create{{Resource}}Schema = z.object({
  {{#each fields}}
  {{name}}: z.{{zodType}}(){{#if required}}{{else}}.optional(){{/if}}{{#if validation}}.{{validation}}{{/if}},
  {{/each}}
});

export const update{{Resource}}Schema = create{{Resource}}Schema.partial();

export type Create{{Resource}}Input = z.infer<typeof create{{Resource}}Schema>;
export type Update{{Resource}}Input = z.infer<typeof update{{Resource}}Schema>;
```

**Route:**

```typescript
import { Router } from 'express';
import { {{Resource}}Model } from '../models/{{Resource}}';
import { validate } from '../middleware/validate';
import { create{{Resource}}Schema, update{{Resource}}Schema } from '../validators/{{resource}}Validator';
import { authMiddleware } from '../middleware/auth';

const router = Router();

// Apply auth middleware to all routes (if needed)
router.use(authMiddleware);

router.get('/', async (req, res) => {
  const items = await {{Resource}}Model.find();
  res.json(items);
});

router.get('/:id', async (req, res) => {
  const item = await {{Resource}}Model.findById(req.params.id);
  if (!item) return res.status(404).json({ error: '{{Resource}} not found' });
  res.json(item);
});

router.post('/', validate(create{{Resource}}Schema), async (req, res) => {
  const item = await {{Resource}}Model.create(req.body);
  res.status(201).json(item);
});

router.put('/:id', validate(update{{Resource}}Schema), async (req, res) => {
  const item = await {{Resource}}Model.findByIdAndUpdate(req.params.id, req.body, { new: true });
  if (!item) return res.status(404).json({ error: '{{Resource}} not found' });
  res.json(item);
});

router.delete('/:id', async (req, res) => {
  const item = await {{Resource}}Model.findByIdAndDelete(req.params.id);
  if (!item) return res.status(404).json({ error: '{{Resource}} not found' });
  res.status(204).end();
});

export default router;
```

### For FastAPI Backend (Python)

**Schema (Pydantic):**

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class {{Resource}}Role(str, Enum):
    {{#each enums}}
    {{value}} = "{{value}}"
    {{/each}}

class {{Resource}}Base(BaseModel):
    {{#each fields}}
    {{name}}: {{pythonType}} = Field(
        {{#if required}}...{{else}}None{{/if}},
        {{#if validation}}...{{/if}}
    )
    {{/each}}

class {{Resource}}Create({{Resource}}Base):
    {{#each requiredFields}}
    {{name}}: {{pythonType}}
    {{/each}}

class {{Resource}}Update(BaseModel):
    {{#each fields}}
    {{name}}: Optional[{{pythonType}}] = None
    {{/each}}

class {{Resource}}Out({{Resource}}Base):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```

**Router:**

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.{{resource}} import {{Resource}}Create, {{Resource}}Update, {{Resource}}Out
from app import crud

router = APIRouter(prefix="/{{resource}}s", tags=["{{resource}}s"])

@router.get("", response_model=List[{{Resource}}Out])
async def list_{{resource}}s(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.{{resource}}.get_multi(db, skip=skip, limit=limit)

@router.get("/{{item_id}}", response_model={{Resource}}Out)
async def get_{{resource}}({{item_id}}: str, db: Session = Depends(get_db)):
    item = crud.{{resource}}.get(db, id={{item_id}})
    if not item:
        raise HTTPException(status_code=404, detail="{{Resource}} not found")
    return item

@router.post("", response_model={{Resource}}Out, status_code=201)
async def create_{{resource}}(
    item: {{Resource}}Create,
    db: Session = Depends(get_db),
):
    return crud.{{resource}}.create(db, obj_in=item)

@router.put("/{{item_id}}", response_model={{Resource}}Out)
async def update_{{resource}}(
    {{item_id}}: str,
    item: {{Resource}}Update,
    db: Session = Depends(get_db),
):
    db_item = crud.{{resource}}.get(db, id={{item_id}})
    if not db_item:
        raise HTTPException(status_code=404, detail="{{Resource}} not found")
    return crud.{{resource}}.update(db, db_obj=db_item, obj_in=item)

@router.delete("/{{item_id}}", status_code=204)
async def delete_{{resource}}({{item_id}}: str, db: Session = Depends(get_db)):
    item = crud.{{resource}}.get(db, id={{item_id}})
    if not item:
        raise HTTPException(status_code=404, detail="{{Resource}} not found")
    crud.{{resource}}.remove(db, id={{item_id}})
```

### For React + TypeScript Frontend

**Types:**

```typescript
// types/{{resource}}.ts
export interface {{Resource}} {
  id: string;
  {{#each fields}}
  {{name}}: {{tsType}};
  {{/each}}
  createdAt: string;
  updatedAt: string;
}

export interface Create{{Resource}}Input {
  {{#each requiredFields}}
  {{name}}: {{tsType}};
  {{/each}}
  {{#each optionalFields}}
  {{name}}?: {{tsType}};
  {{/each}}
}

export interface Update{{Resource}}Input {
  {{#each fields}}
  {{name}}?: {{tsType}};
  {{/each}}
}
```

**API Client:**

```typescript
// api/{{resource}}.ts
import axios from 'axios';
import type { {{Resource}}, Create{{Resource}}Input, Update{{Resource}}Input } from '../types/{{resource}}';

const BASE_URL = '/api/{{resource}}s';

export const {{resource}}Api = {
  list: () => axios.get<{{Resource}}[]>(BASE_URL),
  
  getById: (id: string) => axios.get<{{Resource}}>(`${BASE_URL}/${id}`),
  
  create: (data: Create{{Resource}}Input) => axios.post<{{Resource}}>(BASE_URL, data),
  
  update: (id: string, data: Update{{Resource}}Input) => 
    axios.put<{{Resource}}>(`${BASE_URL}/${id}`, data),
  
  delete: (id: string) => axios.delete(`${BASE_URL}/${id}`),
};
```

**React Query Hooks:**

```typescript
// hooks/use{{Resource}}s.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { {{resource}}Api } from '../api/{{resource}}';
import type { Create{{Resource}}Input, Update{{Resource}}Input } from '../types/{{resource}}';

export function use{{Resource}}s() {
  return useQuery({
    queryKey: ['{{resource}}s'],
    queryFn: async () => {
      const { data } = await {{resource}}Api.list();
      return data;
    },
  });
}

export function use{{Resource}}(id: string) {
  return useQuery({
    queryKey: ['{{resource}}s', id],
    queryFn: async () => {
      const { data } = await {{resource}}Api.getById(id);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreate{{Resource}}() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: Create{{Resource}}Input) => {{resource}}Api.create(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['{{resource}}s'] });
    },
  });
}

export function useUpdate{{Resource}}() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...input }: Update{{Resource}}Input & { id: string }) => 
      {{resource}}Api.update(id, input),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['{{resource}}s'] });
      queryClient.invalidateQueries({ queryKey: ['{{resource}}s', id] });
    },
  });
}

export function useDelete{{Resource}}() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => {{resource}}Api.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['{{resource}}s'] });
    },
  });
}
```

### For Vue 3 + TypeScript Frontend

**Composable:**

```typescript
// composables/use{{Resource}}s.ts
import { ref, readonly } from 'vue';
import axios from 'axios';
import type { {{Resource}}, Create{{Resource}}Input, Update{{Resource}}Input } from '../types/{{resource}}';

export function use{{Resource}}s() {
  const items = ref<{{Resource}}[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentItem = ref<{{Resource}} | null>(null);

  const fetchAll = async () => {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await axios.get<{{Resource}}[]>('/api/{{resource}}s');
      items.value = data;
    } catch (e) {
      error.value = (e as Error).message;
    } finally {
      loading.value = false;
    }
  };

  const fetchOne = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await axios.get<{{Resource}}>(`/api/{{resource}}s/${id}`);
      currentItem.value = data;
      return data;
    } catch (e) {
      error.value = (e as Error).message;
      throw e;
    } finally {
      loading.value = false;
    }
  };

  const create = async (input: Create{{Resource}}Input) => {
    const { data } = await axios.post<{{Resource}}>('/api/{{resource}}s', input);
    items.value.push(data);
    return data;
  };

  const update = async (id: string, input: Update{{Resource}}Input) => {
    const { data } = await axios.put<{{Resource}}>(`/api/{{resource}}s/${id}`, input);
    const index = items.value.findIndex(i => i.id === id);
    if (index !== -1) items.value[index] = data;
    if (currentItem.value?.id === id) currentItem.value = data;
    return data;
  };

  const remove = async (id: string) => {
    await axios.delete(`/api/{{resource}}s/${id}`);
    items.value = items.value.filter(i => i.id !== id);
    if (currentItem.value?.id === id) currentItem.value = null;
  };

  return {
    items: readonly(items),
    currentItem: readonly(currentItem),
    loading: readonly(loading),
    error: readonly(error),
    fetchAll,
    fetchOne,
    create,
    update,
    remove,
  };
}
```

---

## Special Scenarios

### Scenario 1: Sync Existing Code (Diff Mode)

User says: "My FastAPI backend added a `phone` field to User. Update my React frontend."

**Process:**

1. Read backend model to find the new `phone` field
2. Read frontend types to see current state
3. Identify the diff: what's missing in frontend
4. Generate only the changes needed:
   - Add `phone: string` to User interface
   - Add `phone` to CreateUserInput/UpdateUserInput
   - Update API client if needed (no change for GET, need to include in POST/PUT)
   - Update form component to include phone field
5. Output each changed file with the specific changes, not full files (unless user asks for full)

**Output format for sync:**

I found the new `phone` field in your backend User model. Here are the frontend updates needed:

`src/types/user.ts` — add `phone` field:

```diff
  export interface User {
    id: string;
    name: string;
    email: string;
+   phone: string;
    role: 'admin' | 'user';
    createdAt: string;
  }
```

`src/api/users.ts` — no change needed (API calls remain the same)

`src/components/UserForm.tsx` — add phone input:

```diff
  const schema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
+   phone: z.string().regex(/^\+?[1-9]\d{1,14}$/),
  });
```

### Scenario 2: One Side Only, Generate Full Counterpart

User says: "Here's my React form for creating a product. Generate the Express backend."

**Process:**

1. Extract from React:
   - API endpoint: `POST /api/products`
   - Request body fields: `name`, `price`, `description`
   - Validation rules: `name` required, `price` positive number
2. Generate complete backend:
   - Product model with extracted fields
   - Zod validator with same rules
   - POST route handler
   - (Optional) GET list route for completeness
3. Output complete, runnable files

### Scenario 3: Full-Stack Feature from Description

User says: "I need a todo app with users. Generate React frontend and Express backend."

**Process:**

1. Design schema from description:
   - User: `id`, `name`, `email`, `password` (hashed)
   - Todo: `id`, `title`, `completed`, `userId`, `createdAt`
2. Generate backend in order:
   - Models (User, Todo)
   - Validators (create user, update todo, etc.)
   - Routes (auth, todos CRUD)
   - Auth middleware (JWT)
3. Generate frontend in order:
   - Types (User, Todo)
   - API client (auth calls, todo calls)
   - Auth context/hooks
   - React Query hooks
   - Components (Login, Register, TodoList, TodoForm)
   - Routes (protected routes)
4. Ensure all endpoints match between frontend API calls and backend routes

---

## Type Mapping Reference

When converting between languages, use these mappings:

### TypeScript ↔ Python (FastAPI)

| TypeScript                      | Python (Pydantic)                    |
| ------------------------------- | ------------------------------------ |
| `string`                        | `str`                                |
| `number`                        | `int` \| `float`                     |
| `boolean`                       | `bool`                               |
| `Date` / `string` (ISO)         | `datetime`                           |
| `Array<T>` \| `T[]`             | `List[T]`                            |
| `Record<string, T>`             | `Dict[str, T]`                       |
| `T \| null` \| `T \| undefined` | `Optional[T]`                        |
| `interface`                     | `BaseModel`                          |
| `enum`                          | `Enum` or `Literal`                  |
| `'a' \| 'b'`                    | `Literal['a', 'b']`                  |
| `Partial<T>`                    | Separate Update model (all optional) |
| `Omit<T, 'id'>`                 | Separate Create model without id     |

### TypeScript ↔ Go

| TypeScript          | Go                                      |
| ------------------- | --------------------------------------- |
| `string`            | `string`                                |
| `number`            | `int` \| `int64` \| `float64`           |
| `boolean`           | `bool`                                  |
| `Date`              | `time.Time`                             |
| `Array<T>` \| `T[]` | `[]T`                                   |
| `Record<string, T>` | `map[string]T`                          |
| `T \| null`         | `*T` (pointer)                          |
| `interface`         | `struct` with JSON tags                 |
| `enum`              | `const` with `iota` or string constants |

### TypeScript ↔ Java (Spring Boot)

| TypeScript          | Java                           |
| ------------------- | ------------------------------ |
| `string`            | `String`                       |
| `number`            | `int` \| `Long` \| `Double`    |
| `boolean`           | `boolean` \| `Boolean`         |
| `Date`              | `LocalDateTime` \| `Instant`   |
| `Array<T>` \| `T[]` | `List<T>`                      |
| `Record<string, T>` | `Map<String, T>`               |
| `T \| null`         | `Optional<T>` or `@Nullable`   |
| `interface`         | DTO class with getters/setters |
| `enum`              | `enum`                         |

### TypeScript ↔ C# (ASP.NET Core)

| TypeScript          | C#                                       |
| ------------------- | ---------------------------------------- |
| `string`            | `string`                                 |
| `number`            | `int` \| `long` \| `double` \| `decimal` |
| `boolean`           | `bool`                                   |
| `Date`              | `DateTime` \| `DateTimeOffset`           |
| `Array<T>` \| `T[]` | `List<T>` \| `T[]`                       |
| `Record<string, T>` | `Dictionary<string, T>`                  |
| `T \| null`         | `T?` (nullable reference types)          |
| `interface`         | `class` with properties                  |

---

## Example Usage

### Example 1: Frontend → Backend

**User:**

Here's my React component for user management. Generate the Express backend for it.

```tsx
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  
  useEffect(() => {
    axios.get('/api/users').then(res => setUsers(res.data));
  }, []);
  
  const addUser = async (name: string, email: string, role: string) => {
    const res = await axios.post('/api/users', { name, email, role });
    setUsers([...users, res.data]);
  };
  
  const deleteUser = async (id: number) => {
    await axios.delete(`/api/users/${id}`);
    setUsers(users.filter(u => u.id !== id));
  };
  
  // ... render
}
```

**Code Mirror response:**

I'll generate the Express backend that mirrors your React frontend.

From your frontend, I identified:

- GET /api/users → returns User[]
- POST /api/users → accepts { name, email, role } → returns User
- DELETE /api/users/:id

`src/models/User.ts`

```typescript
import mongoose, { Schema, Document } from 'mongoose';

export interface IUser extends Document {
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
  updatedAt: Date;
}

const UserSchema = new Schema<IUser>(
  {
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    role: { type: String, enum: ['admin', 'user'], default: 'user' },
  },
  { timestamps: true }
);

export const UserModel = mongoose.model<IUser>('User', UserSchema);
```

`src/validators/userValidator.ts`

```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(['admin', 'user']).default('user'),
});

export const updateUserSchema = createUserSchema.partial();
```

`src/routes/users.ts`

```typescript
import { Router } from 'express';
import { UserModel } from '../models/User';
import { validate } from '../middleware/validate';
import { createUserSchema, updateUserSchema } from '../validators/userValidator';

const router = Router();

router.get('/', async (req, res) => {
  const users = await UserModel.find();
  res.json(users);
});

router.post('/', validate(createUserSchema), async (req, res) => {
  const user = await UserModel.create(req.body);
  res.status(201).json(user);
});

router.delete('/:id', async (req, res) => {
  const user = await UserModel.findByIdAndDelete(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.status(204).end();
});

export default router;
```

The routes exactly match your frontend calls. The POST validator enforces the same required fields your frontend sends.

```
### Example 2: Backend → Frontend (Sync Mode)

**User:**
```

My FastAPI backend User model added a `phone` field. Update my React frontend types and form.

Backend model:

```python
class User(BaseModel):
    id: str
    name: str
    email: str
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    role: Literal['admin', 'user'] = 'user'
    created_at: datetime
```

```
**Code Mirror response:**
```

I found the new `phone` field. Here are the frontend updates:

`src/types/user.ts` — add phone field:

```diff
  export interface User {
    id: string;
    name: string;
    email: string;
+   phone: string;
    role: 'admin' | 'user';
    createdAt: string;
  }

  export interface CreateUserInput {
    name: string;
    email: string;
+   phone: string;
    role?: 'admin' | 'user';
  }
```

`src/components/UserForm.tsx` — add phone field with validation:

```diff
  const schema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
+   phone: z.string().regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number'),
    role: z.enum(['admin', 'user']).optional(),
  });
```

`src/api/users.ts` — no change needed (API calls remain the same, phone will be included automatically in POST/PUT)

The validation pattern matches your backend's `Field(pattern=...)` constraint.
---

## Quality Checklist

Before finalizing generated code, verify:

- [ ] **Endpoint coverage** — Every endpoint in source has counterpart in target
- [ ] **Type alignment** — All fields, types, optional/required markers match
- [ ] **Validation consistency** — Same rules exist on both sides (required fields, email format, min/max, patterns)
- [ ] **Error handling** — Error responses have consistent shapes and status codes (400 for validation, 401 for auth, 404 for not found, 500 for server errors)
- [ ] **Authentication** — Token storage/sending in frontend matches backend middleware expectations
- [ ] **Code style** — Generated code matches existing project patterns (import style, naming, file organization)
- [ ] **Completeness** — No placeholder comments like `// TODO: implement this`
- [ ] **Runnable** — Code would run as-is (assuming correct dependencies are installed)
- [ ] **No hallucinations** — Generated types, validators, and routes are directly derived from source, not invented

---

## Error Handling in Generated Code

Always include proper error handling appropriate to the stack:

### Backend error handling patterns:

```typescript
// Express - 404
if (!item) return res.status(404).json({ error: 'Resource not found' });

// Express - validation
if (!result.success) return res.status(400).json({ errors: result.error.flatten() });

// Express - duplicate
try {
  await Model.create(data);
} catch (err) {
  if (err.code === 11000) return res.status(409).json({ error: 'Duplicate key' });
  throw err;
}
```

```python
# FastAPI - 404
if not item:
    raise HTTPException(status_code=404, detail="Resource not found")

# FastAPI - validation (handled automatically by Pydantic)
# FastAPI - duplicate
if existing:
    raise HTTPException(status_code=409, detail="Email already registered")
```

### Frontend error handling patterns:

```typescript
// React Query - errors are automatically available in query result
const { error } = useQuery(...);

// Axios interceptor for global error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // redirect to login
    }
    return Promise.reject(error);
  }
);
```

---

## Notes for the AI

When using this skill:

1. **Always read the source code thoroughly** before generating. Don't assume or invent fields.
2. **Detect the stack from existing project files** if available. Match the existing code style.
3. **Generate complete files** — no snippets, no placeholders. Users should be able to copy-paste and run.
4. **Show file paths** as headings so users know where files go.
5. **For sync operations**, show diffs (using ```diff format) unless user asks for full files.
6. **Preserve all business logic** from source — don't drop validation rules or computed fields.
7. **If anything is ambiguous**, ask clarifying questions before generating.
8. **After generation**, run through the Quality Checklist mentally to ensure nothing was missed.
