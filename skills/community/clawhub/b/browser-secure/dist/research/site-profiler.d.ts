import type { Page } from 'playwright';
import type { SiteProfile, SitePlaybook } from './scrapbook.js';
export interface SiteAnalysis {
    url: string;
    hasLoginForm: boolean;
    loginUrl?: string;
    hasSearch: boolean;
    searchSelector?: string;
    navigation: Array<{
        name: string;
        url: string;
    }>;
    contentLinks: string[];
    suggestedSelectors: {
        title?: string;
        body?: string;
        author?: string;
        date?: string;
    };
    screenshots: string[];
    sampleExcerpt?: string;
}
export declare function analyzeSite(page: Page, url: string): Promise<SiteAnalysis>;
export declare function generateSiteId(url: string): string;
export declare function buildPlaybook(analysis: SiteAnalysis, loginRequired: boolean): SitePlaybook;
export declare function buildSiteProfile(url: string, analysis: SiteAnalysis, loginRequired: boolean, sampleExcerpt?: string): SiteProfile;
