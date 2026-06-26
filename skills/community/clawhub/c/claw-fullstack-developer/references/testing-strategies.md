# Testing Strategies

How to test a full-stack app — what to write, what to skip, and how to keep the suite fast.

## The testing pyramid

```
        ▲
       /─\      E2E (few, slow, realistic)     ~5%
      /───\
     /─────\    Integration (DB + API)         ~25%
    /───────\
   /─────────\  Unit (pure logic, fast)        ~70%
  ─────────────
```

Rough target ratios. The numbers don't matter; the shape does — lots of fast unit tests, fewer integration tests, very few E2E tests.

### Why the pyramid
- Unit tests: fast (<1s for thousands), run on every save, catch logic bugs early.
- Integration tests: medium-speed, catch contract bugs between layers (API ↔ DB, service ↔ external).
- E2E tests: slow, flaky-prone, but catch things nothing else catches — real browser + real backend + real DB.

Inverting the pyramid (mostly E2E, few unit tests) produces test suites that take 20 minutes and fail randomly. Don't.

## Unit tests — what to test

### Test pure logic
- Domain rules: pricing, permissions, validation, date calculations
- Transformations: parsers, formatters, mappers between layers
- Decision functions: "should this alert fire", "can this user see this post"

### Skip things not worth testing
- Framework plumbing (routing, middleware registration)
- Trivial getters/setters or pass-throughs
- Third-party library behavior (trust it, or test at the integration level)

### Patterns

**Arrange-Act-Assert**:
```ts
test('premium users get free shipping', () => {
  // Arrange
  const user = makeUser({ tier: 'premium' });
  const cart = makeCart({ subtotal: 50 });

  // Act
  const total = calculateTotal(user, cart);

  // Assert
  expect(total.shipping).toBe(0);
});
```

**Table-driven tests** for similar cases:
```ts
test.each([
  { tier: 'free', subtotal: 50, expectedShipping: 10 },
  { tier: 'free', subtotal: 100, expectedShipping: 0 },  // free over $75
  { tier: 'premium', subtotal: 10, expectedShipping: 0 },
])('shipping: $tier tier, $$$subtotal cart', ({ tier, subtotal, expectedShipping }) => {
  const total = calculateTotal(makeUser({ tier }), makeCart({ subtotal }));
  expect(total.shipping).toBe(expectedShipping);
});
```

### What's a "unit"?
A unit is a coherent behavior, not a file or function. One test per public function is fine; one test per private helper is usually noise. Test behavior, not implementation.

### Tools by language
| Lang | Framework |
|---|---|
| JS/TS | **Vitest** (fast, ESM-native, Jest-compatible). Jest still works but is slower. |
| Python | **pytest** |
| Go | built-in `testing` + `testify` (optional) |
| Rust | built-in `#[test]` |

## Integration tests — the API + DB layer

This is where the most valuable tests live for a typical app. You spin up the app, hit real endpoints, verify the response and DB state.

### Setup pattern (Node/Postgres)
- Dedicated test database (e.g., `myapp_test`).
- Migrate schema once before the suite.
- Each test (or test file) runs in a transaction that rolls back — fast, isolated.
- Seed minimal data inside each test.

### Example (Fastify + Prisma + Vitest)
```ts
import { buildApp } from '@/server';
import { prisma } from '@/lib/db';

describe('POST /users', () => {
  const app = buildApp();

  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  test('creates user with valid input', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/users',
      payload: { email: 'test@example.com', name: 'Test' },
    });
    expect(response.statusCode).toBe(201);
    const user = await prisma.user.findUnique({ where: { email: 'test@example.com' } });
    expect(user).not.toBeNull();
  });

  test('rejects invalid email', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/users',
      payload: { email: 'not-an-email', name: 'Test' },
    });
    expect(response.statusCode).toBe(400);
  });
});
```

### Setup pattern (Python/FastAPI)
```python
import pytest
from httpx import AsyncClient
from app.main import app
from app.db import Base, engine, SessionLocal

@pytest.fixture(autouse=True)
def db_reset():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users", json={"email": "a@b.com", "name": "A"})
        assert response.status_code == 201
```

## What NOT to mock

**Don't mock your own database.** Integration tests that use a mock DB give you confidence in the mock, not in the code. A changed schema won't break the test. Use a real test database — SQLite in-memory for speed if your app is DB-agnostic, Postgres (Docker, Testcontainers, or local) if you rely on Postgres features.

**Don't mock your own services from other services.** If service A calls service B, and both are in your repo, test them together (or test the contract with consumer-driven contract tests).

**Do mock:**
- Third-party HTTP APIs (Stripe, OpenAI, SendGrid) — record and replay with [`msw`](https://mswjs.io/), [`vcrpy`](https://vcrpy.readthedocs.io/), or [Prism](https://stoplight.io/open-source/prism).
- Time and randomness — stub `Date.now()`, UUID generation, etc., with test doubles.
- Slow or destructive side effects (sending real emails, charging real cards).

### Stripe-specific pattern
Use Stripe's [test mode](https://docs.stripe.com/testing) for integration tests that hit real Stripe APIs with test keys. For unit tests, mock the Stripe client.

## End-to-end tests

E2E tests drive a real browser against the real app (or a production-like staging env). They catch what nothing else catches, but they're expensive and flaky if overused.

### Tools
- **Playwright** (recommended): fast, reliable, multi-browser, great debugging.
- Cypress: still popular, fine. Playwright has overtaken it for most teams.
- Selenium: only if you need a language or browser matrix Playwright doesn't cover.

### What to E2E test
Pick 3–10 "critical user journeys," the paths where regression would be catastrophic:
- Signup → email verify → first login
- Login → do the app's main action → logout
- Checkout / payment flow
- Password reset

Don't E2E test every feature. That's what integration tests are for.

### Keeping E2E stable
- Use `data-testid` attributes for selectors. Don't select by CSS class names — those change.
- Always wait on real signals (element visibility, network idle), never on arbitrary `sleep(2000)`.
- Reset test data between tests — a seed function that creates a known user and cleans up.
- Retry flaky tests automatically (Playwright has `retries: 2` in CI). But: chronic flake = real bug, investigate.
- Run in CI on a staging deployment, not locally-against-localhost (that's too hermetic).

## Frontend component tests

Between unit tests and E2E sits component testing — test a React/Vue component in isolation.

Tools: **Vitest + React Testing Library** (or Vue Testing Library). Playwright has a component testing mode too.

Useful for:
- Complex forms (validation states, error display)
- Stateful components (wizards, multi-step flows)
- Components with lots of conditional rendering

Not useful for:
- Pure presentational components (snapshot tests age badly)
- Things better covered by E2E (checkout flow, multi-page navigation)

## Type checks and linters are tests too

- `tsc --noEmit` or `mypy` or `go vet` in CI — catches a whole class of bugs before they hit the test suite.
- ESLint / Ruff with reasonable rules — catches bugs and enforces consistency.
- **Run them on every push.** Make CI fail on lint and type errors, not just test failures.

## Coverage — useful signal, bad target

- Track coverage as a signal of untested code, not a goal to hit.
- 80% coverage with meaningful assertions is much better than 100% with dumb tests.
- **Don't** set a coverage gate at 100% — it incentivizes test-shaped noise.
- **Do** look at coverage before a risky refactor to see what's untested.

## Speed matters

A slow test suite is one you won't run. Optimization targets:
- Unit suite: <10 seconds.
- Integration suite: <60 seconds.
- E2E: <5 minutes per critical-path run.

Techniques:
- **Parallel test runs** (Vitest, pytest-xdist, Go's `-parallel`).
- **Skip slow tests in watch mode**; run them in CI and pre-push.
- **Shared test DB** that only re-migrates when schema changes; transactions for isolation.
- **Mock external APIs** — a real HTTP call in a unit test suite is a bug.

## CI integration

Every PR runs:
1. Install deps
2. Lint
3. Typecheck
4. Unit + integration tests
5. Build
6. (Optional) E2E against a preview deployment

All must pass to merge. No "just this once."

## When tests fail in CI but pass locally

The usual culprits:
- **Time zone**: tests hardcode times or assume local TZ. Fix: always set `TZ=UTC` in CI; write tests that work in any TZ.
- **Order dependence**: test A leaves state test B relies on (or fights against). Fix: randomize test order, clean state between tests.
- **Flaky due to async race**: awaited wrong thing, or `setTimeout`-based waiting. Fix: wait on real signals.
- **Env var missing in CI**: tests silently used a local default. Fix: validate env on boot, fail loud.

## Test data — fixtures and factories

Prefer **factories** over static fixtures:

```ts
function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: randomUUID(),
    email: `user-${randomUUID()}@test.com`,
    name: 'Test User',
    createdAt: new Date(),
    ...overrides,
  };
}
```

Factories scale to new fields (new required field = update one place). Fixtures rot as the schema evolves.

Libraries: `fishery` (TS), `factory_boy` (Python), `factory` (Go).

## Property-based / fuzz tests (bonus)

For tricky pure functions (parsers, validators, state machines), property-based tests generate many inputs and check invariants:

```ts
import { fc, test } from '@fast-check/vitest';

test.prop([fc.integer(), fc.integer()])('add is commutative', (a, b) => {
  expect(add(a, b)).toBe(add(b, a));
});
```

Tools: `fast-check` (TS), `hypothesis` (Python), Go's built-in `f.Fuzz`.

Not necessary for most app code, but gold for parsers, domain logic, and anything security-sensitive.
