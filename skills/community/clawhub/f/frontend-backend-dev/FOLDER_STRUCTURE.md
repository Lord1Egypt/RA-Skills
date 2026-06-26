---
name: folder-structure-conventions
description: MVC for frontend; feature, controller, model, repository for backend. Use when adding or refactoring code to keep layout consistent.
---

# Folder Structure Conventions

Follow these layouts when creating or moving code so the codebase stays consistent.

---

## Frontend: MVC

Organize frontend code by **Model**, **View**, and **Controller**.

### Target structure

```
frontend/src/
├── models/           # Data shapes, types, API contracts
├── views/            # UI only (components + pages)
├── controllers/     # Orchestration: hooks, handlers, glue between view and model
├── api/              # API client layer (calls backend; used by controllers)
├── lib/              # Shared utilities, config, constants
└── ...
```

### Models

- **Purpose**: Data structures, domain types, API request/response types.
- **Where**: `src/models/` (or `src/types/`). One file or folder per domain (e.g. `entity.type.ts`).
- **Contains**: TypeScript interfaces/types, Zod schemas if used for validation. No UI, no side effects.
- **Naming**: `*.type.ts` or `*.model.ts`; directory: `models/` or `types/`.

### Views

- **Purpose**: Presentational UI. Render data and call controller callbacks (e.g. `onSave`, `onFilter`).
- **Where**: `src/views/` or keep `src/components/` and `src/pages/` with the understanding they are the View layer.
- **Contains**: React components and pages. Minimal business logic; receive data and handlers via props.
- **Naming**: Lowercase with dashes for directories (e.g. `feature-area/`). PascalCase for components.

### Controllers

- **Purpose**: Connect View and Model. Handle events, call API (via `api/`), update state, coordinate side effects.
- **Where**: `src/controllers/` for controller modules, or `src/hooks/` for React hook–style controllers (e.g. `useFeature`, `useFeatureOperations`).
- **Contains**: Custom hooks that fetch/mutate and expose `{ data, isLoading, handlers }`; or plain functions that views call. Controllers use `api/` and optionally global store; they do not define UI.
- **Naming**: `use-*.ts` / `use*.ts` for hooks; `*-controller.ts` if using non-hook modules.

### Mapping from current layout

When aligning existing code to MVC:

| Current (example)     | MVC role   | Prefer placing in |
|-----------------------|------------|-------------------|
| `api/types.ts`, store shapes | Model      | `models/` (or `types/`) |
| `components/`, `pages/`     | View       | Keep or move under `views/` |
| `hooks/`, orchestration logic | Controller | `controllers/` or keep `hooks/` as controllers |

---

## Backend: Feature, Controller, Model, Repository

Organize backend code by **feature**, with clear **controller**, **model**, and **repository** layers.

### Target structure

```
backend/
├── features/                    # Optional: one folder per feature (see below)
│   └── <feature>/
│       ├── controller.py
│       ├── model.py
│       ├── repository.py
│       └── schema.py
├── controllers/                 # Request handling, orchestration (one module per feature)
├── models/                      # ORM/domain models (one module per entity)
├── repositories/                # Data access (CRUD); one per entity (or keep crud/)
├── schemas/                     # Pydantic request/response schemas
├── routers/                     # Route registration (thin; delegate to controller)
├── deps.py
├── database.py
└── main.py
```

If you keep a flat layout (no `features/` folder), group by **layer** and **feature name**:

- `controllers/<feature>.py` — controller layer  
- `models/<entity>.py` — model layer  
- `repositories/<entity>.py` or `crud/<entity>.py` — repository layer  
- `schemas/<entity>.py` — DTOs  
- `routers/<feature>.py` — HTTP routes  

### Feature

- **Purpose**: A vertical slice of the app.
- **Naming**: Plural, lowercase (e.g. `items`, `users`). Same name used across controller, model, repository, router, schema.

### Controller

- **Purpose**: Handle request logic: validate input, call repository, map to response, raise HTTP errors.
- **Where**: `controllers/<feature>.py`.
- **Contains**: Functions that take `db`, `current_user`, and request data; call repository; return DTOs or raise HTTP exceptions. No SQL or ORM details; use repository only.
- **Naming**: `controllers/<feature>.py`. Functions: verb + noun (e.g. `read_items`, `create_item`).

### Model

- **Purpose**: Domain/ORM entities (database tables).
- **Where**: `models/<entity>.py`.
- **Contains**: ORM model classes (e.g. SQLAlchemy). No request/response schemas here; those go in `schemas/`.
- **Naming**: Singular (e.g. `Item`, `User`). File: `models/<entity>.py`.

### Repository

- **Purpose**: Data access only. CRUD and queries against the database.
- **Where**: `repositories/<entity>.py` or `crud/<entity>.py`.
- **Contains**: Functions/classes that take `db` and query or mutate models. Return model instances or simple structures. No HTTP or schema types here.
- **Naming**: `repositories/<entity>.py` or `crud/<entity>.py` (e.g. `item_crud`, `ItemRepository`).

### Request flow

1. **Router** receives HTTP request, resolves dependencies (`db`, `current_user`), calls **controller**.
2. **Controller** uses **repository** for data and **schemas** for input/output; returns response or raises.
3. **Repository** uses **models** and `db` only.

---

## Quick reference

| Layer       | Frontend (MVC)              | Backend (feature-based)        |
|------------|-----------------------------|---------------------------------|
| Data shape | `models/` or `types/`       | `schemas/` (DTOs), `models/` (ORM) |
| UI         | `views/` or `components/`, `pages/` | —                              |
| Logic / orchestration | `controllers/` or `hooks/` | `controllers/`                 |
| Data access| `api/` (client)             | `repositories/` or `crud/`      |
| Routes     | Router (e.g. React Router)  | `routers/`                      |

When adding new code, place it in the correct layer and use the same feature/entity name across backend files (e.g. feature `items` → `controllers/items.py`, `models/item.py`, `crud/item.py`).
