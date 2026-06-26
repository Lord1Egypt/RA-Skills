// src/state-store.ts
// Persistent workflow state using one JSON file per workflow.
// Storage: ~/.openclaw/workspace/agent-workflow/workflows/
// Each workflow gets its own file: {workflowId}.json
// An index file tracks all workflows: index.json

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

// ─── Types ────────────────────────────────────────────────────────────────────

export type NodeStatus = "pending" | "active" | "completed" | "skipped";
export type WorkflowStatus = "active" | "paused" | "completed" | "abandoned";

export interface ForkState {
  forkId: string;
  plugin: string;             // context-plugin node id
  status: "active" | "completed";
  startedAt: string;
  completedAt?: string;
  joinTarget: string;         // main-flow node to return to after join
  note?: string;
}

export interface ContextStackEntry {
  returnTo: string;           // node to return to after utility is done
  enteredAt: string;
}

export interface HistoryEntry {
  node: string;
  enteredAt: string;
  completedAt?: string;
  note?: string;
  output?: unknown;
}

export interface WorkflowState {
  version: 1;
  workflowId: string;
  stateVersion: number;       // optimistic lock: increment on every write
  projectName: string;
  createdAt: string;
  updatedAt: string;
  status: WorkflowStatus;

  // Node state map (replaces currentNode + completedNodes)
  nodes: Record<string, NodeStatus>;

  // Currently active main-flow node id
  currentNode: string;

  // Parallel forks (context-plugins)
  forks: Record<string, ForkState>;

  // Utility node call stack
  contextStack: ContextStackEntry[];

  // Branch choices made at branch points
  branchChoices: Record<string, string>;

  // Full history
  history: HistoryEntry[];
}

export interface WorkflowIndex {
  workflows: WorkflowIndexEntry[];
}

export interface WorkflowIndexEntry {
  workflowId: string;
  projectName: string;
  status: WorkflowStatus;
  currentNode: string;
  createdAt: string;
  updatedAt: string;
}

// ─── Store class ──────────────────────────────────────────────────────────────

export class StateStore {
  private storageDir: string;
  private workflowsDir: string;
  private indexPath: string;
  private lockPath: string;

  constructor(baseDir: string) {
    this.storageDir = path.join(baseDir, "agent-workflow");
    this.workflowsDir = path.join(this.storageDir, "workflows");
    this.indexPath = path.join(this.workflowsDir, "index.json");
    this.lockPath = path.join(this.storageDir, ".lock");
    this.ensureDirectories();
  }

  private ensureDirectories(): void {
    fs.mkdirSync(this.workflowsDir, { recursive: true });
    if (!fs.existsSync(this.indexPath)) {
      this.writeJson(this.indexPath, { workflows: [] } as WorkflowIndex);
    }
  }

  private workflowPath(workflowId: string): string {
    return path.join(this.workflowsDir, `${workflowId}.json`);
  }

  private readJson<T>(filePath: string): T {
    try {
      const raw = fs.readFileSync(filePath, "utf-8");
      return JSON.parse(raw) as T;
    } catch (err) {
      throw new Error(
        `Failed to read or parse JSON at ${filePath}: ${err instanceof Error ? err.message : String(err)}`
      );
    }
  }

  private writeJson(filePath: string, data: unknown): void {
    // Use UUID for tmp name to avoid conflicts when same process writes concurrently
    const tmp = `${filePath}.tmp.${crypto.randomUUID()}`;
    fs.writeFileSync(tmp, JSON.stringify(data, null, 2), "utf-8");
    fs.renameSync(tmp, filePath);  // atomic replace on same filesystem
  }

  // Acquire a file lock with non-blocking retries (avoids busy-wait blocking event loop).
  // Uses a lock file with PID + timestamp to detect stale locks.
  private acquireLock(timeoutMs = 3000): void {
    const lockContent = `${process.pid}:${Date.now()}`;
    const staleThresholdMs = 5000; // locks older than 5s are considered stale
    const retryIntervalMs = 50;
    const start = Date.now();

    while (true) {
      try {
        fs.writeFileSync(this.lockPath, lockContent, { flag: "wx" });
        return; // acquired
      } catch {
        // Lock exists — check if stale
        try {
          const existing = fs.readFileSync(this.lockPath, "utf-8");
          const parts = existing.split(":");
          const lockTime = parts.length === 2 ? Number(parts[1]) : 0;
          if (Date.now() - lockTime > staleThresholdMs) {
            // Stale lock: remove it and retry immediately
            fs.unlinkSync(this.lockPath);
            continue;
          }
        } catch {
          // Lock file disappeared between check and read — retry
          continue;
        }

        if (Date.now() - start > timeoutMs) {
          throw new Error(
            `Could not acquire workflow lock after ${timeoutMs}ms. ` +
            `Another process may be holding it. Delete ${this.lockPath} if stuck.`
          );
        }

        // Yield to event loop instead of busy-waiting
        // In sync context this is the best we can do without going fully async
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, retryIntervalMs);
      }
    }
  }

  private releaseLock(): void {
    try { fs.unlinkSync(this.lockPath); } catch { /* ignore */ }
  }

  // ── Public API ──────────────────────────────────────────────────────────────

  createWorkflow(projectName: string, entryNode: string): WorkflowState {
    const workflowId = crypto.randomUUID();
    const now = new Date().toISOString();
    const state: WorkflowState = {
      version: 1,
      workflowId,
      stateVersion: 1,
      projectName,
      createdAt: now,
      updatedAt: now,
      status: "active",
      nodes: { [entryNode]: "active" },
      currentNode: entryNode,
      forks: {},
      contextStack: [],
      branchChoices: {},
      history: [{ node: entryNode, enteredAt: now }],
    };

    this.acquireLock();
    try {
      this.writeJson(this.workflowPath(workflowId), state);
      this.updateIndex(state);
    } finally {
      this.releaseLock();
    }

    return state;
  }

  loadWorkflow(workflowId: string): WorkflowState | null {
    const p = this.workflowPath(workflowId);
    if (!fs.existsSync(p)) return null;
    return this.readJson<WorkflowState>(p);
  }

  saveWorkflow(state: WorkflowState, expectedVersion: number): WorkflowState {
    this.acquireLock();
    try {
      const current = this.loadWorkflow(state.workflowId);
      if (current && current.stateVersion !== expectedVersion) {
        throw new Error(
          `Version conflict: expected ${expectedVersion}, found ${current.stateVersion}. ` +
          `Re-load the workflow and retry.`
        );
      }
      const updated: WorkflowState = {
        ...state,
        stateVersion: expectedVersion + 1,
        updatedAt: new Date().toISOString(),
      };
      this.writeJson(this.workflowPath(state.workflowId), updated);
      this.updateIndex(updated);
      return updated;
    } finally {
      this.releaseLock();
    }
  }

  listWorkflows(statusFilter?: WorkflowStatus): WorkflowIndexEntry[] {
    if (!fs.existsSync(this.indexPath)) return [];
    const index = this.readJson<WorkflowIndex>(this.indexPath);
    if (!statusFilter) return index.workflows;
    return index.workflows.filter(w => w.status === statusFilter);
  }

  private updateIndex(state: WorkflowState): void {
    const index: WorkflowIndex = fs.existsSync(this.indexPath)
      ? this.readJson<WorkflowIndex>(this.indexPath)
      : { workflows: [] };

    const entry: WorkflowIndexEntry = {
      workflowId: state.workflowId,
      projectName: state.projectName,
      status: state.status,
      currentNode: state.currentNode,
      createdAt: state.createdAt,
      updatedAt: state.updatedAt,
    };

    const idx = index.workflows.findIndex(w => w.workflowId === state.workflowId);
    if (idx >= 0) {
      index.workflows[idx] = entry;
    } else {
      index.workflows.push(entry);
    }

    this.writeJson(this.indexPath, index);
  }
}
