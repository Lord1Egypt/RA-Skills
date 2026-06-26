export interface DeferredInitResult {
    readonly ok: boolean;
    readonly detail: string;
}
export declare function runDeferredInit(_trusted: boolean): DeferredInitResult;
