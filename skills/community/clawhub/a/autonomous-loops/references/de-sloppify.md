# De-Sloppify Pattern — Quality Cleanup Pass

An add-on pattern for any loop: add a dedicated cleanup/refactor step after implementation.

## The Problem

When you ask an LLM to implement with TDD, it takes "be thorough" too literally:

- Tests that verify TypeScript's type system works (e.g., `typeof x === 'string'`)
- Overly defensive runtime checks for things the type system already enforces
- Tests for framework behavior rather than business logic
- Excessive error handling that obscures actual code
- Console.log statements left behind

## Why Not Negative Instructions?

Adding "don't test type systems" or "don't add unnecessary checks" to the implementation prompt has downstream effects:

- Model becomes hesitant about ALL testing
- Skips legitimate edge case tests
- Quality degrades unpredictably

## The Solution: Separate Pass

Let the implementer be thorough. Then add a focused cleanup agent:

```bash
# Step 1: Implement (be thorough)
claude -p "Implement the feature with full TDD. Be thorough with tests."

# Step 2: Clean up (separate context, focused cleanup)
claude -p "Review all changes. Remove:
- Tests that verify language/framework behavior (not business logic)
- Redundant type checks the type system already enforces
- Overly defensive error handling for impossible states
- Console.log and debug statements
- Commented-out code

Keep all business logic tests. Run test suite after cleanup to verify nothing breaks."
```

## In a Loop

```bash
for feature in "${features[@]}"; do
  # Implement
  claude -p "Implement $feature with TDD."

  # De-sloppify
  claude -p "Cleanup: review changes, remove test/code slop, run tests."

  # Verify
  claude -p "Build + lint + tests. Fix failures."

  # Commit
  claude -p "Commit: feat: add $feature"
done
```

## What to Remove

### Type System Tests (❌ Remove)

```typescript
// Tests that TypeScript guarantees
test('string is a string', () => {
  const s: string = 'hello'
  expect(typeof s).toBe('string')  // Remove: type system ensures this
})

// Tests for generics working
test('generic array stores any type', () => {
  const arr: string[] = ['a', 'b']
  expect(arr.length).toBe(2)  // Remove: testing language features
})
```

### Redundant Checks (❌ Remove)

```typescript
// Type system says id is string, but code checks at runtime
function getUser(id: string) {
  if (typeof id !== 'string') {  // Remove: type system guarantees this
    throw new Error('id must be string')
  }
  return users[id]
}
```

### Overly Defensive Error Handling (❌ Remove)

```typescript
// Handling impossible states
try {
  const sum = a + b
  if (isNaN(sum)) {  // Remove: impossible with number types
    throw new Error('NaN result')
  }
} catch (error) {
  // ...
}
```

### What to Keep (✅ Keep)

#### Business logic tests

```typescript
test('applies coupon discount correctly', () => {
  const total = 100
  const discounted = applyCoupon(total, 'SAVE10')
  expect(discounted).toBe(90)  // Keep: tests actual behavior
})
```

#### Edge case tests

```typescript
test('handles empty order gracefully', () => {
  const result = calculateTotal([])
  expect(result).toBe(0)  // Keep: edge case
})
```

#### Integration tests

```typescript
test('creates user and sends welcome email', async () => {
  const user = await createUser({ name: 'Alice' })
  expect(emailService.send).toHaveBeenCalledWith(user.email)  // Keep: integration
})
```

## Key Insight

> Rather than adding negative instructions (which constrain the model), use a separate cleanup pass. Two focused agents outperform one constrained agent.

**Agent 1:** "Be thorough, implement with all tests"
**Agent 2:** "Remove unnecessary defensive code"

Better than:

**Agent 1:** "Implement with tests, but don't test type systems, and don't over-defensive code handling..."

## When Not to De-Sloppify

- Simple one-line changes
- Code review already performed by human
- Testing is not the focus
- Time/cost constraints (cleanup pass costs tokens)
