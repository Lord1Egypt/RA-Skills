# Technical Writing Mastery

> Standards and techniques for documentation, API references, tutorials, whitepapers, and technical content that developers and professionals actually read.

---

## 1. The Technical Writing Pyramid

```
        [Executive Summary]
              |
        [Key Findings]
              |
     [Detailed Analysis]
              |
    [Supporting Evidence]
              |
      [Appendices]
```

**Rule**: Every layer must be independently readable. A busy CTO should get value from just the top two layers.

---

## 2. The CRUD Principle for Documentation

**Every technical document must be:**

```
C - CLEAR
  -> One idea per paragraph
  -> One concept per section
  -> Active voice always
  -> "The system processes data" NOT "Data is processed by the system"

R - RELEVANT
  -> Cut everything not essential to the task
  -> No "nice to know" - only "need to know"
  -> Link to deeper docs, don't inline everything

U - USABLE
  -> Start with the goal, not the theory
  -> Include copy-pasteable code examples
  -> Show expected output
  -> Include error handling

D - DEPENDABLE
  -> Every code example tested
  -> Version numbers specified
  -> Screenshots dated
  -> Links verified
```

---

## 3. The Documentation Types Matrix

| Type | Purpose | Structure | Audience |
|------|---------|-----------|----------|
| **README** | Quick start, overview | Install -> Usage -> API -> Contribute | New users |
| **API Reference** | Complete endpoint docs | Endpoint -> Method -> Params -> Response -> Errors | Developers |
| **Tutorial** | Learn by doing | Goal -> Steps -> Verification -> Next | Beginners |
| **How-To Guide** | Solve specific problem | Problem -> Solution -> Verification | Users with context |
| **Conceptual Doc** | Understand architecture | Overview -> Components -> Data Flow -> Decisions | Architects |
| **Troubleshooting** | Fix common issues | Symptom -> Cause -> Solution -> Prevention | Support + Users |
| **Changelog** | Track changes | Version -> Breaking -> Features -> Fixes -> Deprecations | All users |
| **Whitepaper** | Deep technical analysis | Problem -> Research -> Solution -> Results -> Future | Decision makers |
| **RFC** | Propose changes | Context -> Proposal -> Trade-offs -> Timeline -> Decision | Team |

---

## 4. The README Template

```markdown
# Project Name

> One-sentence description of what this does and why it matters.

## Quick Start

```bash
# Install
npm install package-name

# Usage
const result = packageName.doSomething();
```

## Features

- [x] Feature 1: One-line benefit
- [x] Feature 2: One-line benefit
- [x] Feature 3: One-line benefit

## Installation

### Prerequisites
- Node.js >= 18.0
- Python >= 3.9

### Setup
```bash
# Step-by-step commands
```

## Usage

### Basic Example
```code
// Minimal working example
```

### Advanced Example
```code
// More complex use case
```

## API Reference

### functionName(param1, param2)
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | Yes | What this does |
| param2 | number | No | Default: 0 |

**Returns**: Type - Description

**Throws**: ErrorType - When this happens

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| timeout | number | 5000 | Request timeout in ms |

## Contributing

See CONTRIBUTING.md

## License

MIT (c) Author Name
```

---

## 5. The API Documentation Standard

```
ENDPOINT: POST /api/v1/resource

DESCRIPTION:
What this endpoint does in one sentence.

AUTHENTICATION:
Required headers or tokens.

REQUEST:
```json
{
  "field1": "string (required) - Description",
  "field2": "number (optional) - Description, default: 0"
}
```

RESPONSE (200 OK):
```json
{
  "id": "string - Unique identifier",
  "status": "string - Current state",
  "created_at": "ISO 8601 timestamp"
}
```

RESPONSE (400 Bad Request):
```json
{
  "error": "validation_error",
  "message": "field1 is required",
  "field": "field1"
}
```

RESPONSE (401 Unauthorized):
```json
{
  "error": "unauthorized",
  "message": "Invalid or expired token"
}
```

RESPONSE (500 Server Error):
```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred"
}
```

EXAMPLE:
```bash
curl -X POST https://api.example.com/v1/resource \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value"}'
```

RATE LIMITS:
- 100 requests/minute for free tier
- 1000 requests/minute for pro tier
```

---

## 6. The Tutorial Writing Formula

```
TITLE: How to [Achieve Specific Outcome] in [Tool/Framework]

PREREQUISITES:
- What they need to know first
- What they need to install
- What accounts they need

STEP 1: [Action]
-> What to do
-> Why this matters (1 sentence)
-> Code/command example
-> Expected output
-> Common pitfall and how to avoid it

STEP 2: [Action]
-> [Same structure]

...

VERIFICATION:
-> How to confirm it worked
-> What success looks like
-> What to do if it didn't work

NEXT STEPS:
-> What to learn next
-> Related tutorials
-> Where to get help
```

---

## 7. The Whitepaper Structure

```
EXECUTIVE SUMMARY (1 page)
  -> Problem statement
  -> Key findings
  -> Recommendation

1. INTRODUCTION (2-3 pages)
  -> Context and background
  -> Why this matters NOW
  -> Scope and methodology

2. PROBLEM ANALYSIS (3-5 pages)
  -> Current state
  -> Pain points with data
  -> Cost of inaction

3. SOLUTION OVERVIEW (3-5 pages)
  -> Proposed approach
  -> Technical architecture
  -> Key differentiators

4. IMPLEMENTATION (2-3 pages)
  -> Step-by-step plan
  -> Timeline
  -> Resource requirements

5. RESULTS & VALIDATION (2-3 pages)
  -> Case studies
  -> Performance data
  -> Comparative analysis

6. CONCLUSION (1 page)
  -> Summary of benefits
  -> Call to action
  -> Next steps

APPENDICES
  -> Detailed data
  -> Additional references
  -> Glossary
```

---

## 8. Code Documentation Best Practices

### Inline Comments
```python
# BAD: Explains WHAT (obvious from code)
# Increment counter by 1
counter += 1

# GOOD: Explains WHY
# Compensate for off-by-one error in legacy API response
counter += 1

# BAD: Outdated comment
# TODO: Fix this later (from 2019)

# GOOD: Context for complex logic
# Edge case: When user has both premium and trial active,
# premium takes precedence per business rule #2847
```

### Docstrings
```python
def process_payment(user_id, amount, currency="USD"):
    """
    Process a payment for a user.

    Args:
        user_id: Unique identifier for the user
        amount: Payment amount (must be positive)
        currency: ISO 4217 currency code (default: USD)

    Returns:
        dict: Payment result containing transaction_id, status, timestamp

    Raises:
        ValueError: If amount <= 0 or currency is invalid
        UserNotFoundError: If user_id doesn't exist
        InsufficientFundsError: If user balance < amount

    Example:
        >>> result = process_payment("user_123", 99.99, "EUR")
        >>> print(result["status"])
        "success"
    """
```

---

## 9. The Error Message Framework

**Every error message must include:**

```
1. WHAT HAPPENED - Clear, non-technical description
   -> "Your payment could not be processed"

2. WHY IT HAPPENED - Root cause (if known)
   -> "Your card was declined by the bank"

3. HOW TO FIX IT - Actionable next step
   -> "Try a different payment method or contact your bank"

4. WHERE TO GET HELP - Support channel
   -> "Error code: PAY-4021 | Support: help@example.com"
```

**Error Message Checklist:**
- [ ] No jargon ("HTTP 500" -> "Something went wrong on our end")
- [ ] No blame ("You entered wrong" -> "The password didn't match")
- [ ] Actionable (not just "Error occurred")
- [ ] Specific (not "Something went wrong")
- [ ] Consistent format across all errors

---

## 10. Technical Writing Style Rules

### DO:
- Use active voice
- Use present tense for documentation
- Use second person ("you") for instructions
- Use specific numbers ("3 seconds" not "fast")
- Use parallel structure in lists
- Define acronyms on first use
- Use consistent terminology

### DON'T:
- Use passive voice ("The button should be clicked")
- Use future tense ("You will need to" -> "You need to")
- Use first person ("We recommend" -> "Recommended")
- Use vague qualifiers ("very", "really", "quite")
- Use idioms or cultural references
- Assume reader's knowledge level
- Use different terms for the same concept

---

## 11. The Review Checklist for Technical Docs

```
[x] Accuracy: All code examples compile and run
[x] Completeness: All parameters documented
[x] Clarity: Non-expert can follow instructions
[x] Consistency: Terminology matches throughout
[x] Currency: Version numbers and screenshots up to date
[x] Links: All internal and external links work
[x] Accessibility: Alt text on images, proper heading hierarchy
[x] Searchability: Keywords in headings and first paragraphs
```
