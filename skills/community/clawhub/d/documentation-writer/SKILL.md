---
name: documentation-writer
description: Write clear, comprehensive documentation. Covers README files, API docs, user guides, and code comments. Create documentation that users actually read and understand. Use when writing docs, creating guides, documenting APIs, or improving README. Triggers on "documentation", "readme", "api docs", "user guide", "how to document".
---

# Documentation Writer

Create documentation that people actually read, understand, and follow.

## Documentation Types

### 1. README Files

**Structure:**
```markdown
# Project Name

Brief description (1-2 sentences)

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Quick Start

```bash
# Install
npm install package

# Use
package do-thing
```

## Usage

Detailed usage examples

## Configuration

Options and settings

## API

API reference

## Contributing

How to contribute

## License

MIT
```

**What Makes Good README:**
- Clear project name
- One-sentence description
- Installation in 3 commands or less
- Working examples
- Common use cases
- Link to full docs

### 2. API Documentation

**Endpoint Documentation:**
```markdown
## Get User

`GET /api/users/{id}`

Retrieves user details by ID.

### Parameters

| Name | Type | In | Required | Description |
|------|------|------|----------|-------------|
| id | string | path | Yes | User ID |
| fields | string | query | No | Fields to return |

### Response

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2026-01-15T10:30:00Z"
}
```

### Errors

| Code | Description |
|------|-------------|
| 404 | User not found |
| 401 | Unauthorized |
| 500 | Server error |

### Example

```bash
curl -X GET "https://api.example.com/users/123" \
  -H "Authorization: Bearer {token}"
```
```

**API Doc Structure:**
- HTTP method and endpoint
- Brief description
- Parameters (path, query, body)
- Response format
- Error codes
- Example request
- Rate limits (if applicable)

### 3. User Guides

**Structure:**
```markdown
# Getting Started with X

## Prerequisites

- Requirement 1
- Requirement 2

## Step 1: First Action

Detailed explanation with screenshots

## Step 2: Second Action

Continue with clear instructions

## Troubleshooting

Common problems and solutions

## Next Steps

- Advanced feature 1
- Advanced feature 2
```

**Writing Tips:**
- Start with simplest path
- One concept per section
- Use numbered steps
- Include screenshots
- Anticipate problems

### 4. Code Comments

**When to Comment:**
- Why, not what
- Complex logic
- Non-obvious decisions
- Workarounds
- TODOs with context

**Good Comments:**
```python
# Using binary search because the list is sorted and we need O(log n) performance
# for real-time autocomplete. Linear search was too slow on lists > 10,000 items.
def find_item(sorted_list, target):
    ...

# Workaround for Safari bug: Safari doesn't handle null values in localStorage
# See: https://bugs.webkit.org/show_bug?id=123456
def safe_store(key, value):
    ...

# TODO(john): This should be refactored into a separate service when we add
# support for multiple payment providers. Currently only handles Stripe.
def process_payment(amount):
    ...
```

**Bad Comments:**
```python
# Increment counter
counter += 1  # Obvious

# Loop through items
for item in items:  # Obvious
    process(item)  # Obvious
```

## Documentation Principles

### 1. Audience First

**Identify Reader:**
- Beginner? Explain concepts
- Expert? Focus on specifics
- Internal team? Use shorthand
- External users? Full context

**Match Tone:**
```
Beginner: "First, install Node.js from nodejs.org"
Expert: "Requires Node 18+"
```

### 2. Show, Don't Tell

**Bad:**
```
The function processes data efficiently.
```

**Good:**
```
The function processes 1 million records in under 2 seconds on a standard laptop.
```

**Even Better:**
```python
# Processes 1M records in <2s on M1 MacBook
# Benchmark: test_process_benchmark.py
def process_batch(data):
    ...
```

### 3. Complete Examples

**Bad:**
```python
# Use the API
client.do_something()
```

**Good:**
```python
import MyClient

# Initialize with API key
client = MyClient(api_key="your-api-key")

# Create a new resource
response = client.create_resource(
    name="My Resource",
    type="standard"
)

# Handle response
if response.success:
    print(f"Created: {response.id}")
```

### 4. Keep Updated

**Version Your Docs:**
```markdown
> Last updated: 2026-03-16
> Version: 2.1.0
```

**Mark Outdated:**
```markdown
⚠️ **Deprecated**: This endpoint will be removed in v3.0. Use `/api/v2/users` instead.
```

**Changelog:**
```markdown
## v2.1.0 (2026-03-16)

### Added
- New `/api/batch` endpoint

### Changed
- `/api/users` now returns created_at timestamp

### Deprecated
- `/api/legacy-endpoint` will be removed in v3.0
```

## Documentation Patterns

### Quick Start

**Pattern:**
```markdown
## Quick Start (5 minutes)

### 1. Install

```bash
npm install my-package
```

### 2. Configure

```javascript
const myPackage = require('my-package');
myPackage.configure({ apiKey: 'your-key' });
```

### 3. Use

```javascript
const result = myPackage.doSomething();
console.log(result); // "Success!"
```

That's it! See [Full Documentation](docs/) for more.
```

### FAQ

**Pattern:**
```markdown
## Frequently Asked Questions

### How do I do X?

Brief answer with code example.

### Why does Y happen?

Explanation of why with solution if applicable.

### Can I do Z?

Yes/No with explanation of how or why not.
```

### Troubleshooting

**Pattern:**
```markdown
## Troubleshooting

### Error: "Connection refused"

**Cause:** The server isn't running.
**Solution:** Start the server with `npm start`.

### Error: "Invalid API key"

**Cause:** Your API key is incorrect or expired.
**Solution:** 
1. Check your API key in settings
2. Regenerate if needed
3. Update your configuration

### Performance is slow

**Cause:** Large datasets without pagination.
**Solution:** Use pagination for datasets > 1000 items:

```javascript
client.getRecords({ limit: 100, offset: 0 });
```
```

## Tools and Formats

### Markdown Best Practices

**Headers:**
```markdown
# H1 - Title
## H2 - Major Section
### H3 - Subsection
#### H4 - Detail
```

**Code Blocks:**
```markdown
Inline `code` for short references.

```python
# Block code for examples
def example():
    return "example"
```
```

**Tables:**
```markdown
| Column 1 | Column 2 | Column 3 |
|-----------|----------|----------|
| Value 1   | Value 2  | Value 3  |
| Value 4   | Value 5  | Value 6  |
```

**Lists:**
```markdown
- Unordered item
- Another item

1. Ordered item
2. Another item

- [ ] Task item
- [x] Completed task
```

### Documentation Generators

**JSDoc (JavaScript):**
```javascript
/**
 * Calculate the sum of two numbers.
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 * @example
 * sum(2, 3) // returns 5
 */
function sum(a, b) {
    return a + b;
}
```

**Python Docstrings:**
```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        The arithmetic mean of the numbers
        
    Raises:
        ValueError: If numbers list is empty
        
    Example:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

## Documentation Checklist

**README:**
- [ ] Project name and description
- [ ] Installation instructions
- [ ] Basic usage example
- [ ] License
- [ ] Contact/support

**API Docs:**
- [ ] All endpoints documented
- [ ] Request/response examples
- [ ] Error codes
- [ ] Authentication
- [ ] Rate limits

**User Guide:**
- [ ] Prerequisites clear
- [ ] Step-by-step instructions
- [ ] Screenshots/diagrams
- [ ] Troubleshooting section
- [ ] Next steps

**Code Comments:**
- [ ] Why, not what
- [ ] Complex logic explained
- [ ] TODOs have context
- [ ] No obvious comments

## Common Mistakes

### 1. Assumption Dumping

**Bad:**
```
Configure your environment variables.
```

**Good:**
```
Set these environment variables:

```bash
export API_KEY="your-api-key"
export API_URL="https://api.example.com"
```

You can find your API key in your dashboard at https://dashboard.example.com/keys.
```

### 2. Missing Prerequisites

**Bad:**
```
Run `npm start` to begin.
```

**Good:**
```
## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- API key from [dashboard](https://dashboard.example.com)

## Start

```bash
npm install
npm start
```
```

### 3. Outdated Examples

**Bad:**
```javascript
// Example from v1.0
oldApi.call();
```

**Good:**
```javascript
// Current version (v2.0)
newApi.call();

// v1.0 (deprecated) - remove in next major version
// oldApi.call();
```

### 4. No Error Handling

**Bad:**
```javascript
const result = api.getData();
console.log(result);
```

**Good:**
```javascript
try {
    const result = await api.getData();
    console.log(result);
} catch (error) {
    if (error.code === 'NOT_FOUND') {
        console.log('No data found. Create some first!');
    } else {
        console.error('Error:', error.message);
    }
}
```

## Writing Style

### Be Concise

```
Bad: In order to use this function, you will need to first install the package.
Good: Install the package to use this function.
```

### Be Precise

```
Bad: The function might return something.
Good: Returns a User object or null if not found.
```

### Be Active

```
Bad: The data is processed by the system.
Good: The system processes the data.
```

### Use Examples

```
Bad: The configuration accepts various options.
Good: The configuration accepts:
```json
{
    "timeout": 5000,
    "retries": 3
}
```
```
