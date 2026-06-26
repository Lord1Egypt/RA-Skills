export interface SecureSession {
    id: string;
    workDir: string;
    screenshotDir: string;
    startTime: number;
    maxDuration: number;
    site?: string;
}
export declare function createSecureSession(site?: string, maxDurationMs?: number): SecureSession;
export declare function getActiveSession(): SecureSession | null;
export declare function isSessionExpired(): boolean;
export declare function getSessionTimeRemaining(): number;
export declare function secureCleanup(): boolean;
export declare function getScreenshotPath(actionIndex: number, action: string): string;
export declare function setupTimeoutWatcher(onTimeout: () => void): void;
