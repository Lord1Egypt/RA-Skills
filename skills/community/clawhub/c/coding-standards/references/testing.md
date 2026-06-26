# Testing Standards

## AAA Pattern (Arrange, Act, Assert)

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})
```

## Test Naming

```typescript
// Good: Descriptive names
test('returns empty array when no markets match query', () => {})
test('throws error when OpenAI API key is missing', () => {})
test('falls back to substring search when Redis unavailable', () => {})

// Bad: Vague names
test('works', () => {})
test('test search', () => {})
```

## Testing Patterns

### Happy Path Test

```typescript
test('successfully creates market with valid data', () => {
  const input = {
    name: 'Election 2024',
    description: 'US Presidential Election',
    endDate: '2024-11-05'
  }

  const market = createMarket(input)

  expect(market.id).toBeDefined()
  expect(market.name).toBe('Election 2024')
})
```

### Error Handling Test

```typescript
test('throws ValidationError when name is too long', () => {
  const input = { name: 'x'.repeat(300) }

  expect(() => createMarket(input)).toThrow(ValidationError)
})
```

### Edge Case Test

```typescript
test('handles empty string query gracefully', () => {
  const results = searchMarkets('')

  expect(results).toEqual([])
  expect(results).not.toThrow()
})
```

## Mocking

```typescript
// Mock external dependency
jest.mock('@/lib/api/openai')

test('falls back when OpenAI is unavailable', async () => {
  const openai = require('@/lib/api/openai')
  openai.generateEmbedding.mockRejectedValue(new Error('API down'))

  const results = await searchMarkets('query')

  expect(results).toBeDefined()  // Falls back to substring search
})
```

## Test File Organization

```bash
src/
├── lib/
│   ├── api.ts
│   └── api.test.ts        # Test right next to code
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx    # Collocate tests with components
├── __tests__/             # For shared test utilities
│   ├── fixtures.ts
│   └── mocks.ts
```

## What NOT to Test

❌ Language/framework behavior (TypeScript generics, React hooks internals)
❌ Library functionality (testing that `array.push()` works)
❌ UI implementation details (exact CSS class names)
✅ Business logic
✅ Edge cases and error states
✅ Integration between modules
✅ User workflows
