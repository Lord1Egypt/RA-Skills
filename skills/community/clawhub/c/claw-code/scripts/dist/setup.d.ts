import { DeferredInitResult } from './deferred_init.js';
import { PrefetchResult } from './prefetch.js';
export declare class WorkspaceSetup {
    readonly python_version: string;
    readonly implementation: string;
    readonly platform_name: string;
    readonly test_command: string;
    constructor(args?: {
        python_version?: string;
        implementation?: string;
        platform_name?: string;
        test_command?: string;
    });
    startup_steps(): readonly string[];
}
export interface SetupReport {
    readonly setup: WorkspaceSetup;
    readonly prefetches: readonly PrefetchResult[];
    readonly deferred_init: DeferredInitResult;
    readonly trusted: boolean;
    readonly cwd: string;
}
export declare function runSetup(_cwd?: string, trusted?: boolean): SetupReport;
