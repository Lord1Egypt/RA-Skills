'use strict';

class HermesSessionStore {
  constructor() {
    this.sessions = new Map();
  }

  get(sessionId) {
    return this.sessions.get(sessionId) || null;
  }

  upsert(sessionId, patch) {
    const current = this.get(sessionId) || {
      sessionId,
      selectedNfaId: null,
      lastBoot: null,
      language: null,
      pendingTask: null,
      pendingPk: null,
      hippocampus: []
    };

    const next = Object.assign({}, current, patch || {});
    this.sessions.set(sessionId, next);
    return next;
  }

  appendMemory(sessionId, entry) {
    const current = this.get(sessionId) || this.upsert(sessionId);
    const hippocampus = current.hippocampus.concat([entry]);
    return this.upsert(sessionId, { hippocampus });
  }

  clear(sessionId) {
    this.sessions.delete(sessionId);
  }
}

module.exports = {
  HermesSessionStore
};
