/**
 * agentmemory OpenClaw Plugin
 * 
 * Provides automatic memory recall before sessions and capture after.
 * Requires agentmemory server running on localhost:3111.
 */

const axios = require('axios');

class AgentMemoryPlugin {
  constructor(config = {}) {
    this.baseUrl = config.base_url || 'http://localhost:3111';
    this.tokenBudget = config.token_budget || 2000;
    this.minConfidence = config.min_confidence || 0.5;
    this.fallbackOnError = config.fallback_on_error !== false;
    this.timeoutMs = config.timeout_ms || 5000;
    this.enabled = true;
  }

  // Called before agent starts - recall relevant memories
  async onBeforeAgent(context) {
    try {
      const query = this.buildContextQuery(context);
      const response = await axios.post(
        `${this.baseUrl}/agentmemory/recall`,
        { query, limit: 5, threshold: this.minConfidence },
        { timeout: this.timeoutMs }
      );
      
      if (response.data?.memories?.length > 0) {
        return {
          injected: response.data.memories.map(m => ({
            role: 'system',
            content: `[agentmemory] Relevant memory: ${m.content}`
          })),
          source: 'agentmemory'
        };
      }
    } catch (err) {
      if (this.fallbackOnError) {
        console.warn('[agentmemory] Recall failed, continuing without memory:', err.message);
      } else {
        throw err;
      }
    }
    return null;
  }

  // Called after agent finishes - capture key decisions
  async onAfterAgent(context) {
    try {
      const summary = this.extractSummary(context);
      if (summary) {
        await axios.post(
          `${this.baseUrl}/agentmemory/save`,
          {
            content: summary,
            type: 'observation',
            tags: this.extractTags(context),
            metadata: {
              session: context.sessionId,
              timestamp: new Date().toISOString()
            }
          },
          { timeout: this.timeoutMs }
        );
      }
    } catch (err) {
      console.error('[agentmemory] Capture failed:', err.message);
    }
  }

  buildContextQuery(context) {
    const parts = [];
    if (context.topic) parts.push(context.topic);
    if (context.project) parts.push(context.project);
    if (context.recentTasks?.length) parts.push(...context.recentTasks.slice(0, 3));
    return parts.join(' ');
  }

  extractSummary(context) {
    if (context.result?.summary) return context.result.summary;
    if (context.messages?.length) {
      const last = context.messages[context.messages.length - 1];
      return last.content?.slice(0, 500);
    }
    return null;
  }

  extractTags(context) {
    const tags = [];
    if (context.channel) tags.push(context.channel);
    if (context.topic) tags.push(context.topic);
    return tags;
  }

  // Health check for plugin loader
  async ping() {
    try {
      const response = await axios.get(
        `${this.baseUrl}/agentmemory/health`,
        { timeout: this.timeoutMs }
      );
      return { ok: true, version: response.data?.version };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  }
}

module.exports = AgentMemoryPlugin;