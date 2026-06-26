/**
 * Query Engine — TypeScript port of query_engine.py
 *
 * Porting notes:
 * - Python `uuid4().hex`  →  `crypto.randomUUID()` (Node 14.17+)
 * - Python `@dataclass(frozen=True)`  →  `Readonly<T>` / immutable class
 * - Python `tuple[T, ...]`  →  `readonly T[]`
 * - Python generator `yield`  →  `Generator<T, void, unknown>`
 * - Token estimation: `prompt.split(/\s+/).filter(Boolean).length`
 *
 * Strict mode: enabled (tsconfig.json strict:true)
 */
import type { PermissionDenial } from './models.js';
/** Mirrors models.py Subsystem */
interface Subsystem {
    readonly name: string;
    readonly path: string;
    readonly fileCount: number;
    readonly notes: string;
}
/** Mirrors models.py UsageSummary */
interface UsageSummary {
    readonly inputTokens: number;
    readonly outputTokens: number;
    addTurn(prompt: string, output: string): UsageSummary;
}
/** Minimal PortingBacklog duck-type (summaryLines method only) */
interface PortingBacklog {
    readonly modules: readonly {
        name: string;
        sourceHint: string;
    }[];
    summaryLines(): string[];
}
declare class TranscriptStore {
    private _entries;
    private _flushed;
    get entries(): readonly string[];
    get flushed(): boolean;
    append(entry: string): void;
    compact(keepLast?: number): void;
    replay(): readonly string[];
    flush(): void;
}
interface PortManifest {
    readonly srcRoot: string;
    readonly totalPythonFiles: number;
    readonly topLevelModules: readonly Subsystem[];
}
declare function buildPortManifest(_srcRoot?: string): PortManifest;
declare function buildCommandBacklog(): PortingBacklog;
declare function buildToolBacklog(): PortingBacklog;
interface QueryEngineConfig {
    readonly maxTurns: number;
    readonly maxBudgetTokens: number;
    readonly compactAfterTurns: number;
    readonly structuredOutput: boolean;
    readonly structuredRetryLimit: number;
}
declare const DEFAULT_QUERY_ENGINE_CONFIG: QueryEngineConfig;
interface TurnResult {
    readonly prompt: string;
    readonly output: string;
    readonly matchedCommands: readonly string[];
    readonly matchedTools: readonly string[];
    readonly permissionDenials: readonly PermissionDenial[];
    readonly usage: UsageSummary;
    readonly stopReason: string;
}
type StreamEvent = {
    readonly type: 'message_start';
    readonly sessionId: string;
    readonly prompt: string;
} | {
    readonly type: 'command_match';
    readonly commands: readonly string[];
} | {
    readonly type: 'tool_match';
    readonly tools: readonly string[];
} | {
    readonly type: 'permission_denial';
    readonly denials: readonly string[];
} | {
    readonly type: 'message_delta';
    readonly text: string;
} | {
    readonly type: 'message_stop';
    readonly usage: {
        readonly inputTokens: number;
        readonly outputTokens: number;
    };
    readonly stopReason: string;
    readonly transcriptSize: number;
};
declare class QueryEnginePort {
    private readonly _manifest;
    private _config;
    private readonly _sessionId;
    private _mutableMessages;
    private _permissionDenials;
    private _totalUsage;
    private _transcriptStore;
    constructor(manifest: PortManifest, config?: QueryEngineConfig, sessionId?: string);
    get sessionId(): string;
    get manifest(): PortManifest;
    get config(): QueryEngineConfig;
    set config(value: QueryEngineConfig);
    static fromWorkspace(): QueryEnginePort;
    static fromSavedSession(sessionId: string): QueryEnginePort;
    submitMessage(prompt: string, matchedCommands?: readonly string[], matchedTools?: readonly string[], deniedTools?: readonly PermissionDenial[]): TurnResult;
    streamSubmitMessage(prompt: string, matchedCommands?: readonly string[], matchedTools?: readonly string[], deniedTools?: readonly PermissionDenial[]): Generator<StreamEvent, void, unknown>;
    persistSession(): string;
    private _compactMessagesIfNeeded;
    replayUserMessages(): readonly string[];
    flushTranscript(): void;
    private _formatOutput;
    private _renderStructuredOutput;
    renderSummary(): string;
    private _manifestToMarkdown;
}
export { QueryEnginePort, type QueryEngineConfig, DEFAULT_QUERY_ENGINE_CONFIG, type TurnResult, type StreamEvent, TranscriptStore, buildPortManifest, type PortManifest, buildCommandBacklog, buildToolBacklog, type Subsystem, type UsageSummary, type PortingBacklog, };
