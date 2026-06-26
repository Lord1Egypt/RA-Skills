// Execution Registry – mirrors commands and tools for execution
// Mirrored from Python src/execution_registry.py
import { PORTED_COMMANDS } from './commands.js';
import { PORTED_TOOLS } from './tools.js';
export class MirroredCommand {
    constructor(name, source_hint) {
        this.name = name;
        this.source_hint = source_hint;
    }
    execute(prompt) {
        // deferred import to avoid circular dependency at module level
        const { executeCommand } = require('./commands.js');
        return executeCommand(this.name, prompt).message;
    }
}
export class MirroredTool {
    constructor(name, source_hint) {
        this.name = name;
        this.source_hint = source_hint;
    }
    execute(payload) {
        const { executeTool } = require('./tools.js');
        return executeTool(this.name, payload).message;
    }
}
export class ExecutionRegistry {
    constructor(commands, tools) {
        this.commands = commands;
        this.tools = tools;
    }
    command(name) {
        const lowered = name.toLowerCase();
        return this.commands.find((c) => c.name.toLowerCase() === lowered) ?? undefined;
    }
    tool(name) {
        const lowered = name.toLowerCase();
        return this.tools.find((t) => t.name.toLowerCase() === lowered) ?? undefined;
    }
}
export function buildExecutionRegistry() {
    const commands = PORTED_COMMANDS.map((m) => new MirroredCommand(m.name, m.source_hint));
    const tools = PORTED_TOOLS.map((m) => new MirroredTool(m.name, m.source_hint));
    return new ExecutionRegistry(commands, tools);
}
