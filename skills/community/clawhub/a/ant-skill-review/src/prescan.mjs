import { lstatSync, readFileSync, readlinkSync } from "node:fs";
import { join, relative, extname } from "node:path";
import { formatMode, formatSize, walkDir, isBinaryBuffer } from "./utils.mjs";

const LARGE_TEXT_THRESHOLD = 100 * 1024; // 100KB

// ---------------------------------------------------------------------------
// Scanner registry
// ---------------------------------------------------------------------------

/**
 * scanFile(ctx) is called for every file. ctx contains:
 *   - filePath:  absolute path
 *   - relPath:   path relative to skill root
 *   - fileName:  basename
 *   - stat:      lstat result (may be null on error)
 *   - isSymlink: boolean
 *   - symlinkTarget: string | null
 *   - content:   Buffer | null (lazy-loaded raw bytes)
 *
 * Return an array of finding strings, or an empty array.
 */
const scanners = [];

export function registerScanner(title, scanFile) {
  scanners.push({ title, scanFile });
}

// ---------------------------------------------------------------------------
// Regex content scanner helper
// ---------------------------------------------------------------------------

/**
 * Register a scanner that matches a regex against file content.
 * Content is read as latin1 (single-byte) so regex operates on raw bytes.
 * Options:
 *   - exts: Set of file extensions to limit scanning (null = all files)
 *   - maxSize: skip files larger than this (bytes, default unlimited)
 *   - formatMatch(match, ctx, lineNum, lineText): return a finding string
 */
const MAX_CONTEXT_LINE_LEN = 200;
const CONTEXT_CHARS = 5;

function defaultFormatMatch(m, ctx, line, lineText) {
  let snippet;
  if (lineText.length <= MAX_CONTEXT_LINE_LEN) {
    snippet = lineText.trimEnd();
  } else {
    const start = Math.max(0, m.index - CONTEXT_CHARS);
    const end = Math.min(lineText.length, m.index + m[0].length + CONTEXT_CHARS);
    snippet = (start > 0 ? "..." : "") + lineText.substring(start, end) + (end < lineText.length ? "..." : "");
  }
  return `  ${ctx.relPath}:${line}: ${snippet}`;
}

export function registerPatternScanner(title, regex, opts = {}) {
  const { exts = null, maxSize = Infinity, formatMatch } = opts;
  const fmt = formatMatch || defaultFormatMatch;

  registerScanner(title, (ctx) => {
    if (!ctx.content) return [];
    if (exts && !exts.has(extname(ctx.fileName).toLowerCase())) return [];
    if (ctx.stat && ctx.stat.size > maxSize) return [];

    const text = ctx.content.toString("latin1");
    const findings = [];
    const lines = text.split("\n");
    for (let i = 0; i < lines.length; i++) {
      const m = regex.exec(lines[i]);
      if (m) findings.push(fmt(m, ctx, i + 1, lines[i]));
    }
    return findings;
  });
}

// ---------------------------------------------------------------------------
// Built-in scanners
// ---------------------------------------------------------------------------

registerScanner("Symlinks", (ctx) => {
  if (!ctx.isSymlink) return [];
  return [`  ${ctx.relPath} -> ${ctx.symlinkTarget || "[broken]"}`];
});

const SUSPICIOUS_FILENAME_RE = /[\u0400-\u04ff\u0370-\u03ff\u0530-\u058f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\ufe00-\ufe0f]|[\u{e0100}-\u{e01ef}]/u;

// Shell metacharacters that enable command injection when filenames are
// interpolated without proper quoting: $() `` ; | & < > \n etc.
const SHELL_INJECTION_RE = /\$\(|`|[;&|<>\n\r]/;

registerScanner("Suspicious Filenames", (ctx) => {
  const findings = [];

  // Check for confusable / invisible Unicode characters
  if (SUSPICIOUS_FILENAME_RE.test(ctx.fileName)) {
    const codepoints = [...ctx.fileName]
      .filter(ch => SUSPICIOUS_FILENAME_RE.test(ch))
      .map(ch => "U+" + ch.codePointAt(0).toString(16).toUpperCase().padStart(4, "0"));
    findings.push(`  ${ctx.relPath}: unicode ${codepoints.join(", ")}`);
  }

  // Check for shell injection metacharacters
  if (SHELL_INJECTION_RE.test(ctx.fileName)) {
    const chars = [...new Set(ctx.fileName.match(/\$\(|`|[;&|<>\n\r]/g))]
      .map(c => c === "\n" ? "\\n" : c === "\r" ? "\\r" : c);
    findings.push(`  ${ctx.relPath}: shell metachar ${chars.join(" ")}`);
  }

  return findings;
});

registerScanner("Large Files (>100KB)", (ctx) => {
  const size = ctx.stat?.size || 0;
  if (size >= LARGE_TEXT_THRESHOLD) {
    return [`  ${ctx.relPath}: ${formatSize(size)}`];
  }
  return [];
});

// Known-safe binary formats — excluded from Binary Codes findings
const SAFE_BINARY_EXTS = new Set([
  ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
  ".tiff", ".tif", ".avif", ".heic", ".heif",
  ".woff", ".woff2", ".ttf", ".otf", ".eot",
]);

registerScanner("Binary Codes", (ctx) => {
  if (ctx.isSymlink || !ctx.stat) return [];

  const ext = extname(ctx.fileName).toLowerCase();
  const isExecutable = !!(ctx.stat.mode & 0o111);

  if (ctx.isBinary && !SAFE_BINARY_EXTS.has(ext)) {
    const tag = isExecutable ? "+x" : "binary";
    return [`  ${ctx.relPath}: ${formatSize(ctx.stat.size)} (${tag})`];
  }

  return [];
});

// Invisible chars: match UTF-8 byte sequences for invisible Unicode codepoints
// U+200B-200D (e2 80 8b-8d), U+FEFF (ef bb bf), U+202E (e2 80 ae),
// U+2060-2064 (e2 81 a0-a4), U+00AD (c2 ad), U+FE00-FE0F (ef b8 80-8f),
// U+E0100-E01EF (f3 a0 84 80 - f3 a0 87 af)
const INVISIBLE_BYTES_RE = /\xe2\x80[\x8b-\x8d\xae]|\xef\xbb\xbf|\xe2\x81[\xa0-\xa4]|\xc2\xad|\xef\xb8[\x80-\x8f]|\xf3\xa0[\x84-\x87][\x80-\xaf]/g;

// Map invisible UTF-8 byte sequences to their Unicode codepoint names
function describeInvisible(bytes) {
  const hex = [...bytes].map(b => b.toString(16).padStart(2, "0")).join("");
  const map = {
    "e2808b": "U+200B ZERO WIDTH SPACE",
    "e2808c": "U+200C ZERO WIDTH NON-JOINER",
    "e2808d": "U+200D ZERO WIDTH JOINER",
    "e280ae": "U+202E RIGHT-TO-LEFT OVERRIDE",
    "efbbbf": "U+FEFF BOM/ZERO WIDTH NO-BREAK SPACE",
    "e281a0": "U+2060 WORD JOINER",
    "e281a1": "U+2061 FUNCTION APPLICATION",
    "e281a2": "U+2062 INVISIBLE TIMES",
    "e281a3": "U+2063 INVISIBLE SEPARATOR",
    "e281a4": "U+2064 INVISIBLE PLUS",
    "c2ad":   "U+00AD SOFT HYPHEN",
  };
  if (map[hex]) return map[hex];
  if (hex.startsWith("efb8")) return `U+FE0x VARIATION SELECTOR`;
  if (hex.startsWith("f3a0")) return `U+E01xx TAG CHARACTER`;
  return `invisible [${hex}]`;
}

registerScanner("Invisible Characters", (ctx) => {
  if (ctx.isBinary) return [];

  const raw = ctx.content.toString("latin1");
  const re = new RegExp(INVISIBLE_BYTES_RE.source, "g");
  let m;
  // count matches per character type
  const counts = new Map();
  while ((m = re.exec(raw)) !== null) {
    const desc = describeInvisible(Buffer.from(m[0], "latin1"));
    counts.set(desc, (counts.get(desc) || 0) + 1);
  }
  if (counts.size === 0) return [];

  const total = [...counts.values()].reduce((a, b) => a + b, 0);
  // Skip files with 10 or fewer invisible chars — likely false positives
  if (total <= 10) return [];

  const parts = [...counts.entries()].map(([desc, n]) => `${desc} (${n})`);
  return [`  ${ctx.relPath}: ${parts.join(", ")}`];
});

// ANSI / terminal escape sequences (raw \x1b bytes in text files)
// These can manipulate terminal display to hide malicious content from reviewers:
//   - CSI (\x1b[): cursor movement, erase lines, change colors (hide text)
//   - OSC (\x1b]): set window title (historically exploitable in some terminals)
registerScanner("ANSI Escape Sequences", (ctx) => {
  if (ctx.isBinary) return [];

  const raw = ctx.content.toString("latin1");

  // Match: CSI sequences, OSC sequences, or other ESC+byte pairs
  const re = /\x1b(?:\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]|\][^\x07\x1b]*(?:\x07|\x1b\\)|.)/g;
  let m;
  const types = new Map();
  while ((m = re.exec(raw)) !== null) {
    const kind = m[0][1] === "[" ? "CSI" : m[0][1] === "]" ? "OSC" : "ESC";
    types.set(kind, (types.get(kind) || 0) + 1);
  }
  if (types.size === 0) return [];

  const total = [...types.values()].reduce((a, b) => a + b, 0);
  const parts = [...types.entries()].map(([t, n]) => `${t}(${n})`);
  return [`  ${ctx.relPath}: ${total} escape sequence(s) — ${parts.join(", ")}`];
});

registerPatternScanner(
  "JS Obfuscation",
  /var a0_0x|return!!\[\]|while\s*\(\s*!!\[\]\s*\)|\['atob'\]\s*=\s*function\(|parseInt\(_0x[a-f0-9]{4,8}\(0x[a-f0-9]{1,5}\)\)/,
);

registerScanner("Hardcoded URLs", (ctx) => {
  if (ctx.isBinary) return [];
  const text = ctx.content.toString("utf8");
  // Keep extraction conservative to avoid swallowing surrounding CJK text or
  // punctuation from markdown/Chinese prose when URLs are immediately followed
  // by full-width punctuation or natural language without ASCII whitespace.
  const re = /https?:\/\/[^\s"'`<>\u0000-\u001f\u007f\u3000-\u303f\uff00-\uffef\u4e00-\u9fff]{5,}/g;
  const urls = new Set();
  let m;
  while ((m = re.exec(text)) !== null) {
    const url = m[0].replace(/[)\].,;:!?]+$/, "");
    urls.add(url);
  }
  if (urls.size === 0) return [];
  const all = [...urls];
  const list = all.slice(0, 5).map((u) => `    ${u}`).join("\n");
  const more = all.length > 5 ? `\n    ... and ${all.length - 5} more` : "";
  return [`  ${ctx.relPath}: ${all.length} URL(s)\n${list}${more}`];
});

// ---------------------------------------------------------------------------
// Main prescan
// ---------------------------------------------------------------------------

export function prescan(skillDir) {
  const fileLines = [];
  const results = scanners.map(() => []);
  let totalFiles = 0;

  walkDir(skillDir, (dir, files) => {
    const relDir = relative(skillDir, dir) || ".";
    fileLines.push("");
    fileLines.push(`${relDir}:`);

    for (const name of files) {
      totalFiles += 1;
      const fpath = join(dir, name);
      const relPath = relative(skillDir, fpath);

      let stat = null;
      let isSymlink = false;
      let symlinkTarget = null;
      try {
        stat = lstatSync(fpath);
        isSymlink = stat.isSymbolicLink();
      } catch {}

      const modeStr = stat ? formatMode(stat.mode) : "----------";
      const size = stat?.size || 0;

      if (isSymlink) {
        try { symlinkTarget = readlinkSync(fpath); } catch {}
        fileLines.push(`  ${modeStr} ${String(size).padStart(8)}  ${relPath}${symlinkTarget ? ` -> ${symlinkTarget}` : " [broken symlink]"}`);
      } else {
        fileLines.push(`  ${modeStr} ${String(size).padStart(8)}  ${relPath}`);
      }

      let _content = undefined;
      let _isBinary = undefined;

      const ctx = {
        filePath: fpath,
        relPath,
        fileName: name,
        stat,
        isSymlink,
        symlinkTarget,
        get content() {
          if (_content === undefined) {
            if (isSymlink) { _content = null; return null; }
            try { _content = readFileSync(fpath); } catch { _content = null; }
          }
          return _content;
        },
        get isBinary() {
          if (_isBinary === undefined) {
            _isBinary = !this.content || isBinaryBuffer(this.content);
          }
          return _isBinary;
        },
      };

      for (let i = 0; i < scanners.length; i++) {
        const findings = scanners[i].scanFile(ctx);
        if (findings.length) results[i].push(...findings);
      }
    }
  });

  // -- Build output --
  let out = `# SKILL Files\nNote: Complete file inventory. Avoid broad file discovery unless needed for a specific referenced path.\n\nTotal ${totalFiles} file(s)\n` + fileLines.join("\n") + "\n";

  out += "\n# Pre-Scan Results";
  out += "\nUse these as leads, not as the traversal order.";
  out += `\n\nScan Summary:\n`
  for (let i = 0; i < scanners.length; i++) {
    out += `- (${results[i].length}) ${scanners[i].title}\n`;
  }

  out += "\n> Note: Pre-scan results are hints, not final conclusions.";
  out += `\n\nScan details:\n`

  for (let i = 0; i < scanners.length; i++) {
    if (results[i].length === 0) continue;
    out += `\n## ${scanners[i].title}\n\n`;
    out += results[i].join("\n") + "\n";
  }

  return out;
}
