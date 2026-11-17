# Web Development TDD Best Practices

## Frontend Testing Stack

### Framework Recommendations

| Type              | Tool                                                        | Notes                         |
| ----------------- | ----------------------------------------------------------- | ----------------------------- |
| Test Runner       | Vitest                                                      | Fast, modern, Jest-compatible |
| Component Testing | @testing-library/react (React) / @testing-library/vue (Vue) | User-centric testing          |
| E2E Testing       | Playwright / Cypress                                        | Browser automation            |
| Mock API          | MSW (Mock Service Worker)                                   | Intercept network requests    |

### Setup (React + Vitest + Testing Library)

```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

### Component Test Example

```typescript
// UserProfile.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { UserProfile } from "./UserProfile";

describe("UserProfile", () => {
  it("displays user name", () => {
    // Arrange
    const user = { name: "Alice", email: "alice@example.com" };

    // Act
    render(<UserProfile user={user} />);

    // Assert
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });

  it("calls onEdit when edit button clicked", () => {
    // Arrange
    const onEdit = vi.fn();
    const user = { name: "Alice", email: "alice@example.com" };

    // Act
    render(<UserProfile user={user} onEdit={onEdit} />);
    fireEvent.click(screen.getByRole("button", { name: /edit/i }));

    // Assert
    expect(onEdit).toHaveBeenCalledWith(user);
  });

  it("displays loading state", () => {
    render(<UserProfile loading={true} />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

### API Mocking with MSW

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users/:id", ({ params }) => {
    return HttpResponse.json({ id: params.id, name: "Alice" });
  }),

  http.post("/api/users", async ({ request }) => {
    const data = await request.json();
    return HttpResponse.json({ id: "123", ...data }, { status: 201 });
  }),
];

// mocks/browser.ts
import { setupWorker } from "msw/browser";
import { handlers } from "./handlers";
export const worker = setupWorker(...handlers);
```

### E2E Test Example (Playwright)

```typescript
// e2e/user-flow.spec.ts
import { test, expect } from "@playwright/test";

test("user can log in and see dashboard", async ({ page }) => {
  // Arrange
  await page.goto("http://localhost:3000");

  // Act
  await page.fill('[name="email"]', "user@example.com");
  await page.fill('[name="password"]', "password123");
  await page.click('button[type="submit"]');

  // Assert
  await expect(page).toHaveURL(/.*dashboard/);
  await expect(page.getByText("Welcome")).toBeVisible();
});
```

## Backend Testing (Node.js/Express)

### Setup

```bash
npm install --save-dev supertest
```

### API Test Example

```typescript
// api/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { app } from "../src/app";
import { db } from "../src/db";

describe("Users API", () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  afterAll(async () => {
    await db.destroy();
  });

  describe("GET /api/users/:id", () => {
    it("returns user when found", async () => {
      // Arrange
      await db("users").insert({ id: "1", name: "Alice" });

      // Act
      const response = await request(app).get("/api/users/1").expect(200);

      // Assert
      expect(response.body).toMatchObject({ id: "1", name: "Alice" });
    });

    it("returns 404 when user not found", async () => {
      await request(app).get("/api/users/nonexistent").expect(404);
    });
  });

  describe("POST /api/users", () => {
    it("creates a new user", async () => {
      const response = await request(app)
        .post("/api/users")
        .send({ name: "Bob", email: "bob@example.com" })
        .expect(201);

      expect(response.body).toHaveProperty("id");
      expect(response.body.name).toBe("Bob");
    });
  });
});
```

## Best Practices

- Test user behavior, not implementation details
- Use `data-testid` only when necessary (prefer accessible queries)
- Keep component tests isolated (mock API calls)
- Use MSW for realistic API mocking
- E2E tests: test critical paths only (slow)
- Backend: test API contracts (status codes, response shape)
- Use test fixtures/factories for test data
- Aim for: 70%+ unit test coverage, 100% critical path coverage
