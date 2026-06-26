'use strict';

// Rewrites the `model` field on an Anthropic /v1/messages request body
// without touching the `messages` array. The Anthropic prompt cache keys
// off the (model + messages + system + tools) tuple including any
// per-block `cache_control: { type: "ephemeral" }` markers. Since we
// only swap the top-level model string, all cache_control breakpoints
// the client placed remain intact and the cache prefix the client
// established with prior turns continues to hit.
//
// This is a pure function: it returns a shallow clone, never mutates
// the input. Callers pass a fresh body each request so deep cloning
// would be wasted work.
//
// Why a fresh module under src/proxy/router/: this is the second
// utility for Phase C alongside model_router.js. Bundling them into a
// shared dir keeps slice 4+ from sprawling helpers across src/proxy/.

function rewriteModel(body, newModel) {
  if (!body || typeof body !== 'object') return body;
  if (!newModel || typeof newModel !== 'string') return body;
  if (body.model === newModel) return body;
  return { ...body, model: newModel };
}

module.exports = { rewriteModel };
