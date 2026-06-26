#!/usr/bin/env bash
# ErrorLens -- Error Handling Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Dangerous error handling that will cause silent failures or data loss
#   high     -- Significant error handling gaps that reduce reliability
#   medium   -- Suboptimal error handling that should be improved
#   low      -- Informational, potential false positives, style preferences
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, \b, etc.)
#
# Categories:
#   EC -- Empty Catches        (EC-001 to EC-015)
#   SE -- Swallowed Exceptions (SE-001 to SE-015)
#   EB -- Error Boundaries     (EB-001 to EB-015)
#   GE -- Generic Errors       (GE-001 to GE-015)
#   RP -- Resource & Propagation (RP-001 to RP-015)
#   IL -- Information Leak     (IL-001 to IL-015)

set -euo pipefail

# ============================================================================
# 1. EMPTY CATCHES (EC-001 through EC-015)
# ============================================================================

declare -a ERRORLENS_EMPTY_CATCH_PATTERNS=()

ERRORLENS_EMPTY_CATCH_PATTERNS+=(
  # --- EC-001: Empty catch block in JS/TS (single line) ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|critical|EC-001|Empty catch block in JavaScript/TypeScript|Add error logging, rethrow, or handle the error explicitly; never silently swallow exceptions'

  # --- EC-002: Empty catch block in Java ---
  'catch[[:space:]]*\([[:space:]]*(Exception|Throwable|Error|IOException|RuntimeException|SQLException)[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\)[[:space:]]*\{[[:space:]]*\}|critical|EC-002|Empty catch block in Java|Add logging with the exception details, rethrow, or handle the error; empty catches mask bugs'

  # --- EC-003: Empty catch block in C# ---
  'catch[[:space:]]*\([[:space:]]*(Exception|SystemException|ApplicationException|IOException|InvalidOperationException)[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\)[[:space:]]*\{[[:space:]]*\}|critical|EC-003|Empty catch block in C#|Add logging or rethrow; empty catches violate exception safety principles'

  # --- EC-004: Catch block with only a comment (JS/TS/Java/C#) ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*/[/*].*[[:space:]]*\}|high|EC-004|Catch block contains only a comment -- effectively empty|Replace the comment with actual error handling: log, rethrow, or recover'

  # --- EC-005: Python bare except with pass ---
  'except[[:space:]]*:[[:space:]]*$|critical|EC-005|Python bare except clause (catches all exceptions including SystemExit, KeyboardInterrupt)|Use specific exception types: except ValueError, except IOError, etc.'

  # --- EC-006: Python except with only pass ---
  'except[[:space:]].*:[[:space:]]*pass[[:space:]]*$|critical|EC-006|Python except block with only pass -- silently swallows exception|Log the exception, reraise, or handle explicitly; pass hides bugs'

  # --- EC-007: Python except Exception with pass ---
  'except[[:space:]]+Exception[[:space:]]*.*:[[:space:]]*pass|critical|EC-007|Python except Exception with pass -- swallows all standard exceptions|At minimum log the exception; consider handling specific exception types'

  # --- EC-008: JS/TS catch block with only console.log of a string ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*console\.log\(['"'"'"][^'"'"'"]*['"'"'"]\)[[:space:]]*;?[[:space:]]*\}|medium|EC-008|Catch block only logs a static string, ignoring the error object|Include the error object in the log: console.error(message, error)'

  # --- EC-009: Empty catch-all in JS/TS (no parameter) ---
  'catch[[:space:]]*\{[[:space:]]*\}|critical|EC-009|Empty catch block with no parameter in JavaScript/TypeScript|Add error handling; a completely empty catch silently discards all errors'

  # --- EC-010: Java catch with empty body on multiple lines ---
  'catch[[:space:]]*\([^)]+\)[[:space:]]*\{[[:space:]]*(//[^\n]*)?\}|high|EC-010|Java/C# catch block with empty or comment-only body|Add proper error handling: logging, rethrowing, or recovery logic'

  # --- EC-011: C# empty catch without parameter ---
  'catch[[:space:]]*\{[[:space:]]*\}|critical|EC-011|C# catch-all block with no exception parameter -- swallows all exceptions|Specify an exception type and add handling: catch (SpecificException ex) { ... }'

  # --- EC-012: Kotlin/Scala try-catch with empty catch ---
  'catch[[:space:]]*\{[[:space:]]*_[[:space:]]*->[[:space:]]*\}|high|EC-012|Kotlin catch block with discarded exception (underscore)|Handle the exception or log it; discarding with _ masks failures'

  # --- EC-013: Ruby empty rescue block ---
  'rescue[[:space:]].*=>?[[:space:]]*[a-z_]*[[:space:]]*$|medium|EC-013|Ruby rescue block that may be empty or only captures without handling|Ensure the rescued exception is logged, reraised, or handled'

  # --- EC-014: Go blank identifier for error ---
  'if[[:space:]]+_[[:space:]]*,[[:space:]]*err[[:space:]]*:=[[:space:]]|medium|EC-014|Go error assignment pattern where error may be ignored in subsequent code|Always check the err return value; do not discard with _'

  # --- EC-015: PHP empty catch block ---
  'catch[[:space:]]*\([[:space:]]*(Exception|\$[a-z])[^)]*\)[[:space:]]*\{[[:space:]]*\}|critical|EC-015|PHP empty catch block -- silently swallows exception|Add error logging or handling; empty catches are a security and reliability risk'
)

# ============================================================================
# 2. SWALLOWED EXCEPTIONS (SE-001 through SE-015)
# ============================================================================

declare -a ERRORLENS_SWALLOWED_PATTERNS=()

ERRORLENS_SWALLOWED_PATTERNS+=(
  # --- SE-001: Catch returns null (JS/TS) ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]+null[[:space:]]*;?[[:space:]]*\}|critical|SE-001|Catch block returns null, silently swallowing the exception|Log the error and return a meaningful error value, throw, or use a Result type'

  # --- SE-002: Catch returns undefined (JS/TS) ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]+undefined[[:space:]]*;?[[:space:]]*\}|critical|SE-002|Catch block returns undefined, silently swallowing the exception|Log the error and rethrow or return a typed error result'

  # --- SE-003: Catch returns false (JS/TS/Java) ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]+false[[:space:]]*;?[[:space:]]*\}|high|SE-003|Catch block returns false, masking the real error|Propagate or log the original error; boolean returns hide failure details'

  # --- SE-004: Catch returns empty string ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]+['"'"'"]['"'"'"][[:space:]]*;?[[:space:]]*\}|high|SE-004|Catch block returns empty string, discarding error information|Return the error message or rethrow; empty strings hide failures'

  # --- SE-005: Catch returns -1 (error code swallowing) ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]+-1[[:space:]]*;?[[:space:]]*\}|medium|SE-005|Catch block returns -1 error code, losing exception detail|Log the original exception before returning error codes; consider typed error returns'

  # --- SE-006: Python except that returns None ---
  'except[[:space:]].*:[[:space:]]*return[[:space:]]+None|high|SE-006|Python except block returns None, swallowing the exception|Log the exception, reraise, or return a meaningful error indicator'

  # --- SE-007: console.log instead of console.error in catch ---
  'catch[[:space:]]*\([[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\)[[:space:]]*\{[[:space:]]*console\.log\(|medium|SE-007|Using console.log instead of console.error in catch block|Use console.error() for error logging to ensure proper output stream'

  # --- SE-008: Exception variable unused in catch (JS/TS) ---
  'catch[[:space:]]*\([[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*)[[:space:]]*\)[[:space:]]*\{[^}]*\}|medium|SE-008|Exception variable may be unused in catch block -- check for swallowed error|Reference the caught exception in logging or error handling within the catch block'

  # --- SE-009: Go error explicitly ignored with blank identifier ---
  '[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*,[[:space:]]*_[[:space:]]*:?=[[:space:]]*[a-zA-Z_]|high|SE-009|Go error return value explicitly discarded with blank identifier (_)|Always handle error returns; use if err != nil pattern'

  # --- SE-010: Catch that only sets a boolean flag ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*[a-zA-Z_]*[Ee]rror[a-zA-Z_]*[[:space:]]*=[[:space:]]*(true|false)|medium|SE-010|Catch block only sets a boolean flag, losing error detail|Preserve the error message or stack trace alongside the flag'

  # --- SE-011: Promise .catch with empty callback ---
  '\.catch\([[:space:]]*\([[:space:]]*\)[[:space:]]*=>[[:space:]]*\{[[:space:]]*\}[[:space:]]*\)|critical|SE-011|Promise .catch() with empty callback -- silently swallows rejection|Handle or log the rejection; empty .catch() hides async failures'

  # --- SE-012: Promise .catch with noop function ---
  '\.catch\([[:space:]]*\(\)[[:space:]]*=>[[:space:]]*null[[:space:]]*\)|critical|SE-012|Promise .catch() returns null -- swallows rejection|Handle or log the rejection reason; returning null hides async errors'

  # --- SE-013: Promise .catch with console.log of static text ---
  '\.catch\([[:space:]]*\(\)[[:space:]]*=>[[:space:]]*console\.log\(['"'"'"][^'"'"'"]*['"'"'"]\)|medium|SE-013|Promise .catch() logs static text, ignoring the rejection reason|Include the error object: .catch(err => console.error(message, err))'

  # --- SE-014: Java catch that only returns null ---
  'catch[[:space:]]*\([[:space:]]*(Exception|Throwable)[[:space:]]+[a-zA-Z_]+[[:space:]]*\)[[:space:]]*\{[[:space:]]*return[[:space:]]+null|critical|SE-014|Java catch block returns null, swallowing the exception|Log the exception or rethrow wrapped in a custom exception'

  # --- SE-015: C# catch that only breaks/continues ---
  'catch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*(break|continue)[[:space:]]*;[[:space:]]*\}|high|SE-015|Catch block only breaks/continues loop, silently swallowing the exception|Log the error before break/continue to preserve diagnostic information'
)

# ============================================================================
# 3. ERROR BOUNDARIES (EB-001 through EB-015)
# ============================================================================

declare -a ERRORLENS_BOUNDARY_PATTERNS=()

ERRORLENS_BOUNDARY_PATTERNS+=(
  # --- EB-001: Unhandled promise rejection (Node.js) ---
  'process\.on\(['"'"'"]unhandledRejection['"'"'"][[:space:]]*,[[:space:]]*\([[:space:]]*\)[[:space:]]*=>|high|EB-001|Unhandled rejection handler with empty callback|Add logging and graceful shutdown logic to the unhandledRejection handler'

  # --- EB-002: Missing unhandledRejection handler indicator ---
  'new[[:space:]]+Promise[[:space:]]*\([[:space:]]*\([[:space:]]*(resolve|reject|res|rej)[[:space:]]*\)|medium|EB-002|Promise constructor found -- ensure unhandledRejection handler exists|Add process.on(unhandledRejection) handler if not already present in your app entry point'

  # --- EB-003: Async function without try-catch ---
  'async[[:space:]]+function[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*[^t]|medium|EB-003|Async function may lack try-catch -- unhandled rejections possible|Wrap async function body in try-catch or use a global error handler'

  # --- EB-004: Express route without error handling ---
  'app\.(get|post|put|delete|patch)\([[:space:]]*['"'"'"/][^,]*,[[:space:]]*async[[:space:]]*\(req|medium|EB-004|Express async route handler -- ensure errors are forwarded to error middleware|Wrap handler in try-catch and call next(error), or use express-async-errors'

  # --- EB-005: Express app without error middleware ---
  'app\.listen\([[:space:]]*[0-9]|medium|EB-005|Express app.listen found -- verify error middleware is registered|Ensure app.use((err, req, res, next) => ...) is registered before app.listen()'

  # --- EB-006: React component without error boundary ---
  'class[[:space:]]+[A-Z][a-zA-Z]*[[:space:]]+extends[[:space:]]+React\.Component|medium|EB-006|React class component found -- consider wrapping in an error boundary|Add a componentDidCatch or static getDerivedStateFromError method, or wrap with an ErrorBoundary component'

  # --- EB-007: React componentDidCatch with empty body ---
  'componentDidCatch[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|critical|EB-007|React componentDidCatch is empty -- errors will be silently swallowed|Log the error and errorInfo to an error reporting service'

  # --- EB-008: window.onerror with empty handler ---
  'window\.onerror[[:space:]]*=[[:space:]]*function[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|critical|EB-008|window.onerror handler is empty -- browser errors will be silently lost|Add error logging to a monitoring service in the onerror handler'

  # --- EB-009: addEventListener error with empty handler ---
  'addEventListener\([[:space:]]*['"'"'"]error['"'"'"][[:space:]]*,[[:space:]]*function[[:space:]]*\([^)]*\)[[:space:]]*\{[[:space:]]*\}|high|EB-009|Error event listener with empty handler|Add error logging or reporting to the error event handler'

  # --- EB-010: Koa without error middleware ---
  'const[[:space:]]+app[[:space:]]*=[[:space:]]*new[[:space:]]+Koa|medium|EB-010|Koa application found -- ensure error middleware is registered|Add app.on(error, handler) and error-handling middleware early in the middleware chain'

  # --- EB-011: Fastify without error handler ---
  'fastify\.(listen|register)|medium|EB-011|Fastify application found -- ensure error handler is configured|Use fastify.setErrorHandler() to register a global error handler'

  # --- EB-012: Python Flask without errorhandler ---
  'app[[:space:]]*=[[:space:]]*Flask\(|medium|EB-012|Flask application found -- ensure error handlers are registered|Add @app.errorhandler(Exception) and @app.errorhandler(500) decorators'

  # --- EB-013: Python Django without exception middleware ---
  'MIDDLEWARE[[:space:]]*=[[:space:]]*\[|medium|EB-013|Django MIDDLEWARE setting found -- verify exception handling middleware exists|Ensure a custom exception handling middleware is in the MIDDLEWARE list'

  # --- EB-014: Java Spring without @ExceptionHandler ---
  '@RestController|medium|EB-014|Spring @RestController found -- ensure @ControllerAdvice with @ExceptionHandler exists|Create a @ControllerAdvice class with @ExceptionHandler methods for proper API error handling'

  # --- EB-015: .NET without global exception handler ---
  'app\.UseExceptionHandler|low|EB-015|ASP.NET UseExceptionHandler found -- verify it has proper error handling|Ensure the exception handler middleware logs errors and returns appropriate HTTP responses'
)

# ============================================================================
# 4. GENERIC ERRORS (GE-001 through GE-015)
# ============================================================================

declare -a ERRORLENS_GENERIC_PATTERNS=()

ERRORLENS_GENERIC_PATTERNS+=(
  # --- GE-001: Throwing generic Error in JS/TS ---
  'throw[[:space:]]+new[[:space:]]+Error\([[:space:]]*['"'"'"][^'"'"'"]*['"'"'"][[:space:]]*\)|high|GE-001|Throwing generic Error instead of a specific error subclass|Create and throw custom error classes (e.g., ValidationError, NotFoundError) for better error handling'

  # --- GE-002: Throwing string literal in JS/TS ---
  'throw[[:space:]]+['"'"'"][^'"'"'"]+['"'"'"]|critical|GE-002|Throwing a string literal instead of an Error object|Throw new Error(message) or a custom error class; string throws lose stack traces'

  # --- GE-003: Throwing non-Error object in JS/TS ---
  'throw[[:space:]]+\{|high|GE-003|Throwing a plain object instead of an Error instance|Throw new Error() or a custom error class; plain objects lack stack traces'

  # --- GE-004: Python bare except (no exception type) ---
  '^[[:space:]]*except[[:space:]]*:|critical|GE-004|Python bare except clause catches all exceptions including SystemExit and KeyboardInterrupt|Specify exception types: except (ValueError, TypeError) or at minimum except Exception'

  # --- GE-005: Python catching BaseException ---
  'except[[:space:]]+BaseException|critical|GE-005|Python except BaseException catches SystemExit, KeyboardInterrupt, and GeneratorExit|Use except Exception to avoid catching system-level exceptions'

  # --- GE-006: Python raise without exception type ---
  '^[[:space:]]*raise[[:space:]]+Exception\([[:space:]]*['"'"'"]|high|GE-006|Raising generic Exception instead of a specific exception type|Create and raise specific exceptions (e.g., ValueError, custom exceptions)'

  # --- GE-007: Java catching Throwable ---
  'catch[[:space:]]*\([[:space:]]*Throwable[[:space:]]|critical|GE-007|Catching Throwable in Java -- includes Errors that should not be caught|Catch specific exception types; catching Throwable masks JVM errors like OutOfMemoryError'

  # --- GE-008: Java catching generic Exception ---
  'catch[[:space:]]*\([[:space:]]*Exception[[:space:]]+[a-zA-Z_]|high|GE-008|Catching generic Exception in Java -- overly broad error handling|Catch specific exception types (IOException, SQLException, etc.) for targeted handling'

  # --- GE-009: Java throwing generic RuntimeException ---
  'throw[[:space:]]+new[[:space:]]+RuntimeException\(|high|GE-009|Throwing generic RuntimeException in Java|Create and throw specific exception subclasses for better API contracts'

  # --- GE-010: C# catching System.Exception ---
  'catch[[:space:]]*\([[:space:]]*(System\.)?Exception[[:space:]]|high|GE-010|Catching generic System.Exception in C#|Catch specific exception types (ArgumentException, InvalidOperationException, etc.)'

  # --- GE-011: C# throwing generic Exception ---
  'throw[[:space:]]+new[[:space:]]+Exception\([[:space:]]*"|high|GE-011|Throwing generic Exception in C#|Create and throw specific exception types that inherit from Exception'

  # --- GE-012: Go generic errors.New with format string ---
  'errors\.New\([[:space:]]*fmt\.Sprintf|medium|GE-012|Using errors.New with fmt.Sprintf -- consider using fmt.Errorf directly|Use fmt.Errorf(format, args...) which is more idiomatic and supports %w for wrapping'

  # --- GE-013: Rust panic! in library code ---
  'panic!\([[:space:]]*"|high|GE-013|Using panic! which will crash the program -- prefer returning Result or Option|Return Result<T, E> or Option<T> instead of panicking; reserve panic! for truly unrecoverable states'

  # --- GE-014: TypeScript catching unknown as any ---
  'catch[[:space:]]*\([[:space:]]*[a-zA-Z_]+[[:space:]]*:[[:space:]]*any[[:space:]]*\)|medium|GE-014|TypeScript catch with any type annotation loses type safety|Use catch (error: unknown) and narrow the type with instanceof checks'

  # --- GE-015: Kotlin catching Exception broadly ---
  'catch[[:space:]]*\([[:space:]]*e[[:space:]]*:[[:space:]]*Exception[[:space:]]*\)|high|GE-015|Kotlin catching generic Exception -- overly broad|Catch specific exception types for targeted handling'
)

# ============================================================================
# 5. RESOURCE & PROPAGATION (RP-001 through RP-015)
# ============================================================================

declare -a ERRORLENS_RESOURCE_PATTERNS=()

ERRORLENS_RESOURCE_PATTERNS+=(
  # --- RP-001: Try without finally for resource (Java) ---
  'new[[:space:]]+(FileInputStream|FileOutputStream|BufferedReader|BufferedWriter|Connection|PreparedStatement|Socket)\(|medium|RP-001|Resource opened without try-with-resources in Java|Use try-with-resources: try (var r = new Resource()) { ... } for automatic cleanup'

  # --- RP-002: Try without finally for file handles (Python) ---
  'open\([[:space:]]*['"'"'"][^'"'"'"]+['"'"'"][[:space:]]*,[[:space:]]*['"'"'"][rwa]|medium|RP-002|File opened -- ensure it is used with a context manager (with statement)|Use with open(path) as f: for automatic file handle cleanup'

  # --- RP-003: Go error return not checked (common pattern) ---
  '[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*=[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*\.[A-Z][a-zA-Z]*\([^)]*\)[[:space:]]*$|medium|RP-003|Go function call result assigned without error check -- may discard errors|Use multi-return with error: result, err := fn(); if err != nil { return err }'

  # --- RP-004: Go explicitly discarding error with _ ---
  '_[[:space:]]*=[[:space:]]*[a-zA-Z_][a-zA-Z0-9_.]*\([^)]*\)|critical|RP-004|Go error return explicitly discarded with blank identifier (_)|Handle the error: if err := fn(); err != nil { return fmt.Errorf(\"context: %w\", err) }'

  # --- RP-005: Go defer without error check ---
  'defer[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*\.Close\(\)|medium|RP-005|Go defer Close() without checking the error return|Wrap in a closure: defer func() { if err := r.Close(); err != nil { log(err) } }()'

  # --- RP-006: Rust unwrap on Result ---
  '\.unwrap\(\)|high|RP-006|Rust .unwrap() will panic on Err -- unsafe in production code|Use ? operator, .unwrap_or(), .unwrap_or_else(), or match for safe error handling'

  # --- RP-007: Rust expect in non-test code ---
  '\.expect\([[:space:]]*"|medium|RP-007|Rust .expect() will panic with message on Err -- consider proper error propagation|Use ? operator or match for recoverable errors; reserve .expect() for truly impossible cases'

  # --- RP-008: Rust ignoring Result with let _ ---
  'let[[:space:]]+_[[:space:]]*=[[:space:]]*[a-zA-Z_][a-zA-Z0-9_:]*\(|medium|RP-008|Rust Result explicitly ignored with let _ -- potential silent failure|Handle the Result with match, if let Err, or propagate with ?'

  # --- RP-009: Missing error propagation in async JS/TS ---
  'await[[:space:]]+[a-zA-Z_][a-zA-Z0-9_.]*\([^)]*\)[[:space:]]*;[[:space:]]*$|low|RP-009|Await without try-catch or .catch() -- unhandled rejection possible|Wrap in try-catch or ensure a global unhandledRejection handler exists'

  # --- RP-010: Go os.Exit without cleanup ---
  'os\.Exit\([[:space:]]*[0-9]+[[:space:]]*\)|medium|RP-010|os.Exit() bypasses deferred cleanup functions|Use return from main() or a controlled shutdown to ensure deferred functions execute'

  # --- RP-011: C# Dispose without try-finally or using ---
  '\.Dispose\(\)|medium|RP-011|Manual Dispose() call -- may not execute if an exception occurs before it|Use using statement or try-finally to guarantee resource disposal'

  # --- RP-012: Java close() outside finally block ---
  '\.(close|disconnect|shutdown)\(\)|medium|RP-012|Resource close/shutdown call may not execute on exception path|Use try-with-resources or ensure close() is in a finally block'

  # --- RP-013: Node.js createReadStream without error handler ---
  'createReadStream\([^)]+\)|medium|RP-013|Node.js stream created -- ensure error event handler is attached|Add stream.on(error, handler) immediately after creation'

  # --- RP-014: Python subprocess without error handling ---
  'subprocess\.(run|call|Popen)\(|medium|RP-014|Python subprocess call -- ensure CalledProcessError is handled|Use subprocess.run(check=True) or handle CalledProcessError explicitly'

  # --- RP-015: Go http handler without error response ---
  'func[[:space:]]+[a-zA-Z_]*[Hh]andler[[:space:]]*\([[:space:]]*w[[:space:]]+http\.ResponseWriter|medium|RP-015|Go HTTP handler -- ensure all error paths write an HTTP error response|Use http.Error(w, message, statusCode) on all error branches'
)

# ============================================================================
# 6. INFORMATION LEAK (IL-001 through IL-015)
# ============================================================================

declare -a ERRORLENS_INFOLEAK_PATTERNS=()

ERRORLENS_INFOLEAK_PATTERNS+=(
  # --- IL-001: Stack trace in HTTP response (Express/Node) ---
  'res\.(send|json|write)\([^)]*err\.(stack|message|toString)|critical|IL-001|Error stack trace or message sent directly in HTTP response|Send a generic error message to the client; log the full error server-side'

  # --- IL-002: Stack trace in res.status().json ---
  'res\.status\([0-9]+\)\.(json|send)\([[:space:]]*\{[^}]*stack|critical|IL-002|Stack trace included in HTTP error response body|Remove stack trace from response; return only a user-safe error message and error code'

  # --- IL-003: Express error handler exposing error details ---
  'res\.(json|send)\([[:space:]]*\{[^}]*(error|err|exception)[[:space:]]*:[[:space:]]*(err|error|e)\.|high|IL-003|Error object properties exposed in API response|Map errors to safe response objects; never pass raw error properties to clients'

  # --- IL-004: Python traceback in HTTP response ---
  'traceback\.(format_exc|print_exc|format_tb)|high|IL-004|Python traceback formatting -- ensure output is not sent to HTTP responses|Log tracebacks server-side only; return generic error messages to clients'

  # --- IL-005: Python returning exception string to client ---
  'return[[:space:]]+(str\(e\)|str\(err\)|str\(exception\))|high|IL-005|Python converting exception to string for return value -- may leak to client|Return a generic error message; log the exception details server-side'

  # --- IL-006: Java printStackTrace in web context ---
  '\.printStackTrace\(\)|high|IL-006|Java printStackTrace() writes to stderr -- may leak to logs or error pages|Use a logging framework (SLF4J, Log4j) with appropriate log levels instead'

  # --- IL-007: C# ToString on exception in response ---
  'exception\.ToString\(\)|high|IL-007|C# exception.ToString() includes full stack trace -- may leak in responses|Use exception.Message for user-facing text; log full details separately'

  # --- IL-008: Django DEBUG = True in settings ---
  'DEBUG[[:space:]]*=[[:space:]]*True|high|IL-008|Django DEBUG mode is True -- exposes detailed error pages to users|Set DEBUG = False in production; use environment variables for configuration'

  # --- IL-009: Node.js NODE_ENV not production check ---
  'NODE_ENV[[:space:]]*!==[[:space:]]*['"'"'"]production['"'"'"]|medium|IL-009|Code path conditional on non-production NODE_ENV -- may leak debug info|Ensure error detail exposure is explicitly disabled in production'

  # --- IL-010: Flask debug mode enabled ---
  'app\.run\([^)]*debug[[:space:]]*=[[:space:]]*True|high|IL-010|Flask debug mode is enabled -- exposes interactive debugger and stack traces|Set debug=False in production; use environment variables for configuration'

  # --- IL-011: Spring Boot detailed error attributes ---
  'server\.error\.include-stacktrace[[:space:]]*=[[:space:]]*always|critical|IL-011|Spring Boot configured to always include stack traces in error responses|Set server.error.include-stacktrace=never in production configuration'

  # --- IL-012: ASP.NET developer exception page ---
  'UseDeveloperExceptionPage|high|IL-012|ASP.NET Developer Exception Page exposes detailed error information|Use UseExceptionHandler in production; restrict UseDeveloperExceptionPage to development'

  # --- IL-013: PHP display_errors enabled ---
  'display_errors[[:space:]]*=[[:space:]]*(On|1|true)|critical|IL-013|PHP display_errors is enabled -- exposes error details to users|Set display_errors = Off in production; use error_log for server-side logging'

  # --- IL-014: Error message includes file path ---
  '(error|err|exception).*(__FILE__|__file__|__dirname|__filename)|medium|IL-014|Error message may include server file paths -- information disclosure risk|Remove file path references from user-facing error messages'

  # --- IL-015: Verbose SQL error in response ---
  '(res\.(send|json)|return)[[:space:]]*\([^)]*sql[[:space:]]*(error|err|exception)|critical|IL-015|SQL error details may be exposed in HTTP response|Never expose SQL errors to clients; log them server-side and return a generic database error message'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
errorlens_pattern_count() {
  local count=0
  count=$((count + ${#ERRORLENS_EMPTY_CATCH_PATTERNS[@]}))
  count=$((count + ${#ERRORLENS_SWALLOWED_PATTERNS[@]}))
  count=$((count + ${#ERRORLENS_BOUNDARY_PATTERNS[@]}))
  count=$((count + ${#ERRORLENS_GENERIC_PATTERNS[@]}))
  count=$((count + ${#ERRORLENS_RESOURCE_PATTERNS[@]}))
  count=$((count + ${#ERRORLENS_INFOLEAK_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
errorlens_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    EMPTY_CATCH) _patterns_ref=ERRORLENS_EMPTY_CATCH_PATTERNS ;;
    SWALLOWED)   _patterns_ref=ERRORLENS_SWALLOWED_PATTERNS ;;
    BOUNDARY)    _patterns_ref=ERRORLENS_BOUNDARY_PATTERNS ;;
    GENERIC)     _patterns_ref=ERRORLENS_GENERIC_PATTERNS ;;
    RESOURCE)    _patterns_ref=ERRORLENS_RESOURCE_PATTERNS ;;
    INFOLEAK)    _patterns_ref=ERRORLENS_INFOLEAK_PATTERNS ;;
    all)
      errorlens_list_patterns "EMPTY_CATCH"
      errorlens_list_patterns "SWALLOWED"
      errorlens_list_patterns "BOUNDARY"
      errorlens_list_patterns "GENERIC"
      errorlens_list_patterns "RESOURCE"
      errorlens_list_patterns "INFOLEAK"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a category
get_errorlens_patterns_for_category() {
  local category="$1"
  case "$category" in
    empty_catch) echo "ERRORLENS_EMPTY_CATCH_PATTERNS" ;;
    swallowed)   echo "ERRORLENS_SWALLOWED_PATTERNS" ;;
    boundary)    echo "ERRORLENS_BOUNDARY_PATTERNS" ;;
    generic)     echo "ERRORLENS_GENERIC_PATTERNS" ;;
    resource)    echo "ERRORLENS_RESOURCE_PATTERNS" ;;
    infoleak)    echo "ERRORLENS_INFOLEAK_PATTERNS" ;;
    *)           echo "" ;;
  esac
}

# All category names for iteration
get_all_errorlens_categories() {
  echo "empty_catch swallowed boundary generic resource infoleak"
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}
