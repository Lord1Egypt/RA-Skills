/**
 * Tool Pool – assembled tool inventory with default settings.
 * Mirrored from Python src/tool_pool.py
 *
 * Strict mode: enabled (tsconfig.json strict:true)
 */
import { getTools } from './tools.js';
/**
 * Frozen snapshot of the assembled tool pool.
 */
export class ToolPool {
    constructor(args) {
        this.tools = args.tools;
        this.simple_mode = args.simple_mode;
        this.include_mcp = args.include_mcp;
    }
    /**
     * Render the tool pool as a Markdown summary.
     */
    asMarkdown() {
        const lines = [
            '# Tool Pool',
            '',
            `Simple mode: ${this.simple_mode}`,
            `Include MCP: ${this.include_mcp}`,
            `Tool count: ${this.tools.length}`,
        ];
        for (const tool of this.tools.slice(0, 15)) {
            lines.push(`- ${tool.name} — ${tool.source_hint}`);
        }
        return lines.join('\n');
    }
}
/**
 * Assemble the tool pool with the given options.
 */
export function assembleToolPool(simple_mode = false, include_mcp = true, permission_context) {
    return new ToolPool({
        tools: getTools(simple_mode, include_mcp, permission_context),
        simple_mode,
        include_mcp,
    });
}
