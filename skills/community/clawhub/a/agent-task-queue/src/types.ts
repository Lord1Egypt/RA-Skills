export type TaskStatus =
  | "pending"
  | "queued"
  | "waiting_dependencies"
  | "running"
  | "retry_scheduled"
  | "completed"
  | "failed"
  | "dead_letter"
  | "cancelled";

export interface RetryPolicy {
  maxAttempts: number;
  backoffMs?: number;
  backoffMultiplier?: number;
  maxBackoffMs?: number;
}

export interface TaskOptions<TPayload = unknown> {
  id?: string;
  type: string;
  payload: TPayload;
  priority?: number;
  runAt?: Date;
  timeoutMs?: number;
  dependencies?: string[];
  retryPolicy?: Partial<RetryPolicy>;
  metadata?: Record<string, unknown>;
}

export interface TaskRecord<TPayload = unknown, TResult = unknown> {
  id: string;
  type: string;
  payload: TPayload;
  priority: number;
  runAt: string;
  timeoutMs?: number;
  dependencies: string[];
  retryPolicy: RetryPolicy;
  metadata: Record<string, unknown>;
  status: TaskStatus;
  attempts: number;
  createdAt: string;
  updatedAt: string;
  startedAt?: string;
  completedAt?: string;
  lastError?: string;
  result?: TResult;
}

export interface TaskLogEntry {
  taskId: string;
  level: "info" | "warn" | "error";
  message: string;
  timestamp: string;
  context?: Record<string, unknown>;
}

export interface TaskMetrics {
  queued: number;
  running: number;
  waitingDependencies: number;
  retryScheduled: number;
  completed: number;
  failed: number;
  deadLetter: number;
  avgDurationMs: number;
}

export interface TaskExecutionContext<TResult = unknown> {
  attempt: number;
  signal: AbortSignal;
  dependencies: Map<string, TResult>;
  log: (level: TaskLogEntry["level"], message: string, context?: Record<string, unknown>) => Promise<void>;
}

export type TaskHandler<TPayload = unknown, TResult = unknown> = (
  payload: TPayload,
  context: TaskExecutionContext<TResult>
) => Promise<TResult>;

export interface QueueStorage {
  saveTask(task: TaskRecord): Promise<void>;
  getTask(taskId: string): Promise<TaskRecord | undefined>;
  updateTask(task: TaskRecord): Promise<void>;
  listTasks(): Promise<TaskRecord[]>;
  listLogs(taskId?: string): Promise<TaskLogEntry[]>;
  appendLog(entry: TaskLogEntry): Promise<void>;
  saveDependencyResult(taskId: string, dependencyId: string, value: unknown): Promise<void>;
  getDependencyResults(taskId: string): Promise<Map<string, unknown>>;
}

export interface QueueSnapshot {
  ready: TaskRecord[];
  delayed: TaskRecord[];
  deadLetter: TaskRecord[];
}
