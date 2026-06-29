/**
 * Claude Code Platform Adapter
 * 
 * Handles Claude Code's JSONL format:
 * - Entry filter: type === 'user' || type === 'assistant' (NOT 'message')
 * - Tool call: content[].type === "tool_use", input field → normalized to toolCall + arguments
 * - Tool result: embedded in user message content as type === "tool_result", tool_use_id field
 * - Has thinking content (filtered)
 * - Subagent JSONL in <uuid>/subagents/ → MVP does NOT process these
 * - Session path: ~/.claude-internal/projects/<encoded-path>/*.jsonl (Tencent)
 *                 ~/.claude/projects/<encoded-path>/*.jsonl (official)
 * 
 * Key naming differences from OpenClaw:
 *   tool_use → toolCall, input → arguments, tool_result.tool_use_id → toolCallId
 *   Read (capital R) vs read (lowercase) — isSkillActivation handles both
 */

const os = require('os');
const path = require('path');
const fs = require('fs');
const { PlatformAdapter } = require('./base');

class ClaudeCodeAdapter extends PlatformAdapter {
  get name() { return 'claude-code'; }

  detectPaths() {
    // Config override first
    const cfgPaths = super.detectPaths();
    if (cfgPaths.length > 0) return cfgPaths;
    
    const results = [];

    // Tencent customized version
    const internalBase = path.join(os.homedir(), '.claude-internal', 'projects');
    // Official version
    const officialBase = path.join(os.homedir(), '.claude', 'projects');

    for (const base of [internalBase, officialBase]) {
      if (!fs.existsSync(base)) continue;
      try {
        const subdirs = fs.readdirSync(base)
          .map(d => path.join(base, d))
          .filter(p => { try { return fs.statSync(p).isDirectory(); } catch { return false; } });
        results.push(...subdirs);
      } catch { /* skip */ }
    }
    return results;
  }

  isMessageEntry(entry) {
    // Claude Code uses 'user' and 'assistant' as top-level type (not 'message')
    // Filter out: system, progress, queue-operation, file-history-snapshot, etc.
    return entry.type === 'user' || entry.type === 'assistant';
  }

  normalizeEntry(entry, idx) {
    const msg = entry.message || {};
    const role = msg.role || entry.type; // 'user' | 'assistant'

    // Normalize content: string → [{type:'text', text}], missing → []
    const rawContent = Array.isArray(msg.content)
      ? msg.content
      : (typeof msg.content === 'string' && msg.content ? [{ type: 'text', text: msg.content }] : []);

    const content = rawContent.map(c => {
      if (c.type === 'thinking') return null; // filter thinking

      if (c.type === 'tool_use') {
        // Claude Code: tool_use + input → toolCall + arguments
        return {
          type: 'toolCall',
          id: c.id || '',
          name: c.name,
          arguments: c.input || {},
        };
      }

      if (c.type === 'tool_result') {
        // Claude Code: tool_result embedded in user message content
        // Normalize content: can be string, array of {text}, or other
        let resultContent = '';
        if (typeof c.content === 'string') {
          resultContent = c.content;
        } else if (Array.isArray(c.content)) {
          resultContent = c.content.map(x => x.text || '').join('');
        }

        return {
          type: 'toolResult',
          toolCallId: c.tool_use_id || '',
          content: resultContent,
          isError: c.is_error || false,
        };
      }

      return c; // text etc.
    }).filter(Boolean);

    // For user messages containing tool_result, we need to handle them specially:
    // trace-extractor expects toolResult as independent messages (role='toolResult')
    // but Claude Code embeds them in user messages.
    // We'll handle this in postProcess.

    return {
      idx,
      type: 'message',
      role,
      content,
      timestamp: entry.timestamp || '',
      toolCallId: null,
      toolName: null,
      isError: false,
      metadata: {
        sessionId: entry.sessionId,
        uuid: entry.uuid,
        cwd: entry.cwd,
        gitBranch: entry.gitBranch,
        model: msg.model,
      },
    };
  }

  /**
   * Post-process: split user messages with embedded tool_result into
   * independent toolResult messages, matching OpenClaw behavior.
   * 
   * Claude Code embeds tool_result in user message content:
   *   { role: 'user', content: [{ type: 'tool_result', tool_use_id: '...', content: '...' }] }
   * 
   * trace-extractor's formatTrace expects independent messages with role='toolResult'.
   * We split each tool_result content item into its own message.
   */
  postProcess(messages) {
    const result = [];
    let reIdx = 0;

    for (const msg of messages) {
      if (msg.role === 'user') {
        const safeContent = Array.isArray(msg.content) ? msg.content : [];
        const toolResults = safeContent.filter(c => c.type === 'toolResult');
        const otherContent = safeContent.filter(c => c.type !== 'toolResult');

        // If user message has non-tool_result content (actual user text), keep it
        if (otherContent.length > 0) {
          result.push({ ...msg, idx: reIdx++, content: otherContent });
        }

        // Split each tool_result into independent message
        for (const tr of toolResults) {
          result.push({
            idx: reIdx++,
            type: 'message',
            role: 'toolResult',
            content: [{ type: 'text', text: tr.content || '' }],
            timestamp: msg.timestamp,
            toolCallId: tr.toolCallId || null,
            toolName: null, // Claude Code tool_result doesn't carry toolName
            isError: tr.isError || false,
            metadata: msg.metadata,
          });
        }
      } else {
        result.push({ ...msg, idx: reIdx++ });
      }
    }

    return result;
  }

  getSkillSearchPaths() {
    const cfgPaths = super.getSkillSearchPaths();
    if (cfgPaths.length > 0) return cfgPaths;
    
    // Claude Code skills: ~/.claude/skills/ (standard) or project-local .claude/skills/
    const paths = [
      path.join(os.homedir(), '.claude', 'skills'),
      path.join(os.homedir(), '.claude-internal', 'skills'),
    ];
    // Also check project-local .claude/skills if cwd has one
    const localSkills = path.join(process.cwd(), '.claude', 'skills');
    paths.push(localSkills);
    return paths.filter(p => {
      try { return fs.statSync(p).isDirectory(); } catch { return false; }
    });
  }

  // Claude Code uses OAuth tokens, not API keys. Cannot auto-detect LLM config.
  // Users need to set EVOLVER_API_KEY/EVOLVER_BASE_URL/EVOLVER_MODEL env vars.
  // detectLLM() returns null (inherited from base).

  /**
   * Override: Detect skill activation for Claude Code.
   *
   * Two activation paths (in priority order):
   *
   *   1. Native Skill tool (current primary path):
   *      Claude Code's built-in `Skill` tool:
   *        { name: 'Skill', input: { skill: 'some-skill-name' } }
   *      The framework injects SKILL.md body directly; no Read tool call occurs.
   *
   *   2. Legacy Read SKILL.md (retained for back-compat with older JSONL):
   *      Pre-Skill-tool Claude Code versions used file-read activation.
   *      Capitalized tool name 'Read' and 'file_path' arg.
   *
   * NOT yet covered (design doc §4: Agent(subagent_type=...) subagent delegation):
   *   Subagent path (`Agent` tool with `subagent_type`) produces its own JSONL.
   *   See 跨平台适配设计.md L188 for the original plan; not implemented here.
   */
  isSkillActivation(msg) {
    if (msg.role !== 'assistant') return { detected: false, skillName: null };
    for (const c of (Array.isArray(msg.content) ? msg.content : [])) {
      if (c.type !== 'toolCall') continue;

      // Path 1: native Skill tool (primary since Claude Code built-in Skill support)
      if (c.name === 'Skill') {
        const skillName = (c.arguments || {}).skill || null;
        if (skillName && skillName !== 'skill-evolver') {
          return { detected: true, skillName };
        }
        continue;
      }

      // Path 2: legacy Read SKILL.md (kept for old JSONL compatibility)
      if (c.name !== 'read' && c.name !== 'Read') continue;
      const readPath = (c.arguments || {}).path || (c.arguments || {}).file_path || '';
      if (!readPath.match(/SKILL\.md$/i)) continue;
      const parts = readPath.replace(/\\/g, '/').split('/');
      const skillMdIdx = parts.lastIndexOf('SKILL.md');
      const skillName = skillMdIdx > 0 ? parts[skillMdIdx - 1] : null;
      if (skillName && skillName !== 'skill-evolver') {
        return { detected: true, skillName };
      }
    }
    return { detected: false, skillName: null };
  }
}

module.exports = { ClaudeCodeAdapter };
