/**
 * OpenClaw Platform Adapter
 * 
 * Handles OpenClaw's JSONL format:
 * - Entry filter: type === 'message'
 * - Tool call: content[].type === "toolCall", arguments field
 * - Tool result: embedded in user message content as type === "toolResult",
 *   OR as independent message with role === "toolResult" (both supported)
 * - No thinking content in current format
 * - Session path: ~/.openclaw/agents/main/sessions/*.jsonl
 *   or /projects/.openclaw/agents/main/sessions/*.jsonl (Gongfeng/DevCloud environment)
 */

const os = require('os');
const path = require('path');
const fs = require('fs');
const { PlatformAdapter } = require('./base');

class OpenClawAdapter extends PlatformAdapter {
  get name() { return 'openclaw'; }

  detectPaths() {
    // Config override first
    const cfgPaths = super.detectPaths();
    if (cfgPaths.length > 0) return cfgPaths;
    
    const candidates = [
      // Gongfeng/DevCloud environment (non-standard HOME)
      '/projects/.openclaw/agents/main/sessions',
      // Standard HOME-based install
      path.join(os.homedir(), '.openclaw', 'agents', 'main', 'sessions'),
    ];
    return candidates.filter(p => {
      try { return fs.statSync(p).isDirectory(); } catch { return false; }
    });
  }

  isMessageEntry(entry) {
    return entry.type === 'message';
  }

  normalizeEntry(entry, idx) {
    const msg = entry.message || {};
    return {
      idx,
      type: 'message',
      role: msg.role || '',
      content: msg.content || [],
      timestamp: entry.timestamp || msg.timestamp || '',
      toolCallId: msg.toolCallId || null,
      toolName: msg.toolName || null,
      isError: msg.isError || false,
      metadata: {},
      raw: msg,
    };
  }

  // OpenClaw content already uses toolCall/toolResult naming,
  // no field renaming needed. No postProcess needed.

  getSkillSearchPaths() {
    // Config override first
    const cfgPaths = super.getSkillSearchPaths();
    if (cfgPaths.length > 0) return cfgPaths;
    
    const paths = [
      // Derive from adapter's own location
      path.resolve(__dirname, '..', '..', '..'),
      path.join(os.homedir(), '.openclaw', 'skills'),
      '/projects/.openclaw/skills',
    ];
    // Deduplicate (resolve may match static path)
    const seen = new Set();
    return paths.filter(p => {
      try {
        const real = fs.realpathSync(p);
        if (seen.has(real)) return false;
        seen.add(real);
        return fs.statSync(p).isDirectory();
      } catch { return false; }
    });
  }

  detectLLM() {
    // Config override first
    const cfgLLM = super.detectLLM();
    if (cfgLLM) return cfgLLM;
    
    // Read openclaw.json to find a provider with apiKey
    const { loadOpenClawConfig } = require('../lib/llm-client');
    let cfg;
    try {
      const result = loadOpenClawConfig();
      cfg = result?.cfg;
    } catch { return null; }
    if (!cfg) return null;

    const providers = cfg.models?.providers || {};

    // Priority: subagents model > main model > any provider with apiKey
    const candidates = [];
    const subModel = cfg.agents?.defaults?.subagents?.model;
    if (subModel?.primary) candidates.push(subModel.primary);
    if (Array.isArray(subModel?.fallbacks)) candidates.push(...subModel.fallbacks);
    const mainModel = cfg.agents?.defaults?.model?.primary;
    if (mainModel) candidates.push(mainModel);

    for (const spec of candidates) {
      const slash = spec.indexOf('/');
      if (slash < 0) continue;
      const provName = spec.substring(0, slash);
      const modelId = spec.substring(slash + 1);
      const provider = providers[provName];
      if (provider?.baseUrl && provider?.apiKey) {
        return {
          baseUrl: provider.baseUrl,
          apiKey: provider.apiKey,
          model: modelId,
          api: provider.api || 'openai-completions',
          providerName: provName,
          source: 'openclaw.json',
        };
      }
    }

    // Fallback: any provider with apiKey
    for (const [name, provider] of Object.entries(providers)) {
      if (provider?.baseUrl && provider?.apiKey && provider?.models?.length > 0) {
        return {
          baseUrl: provider.baseUrl,
          apiKey: provider.apiKey,
          model: provider.models[0].id,
          api: provider.api || 'openai-completions',
          providerName: name,
          source: 'openclaw.json',
        };
      }
    }

    return null;
  }
}

module.exports = { OpenClawAdapter };
