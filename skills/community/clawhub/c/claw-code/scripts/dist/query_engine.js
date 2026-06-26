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
import * as crypto from 'crypto';
import { loadSession, saveSession } from './session_store.js';
// ---------------------------------------------------------------------------
// TranscriptStore — mirrors transcript.py
// ---------------------------------------------------------------------------
class TranscriptStore {
    constructor() {
        this._entries = [];
        this._flushed = false;
    }
    get entries() {
        return this._entries;
    }
    get flushed() {
        return this._flushed;
    }
    append(entry) {
        this._entries.push(entry);
        this._flushed = false;
    }
    compact(keepLast = 10) {
        if (this._entries.length > keepLast) {
            this._entries = this._entries.slice(-keepLast);
        }
    }
    replay() {
        return this._entries;
    }
    flush() {
        this._flushed = true;
    }
}
function buildPortManifest(_srcRoot) {
    return {
        srcRoot: _srcRoot ?? 'src',
        totalPythonFiles: 0,
        topLevelModules: [],
    };
}
// ---------------------------------------------------------------------------
// Command & tool backlog stubs — mirrors commands.py / tools.py
// ---------------------------------------------------------------------------
function buildCommandBacklog() {
    return {
        modules: [],
        summaryLines() {
            return [];
        },
    };
}
function buildToolBacklog() {
    return {
        modules: [],
        summaryLines() {
            return [];
        },
    };
}
// ---------------------------------------------------------------------------
// UsageSummary factory (mirrors models.py UsageSummary.add_turn logic)
// ---------------------------------------------------------------------------
function makeUsageSummary(inputTokens = 0, outputTokens = 0) {
    return {
        inputTokens,
        outputTokens,
        addTurn(prompt, output) {
            return makeUsageSummary(inputTokens + prompt.split(/\s+/).filter(Boolean).length, outputTokens + output.split(/\s+/).filter(Boolean).length);
        },
    };
}
const DEFAULT_QUERY_ENGINE_CONFIG = Object.freeze({
    maxTurns: 8,
    maxBudgetTokens: 2000,
    compactAfterTurns: 12,
    structuredOutput: false,
    structuredRetryLimit: 2,
});
// ---------------------------------------------------------------------------
// QueryEnginePort — mirrors @dataclass QueryEnginePort
// ---------------------------------------------------------------------------
class QueryEnginePort {
    constructor(manifest, config = DEFAULT_QUERY_ENGINE_CONFIG, sessionId) {
        this._manifest = manifest;
        this._config = config;
        this._sessionId = sessionId ?? crypto.randomUUID();
        this._mutableMessages = [];
        this._permissionDenials = [];
        this._totalUsage = makeUsageSummary();
        this._transcriptStore = new TranscriptStore();
    }
    get sessionId() {
        return this._sessionId;
    }
    get manifest() {
        return this._manifest;
    }
    get config() {
        return this._config;
    }
    set config(value) {
        this._config = value;
    }
    // -------------------------------------------------------------------------
    // Factory methods
    // -------------------------------------------------------------------------
    static fromWorkspace() {
        return new QueryEnginePort(buildPortManifest());
    }
    static fromSavedSession(sessionId) {
        const stored = loadSession(sessionId);
        const transcript = new TranscriptStore();
        for (const msg of stored.messages) {
            transcript.append(msg);
        }
        transcript.flush();
        const port = new QueryEnginePort(buildPortManifest(), DEFAULT_QUERY_ENGINE_CONFIG, stored.session_id);
        port._mutableMessages = [...stored.messages];
        port._totalUsage = makeUsageSummary(stored.input_tokens, stored.output_tokens);
        port._transcriptStore = transcript;
        return port;
    }
    // -------------------------------------------------------------------------
    // Core submit logic
    // -------------------------------------------------------------------------
    submitMessage(prompt, matchedCommands = [], matchedTools = [], deniedTools = []) {
        if (this._mutableMessages.length >= this._config.maxTurns) {
            const output = `Max turns reached before processing prompt: ${prompt}`;
            return {
                prompt,
                output,
                matchedCommands,
                matchedTools,
                permissionDenials: deniedTools,
                usage: this._totalUsage,
                stopReason: 'max_turns_reached',
            };
        }
        const summaryLines = [
            `Prompt: ${prompt}`,
            `Matched commands: ${matchedCommands.length > 0 ? matchedCommands.join(', ') : 'none'}`,
            `Matched tools: ${matchedTools.length > 0 ? matchedTools.join(', ') : 'none'}`,
            `Permission denials: ${deniedTools.length}`,
        ];
        const output = this._formatOutput(summaryLines);
        const projectedUsage = this._totalUsage.addTurn(prompt, output);
        let stopReason = 'completed';
        if (projectedUsage.inputTokens + projectedUsage.outputTokens >
            this._config.maxBudgetTokens) {
            stopReason = 'max_budget_reached';
        }
        this._mutableMessages.push(prompt);
        this._transcriptStore.append(prompt);
        this._permissionDenials.push(...deniedTools);
        this._totalUsage = projectedUsage;
        this._compactMessagesIfNeeded();
        return {
            prompt,
            output,
            matchedCommands,
            matchedTools,
            permissionDenials: deniedTools,
            usage: this._totalUsage,
            stopReason,
        };
    }
    // -------------------------------------------------------------------------
    // Streaming submit — synchronous Generator<StreamEvent>
    // -------------------------------------------------------------------------
    *streamSubmitMessage(prompt, matchedCommands = [], matchedTools = [], deniedTools = []) {
        yield {
            type: 'message_start',
            sessionId: this._sessionId,
            prompt,
        };
        if (matchedCommands.length > 0) {
            yield { type: 'command_match', commands: matchedCommands };
        }
        if (matchedTools.length > 0) {
            yield { type: 'tool_match', tools: matchedTools };
        }
        if (deniedTools.length > 0) {
            yield {
                type: 'permission_denial',
                denials: deniedTools.map((d) => d.tool_name),
            };
        }
        const result = this.submitMessage(prompt, matchedCommands, matchedTools, deniedTools);
        yield { type: 'message_delta', text: result.output };
        yield {
            type: 'message_stop',
            usage: {
                inputTokens: result.usage.inputTokens,
                outputTokens: result.usage.outputTokens,
            },
            stopReason: result.stopReason,
            transcriptSize: this._transcriptStore.entries.length,
        };
    }
    // -------------------------------------------------------------------------
    // Session persistence
    // -------------------------------------------------------------------------
    persistSession() {
        this.flushTranscript();
        const session = {
            session_id: this._sessionId,
            messages: this._mutableMessages,
            input_tokens: this._totalUsage.inputTokens,
            output_tokens: this._totalUsage.outputTokens,
        };
        return saveSession(session);
    }
    // -------------------------------------------------------------------------
    // Internal helpers
    // -------------------------------------------------------------------------
    _compactMessagesIfNeeded() {
        if (this._mutableMessages.length > this._config.compactAfterTurns) {
            this._mutableMessages = this._mutableMessages.slice(-this._config.compactAfterTurns);
        }
        this._transcriptStore.compact(this._config.compactAfterTurns);
    }
    replayUserMessages() {
        return this._transcriptStore.replay();
    }
    flushTranscript() {
        this._transcriptStore.flush();
    }
    _formatOutput(summaryLines) {
        if (this._config.structuredOutput) {
            const payload = {
                summary: [...summaryLines],
                sessionId: this._sessionId,
            };
            return this._renderStructuredOutput(payload);
        }
        return summaryLines.join('\n');
    }
    _renderStructuredOutput(payload) {
        let lastError = null;
        for (let i = 0; i < this._config.structuredRetryLimit; i++) {
            try {
                return JSON.stringify(payload, null, 2);
            }
            catch (exc) {
                lastError = exc;
                payload = {
                    summary: ['structured output retry'],
                    sessionId: this._sessionId,
                };
            }
        }
        // Defensive: all retries failed — surface the error
        throw new Error('structured output rendering failed');
    }
    // -------------------------------------------------------------------------
    // Summary renderer — mirrors render_summary()
    // -------------------------------------------------------------------------
    renderSummary() {
        const commandBacklog = buildCommandBacklog();
        const toolBacklog = buildToolBacklog();
        const cmdLines = commandBacklog.summaryLines().slice(0, 10);
        const toolLines = toolBacklog.summaryLines().slice(0, 10);
        const sections = [
            '# Python Porting Workspace Summary',
            '',
            this._manifestToMarkdown(),
            '',
            `Command surface: ${commandBacklog.modules.length} mirrored entries`,
            ...(cmdLines.length > 0 ? cmdLines : ['  (no command modules loaded)']),
            '',
            `Tool surface: ${toolBacklog.modules.length} mirrored entries`,
            ...(toolLines.length > 0 ? toolLines : ['  (no tool modules loaded)']),
            '',
            `Session id: ${this._sessionId}`,
            `Conversation turns stored: ${this._mutableMessages.length}`,
            `Permission denials tracked: ${this._permissionDenials.length}`,
            `Usage totals: in=${this._totalUsage.inputTokens} out=${this._totalUsage.outputTokens}`,
            `Max turns: ${this._config.maxTurns}`,
            `Max budget tokens: ${this._config.maxBudgetTokens}`,
            `Transcript flushed: ${this._transcriptStore.flushed}`,
        ];
        return sections.join('\n');
    }
    _manifestToMarkdown() {
        const lines = [
            `Port root: \`${this._manifest.srcRoot}\``,
            `Total Python files: **${this._manifest.totalPythonFiles}**`,
            '',
            'Top-level Python modules:',
        ];
        for (const mod of this._manifest.topLevelModules) {
            lines.push(`- \`${mod.name}\` (${mod.fileCount} files) — ${mod.notes}`);
        }
        return lines.join('\n');
    }
}
// ---------------------------------------------------------------------------
// Public exports
// ---------------------------------------------------------------------------
export { QueryEnginePort, DEFAULT_QUERY_ENGINE_CONFIG, TranscriptStore, buildPortManifest, buildCommandBacklog, buildToolBacklog, };
