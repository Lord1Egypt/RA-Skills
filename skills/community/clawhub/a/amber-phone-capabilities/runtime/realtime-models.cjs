'use strict';

const REALTIME_MODELS = Object.freeze(['gpt-realtime-2.1', 'gpt-realtime-2.1-mini']);
const DEFAULT_REALTIME_MODEL = REALTIME_MODELS[0];
const legacyModels = new Map([
  ['gpt-realtime', REALTIME_MODELS[0]],
  ['gpt-realtime-2025-08-28', REALTIME_MODELS[0]],
  ['gpt-realtime-mini', REALTIME_MODELS[1]],
  ['gpt-realtime-mini-2025-12-15', REALTIME_MODELS[1]],
  ['gpt-realtime-mini-2025-10-06', REALTIME_MODELS[1]],
]);

function normalizeRealtimeModel(value) {
  const model = value.trim();
  return legacyModels.get(model) ?? model;
}

module.exports = { DEFAULT_REALTIME_MODEL, REALTIME_MODELS, normalizeRealtimeModel };
