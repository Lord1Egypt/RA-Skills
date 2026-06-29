/**
 * PlatformAdapter base class.
 * 
 * Each platform adapter normalizes raw JSONL entries into a standard format
 * that trace-extractor can consume without modification.
 * 
 * Naming convention: normalized output uses OpenClaw-style field names
 * (toolCall/toolResult) so trace-extractor internals need zero changes.
 */

const path = require('path');
const fs = require('fs');

class PlatformAdapter {
  /**
   * @param {object} [config] - evolver-config.json contents (optional overrides)
   */
  constructor(config = {}) {
    this._config = config;
  }

  /**
   * Human-readable platform name.
   * @returns {string}
   */
  get name() { return 'unknown'; }

  /**
   * Detect session directory paths for this platform.
   * Config override: sessions.paths (array of absolute paths)
   * @returns {string[]} existing directory paths (may be empty)
   */
  detectPaths() {
    const cfgPaths = this._config?.sessions?.paths;
    if (Array.isArray(cfgPaths) && cfgPaths.length > 0) {
      return cfgPaths.filter(p => {
        try { return fs.statSync(p).isDirectory(); } catch { return false; }
      });
    }
    return [];
  }

  /**
   * Is this JSONL entry a message record (vs session metadata, model_change, etc)?
   * @param {object} entry - parsed JSONL line
   * @returns {boolean}
   */
  isMessageEntry(entry) { throw new Error('not implemented'); }

  /**
   * Normalize a single JSONL entry into standard message format.
   * Caller guarantees isMessageEntry(entry) === true.
   * 
   * @param {object} entry - raw parsed JSONL line
   * @param {number} idx - 0-based index within session
   * @returns {NormalizedMessage}
   */
  normalizeEntry(entry, idx) { throw new Error('not implemented'); }

  /**
   * Optional batch post-processing (e.g. toolResult reordering).
   * Default: identity.
   * @param {NormalizedMessage[]} messages
   * @returns {NormalizedMessage[]}
   */
  postProcess(messages) { return messages; }

  /**
   * Detect if a normalized message is a SKILL.md activation event.
   * Default implementation: file-read activation (covers most platforms).
   * 
   * @param {NormalizedMessage} msg
   * @returns {{ detected: boolean, skillName: string | null }}
   */
  isSkillActivation(msg) {
    if (msg.role !== 'assistant') return { detected: false, skillName: null };
    for (const c of msg.content) {
      if (c.type !== 'toolCall') continue;
      const readPath = (c.arguments || {}).path || (c.arguments || {}).file_path || '';
      if (!readPath.match(/SKILL\.md$/i)) continue;
      const parts = readPath.replace(/\\/g, '/').split('/');
      const skillMdIdx = parts.lastIndexOf('SKILL.md');
      const dirName = skillMdIdx > 0 ? parts[skillMdIdx - 1] : null;
      if (!dirName) continue;

      const skillName = this._resolveSkillName(dirName);
      if (skillName === 'skill-evolver') continue;

      return { detected: true, skillName };
    }
    return { detected: false, skillName: null };
  }

  /**
   * Return skill directory search paths for this platform.
   * Config override: skills.paths (array of absolute paths)
   * Used by patcher to find SKILL.md files for inline.
   * @returns {string[]}
   */
  getSkillSearchPaths() {
    const cfgPaths = this._config?.skills?.paths;
    if (Array.isArray(cfgPaths) && cfgPaths.length > 0) {
      return cfgPaths.filter(p => {
        try { return fs.statSync(p).isDirectory(); } catch { return false; }
      });
    }
    return [];
  }

  /**
   * Detect LLM provider configuration.
   * Config override: llm { apiKey, baseUrl, model, api }
   * Returns { baseUrl, apiKey, model, api, providerName, source } or null.
   * @returns {{ baseUrl: string, apiKey: string, model: string, api: string, providerName: string, source: string } | null}
   */
  detectLLM() {
    const cfgLLM = this._config?.llm;
    if (cfgLLM?.apiKey && cfgLLM?.baseUrl && cfgLLM?.model) {
      return {
        baseUrl: cfgLLM.baseUrl,
        apiKey: cfgLLM.apiKey,
        model: cfgLLM.model,
        api: cfgLLM.api || 'openai-completions',
        providerName: 'evolver-config',
        source: 'evolver-config.json',
      };
    }
    return null;
  }

  /**
   * Resolve directory name to skill name.
   * Override in adapters where dir name != skill name (e.g. UUID dirs).
   * @param {string} dirName
   * @returns {string}
   */
  _resolveSkillName(dirName) {
    return dirName;
  }
}

module.exports = { PlatformAdapter };
