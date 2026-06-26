# Code Review Checklist

A comprehensive checklist of patterns to check during code review, organized by category.

## Security Vulnerabilities

### Injection Attacks

#### SQL Injection [CWE-89]

❌ **Vulnerable**:
```javascript
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.execute(query);
```

✅ **Secure**:
```javascript
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [userId]);
```

**Detection**: Look for string concatenation or template literals building SQL queries

---

#### NoSQL Injection

❌ **Vulnerable**:
```javascript
db.users.find({ username: req.body.username });
// Attack: { username: { $gt: "" } } returns all users
```

✅ **Secure**:
```javascript
const username = String(req.body.username);
if (!/^[a-zA-Z0-9_]+$/.test(username)) {
  throw new Error('Invalid username');
}
db.users.find({ username });
```

---

#### Command Injection [CWE-78]

❌ **Vulnerable**:
```python
import os
filename = request.args.get('file')
os.system(f'cat {filename}')  # Attack: file=test.txt; rm -rf /
```

✅ **Secure**:
```python
import subprocess
filename = sanitize_filename(request.args.get('file'))
subprocess.run(['cat', filename], check=True)
```

---

#### XSS (Cross-Site Scripting) [CWE-79]

❌ **Vulnerable**:
```javascript
document.getElementById('output').innerHTML = userInput;
// Attack: <script>steal_cookies()</script>
```

✅ **Secure**:
```javascript
document.getElementById('output').textContent = userInput;
// Or use framework escaping (React, Vue auto-escape)
```

---

### Authentication & Authorization

#### Missing Authentication

❌ **Missing**:
```javascript
app.delete('/api/users/:id', (req, res) => {
  deleteUser(req.params.id);
  res.json({ success: true });
});
```

✅ **Protected**:
```javascript
app.delete('/api/users/:id',
  authenticateUser,
  authorizeAdmin,
  (req, res) => {
    deleteUser(req.params.id);
    res.json({ success: true });
  }
);
```

---

#### Weak Password Requirements

❌ **Weak**:
```python
if len(password) < 6:
    raise ValueError("Password too short")
```

✅ **Strong**:
```python
if len(password) < 12:
    raise ValueError("Password must be at least 12 characters")
if not re.search(r'[A-Z]', password):
    raise ValueError("Password must contain uppercase letter")
if not re.search(r'[0-9]', password):
    raise ValueError("Password must contain number")
if not re.search(r'[^A-Za-z0-9]', password):
    raise ValueError("Password must contain special character")
```

---

#### Insecure Token Storage

❌ **Insecure**:
```javascript
localStorage.setItem('authToken', token);  // Vulnerable to XSS
```

✅ **Secure**:
```javascript
// Use httpOnly cookie (server-side)
res.cookie('authToken', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});
```

---

### Data Exposure

#### Exposed Secrets

❌ **Exposed**:
```javascript
const API_KEY = 'YOUR_API_KEY_HERE';
const dbPassword = 'YOUR_DB_PASSWORD_HERE';
```

✅ **Secure**:
```javascript
const API_KEY = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;
```

**Check for**:
- API keys hardcoded
- Passwords in source
- AWS/GCP credentials
- Private keys
- JWT secrets

---

#### Information Disclosure

❌ **Leaks Info**:
```javascript
catch (err) {
  res.status(500).json({ error: err.stack });
  // Exposes: file paths, library versions, database structure
}
```

✅ **Safe**:
```javascript
catch (err) {
  logger.error('Database error:', err);
  res.status(500).json({ error: 'Internal server error' });
}
```

---

#### Sensitive Data in Logs

❌ **Logs Secrets**:
```python
logger.info(f"User login: {username}, password: {password}")
logger.debug(f"Credit card: {card_number}")
```

✅ **Safe Logging**:
```python
logger.info(f"User login: {username}")
logger.debug(f"Credit card: {mask_card(card_number)}")
```

---

### Mass Assignment

❌ **Vulnerable**:
```javascript
const user = await User.findById(req.params.id);
Object.assign(user, req.body);  // User can set isAdmin: true
await user.save();
```

✅ **Protected**:
```javascript
const allowedFields = ['name', 'email', 'bio'];
const updates = pick(req.body, allowedFields);
const user = await User.findById(req.params.id);
Object.assign(user, updates);
await user.save();
```

---

### CSRF (Cross-Site Request Forgery)

❌ **Missing Protection**:
```javascript
app.post('/api/transfer', (req, res) => {
  transfer(req.user.id, req.body.amount, req.body.to);
});
```

✅ **CSRF Protected**:
```javascript
app.post('/api/transfer',
  csrfProtection,  // Validates CSRF token
  (req, res) => {
    transfer(req.user.id, req.body.amount, req.body.to);
  }
);
```

---

## Bug Patterns

### Null/Undefined Handling

#### Missing Null Check

❌ **Bug**:
```javascript
function formatUser(user) {
  return `${user.firstName} ${user.lastName}`;  // Crashes if user is null
}
```

✅ **Safe**:
```javascript
function formatUser(user) {
  if (!user) return 'Unknown';
  return `${user.firstName ?? ''} ${user.lastName ?? ''}`.trim();
}
```

---

#### Optional Chaining Misuse

❌ **Still Buggy**:
```javascript
const email = user?.profile?.email.toLowerCase();  // Crashes if email is null
```

✅ **Correct**:
```javascript
const email = user?.profile?.email?.toLowerCase() ?? '';
```

---

### Array Operations

#### Array Index Out of Bounds

❌ **Bug**:
```python
def get_first_item(items):
    return items[0]  # IndexError if empty
```

✅ **Safe**:
```python
def get_first_item(items):
    return items[0] if items else None
```

---

#### Modifying Array During Iteration

❌ **Bug**:
```javascript
for (let i = 0; i < items.length; i++) {
  if (shouldRemove(items[i])) {
    items.splice(i, 1);  // Skips next item
  }
}
```

✅ **Correct**:
```javascript
// Option 1: Iterate backwards
for (let i = items.length - 1; i >= 0; i--) {
  if (shouldRemove(items[i])) {
    items.splice(i, 1);
  }
}

// Option 2: Filter
items = items.filter(item => !shouldRemove(item));
```

---

### Async/Await Issues

#### Unhandled Promise Rejection

❌ **Bug**:
```javascript
async function fetchData() {
  const data = await api.get('/data');  // No error handling
  return data;
}
```

✅ **Handled**:
```javascript
async function fetchData() {
  try {
    const data = await api.get('/data');
    return data;
  } catch (error) {
    logger.error('Failed to fetch data:', error);
    throw new DataFetchError('Unable to load data');
  }
}
```

---

#### Missing Await

❌ **Bug**:
```javascript
async function saveUser(user) {
  db.users.create(user);  // Missing await, returns promise
  return { success: true };  // Returns before save completes
}
```

✅ **Correct**:
```javascript
async function saveUser(user) {
  await db.users.create(user);
  return { success: true };
}
```

---

#### Promise.all Error Handling

❌ **Fails All on One Error**:
```javascript
const results = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
]);  // If any fails, all fail
```

✅ **Graceful Degradation**:
```javascript
const results = await Promise.allSettled([
  fetchUser(),
  fetchPosts(),
  fetchComments()
]);

const [user, posts, comments] = results.map(r =>
  r.status === 'fulfilled' ? r.value : null
);
```

---

### Race Conditions

#### Check-Then-Act

❌ **Race Condition**:
```javascript
if (!cache.has(key)) {  // Check
  cache.set(key, expensiveComputation());  // Act
}
// Two threads can both pass check and compute twice
```

✅ **Atomic Operation**:
```javascript
cache.getOrSet(key, () => expensiveComputation());
// Or use mutex/lock
```

---

#### Concurrent Modification

❌ **Bug**:
```javascript
let balance = await getBalance(userId);
balance -= amount;  // Another request could modify balance here
await setBalance(userId, balance);
```

✅ **Atomic Update**:
```javascript
await db.users.update(
  { id: userId },
  { $inc: { balance: -amount } }  // Atomic increment
);
```

---

### Resource Leaks

#### Unclosed File Handles

❌ **Leak**:
```python
def read_file(path):
    f = open(path)
    data = f.read()
    return data  # File never closed
```

✅ **Cleaned Up**:
```python
def read_file(path):
    with open(path) as f:
        return f.read()  # Automatically closed
```

---

#### Memory Leaks (Event Listeners)

❌ **Leak**:
```javascript
useEffect(() => {
  window.addEventListener('resize', handleResize);
  // Missing cleanup
}, []);
```

✅ **Cleaned Up**:
```javascript
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

---

## Performance Issues

### Database Anti-Patterns

#### N+1 Query Problem

❌ **Slow**:
```javascript
const users = await db.users.findAll();
for (const user of users) {
  user.posts = await db.posts.findMany({ authorId: user.id });
}
// 1 query for users + N queries for posts = N+1
```

✅ **Optimized**:
```javascript
const users = await db.users.findAll({
  include: { posts: true }  // Single query with JOIN
});
```

---

#### Missing Indexes

❌ **Slow**:
```sql
SELECT * FROM orders WHERE user_id = ? AND status = 'pending';
-- Table scan without index
```

✅ **Indexed**:
```sql
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Now uses index
```

**Check**: Ensure WHERE, JOIN, ORDER BY columns are indexed

---

#### SELECT *

❌ **Wasteful**:
```sql
SELECT * FROM users;  -- Returns 50 columns, need 3
```

✅ **Efficient**:
```sql
SELECT id, name, email FROM users;
```

---

### Algorithm Complexity

#### Inefficient Search

❌ **O(n)**:
```javascript
function findUser(users, id) {
  return users.find(u => u.id === id);  // Linear search
}

// Called in loop: O(n²)
for (const order of orders) {
  const user = findUser(users, order.userId);
}
```

✅ **O(1)**:
```javascript
const userMap = new Map(users.map(u => [u.id, u]));

for (const order of orders) {
  const user = userMap.get(order.userId);  // Constant time
}
```

---

#### Nested Loops

❌ **O(n²)**:
```python
for item in list1:
    for other in list2:
        if item.id == other.id:
            # O(n²) comparison
```

✅ **O(n)**:
```python
set2 = {other.id for other in list2}
for item in list1:
    if item.id in set2:  # O(1) lookup
        # O(n) total
```

---

### Frontend Performance

#### Unnecessary Re-renders

❌ **Re-renders Too Much**:
```javascript
function UserList({ users }) {
  return users.map(user => (
    <UserCard
      user={user}
      onUpdate={() => updateUser(user.id)}  // New function every render
    />
  ));
}
```

✅ **Optimized**:
```javascript
function UserList({ users }) {
  const handleUpdate = useCallback((userId) => {
    updateUser(userId);
  }, []);

  return users.map(user => (
    <UserCard
      user={user}
      onUpdate={handleUpdate}
    />
  ));
}

const UserCard = React.memo(({ user, onUpdate }) => {
  // Only re-renders when user changes
});
```

---

#### Large Bundle Size

❌ **Imports Everything**:
```javascript
import _ from 'lodash';  // 70kb
import moment from 'moment';  // 200kb
```

✅ **Tree-Shaking**:
```javascript
import debounce from 'lodash/debounce';  // 2kb
import { format } from 'date-fns';  // 5kb
```

---

### Memory Issues

#### Memory Leak (Closure)

❌ **Leak**:
```javascript
function createHandler() {
  const largeData = new Array(1000000).fill('data');

  return function() {
    console.log('Handler called');
    // largeData is retained even though not used
  };
}
```

✅ **Fixed**:
```javascript
function createHandler() {
  const largeData = new Array(1000000).fill('data');
  processData(largeData);  // Use it

  return function() {
    console.log('Handler called');
    // largeData can be garbage collected
  };
}
```

---

## Best Practices Violations

### SOLID Principles

#### Single Responsibility Violation

❌ **Too Many Responsibilities**:
```javascript
class UserManager {
  createUser(data) { /* ... */ }
  sendWelcomeEmail(user) { /* ... */ }
  validateEmail(email) { /* ... */ }
  hashPassword(password) { /* ... */ }
  logActivity(action) { /* ... */ }
}
```

✅ **Separated**:
```javascript
class UserService {
  createUser(data) { /* ... */ }
}

class EmailService {
  sendWelcome(user) { /* ... */ }
}

class ValidationService {
  validateEmail(email) { /* ... */ }
}
```

---

#### Open/Closed Violation

❌ **Requires Modification**:
```javascript
function calculateShipping(order) {
  if (order.type === 'standard') {
    return 5.00;
  } else if (order.type === 'express') {
    return 15.00;
  } else if (order.type === 'overnight') {
    return 30.00;
  }
  // Adding new type requires modifying this function
}
```

✅ **Open for Extension**:
```javascript
const shippingStrategies = {
  standard: () => 5.00,
  express: () => 15.00,
  overnight: () => 30.00
};

function calculateShipping(order) {
  const strategy = shippingStrategies[order.type];
  if (!strategy) throw new Error('Invalid shipping type');
  return strategy();
}
// Adding new type: just add to object
```

---

### Code Duplication

#### Copy-Paste Code

❌ **Duplicated**:
```javascript
function getAdminUsers() {
  const users = db.users.findAll();
  return users.filter(u => u.role === 'admin' && u.active === true);
}

function getModeratorUsers() {
  const users = db.users.findAll();
  return users.filter(u => u.role === 'moderator' && u.active === true);
}
```

✅ **DRY (Don't Repeat Yourself)**:
```javascript
function getUsersByRole(role) {
  const users = db.users.findAll();
  return users.filter(u => u.role === role && u.active === true);
}

const getAdminUsers = () => getUsersByRole('admin');
const getModeratorUsers = () => getUsersByRole('moderator');
```

---

### Magic Numbers/Strings

❌ **Magic Values**:
```javascript
if (user.age >= 18 && user.age <= 65) {
  if (order.total > 100) {
    discount = order.total * 0.1;
  }
}
```

✅ **Named Constants**:
```javascript
const MIN_ADULT_AGE = 18;
const MAX_WORKING_AGE = 65;
const DISCOUNT_THRESHOLD = 100;
const DISCOUNT_RATE = 0.1;

if (user.age >= MIN_ADULT_AGE && user.age <= MAX_WORKING_AGE) {
  if (order.total > DISCOUNT_THRESHOLD) {
    discount = order.total * DISCOUNT_RATE;
  }
}
```

---

### Deep Nesting

❌ **Arrow Anti-Pattern**:
```javascript
function processOrder(order) {
  if (order) {
    if (order.items) {
      if (order.items.length > 0) {
        if (order.user) {
          if (order.user.verified) {
            // Finally do something
          }
        }
      }
    }
  }
}
```

✅ **Early Returns**:
```javascript
function processOrder(order) {
  if (!order) return;
  if (!order.items || order.items.length === 0) return;
  if (!order.user || !order.user.verified) return;

  // Do something
}
```

---

### Error Handling

#### Swallowing Errors

❌ **Silent Failure**:
```python
try:
    process_payment(order)
except Exception:
    pass  # Error silently ignored
```

✅ **Proper Handling**:
```python
try:
    process_payment(order)
except PaymentError as e:
    logger.error(f"Payment failed for order {order.id}: {e}")
    notify_admin(order, e)
    raise
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    raise
```

---

#### Too Broad Exception Catch

❌ **Catches Everything**:
```javascript
try {
  const user = await fetchUser(id);
  updateUI(user);
} catch (e) {
  console.log('Error');  // What error? Network? Parsing? UI?
}
```

✅ **Specific Handling**:
```javascript
try {
  const user = await fetchUser(id);
  updateUI(user);
} catch (e) {
  if (e instanceof NetworkError) {
    showRetryOption();
  } else if (e instanceof ValidationError) {
    showValidationMessage(e.message);
  } else {
    logger.error('Unexpected error:', e);
    showGenericError();
  }
}
```

---

## Testing Anti-Patterns

### Testing Implementation Details

❌ **Brittle Test**:
```javascript
it('should call internal helper', () => {
  const spy = jest.spyOn(service, '_internalHelper');
  service.publicMethod();
  expect(spy).toHaveBeenCalled();  // Breaks on refactoring
});
```

✅ **Test Behavior**:
```javascript
it('should return correct result', () => {
  const result = service.publicMethod();
  expect(result).toEqual(expectedOutput);
});
```

---

### Missing Edge Cases

❌ **Incomplete**:
```javascript
it('should add numbers', () => {
  expect(add(2, 3)).toBe(5);
});
```

✅ **Comprehensive**:
```javascript
describe('add', () => {
  it('should add positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('should handle zero', () => {
    expect(add(0, 5)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(add(-2, 3)).toBe(1);
  });

  it('should handle decimal numbers', () => {
    expect(add(0.1, 0.2)).toBeCloseTo(0.3);
  });
});
```

---

## Summary

Use this checklist to systematically review code for:
- ✅ Security vulnerabilities (injection, auth, data exposure)
- ✅ Common bugs (null checks, async issues, race conditions)
- ✅ Performance problems (N+1 queries, inefficient algorithms)
- ✅ Best practices (SOLID, DRY, error handling)
- ✅ Testing completeness (edge cases, behavior vs implementation)

Remember: The goal is not to find every possible issue, but to catch the most impactful problems that affect security, reliability, and maintainability.
