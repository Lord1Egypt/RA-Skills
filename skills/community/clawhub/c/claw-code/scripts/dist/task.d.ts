/**
 * Task data class and task status management.
 * Ported from task.py
 */
export type TaskStatus = "pending" | "in_progress" | "completed" | "blocked";
export interface TaskFields {
    id: string;
    description: string;
    status: TaskStatus;
    createdAt: Date;
    completedAt: Date | null;
}
export declare class PortingTask {
    private readonly _id;
    private readonly _description;
    private _status;
    private readonly _createdAt;
    private _completedAt;
    constructor(id: string, description: string);
    get id(): string;
    get description(): string;
    get status(): TaskStatus;
    get createdAt(): Date;
    get completedAt(): Date | null;
    isPending(): boolean;
    isInProgress(): boolean;
    isCompleted(): boolean;
    isBlocked(): boolean;
    start(): void;
    block(): void;
    complete(): void;
    reset(): void;
    toFields(): TaskFields;
}
