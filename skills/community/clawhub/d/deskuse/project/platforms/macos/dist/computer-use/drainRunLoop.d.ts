declare function retain(): void;
declare function release(): void;
export declare const retainPump: typeof retain;
export declare const releasePump: typeof release;
export declare function drainRunLoop<T>(fn: () => Promise<T>): Promise<T>;
export {};
