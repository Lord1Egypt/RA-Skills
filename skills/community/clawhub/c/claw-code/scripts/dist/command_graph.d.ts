import type { PortingModule } from './models.js';
/**
 * Read-only command graph.
 * Commands are bucketed by their `sourceHint` category.
 */
export declare class CommandGraph {
    readonly builtins: readonly PortingModule[];
    readonly pluginLike: readonly PortingModule[];
    readonly skillLike: readonly PortingModule[];
    constructor(builtins: readonly PortingModule[], pluginLike: readonly PortingModule[], skillLike: readonly PortingModule[]);
    /**
     * All commands in a single flat tuple, in the order:
     * builtins → pluginLike → skillLike.
     */
    flattened(): readonly PortingModule[];
    /**
     * Render the command graph as a Markdown summary.
     */
    asMarkdown(): string;
}
/**
 * Build the canonical command graph by partitioning all registered commands
 * according to their `sourceHint` field.
 */
export declare function buildCommandGraph(): CommandGraph;
