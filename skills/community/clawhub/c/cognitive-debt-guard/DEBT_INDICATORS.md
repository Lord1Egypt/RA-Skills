# Debt Indicators: 15 Early Warning Signs of Cognitive Debt in AI Code

A diagnostic checklist for identifying when AI-generated code is creating hidden maintenance burdens and technical debt.

---

## What Is Cognitive Debt?

**Cognitive debt** is the hidden cost of code that "works" but is difficult to understand, modify, or debug. Unlike traditional technical debt (which is often conscious and documented), cognitive debt accumulates silently when developers (human or AI) produce code that lacks clarity, structure, or proper abstraction.

AI-generated code is particularly prone to cognitive debt because:
- It optimizes for immediate functionality over long-term maintainability
- It lacks the experiential knowledge of why certain patterns are problematic
- It can't "learn" from project history without explicit context
- It produces code that looks correct but may be subtly wrong

---

## The 15 Warning Signs

### 1. ❓ Can You Explain What It Does in Plain Language?

**Indicator:** You cannot summarize the code's purpose in one or two sentences without using technical jargon.

**Why It Matters:** Code that can't be explained simply is code that can't be maintained easily. Every function should have a clear, single purpose.

**Example of Debt:**
```python
def process(data, flag=None, mode='default', opts=None, **kwargs):
    # 47 lines of nested conditionals and transformations
    # What does this actually do? Who knows.
```

**Fix:** Break into smaller, named functions with clear purposes.

---

### 2. 🔗 Can You Trace Data Flow From Input to Output?

**Indicator:** You can't easily follow how input data transforms into output.

**Why It Matters:** Data flow is the essence of program logic. If you can't trace it, you can't debug it.

**Example of Debt:**
```javascript
function handleRequest(req, res) {
  let data = req.body;
  process(data);
  // data is mutated somewhere deep in the call stack
  // now data has different shape, but where did it change?
  return transform(data);
}
```

**Fix:** Make data transformations explicit and traceable. Avoid in-place mutation of shared state.

---

### 3. 📏 Does the Function Exceed 30 Lines?

**Indicator:** Functions longer than 30 lines typically do too much.

**Why It Matters:** Long functions are hard to test, hard to understand, and often have hidden side effects.

**Example of Debt:**
```python
def create_user(request):
    # Validate input (10 lines)
    # Check database (5 lines)
    # Hash password (3 lines)
    # Send welcome email (15 lines)
    # Create audit log (8 lines)
    # Return response (5 lines)
    # Total: 46 lines, 6 different responsibilities
```

**Fix:** Extract helper functions. One function = one responsibility.

---

### 4. 🌲 Is There More Than 3 Levels of Nesting?

**Indicator:** Deeply nested conditionals and loops create a "pyramid of doom."

**Why It Matters:** Each nesting level adds cognitive load. Beyond 3 levels, understanding drops sharply.

**Example of Debt:**
```javascript
if (user) {
  if (user.isActive) {
    if (user.hasPermission('edit')) {
      if (resource) {
        if (resource.isEditable) {
          // Finally, the actual logic
        }
      }
    }
  }
}
```

**Fix:** Use early returns, guard clauses, or extract nested logic into separate functions.

---

### 5. 📛 Are Variables Named Vague or Generic Terms?

**Indicator:** Names like `data`, `result`, `temp`, `value`, `item` appear frequently.

**Why It Matters:** Generic names force readers to derive meaning from context instead of the name itself.

**Example of Debt:**
```python
def process(data):
    result = []
    for item in data:
        value = transform(item)
        if value:
            result.append(value)
    return result
```

**Fix:** Use domain-specific names: `users`, `validated_emails`, `normalized_record`.

---

### 6. 🔮 Are There "Magic Numbers" Without Explanation?

**Indicator:** Numeric literals appear without context or explanation.

**Why It Matters:** Magic numbers obscure intent and make future changes error-prone.

**Example of Debt:**
```javascript
if (status === 2) {
  await wait(5000);
  retry(3);
}
```

**Fix:** Use named constants: `if (status === STATUS.PENDING)`, `await wait(RETRY_DELAY_MS)`.

---

### 7. 🎭 Does the Code Mix Multiple Abstraction Levels?

**Indicator:** High-level business logic is mixed with low-level implementation details.

**Why It Matters:** Abstraction levels should be consistent within each function. Mixing them forces readers to context-switch.

**Example of Debt:**
```python
def send_report(report):
    # High level
    recipients = get_recipients(report)
    
    # Suddenly, low level
    smtp = smtplib.SMTP('smtp.example.com', 587)
    smtp.starttls()
    smtp.login('user', 'pass')
    
    # Back to high level
    for recipient in recipients:
        send_email(recipient, report)
```

**Fix:** Extract low-level details into helper functions. Keep each function at one abstraction level.

---

### 8. 🧩 Are There Duplicate Code Blocks (>5 Lines)?

**Indicator:** Similar code appears in multiple places.

**Why It Matters:** Duplicated code means duplicated bugs and duplicated maintenance effort.

**Example of Debt:**
```javascript
// In function A
const user = await db.users.findOne({ id });
if (!user) throw new Error('User not found');
if (!user.isActive) throw new Error('User inactive');

// In function B (nearly identical)
const user = await db.users.findOne({ id });
if (!user) throw new Error('User not found');
if (!user.isActive) throw new Error('User inactive');
```

**Fix:** Extract common logic into a shared function.

---

### 9. 📦 Does the Function Have Hidden Dependencies?

**Indicator:** The function relies on external state, global variables, or implicit context not visible in its signature.

**Why It Matters:** Hidden dependencies make functions hard to test and reason about in isolation.

**Example of Debt:**
```python
def calculate_total(items):
    # Secretly depends on global TAX_RATE
    # Secretly depends on external API call to get discounts
    # Secretly logs to a global logger
    return sum(item.price for item in items) * TAX_RATE
```

**Fix:** Pass dependencies as parameters or use dependency injection.

---

### 10. 🎪 Is Error Handling Inconsistent or Missing?

**Indicator:** Some errors are caught, others aren't. Some return null, others throw. No clear error handling strategy.

**Why It Matters:** Inconsistent error handling creates unpredictable behavior and makes debugging a nightmare.

**Example of Debt:**
```javascript
function fetchUser(id) {
  if (!id) return null;  // Returns null for invalid input
  // ...
  if (userNotFound) throw new Error();  // Throws for not found
  // ...
  if (dbError) return { error: 'db' };  // Returns error object
}
```

**Fix:** Establish a consistent error handling pattern (exceptions vs. Result types) and apply it uniformly.

---

### 11. 🏗️ Does the Code Require External Documentation to Understand?

**Indicator:** You need to read a wiki, comment, or external doc to understand what the code does.

**Why It Matters:** Code should be self-documenting. If you need external docs for basic understanding, the code structure is wrong.

**Example of Debt:**
```python
# This function implements the XYZ algorithm from paper doi:10.1234/abc
# See docs/architecture.md for the full explanation
# Trust me, it works
def process(data):
    # Cryptic implementation with no clear logic flow
```

**Fix:** Refactor code to be self-explanatory. Use clear names and structure that reveals intent.

---

### 12. 🧪 Can You Write a Simple Unit Test Without Complex Setup?

**Indicator:** Testing the function requires extensive mocking, fixtures, or complex environment setup.

**Why It Matters:** Functions that are hard to test are usually poorly structured. Test difficulty is a code smell.

**Example of Debt:**
```javascript
// To test this, you need to:
// 1. Mock the database connection
// 2. Mock the file system
// 3. Set up environment variables
// 4. Mock the external API
// 5. Initialize global state
function processOrder(order) {
  // Uses database, file system, env vars, external API, and global state
}
```

**Fix:** Reduce dependencies. Pass them as parameters. Make the function more focused.

---

### 13. ⚡ Does "Fixing" One Bug Often Create Another?

**Indicator:** Changes to the code frequently cause regressions in unrelated areas.

**Why It Matters:** Fragile code indicates hidden coupling and implicit dependencies.

**Example of Debt:**
```python
# Changing this line breaks something in a totally different module
# because they share mutable global state
DISCOUNT_RATE = 0.1
```

**Fix:** Identify and eliminate hidden coupling. Make dependencies explicit.

---

### 14. 🔨 Does the Code Look Like It Was Written by Different People?

**Indicator:** Inconsistent style, patterns, and conventions throughout the codebase.

**Why It Matters:** Inconsistent code is harder to read because readers can't form expectations.

**Example of Debt:**
```javascript
// File A
const getUser = async (id) => { ... }

// File B (same codebase)
function fetch_user(userId) { ... }

// File C (same codebase)
const retrieveUser = function(userId) { ... }
```

**Fix:** Establish and enforce consistent coding standards. Use linters and formatters.

---

### 15. 🚫 Does the Code Fail the "Six-Month Test"?

**Indicator:** If you came back to this code in six months, would you understand it without prior knowledge?

**Why It Matters:** Code is read far more often than it's written. Future-you (or your successor) will thank you for clear code.

**Example of Debt:**
```python
# What was I thinking? This makes no sense now.
# I wrote this 6 months ago and I have no idea how it works.
def transform(x):
    return x if x else x and not x or True
```

**Fix:** Write code for the reader, not the writer. Prefer clarity over cleverness.

---

## Quick Assessment Checklist

Run through this list whenever you review AI-generated code:

| # | Question | ✅ Clear | ⚠️ Needs Work | ❌ Debt Detected |
|---|----------|---------|---------------|------------------|
| 1 | Can explain in plain language? | | | |
| 2 | Can trace data flow? | | | |
| 3 | Function under 30 lines? | | | |
| 4 | Nesting under 3 levels? | | | |
| 5 | Variables meaningfully named? | | | |
| 6 | No magic numbers? | | | |
| 7 | Consistent abstraction level? | | | |
| 8 | No code duplication? | | | |
| 9 | No hidden dependencies? | | | |
| 10 | Consistent error handling? | | | |
| 11 | Self-documenting? | | | |
| 12 | Easy to test? | | | |
| 13 | Changes don't cause cascades? | | | |
| 14 | Consistent style? | | | |
| 15 | Passes six-month test? | | | |

**Scoring:**
- **0-3 warnings:** Good code quality
- **4-7 warnings:** Moderate cognitive debt — schedule refactoring
- **8+ warnings:** High cognitive debt — refactor before merging

---

## Prevention Strategies

1. **Before accepting AI code:** Run through this checklist
2. **During code review:** Look for these patterns explicitly
3. **When refactoring:** Use these as targets for improvement
4. **In documentation:** Reference this checklist as a quality standard

---

## The Core Principle

> **Code is communication.** It tells the next person (including future-you) what the system does and how it works. If it doesn't communicate clearly, it's broken — even if it runs without errors.

AI can write code that works. But it takes human oversight to ensure the code *communicates*.
