# Testing Strategy — Aegis Approach

## The Problem with AI-Generated Tests

AI agents love to mock everything. The result: all tests pass, but the system doesn't work.

Aegis enforces a testing pyramid where **mocks are only allowed at the bottom layer**.

## Testing Pyramid

```
         ╱  E2E Test  ╲              ← Real browser + real backend (Playwright)
        ╱───────────────╲
       ╱ Integration Test╲           ← Real HTTP server + real DB (no mocks)
      ╱───────────────────╲
     ╱   Contract Test     ╲         ← Validates conformance to API spec
    ╱───────────────────────╲
   ╱    Frontend Test        ╲       ← Vitest + RTL + MSW (contract-typed mocks)
  ╱───────────────────────────╲
 ╱       Unit Test             ╲     ← Pure logic, mocks allowed
╱───────────────────────────────╲
```

**CI Pipeline Order (canonical):**
```
lint → type-check → unit → frontend-test → contract → integration → build → E2E
```

---

## Layer 1: Unit Tests

- **What:** Pure business logic, utilities, transformations
- **Mocks:** Yes — external dependencies (DB, HTTP, etc.)
- **Speed:** Milliseconds
- **When:** Every code change

---

## Layer 2: Frontend Tests (Production-Ready Standard)

**When the project has a frontend, these are mandatory.**

### Required Stack

| Tool | Role | Alternatives |
|------|------|-------------|
| **Vitest** | Test runner (fast, ESM-native) | Jest (if not Vite-based) |
| **React Testing Library** | Component testing | Vue Testing Library, Svelte Testing Library |
| **MSW (Mock Service Worker)** | Network-level API mocking | None — MSW is the standard |

### Coverage Requirements

#### 1. API Client Tests
Every API function must be tested for three scenarios:

```typescript
// ✅ Good: tests all three paths
describe('getProducts', () => {
  it('returns products on success', async () => {
    // MSW returns 200 with contract-typed data
    const result = await getProducts();
    expect(result).toHaveLength(2);
    expect(result[0]).toMatchObject({ id: expect.any(String), name: expect.any(String) });
  });

  it('throws on API error', async () => {
    // MSW returns 500
    server.use(http.get('/api/products', () => HttpResponse.json({ error: 'INTERNAL_ERROR' }, { status: 500 })));
    await expect(getProducts()).rejects.toThrow();
  });

  it('handles 401 by redirecting to login', async () => {
    // MSW returns 401
    server.use(http.get('/api/products', () => HttpResponse.json({ error: 'UNAUTHORIZED' }, { status: 401 })));
    await getProducts();
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });
});
```

#### 2. Data Hooks Tests
Every data-fetching hook must cover three states:

```typescript
// ✅ Good: tests loading, success, and error states
describe('useProducts', () => {
  it('shows loading state initially', () => {
    const { result } = renderHook(() => useProducts(), { wrapper: QueryProvider });
    expect(result.current.isLoading).toBe(true);
  });

  it('returns data on success', async () => {
    const { result } = renderHook(() => useProducts(), { wrapper: QueryProvider });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(2);
  });

  it('handles error state', async () => {
    server.use(http.get('/api/products', () => HttpResponse.error()));
    const { result } = renderHook(() => useProducts(), { wrapper: QueryProvider });
    await waitFor(() => expect(result.current.isError).toBe(true));
  });
});
```

#### 3. Key Component Rendering
Critical UI components must have render tests:

```typescript
// ✅ Good: tests rendering states + interaction
describe('ProductCard', () => {
  it('renders product data', () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText('Premium Plan')).toBeInTheDocument();
    expect(screen.getByText('$29.99/mo')).toBeInTheDocument();
  });

  it('renders loading skeleton', () => {
    render(<ProductCard loading />);
    expect(screen.getByTestId('skeleton')).toBeInTheDocument();
  });

  it('calls onSubscribe when button clicked', async () => {
    const onSubscribe = vi.fn();
    render(<ProductCard product={mockProduct} onSubscribe={onSubscribe} />);
    await userEvent.click(screen.getByRole('button', { name: /subscribe/i }));
    expect(onSubscribe).toHaveBeenCalledWith(mockProduct.id);
  });
});
```

#### 4. MSW Setup Pattern

```typescript
// src/test/handlers.ts — MSW handlers MUST use contract types
import type { Product, ApiError } from '../../contracts/shared-types';

const mockProducts: Product[] = [
  { id: 'prod_1', name: 'Basic', price: 999, currency: 'usd', interval: 'month' },
  { id: 'prod_2', name: 'Pro', price: 2999, currency: 'usd', interval: 'month' },
];

export const handlers = [
  http.get('/api/products', () => HttpResponse.json(mockProducts)),
  http.get('/api/products/:id', ({ params }) => {
    const product = mockProducts.find(p => p.id === params.id);
    if (!product) return HttpResponse.json({ code: 'PRODUCT_NOT_FOUND' } satisfies ApiError, { status: 404 });
    return HttpResponse.json(product);
  }),
  // ... handler for EVERY endpoint the frontend calls
];
```

**Key rule:** MSW mock data types must be imported from `contracts/shared-types.ts`. Never use ad-hoc `{ id: 1, name: 'test' }`.

### CI Gate
- `pnpm test` (or `npm test`) must pass in CI
- Failed frontend tests = blocked PR, same severity as backend failures

---

## Layer 3: Contract Tests

- **What:** Does the implementation match the API contract?
- **Backend (Provider):** Start the real server, hit endpoints, validate response schema against OpenAPI spec
- **Frontend (Consumer):** Build test data from contract types, verify components handle them correctly
- **Mocks:** Only for dependencies external to the contract scope
- **Speed:** Seconds
- **When:** Every code change that touches an API

---

## Layer 4: Backend Integration Tests (HTTP E2E Standard)

**Every API endpoint must have HTTP-level integration tests. No exceptions.**

### What This Means

```
Start real HTTP server
  → Send real HTTP requests
  → Hit real database (isolated test DB)
  → Validate complete HTTP response (status + headers + body)
  → Verify side effects (GET after mutation to confirm state change)
```

### Coverage Matrix Per Endpoint

| Scenario | What to verify | Required? |
|----------|---------------|-----------|
| **Happy path (200/201)** | Response body matches contract schema | ✅ Always |
| **Bad request (400)** | Missing/invalid params → proper error from `errors.yaml` | ✅ Always |
| **Not found (404)** | Non-existent resource → 404 with correct error code | ✅ For GET/PUT/DELETE |
| **Auth failure (401/403)** | Missing/invalid/expired token → proper auth error | ✅ For protected endpoints |
| **Mutation verification** | POST/PUT/DELETE → GET → confirm state change | ✅ For all mutations |
| **Pagination** | Correct page size, next/prev links, total count | ✅ For list endpoints |
| **Idempotency** | Same request twice → same result (for PUT, idempotent POST) | ⚡ Recommended |

### Language-Specific Testing Tools

| Language | HTTP Test Tool | DB Setup | Example |
|----------|---------------|----------|---------|
| **Go** | `net/http/httptest` + `testing` | testcontainers-go or SQLite | `httptest.NewServer(router)` |
| **TypeScript/Node** | `supertest` + `vitest`/`jest` | testcontainers or SQLite | `request(app).get('/api/products')` |
| **Python** | `httpx` + `pytest` | testcontainers or SQLite | `client.get('/api/products')` |
| **Rust** | `reqwest` + `tokio::test` | testcontainers-rs or SQLite | `client.get(url).send().await` |
| **Java/Kotlin** | `RestAssured` or `WebTestClient` | Testcontainers | `given().when().get("/api/products")` |

### Concrete Example (Go)

```go
func TestCreateProduct(t *testing.T) {
    // Setup: real server + real test DB
    db := setupTestDB(t)
    srv := httptest.NewServer(NewRouter(db))
    defer srv.Close()

    // Happy path
    resp, err := http.Post(srv.URL+"/api/products", "application/json",
        strings.NewReader(`{"name":"Pro","price":2999,"currency":"usd"}`))
    require.NoError(t, err)
    require.Equal(t, 201, resp.StatusCode)

    var created Product
    json.NewDecoder(resp.Body).Decode(&created)
    assert.NotEmpty(t, created.ID)
    assert.Equal(t, "Pro", created.Name)

    // Mutation verification: GET the created resource
    resp, _ = http.Get(srv.URL + "/api/products/" + created.ID)
    require.Equal(t, 200, resp.StatusCode)
    var fetched Product
    json.NewDecoder(resp.Body).Decode(&fetched)
    assert.Equal(t, created.ID, fetched.ID)

    // Bad request
    resp, _ = http.Post(srv.URL+"/api/products", "application/json",
        strings.NewReader(`{"name":""}`))
    assert.Equal(t, 400, resp.StatusCode)

    // Auth failure
    req, _ := http.NewRequest("POST", srv.URL+"/api/products", strings.NewReader(`{"name":"X"}`))
    req.Header.Set("Authorization", "Bearer invalid")
    resp, _ = http.DefaultClient.Do(req)
    assert.Equal(t, 401, resp.StatusCode)
}
```

### Concrete Example (TypeScript/Node)

```typescript
describe('POST /api/products', () => {
  let app: Express;
  let db: TestDB;

  beforeAll(async () => {
    db = await setupTestDB();
    app = createApp(db);
  });
  afterAll(() => db.cleanup());

  it('creates a product (201)', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Pro', price: 2999, currency: 'usd' })
      .expect(201);
    expect(res.body.id).toBeDefined();
    expect(res.body.name).toBe('Pro');

    // Mutation verification
    const fetched = await request(app).get(`/api/products/${res.body.id}`).expect(200);
    expect(fetched.body.id).toBe(res.body.id);
  });

  it('rejects invalid input (400)', async () => {
    await request(app).post('/api/products').send({ name: '' }).expect(400);
  });

  it('rejects unauthorized (401)', async () => {
    await request(app)
      .post('/api/products')
      .set('Authorization', 'Bearer invalid')
      .expect(401);
  });
});
```

### Real Dependencies, Not Mocks

- **Database:** Real test database — SQLite in-memory for simple cases, containerized Postgres/MySQL for production parity
- **Test isolation:** Each test suite gets clean DB state (migrations + seed, or transaction rollback per test)
- **External services:** Only mock truly external third-party APIs (Stripe, SendGrid, etc.) — all internal services stay real

---

## Layer 5: E2E Tests

- **What:** Does the deployed system work from a user's perspective?
- **Setup:** Playwright against a real deployment (or playwright-forge for remote execution)
- **Mocks:** None
- **Speed:** Minutes
- **When:** After build, before release
- **Scope:** Critical user flows only — not every permutation

---

## Test Strategy in Design Review (Mandatory Gate)

**When a project includes both frontend and backend**, the Design Brief's Testing Strategy section must define **all layers upfront**:

1. **Frontend tests:** API client coverage list, hook coverage list, key component list, MSW handler plan
2. **Backend integration tests:** endpoint list, scenario matrix per endpoint, DB setup requirements
3. **E2E tests:** critical user flows that need browser-level verification

This is a **Design Review gate** — a Design Brief without a complete testing strategy for a full-stack feature cannot be approved. Testing is designed before code, not bolted on after.

### Testing Strategy Template (for Design Brief)

```markdown
## Testing Strategy

### Frontend Tests
- **API clients to test:** [list each client function]
- **Hooks to test:** [list each data hook]
- **Key components:** [list components needing render tests]
- **MSW coverage:** [list endpoints to mock, note any special scenarios]

### Backend Integration Tests
| Endpoint | Happy | 400 | 404 | 401 | Mutation | Notes |
|----------|-------|-----|-----|-----|----------|-------|
| POST /api/products | ✅ | ✅ | — | ✅ | ✅ GET after create | |
| GET /api/products/:id | ✅ | — | ✅ | ✅ | — | |

### E2E Flows
- [ ] User signup → first product creation → subscription
- [ ] Admin login → dashboard → view metrics
```

---

## Key Principles

1. **Never mock across contract boundaries** — If frontend tests mock the API, you're testing your assumptions, not the system
2. **Contract tests are mandatory** — They're cheap and catch 80% of integration issues
3. **Integration tests prove it works** — Real HTTP + real DB is your safety net
4. **E2E tests validate the user experience** — Not every flow, just the critical paths
5. **Frontend tests are not second-class** — Same rigor as backend. Same CI gates. Same blocking power.
6. **Test strategy is a design artifact** — Define it in the Design Brief, before writing code. Not after.
7. **Mock only what you don't own** — Third-party APIs (Stripe, SendGrid) get mocked. Your own services don't.
