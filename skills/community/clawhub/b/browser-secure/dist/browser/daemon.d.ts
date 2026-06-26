export interface DaemonState {
    version: 1;
    pid: number;
    port: number;
    wsUrl: string;
    profile: string;
    profileId: string;
    profilePath: string;
    startedAt: string;
    browserPath: string;
}
export declare function getDaemonStatePath(): string;
export declare function loadDaemonState(): DaemonState | null;
export declare function clearDaemonState(): void;
export declare function isDaemonRunning(state?: DaemonState | null): boolean;
export interface StartDaemonOptions {
    profileId?: string;
    closeChrome?: boolean;
    isUnattended?: boolean;
}
export declare function startDaemon(optsOrProfile?: string | StartDaemonOptions): Promise<{
    state: DaemonState;
}>;
export declare function stopDaemon(): Promise<void>;
export declare function getDaemonStatus(): DaemonState | null;
export declare function printDaemonStatus(): void;
