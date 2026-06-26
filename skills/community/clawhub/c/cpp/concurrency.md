# Concurrency Traps

- Data race — concurrent read+write without sync is UB
- `mutex` not RAII — use `lock_guard` or `unique_lock`
- Deadlock — lock order must be consistent, use `scoped_lock`
- `volatile` is not atomic — doesn't prevent races, use `std::atomic`
- False sharing — adjacent atomics on same cache line = slow
- `condition_variable` spurious wake — always use predicate in `wait`
- `thread` must join/detach — destructor calls `terminate` otherwise
- `async` may be deferred — `std::launch::async` to force thread
