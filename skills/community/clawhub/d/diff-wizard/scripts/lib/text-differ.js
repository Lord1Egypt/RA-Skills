/**
 * text-differ.js — Plain text unified diff implementation
 *
 * Implements Myers diff algorithm for line-level comparison,
 * producing standard unified diff format output.
 */

'use strict';

/**
 * Myers diff algorithm — compute shortest edit script between two arrays of lines.
 * Returns a list of operations: { type: 'equal'|'insert'|'delete', line: string, oldLine?: number, newLine?: number }
 *
 * Implementation based on the standard Myers O(ND) algorithm.
 */
function myersDiff(a, b) {
  const n = a.length;
  const m = b.length;
  const max = n + m;

  const v = new Int32Array(2 * max + 1);
  const trace = [];

  // Build trace
  for (let d = 0; d <= max; d++) {
    trace.push(new Int32Array(v));

    for (let k = -d; k <= d; k += 2) {
      const idx = k + max;
      let x;
      if (k === -d || (k !== d && v[idx - 1] < v[idx + 1])) {
        x = v[idx + 1];
      } else {
        x = v[idx - 1] + 1;
      }

      let y = x - k;

      // Move diagonally
      while (x < n && y < m && a[x] === b[y]) {
        x++;
        y++;
      }

      v[idx] = x;

      if (x >= n && y >= m) {
        // Done, reconstruct path
        return backtrack(a, b, trace, max, d);
      }
    }
  }

  // Fallback (shouldn't reach here in practice)
  return simpleDiff(a, b);
}

function backtrack(a, b, trace, max, d) {
  const ops = [];
  let x = a.length;
  let y = b.length;

  for (let d2 = d; d2 > 0; d2--) {
    const v = trace[d2];
    const k = x - y;
    const idx = k + max;

    // Which move got us here?
    let prevK;
    if (k === -d2 || (k !== d2 && v[idx - 1] < v[idx + 1])) {
      prevK = k + 1;
    } else {
      prevK = k - 1;
    }

    const prevIdx = prevK + max;
    const prevX = v[prevIdx];
    const prevY = prevX - prevK;

    // Walk diagonals backwards
    while (x > prevX && y > prevY) {
      ops.push({ type: 'equal', line: a[x - 1], oldLine: x, newLine: y });
      x--;
      y--;
    }

    if (x > prevX) {
      ops.push({ type: 'delete', line: a[x - 1], oldLine: x });
      x--;
    } else if (y > prevY) {
      ops.push({ type: 'insert', line: b[y - 1], newLine: y });
      y--;
    }
  }

  // Remaining equal lines
  while (x > 0 && y > 0) {
    ops.push({ type: 'equal', line: a[x - 1], oldLine: x, newLine: y });
    x--;
    y--;
  }

  ops.reverse();
  return ops;
}

/**
 * Simple fallback diff when Myers is impractical (e.g., very large inputs).
 */
function simpleDiff(a, b) {
  const ops = [];
  const commonLen = Math.min(a.length, b.length);

  for (let i = 0; i < commonLen; i++) {
    if (a[i] === b[i]) {
      ops.push({ type: 'equal', line: a[i], oldLine: i + 1, newLine: i + 1 });
    } else {
      ops.push({ type: 'delete', line: a[i], oldLine: i + 1 });
      ops.push({ type: 'insert', line: b[i], newLine: i + 1 });
    }
  }

  for (let i = commonLen; i < a.length; i++) {
    ops.push({ type: 'delete', line: a[i], oldLine: i + 1 });
  }
  for (let i = commonLen; i < b.length; i++) {
    ops.push({ type: 'insert', line: b[i], newLine: i + 1 });
  }

  return ops;
}

/**
 * Generate unified diff string from two texts.
 * @param {string} textA - Original text
 * @param {string} textB - Modified text
 * @param {object} [opts]
 * @param {string} [opts.labelA='a']
 * @param {string} [opts.labelB='b']
 * @param {number} [opts.contextLines=3]
 * @param {boolean} [opts.ignoreWhitespace=false]
 * @param {boolean} [opts.ignoreCase=false]
 * @returns {{ unified: string, stats: object, hunks: object[] }}
 */
function unifiedDiff(textA, textB, opts = {}) {
  const ctx = opts.contextLines !== undefined ? opts.contextLines : 3;
  const labelA = opts.labelA || 'a';
  const labelB = opts.labelB || 'b';

  let linesA = textA.split('\n');
  let linesB = textB.split('\n');

  // Normalize trailing newline
  if (textA.endsWith('\n')) linesA = linesA.slice(0, -1);
  if (textB.endsWith('\n')) linesB = linesB.slice(0, -1);

  // Apply ignore options
  if (opts.ignoreWhitespace) {
    linesA = linesA.map(l => l.replace(/\s+/g, ' ').trimEnd());
    linesB = linesB.map(l => l.replace(/\s+/g, ' ').trimEnd());
  }
  if (opts.ignoreCase) {
    linesA = linesA.map(l => l.toLowerCase());
    linesB = linesB.map(l => l.toLowerCase());
  }

  const ops = myersDiff(linesA, linesB);

  // Build hunks
  const hunks = [];
  let hunk = null;
  let added = 0, deleted = 0;

  for (let i = 0; i < ops.length; i++) {
    const op = ops[i];

    if (op.type === 'equal') {
      if (hunk) {
        hunk.after++;
        hunk.lines.push({ type: 'equal', text: op.line, oldLine: op.oldLine, newLine: op.newLine });

        // Check if we have enough trailing context to close the hunk
        if (hunk.after > ctx) {
          // Trim the trailing context
          hunk.lines = hunk.lines.slice(0, -(hunk.after - ctx));
          hunk.after = ctx;
          hunk.endA = hunk.after > 0 ? ops[i - (hunk.after)].oldLine || 0 : hunk.startA + hunk.before;
          hunk.endB = hunk.after > 0 ? ops[i - (hunk.after)].newLine || 0 : hunk.startB + hunk.before;
          hunks.push(hunk);
          hunk = null;
        }
      }
    } else {
      if (!hunk) {
        // Start a new hunk: include preceding context
        hunk = {
          startA: Math.max(1, (op.oldLine || 0) - ctx),
          startB: Math.max(1, (op.newLine || 0) - ctx),
          before: 0,
          after: 0,
          endA: op.oldLine || 0,
          endB: op.newLine || 0,
          lines: [],
        };

        // Add preceding equal lines as context
        const ctxBefore = ops.slice(Math.max(0, i - ctx), i);
        for (const c of ctxBefore) {
          if (c.type === 'equal') {
            hunk.lines.push({ type: 'equal', text: c.line, oldLine: c.oldLine, newLine: c.newLine });
            hunk.before++;
          }
        }
      }

      if (op.type === 'delete') {
        hunk.lines.push({ type: 'delete', text: op.line, oldLine: op.oldLine });
        hunk.endA = op.oldLine || 0;
        deleted++;
      } else if (op.type === 'insert') {
        hunk.lines.push({ type: 'insert', text: op.line, newLine: op.newLine });
        hunk.endB = op.newLine || 0;
        added++;
      }

      hunk.after = 0;

      // Check if this is the last operation
      if (i === ops.length - 1) {
        hunks.push(hunk);
      }
    }
  }

  // Close any remaining open hunk
  if (hunk) {
    hunks.push(hunk);
  }

  // If no hunks, files are identical
  if (hunks.length === 0) {
    return {
      unified: '',
      stats: { lines_added: 0, lines_deleted: 0, lines_modified: 0, total_changes: 0 },
      identical: true,
      hunks: [],
    };
  }

  // Build unified diff string
  let output = `--- ${labelA}\n+++ ${labelB}\n`;
  for (const h of hunks) {
    const lenA = h.endA - h.startA + 1;
    const lenB = h.endB - h.startB + 1;
    output += `@@ -${h.startA},${lenA} +${h.startB},${lenB} @@\n`;

    for (const line of h.lines) {
      if (line.type === 'equal') output += ' ' + line.text + '\n';
      else if (line.type === 'delete') output += '-' + line.text + '\n';
      else if (line.type === 'insert') output += '+' + line.text + '\n';
    }
  }

  return {
    unified: output,
    stats: {
      lines_added: added,
      lines_deleted: deleted,
      lines_modified: Math.min(added, deleted),
      total_changes: added + deleted,
    },
    identical: false,
    hunks,
  };
}

/**
 * Quick text comparison returning only stats.
 * @param {string} textA
 * @param {string} textB
 * @returns {{ identical: boolean, stats: object }}
 */
function quickCompare(textA, textB) {
  if (textA === textB) {
    return {
      identical: true,
      stats: { lines_added: 0, lines_deleted: 0, lines_modified: 0, total_changes: 0 },
    };
  }

  const result = unifiedDiff(textA, textB, { contextLines: 0 });
  return {
    identical: false,
    stats: result.stats,
  };
}

module.exports = {
  unifiedDiff,
  quickCompare,
  myersDiff,
};
