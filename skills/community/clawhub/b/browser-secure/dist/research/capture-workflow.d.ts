import type { Page } from 'playwright';
import { type Capture } from './scrapbook.js';
export interface CaptureResult {
    capture: Capture;
    screenshotPath: string;
    htmlPath?: string;
}
export interface CaptureOptions {
    saveHtml?: boolean;
    saveFullText?: boolean;
    autoApproved?: boolean;
    referrer?: string;
    discoveryMethod?: string;
}
export declare function capturePage(page: Page, url: string, siteId: string, credentialsUsed: boolean, options?: CaptureOptions): Promise<CaptureResult>;
export declare function getCapturePreview(capture: Capture): string;
