import type { ComputerExecutor } from '../vendor/computer-use-mcp/executor.js';
export declare function createCliExecutor(_opts: {
    getMouseAnimationEnabled: () => boolean;
    getHideBeforeActionEnabled: () => boolean;
}): ComputerExecutor;
export declare function unhideComputerUseApps(_bundleIds: readonly string[]): Promise<void>;
