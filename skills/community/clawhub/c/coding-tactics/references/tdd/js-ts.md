# JavaScript/TypeScript TDD Best Practices

## Test Framework: Jest (Node.js) / Vitest (modern alternative)

### Setup

```bash
# Jest
npm install --save-dev jest @types/jest
# TypeScript
npm install --save-dev ts-jest @types/jest

# Vitest (recommended for modern projects)
npm install --save-dev vitest @vitest/ui
```

### Test Structure (Jest)

```javascript
// math.test.js
const { add, divide } = require("./math");

describe("add", () => {
  test("adds two positive numbers", () => {
    expect(add(1, 2)).toBe(3);
  });

  test("handles negative numbers", () => {
    expect(add(-1, -2)).toBe(-3);
  });
});

describe("divide", () => {
  test("divides two numbers", () => {
    expect(divide(6, 2)).toBe(3);
  });

  test("throws on division by zero", () => {
    expect(() => divide(1, 0)).toThrow("division by zero");
  });
});
```

### Test Structure (TypeScript + Vitest)

```typescript
// math.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { UserService } from "./UserService";
import { ApiClient } from "./ApiClient";

describe("UserService", () => {
  let service: UserService;
  let mockApi: ApiClient;

  beforeEach(() => {
    mockApi = { fetch: vi.fn() } as unknown as ApiClient;
    service = new UserService(mockApi);
  });

  it("should return user data when API succeeds", async () => {
    // Arrange
    mockApi.fetch = vi.fn().mockResolvedValue({ id: "1", name: "Alice" });

    // Act
    const result = await service.getUser("1");

    // Assert
    expect(result.name).toBe("Alice");
    expect(mockApi.fetch).toHaveBeenCalledWith("/users/1");
  });

  it("should throw when API fails", async () => {
    mockApi.fetch = vi.fn().mockRejectedValue(new Error("Network error"));

    await expect(service.getUser("1")).rejects.toThrow("Network error");
  });
});
```

### Mocking

```javascript
// Jest mocks
// Manual mock
jest.mock("./ApiClient", () => ({
  fetch: jest.fn().mockResolvedValue({ data: 1 }),
}));

// Function mock
const mockFn = jest.fn();
mockFn.mockReturnValue(42);

// Vitest mocks
import { vi } from "vitest";
vi.mock("./ApiClient");
const { ApiClient } = await import("./ApiClient");
ApiClient.prototype.fetch = vi.fn();
```

## Best Practices

- Use `describe` to group related tests
- Use `it`/`test` (prefer `it` for readability)
- AAA pattern: Arrange, Act, Assert
- Mock at boundaries (API, database, filesystem)
- Use `beforeEach` for setup (DRY)
- Test both happy path and error cases
- Use `toThrow` for exception testing
