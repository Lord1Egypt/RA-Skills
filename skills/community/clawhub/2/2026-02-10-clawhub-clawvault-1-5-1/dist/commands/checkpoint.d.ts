/**
 * Quick checkpoint command - fast state save for context death resilience
 */
interface CheckpointOptions {
    workingOn?: string;
    focus?: string;
    blocked?: string;
    vaultPath: string;
    urgent?: boolean;
}
interface CheckpointData {
    timestamp: string;
    workingOn: string | null;
    focus: string | null;
    blocked: string | null;
    sessionId?: string;
    sessionKey?: string;
    model?: string;
    tokenEstimate?: number;
    sessionStartedAt?: string;
    urgent?: boolean;
}
interface SessionState {
    sessionId?: string;
    sessionKey?: string;
    model?: string;
    tokenEstimate?: number;
    startedAt?: string;
}
declare function flush(): Promise<CheckpointData | null>;
declare function checkpoint(options: CheckpointOptions): Promise<CheckpointData>;
declare function clearDirtyFlag(vaultPath: string): Promise<void>;
declare function cleanExit(vaultPath: string): Promise<void>;
declare function checkDirtyDeath(vaultPath: string): Promise<{
    died: boolean;
    checkpoint: CheckpointData | null;
    deathTime: string | null;
}>;
declare function setSessionState(vaultPath: string, session: string | SessionState): Promise<void>;

export { type CheckpointData, type CheckpointOptions, type SessionState, checkDirtyDeath, checkpoint, cleanExit, clearDirtyFlag, flush, setSessionState };
