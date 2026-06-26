---
name: automatic-test-generator
description: Automatically generate unit tests from functions with comprehensive coverage and edge cases
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧪"
    homepage: https://jestjs.io
    requires:
      bins:
        - node
    os: ["macos", "linux", "windows"]
---

# Automatic Test Generator

Automatically generates comprehensive unit tests from your existing functions and classes. Analyzes function signatures, implementation details, and edge cases to create thorough test suites that improve code quality and catch bugs before production.

## What This Skill Does

This skill analyzes your code and generates complete, runnable unit tests including:

- **Test structure** following best practices (Arrange-Act-Assert pattern)
- **Happy path tests** for expected behavior
- **Edge case coverage** (null, undefined, empty arrays, boundary values)
- **Error handling tests** for exceptions and validation
- **Mock setup** for dependencies and external services
- **Type checking tests** for TypeScript
- **Integration test scaffolds** when appropriate

Supports multiple testing frameworks:
- **Jest** (JavaScript/TypeScript default)
- **Vitest** (modern, fast alternative)
- **Mocha + Chai** (traditional Node.js)
- **Pytest** (Python)
- **Go testing** (Go standard library)
- **JUnit** (Java)

## Why Use This Skill

### Saves Massive Time

Writing tests is time-consuming and often postponed:
- Manual test writing: 30-60 minutes per module
- With this skill: 2-3 minutes to generate + 5 minutes to review
- **Time saved: 80-90% per module**

### Improves Test Quality

- Catches edge cases developers often miss (null, empty, boundary values)
- Ensures consistent test structure across codebase
- Includes proper setup/teardown and mocking
- Follows framework-specific best practices

### Increases Coverage

- Tests all code paths (happy path, error cases, edge cases)
- Generates tests for existing untested legacy code
- Helps achieve 80%+ code coverage goals
- Includes assertion suggestions for complex return values

### Reduces Bugs

Studies show code with comprehensive tests has:
- 40-80% fewer production bugs
- Faster debugging when issues occur
- Better refactoring confidence
- Clearer documentation through test examples

## When to Use This Skill

Use this skill whenever you need tests:

- ✅ After writing new functions (TDD catch-up)
- ✅ For legacy code lacking tests
- ✅ When increasing coverage for CI/CD requirements
- ✅ Before refactoring (safety net for changes)
- ✅ During code review prep (show comprehensive testing)
- ✅ Learning test patterns for new frameworks
- ✅ Creating test templates for repetitive patterns

## When NOT to Use This Skill

- ❌ For already well-tested code (redundant effort)
- ❌ As a substitute for TDD (use TDD when starting fresh)
- ❌ For UI interaction tests (use Playwright/Cypress instead)
- ❌ For integration tests requiring real databases (this generates unit tests)
- ❌ When you need custom business logic assertions (review and customize generated tests)

## How It Works

### Step-by-Step Process

1. **Analyzes function signature**: Parameters, return type, TypeScript types
2. **Reads implementation**: Understands logic flow, conditionals, loops
3. **Identifies dependencies**: External calls, imports, side effects
4. **Detects edge cases**: Null checks, array operations, number boundaries
5. **Generates test structure**: describe/it blocks, setup, assertions
6. **Creates mocks**: For external dependencies (API calls, database, file system)
7. **Adds coverage**: Ensures all branches and paths are tested
8. **Formats output**: Follows project style guide and linting rules

### Test Generation Strategy

**For simple functions:**
- Basic input/output tests
- Edge case handling
- Type validation

**For complex functions:**
- Multiple test cases per code branch
- Mock setup for dependencies
- Error scenario coverage
- Integration test suggestions

**For classes:**
- Constructor tests
- Method tests with shared setup
- State management tests
- Inheritance/composition tests

## Usage Examples

### Example 1: Simple Utility Function

**Your code:**
```typescript
// src/utils/string.ts
export function capitalize(str: string): string {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
```

**Ask Claude:**
```
"Generate unit tests for the capitalize function in src/utils/string.ts"
```

**Generated tests:**
```typescript
// src/utils/string.test.ts
import { capitalize } from './string';

describe('capitalize', () => {
  it('should capitalize first letter of lowercase string', () => {
    expect(capitalize('hello')).toBe('Hello');
  });

  it('should capitalize and lowercase rest of string', () => {
    expect(capitalize('hELLO')).toBe('Hello');
  });

  it('should handle single character string', () => {
    expect(capitalize('a')).toBe('A');
  });

  it('should return empty string for empty input', () => {
    expect(capitalize('')).toBe('');
  });

  it('should return empty string for null input', () => {
    expect(capitalize(null as any)).toBe('');
  });

  it('should return empty string for undefined input', () => {
    expect(capitalize(undefined as any)).toBe('');
  });

  it('should handle string with spaces', () => {
    expect(capitalize('hello world')).toBe('Hello world');
  });

  it('should handle string with numbers', () => {
    expect(capitalize('123abc')).toBe('123abc');
  });

  it('should handle already capitalized string', () => {
    expect(capitalize('Hello')).toBe('Hello');
  });
});
```

### Example 2: Function with Dependencies

**Your code:**
```typescript
// src/api/users.ts
import { db } from './database';
import { cache } from './cache';

export async function getUser(id: string): Promise<User> {
  const cached = await cache.get(`user:${id}`);
  if (cached) return cached;

  const user = await db.users.findById(id);
  if (!user) throw new Error('User not found');

  await cache.set(`user:${id}`, user, { ttl: 300 });
  return user;
}
```

**Ask Claude:**
```
"Generate Jest tests for getUser function with proper mocking"
```

**Generated tests:**
```typescript
// src/api/users.test.ts
import { getUser } from './users';
import { db } from './database';
import { cache } from './cache';

jest.mock('./database');
jest.mock('./cache');

describe('getUser', () => {
  const mockUser = { id: '123', name: 'John Doe', email: 'john@example.com' };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return cached user if available', async () => {
    (cache.get as jest.Mock).mockResolvedValue(mockUser);

    const result = await getUser('123');

    expect(result).toEqual(mockUser);
    expect(cache.get).toHaveBeenCalledWith('user:123');
    expect(db.users.findById).not.toHaveBeenCalled();
  });

  it('should fetch from database when cache misses', async () => {
    (cache.get as jest.Mock).mockResolvedValue(null);
    (db.users.findById as jest.Mock).mockResolvedValue(mockUser);

    const result = await getUser('123');

    expect(result).toEqual(mockUser);
    expect(cache.get).toHaveBeenCalledWith('user:123');
    expect(db.users.findById).toHaveBeenCalledWith('123');
  });

  it('should cache user after database fetch', async () => {
    (cache.get as jest.Mock).mockResolvedValue(null);
    (db.users.findById as jest.Mock).mockResolvedValue(mockUser);

    await getUser('123');

    expect(cache.set).toHaveBeenCalledWith('user:123', mockUser, { ttl: 300 });
  });

  it('should throw error when user not found', async () => {
    (cache.get as jest.Mock).mockResolvedValue(null);
    (db.users.findById as jest.Mock).mockResolvedValue(null);

    await expect(getUser('999')).rejects.toThrow('User not found');
  });

  it('should not cache when user not found', async () => {
    (cache.get as jest.Mock).mockResolvedValue(null);
    (db.users.findById as jest.Mock).mockResolvedValue(null);

    await expect(getUser('999')).rejects.toThrow();
    expect(cache.set).not.toHaveBeenCalled();
  });

  it('should handle cache errors gracefully', async () => {
    (cache.get as jest.Mock).mockRejectedValue(new Error('Cache unavailable'));
    (db.users.findById as jest.Mock).mockResolvedValue(mockUser);

    // Should fallback to database when cache fails
    const result = await getUser('123');
    expect(result).toEqual(mockUser);
  });
});
```

### Example 3: Class with State

**Your code:**
```typescript
// src/services/counter.ts
export class Counter {
  private count: number = 0;

  increment(): number {
    this.count++;
    return this.count;
  }

  decrement(): number {
    this.count--;
    return this.count;
  }

  reset(): void {
    this.count = 0;
  }

  getValue(): number {
    return this.count;
  }
}
```

**Ask Claude:**
```
"Generate tests for Counter class"
```

**Generated tests:**
```typescript
// src/services/counter.test.ts
import { Counter } from './counter';

describe('Counter', () => {
  let counter: Counter;

  beforeEach(() => {
    counter = new Counter();
  });

  describe('increment', () => {
    it('should increment counter by 1', () => {
      expect(counter.increment()).toBe(1);
    });

    it('should increment multiple times correctly', () => {
      counter.increment();
      counter.increment();
      expect(counter.increment()).toBe(3);
    });

    it('should return current value after increment', () => {
      const result = counter.increment();
      expect(result).toBe(counter.getValue());
    });
  });

  describe('decrement', () => {
    it('should decrement counter by 1', () => {
      counter.increment(); // Set to 1 first
      expect(counter.decrement()).toBe(0);
    });

    it('should allow negative values', () => {
      expect(counter.decrement()).toBe(-1);
    });

    it('should decrement multiple times correctly', () => {
      counter.decrement();
      counter.decrement();
      expect(counter.decrement()).toBe(-3);
    });
  });

  describe('reset', () => {
    it('should reset counter to 0', () => {
      counter.increment();
      counter.increment();
      counter.reset();
      expect(counter.getValue()).toBe(0);
    });

    it('should reset from negative values', () => {
      counter.decrement();
      counter.reset();
      expect(counter.getValue()).toBe(0);
    });
  });

  describe('getValue', () => {
    it('should return initial value of 0', () => {
      expect(counter.getValue()).toBe(0);
    });

    it('should return current value after operations', () => {
      counter.increment();
      counter.increment();
      counter.decrement();
      expect(counter.getValue()).toBe(1);
    });
  });

  describe('integration', () => {
    it('should handle complex operation sequences', () => {
      counter.increment(); // 1
      counter.increment(); // 2
      counter.decrement(); // 1
      counter.increment(); // 2
      counter.reset();     // 0
      counter.decrement(); // -1

      expect(counter.getValue()).toBe(-1);
    });
  });
});
```

### Example 4: Async Function with Validation

**Your code:**
```typescript
// src/api/posts.ts
export async function createPost(title: string, content: string, authorId: string): Promise<Post> {
  if (!title || title.trim().length === 0) {
    throw new Error('Title is required');
  }
  if (!content || content.length < 10) {
    throw new Error('Content must be at least 10 characters');
  }
  if (!authorId) {
    throw new Error('Author ID is required');
  }

  const post = await db.posts.create({
    title: title.trim(),
    content,
    authorId,
    createdAt: new Date()
  });

  return post;
}
```

**Ask Claude:**
```
"Generate comprehensive tests for createPost with all validation cases"
```

**Generated tests:**
```typescript
// src/api/posts.test.ts
import { createPost } from './posts';
import { db } from './database';

jest.mock('./database');

describe('createPost', () => {
  const validTitle = 'Test Post';
  const validContent = 'This is valid content with enough characters';
  const validAuthorId = 'author-123';

  beforeEach(() => {
    jest.clearAllMocks();
    (db.posts.create as jest.Mock).mockResolvedValue({
      id: 'post-123',
      title: validTitle,
      content: validContent,
      authorId: validAuthorId,
      createdAt: expect.any(Date)
    });
  });

  describe('validation', () => {
    it('should throw error when title is empty', async () => {
      await expect(createPost('', validContent, validAuthorId))
        .rejects.toThrow('Title is required');
    });

    it('should throw error when title is only whitespace', async () => {
      await expect(createPost('   ', validContent, validAuthorId))
        .rejects.toThrow('Title is required');
    });

    it('should throw error when title is null', async () => {
      await expect(createPost(null as any, validContent, validAuthorId))
        .rejects.toThrow('Title is required');
    });

    it('should throw error when content is empty', async () => {
      await expect(createPost(validTitle, '', validAuthorId))
        .rejects.toThrow('Content must be at least 10 characters');
    });

    it('should throw error when content is less than 10 characters', async () => {
      await expect(createPost(validTitle, 'short', validAuthorId))
        .rejects.toThrow('Content must be at least 10 characters');
    });

    it('should throw error when authorId is missing', async () => {
      await expect(createPost(validTitle, validContent, ''))
        .rejects.toThrow('Author ID is required');
    });

    it('should throw error when authorId is null', async () => {
      await expect(createPost(validTitle, validContent, null as any))
        .rejects.toThrow('Author ID is required');
    });
  });

  describe('success cases', () => {
    it('should create post with valid data', async () => {
      const result = await createPost(validTitle, validContent, validAuthorId);

      expect(db.posts.create).toHaveBeenCalledWith({
        title: validTitle,
        content: validContent,
        authorId: validAuthorId,
        createdAt: expect.any(Date)
      });
      expect(result).toHaveProperty('id');
    });

    it('should trim whitespace from title', async () => {
      await createPost('  Trimmed Title  ', validContent, validAuthorId);

      expect(db.posts.create).toHaveBeenCalledWith(
        expect.objectContaining({ title: 'Trimmed Title' })
      );
    });

    it('should accept content exactly 10 characters', async () => {
      const result = await createPost(validTitle, '1234567890', validAuthorId);

      expect(result).toBeDefined();
    });

    it('should accept very long content', async () => {
      const longContent = 'a'.repeat(10000);
      const result = await createPost(validTitle, longContent, validAuthorId);

      expect(result).toBeDefined();
    });
  });

  describe('database integration', () => {
    it('should handle database errors', async () => {
      (db.posts.create as jest.Mock).mockRejectedValue(new Error('Database error'));

      await expect(createPost(validTitle, validContent, validAuthorId))
        .rejects.toThrow('Database error');
    });

    it('should include timestamp in created post', async () => {
      const beforeCreate = new Date();
      await createPost(validTitle, validContent, validAuthorId);
      const afterCreate = new Date();

      const createCall = (db.posts.create as jest.Mock).mock.calls[0][0];
      expect(createCall.createdAt.getTime()).toBeGreaterThanOrEqual(beforeCreate.getTime());
      expect(createCall.createdAt.getTime()).toBeLessThanOrEqual(afterCreate.getTime());
    });
  });
});
```

## Configuration

### Specify Testing Framework

```
"Generate Jest tests for this function"
"Create Vitest tests for this component"
"Write Pytest tests for this Python function"
"Generate Go tests for this package"
```

### Customize Coverage Level

```
"Generate basic tests with happy path only"
"Create comprehensive tests with all edge cases"
"Write tests for error scenarios only"
```

### Mock Configuration

```
"Generate tests with Jest mocks for dependencies"
"Create tests using manual mocks"
"Write tests without mocking (integration style)"
```

## Best Practices

### For Best Results

1. **Provide context**: Share related code (types, interfaces, dependencies)
2. **Specify framework**: Mention Jest, Vitest, Pytest, etc. if non-standard
3. **Review generated tests**: Always verify assertions match business logic
4. **Run tests immediately**: Ensure they pass before committing
5. **Customize as needed**: Generated tests are a starting point, refine them
6. **Keep functions small**: Smaller functions = better test generation

### Test Quality Checklist

After generation, verify:
- ✅ All code paths are covered (if/else, try/catch, loops)
- ✅ Edge cases are tested (null, empty, boundaries)
- ✅ Mocks are properly setup and reset
- ✅ Assertions are specific and meaningful
- ✅ Test names clearly describe what they test
- ✅ Setup and teardown are appropriate

### Integration with CI/CD

```bash
# package.json
{
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch"
  }
}

# Enforce coverage thresholds
# jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

## Framework-Specific Features

### Jest / Vitest

- Automatic mock generation
- Snapshot testing for complex objects
- Timer mocking for async operations
- Coverage reports

### Pytest

- Fixture generation
- Parametrized tests for multiple inputs
- Async test support
- Mock generation with unittest.mock

### Go Testing

- Table-driven test generation
- Benchmark tests
- Example tests for documentation
- Testify assertions

## Troubleshooting

### Issue: Generated tests don't pass

**Cause**: Implementation has bugs or generated assertions are incorrect.

**Solution**:
1. Run tests: `npm test`
2. Read error messages carefully
3. Fix implementation bugs OR adjust assertions
4. Common fixes:
   - Update expected values
   - Fix mock return values
   - Add missing setup

### Issue: Tests are too basic

**Cause**: Simple function with obvious behavior.

**Solution**: Ask for more comprehensive tests:
```
"Generate more edge case tests for this function"
"Add error scenario tests"
"Include boundary value tests"
```

### Issue: Missing mocks for dependencies

**Cause**: Claude didn't detect all dependencies.

**Solution**: Specify what to mock:
```
"Generate tests and mock the 'database' and 'logger' modules"
```

### Issue: Tests for TypeScript have type errors

**Cause**: Mock types don't match original.

**Solution**:
- Use `as jest.Mock` type assertions
- Install `@types/jest` or `@types/vitest`
- Use `jest.MockedFunction<typeof fn>` for better types

## Advanced Usage

### Test Data Builders

Generate test data factories:

```typescript
// Generated test builders
function buildUser(overrides?: Partial<User>): User {
  return {
    id: '123',
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  };
}
```

### Snapshot Testing

For complex output:

```typescript
it('should generate correct user profile', () => {
  const result = generateProfile(mockUser);
  expect(result).toMatchSnapshot();
});
```

### Parameterized Tests

For multiple similar cases:

```typescript
describe.each([
  ['hello', 'Hello'],
  ['WORLD', 'World'],
  ['tEsT', 'Test'],
])('capitalize(%s)', (input, expected) => {
  it(`should return ${expected}`, () => {
    expect(capitalize(input)).toBe(expected);
  });
});
```

### Coverage Reports

Generate and review coverage:

```bash
npm test -- --coverage

# View HTML report
open coverage/lcov-report/index.html
```

## Testing Patterns Reference

### Arrange-Act-Assert (AAA)

```typescript
it('should do something', () => {
  // Arrange: Setup test data
  const input = 'test';

  // Act: Execute function
  const result = doSomething(input);

  // Assert: Verify result
  expect(result).toBe('expected');
});
```

### Given-When-Then (BDD)

```typescript
it('should format user name when user has full name', () => {
  // Given: a user with first and last name
  const user = { firstName: 'John', lastName: 'Doe' };

  // When: formatting the name
  const result = formatUserName(user);

  // Then: should return full name
  expect(result).toBe('John Doe');
});
```

### Test Doubles Types

- **Stub**: Returns predefined values
- **Mock**: Verifies interactions
- **Spy**: Wraps real implementation
- **Fake**: Working implementation (simpler than real)
- **Dummy**: Placeholder (not used)

## Real-World Examples

### Before (No Tests)

```typescript
// src/utils/math.ts
export function divide(a: number, b: number): number {
  return a / b;
}

// ❌ No tests, bugs in production:
// divide(10, 0) => Infinity (should throw error)
// divide(null, 5) => NaN (should validate input)
```

### After (With Generated Tests)

```typescript
// Tests catch bugs during development
describe('divide', () => {
  it('should divide two positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should throw error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });

  it('should validate input types', () => {
    expect(() => divide(null as any, 5)).toThrow('Invalid input');
  });

  // Bug found! Implementation needs fixing.
});
```

## Code Coverage Goals

Industry standards:
- **Good**: 70-80% coverage
- **Excellent**: 80-90% coverage
- **Overkill**: 95%+ coverage (diminishing returns)

Focus on:
- Critical business logic (100% coverage)
- Error handling (100% coverage)
- Edge cases (high coverage)
- Simple getters/setters (optional)

## Related Resources

- [Jest Documentation](https://jestjs.io)
- [Vitest Documentation](https://vitest.dev)
- [Testing Library Best Practices](https://testing-library.com/docs/guiding-principles/)
- [Pytest Documentation](https://docs.pytest.org)
- [Test Driven Development (Kent Beck)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)

## Tips for Test-Driven Development (TDD)

While this skill helps write tests after code, consider using it to learn TDD:

1. **Red**: Generate tests first (they'll fail)
2. **Green**: Implement code to pass tests
3. **Refactor**: Improve code while tests ensure correctness

This reverses typical workflow but teaches TDD patterns.

---

**Pro Tip**: Use this skill to learn testing patterns, then gradually write tests yourself as you internalize best practices. The goal is test coverage, not dependency on automation!

**License**: MIT-0 (Public Domain)
