export declare class TranscriptStore {
    entries: readonly string[];
    flushed: boolean;
    constructor(entries?: readonly string[], flushed?: boolean);
    append(_message: string): void;
    compact(_keepLast: number): void;
    replay(): readonly string[];
    flush(): void;
}
