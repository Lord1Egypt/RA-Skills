/**
 * ai-explainer.js — AI explanation module for diff-wizard
 *
 * Generates natural-language explanations of diffs using LLM.
 * Only sends diff hunks (not full files) with credential redaction.
 * Falls back gracefully when LLM is unavailable.
 */

'use strict';

const security = require('./security');

/**
 * Generate AI explanation context from diff result.
 * Builds a concise prompt with only the essential diff info.
 * @param {object} diffResult - The result from diff-engine
 * @param {object} [opts]
 * @param {string} [opts.language='auto']  - 'zh-CN', 'en-US', or 'auto'
 * @returns {string} Prompt content for LLM
 */
function buildExplainPrompt(diffResult, opts = {}) {
  const lang = opts.language || 'auto';
  const format = diffResult.format_detected || 'text';

  // Build a compact diff summary for the LLM
  let hunksText = '';
  let totalChars = 0;
  const maxChars = 4000;

  if (diffResult.structured_diff && diffResult.structured_diff.length > 0) {
    // Use structured diff entries
    for (const entry of diffResult.structured_diff) {
      let entryText;
      if (entry.type === 'added') {
        entryText = `+ ${entry.content || entry.new_value || ''}`;
      } else if (entry.type === 'deleted') {
        entryText = `- ${entry.content || entry.old_value || ''}`;
      } else {
        entryText = `~ ${entry.old_value || ''} → ${entry.new_value || ''}`;
      }

      if (totalChars + entryText.length + 1 <= maxChars) {
        hunksText += entryText + '\n';
        totalChars += entryText.length + 1;
      } else {
        hunksText += '... (truncated)\n';
        break;
      }
    }
  } else if (diffResult.hunks) {
    // Use hunk-based diff
    for (const hunk of diffResult.hunks) {
      const header = `@@ -${hunk.startA},${hunk.endA - hunk.startA + 1} +${hunk.startB},${hunk.endB - hunk.startB + 1} @@\n`;
      if (totalChars + header.length > maxChars) break;
      hunksText += header;
      totalChars += header.length;

      for (const line of hunk.lines) {
        let lineText;
        if (line.type === 'equal') lineText = ' ' + line.text + '\n';
        else if (line.type === 'delete') lineText = '-' + line.text + '\n';
        else lineText = '+' + line.text + '\n';

        if (totalChars + lineText.length > maxChars) {
          hunksText += '... (truncated)\n';
          break;
        }
        hunksText += lineText;
        totalChars += lineText.length;
      }
    }
  } else {
    hunksText = '(empty diff)';
  }

  // Build the prompt
  const langHint = lang === 'auto' ? 'Auto-detect language based on content' :
    lang === 'zh-CN' ? 'Respond in Chinese (zh-CN)' : 'Respond in English (en-US)';

  const types = format === 'json' ? 'JSON' :
    format === 'csv' ? 'CSV/TSV' :
    format === 'yaml' ? 'YAML' :
    format === 'code' ? 'source code' :
    format === 'toml' ? 'TOML' :
    'text';

  const prompt = [
    `[System] You are a code/file review assistant. Analyze the following ${types} diff and explain in 2-4 sentences: what changed, why it might matter, and any notable patterns. ${langHint}`,
    '',
    `[Stats] Added: ${diffResult.stats?.lines_added || diffResult.stats?.fields_added || 0} | Deleted: ${diffResult.stats?.lines_deleted || diffResult.stats?.fields_deleted || 0} | Modified: ${diffResult.stats?.lines_modified || diffResult.stats?.fields_modified || 0}`,
    '',
    '[Diff]',
    hunksText,
    '',
    '[Analysis]',
  ].join('\n');

  return prompt;
}

/**
 * Generate AI explanation for a diff.
 * In skill context, the LLM invocation is handled by the platform.
 * This method prepares a structured prompt that can be passed to the AI.
 *
 * @param {object} diffResult - The result object from diff-engine
 * @param {object} [opts]
 * @param {string} [opts.language='auto']
 * @param {boolean} [opts.redactCredentials=true]
 * @returns {{ ok: boolean, prompt: string|null, explanation: string|null, summary: string|null, error: string|null }}
 */
function generateExplanation(diffResult, opts = {}) {
  const redact = opts.redactCredentials !== false;

  try {
    const prompt = buildExplainPrompt(diffResult, opts);
    const redactedPrompt = redact ? security.redactCredentials(prompt) : prompt;

    // Audit the request
    security.auditAiRequest(
      `${diffResult.labelA || '?'} ↔ ${diffResult.labelB || '?'}`,
      (diffResult.structured_diff || diffResult.hunks || []).length
    );

    // In the skill context, the platform handles LLM calls.
    // We provide the structured prompt and return heuristic explanations as fallback.
    const explanation = generateHeuristicExplanation(diffResult, opts.language);

    return {
      ok: true,
      prompt: redactedPrompt,
      explanation: explanation.text,
      summary: explanation.summary,
      error: null,
    };
  } catch (err) {
    return {
      ok: false,
      prompt: null,
      explanation: null,
      summary: null,
      error: `E007: AI explanation failed — ${err.message}`,
    };
  }
}

/**
 * Generate heuristic (rule-based) explanation as fallback when LLM is unavailable.
 * This provides useful AI-like explanations without LLM dependency.
 */
function generateHeuristicExplanation(diffResult, language = 'auto') {
  const isZh = language === 'zh-CN' || (language === 'auto' && detectChineseContent(diffResult));
  const stats = diffResult.stats || {};
  const format = diffResult.format_detected || 'text';
  const changes = diffResult.changes || [];

  const added = stats.lines_added || stats.fields_added || stats.rows_added || 0;
  const deleted = stats.lines_deleted || stats.fields_deleted || stats.rows_deleted || 0;
  const modified = stats.lines_modified || stats.fields_modified || stats.cells_modified || 0;

  let text, summary;

  if (diffResult.identical) {
    text = isZh
      ? '两个文件内容完全一致，没有任何差异。'
      : 'Both files are identical — no differences found.';
    summary = isZh ? '完全一致' : 'Identical';
  } else if (format === 'json') {
    if (isZh) {
      text = `共有 ${changes.length} 处 JSON 字段变更。新增 ${added} 个字段，删除 ${deleted} 个字段，修改 ${modified} 个字段。`;
      if (changes.length > 0) {
        const paths = changes.slice(0, 5).map(c => c.path).join('、');
        text += `涉及路径：${paths}${changes.length > 5 ? ' 等' : ''}。`;
      }
      summary = `JSON 结构变更：+${added} -${deleted} ~${modified}`;
    } else {
      text = `Found ${changes.length} JSON field changes. Added ${added}, deleted ${deleted}, modified ${modified}.`;
      if (changes.length > 0) {
        const paths = changes.slice(0, 5).map(c => c.path).join(', ');
        text += ` Affected paths: ${paths}${changes.length > 5 ? ', ...' : ''}.`;
      }
      summary = `JSON structure: +${added} -${deleted} ~${modified}`;
    }
  } else if (format === 'csv' || format === 'tsv') {
    if (isZh) {
      text = `数据表变更：新增 ${added} 行，删除 ${deleted} 行，修改 ${modified} 个单元格。`;
      if (modified > 0) {
        text += ' 建议使用 --detail-level detailed 查看具体变更值。';
      }
      summary = `CSV 变更：+${added}行 -${deleted}行 ~${modified}格`;
    } else {
      text = `Data table changes: ${added} rows added, ${deleted} rows deleted, ${modified} cells modified.`;
      if (modified > 0) {
        text += ' Use --detail-level detailed to see per-cell changes.';
      }
      summary = `CSV changes: +${added} rows -${deleted} rows ~${modified} cells`;
    }
  } else {
    // Text/code diff
    const total = added + deleted;
    if (isZh) {
      text = `共 ${total} 处变更：新增 ${added} 行，删除 ${deleted} 行。`;
      if (modified > 0) text += `其中 ${modified} 处为修改。`;
      if (format === 'code') text += ' 代码语义对比模式已启用，忽略纯空白变更和注释变更。';
      summary = `文本变更：+${added} -${deleted}`;
    } else {
      text = `Found ${total} changes: ${added} additions, ${deleted} deletions.`;
      if (modified > 0) text += ` ${modified} modifications detected.`;
      if (format === 'code') text += ' Semantic code diff enabled — whitespace-only and comment changes filtered.';
      summary = `Text diff: +${added} -${deleted}`;
    }
  }

  return { text, summary };
}

/**
 * Detect if diff content contains Chinese characters.
 */
function detectChineseContent(diffResult) {
  const texts = [
    diffResult.labelA || '',
    diffResult.labelB || '',
  ];

  for (const t of texts) {
    if (/[\u4e00-\u9fff]/.test(t)) return true;
  }

  // Check structured diff content
  if (diffResult.changes) {
    for (const c of diffResult.changes.slice(0, 10)) {
      const vals = [c.old_value, c.new_value].filter(Boolean).join(' ');
      if (/[\u4e00-\u9fff]/.test(vals)) return true;
    }
  }

  return false;
}

module.exports = {
  buildExplainPrompt,
  generateExplanation,
  generateHeuristicExplanation,
};
