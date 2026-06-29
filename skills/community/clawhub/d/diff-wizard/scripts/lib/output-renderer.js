/**
 * output-renderer.js — Multi-format output renderer for diff-wizard
 *
 * Renders diff results in terminal (color), markdown, HTML, unified, or JSON formats.
 */

'use strict';

const security = require('./security');

// ── ANSI Color Constants ──────────────────────────────────────────────
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
  bgGreen: '\x1b[42m',
  bgRed: '\x1b[41m',
  bgYellow: '\x1b[43m',
};

/**
 * Render diff result in terminal-friendly colored output.
 * @param {object} result - Result from diff-engine
 * @param {object} [opts]
 * @param {boolean} [opts.color=true]
 * @param {string} [opts.detailLevel='normal']
 * @returns {string}
 */
function renderTerminal(result, opts = {}) {
  const useColor = opts.color !== false;
  const c = (code, str) => useColor ? `${code}${str}${colors.reset}` : str;
  const detail = opts.detailLevel || 'normal';

  let output = '';

  // Header
  output += '\n' + c(colors.bold, '═'.repeat(55)) + '\n';
  const labelPair = `${result.labelA || 'Left'}  ↔  ${result.labelB || 'Right'}`;
  output += c(colors.bold, ` ${labelPair}`) + '\n';
  output += c(colors.bold, '═'.repeat(55)) + '\n';

  // Format info
  const formatLabel = result.format_detected || 'text';
  output += c(colors.dim, ` Format: ${formatLabel}`) + '\n';

  // Sensitive file warning
  if (result.sensitive_files && result.sensitive_files.length > 0) {
    output += '\n' + c(colors.yellow, ' ⚠ Sensitive files detected:') + '\n';
    for (const sf of result.sensitive_files) {
      output += c(colors.yellow, `   ${sf}`) + '\n';
    }
    output += '\n';
  }

  if (result.identical) {
    output += '\n' + c(colors.green, ' ✅ Files are identical') + '\n';
    if (result.format_detected === 'json') {
      output += c(colors.dim, '   All JSON fields match exactly.') + '\n';
    }
    return output;
  }

  // Stats summary
  const s = result.stats || {};
  const added = s.lines_added || s.fields_added || s.rows_added || 0;
  const deleted = s.lines_deleted || s.fields_deleted || s.rows_deleted || 0;
  const modified = s.lines_modified || s.fields_modified || s.cells_modified || 0;

  output += '\n' + c(colors.bold, ' 📊 Statistics:');
  output += ` Added ${c(colors.green, added)}`;
  output += ` | Deleted ${c(colors.red, deleted)}`;
  output += ` | Modified ${c(colors.yellow, modified)}`;
  output += ` | Total ${s.total_changes || (added + deleted)}`;
  output += '\n\n';

  if (detail === 'summary') {
    if (result.ai_explanation) {
      output += c(colors.cyan, ' 🤖 AI Explanation:') + '\n';
      output += `    ${result.ai_explanation}` + '\n';
    }
    return output;
  }

  // Render changes
  if (result.format_detected === 'json' && result.changes) {
    output += renderJsonChanges(result.changes, c, detail);
  } else if ((result.format_detected === 'csv' || result.format_detected === 'tsv') && result.changes) {
    output += renderCsvChanges(result.changes, c, detail);
  } else if (result.hunks) {
    output += renderHunks(result.hunks, c, detail);
  }

  // AI Explanation
  if (result.ai_explanation) {
    output += '\n' + c(colors.cyan, ' 🤖 AI Explanation:') + '\n';
    output += `    ${result.ai_explanation}` + '\n';
  }
  if (result.ai_summary) {
    output += '\n' + c(colors.dim, ` Summary: ${result.ai_summary}`) + '\n';
  }

  return output;
}

/**
 * Render JSON field-level changes.
 */
function renderJsonChanges(changes, c, detail) {
  let output = '';

  const added = changes.filter(ch => ch.type === 'added');
  const deleted = changes.filter(ch => ch.type === 'deleted');
  const modified = changes.filter(ch => ch.type === 'modified');

  if (deleted.length > 0) {
    output += ` ${c(colors.red, '🔴 Deleted fields:')}\n`;
    for (const d of deleted.slice(0, detail === 'detailed' ? 99 : 20)) {
      output += `    ${c(colors.red, '-')} ${d.path}: ${d.old_value}\n`;
    }
    if (deleted.length > 20 && detail !== 'detailed') {
      output += `    ${c(colors.dim, `... and ${deleted.length - 20} more`)}\n`;
    }
  }

  if (added.length > 0) {
    output += ` ${c(colors.green, '🟢 Added fields:')}\n`;
    for (const a of added.slice(0, detail === 'detailed' ? 99 : 20)) {
      output += `    ${c(colors.green, '+')} ${a.path}: ${a.new_value}\n`;
    }
    if (added.length > 20 && detail !== 'detailed') {
      output += `    ${c(colors.dim, `... and ${added.length - 20} more`)}\n`;
    }
  }

  if (modified.length > 0) {
    output += ` ${c(colors.yellow, '🟡 Modified fields:')}\n`;
    for (const m of modified.slice(0, detail === 'detailed' ? 99 : 20)) {
      output += `    ${c(colors.yellow, '~')} ${m.path}: ${m.old_value} → ${m.new_value}\n`;
    }
    if (modified.length > 20 && detail !== 'detailed') {
      output += `    ${c(colors.dim, `... and ${modified.length - 20} more`)}\n`;
    }
  }

  return output;
}

/**
 * Render CSV changes.
 */
function renderCsvChanges(changes, c, detail) {
  let output = '';

  const added = changes.filter(ch => ch.type === 'added');
  const deleted = changes.filter(ch => ch.type === 'deleted');
  const modified = changes.filter(ch => ch.type === 'modified');

  if (added.length > 0) {
    output += ` ${c(colors.green, '🟢 Added rows:')} ${added.length}\n`;
  }
  if (deleted.length > 0) {
    output += ` ${c(colors.red, '🔴 Deleted rows:')} ${deleted.length}\n`;
  }
  if (modified.length > 0) {
    output += ` ${c(colors.yellow, '🟡 Modified cells:')} ${modified.length}\n`;
    if (detail === 'detailed') {
      for (const m of modified.slice(0, 30)) {
        output += `    ${c(colors.yellow, '~')} ${m.path}: "${m.old_value}" → "${m.new_value}"\n`;
      }
      if (modified.length > 30) {
        output += `    ${c(colors.dim, `... and ${modified.length - 30} more cells`)}\n`;
      }
    }
  }

  return output;
}

/**
 * Render hunk-based diff (text/code).
 */
function renderHunks(hunks, c, detail) {
  let output = '';

  for (const hunk of hunks) {
    if (detail === 'summary') continue;

    output += ` ${c(colors.dim, `@@ -${hunk.startA},${hunk.endA - hunk.startA + 1} +${hunk.startB},${hunk.endB - hunk.startB + 1} @@`)}\n`;

    for (const line of hunk.lines) {
      if (line.type === 'equal' && detail !== 'detailed') continue;

      if (line.type === 'equal') {
        output += `  ${c(colors.dim, line.text)}\n`;
      } else if (line.type === 'delete') {
        output += ` ${c(colors.red, '-')}${c(colors.red, line.text)}\n`;
      } else if (line.type === 'insert') {
        output += ` ${c(colors.green, '+')}${c(colors.green, line.text)}\n`;
      }
    }
  }

  return output;
}

/**
 * Render diff result as markdown.
 * @param {object} result
 * @returns {string}
 */
function renderMarkdown(result) {
  let md = `# Diff Report\n\n`;
  md += `**Compare**: \`${result.labelA || 'Left'}\` ↔ \`${result.labelB || 'Right'}\`\n\n`;
  md += `**Format**: ${result.format_detected || 'text'}\n\n`;

  if (result.identical) {
    md += `> ✅ Files are identical\n\n`;
    return md;
  }

  const s = result.stats || {};
  md += `## Statistics\n\n`;
  md += `| Metric | Value |\n|--------|-------|\n`;
  md += `| Added | ${s.lines_added || s.fields_added || s.rows_added || 0} |\n`;
  md += `| Deleted | ${s.lines_deleted || s.fields_deleted || s.rows_deleted || 0} |\n`;
  md += `| Modified | ${s.lines_modified || s.fields_modified || s.cells_modified || 0} |\n`;
  md += `| Total | ${s.total_changes || 0} |\n\n`;

  if (result.changes && result.changes.length > 0) {
    md += `## Changes\n\n`;

    const added = result.changes.filter(c => c.type === 'added');
    const deleted = result.changes.filter(c => c.type === 'deleted');
    const modified = result.changes.filter(c => c.type === 'modified');

    if (deleted.length > 0) {
      md += `### Deleted\n\n`;
      for (const d of deleted) {
        md += `- \`${d.path}\`: ~~${d.old_value}~~\n`;
      }
      md += '\n';
    }
    if (added.length > 0) {
      md += `### Added\n\n`;
      for (const a of added) {
        md += `- \`${a.path}\`: **${a.new_value}**\n`;
      }
      md += '\n';
    }
    if (modified.length > 0) {
      md += `### Modified\n\n`;
      for (const m of modified) {
        md += `- \`${m.path}\`: \`${m.old_value}\` → \`${m.new_value}\`\n`;
      }
      md += '\n';
    }
  }

  if (result.ai_explanation) {
    md += `## AI Explanation\n\n${result.ai_explanation}\n\n`;
  }

  if (result.ai_summary) {
    md += `> **Summary**: ${result.ai_summary}\n\n`;
  }

  return md;
}

/**
 * Render diff result as HTML.
 * @param {object} result
 * @returns {string}
 */
function renderHTML(result) {
  const sanitize = (str) => security.sanitizeHtml(String(str || ''));
  let html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diff Report — ${sanitize(result.labelA)} ↔ ${sanitize(result.labelB)}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 960px; margin: 0 auto; padding: 20px; background: #0d1117; color: #c9d1d9; }
  h1 { border-bottom: 1px solid #30363d; padding-bottom: 8px; }
  .stats { display: flex; gap: 16px; margin: 16px 0; }
  .stat { padding: 8px 16px; border-radius: 6px; background: #161b22; border: 1px solid #30363d; }
  .stat-added { border-left: 3px solid #3fb950; }
  .stat-deleted { border-left: 3px solid #f85149; }
  .stat-modified { border-left: 3px solid #d29922; }
  .stat-value { font-size: 1.4em; font-weight: bold; }
  .stat-label { font-size: 0.85em; color: #8b949e; }
  .change { padding: 4px 8px; font-family: 'SF Mono', Monaco, monospace; font-size: 13px; }
  .change-added { background: rgba(63,185,80,0.15); color: #3fb950; }
  .change-deleted { background: rgba(248,81,73,0.15); color: #f85149; }
  .change-modified { background: rgba(210,153,34,0.15); color: #d29922; }
  .ai-explanation { padding: 12px 16px; background: #161b22; border-radius: 6px; margin: 16px 0; border: 1px solid #30363d; }
  .ai-summary { color: #8b949e; font-style: italic; }
  table { border-collapse: collapse; width: 100%; margin: 8px 0; }
  th, td { border: 1px solid #30363d; padding: 6px 12px; text-align: left; }
  th { background: #161b22; }
  .identical { color: #3fb950; font-size: 1.2em; }
</style>
</head>
<body>
<h1>📄 Diff Report: ${sanitize(result.labelA)} ↔ ${sanitize(result.labelB)}</h1>
<p>Format: <strong>${sanitize(result.format_detected || 'text')}</strong></p>
`;

  if (result.identical) {
    html += '<p class="identical">✅ Files are identical</p>';
  } else {
    const s = result.stats || {};
    html += `<div class="stats">
      <div class="stat stat-added"><div class="stat-value">+${s.lines_added || s.fields_added || s.rows_added || 0}</div><div class="stat-label">Added</div></div>
      <div class="stat stat-deleted"><div class="stat-value">-${s.lines_deleted || s.fields_deleted || s.rows_deleted || 0}</div><div class="stat-label">Deleted</div></div>
      <div class="stat stat-modified"><div class="stat-value">~${s.lines_modified || s.fields_modified || s.cells_modified || 0}</div><div class="stat-label">Modified</div></div>
    </div>`;

    if (result.changes && result.changes.length > 0) {
      html += '<table><thead><tr><th>Type</th><th>Path</th><th>Old Value</th><th>New Value</th></tr></thead><tbody>';
      for (const ch of result.changes) {
        const cls = ch.type === 'added' ? 'change-added' : ch.type === 'deleted' ? 'change-deleted' : 'change-modified';
        html += `<tr class="change ${cls}">
          <td>${ch.type === 'added' ? '🟢 +' : ch.type === 'deleted' ? '🔴 -' : '🟡 ~'}</td>
          <td>${sanitize(ch.path)}</td>
          <td>${sanitize(String(ch.old_value != null ? ch.old_value : ''))}</td>
          <td>${sanitize(String(ch.new_value != null ? ch.new_value : ''))}</td>
        </tr>`;
      }
      html += '</tbody></table>';
    }
  }

  if (result.ai_explanation) {
    html += `<div class="ai-explanation"><strong>🤖 AI Explanation</strong><p>${sanitize(result.ai_explanation)}</p></div>`;
  }

  html += '</body></html>';
  return html;
}

/**
 * Render diff result as JSON.
 * @param {object} result
 * @returns {string}
 */
function renderJSON(result) {
  const output = {
    meta: {
      mode: result.fileA ? 'file-diff' : 'content-diff',
      format_detected: result.format_detected || 'text',
      left_label: result.labelA || 'left',
      right_label: result.labelB || 'right',
      timestamp: new Date().toISOString(),
    },
    diff: {
      identical: result.identical || false,
      stats: result.stats || {},
      changes: result.changes || [],
      ai_explanation: result.ai_explanation || null,
      ai_summary: result.ai_summary || null,
    },
  };

  return JSON.stringify(output, null, 2);
}

/**
 * Render diff result as unified diff string.
 * @param {object} result
 * @returns {string}
 */
function renderUnified(result) {
  if (result.identical) {
    return '';
  }
  if (result.unified) return result.unified;
  if (result.changes && result.changes.length > 0) {
    let lines = [];
    lines.push('--- ' + (result.labelA || 'left'));
    lines.push('+++ ' + (result.labelB || 'right'));
    lines.push('');
    for (const ch of result.changes) {
      if (ch.type === 'added') {
        lines.push('+ ' + ch.path + ': ' + (ch.new_value || ''));
      } else if (ch.type === 'deleted') {
        lines.push('- ' + ch.path + ': ' + (ch.old_value || ''));
      } else if (ch.type === 'modified') {
        lines.push('- ' + ch.path + ': ' + (ch.old_value || ''));
        lines.push('+ ' + ch.path + ': ' + (ch.new_value || ''));
      }
    }
    return lines.join("\n");
  }
  return '';
}

/**
 * Render merge result in terminal.
 * @param {object} mergeResult - Result from three-way-merger
 * @param {object} [opts]
 * @param {boolean} [opts.color=true]
 * @returns {string}
 */
function renderMergeResult(mergeResult, opts = {}) {
  const useColor = opts.color !== false;
  const c = (code, str) => useColor ? `${code}${str}${colors.reset}` : str;

  let output = '';
  output += '\n' + c(colors.bold, '═'.repeat(55)) + '\n';
  output += c(colors.bold, ' 🔀 3-Way Merge Result') + '\n';
  output += c(colors.bold, '═'.repeat(55)) + '\n';

  if (mergeResult.hasConflicts) {
    output += `\n ${c(colors.yellow, `⚠ ${mergeResult.conflictCount} conflict(s) found`)}`;
    if (mergeResult.autoResolvedCount > 0) {
      output += ` (${c(colors.green, `${mergeResult.autoResolvedCount} auto-resolved`)})`;
    }
    output += '\n\n';

    if (mergeResult.conflictOverflow) {
      output += ` ${c(colors.red, '⚠ Conflict overflow (>100). Manual review recommended.')}\n\n`;
    }

    for (const conflict of mergeResult.conflicts) {
      output += ` ${c(colors.yellow, `⚠ Conflict: ${conflict.location}`)}\n`;
      output += `  ${c(colors.red, '  <<<<<<< ours')}\n`;
      for (const line of conflict.ours.split('\n')) {
        if (line) output += `  ${c(colors.red, line)}\n`;
      }
      output += `  ${c(colors.yellow, '  =======')}\n`;
      for (const line of conflict.theirs.split('\n')) {
        if (line) output += `  ${c(colors.green, line)}\n`;
      }
      output += `  ${c(colors.blue, '  >>>>>>> theirs')}\n`;

      if (conflict.ai_suggestion) {
        output += `  ${c(colors.cyan, '🤖 AI suggestion:')} ${conflict.ai_suggestion}\n`;
      }
      output += '\n';
    }
  } else {
    output += `\n ${c(colors.green, '✅ All changes merged successfully')}`;
    if (mergeResult.autoResolvedCount > 0) {
      output += ` (${mergeResult.autoResolvedCount} auto-resolved)`;
    }
    output += '\n';
  }

  return output;
}

/**
 * Main render function — routes to the appropriate renderer.
 * @param {object} result - Result from diff-engine or three-way-merger
 * @param {string} [outputFormat='terminal']
 * @param {object} [opts]
 * @returns {string}
 */
function render(result, outputFormat = 'terminal', opts = {}) {
  switch (outputFormat) {
    case 'unified':
      return renderUnified(result);
    case 'markdown':
      return renderMarkdown(result);
    case 'html':
      return renderHTML(result);
    case 'json':
      return renderJSON(result);
    case 'side-by-side':
      // Fallback to terminal for side-by-side (true side-by-side needs TUI)
      return renderTerminal(result, opts) + '\n(Side-by-side mode: use terminal or HTML for visual comparison)';
    case 'terminal':
    default:
      return renderTerminal(result, opts);
  }
}

module.exports = {
  render,
  renderTerminal,
  renderMarkdown,
  renderHTML,
  renderJSON,
  renderUnified,
  renderMergeResult,
};
