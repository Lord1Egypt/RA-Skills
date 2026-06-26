import { createClient, type RedisClientType } from "redis";
import type { QueueStorage, TaskLogEntry, TaskRecord } from "../types.js";

export interface RedisStorageOptions {
  url?: string;
  namespace?: string;
}

export class RedisStorage implements QueueStorage {
  private readonly client: RedisClientType;
  private readonly namespace: string;

  constructor(options: RedisStorageOptions = {}) {
    this.client = createClient({ url: options.url });
    this.namespace = options.namespace ?? "agent-task-queue";
  }

  async connect(): Promise<void> {
    if (!this.client.isOpen) {
      await this.client.connect();
    }
  }

  async disconnect(): Promise<void> {
    if (this.client.isOpen) {
      await this.client.disconnect();
    }
  }

  async saveTask(task: TaskRecord): Promise<void> {
    await this.connect();
    await this.client.hSet(this.key("tasks"), task.id, JSON.stringify(task));
  }

  async getTask(taskId: string): Promise<TaskRecord | undefined> {
    await this.connect();
    const raw = await this.client.hGet(this.key("tasks"), taskId);
    return raw ? (JSON.parse(raw) as TaskRecord) : undefined;
  }

  async updateTask(task: TaskRecord): Promise<void> {
    await this.saveTask(task);
  }

  async listTasks(): Promise<TaskRecord[]> {
    await this.connect();
    const entries = await this.client.hVals(this.key("tasks"));
    return entries.map((entry) => JSON.parse(entry) as TaskRecord);
  }

  async listLogs(taskId?: string): Promise<TaskLogEntry[]> {
    await this.connect();
    const entries = taskId
      ? await this.client.lRange(this.key(`logs:${taskId}`), 0, -1)
      : await this.client.lRange(this.key("logs"), 0, -1);
    return entries.map((entry) => JSON.parse(entry) as TaskLogEntry);
  }

  async appendLog(entry: TaskLogEntry): Promise<void> {
    await this.connect();
    const value = JSON.stringify(entry);
    await this.client.rPush(this.key("logs"), value);
    await this.client.rPush(this.key(`logs:${entry.taskId}`), value);
  }

  async saveDependencyResult(taskId: string, dependencyId: string, value: unknown): Promise<void> {
    await this.connect();
    await this.client.hSet(this.key(`deps:${taskId}`), dependencyId, JSON.stringify(value));
  }

  async getDependencyResults(taskId: string): Promise<Map<string, unknown>> {
    await this.connect();
    const entries = await this.client.hGetAll(this.key(`deps:${taskId}`));
    return new Map(Object.entries(entries).map(([key, value]) => [key, JSON.parse(value)]));
  }

  private key(value: string): string {
    return `${this.namespace}:${value}`;
  }
}
