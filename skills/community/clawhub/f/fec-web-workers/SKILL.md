---
name: fec-web-workers
description: Use when moving expensive browser work off the main thread with Web Workers, SharedWorker, worker pools, Comlink, transferable objects, Vite/Webpack worker integration, or UI responsiveness fixes. Do not use for lightweight synchronous work or DOM manipulation; Chinese triggers include Web Worker, background thread, main thread blocking.
---

# Web Workers

## Purpose

Move expensive calculations off the main thread and keep input, scrolling, and animations responsive.

## Procedure

1. Confirm the bottleneck first: consider workers only if the task exceeds about 10ms, user input delay is obvious, FPS drops, or large file parsing/image processing/encryption calculation.
2. Choose a communication model: use `postMessage` for simple tasks, use Comlink for functional RPC, use Worker pool for a large number of parallel small tasks, and use SharedWorker for cross-Tab synchronization.
3. Design the message protocol: request/response types, error types, cancellation or timeout strategies must be clear.
4. Prioritize Transferable Objects when transferring large objects; don’t let structured cloning swallow up the benefits brought by Worker.
5. `terminate()` when a component or page is unloaded and verify main thread improvements through Profiler, Performance panel or FPS metrics.

## Detailed reference

- Load [references/basic-worker.md](references/basic-worker.md) when you need native Worker files, build tool imports, React lifecycle encapsulation and cleanup examples.
- Load [references/advanced-workers.md](references/advanced-workers.md) when Transferable Objects, Comlink, Worker pool, SharedWorker, CSP and SharedArrayBuffer considerations are required.

## Constraints

- Cannot access DOM, `window`, `document`, `alert()` or synchronize `localStorage` within Worker.
- High frequency communication may be slower than main thread calculations; measure first then split.
- Worker files must be loaded from the same source and are subject to `worker-src` CSP restrictions.
- Large binary data is transferred first, and the original reference will become invalid after the transfer.
- Each Worker has an independent JS heap and must actively manage life cycle and memory.

## Expected Output

Computationally intensive operations are performed on a background thread, main thread input and scrolling resume smoothly, error and cancellation paths are clear, and workers are terminated on unloading without memory leaks.
