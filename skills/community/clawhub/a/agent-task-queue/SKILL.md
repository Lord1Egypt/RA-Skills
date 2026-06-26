---
name: agent-task-queue
description: Build and operate a multi-agent task queue in OpenClaw with priority queues, delayed/dead-letter queues, scheduling, retry/timeout control, dependency management, parallel execution, and execution tracking using the bundled TypeScript runtime.
---

# Agent Task Queue

Use this skill when a task needs queue-based orchestration for multiple agents or workers. The bundled runtime is in `src/` and covers:

- Priority queue, delayed queue, and dead-letter queue behavior
- Scheduler polling with concurrency limits, retries, and timeouts
- Dependency validation, dependency gating, and result propagation
- Task logs and aggregate metrics
- Pluggable storage through in-memory, SQLite, or Redis backends

## Workflow

1. Import `TaskQueue` and `Scheduler` from `src/index.ts`.
2. Pick storage:
   - Default `InMemoryStorage` for local execution or tests
   - `SQLiteStorage` for single-node persistence
   - `RedisStorage` for distributed workers
3. Register handlers with `scheduler.register(taskType, handler)`.
4. Enqueue tasks with `priority`, `runAt`, `dependencies`, `retryPolicy`, and `timeoutMs` as needed.
5. Drive execution via `scheduler.tick()` or `scheduler.start()`.
6. Inspect `queue.logs()`, `queue.metrics()`, `queue.getSnapshot()`, and `queue.get(taskId)` for state and traceability.

## Key Files

- `src/TaskQueue.ts`: queue lifecycle, ready/dead-letter snapshots, logs, metrics
- `src/Scheduler.ts`: polling loop, concurrency control, retries, timeout handling
- `src/DependencyManager.ts`: DAG validation and dependency result propagation
- `src/storage/`: storage implementations
- `tests/task-queue.test.ts`: behavior coverage
- `examples/basic.ts`: end-to-end usage

## Implementation Notes

- Dependency tasks must already exist when a dependent task is enqueued.
- A task becomes runnable only after all dependencies are `completed`.
- Completed dependency results are stored and exposed to downstream handlers through `context.dependencies`.
- When retries are exhausted, the task is moved to `dead_letter`.
- Timeout cancellation uses `AbortSignal`; long-running handlers should watch `context.signal`.

## Validation

Run:

```bash
npm run check
```

If Redis or SQLite packages are unavailable in the environment, install dependencies first with `npm install`.
