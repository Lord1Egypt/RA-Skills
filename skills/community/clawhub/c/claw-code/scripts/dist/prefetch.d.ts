export interface PrefetchResult {
    readonly name: string;
    readonly detail: string;
}
export declare function startMdmRawRead(): PrefetchResult;
export declare function startKeychainPrefetch(): PrefetchResult;
export declare function startProjectScan(_root: string): PrefetchResult;
