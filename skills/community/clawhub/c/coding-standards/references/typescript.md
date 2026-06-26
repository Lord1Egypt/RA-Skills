# TypeScript & JavaScript Standards

## Type Safety

```typescript
// Good: Explicit interfaces
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> {
  // Implementation
}

// Bad: Using 'any'
function getMarket(id: any): Promise<any> {
  // Implementation
}
```

## Immutability Pattern (CRITICAL)

```typescript
// Good: Always use spread operator
const updatedUser = { ...user, name: 'New Name' }
const updatedArray = [...items, newItem]

// Bad: Never mutate directly
user.name = 'New Name'  // WRONG
items.push(newItem)     // WRONG
```

## Error Handling

```typescript
// Good: Comprehensive error handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}

// Bad: No error handling
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()
}
```

## Async/Await Best Practices

```typescript
// Good: Parallel execution when possible
const [users, markets] = await Promise.all([
  fetchUsers(),
  fetchMarkets()
])

// Bad: Sequential when unnecessary
const users = await fetchUsers()
const markets = await fetchMarkets()
```

## Retry with Exponential Backoff

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      if (i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }

  throw lastError!
}
```

## Comments

Write comments that explain **WHY**, not **WHAT**:

```typescript
// Good: Why
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)
// Exponential backoff prevents overwhelming API during outages

// Bad: What (obvious from code)
count++  // Increment counter by 1
```

## JSDoc for Public APIs

```typescript
/**
 * Searches markets using semantic similarity.
 *
 * @param query - Natural language search query
 * @param limit - Maximum number of results (default: 10)
 * @returns Markets sorted by similarity score
 * @throws {Error} If OpenAI API fails
 *
 * @example
 * const results = await searchMarkets('election', 5)
 */
export async function searchMarkets(
  query: string,
  limit: number = 10
): Promise<Market[]> {
  // Implementation
}
```
