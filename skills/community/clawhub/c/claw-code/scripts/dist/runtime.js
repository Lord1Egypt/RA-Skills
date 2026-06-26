// Runtime – PortRuntime core orchestration
// Mirrored from Python src/runtime.py
import { PermissionDenial } from './models.js';
import { PORTED_COMMANDS } from './commands.js';
import { PORTED_TOOLS } from './tools.js';
import { buildPortContext, renderContext } from './context.js';
import { HistoryLog } from './history.js';
import { QueryEnginePort, } from './query_engine.js';
import { runSetup } from './setup.js';
import { buildSystemInitMessage } from './system_init.js';
import { buildExecutionRegistry } from './execution_registry.js';
/**
 * Runtime session – aggregates all state produced by a single bootstrap.
 * Mirrors Python's @dataclass RuntimeSession.
 */
export class RuntimeSession {
    constructor(params) {
        this.prompt = params.prompt;
        this.context = params.context;
        this.setup = params.setup;
        this.setup_report = params.setup_report;
        this.system_init_message = params.system_init_message;
        this.history = params.history;
        this.routed_matches = params.routed_matches;
        this.turn_result = params.turn_result;
        this.command_execution_messages = params.command_execution_messages;
        this.tool_execution_messages = params.tool_execution_messages;
        this.stream_events = params.stream_events;
        this.persisted_session_path = params.persisted_session_path;
    }
    asMarkdown() {
        const lines = [
            '# Runtime Session',
            '',
            `Prompt: ${this.prompt}`,
            '',
            '## Context',
            renderContext(this.context),
            '',
            '## Setup',
            `- Python: ${this.setup.python_version} (${this.setup.implementation})`,
            `- Platform: ${this.setup.platform_name}`,
            `- Test command: ${this.setup.test_command}`,
            '',
            '## Startup Steps',
            ...this.setup.startup_steps().map((step) => `- ${step}`),
            '',
            '## System Init',
            this.system_init_message,
            '',
            '## Routed Matches',
        ];
        if (this.routed_matches.length > 0) {
            for (const match of this.routed_matches) {
                lines.push(`- [${match.kind}] ${match.name} (${match.score}) — ${match.source_hint}`);
            }
        }
        else {
            lines.push('- none');
        }
        lines.push('', '## Command Execution', ...(this.command_execution_messages.length > 0
            ? [...this.command_execution_messages]
            : ['none']), '', '## Tool Execution', ...(this.tool_execution_messages.length > 0
            ? [...this.tool_execution_messages]
            : ['none']), '', '## Stream Events', ...this.stream_events.map((event) => `- ${event['type']}: ${JSON.stringify(event)}`), '', '## Turn Result', this.turn_result.output, '', `Persisted session path: ${this.persisted_session_path}`, '', this.history.asMarkdown());
        return lines.join('\n');
    }
}
/**
 * Core runtime – routes prompts, manages sessions and turn loops.
 * Mirrors Python class PortRuntime.
 */
export class PortRuntime {
    /**
     * Route a prompt to the best-matching commands and tools.
     * Returns up to `limit` matches sorted by score, with one command
     * and one tool promoted to the front if present.
     */
    route_prompt(prompt, limit = 5) {
        const tokens = new Set(prompt
            .replace('/', ' ')
            .replace('-', ' ')
            .split(/\s+/)
            .filter((t) => t.length > 0)
            .map((t) => t.toLowerCase()));
        const byKind = {
            command: this._collectMatches(tokens, PORTED_COMMANDS, 'command'),
            tool: this._collectMatches(tokens, PORTED_TOOLS, 'tool'),
        };
        const selected = [];
        for (const kind of ['command', 'tool']) {
            const matches = byKind[kind];
            if (matches.length > 0) {
                const first = matches[0];
                if (first !== undefined)
                    selected.push(first);
            }
        }
        const leftovers = [
            ...(byKind['command'] ?? []),
            ...(byKind['tool'] ?? []),
        ]
            .filter((m) => !selected.includes(m))
            .sort((a, b) => {
            if (b.score !== a.score)
                return b.score - a.score;
            if (a.kind !== b.kind)
                return a.kind.localeCompare(b.kind);
            return a.name.localeCompare(b.name);
        });
        const remaining = limit - selected.length;
        if (remaining > 0) {
            selected.push(...leftovers.slice(0, remaining));
        }
        return selected;
    }
    /** Bootstrap a new runtime session from a prompt. */
    bootstrap_session(prompt, limit = 5) {
        const context = buildPortContext();
        const setupReport = runSetup(undefined, true);
        const setup = setupReport.setup;
        const history = new HistoryLog();
        history.add('context', `python_file_count=${context.python_file_count}, archive_available=${context.archive_available}`);
        history.add('registry', `commands=${PORTED_COMMANDS.length}, tools=${PORTED_TOOLS.length}`);
        const matches = this.route_prompt(prompt, limit);
        const registry = buildExecutionRegistry();
        const commandExecs = [];
        for (const match of matches) {
            if (match.kind === 'command') {
                const cmd = registry.command(match.name);
                if (cmd !== undefined)
                    commandExecs.push(cmd.execute(prompt));
            }
        }
        const toolExecs = [];
        for (const match of matches) {
            if (match.kind === 'tool') {
                const tool = registry.tool(match.name);
                if (tool !== undefined)
                    toolExecs.push(tool.execute(prompt));
            }
        }
        const denials = this._inferPermissionDenials(matches);
        const engine = QueryEnginePort.fromWorkspace();
        const matchedCommandNames = matches
            .filter((m) => m.kind === 'command')
            .map((m) => m.name);
        const matchedToolNames = matches
            .filter((m) => m.kind === 'tool')
            .map((m) => m.name);
        const streamEvents = [
            ...engine.streamSubmitMessage(prompt, matchedCommandNames, matchedToolNames, denials),
        ];
        const turnResult = engine.submitMessage(prompt, matchedCommandNames, matchedToolNames, denials);
        const persistedSessionPath = engine.persistSession();
        history.add('routing', `matches=${matches.length} for prompt=${JSON.stringify(prompt)}`);
        history.add('execution', `command_execs=${commandExecs.length} tool_execs=${toolExecs.length}`);
        history.add('turn', `commands=${turnResult.matchedCommands.length} tools=${turnResult.matchedTools.length} denials=${turnResult.permissionDenials.length} stop=${turnResult.stopReason}`);
        history.add('session_store', persistedSessionPath);
        return new RuntimeSession({
            prompt,
            context,
            setup,
            setup_report: setupReport,
            system_init_message: buildSystemInitMessage(true),
            history,
            routed_matches: matches,
            turn_result: turnResult,
            command_execution_messages: commandExecs,
            tool_execution_messages: toolExecs,
            stream_events: streamEvents,
            persisted_session_path: persistedSessionPath,
        });
    }
    /**
     * Run a multi-turn conversation loop.
     * Returns all TurnResult instances produced across the turns.
     */
    run_turn_loop(prompt, limit = 5, max_turns = 3, structured_output = false) {
        const engine = QueryEnginePort.fromWorkspace();
        engine.config = {
            ...engine.config,
            maxTurns: max_turns,
            structuredOutput: structured_output,
        };
        const matches = this.route_prompt(prompt, limit);
        const commandNames = matches
            .filter((m) => m.kind === 'command')
            .map((m) => m.name);
        const toolNames = matches
            .filter((m) => m.kind === 'tool')
            .map((m) => m.name);
        const results = [];
        for (let turn = 0; turn < max_turns; turn++) {
            const turnPrompt = turn === 0 ? prompt : `${prompt} [turn ${turn + 1}]`;
            const result = engine.submitMessage(turnPrompt, commandNames, toolNames, []);
            results.push(result);
            if (result.stopReason !== 'completed') {
                break;
            }
        }
        return results;
    }
    /** Infer permission denials for dangerous tools. */
    _inferPermissionDenials(matches) {
        const denials = [];
        for (const match of matches) {
            if (match.kind === 'tool' && match.name.toLowerCase().includes('bash')) {
                denials.push(new PermissionDenial({
                    tool_name: match.name,
                    reason: 'destructive shell execution remains gated in the Python port',
                }));
            }
        }
        return denials;
    }
    /** Collect matching modules for a given token set and kind. */
    _collectMatches(tokens, modules, kind) {
        const matches = [];
        for (const module of modules) {
            const score = PortRuntime._score(tokens, module);
            if (score > 0) {
                matches.push({
                    kind: kind,
                    name: module.name,
                    source_hint: module.source_hint,
                    score,
                });
            }
        }
        matches.sort((a, b) => {
            if (b.score !== a.score)
                return b.score - a.score;
            return a.name.localeCompare(b.name);
        });
        return matches;
    }
    /**
     * Score a module against a token set – returns number of matching tokens.
     * Static method mirrors Python's @staticmethod _score.
     */
    static _score(tokens, module) {
        const haystacks = [
            module.name.toLowerCase(),
            module.source_hint.toLowerCase(),
            module.responsibility.toLowerCase(),
        ];
        let score = 0;
        for (const token of tokens) {
            if (haystacks.some((haystack) => haystack.includes(token))) {
                score++;
            }
        }
        return score;
    }
}
