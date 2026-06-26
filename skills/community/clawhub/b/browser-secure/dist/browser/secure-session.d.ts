import { Page } from 'playwright';
import { UnattendedOptions } from '../security/approval.js';
import { ChromeProfile } from './chrome-profiles.js';
interface BrowserOptions {
    site?: string;
    autoVault?: boolean;
    headless?: boolean;
    timeout?: number;
    profile?: ChromeProfile;
    unattended?: UnattendedOptions;
    closeChrome?: boolean;
}
export declare function startBrowser(url: string, options?: BrowserOptions): Promise<void>;
export declare function handleSiteAuthentication(site: string, unattended?: UnattendedOptions): Promise<void>;
export declare function performAction(action: string, options?: {
    autoApprove?: boolean;
    unattended?: UnattendedOptions;
}): Promise<void>;
export declare function extractData(instruction: string, schema?: Record<string, unknown>): Promise<unknown>;
export declare function getPage(): Page | null;
export declare function reconnectToDaemon(): Promise<void>;
export declare function takeScreenshot(action?: string): Promise<string | null>;
export declare function closeBrowser(options?: {
    keepPage?: boolean;
}): Promise<void>;
export declare function getBrowserStatus(): {
    active: boolean;
    sessionId?: string;
    timeRemaining?: number;
    site?: string;
    actionCount: number;
    suspended?: boolean;
    warningShown?: boolean;
    daemon?: {
        profile: string;
        profileId: string;
        pid: number;
        port: number;
        uptime: string;
    };
};
export declare function suspendSession(): void;
export declare function resumeSession(): void;
export {};
