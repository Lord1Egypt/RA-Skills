import type { Page } from 'playwright';
export interface ExtractedContent {
    title: string;
    body: string;
    excerpt: string;
    author?: string;
    date?: string;
    wordCount: number;
}
export declare function extractContent(page: Page): Promise<ExtractedContent>;
export declare function extractWithCustomSelectors(page: Page, selectors: {
    title?: string;
    body?: string;
    author?: string;
    date?: string;
}): Promise<ExtractedContent>;
