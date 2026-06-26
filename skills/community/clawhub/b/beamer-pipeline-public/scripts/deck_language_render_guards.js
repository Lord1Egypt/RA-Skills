"use strict";

const fs = require("node:fs");
const { spawnSync } = require("node:child_process");

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function uniqueStrings(values) {
  const seen = new Set();
  const result = [];
  for (const value of Array.isArray(values) ? values : []) {
    const text = String(value || "").trim();
    if (!text || seen.has(text)) continue;
    seen.add(text);
    result.push(text);
  }
  return result;
}

function countCjkChars(text) {
  return (String(text || "").match(/[\u3400-\u9FFF]/gu) || []).length;
}

function countAsciiLetters(text) {
  return (String(text || "").match(/[A-Za-z]/g) || []).length;
}

function countEnglishWords(text) {
  return (String(text || "").match(/\b[A-Za-z][A-Za-z'-]{1,}\b/g) || []).length;
}

function paragraphLedgerSummaryText(entry) {
  return entry?.summary_sentence ?? entry?.summary ?? entry?.summary_zh ?? entry?.summary_text ?? "";
}

function stripMathAndTexForLanguageStats(text) {
  return String(text || "")
    .replace(/\$[^$]*\$/g, " ")
    .replace(/\\\[[\s\S]*?\\\]/g, " ")
    .replace(/\\\([\s\S]*?\\\)/g, " ")
    .replace(/\\begin\{(?:equation|align|gather|multline)\*?\}[\s\S]*?\\end\{(?:equation|align|gather|multline)\*?\}/gi, " ")
    .replace(/\\[A-Za-z]+\*?(?:\s*\[[^\]]*\])?(?:\s*\{[^{}]*\})?/g, " ")
    .replace(/\\./g, " ")
    .replace(/\b(?:Eq|Eqs|Fig|Figs|Table|Tables|PIDO|PINN|PDE|ODE|CCS|CCUS|CO2|NPV|DCF|ROC|OCR|kWh|MWh|GWh|MW|GW|USD|RMB)\b/gi, " ")
    .replace(/[0-9_{}^=+\-*/.,;:()[\]|<>$]/g, " ");
}

function mostlyEnglishNaturalLanguageStats(text) {
  const cleaned = stripMathAndTexForLanguageStats(text);
  const cjkChars = countCjkChars(cleaned);
  const asciiLetters = countAsciiLetters(cleaned);
  const englishWords = countEnglishWords(cleaned);
  const asciiToCjkRatio = asciiLetters / Math.max(1, cjkChars);
  const hasSourceCopyCue = /\b(?:where|whereas|currently|as\s+the|the\s+model|the\s+paper|this\s+paper|we\s+(?:assume|consider|show|derive)|is\s+existing|is\s+the|are\s+the|denotes?|represents?|respectively|given\s+by|defined\s+as|can\s+be\s+written)\b/i.test(cleaned);
  const reject = (
    (asciiLetters >= 64 && englishWords >= 8 && cjkChars < 16 && asciiToCjkRatio >= 2.8)
    || (hasSourceCopyCue && asciiLetters >= 36 && englishWords >= 5 && cjkChars < 14 && asciiToCjkRatio >= 2.2)
  );
  return {
    reject,
    cjkChars,
    asciiLetters,
    englishWords,
    asciiToCjkRatio,
    hasSourceCopyCue,
  };
}

function compactPreview(text, maxLength = 96) {
  const value = String(text || "").replace(/\s+/g, " ").trim();
  if (value.length <= maxLength) return value;
  return `${value.slice(0, maxLength - 1)}...`;
}

function paragraphLedgerLanguageDiagnostics(paragraphLedger, options = {}) {
  const errors = [];
  const maxErrors = Number.isFinite(Number(options.maxErrors)) ? Math.max(1, Number(options.maxErrors)) : 8;
  const ledger = Array.isArray(paragraphLedger) ? paragraphLedger : [];
  for (const entry of ledger) {
    if (!isPlainObject(entry)) continue;
    const summary = String(paragraphLedgerSummaryText(entry) || "").trim();
    if (!summary) continue;
    const stats = mostlyEnglishNaturalLanguageStats(summary);
    if (!stats.reject) continue;
    const paragraphId = String(entry.paragraph_id ?? entry.id ?? "").trim() || "unknown";
    errors.push(`paragraph_ledger ${paragraphId} summary_sentence appears to copy English source prose instead of a Chinese summary; move raw English to source_excerpt and rewrite summary_sentence in Chinese: "${compactPreview(summary)}"`);
    if (errors.length >= maxErrors) {
      errors.push(`paragraph_ledger has more English-source-copy summary_sentence failures; showing first ${maxErrors}`);
      break;
    }
  }
  return errors;
}

function extractFrameBodies(tex) {
  const source = String(tex || "");
  const bodies = [];
  const beginMarker = "\\begin{frame}";
  const endMarker = "\\end{frame}";
  let cursor = 0;
  while (cursor < source.length) {
    const beginIndex = source.indexOf(beginMarker, cursor);
    if (beginIndex === -1) break;
    const headerEnd = source.indexOf("\n", beginIndex);
    const bodyStart = headerEnd === -1 ? beginIndex + beginMarker.length : headerEnd + 1;
    const endIndex = source.indexOf(endMarker, bodyStart);
    if (endIndex === -1) break;
    bodies.push(source.slice(bodyStart, endIndex));
    cursor = endIndex + endMarker.length;
  }
  return bodies;
}

function extractLatexItemTexts(tex) {
  const items = [];
  for (const body of extractFrameBodies(tex)) {
    const itemPattern = /\\item(?:\s*<[^>]*>)?(?:\s*\[[^\]]*\])?\s*([\s\S]*?)(?=\n\s*\\item\b|\n\s*\\end\{(?:itemize|enumerate|description)\}|$)/g;
    for (const match of body.matchAll(itemPattern)) {
      const item = String(match[1] || "")
        .replace(/\\begin\{(?:equation|align|gather|multline)\*?\}[\s\S]*?\\end\{(?:equation|align|gather|multline)\*?\}/gi, " ")
        .replace(/\s+/g, " ")
        .trim();
      if (item) items.push(item);
    }
  }
  return items;
}

function literalLatexLeakPatternDiagnostics(text, sourceLabel) {
  const source = String(text || "");
  if (!source) return [];
  const checks = [
    {
      pattern: /\\textbackslash(?:\{\}|\\\{\\\})?/i,
      message: `${sourceLabel} contains visible \\textbackslash{} leakage from blanket TeX escaping`,
    },
    {
      pattern: /\\textasciicircum(?:\{\}|\\\{\\\})?/i,
      message: `${sourceLabel} contains visible \\textasciicircum{} leakage from blanket TeX escaping`,
    },
    {
      pattern: /\\\$\s*[A-Za-z]\\_/,
      message: `${sourceLabel} contains escaped inline math like \\$P\\_..., so LaTeX math will render as literal text`,
    },
    {
      pattern: /\bwhere\s+\\?\$/i,
      message: `${sourceLabel} contains an English raw-math prose fragment such as "where $...", which must be rewritten as Chinese prose plus equation_blocks`,
    },
    {
      pattern: /\\\{\\\}\s*[A-Za-z]+/,
      message: `${sourceLabel} contains escaped command braces such as \\{}mathrm/\\{}gamma, indicating LaTeX was rendered as text`,
    },
    {
      pattern: /\\ensuremath\s*\{/,
      message: `${sourceLabel} contains \\ensuremath{...} in visible prose; move math symbols into equation_blocks and rewrite visible bullets as Chinese natural-language explanation`,
    },
  ];
  return checks.filter((check) => check.pattern.test(source)).map((check) => check.message);
}

function latexItemLanguageDiagnostics(tex, options = {}) {
  const sourceLabel = String(options.sourceLabel || "main.tex");
  const errors = [];
  const maxErrors = Number.isFinite(Number(options.maxErrors)) ? Math.max(1, Number(options.maxErrors)) : 6;
  for (const item of extractLatexItemTexts(tex)) {
    const stats = mostlyEnglishNaturalLanguageStats(item);
    if (!stats.reject) continue;
    errors.push(`${sourceLabel} contains a mostly-English visible bullet; visible Beamer prose should be Chinese and raw source excerpts should stay out of slide bullets: "${compactPreview(item)}"`);
    if (errors.length >= maxErrors) {
      errors.push(`${sourceLabel} has more mostly-English visible bullet failures; showing first ${maxErrors}`);
      break;
    }
  }
  return errors;
}

function latexItemInlineMathDiagnostics(tex, options = {}) {
  const sourceLabel = String(options.sourceLabel || "main.tex");
  const errors = [];
  const maxErrors = Number.isFinite(Number(options.maxErrors)) ? Math.max(1, Number(options.maxErrors)) : 12;
  for (const item of extractLatexItemTexts(tex)) {
    const hasEnsuremath = /\\ensuremath(?:\s*\[[^\]]*\])?(?:\s*\{[^}]*\})/.test(item);
    if (!hasEnsuremath) continue;
    errors.push(`${sourceLabel} visible bullet contains \\ensuremath{...} bypass; move symbols into equation_blocks and write the bullet as Chinese natural-language explanation: "${compactPreview(item)}"`);
    if (errors.length >= maxErrors) {
      errors.push(`${sourceLabel} has more \\ensuremath-bypass failures; showing first ${maxErrors}`);
      break;
    }
  }
  return errors;
}

// Non-blocking: $...$ inline math is legitimate LaTeX.  Flag as informational warning
// so the programmer can still see it, but do NOT treat these as repair-blocking errors.
function latexItemInlineMathWarnings(tex, options = {}) {
  const sourceLabel = String(options.sourceLabel || "main.tex");
  const warnings = [];
  const maxWarnings = Number.isFinite(Number(options.maxErrors)) ? Math.max(1, Number(options.maxErrors)) : 12;
  for (const item of extractLatexItemTexts(tex)) {
    const hasRawInlineMath = /\$[^$]+\$/.test(item);
    if (!hasRawInlineMath) continue;
    warnings.push(`${sourceLabel} visible bullet contains $...$ inline math (informational — allowed, not blocking): "${compactPreview(item)}"`);
    if (warnings.length >= maxWarnings) {
      warnings.push(`${sourceLabel} has more $...$ inline-math bullets; showing first ${maxWarnings}`);
      break;
    }
  }
  return warnings;
}

function beamerMainTexLanguageAndLatexLeakDiagnostics(mainTex, options = {}) {
  const sourceLabel = String(options.sourceLabel || "main.tex");
  return uniqueStrings([
    ...literalLatexLeakPatternDiagnostics(mainTex, sourceLabel),
    ...latexItemLanguageDiagnostics(mainTex, { sourceLabel }),
    ...latexItemInlineMathDiagnostics(mainTex, { sourceLabel }),
  ]);
}

// Non-blocking: returns $...$ inline-math warnings separate from blocking errors.
function beamerMainTexLanguageAndLatexLeakWarnings(mainTex, options = {}) {
  const sourceLabel = String(options.sourceLabel || "main.tex");
  return uniqueStrings([
    ...latexItemInlineMathWarnings(mainTex, { sourceLabel }),
  ]);
}

function renderedTextLatexLeakDiagnostics(renderedText, options = {}) {
  const sourceLabel = String(options.sourceLabel || "main.pdf text");
  const text = String(renderedText || "");
  if (!text.trim()) return [];
  const errors = [
    ...literalLatexLeakPatternDiagnostics(text, sourceLabel),
  ];
  if (/\$[A-Za-z]_\{?[A-Za-z0-9]/.test(text) || /\\(?:mathrm|gamma|alpha|beta|theta|frac|sum|int)\b/.test(text)) {
    errors.push(`${sourceLabel} contains literal math markup after rendering; formulas should render as math, not dollar/backslash text`);
  }
  for (const line of text.split(/\r?\n/).map((item) => item.trim()).filter(Boolean)) {
    const stats = mostlyEnglishNaturalLanguageStats(line);
    if (stats.reject) {
      errors.push(`${sourceLabel} contains a mostly-English rendered prose line; visible Beamer prose should be Chinese: "${compactPreview(line)}"`);
      break;
    }
  }
  return uniqueStrings(errors);
}

function extractPdfTextIfAvailable(pdfPath, options = {}) {
  const minBytes = Number.isFinite(Number(options.minBytes)) ? Math.max(0, Number(options.minBytes)) : 512;
  try {
    if (!pdfPath || !fs.existsSync(pdfPath)) return "";
    const stat = fs.statSync(pdfPath);
    if (!stat.isFile() || stat.size < minBytes) return "";
    const result = spawnSync("pdftotext", ["-layout", String(pdfPath), "-"], {
      encoding: "utf8",
      timeout: 5000,
      maxBuffer: 2 * 1024 * 1024,
    });
    if (result.status !== 0 || result.error) return "";
    return String(result.stdout || "");
  } catch {
    return "";
  }
}

module.exports = {
  beamerMainTexLanguageAndLatexLeakDiagnostics,
  beamerMainTexLanguageAndLatexLeakWarnings,
  countAsciiLetters,
  countCjkChars,
  extractPdfTextIfAvailable,
  mostlyEnglishNaturalLanguageStats,
  paragraphLedgerLanguageDiagnostics,
  latexItemInlineMathDiagnostics,
  latexItemInlineMathWarnings,
  renderedTextLatexLeakDiagnostics,
};
