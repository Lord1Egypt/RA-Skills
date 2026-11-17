/**
 * EXAMPLE block handler — replace with real blocks generated per DSL.
 *
 * Handler signature: (nodeId, config, pool, engine) => void | Promise<void>
 * Write outputs via pool.set(nodeId, '<var>', value).
 */
function templateTransform(nodeId, config, pool) {
  pool.set(nodeId, 'output', pool.resolve(config.template || ''));
}

export const HANDLERS = {
  'tpl-1': templateTransform,
};
