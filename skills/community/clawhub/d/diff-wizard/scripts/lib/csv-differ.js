/**
 * csv-differ.js — CSV/TSV row-column comparison engine
 *
 * Compares CSV data at the row and column level, identifying
 * which row and which column changed.
 */

'use strict';

/**
 * Parse CSV string into rows of arrays.
 * Handles basic CSV (no embedded newlines in quoted fields for simplicity).
 * @param {string} content
 * @returns {{ ok: boolean, headers: string[], rows: string[][], error: string|null }}
 */
function parseCSV(content) {
  try {
    const lines = content.trim().split('\n');
    if (lines.length === 0) {
      return { ok: false, headers: [], rows: [], error: 'E004: Empty CSV content' };
    }

    // Parse headers from first line
    const headers = parseLine(lines[0]);
    const rows = [];

    for (let i = 1; i < lines.length; i++) {
      const row = parseLine(lines[i]);
      if (row.length > 0) {
        rows.push(row);
      }
    }

    return { ok: true, headers, rows, error: null };
  } catch (err) {
    return { ok: false, headers: [], rows: [], error: `E010: CSV parse error — ${err.message}` };
  }
}

/**
 * Parse a single CSV/TSV line into fields.
 * Supports quoted fields with commas inside.
 */
function parseLine(line) {
  const fields = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      fields.push(current.trim());
      current = '';
    } else {
      current += ch;
    }
  }
  fields.push(current.trim());
  return fields;
}

/**
 * Check if content is tab-separated.
 */
function isTSV(content) {
  const lines = content.trim().split('\n');
  if (lines.length < 2) return false;
  return lines[0].includes('\t') && !lines[0].includes(',');
}

/**
 * Parse TSV (tab-separated) content.
 */
function parseTSV(content) {
  try {
    const lines = content.trim().split('\n');
    if (lines.length === 0) {
      return { ok: false, headers: [], rows: [], error: 'E004: Empty TSV content' };
    }
    const headers = lines[0].split('\t').map(h => h.trim());
    const rows = lines.slice(1).map(line => line.split('\t').map(f => f.trim()));
    return { ok: true, headers, rows, error: null };
  } catch (err) {
    return { ok: false, headers: [], rows: [], error: `E010: TSV parse error — ${err.message}` };
  }
}

/**
 * Compare two CSV/TSV datasets.
 * @param {string} csvA - First CSV string
 * @param {string} csvB - Second CSV string
 * @param {object} [opts]
 * @param {string} [opts.labelA='left']
 * @param {string} [opts.labelB='right']
 * @param {string|null} [opts.keyColumn=null] - Column name/idx for row key (for alignment)
 * @returns {object}
 */
function compareCSV(csvA, csvB, opts = {}) {
  const labelA = opts.labelA || 'left';
  const labelB = opts.labelB || 'right';

  // Detect TSV vs CSV
  const isTsv = isTSV(csvA) && isTSV(csvB);
  const parser = isTsv ? parseTSV : parseCSV;

  const resultA = parser(csvA);
  if (!resultA.ok) return { ok: false, identical: false, changes: [], stats: null, error: resultA.error };

  const resultB = parser(csvB);
  if (!resultB.ok) return { ok: false, identical: false, changes: [], stats: null, error: resultB.error };

  // Build header map
  const headerMapA = {};
  const headerMapB = {};
  resultA.headers.forEach((h, i) => headerMapA[h] = i);
  resultB.headers.forEach((h, i) => headerMapB[h] = i);

  // Quick identity check
  if (csvA === csvB) {
    return {
      ok: true, identical: true, changes: [],
      stats: { rows_added: 0, rows_deleted: 0, cells_modified: 0, total_changes: 0 },
      headers: resultA.headers, error: null,
    };
  }

  const changes = [];
  const maxRows = Math.max(resultA.rows.length, resultB.rows.length);

  for (let i = 0; i < maxRows; i++) {
    const rowNum = i + 1; // 1-indexed for display

    if (i >= resultA.rows.length) {
      // Row added in B
      changes.push({
        type: 'added',
        path: `Row ${rowNum}`,
        old_value: null,
        new_value: resultB.rows[i].join(', '),
        context: 'New row',
      });
    } else if (i >= resultB.rows.length) {
      // Row deleted in B
      changes.push({
        type: 'deleted',
        path: `Row ${rowNum}`,
        old_value: resultA.rows[i].join(', '),
        new_value: null,
        context: 'Deleted row',
      });
    } else {
      // Compare cells in row
      const oldRow = resultA.rows[i];
      const newRow = resultB.rows[i];
      const maxCols = Math.max(oldRow.length, newRow.length);

      for (let j = 0; j < maxCols; j++) {
        const colName = resultA.headers[j] || `Col${j + 1}`;
        const oldVal = j < oldRow.length ? oldRow[j] : '';
        const newVal = j < newRow.length ? newRow[j] : '';

        if (oldVal !== newVal) {
          changes.push({
            type: 'modified',
            path: `[Row ${rowNum}, "${colName}"]`,
            old_value: oldVal,
            new_value: newVal,
            context: `Col ${j + 1} (${colName})`,
          });
        }
      }
    }
  }

  const stats = {
    rows_added: Math.max(0, resultB.rows.length - resultA.rows.length),
    rows_deleted: Math.max(0, resultA.rows.length - resultB.rows.length),
    cells_modified: changes.filter(c => c.type === 'modified').length,
    total_changes: changes.length,
  };

  return {
    ok: true,
    identical: changes.length === 0,
    changes,
    stats,
    headers: resultA.headers,
    error: null,
  };
}

module.exports = {
  parseCSV,
  compareCSV,
  isTSV,
};
