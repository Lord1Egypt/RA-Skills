import type { FetchResult } from './types/fetch.types.js';
export declare const fetchWeb: (url: string) => Promise<FetchResult>;
export declare const extractHtml: (html: string) => FetchResult;
