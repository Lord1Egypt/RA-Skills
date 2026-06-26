// Command Graph — organises mirrored commands into three buckets:
//   • builtins   – core commands shipped in the main package
//   • plugin-like – commands that originate from plugins
//   • skill-like  – commands that originate from skills
import { getCommands } from './commands.js';
/**
 * Read-only command graph.
 * Commands are bucketed by their `sourceHint` category.
 */
export class CommandGraph {
    constructor(builtins, pluginLike, skillLike) {
        this.builtins = builtins;
        this.pluginLike = pluginLike;
        this.skillLike = skillLike;
    }
    /**
     * All commands in a single flat tuple, in the order:
     * builtins → pluginLike → skillLike.
     */
    flattened() {
        return [...this.builtins, ...this.pluginLike, ...this.skillLike];
    }
    /**
     * Render the command graph as a Markdown summary.
     */
    asMarkdown() {
        const lines = [
            '# Command Graph',
            '',
            `Builtins: ${this.builtins.length}`,
            `Plugin-like commands: ${this.pluginLike.length}`,
            `Skill-like commands: ${this.skillLike.length}`,
        ];
        return lines.join('\n');
    }
}
/**
 * Build the canonical command graph by partitioning all registered commands
 * according to their `sourceHint` field.
 */
export function buildCommandGraph() {
    const commands = getCommands();
    const builtins = [];
    const pluginLike = [];
    const skillLike = [];
    for (const module of commands) {
        const hint = module.source_hint.toLowerCase();
        if (hint.includes('plugin')) {
            pluginLike.push(module);
        }
        else if (hint.includes('skills')) {
            skillLike.push(module);
        }
        else {
            builtins.push(module);
        }
    }
    return new CommandGraph(builtins, pluginLike, skillLike);
}
