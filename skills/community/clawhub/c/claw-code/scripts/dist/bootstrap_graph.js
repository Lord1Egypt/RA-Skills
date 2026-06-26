// Bootstrap Graph — models the ordered stages of the claw-code bootstrap / runtime lifecycle.
/**
 * A read-only ordered sequence of bootstrap stages.
 * Each stage is a human-readable label describing a phase in the startup pipeline.
 */
export class BootstrapGraph {
    constructor(stages) {
        this.stages = stages;
    }
    /**
     * Render the bootstrap graph as a Markdown document.
     */
    asMarkdown() {
        const lines = ['# Bootstrap Graph', ''];
        for (const stage of this.stages) {
            lines.push(`- ${stage}`);
        }
        return lines.join('\n');
    }
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
export function buildBootstrapGraph() {
    return new BootstrapGraph([
        'top-level prefetch side effects',
        'warning handler and environment guards',
        'CLI parser and pre-action trust gate',
        'setup() + commands/agents parallel load',
        'deferred init after trust',
        'mode routing: local / remote / ssh / teleport / direct-connect / deep-link',
        'query engine submit loop',
    ]);
}
