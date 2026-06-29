/**
 * Minimal YAML-ish frontmatter parser for EU files.
 *
 * Shared by lifecycle.js, validator.js, generator.js, evolver-cli.js,
 * brief-data.js. Before lib extraction each had its own variant with
 * slightly different handling of arrays / quotes / booleans, which
 * caused reader-specific bugs. This implementation is the superset.
 *
 * Supports:
 *   - key: value            (string)
 *   - key: "quoted value"   (strips double quotes)
 *   - key: 'quoted value'   (strips single quotes)
 *   - key: [a, b, c]        (JSON array; safe-fails back to string on parse error)
 *   - key: true | false     (boolean)
 *
 * Does NOT support: multi-line values, nested objects, block scalars.
 * EU frontmatter is flat by design.
 *
 * ─── Schema Version ───────────────────────────────────────────
 *
 * EU frontmatter carries a `schema: N` field since v2.4.1 (2026-04-21).
 * This is an internal compatibility anchor for skill-evolver dev, not
 * something end users need to track. Readers should default to 1 when
 * the field is missing (EUs written before v2.4.1).
 *
 *   CURRENT_SCHEMA_VERSION = 2
 *     - v1 (implicit): EUs written before 2026-04-21; no `schema` field
 *     - v2: EUs written by writeFrontmatter or new generator prompts
 *
 * Use getSchemaVersion(fm) to read. When future schema changes land,
 * bump CURRENT_SCHEMA_VERSION and branch in readers as needed.
 */

const CURRENT_SCHEMA_VERSION = 2;

function getSchemaVersion(fm) {
  if (!fm) return 1;
  const raw = fm.schema;
  if (raw === undefined || raw === null || raw === '') return 1;
  const n = typeof raw === 'number' ? raw : parseInt(String(raw), 10);
  return Number.isFinite(n) && n >= 1 ? n : 1;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};

  const fm = {};
  for (const line of match[1].split('\n')) {
    const colon = line.indexOf(':');
    if (colon <= 0) continue;

    const key = line.substring(0, colon).trim();
    let val = line.substring(colon + 1).trim();

    // JSON array
    if (val.startsWith('[')) {
      try { val = JSON.parse(val); } catch { /* keep as string */ }
    }

    // Quoted strings (both double and single)
    if (typeof val === 'string') {
      if (val.startsWith('"') && val.endsWith('"')) {
        val = val.slice(1, -1);
      } else if (val.startsWith("'") && val.endsWith("'")) {
        val = val.slice(1, -1);
      }
    }

    // Booleans
    if (val === 'true') val = true;
    else if (val === 'false') val = false;

    fm[key] = val;
  }

  return fm;
}

module.exports = { parseFrontmatter, getSchemaVersion, CURRENT_SCHEMA_VERSION };
