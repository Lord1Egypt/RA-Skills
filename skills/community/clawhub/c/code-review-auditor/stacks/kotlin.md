# Kotlin Review Rules

Use for Kotlin JVM, Android-adjacent Kotlin, Spring Kotlin, Ktor, coroutines, and Gradle Kotlin projects.

## Bugs And Reliability

- Check nullable types, platform types from Java interop, unsafe `!!`, late initialization, and default arguments that hide invalid states.
- Review coroutine scopes, cancellation, structured concurrency, dispatcher choice, blocking calls, and exception propagation.
- Look for mutable shared state, data-class copy misuse, and equality/hashCode surprises.

## Security

- Apply Java/Spring or server framework security rules where relevant.
- Check serialization polymorphism, reflection, file paths, and unsafe script/expression evaluation.
- Verify secrets and sensitive data are not logged through structured logging helpers.

## Architecture

- Prefer domain types and sealed hierarchies for finite states when they simplify validation.
- Avoid overusing extension functions when they hide dependencies or side effects.
- Keep coroutine and framework concerns out of pure domain logic where practical.

## Performance

- Check collection chaining on large inputs, blocking in coroutine contexts, excessive object copying, and unbounded flows.
- Review database and network calls for batching and backpressure.

## Testing

- Use deterministic coroutine tests for time, cancellation, retries, and flow behavior.
- Flag tests that rely on real dispatchers, sleeps, or wall-clock timing.
