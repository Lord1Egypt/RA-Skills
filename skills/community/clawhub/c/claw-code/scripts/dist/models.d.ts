/**
 * Data models for claw-code-ts
 * Mirrored from Python src/models.py
 * Strict mode enabled.
 */
export declare class Subsystem {
    readonly name: string;
    readonly path: string;
    readonly file_count: number;
    readonly notes: string;
    constructor(args: {
        name: string;
        path: string;
        file_count: number;
        notes: string;
    });
}
export declare class PortingModule {
    readonly name: string;
    readonly responsibility: string;
    readonly source_hint: string;
    readonly status: string;
    constructor(args: {
        name: string;
        responsibility: string;
        source_hint: string;
        status?: string;
    });
}
export declare class PermissionDenial {
    readonly tool_name: string;
    readonly reason: string;
    constructor(args: {
        tool_name: string;
        reason: string;
    });
}
export declare class UsageSummary {
    readonly input_tokens: number;
    readonly output_tokens: number;
    constructor(args?: {
        input_tokens?: number;
        output_tokens?: number;
    });
    addTurn(prompt: string, output: string): UsageSummary;
}
export declare class PortingBacklog {
    readonly title: string;
    readonly modules: readonly PortingModule[];
    constructor(args?: {
        title?: string;
        modules?: readonly PortingModule[];
    });
    summaryLines(): string[];
}
