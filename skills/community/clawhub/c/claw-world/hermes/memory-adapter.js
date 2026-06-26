'use strict';

function mergeCortex(existing, fragments) {
  const vivid = Array.isArray(existing && existing.vivid) ? existing.vivid.slice() : [];
  const additions = Array.isArray(fragments) ? fragments : [];
  return {
    vivid: vivid.concat(additions).slice(-30),
    sediment: Array.isArray(existing && existing.sediment) ? existing.sediment : []
  };
}

class HermesMemoryAdapter {
  constructor(runtime, sessionStore) {
    this.runtime = runtime;
    this.sessionStore = sessionStore;
  }

  async loadBootMemory(tokenId) {
    const result = await this.runtime.cmlLoad(tokenId, false);
    return result.parsed;
  }

  async flushSessionMemory(sessionId, tokenId, auth) {
    const full = await this.runtime.cmlLoad(tokenId, true);
    const session = this.sessionStore.get(sessionId);
    const fragments = session && Array.isArray(session.hippocampus) ? session.hippocampus : [];
    const cml = {
      version: 3,
      nfa_id: full.parsed.nfa_id,
      IDENTITY: full.parsed.identity,
      PULSE: Object.assign({}, full.parsed.pulse),
      PREFRONTAL: full.parsed.prefrontal,
      BASAL: full.parsed.basal,
      CORTEX: mergeCortex(full.parsed.cortex, fragments)
    };

    const saved = await this.runtime.cmlSave(tokenId, cml, auth);
    this.sessionStore.upsert(sessionId, { hippocampus: [] });
    return saved.parsed;
  }
}

module.exports = {
  HermesMemoryAdapter
};
