// src/api/commands.js
const GeneProcessor = require('../core/gene-processor');
const VerificationEngine = require('../core/verification-engine');
const EnvChecker = require('../core/env-checker');

class CommandHandler {
  constructor(store, embedding, injector, llmClient) {
    this.store = store;
    this.embedding = embedding;
    this.injector = injector;
    this.processor = new GeneProcessor(llmClient);
    this.verifier = new VerificationEngine(llmClient);
  }

  /**
   * !exp consult '<query>'
   * Manual consultation for an experience.
   */
  async consult(query) {
    const vector = await this.embedding.vectorize(query);
    const results = await this.store.findSimilar(vector, { k: 3, minScore: 0.7 });
    
    if (results.length === 0) {
      return "[EvoMap] No matching experience found.";
    }

    return results.map(r => this.injector.format(r)).join('

');
  }

  /**
   * !exp commit
   * Automatically distill and commit current session experience.
   */
  async commit(sessionHistory, options = {}) {
    console.log("[EvoMap] Distilling experience from current session...");
    
    const distilled = await this.processor.distillExperience(sessionHistory, options);
    const env = EnvChecker.getFingerprint();
    const capsule = this.processor.buildCapsule(distilled, env, options);
    
    console.log("[EvoMap] Verifying quality via self-reflection...");
    const reflection = await this.verifier.selfReflect(capsule);
    const trustScore = this.verifier.computeTrustScore(reflection);
    
    capsule.trustScore = trustScore;
    const decision = this.verifier.shouldStore(trustScore);
    
    if (!decision.allow) {
      return `[EvoMap] Commit rejected: ${decision.reason}`;
    }

    await this.store.insert(capsule);
    return `[经验已存储] capsuleId: ${capsule.capsuleId}${decision.quarantine ? ' (Quarantined)' : ''}`;
  }

  /**
   * !exp list
   * List summary of stored experiences.
   */
  async list() {
    const db = this.store.db;
    const stats = db.prepare('SELECT COUNT(*) as count, AVG(trustScore) as avgTrust FROM capsules').get();
    const recent = db.prepare('SELECT capsuleId, category, trustScore FROM capsules ORDER BY createdAt DESC LIMIT 5').all();
    
    let output = `[EvoMap Stats] Count: ${stats.count}, Avg Trust: ${stats.avgTrust?.toFixed(2) || 0}
`;
    output += `[Recent Capsules]:
`;
    recent.forEach(c => {
      output += `  - ${c.capsuleId} [${c.category}] (Score: ${c.trustScore.toFixed(2)})
`;
    });
    
    return output;
  }
}

module.exports = CommandHandler;
