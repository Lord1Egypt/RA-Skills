# agent-task-queue

`agent-task-queue` is an OpenClaw skill project for multi-agent task orchestration. It provides a TypeScript queue runtime with priority ordering, delayed execution, dependency-aware scheduling, retries, timeout handling, logs, and metrics.

## Features

- Priority queue with delayed tasks and dead-letter handling
- Scheduler with polling, concurrency limits, retries, and task timeouts
- Dependency manager with DAG validation, dependency gating, and result propagation
- Storage abstraction with in-memory, SQLite, and Redis implementations
- Execution logs and queue metrics for observability

## Project Structure

```text
.
├── SKILL.md
├── README.md
├── examples/
├── src/
│   ├── DependencyManager.ts
│   ├── Scheduler.ts
│   ├── TaskQueue.ts
│   └── storage/
└── tests/
```

## Install

```bash
npm install
```

## Use

```ts
import { Scheduler, TaskQueue } from "./src/index.js";

const queue = new TaskQueue();
const scheduler = new Scheduler(queue, { concurrency: 2 });

scheduler.register("echo", async (payload) => ({ echoed: payload }));

await queue.enqueue({
  type: "echo",
  payload: { value: "hello" },
  priority: 5,
  retryPolicy: { maxAttempts: 3, backoffMs: 500 }
});

await scheduler.tick();
```

For a fuller example, see [examples/basic.ts](/Users/gaolei/.openclaw/workspace-zhongshu/skills/agent-task-queue/examples/basic.ts).

## Scripts

- `npm run build` compiles the project
- `npm test` runs the test suite
- `npm run check` runs build plus tests

## Storage

- `InMemoryStorage` is the default for tests and local runs
- `SQLiteStorage` persists tasks and logs to a local SQLite database
- `RedisStorage` supports shared queue state for distributed workers

## Notes

- Dependencies must refer to existing tasks and cannot form cycles
- Exhausted retries move tasks to the dead-letter queue
- Timeout handling uses `AbortController`; task handlers should respect `context.signal`
