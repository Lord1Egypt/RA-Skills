/**
 * A read-only ordered sequence of bootstrap stages.
 * Each stage is a human-readable label describing a phase in the startup pipeline.
 */
export declare class BootstrapGraph {
    readonly stages: readonly string[];
    constructor(stages: readonly string[]);
    /**
     * Render the bootstrap graph as a Markdown document.
     */
    asMarkdown(): string;
}
/**
 * Build the canonical bootstrap graph for claw-code.
 *
 * The stages are ordered to reflect the actual startup sequence:
 *  1. top-level prefetch side effects
 *  2. warning handler and environment guards
 *  3. CLI parser and pre-action trust gate
 *  4. setup() + commands/agents parallel load
 *  5. deferred init after trust
 *  6. mode routing: local / remote / ssh / teleport / direct-connect / deep-link
 *  7. query engine submit loop
 */
export declare function buildBootstrapGraph(): BootstrapGraph;
