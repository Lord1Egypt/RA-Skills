import { PermissionDenial, PortingModule } from './models.js';
import { PortContext } from './context.js';
import { HistoryLog } from './history.js';
import { TurnResult as EngineTurnResult } from './query_engine.js';
import { SetupReport, WorkspaceSetup } from './setup.js';
/**
 * RoutedMatch – produced by the prompt routing step.
 * Mirrors Python's @dataclass(frozen=True) RoutedMatch.
 */
export interface RoutedMatch {
    readonly kind: 'command' | 'tool';
    readonly name: string;
    readonly source_hint: string;
    readonly score: number;
}
/**
 * Runtime session – aggregates all state produced by a single bootstrap.
 * Mirrors Python's @dataclass RuntimeSession.
 */
export declare class RuntimeSession {
    readonly prompt: string;
    readonly context: PortContext;
    readonly setup: WorkspaceSetup;
    readonly setup_report: SetupReport;
    readonly system_init_message: string;
    readonly history: HistoryLog;
    readonly routed_matches: readonly RoutedMatch[];
    readonly turn_result: EngineTurnResult;
    readonly command_execution_messages: readonly string[];
    readonly tool_execution_messages: readonly string[];
    readonly stream_events: readonly Record<string, unknown>[];
    readonly persisted_session_path: string;
    constructor(params: {
        prompt: string;
        context: PortContext;
        setup: WorkspaceSetup;
        setup_report: SetupReport;
        system_init_message: string;
        history: HistoryLog;
        routed_matches: readonly RoutedMatch[];
        turn_result: EngineTurnResult;
        command_execution_messages: readonly string[];
        tool_execution_messages: readonly string[];
        stream_events: readonly Record<string, unknown>[];
        persisted_session_path: string;
    });
    asMarkdown(): string;
}
/**
 * Core runtime – routes prompts, manages sessions and turn loops.
 * Mirrors Python class PortRuntime.
 */
export declare class PortRuntime {
    /**
     * Route a prompt to the best-matching commands and tools.
     * Returns up to `limit` matches sorted by score, with one command
     * and one tool promoted to the front if present.
     */
    route_prompt(prompt: string, limit?: number): RoutedMatch[];
    /** Bootstrap a new runtime session from a prompt. */
    bootstrap_session(prompt: string, limit?: number): RuntimeSession;
    /**
     * Run a multi-turn conversation loop.
     * Returns all TurnResult instances produced across the turns.
     */
    run_turn_loop(prompt: string, limit?: number, max_turns?: number, structured_output?: boolean): EngineTurnResult[];
    /** Infer permission denials for dangerous tools. */
    _inferPermissionDenials(matches: readonly RoutedMatch[]): PermissionDenial[];
    /** Collect matching modules for a given token set and kind. */
    _collectMatches(tokens: ReadonlySet<string>, modules: readonly PortingModule[], kind: string): RoutedMatch[];
    /**
     * Score a module against a token set – returns number of matching tokens.
     * Static method mirrors Python's @staticmethod _score.
     */
    static _score(tokens: ReadonlySet<string>, module: PortingModule): number;
}
