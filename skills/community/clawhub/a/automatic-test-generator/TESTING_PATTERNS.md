# Testing Patterns Quick Reference

## Common Test Patterns

### 1. Arrange-Act-Assert (AAA)

The most common pattern for structuring tests:

```typescript
it('should calculate total price with tax', () => {
  // Arrange
  const items = [{ price: 10 }, { price: 20 }];
  const taxRate = 0.1;

  // Act
  const total = calculateTotal(items, taxRate);

  // Assert
  expect(total).toBe(33); // (10 + 20) * 1.1
});
```

### 2. Given-When-Then (BDD)

Behavior-driven development style:

```typescript
describe('Shopping Cart', () => {
  it('should apply discount when total exceeds minimum', () => {
    // Given: a cart with items totaling $100
    const cart = new ShoppingCart();
    cart.addItem({ price: 100 });

    // When: applying a 10% discount for orders over $50
    const total = cart.getTotalWithDiscount({ min: 50, percent: 10 });

    // Then: should return $90
    expect(total).toBe(90);
  });
});
```

### 3. Setup-Exercise-Verify-Teardown

For integration tests:

```typescript
describe('Database Integration', () => {
  let connection;

  beforeEach(async () => {
    // Setup
    connection = await createTestDatabase();
    await connection.migrate();
  });

  afterEach(async () => {
    // Teardown
    await connection.close();
  });

  it('should save user to database', async () => {
    // Exercise
    await saveUser(connection, { name: 'John' });

    // Verify
    const users = await connection.query('SELECT * FROM users');
    expect(users).toHaveLength(1);
    expect(users[0].name).toBe('John');
  });
});
```

## Edge Cases to Test

### Null and Undefined

```typescript
it('should handle null input', () => {
  expect(processValue(null)).toBe(null);
});

it('should handle undefined input', () => {
  expect(processValue(undefined)).toBe(undefined);
});
```

### Empty Collections

```typescript
it('should handle empty array', () => {
  expect(sumArray([])).toBe(0);
});

it('should handle empty string', () => {
  expect(capitalize('')).toBe('');
});

it('should handle empty object', () => {
  expect(hasRequiredFields({})).toBe(false);
});
```

### Boundary Values

```typescript
describe('age validation', () => {
  it('should reject age below minimum', () => {
    expect(isValidAge(17)).toBe(false);
  });

  it('should accept age at minimum', () => {
    expect(isValidAge(18)).toBe(true);
  });

  it('should accept age above minimum', () => {
    expect(isValidAge(19)).toBe(true);
  });

  it('should reject age above maximum', () => {
    expect(isValidAge(121)).toBe(false);
  });

  it('should accept age at maximum', () => {
    expect(isValidAge(120)).toBe(true);
  });
});
```

### Large Inputs

```typescript
it('should handle very long strings', () => {
  const longString = 'a'.repeat(10000);
  expect(() => processString(longString)).not.toThrow();
});

it('should handle large arrays', () => {
  const largeArray = Array(1000000).fill(1);
  expect(sumArray(largeArray)).toBe(1000000);
});
```

### Special Characters

```typescript
it('should handle special characters in email', () => {
  expect(validateEmail('user+tag@example.com')).toBe(true);
});

it('should handle unicode in username', () => {
  expect(sanitizeUsername('José')).toBe('José');
});
```

## Mocking Patterns

### Function Mocks

```typescript
const mockCallback = jest.fn();
mockCallback.mockReturnValue(42);
mockCallback.mockReturnValueOnce(1).mockReturnValueOnce(2);
mockCallback.mockResolvedValue('async result');
mockCallback.mockRejectedValue(new Error('async error'));
```

### Module Mocks

```typescript
jest.mock('./api', () => ({
  fetchUser: jest.fn(),
  saveUser: jest.fn()
}));

import { fetchUser } from './api';
(fetchUser as jest.Mock).mockResolvedValue({ id: 1 });
```

### Partial Mocks

```typescript
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  expensiveOperation: jest.fn() // Only mock this one
}));
```

### Class Mocks

```typescript
jest.mock('./Database');
import { Database } from './Database';

const mockDatabase = Database as jest.MockedClass<typeof Database>;
mockDatabase.prototype.query.mockResolvedValue([]);
```

## Assertion Patterns

### Exact Equality

```typescript
expect(value).toBe(42);
expect(value).toEqual({ id: 1, name: 'John' });
```

### Partial Matching

```typescript
expect(user).toMatchObject({ name: 'John' });
expect(array).toEqual(expect.arrayContaining([1, 2]));
expect(obj).toEqual(expect.objectContaining({ id: 1 }));
```

### Type Checking

```typescript
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeInstanceOf(Date);
```

### Numeric Assertions

```typescript
expect(value).toBeGreaterThan(10);
expect(value).toBeLessThan(100);
expect(value).toBeCloseTo(0.3, 5); // Floating point
```

### String Assertions

```typescript
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');
expect(str).toHaveLength(10);
```

### Array Assertions

```typescript
expect(array).toHaveLength(3);
expect(array).toContain(item);
expect(array).toContainEqual({ id: 1 });
```

### Error Assertions

```typescript
expect(() => throwError()).toThrow();
expect(() => throwError()).toThrow('message');
expect(() => throwError()).toThrow(TypeError);
expect(asyncFn()).rejects.toThrow();
```

## Test Organization

### Nested Describes

```typescript
describe('UserService', () => {
  describe('create', () => {
    it('should create user with valid data', () => {});
    it('should throw error with invalid data', () => {});
  });

  describe('update', () => {
    it('should update existing user', () => {});
    it('should throw error for non-existent user', () => {});
  });
});
```

### Shared Setup

```typescript
describe('Calculator', () => {
  let calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  afterEach(() => {
    calculator = null;
  });

  it('should add numbers', () => {
    expect(calculator.add(2, 3)).toBe(5);
  });
});
```

### Test Factories

```typescript
function createUser(overrides = {}) {
  return {
    id: '123',
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  };
}

it('should format user name', () => {
  const user = createUser({ name: 'John Doe' });
  expect(formatName(user)).toBe('John Doe');
});
```

## Coverage Targets

### Statement Coverage

```typescript
function example(x) {
  if (x > 0) {
    return 'positive';  // Need test with x > 0
  }
  return 'non-positive'; // Need test with x <= 0
}
```

### Branch Coverage

```typescript
function validate(x) {
  if (x && x.valid) {  // Need: x=null, x={valid:false}, x={valid:true}
    return true;
  }
  return false;
}
```

### Path Coverage

```typescript
function complex(a, b) {
  if (a > 0) {
    if (b > 0) {
      return 'both positive';    // Path 1
    }
    return 'a positive';         // Path 2
  }
  if (b > 0) {
    return 'b positive';         // Path 3
  }
  return 'neither positive';     // Path 4
}
// Need 4 tests for full path coverage
```

## Anti-Patterns to Avoid

### ❌ Testing Implementation Details

```typescript
// Bad
it('should call helper function', () => {
  const spy = jest.spyOn(obj, 'helperMethod');
  obj.publicMethod();
  expect(spy).toHaveBeenCalled();
});

// Good
it('should return correct result', () => {
  expect(obj.publicMethod()).toBe(expected);
});
```

### ❌ Overly Complex Tests

```typescript
// Bad
it('should do many things', () => {
  const user = createUser();
  user.login();
  user.updateProfile();
  user.addFriend(otherUser);
  expect(user.friends).toContain(otherUser);
  expect(user.profile).toBeDefined();
  expect(user.isLoggedIn).toBe(true);
});

// Good - split into separate tests
it('should log in user', () => {});
it('should update profile', () => {});
it('should add friend', () => {});
```

### ❌ Brittle Tests

```typescript
// Bad - breaks on any change
expect(result).toEqual({
  id: 1,
  name: 'John',
  email: 'john@example.com',
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z',
  metadata: { ... }
});

// Good - test what matters
expect(result).toMatchObject({
  id: expect.any(Number),
  name: 'John',
  email: 'john@example.com'
});
```

### ❌ Unclear Test Names

```typescript
// Bad
it('test 1', () => {});
it('works', () => {});
it('should return true', () => {}); // True for what?

// Good
it('should return true when user is authenticated', () => {});
it('should throw error when email is invalid', () => {});
```

## Performance Testing Patterns

### Timing Tests

```typescript
it('should complete in under 100ms', async () => {
  const start = Date.now();
  await performOperation();
  const duration = Date.now() - start;
  expect(duration).toBeLessThan(100);
});
```

### Memory Tests

```typescript
it('should not leak memory', () => {
  const before = process.memoryUsage().heapUsed;

  for (let i = 0; i < 1000; i++) {
    createAndDestroyObject();
  }

  global.gc(); // Requires --expose-gc flag
  const after = process.memoryUsage().heapUsed;
  const increase = after - before;

  expect(increase).toBeLessThan(1000000); // 1MB threshold
});
```

## Snapshot Testing

```typescript
it('should match snapshot', () => {
  const component = render(<UserProfile user={mockUser} />);
  expect(component).toMatchSnapshot();
});

// Update snapshots when intentionally changed
// npm test -- -u
```

## Parameterized Tests

```typescript
describe.each([
  [1, 1, 2],
  [2, 2, 4],
  [3, 3, 6],
])('add(%i, %i)', (a, b, expected) => {
  it(`should return ${expected}`, () => {
    expect(add(a, b)).toBe(expected);
  });
});
```

## Async Testing Patterns

### Promises

```typescript
it('should resolve with user data', () => {
  return fetchUser('123').then(user => {
    expect(user.id).toBe('123');
  });
});
```

### Async/Await

```typescript
it('should fetch user data', async () => {
  const user = await fetchUser('123');
  expect(user.id).toBe('123');
});
```

### Callbacks

```typescript
it('should call callback with result', (done) => {
  fetchUser('123', (err, user) => {
    expect(user.id).toBe('123');
    done();
  });
});
```

## Test Doubles Decision Tree

```
Need to verify function was called?
  YES → Use Mock (jest.fn())
  NO ↓

Need to control return value?
  YES → Use Stub (mockReturnValue)
  NO ↓

Need to track calls but use real implementation?
  YES → Use Spy (jest.spyOn)
  NO ↓

Need simplified version of complex system?
  YES → Use Fake (in-memory database)
  NO ↓

Just need something to compile?
  YES → Use Dummy (empty object)
```

## Summary

Good tests are:
- ✅ **Isolated** - Don't depend on other tests
- ✅ **Repeatable** - Same result every time
- ✅ **Fast** - Run quickly for rapid feedback
- ✅ **Clear** - Test names describe behavior
- ✅ **Focused** - Test one thing per test
- ✅ **Maintainable** - Easy to update when code changes
