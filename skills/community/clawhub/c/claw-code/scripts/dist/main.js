/**
 * CLI entry point – TypeScript port of main.py
 *
 * All commands output via console.log; process.argv is parsed with simple if/else.
 * Strict mode: enabled (tsconfig.json strict:true)
 */
import { assembleToolPool } from './tool_pool.js';
import { buildBootstrapGraph } from './bootstrap_graph.js';
import { buildCommandGraph } from './command_graph.js';
import { executeCommand, getCommand, getCommands, renderCommandIndex, } from './commands.js';
import { runDirectConnect, runDeepLink } from './direct_modes.js';
import { parityAuditAsMarkdown, runParityAudit } from './parity_audit.js';
import { buildPortManifest } from './port_manifest.js';
import { QueryEnginePort } from './query_engine.js';
import { runRemoteMode, runSshMode, runTeleportMode, } from './remote_runtime.js';
import { PortRuntime } from './runtime.js';
import { loadSession } from './session_store.js';
import { runSetup } from './setup.js';
import { executeTool, getTool, getTools, renderToolIndex, } from './tools.js';
import { ToolPermissionContext } from './permissions.js';
// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
/** Render a SetupReport as Markdown (mirrors Python SetupReport.as_markdown()). */
function setupReportAsMarkdown(report) {
    const lines = [
        '# Setup Report',
        '',
        `- Python: ${report.setup.python_version} (${report.setup.implementation})`,
        `- Platform: ${report.setup.platform_name}`,
        `- Trusted mode: ${report.trusted}`,
        `- CWD: ${report.cwd}`,
        '',
        'Prefetches:',
        ...report.prefetches.map((p) => `- ${p.name}: ${p.detail}`),
        '',
        'Deferred init:',
        `- ok=${report.deferred_init.ok} — ${report.deferred_init.detail}`,
    ];
    return lines.join('\n');
}
/** Render a PortManifest as Markdown. */
function manifestAsMarkdown(manifest) {
    const lines = [
        '# Port Manifest',
        '',
        `Port root: \`${manifest.src_root}\``,
        `Total Python files: **${manifest.total_python_files}**`,
        '',
        'Top-level modules:',
    ];
    for (const mod of manifest.top_level_modules) {
        lines.push(`- \`${mod.name}\` (${mod.file_count} files) — ${mod.notes}`);
    }
    return lines.join('\n');
}
/** Render a command module as a text block. */
function showModule(module) {
    return [module.name, module.source_hint, module.responsibility].join('\n');
}
function getArgStr(args, key, fallback) {
    const val = args[key];
    return typeof val === 'string' ? val : fallback;
}
function getArgNum(args, key, fallback) {
    const val = args[key];
    return typeof val === 'number' ? val : fallback;
}
function getArgBool(args, key) {
    const val = args[key];
    return val === true;
}
function getArgList(args, key) {
    const val = args[key];
    return Array.isArray(val) ? val : [];
}
/**
 * Parse process.argv into a {command, args} structure using simple if/else.
 */
function parseArgs(argv) {
    // argv[0] = node, argv[1] = script name, argv[2+] = command + args
    const raw = argv.slice(2);
    if (raw.length === 0) {
        return { command: '__help__', args: {} };
    }
    const cmd = raw[0];
    const args = {};
    let i = 1;
    while (i < raw.length) {
        const token = raw[i];
        if (!token.startsWith('--')) {
            // positional arg — consume until next flag
            // For commands that take positional args (prompt, name, target, etc.)
            // we track them by position
            i++;
            continue;
        }
        const key = token.replace(/^--/, '');
        // Handle --no-X boolean flags (sets to false)
        if (key.startsWith('no-')) {
            args[key.substring(3)] = false;
            i++;
            continue;
        }
        // Handle --deny-tool X and --deny-prefix Y (accumulate)
        if (key === 'deny-tool' || key === 'deny-prefix') {
            const existing = args[key];
            if (Array.isArray(existing)) {
                existing.push(raw[i + 1] ?? '');
            }
            else {
                args[key] = [raw[i + 1] ?? ''];
            }
            i += 2;
            continue;
        }
        // Boolean flag (--simple-mode, --structured-output, etc.)
        if (i + 1 >= raw.length || raw[i + 1].startsWith('--')) {
            args[key] = true;
            i++;
            continue;
        }
        // Key=value
        const next = raw[i + 1];
        if (next.startsWith('--')) {
            args[key] = true;
            i++;
            continue;
        }
        const numVal = Number(next);
        args[key] = isNaN(numVal) ? next : numVal;
        i += 2;
    }
    return { command: cmd, args };
}
/**
 * Extract positional arguments in order based on the command.
 */
function getPositionalAt(raw, index) {
    // Count non-flag tokens to find the nth positional
    const positionals = [];
    for (let j = 2; j < raw.length; j++) {
        const tok = raw[j];
        if (!tok.startsWith('--')) {
            positionals.push(tok);
        }
        else if (tok.startsWith('--no-') || tok === '--simple-mode' || tok === '--structured-output') {
            // boolean flags that consume no value are skipped
        }
        else if (tok === '--deny-tool' || tok === '--deny-prefix') {
            j++; // skip the value
        }
        else {
            // flags with values
            j++;
        }
    }
    return positionals[index] ?? '';
}
// Simpler approach: for each command, extract positional args directly from raw argv
function extractPositional(raw, indices) {
    const positionals = [];
    let collected = 0;
    for (let j = 2; j < raw.length; j++) {
        const tok = raw[j];
        if (tok.startsWith('--')) {
            // skip flag name
            if (tok.startsWith('--no-') ||
                tok === '--simple-mode' ||
                tok === '--structured-output') {
                // boolean, no value
            }
            else if (tok === '--deny-tool' || tok === '--deny-prefix') {
                j++; // skip value
            }
            else {
                // assume it has a value
                j++;
            }
        }
        else {
            if (collected < indices.length) {
                positionals[collected] = tok;
                collected++;
            }
        }
    }
    // Fill missing with empty string
    while (positionals.length < indices.length) {
        positionals.push('');
    }
    return positionals;
}
// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
export function main(argv = process.argv) {
    const raw = [...argv];
    // If no command, show help
    if (raw.length <= 2) {
        printHelp();
        return 0;
    }
    const cmd = raw[2];
    // ----------------------------------------------------------------
    // No-arg commands
    // ----------------------------------------------------------------
    if (cmd === 'summary') {
        const manifest = buildPortManifest();
        const engine = new QueryEnginePort({
            srcRoot: manifest.src_root,
            totalPythonFiles: manifest.total_python_files,
            topLevelModules: manifest.top_level_modules.map((m) => ({ name: m.name, path: '', fileCount: m.file_count, notes: m.notes })),
        });
        console.log(engine.renderSummary());
        return 0;
    }
    if (cmd === 'manifest') {
        const m = buildPortManifest();
        console.log(manifestAsMarkdown(m));
        return 0;
    }
    if (cmd === 'parity-audit') {
        const result = runParityAudit();
        console.log(parityAuditAsMarkdown(result));
        return 0;
    }
    if (cmd === 'setup-report') {
        const report = runSetup();
        console.log(setupReportAsMarkdown(report));
        return 0;
    }
    if (cmd === 'command-graph') {
        const graph = buildCommandGraph();
        console.log(graph.asMarkdown());
        return 0;
    }
    if (cmd === 'tool-pool') {
        const pool = assembleToolPool();
        console.log(pool.asMarkdown());
        return 0;
    }
    if (cmd === 'bootstrap-graph') {
        const graph = buildBootstrapGraph();
        console.log(graph.asMarkdown());
        return 0;
    }
    // ----------------------------------------------------------------
    // Subsystems
    // ----------------------------------------------------------------
    if (cmd === 'subsystems') {
        const limit = extractArgNum(raw, '--limit', 3, 32);
        const manifest = buildPortManifest();
        for (const subsystem of manifest.top_level_modules.slice(0, limit)) {
            console.log(`${subsystem.name}\t${subsystem.file_count}\t${subsystem.notes}`);
        }
        return 0;
    }
    // ----------------------------------------------------------------
    // Commands
    // ----------------------------------------------------------------
    if (cmd === 'commands') {
        const limit = extractArgNum(raw, '--limit', 3, 20);
        const query = extractArgStr(raw, '--query', 3, '');
        const noPlugin = hasFlag(raw, '--no-plugin-commands', 3);
        const noSkill = hasFlag(raw, '--no-skill-commands', 3);
        if (query) {
            console.log(renderCommandIndex(limit, query));
        }
        else {
            const commands = getCommands(undefined, !noPlugin, !noSkill);
            const outputLines = [`Command entries: ${commands.length}`, ''];
            for (const mod of commands.slice(0, limit)) {
                outputLines.push(`- ${mod.name} — ${mod.source_hint}`);
            }
            console.log(outputLines.join('\n'));
        }
        return 0;
    }
    // ----------------------------------------------------------------
    // Tools
    // ----------------------------------------------------------------
    if (cmd === 'tools') {
        const limit = extractArgNum(raw, '--limit', 3, 20);
        const query = extractArgStr(raw, '--query', 3, '');
        const simpleMode = hasFlag(raw, '--simple-mode', 3);
        const noMcp = hasFlag(raw, '--no-mcp', 3);
        const denyTools = extractAccumulated(raw, '--deny-tool', 3);
        const denyPrefixes = extractAccumulated(raw, '--deny-prefix', 3);
        const permissionContext = denyTools.length > 0 || denyPrefixes.length > 0
            ? ToolPermissionContext.fromIterables(denyTools, denyPrefixes)
            : undefined;
        if (query) {
            console.log(renderToolIndex(limit, query));
        }
        else {
            const tools = getTools(simpleMode, !noMcp, permissionContext);
            const outputLines = [`Tool entries: ${tools.length}`, ''];
            for (const mod of tools.slice(0, limit)) {
                outputLines.push(`- ${mod.name} — ${mod.source_hint}`);
            }
            console.log(outputLines.join('\n'));
        }
        return 0;
    }
    // ----------------------------------------------------------------
    // Route / Bootstrap / Turn-loop
    // ----------------------------------------------------------------
    if (cmd === 'route' || cmd === 'bootstrap' || cmd === 'turn-loop') {
        const prompt = extractFirstPositional(raw, 3);
        if (!prompt) {
            console.error(`Error: '${cmd}' requires a PROMPT argument`);
            return 1;
        }
        if (cmd === 'route') {
            const limit = extractArgNum(raw, '--limit', 3, 5);
            const runtime = new PortRuntime();
            const matches = runtime.route_prompt(prompt, limit);
            if (matches.length === 0) {
                console.log('No mirrored command/tool matches found.');
                return 0;
            }
            for (const match of matches) {
                console.log(`${match.kind}\t${match.name}\t${match.score}\t${match.source_hint}`);
            }
            return 0;
        }
        if (cmd === 'bootstrap') {
            const limit = extractArgNum(raw, '--limit', 3, 5);
            const runtime = new PortRuntime();
            const session = runtime.bootstrap_session(prompt, limit);
            console.log(session.asMarkdown());
            return 0;
        }
        // turn-loop
        const limit = extractArgNum(raw, '--limit', 3, 5);
        const maxTurns = extractArgNum(raw, '--max-turns', 3, 3);
        const structuredOutput = hasFlag(raw, '--structured-output', 3);
        const runtime = new PortRuntime();
        const results = runtime.run_turn_loop(prompt, limit, maxTurns, structuredOutput);
        for (let idx = 0; idx < results.length; idx++) {
            const result = results[idx];
            console.log(`## Turn ${idx + 1}`);
            console.log(result.output);
            console.log(`stop_reason=${result.stopReason}`);
        }
        return 0;
    }
    // ----------------------------------------------------------------
    // Flush-transcript
    // ----------------------------------------------------------------
    if (cmd === 'flush-transcript') {
        const prompt = extractFirstPositional(raw, 3);
        if (!prompt) {
            console.error("Error: 'flush-transcript' requires a PROMPT argument");
            return 1;
        }
        const engine = QueryEnginePort.fromWorkspace();
        engine.submitMessage(prompt);
        const path = engine.persistSession();
        console.log(path);
        console.log(`flushed=${engine._transcriptStore.flushed}`);
        return 0;
    }
    // ----------------------------------------------------------------
    // Load-session
    // ----------------------------------------------------------------
    if (cmd === 'load-session') {
        const sessionId = extractFirstPositional(raw, 3);
        if (!sessionId) {
            console.error("Error: 'load-session' requires a SESSION_ID argument");
            return 1;
        }
        const session = loadSession(sessionId);
        console.log(`${session.session_id}\n${session.messages.length} messages\nin=${session.input_tokens} out=${session.output_tokens}`);
        return 0;
    }
    // ----------------------------------------------------------------
    // Remote modes
    // ----------------------------------------------------------------
    if (cmd === 'remote-mode') {
        const target = extractFirstPositional(raw, 3);
        if (!target) {
            console.error("Error: 'remote-mode' requires a TARGET argument");
            return 1;
        }
        const report = runRemoteMode(target);
        console.log(`mode=${report.mode}\nconnected=${report.connected}\ndetail=${report.detail}`);
        return 0;
    }
    if (cmd === 'ssh-mode') {
        const target = extractFirstPositional(raw, 3);
        if (!target) {
            console.error("Error: 'ssh-mode' requires a TARGET argument");
            return 1;
        }
        const report = runSshMode(target);
        console.log(`mode=${report.mode}\nconnected=${report.connected}\ndetail=${report.detail}`);
        return 0;
    }
    if (cmd === 'teleport-mode') {
        const target = extractFirstPositional(raw, 3);
        if (!target) {
            console.error("Error: 'teleport-mode' requires a TARGET argument");
            return 1;
        }
        const report = runTeleportMode(target);
        console.log(`mode=${report.mode}\nconnected=${report.connected}\ndetail=${report.detail}`);
        return 0;
    }
    if (cmd === 'direct-connect-mode') {
        const target = extractFirstPositional(raw, 3);
        if (!target) {
            console.error("Error: 'direct-connect-mode' requires a TARGET argument");
            return 1;
        }
        const report = runDirectConnect(target);
        console.log(`mode=${report.mode}\ntarget=${report.target}\nactive=${report.active}`);
        return 0;
    }
    if (cmd === 'deep-link-mode') {
        const target = extractFirstPositional(raw, 3);
        if (!target) {
            console.error("Error: 'deep-link-mode' requires a TARGET argument");
            return 1;
        }
        const report = runDeepLink(target);
        console.log(`mode=${report.mode}\ntarget=${report.target}\nactive=${report.active}`);
        return 0;
    }
    // ----------------------------------------------------------------
    // Show / Exec
    // ----------------------------------------------------------------
    if (cmd === 'show-command') {
        const name = extractFirstPositional(raw, 3);
        if (!name) {
            console.error("Error: 'show-command' requires a NAME argument");
            return 1;
        }
        const module = getCommand(name);
        if (module === undefined) {
            console.log(`Command not found: ${name}`);
            return 1;
        }
        console.log(showModule(module));
        return 0;
    }
    if (cmd === 'show-tool') {
        const name = extractFirstPositional(raw, 3);
        if (!name) {
            console.error("Error: 'show-tool' requires a NAME argument");
            return 1;
        }
        const module = getTool(name);
        if (module === undefined) {
            console.log(`Tool not found: ${name}`);
            return 1;
        }
        console.log(showModule(module));
        return 0;
    }
    if (cmd === 'exec-command') {
        // Two positionals: name, prompt
        const posArgs = extractNPositional(raw, 3, 2);
        const name = posArgs[0];
        const prompt = posArgs[1] ?? '';
        if (!name) {
            console.error("Error: 'exec-command' requires a NAME and PROMPT argument");
            return 1;
        }
        const result = executeCommand(name, prompt);
        console.log(result.message);
        return result.handled ? 0 : 1;
    }
    if (cmd === 'exec-tool') {
        // Two positionals: name, payload
        const posArgs = extractNPositional(raw, 3, 2);
        const name = posArgs[0];
        const payload = posArgs[1] ?? '';
        if (!name) {
            console.error("Error: 'exec-tool' requires a NAME and PAYLOAD argument");
            return 1;
        }
        const result = executeTool(name, payload);
        console.log(result.message);
        return result.handled ? 0 : 1;
    }
    // ----------------------------------------------------------------
    // Unknown command
    // ----------------------------------------------------------------
    console.error(`Error: unknown command: ${cmd}`);
    printHelp();
    return 2;
}
// ---------------------------------------------------------------------------
// Flag / arg extraction helpers
// ---------------------------------------------------------------------------
/** Check if a flag is present in raw argv starting from a given command index. */
function hasFlag(raw, flag, _cmdIdx) {
    return raw.includes(flag);
}
/** Extract a numeric --flag value from raw argv. */
function extractArgNum(raw, flag, _cmdIdx, fallback) {
    const idx = raw.indexOf(flag);
    if (idx === -1 || idx + 1 >= raw.length)
        return fallback;
    const val = raw[idx + 1];
    const num = Number(val);
    return isNaN(num) ? fallback : num;
}
/** Extract a string --flag value from raw argv. */
function extractArgStr(raw, flag, _cmdIdx, fallback) {
    const idx = raw.indexOf(flag);
    if (idx === -1 || idx + 1 >= raw.length)
        return fallback;
    const val = raw[idx + 1];
    return val.startsWith('--') ? fallback : val;
}
/** Extract all occurrences of a repeatable --flag (accumulates values). */
function extractAccumulated(raw, flag, _cmdIdx) {
    const result = [];
    for (let i = 0; i < raw.length; i++) {
        if (raw[i] === flag && i + 1 < raw.length) {
            const val = raw[i + 1];
            if (!val.startsWith('--')) {
                result.push(val);
                i++;
            }
        }
    }
    return result;
}
/** Extract the first positional argument (non-flag, non-value) after the command. */
function extractFirstPositional(raw, startIdx) {
    let positionalIdx = 0;
    for (let i = startIdx; i < raw.length; i++) {
        const tok = raw[i];
        if (tok.startsWith('--')) {
            // Skip flag name
            if (tok === '--no-plugin-commands' ||
                tok === '--no-skill-commands' ||
                tok === '--simple-mode' ||
                tok === '--structured-output' ||
                tok.startsWith('--no-')) {
                // boolean flag, no value
            }
            else if (tok === '--deny-tool' || tok === '--deny-prefix' || tok === '--limit' || tok === '--query' || tok === '--max-turns') {
                i++; // skip value
            }
        }
        else {
            if (positionalIdx === 0)
                return tok;
            positionalIdx++;
        }
    }
    return '';
}
/** Extract the first N positional arguments. */
function extractNPositional(raw, startIdx, n) {
    const result = [];
    let positionalIdx = 0;
    for (let i = startIdx; i < raw.length; i++) {
        const tok = raw[i];
        if (tok.startsWith('--')) {
            if (tok === '--no-plugin-commands' ||
                tok === '--no-skill-commands' ||
                tok === '--simple-mode' ||
                tok === '--structured-output' ||
                tok.startsWith('--no-')) {
                // boolean flag
            }
            else if (tok === '--deny-tool' ||
                tok === '--deny-prefix' ||
                tok === '--limit' ||
                tok === '--query' ||
                tok === '--max-turns') {
                i++; // skip value
            }
        }
        else {
            if (positionalIdx < n) {
                result[positionalIdx] = tok;
                positionalIdx++;
            }
        }
    }
    // Fill missing with empty strings
    while (result.length < n) {
        result.push('');
    }
    return result;
}
// ---------------------------------------------------------------------------
// Help
// ---------------------------------------------------------------------------
function printHelp() {
    console.log(`\
Usage: ts-node src/main.ts <command> [options]

Commands:
  summary                  Render a Markdown summary of the porting workspace
  manifest                 Print the current workspace manifest
  parity-audit             Compare TypeScript port against the archived snapshot
  setup-report             Render the startup/prefetch setup report
  command-graph            Show command graph segmentation
  tool-pool                Show assembled tool pool with default settings
  bootstrap-graph          Show the mirrored bootstrap/runtime graph stages
  subsystems [--limit N]   List the current Python modules in the workspace
  commands [--limit N] [--query Q] [--no-plugin-commands] [--no-skill-commands]
                           List mirrored command entries from the archived snapshot
  tools [--limit N] [--query Q] [--simple-mode] [--no-mcp]
        [--deny-tool X] [--deny-prefix Y]
                           List mirrored tool entries from the archived snapshot
  route PROMPT [--limit N] Route a prompt across mirrored command/tool inventories
  bootstrap PROMPT [--limit N]
                           Build a runtime-style session report from the mirrored inventories
  turn-loop PROMPT [--limit N] [--max-turns N] [--structured-output]
                           Run a small stateful turn loop for the mirrored runtime
  flush-transcript PROMPT  Persist and flush a temporary session transcript
  load-session SESSION_ID  Load a previously persisted session
  remote-mode TARGET       Simulate remote-control runtime branching
  ssh-mode TARGET          Simulate SSH runtime branching
  teleport-mode TARGET      Simulate teleport runtime branching
  direct-connect-mode TARGET
                           Simulate direct-connect runtime branching
  deep-link-mode TARGET    Simulate deep-link runtime branching
  show-command NAME        Show one mirrored command entry by exact name
  show-tool NAME           Show one mirrored tool entry by exact name
  exec-command NAME PROMPT Execute a mirrored command shim by exact name
  exec-tool NAME PAYLOAD   Execute a mirrored tool shim by exact name
`);
}
// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------
main();
