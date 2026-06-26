import type { TaskHandler, TaskRecord } from "./types.js";
import { TaskQueue } from "./TaskQueue.js";

export interface SchedulerOptions {
  pollIntervalMs?: number;
  concurrency?: number;
}

export class Scheduler {
  private readonly handlers = new Map<string, TaskHandler>();
  private readonly pollIntervalMs: number;
  private readonly concurrency: number;
  private timer?: NodeJS.Timeout;
  private activeCount = 0;
  private draining = false;

  constructor(private readonly queue: TaskQueue, options: SchedulerOptions = {}) {
    this.pollIntervalMs = options.pollIntervalMs ?? 250;
    this.concurrency = options.concurrency ?? 4;
  }

  register<TPayload, TResult>(taskType: string, handler: TaskHandler<TPayload, TResult>): void {
    this.handlers.set(taskType, handler as TaskHandler);
  }

  start(): void {
    if (this.timer) {
      return;
    }
    this.timer = setInterval(() => {
      void this.tick();
    }, this.pollIntervalMs);
  }

  async stop(): Promise<void> {
    this.draining = true;
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = undefined;
    }
    while (this.activeCount > 0) {
      await new Promise((resolve) => setTimeout(resolve, 10));
    }
  }

  async tick(): Promise<void> {
    if (this.draining) {
      return;
    }
    while (this.activeCount < this.concurrency) {
      const task = await this.queue.claimNextReady();
      if (!task) {
        return;
      }
      this.activeCount += 1;
      void this.execute(task).finally(() => {
        this.activeCount -= 1;
      });
    }
  }

  private async execute(task: TaskRecord): Promise<void> {
    const handler = this.handlers.get(task.type);
    if (!handler) {
      await this.queue.fail(task.id, `No handler registered for task type "${task.type}"`);
      return;
    }
    const controller = new AbortController();
    const timeout = task.timeoutMs
      ? setTimeout(() => controller.abort(new Error(`Task ${task.id} timed out after ${task.timeoutMs}ms`)), task.timeoutMs)
      : undefined;
    try {
      const dependencies = await this.queue.storage.getDependencyResults(task.id);
      const result = await handler(task.payload, {
        attempt: task.attempts,
        signal: controller.signal,
        dependencies,
        log: async (level, message, context) => this.queue.log(task.id, level, message, context)
      });
      await this.queue.complete(task.id, result);
    } catch (error) {
      const reason = error instanceof Error ? error : new Error(String(error));
      await this.queue.fail(task.id, reason);
    } finally {
      if (timeout) {
        clearTimeout(timeout);
      }
    }
  }
}
