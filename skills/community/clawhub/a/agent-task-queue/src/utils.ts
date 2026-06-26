import { randomUUID } from "node:crypto";
import type { RetryPolicy, TaskOptions, TaskRecord } from "./types.js";

export const DEFAULT_RETRY_POLICY: RetryPolicy = {
  maxAttempts: 3,
  backoffMs: 1_000,
  backoffMultiplier: 2,
  maxBackoffMs: 60_000
};

export function createTaskRecord<TPayload>(options: TaskOptions<TPayload>): TaskRecord<TPayload> {
  const now = new Date().toISOString();
  const retryPolicy = { ...DEFAULT_RETRY_POLICY, ...options.retryPolicy };
  const status = (options.dependencies?.length ?? 0) > 0 ? "waiting_dependencies" : "queued";
  return {
    id: options.id ?? randomUUID(),
    type: options.type,
    payload: options.payload,
    priority: options.priority ?? 0,
    runAt: (options.runAt ?? new Date()).toISOString(),
    timeoutMs: options.timeoutMs,
    dependencies: [...(options.dependencies ?? [])],
    retryPolicy,
    metadata: options.metadata ?? {},
    status,
    attempts: 0,
    createdAt: now,
    updatedAt: now
  };
}

export function computeRetryAt(task: TaskRecord): Date {
  const base = task.retryPolicy.backoffMs ?? DEFAULT_RETRY_POLICY.backoffMs!;
  const multiplier = task.retryPolicy.backoffMultiplier ?? DEFAULT_RETRY_POLICY.backoffMultiplier!;
  const max = task.retryPolicy.maxBackoffMs ?? DEFAULT_RETRY_POLICY.maxBackoffMs!;
  const exponent = Math.max(task.attempts - 1, 0);
  const delay = Math.min(base * multiplier ** exponent, max);
  return new Date(Date.now() + delay);
}

export function compareReadyTasks(left: TaskRecord, right: TaskRecord): number {
  if (left.priority !== right.priority) {
    return right.priority - left.priority;
  }
  const runAtDelta = new Date(left.runAt).getTime() - new Date(right.runAt).getTime();
  if (runAtDelta !== 0) {
    return runAtDelta;
  }
  return new Date(left.createdAt).getTime() - new Date(right.createdAt).getTime();
}
