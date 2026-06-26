/**
 * Tool Pool – assembled tool inventory with default settings.
 * Mirrored from Python src/tool_pool.py
 *
 * Strict mode: enabled (tsconfig.json strict:true)
 */
import { PortingModule } from './models.js';
import { ToolPermissionContext } from './permissions.js';
/**
 * Frozen snapshot of the assembled tool pool.
 */
export declare class ToolPool {
    readonly tools: readonly PortingModule[];
    readonly simple_mode: boolean;
    readonly include_mcp: boolean;
    constructor(args: {
        tools: readonly PortingModule[];
        simple_mode: boolean;
        include_mcp: boolean;
    });
    /**
     * Render the tool pool as a Markdown summary.
     */
    asMarkdown(): string;
}
/**
 * Assemble the tool pool with the given options.
 */
export declare function assembleToolPool(simple_mode?: boolean, include_mcp?: boolean, permission_context?: ToolPermissionContext): ToolPool;
