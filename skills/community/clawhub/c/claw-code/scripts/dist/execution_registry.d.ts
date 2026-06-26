export declare class MirroredCommand {
    readonly name: string;
    readonly source_hint: string;
    constructor(name: string, source_hint: string);
    execute(prompt: string): string;
}
export declare class MirroredTool {
    readonly name: string;
    readonly source_hint: string;
    constructor(name: string, source_hint: string);
    execute(payload: string): string;
}
export declare class ExecutionRegistry {
    readonly commands: readonly MirroredCommand[];
    readonly tools: readonly MirroredTool[];
    constructor(commands: readonly MirroredCommand[], tools: readonly MirroredTool[]);
    command(name: string): MirroredCommand | undefined;
    tool(name: string): MirroredTool | undefined;
}
export declare function buildExecutionRegistry(): ExecutionRegistry;
