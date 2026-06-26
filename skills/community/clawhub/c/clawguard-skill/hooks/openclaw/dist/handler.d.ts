/**
 * ClawWall Auto-Start Hook
 *
 * Runs on gateway:startup to ensure the ClawWall DLP service is running
 * before any agent tool calls are processed.
 */
export declare function onStartup(): Promise<void>;
