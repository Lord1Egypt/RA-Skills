# Code Smell Detection

## Long Functions

```typescript
// Bad: Function > 50 lines
function processMarketData() {
  // 100 lines of validation, transformation, saving...
}

// Good: Break into smaller functions
function processMarketData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

## Deep Nesting

```typescript
// Bad: 5+ levels of nesting
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // Do something
        }
      }
    }
  }
}

// Good: Use early returns
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return

// Do something
```

## Magic Numbers

```typescript
// Bad: Unexplained numbers
if (retryCount > 3) { }
setTimeout(callback, 500)
const fee = price * 0.15

// Good: Named constants
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500
const PROCESSING_FEE_RATE = 0.15

if (retryCount > MAX_RETRIES) { }
setTimeout(callback, DEBOUNCE_DELAY_MS)
const fee = price * PROCESSING_FEE_RATE
```

## Unused Code

```typescript
// Bad: Dead code commented out
function calculateTotal(items: Item[]) {
  // const subtotal = items.reduce((sum, item) => sum + item.price, 0)
  // const tax = subtotal * 0.08
  // return subtotal + tax
  return 0
}

// Good: Delete it, git history has it if needed
function calculateTotal(items: Item[]) {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0)
  const tax = subtotal * TAX_RATE
  return subtotal + tax
}
```

## Boolean Parameter Trap

```typescript
// Bad: Unclear what true/false means
function processData(data, true, false) { }
processData(data, true, false)  // What does this do?

// Good: Use explicit object or separate functions
function processData(data, options: {
  includeArchived: boolean
  sortDesc: boolean
}) { }

processData(data, { includeArchived: true, sortDesc: false })
```

## Too Many Parameters

```typescript
// Bad: Hard to remember parameter order
function createUser(
  name: string,
  email: string,
  age: number,
  isAdmin: boolean,
  isActive: boolean,
  lastLogin: Date,
  preferences: object
) { }

// Good: Use object for related parameters
interface CreateUserInput {
  name: string
  email: string
  age: number
  isAdmin?: boolean
  isActive?: boolean
  lastLogin?: Date
  preferences?: object
}

function createUser(input: CreateUserInput) { }
```

## Inconsistent Naming

```typescript
// Bad: Inconsistent patterns
function getUsers() { }        // fetch
function fetchMarkets() { }    // get
function listPositions() { }   // get/fetch

// Good: Consistent patterns
function getUsers() { }
function getMarkets() { }
function getPositions() { }

// Or for async operations:
async function fetchUsers() { }
async function fetchMarkets() { }
async function fetchPositions() { }
```

## Tight Coupling

```typescript
// Bad: Hard-coded dependencies
function processOrder(order) {
  const stripe = new Stripe(STRIPE_KEY)  // Tightly coupled
  stripe.charge(order.total)
}

// Good: Dependency injection
function processOrder(order, paymentProcessor: PaymentProcessor) {
  paymentProcessor.charge(order.total)
}

// Usage: swap implementations easily
processOrder(order, stripeProcessor)
processOrder(order, mockProcessor)  // For testing
```

## Incomplete Error Handling

```typescript
// Bad: Swallowing errors
try {
  await saveData(data)
} catch (error) {
  // Silent failure
}

// Good: Handle or re-throw with context
try {
  await saveData(data)
} catch (error) {
  logger.error('Failed to save data:', error)
  throw new Error('Data save failed', { cause: error })
}
```
