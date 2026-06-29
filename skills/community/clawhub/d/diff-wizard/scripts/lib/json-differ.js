/**
 * json-differ.js — JSON structured comparison engine
 *
 * Performs field-level comparison of JSON objects with recursive
 * depth-first traversal and key-aligned diffing.
 */

'use strict';

/**
 * Parse JSON string safely.
 * @param {string} content
 * @param {string} [label='input']
 * @returns {{ ok: boolean, data: any|null, error: string|null }}
 */
function parseJSON(content, label = 'input') {
  try {
    const data = JSON.parse(content);
    return { ok: true, data, error: null };
  } catch (err) {
    // Try to extract line:col from error message
    const msg = err.message || '';
    const posMatch = msg.match(/position\s+(\d+)/i);
    if (posMatch) {
      const pos = parseInt(posMatch[1], 10);
      const before = content.slice(0, pos);
      const line = (before.match(/\n/g) || []).length + 1;
      const col = pos - before.lastIndexOf('\n');
      return {
        ok: false,
        data: null,
        error: `E006: JSON parse error at ${label}:${line}:${col} — ${msg}`,
      };
    }
    return { ok: false, data: null, error: `E006: JSON parse error in ${label} — ${msg}` };
  }
}

/**
 * Recursively diff two values, producing structured diff entries.
 * @param {any} oldVal
 * @param {any} newVal
 * @param {string} [keyPath=''] - Current key path (e.g., 'config.database.host')
 * @param {object} [opts]
 * @param {boolean} [opts.sortKeys=false]
 * @param {number} [opts.maxDepth=50]
 * @param {number} [opts._depth=0] - Internal depth counter
 * @returns {Array<{type: string, path: string, old_value: any, new_value: any}>}
 */
function diffValues(oldVal, newVal, keyPath = '', opts = {}) {
  const depth = opts._depth || 0;
  const maxDepth = opts.maxDepth || 50;
  const changes = [];

  if (depth > maxDepth) {
    changes.push({
      type: 'modified',
      path: keyPath || '(root)',
      old_value: '(truncated: depth > ' + maxDepth + ')',
      new_value: '(truncated: depth > ' + maxDepth + ')',
      context: 'Depth limit exceeded, values truncated',
    });
    return changes;
  }

  // Type mismatch
  if (typeof oldVal !== typeof newVal) {
    changes.push({
      type: 'modified',
      path: keyPath || '(root)',
      old_value: formatValue(oldVal),
      new_value: formatValue(newVal),
      context: `Type changed: ${typeof oldVal} → ${typeof newVal}`,
    });
    return changes;
  }

  // Both null / undefined
  if (oldVal == null && newVal == null) return changes;
  if (oldVal == null) {
    changes.push({ type: 'added', path: keyPath || '(root)', old_value: null, new_value: formatValue(newVal) });
    return changes;
  }
  if (newVal == null) {
    changes.push({ type: 'deleted', path: keyPath || '(root)', old_value: formatValue(oldVal), new_value: null });
    return changes;
  }

  // Primitives
  if (typeof oldVal !== 'object' && typeof newVal !== 'object') {
    if (oldVal !== newVal) {
      changes.push({
        type: 'modified',
        path: keyPath || '(root)',
        old_value: formatValue(oldVal),
        new_value: formatValue(newVal),
      });
    }
    return changes;
  }

  // Arrays
  if (Array.isArray(oldVal) || Array.isArray(newVal)) {
    if (!Array.isArray(oldVal) || !Array.isArray(newVal)) {
      changes.push({
        type: 'modified',
        path: keyPath || '(root)',
        old_value: formatValue(oldVal),
        new_value: formatValue(newVal),
        context: 'Array vs non-array type change',
      });
      return changes;
    }

    // Compare arrays element by element
    const maxLen = Math.max(oldVal.length, newVal.length);
    for (let i = 0; i < maxLen; i++) {
      const itemPath = keyPath ? `${keyPath}[${i}]` : `[${i}]`;
      if (i >= oldVal.length) {
        changes.push({ type: 'added', path: itemPath, old_value: null, new_value: formatValue(newVal[i]) });
      } else if (i >= newVal.length) {
        changes.push({ type: 'deleted', path: itemPath, old_value: formatValue(oldVal[i]), new_value: null });
      } else {
        changes.push(...diffValues(oldVal[i], newVal[i], itemPath, { ...opts, _depth: depth + 1 }));
      }
    }
    return changes;
  }

  // Objects
  if (typeof oldVal === 'object' && typeof newVal === 'object') {
    const oldKeys = Object.keys(oldVal);
    const newKeys = Object.keys(newVal);
    const allKeys = opts.sortKeys
      ? [...new Set([...oldKeys, ...newKeys])].sort()
      : [...new Set([...oldKeys, ...newKeys])];

    for (const key of allKeys) {
      const childPath = keyPath ? `${keyPath}.${key}` : key;

      if (!(key in oldVal)) {
        changes.push({ type: 'added', path: childPath, old_value: null, new_value: formatValue(newVal[key]) });
      } else if (!(key in newVal)) {
        changes.push({ type: 'deleted', path: childPath, old_value: formatValue(oldVal[key]), new_value: null });
      } else {
        changes.push(...diffValues(oldVal[key], newVal[key], childPath, { ...opts, _depth: depth + 1 }));
      }
    }
  }

  return changes;
}

/**
 * Format a value for display in diff output.
 */
function formatValue(val) {
  if (val === null || val === undefined) return 'null';
  if (typeof val === 'string') {
    if (val.length > 80) return `"${val.slice(0, 77)}..."`;
    return `"${val}"`;
  }
  if (typeof val === 'object') {
    if (Array.isArray(val)) return `[Array(${val.length})]`;
    return `{Object}`;
  }
  return String(val);
}

/**
 * Full JSON comparison.
 * @param {string} jsonA - First JSON string
 * @param {string} jsonB - Second JSON string
 * @param {string} [labelA='left']
 * @param {string} [labelB='right']
 * @param {object} [opts]
 * @returns {{ ok: boolean, identical: boolean, changes: Array, stats: object, error: string|null }}
 */
function compareJSON(jsonA, jsonB, labelA = 'left', labelB = 'right', opts = {}) {
  const parseA = parseJSON(jsonA, labelA);
  if (!parseA.ok) return { ok: false, identical: false, changes: [], stats: null, error: parseA.error };

  const parseB = parseJSON(jsonB, labelB);
  if (!parseB.ok) return { ok: false, identical: false, changes: [], stats: null, error: parseB.error };

  // Quick identity check via JSON.stringify
  if (jsonA === jsonB) {
    return { ok: true, identical: true, changes: [], stats: { fields_added: 0, fields_deleted: 0, fields_modified: 0, total_changes: 0 }, error: null };
  }

  const changes = diffValues(parseA.data, parseB.data, '', {
    sortKeys: opts.sortKeys || false,
    maxDepth: opts.maxDepth || 50,
  });

  const stats = {
    fields_added: changes.filter(c => c.type === 'added').length,
    fields_deleted: changes.filter(c => c.type === 'deleted').length,
    fields_modified: changes.filter(c => c.type === 'modified').length,
    total_changes: changes.length,
  };

  return { ok: true, identical: changes.length === 0, changes, stats, error: null };
}

module.exports = {
  parseJSON,
  diffValues,
  compareJSON,
};
