/**
 * EXAMPLE definition — regenerate from analyze_dsl.py output for the real DSL.
 *
 * Data-only file: nodes and edges translated 1:1 from the Dify DSL.
 * Handlers for non-engine node types live in src/workflow/blocks/.
 */
import { HANDLERS as exampleHandlers } from './blocks/example.js';

export const DEFINITION = {
  start_id: 'start-1',
  nodes: {
    'start-1': { type: 'start', config: {} },
    'tpl-1': {
      type: 'template-transform',
      config: { template: 'Echo: {{#start-1.text#}}' },
    },
    'end-1': {
      type: 'end',
      config: {
        outputs: [
          { variable: 'result', value_selector: ['tpl-1', 'output'] },
        ],
      },
    },
  },
  edges: [
    { source: 'start-1', target: 'tpl-1', handle: 'source' },
    { source: 'tpl-1', target: 'end-1', handle: 'source' },
  ],
};

/** Return {node_id: handler}. Assembled from blocks/ modules. */
export function buildHandlers() {
  return { ...exampleHandlers };
}
