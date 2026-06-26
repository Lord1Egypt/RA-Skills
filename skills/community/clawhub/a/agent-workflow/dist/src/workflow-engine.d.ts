import { StateStore } from "./state-store.js";
import { SkillLoader } from "./skill-loader.js";
export type ErrorCode = "NOT_FOUND" | "INVALID_TRANSITION" | "MISSING_DEPENDENCIES" | "BRANCH_REQUIRED" | "FORK_LIMIT_EXCEEDED" | "VERSION_CONFLICT" | "WORKFLOW_ENDED" | "UNKNOWN_NODE";
export interface NextOption {
    node: string;
    label: string;
    condition?: string;
}
export interface ActiveForkSummary {
    forkId: string;
    plugin: string;
    status: string;
    startedAt: string;
}
export interface WorkflowResponse {
    ok: boolean;
    workflowId?: string;
    projectName?: string;
    current?: {
        node: string;
        title: string;
        type: string;
        summary: string;
        needsFullContent: boolean;
    };
    next?: NextOption[];
    activeForks?: ActiveForkSummary[];
    progress?: {
        completed: string[];
        remaining: string[];
        percentDone: number;
    };
    warnings?: string[];
    error?: {
        code: ErrorCode;
        message: string;
        suggestion?: string;
    };
    message: string;
}
export interface WorkflowSummary {
    workflowId: string;
    projectName: string;
    status: string;
    currentNode: string;
    currentNodeTitle: string;
    percentDone: number;
    activeForks: number;
    updatedAt: string;
}
export declare class WorkflowEngine {
    private store;
    private skillLoader;
    private maxForks;
    constructor(store: StateStore, skillLoader: SkillLoader, maxForks?: number);
    start(projectName: string): WorkflowResponse;
    status(workflowId?: string): WorkflowResponse;
    list(statusFilter?: string): WorkflowResponse;
    next(workflowId: string, branch?: string): WorkflowResponse;
    goto(workflowId: string, step: string): WorkflowResponse;
    complete(workflowId: string, note?: string, output?: unknown): WorkflowResponse;
    fork(workflowId: string, plugin: string): WorkflowResponse;
    join(workflowId: string, forkId: string, note?: string): WorkflowResponse;
    getSkill(node: string): WorkflowResponse & {
        skillContent: string;
    };
    abandon(workflowId: string): WorkflowResponse;
    private listSummaries;
    private transitionTo;
    private moveToNode;
    private closeLastOpenEntry;
    private buildResponse;
    private currentNodeInfo;
    private activeForksSummary;
    private notFound;
    private error;
}
//# sourceMappingURL=workflow-engine.d.ts.map