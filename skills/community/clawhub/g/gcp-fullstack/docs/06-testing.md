> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Part 15: Testing

Write and run tests for GCP-hosted projects. Detect the test framework in use and adapt. This replaces the need for a separate test-sentinel skill.

### Framework Detection

```bash
# Detect test runner
if [ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ]; then
  TEST_RUNNER="vitest"
elif [ -f "jest.config.ts" ] || [ -f "jest.config.js" ]; then
  TEST_RUNNER="jest"
else
  TEST_RUNNER="vitest"  # default, install if missing
fi

# Detect E2E framework
if [ -f "playwright.config.ts" ]; then
  E2E_RUNNER="playwright"
elif [ -f "cypress.config.ts" ] || [ -f "cypress.config.js" ]; then
  E2E_RUNNER="cypress"
else
  E2E_RUNNER="playwright"  # default
fi
```

### Unit Tests

For: utility functions, Zod schemas, data transformations, hooks, stores.

Location: `src/**/__tests__/<name>.test.ts` (colocated with the code being tested).

```typescript
import { describe, it, expect } from "vitest"; // or jest
import { formatCurrency } from "@/lib/utils";

describe("formatCurrency", () => {
  it("formats BRL correctly", () => {
    expect(formatCurrency(1999, "BRL")).toBe("R$ 19,99");
  });

  it("handles zero", () => {
    expect(formatCurrency(0, "BRL")).toBe("R$ 0,00");
  });
});
```

### Integration Tests

For: API routes, Server Actions, data access functions. Mock the database client.

```typescript
import { describe, it, expect, vi } from "vitest";

// Mock Firestore
vi.mock("@/lib/db/firestore", () => ({
  db: {
    collection: vi.fn(() => ({
      add: vi.fn(() => ({ id: "mock-id" })),
      doc: vi.fn(() => ({
        get: vi.fn(() => ({ exists: true, data: () => ({ name: "Test" }) })),
      })),
      where: vi.fn(() => ({
        get: vi.fn(() => ({
          docs: [{ id: "1", data: () => ({ name: "Test" }) }],
        })),
      })),
    })),
  },
}));

// OR mock Prisma
vi.mock("@/lib/db/sql", () => ({
  prisma: {
    entity: {
      findMany: vi.fn(() => [{ id: "1", name: "Test" }]),
      create: vi.fn((args) => ({ id: "new-id", ...args.data })),
    },
  },
}));
```

### E2E Tests (Playwright)

For: critical user flows (auth, main feature happy paths).

```typescript
import { test, expect } from "@playwright/test";

test.describe("Entity CRUD Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Login (use storageState or test account)
    await page.goto("/login");
    await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!);
    await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!);
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");
  });

  test("create, view, and delete entity", async ({ page }) => {
    // Create
    await page.goto("/entities/new");
    await page.fill('[name="name"]', "Test Entity");
    await page.click('button[type="submit"]');
    await expect(page.locator('[data-sonner-toast]')).toContainText(/created|success/i);

    // View
    await page.goto("/entities");
    await expect(page.locator("text=Test Entity")).toBeVisible();

    // Delete
    await page.click('[data-testid="delete-entity"]');
    await page.click('button:has-text("Confirm")');
    await expect(page.locator('[data-sonner-toast]')).toContainText(/deleted/i);
  });
});
```

### Running Tests

```bash
# Full suite
npx vitest run && npx playwright test

# With coverage
npx vitest run --coverage

# Specific file
npx vitest run src/lib/__tests__/utils.test.ts

# E2E only
npx playwright test e2e/entities.spec.ts
```

### Failure Analysis Workflow

1. Read the error output. Identify: test bug vs code bug.
2. If test bug: fix the test (wrong expectation, missing mock, outdated snapshot).
3. If code bug: fix the source code, re-run the failing test to confirm.
4. If flaky: add retry logic or improve isolation. Mark with `// TODO: flaky`.
5. Re-run the full suite after any fix.
6. Commit: `test: fix <description>`.

### Linting and Type Checking

```bash
# Lint
npx eslint . --ext .ts,.tsx
npx eslint . --ext .ts,.tsx --fix  # auto-fix

# Type check
npx tsc --noEmit

# Format
npx prettier --check .
npx prettier --write .  # auto-fix
```

### Test Data Patterns

Use factory functions, not raw objects:

```typescript
// src/__tests__/__fixtures__/factories.ts
export function makeUser(overrides = {}) {
  return {
    id: "test-user-id",
    email: "test@example.com",
    displayName: "Test User",
    ...overrides,
  };
}

export function makeEntity(overrides = {}) {
  return {
    id: "test-entity-id",
    name: "Test Entity",
    userId: "test-user-id",
    createdAt: new Date().toISOString(),
    ...overrides,
  };
}
```

### Quality Gates (before reporting "all tests pass")

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] E2E tests pass (if applicable)
- [ ] No lint errors
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] Coverage does not decrease
