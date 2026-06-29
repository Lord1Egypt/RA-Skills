# Language-Specific Best Practices

## JavaScript / TypeScript

### Modern Syntax
- Use `const` by default, `let` when reassignment needed, never `var`
- Use arrow functions for callbacks and short functions; use `function` for methods and constructors
- Use template literals over string concatenation
- Use destructuring for object/array extraction
- Use spread operator instead of `Object.assign` for immutability
- Use optional chaining (`?.`) and nullish coalescing (`??`) instead of manual checks

### TypeScript Specific
- Enable `strict: true` in tsconfig.json
- Avoid `any` type - use `unknown` when type is truly unknown, then narrow
- Use `interface` for object shapes, `type` for unions and intersections
- Use `enum` or union types for fixed value sets
- Prefer `readonly` for immutable properties
- Use generics for reusable components/functions
- Enable `noUncheckedIndexedAccess` for safer array/object access

### Async Patterns
- Use `async/await` over `.then()` chains for readability
- Always handle promise rejections (try/catch or .catch())
- Use `Promise.all()` for parallel operations, not sequential awaits
- Avoid fire-and-forget async calls (always await or handle)
- Use `AbortController` for cancellable fetch requests

### Node.js
- Use `path.join()` / `path.resolve()` instead of string concatenation for paths
- Use `fs.promises` (async) over `fs` (sync) in server code
- Validate input with Zod / Joi / express-validator at API boundaries
- Use `crypto.randomUUID()` for ID generation, not `Math.random()`
- Set `helmet()` middleware for security headers
- Use `express-rate-limit` for API rate limiting

### Common Anti-Patterns
- Mutating function arguments
- Comparing with `==` instead of `===`
- Using `forEach` when `map`/`filter`/`reduce` is intended
- Async function without await inside (missing `await` keyword)
- `any` type in TypeScript (loss of type safety)
- Empty catch blocks (`catch (e) {}`)

---

## Python

### Modern Syntax (3.9+)
- Use type hints on all function signatures (`def foo(x: int) -> str:`)
- Use `from __future__ import annotations` for forward references
- Use f-strings for string formatting (not `%` or `.format()`)
- Use `pathlib.Path` instead of `os.path` for path manipulation
- Use dataclasses or Pydantic for data containers
- Use `match` statement for complex pattern matching (3.10+)
- Use `walrus operator` (`:=`) for assignment expressions where it improves readability

### Error Handling
- Catch specific exceptions, not bare `except:` or `except Exception:`
- Use context managers (`with` statements) for resource management
- Raise exceptions with meaningful messages and proper exception types
- Use custom exception hierarchies for application-specific errors
- Never use `except: pass` - at minimum log the error

### Security
- Use `secrets` module for tokens/passwords, not `random`
- Use `bcrypt` or `argon2-cffi` for password hashing
- Use parameterized queries with `psycopg2` / `SQLAlchemy` (never string concat)
- Use `yaml.safe_load()` not `yaml.load()`
- Use `subprocess.run()` with `shell=False` (list arguments, not string)
- Validate and sanitize all user input (use Pydantic or marshmallow)

### Code Organization
- One class per file for major classes
- Group related functions into modules
- Use `__all__` to define public API
- Use `if __name__ == "__main__":` guard for script entry points
- Keep `__init__.py` files minimal (re-exports only)

### Common Anti-Patterns
- Mutable default arguments (`def foo(items=[])`)
- Bare `except:` clauses
- Global variables for state management
- `import *` (use explicit imports)
- Comparing to `None` with `==` (use `is None`)
- Using `type()` for type checking (use `isinstance()`)

---

## Java

### Modern Java (11+)
- Use `var` for local variable type inference when type is obvious
- Use `record` for immutable data carriers (Java 16+)
- Use `switch` expressions with `->` and `yield` (Java 14+)
- Use `Optional<T>` for return types that may be absent (never as field type)
- Use `Stream API` for collection processing over manual loops
- Use `text blocks` (`"""..."""`) for multi-line strings (Java 15+)

### Spring Framework
- Use constructor injection over `@Autowired` field injection
- Use `@Transactional` at service layer, not controller
- Use `@RestController` + `@RequestMapping` for REST APIs
- Use `@Validated` / `@Valid` for request body validation
- Use `@ExceptionHandler` / `@ControllerAdvice` for global error handling
- Use `ResponseEntity<T>` for HTTP responses with proper status codes
- Use `@ConfigurationProperties` over `@Value` for grouped config

### Common Anti-Patterns
- `NullPointerException` from unchecked method chains
- Raw types (`List` instead of `List<String>`)
- `instanceof` chains (use polymorphism or sealed classes)
- `Thread.sleep()` in tests (use `Awaitility`)
- Catching `Exception` or `Throwable` broadly
- Using `Date` / `Calendar` (use `java.time.*`)

---

## Go

### Idiomatic Go
- Return errors as last return value, always check them
- Use `errors.Is()` and `errors.As()` for error comparison (not `==`)
- Use `context.Context` as first parameter in all functions that do I/O
- Use goroutines with proper cancellation (`ctx.Done()`)
- Use `sync.Mutex` / `sync.RWMutex` for shared state protection
- Use channels for goroutine communication, mutexes for state protection
- Prefer composition over inheritance (embed structs, don't subclass)
- Keep interfaces small (single-method interfaces are ideal)

### Error Handling
- Wrap errors with context: `fmt.Errorf("doing X: %w", err)`
- Use `errors.New()` for static errors, `fmt.Errorf()` for formatted
- Define sentinel errors: `var ErrNotFound = errors.New("not found")`
- Check errors immediately, don't ignore them (`_ = someFunc()` is a smell)

### Common Anti-Patterns
- Ignoring errors (`result, _ := doSomething()`)
- Starting goroutines without a way to stop them
- Global mutable state without synchronization
- Interface pollution (defining interfaces before multiple implementations exist)
- `panic()` in library code (return errors instead)
- `init()` side effects (keep init minimal)

---

## General (All Languages)

### SOLID Principles
- **S**ingle Responsibility: Each class/function has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable for base types
- **I**nterface Segregation: Many specific interfaces > one general interface
- **D**ependency Inversion: Depend on abstractions, not concretions

### Clean Code
- Functions should be small and do one thing
- Function names should be verbs, variable names should be nouns
- Avoid negative conditions (`if (!isNotValid)` is hard to read)
- Avoid deep nesting (use guard clauses / early returns)
- Comments should explain WHY, not WHAT
- Remove commented-out code (use version control)

### Version Control
- Commit messages: imperative mood, subject under 50 chars, body under 72
- One logical change per commit
- No secrets in commit history (use `.gitignore` and `git-secrets`)
- Branch names: `feature/`, `bugfix/`, `hotfix/` prefixes

### API Design
- REST: Use proper HTTP methods (GET/POST/PUT/PATCH/DELETE)
- Use plural nouns for resource paths (`/users`, not `/user`)
- Return appropriate HTTP status codes (not 200 for everything)
- Version APIs (`/api/v1/`) to allow breaking changes
- Paginate list endpoints (cursor-based preferred over offset)
- Use consistent naming (camelCase or snake_case, not mixed)
