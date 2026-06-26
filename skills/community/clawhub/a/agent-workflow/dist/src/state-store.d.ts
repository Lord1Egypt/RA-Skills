export type NodeStatus = "pending" | "active" | "completed" | "skipped";
export type WorkflowStatus = "active" | "paused" | "completed" | "abandoned";
export interface ForkState {
    forkId: string;
    plugin: string;
    status: "active" | "completed";
    startedAt: string;
    completedAt?: string;
    joinTarget: string;
    note?: string;
}
export interface ContextStackEntry {
    returnTo: string;
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
    stateVersion: number;
    projectName: string;
    createdAt: string;
    updatedAt: string;
    status: WorkflowStatus;
    nodes: Record<string, NodeStatus>;
    currentNode: string;
    forks: Record<string, ForkState>;
    contextStack: ContextStackEntry[];
    branchChoices: Record<string, string>;
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
export declare class StateStore {
    private storageDir;
    private workflowsDir;
    private indexPath;
    private lockPath;
    constructor(baseDir: string);
    private ensureDirectories;
    private workflowPath;
    private readJson;
    private writeJson;
    private acquireLock;
    private releaseLock;
    createWorkflow(projectName: string, entryNode: string): WorkflowState;
    loadWorkflow(workflowId: string): WorkflowState | null;
    saveWorkflow(state: WorkflowState, expectedVersion: number): WorkflowState;
    listWorkflows(statusFilter?: WorkflowStatus): WorkflowIndexEntry[];
    private updateIndex;
}
//# sourceMappingURL=state-store.d.ts.map