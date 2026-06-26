---
name: error-rosetta
version: 1.0.0
description: >
  Universal translator for cryptic error messages, stack traces, and log
  output. Takes the hieroglyphics your toolchain throws at you and produces
  plain-language diagnosis, root cause, and the exact fix — in your codebase,
  not some generic Stack Overflow answer from 2019.
author: J. DeVere Cooley
category: everyday-tools
tags:
  - error-handling
  - debugging
  - translation
  - daily-driver
metadata:
  openclaw:
    emoji: "📜"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - debugging
---

# Error Rosetta

> "The Rosetta Stone let scholars read Egyptian hieroglyphics by providing the same text in three languages. Your compiler already speaks three languages — the error code, the stack trace, and the actual problem. It just refuses to use the third one."

## What It Does

You see this:

```
TypeError: Cannot read properties of undefined (reading 'map')
    at UserList (webpack-internal:///./src/components/UserList.tsx:14:23)
    at renderWithHooks (webpack-internal:///./node_modules/react-dom/cjs/react-dom.development.js:14985:18)
    at mountIndeterminateComponent (webpack-internal:///./node_modules/react-dom/cjs/react-dom.development.js:17811:13)
```

Error Rosetta gives you this:

```
PLAIN ENGLISH: Your UserList component is trying to call .map() on
something that doesn't exist yet. On line 14, you're accessing a
property that is undefined — probably because the data hasn't loaded
from the API when the component first renders.

ROOT CAUSE: src/components/UserList.tsx:14 accesses `users.map()`
but `users` is undefined on first render. Your useEffect that fetches
users hasn't completed yet.

FIX: Add a guard before mapping:
  {users?.map(...)}  or  {users && users.map(...)}

  Better: Initialize your state with an empty array:
  const [users, setUsers] = useState([]);
```

## The Translation Layers

### Layer 1: Error Identification

Every error message, no matter how cryptic, contains these decodable components:

| Component | What It Tells You | Example |
|---|---|---|
| **Error Type** | Category of problem | `TypeError`, `ENOENT`, `HTTP 422`, `SegFault` |
| **Error Message** | What went wrong (usually poorly) | "Cannot read properties of undefined" |
| **Location** | Where it happened | File path + line number |
| **Stack Trace** | How it got there | Call chain from entry point to error |
| **Error Code** | Machine-readable identifier | `E0308`, `TS2345`, `EPERM` |

### Layer 2: Context Enrichment

Raw error → enriched with your codebase context:

```
ENRICHMENT PROCESS:
├── Read the file + line referenced in the error
├── Understand what the code is TRYING to do (not just what failed)
├── Check the data flow: where does the undefined/null/wrong-type value come from?
├── Check recent changes: did a recent commit introduce this?
├── Check patterns: does this error match a known pattern for this framework/language?
└── Check siblings: are similar errors happening elsewhere?
```

### Layer 3: Plain Language Translation

The enriched error is translated into three outputs:

```
1. WHAT HAPPENED (one sentence, no jargon)
   "Your code tried to use a list of users before the list was loaded."

2. WHY IT HAPPENED (root cause, in your codebase)
   "useState(undefined) + useEffect(async fetch) = undefined on first render."

3. HOW TO FIX IT (specific to your code, not generic advice)
   "Line 8: Change useState() to useState([])"
```

## Error Pattern Library

### JavaScript/TypeScript

| Cryptic Error | Plain Translation | Common Fix |
|---|---|---|
| `Cannot read properties of undefined (reading 'x')` | You're accessing `.x` on something that doesn't exist | Add optional chaining `?.x` or check for null/undefined first |
| `x is not a function` | You're calling something that isn't callable — it's a value, not a function | Check: did you forget `()` on a prior call? Is the import correct? |
| `Maximum call stack size exceeded` | Infinite recursion — a function calls itself forever | Find the recursive call missing its base case |
| `Cannot assign to 'x' because it is a read-only property` | You're mutating something that shouldn't be mutated | Use spread/Object.assign to create a new object instead |
| `Module not found: Can't resolve 'x'` | Import path is wrong or package isn't installed | Check spelling, check node_modules, run npm install |
| `TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'` | Type mismatch — you're passing the wrong shape of data | Check what the function expects vs. what you're giving it |

### Python

| Cryptic Error | Plain Translation | Common Fix |
|---|---|---|
| `AttributeError: 'NoneType' object has no attribute 'x'` | A function returned None when you expected an object | The function upstream returned nothing — check its return paths |
| `IndentationError: unexpected indent` | Whitespace is wrong (tabs vs. spaces or wrong level) | Fix indentation — use consistent spaces |
| `RecursionError: maximum recursion depth exceeded` | Infinite recursion | Find the missing base case in your recursive function |
| `KeyError: 'x'` | You're accessing a dictionary key that doesn't exist | Use `.get('x', default)` or check `if 'x' in dict` first |
| `ImportError: cannot import name 'x' from 'y'` | The thing you're importing doesn't exist in that module | Check spelling, check the module's `__init__.py`, check version |

### Rust

| Cryptic Error | Plain Translation | Common Fix |
|---|---|---|
| `E0382: borrow of moved value: 'x'` | You used a value after giving ownership to something else | Clone it, use a reference, or restructure to avoid the move |
| `E0308: mismatched types` | Expected one type, got another | Check your function signatures and return types |
| `E0502: cannot borrow 'x' as mutable because it is also borrowed as immutable` | You have a read reference and are trying to write | Restructure to not hold both borrows simultaneously |
| `E0106: missing lifetime specifier` | Rust can't figure out how long a reference should live | Add explicit lifetime annotations |

### Go

| Cryptic Error | Plain Translation | Common Fix |
|---|---|---|
| `cannot use x (type Y) as type Z` | Type mismatch in assignment or function call | Check the expected type and convert |
| `undefined: x` | Using a name that doesn't exist in this scope | Check import, check spelling, check scope |
| `fatal error: all goroutines are asleep - deadlock!` | Every goroutine is waiting for something and nothing can proceed | Check channel operations — something isn't sending or receiving |
| `panic: runtime error: index out of range` | Array/slice access beyond its length | Check bounds before accessing |

### System/OS Errors

| Cryptic Error | Plain Translation | Common Fix |
|---|---|---|
| `ENOENT: no such file or directory` | File or directory doesn't exist at that path | Check the path — typo? Missing directory? Relative vs absolute? |
| `EACCES: permission denied` | You don't have permission to access this | Check file permissions, check if you need sudo/admin |
| `EADDRINUSE: address already in use` | Another process is already using that port | Kill the other process or use a different port |
| `ENOMEM: not enough memory` | System is out of memory | Check for memory leaks, increase available memory, or reduce consumption |
| `ETIMEDOUT: connection timed out` | The remote host didn't respond in time | Check network, check if the service is running, check firewall |

### HTTP Errors

| Code | What The Server Actually Means | Developer Action |
|---|---|---|
| `400 Bad Request` | "Your request is malformed — I can't even parse it" | Check request body format, content-type header, required fields |
| `401 Unauthorized` | "Who are you? I don't see valid credentials" | Check auth token, check if it's expired, check the auth header format |
| `403 Forbidden` | "I know who you are. You're not allowed" | Check permissions/roles, check if the resource requires different access |
| `404 Not Found` | "That URL doesn't point to anything" | Check the URL path, check if the resource exists, check API version |
| `409 Conflict` | "This conflicts with the current state" | Check for duplicate resources, check version/ETag conflicts |
| `422 Unprocessable Entity` | "I can read your request but the data doesn't make sense" | Check validation rules, check field values against API docs |
| `429 Too Many Requests` | "Slow down. You're hitting the rate limit" | Add backoff/retry logic, check rate limit headers |
| `500 Internal Server Error` | "Something broke on my end, not your fault" | Check server logs, it's a bug in the backend |
| `502 Bad Gateway` | "I'm a proxy and the server behind me is broken" | Check the upstream service, check proxy config |
| `503 Service Unavailable` | "I'm overloaded or doing maintenance" | Retry with backoff, check status page |

## The Translation Process

```
INPUT: Error message, stack trace, or log output (paste the whole thing)

Phase 1: PARSE
├── Identify error type, code, message, and location
├── Extract stack trace frames
├── Identify the framework/language/tool that produced the error
└── Separate signal from noise (framework internals vs. your code)

Phase 2: LOCATE
├── Find YOUR code in the stack trace (skip framework frames)
├── Read the file and line where the error originated
├── Read the surrounding context (function, class, module)
└── Trace the data flow to the error point

Phase 3: DIAGNOSE
├── Match against known error patterns for this language/framework
├── Analyze the specific code context (not generic advice)
├── Identify the root cause (not the symptom)
├── Check: is this a new bug or a recurring pattern?
└── Check: did a recent change introduce this?

Phase 4: PRESCRIBE
├── Plain English explanation (one sentence)
├── Root cause in your code (specific file, line, variable)
├── Exact fix (code change, not concept)
├── Prevention (how to avoid this class of error in the future)
└── Confidence level (how certain is this diagnosis)
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                    ERROR ROSETTA                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ERROR: TypeError: Cannot read properties of undefined       ║
║         (reading 'map')                                      ║
║                                                              ║
║  TRANSLATION:                                                ║
║  Your UserList component renders before the API response     ║
║  arrives. On the first render, `users` is undefined, and     ║
║  you're calling .map() on undefined.                         ║
║                                                              ║
║  ROOT CAUSE:                                                 ║
║  src/components/UserList.tsx:8                                ║
║    const [users, setUsers] = useState();  ← initialized as  ║
║    undefined, not as empty array                             ║
║                                                              ║
║  FIX:                                                        ║
║  Line 8: useState()  →  useState([])                         ║
║                                                              ║
║  PREVENTION:                                                 ║
║  Always initialize state with the correct empty type:        ║
║    Arrays: useState([])                                      ║
║    Objects: useState(null) with explicit null check           ║
║    Strings: useState('')                                     ║
║                                                              ║
║  CONFIDENCE: 95% (matches React uninitialized-state pattern) ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- **Every time you see an error you don't immediately understand.** That's the whole point.
- When onboarding in a new language or framework (the error messages are a new dialect)
- When the error is in a dependency's code and you need to understand what YOU did wrong
- When debugging a CI failure with a wall of log output
- When a user reports an error and you need to decode it fast

## Why It Matters

Developers spend 35-50% of their time debugging. A significant portion of that time is spent **understanding what the error message is telling them** — not fixing the actual bug. The faster you decode the message, the faster you fix the problem.

Error Rosetta doesn't fix bugs. It removes the translation step between seeing the error and understanding the error. Everything after that is just typing.

Zero external dependencies. Zero API calls. Pure pattern matching and code analysis.
