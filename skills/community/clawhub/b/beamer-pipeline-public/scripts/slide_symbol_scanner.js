#!/usr/bin/env node
/**
 * slide_symbol_scanner.js — Deterministically correct notation_coverage in slides.json
 *
 * Scans every slide's visible content fields (matching pipeline's slideVisibleTextFromPlan),
 * uses pipeline's own matching functions (textContainsSymbolCandidate, symbolCandidatesFromNotationEntry),
 * and rewrites notation_coverage so every entry's first_defined_slide_ids / used_slide_ids
 * are backed by actual visible symbol presence.
 *
 * Usage:
 *   node slide_symbol_scanner.js --fix <slides.json>
 *   node slide_symbol_scanner.js --check <slides.json>    (dry-run, report issues)
 */

const fs = require("fs");
const path = require("path");

const PIPELINE_DIR = path.resolve(__dirname);

function loadCanonModule() {
  const canonPath = path.join(PIPELINE_DIR, "deck_symbol_canonicalization.js");
  const canon = require(canonPath);
  if (!canon || typeof canon.textContainsSymbolCandidate !== "function") {
    console.error("FATAL: deck_symbol_canonicalization.js did not export required functions");
    process.exit(1);
  }
  return canon;
}

// ─── slideVisibleTextFromPlan (matches pipeline behavior) ──────

function appendVisibleTextFragments(target, value) {
  if (typeof value === "string" || typeof value === "number") {
    const text = String(value).trim();
    if (text) target.push(text);
    return;
  }
  if (Array.isArray(value)) {
    for (const item of value) appendVisibleTextFragments(target, item);
  }
}

function visibleFragmentsFromBlock(block) {
  if (!block || typeof block !== "object") return [];
  const fragments = [];
  for (const key of [
    "title", "subtitle", "heading", "header", "caption", "label",
    "latex", "text", "content", "paragraph", "body", "claim",
    "summary", "description", "explanation", "legend", "alt_text", "alt", "value",
  ]) { appendVisibleTextFragments(fragments, block[key]); }
  for (const key of ["items", "bullets", "points", "list", "lines", "paragraphs", "captions"]) {
    appendVisibleTextFragments(fragments, block[key]);
  }
  for (const key of ["blocks", "children", "columns", "left", "right"]) {
    const nested = block[key];
    if (Array.isArray(nested)) {
      for (const item of nested) fragments.push(...visibleFragmentsFromBlock(item));
    } else if (nested && typeof nested === "object") {
      fragments.push(...visibleFragmentsFromBlock(nested));
    }
  }
  return [...new Set(fragments)];
}

function slideVisibleTextFromPlan(slide) {
  if (!slide || typeof slide !== "object") return "";
  const fragments = [];
  for (const key of ["title", "subtitle", "headline", "caption", "core_message", "summary", "description"]) {
    appendVisibleTextFragments(fragments, slide[key]);
  }
  for (const key of ["bullets", "items", "points", "list", "lines", "equations"]) {
    appendVisibleTextFragments(fragments, slide[key]);
  }
  for (const key of ["defines_symbols", "used_symbols"]) {
    appendVisibleTextFragments(fragments, slide[key]);
  }
  const eqs = Array.isArray(slide.equation_blocks) ? slide.equation_blocks : [];
  for (const eq of eqs) {
    if (typeof eq?.latex === "string" && eq.latex.trim()) {
      appendVisibleTextFragments(fragments, eq.latex.trim());
    }
    if (typeof eq?.explanation === "string" && eq.explanation.trim()) {
      appendVisibleTextFragments(fragments, eq.explanation.trim());
    }
  }
  const blocks = Array.isArray(slide.blocks) ? slide.blocks : [];
  for (const block of blocks) fragments.push(...visibleFragmentsFromBlock(block));
  return [...new Set(fragments)].join("\n");
}

// ─── Structural command filter ─────────────────────────────────
const STRUCTURAL_LATEX = new Set([
  // Spacing
  "\\quad", "\\qquad", "\\hspace", "\\vspace", "\\;", "\\,", "\\!", "\\:",
  // Delimiters
  "\\left", "\\right", "\\bigl", "\\bigr", "\\big", "\\Big", "\\bigg", "\\Bigg",
  "\\lvert", "\\rvert", "\\lVert", "\\rVert", "\\langle", "\\rangle", "\\mid",
  // Accents (modify other symbols, not standalone notation)
  "\\hat", "\\tilde", "\\bar", "\\vec", "\\dot", "\\ddot", "\\mathring",
  "\\check", "\\breve", "\\acute", "\\grave",
  // Standard math functions/operators
  "\\ln", "\\log", "\\exp", "\\sin", "\\cos", "\\tan", "\\cot", "\\sec", "\\csc",
  "\\max", "\\min", "\\sup", "\\inf", "\\lim", "\\det", "\\dim", "\\gcd", "\\hom",
  "\\arg", "\\deg", "\\Pr", "\\ker",
  // Integral/sum/product symbols
  "\\int", "\\iint", "\\iiint", "\\oint", "\\sum", "\\prod", "\\coprod",
  "\\bigcup", "\\bigcap", "\\bigvee", "\\bigwedge",
  // Standard constants/symbols
  "\\infty", "\\pi", "\\emptyset", "\\partial", "\\nabla", "\\Delta",
  "\\cdot", "\\cdots", "\\ldots", "\\vdots", "\\ddots",
  "\\colon", "\\to", "\\mapsto", "\\Rightarrow", "\\Leftrightarrow",
  "\\times", "\\otimes", "\\oplus", "\\pm", "\\mp",
  // Fractions
  "\\frac", "\\tfrac", "\\dfrac", "\\binom",
  // Roots
  "\\sqrt",
  // Structural
  "\\begin", "\\end", "\\array", "\\hline", "\\toprule", "\\midrule", "\\bottomrule",
  "\\label", "\\ref", "\\eqref", "\\cite", "\\tag", "\\nonumber", "\\displaystyle",
  "\\textstyle", "\\scriptstyle", "\\scriptscriptstyle",
  // Typographic wrappers (single-letter arg → typographic, multi-letter → keep as notation)
  // These are handled specially below, not in the Set
]);

const TYPOGRAPHIC_ARG_PATTERN = /^\\(?:mathrm|mathbf|mathcal|mathbb|mathit|mathsf|mathtt|operatorname|text)\{(\{?[^}]+\}?)\}$/;

const STRUCTURAL_PREFIXES = [
  "\\begin{", "\\end{", "\\tag{", "\\frac{", "\\tfrac{", "\\dfrac{", "\\binom{",
  "\\sqrt{",
  "\\displaystyle", "\\textstyle",
];

function isStructuralLatexCommand(raw) {
  // Direct structural match
  if (STRUCTURAL_LATEX.has(raw)) return true;
  // Prefix match (e.g. \begin{aligned}, \tag{2.1}, \frac{...})
  for (const prefix of STRUCTURAL_PREFIXES) {
    if (raw.startsWith(prefix) && raw !== prefix) return true;
  }
  // Match \mathbf{X} etc where X is a single letter → typographic
  const typoMatch = raw.match(TYPOGRAPHIC_ARG_PATTERN);
  if (typoMatch) {
    const arg = typoMatch[1].replace(/[{}]/g, "").trim();
    // Single letter = typographic variant of standard math
    if (/^[a-zA-Z]$/.test(arg)) return true;
    // Common typographic words
    if (/^(d|i|e|dx|dy|dt|id|tr|Re|Im|mod|rank|span|diag|trace|s\.t\.|w\.r\.t\.)$/i.test(arg)) return true;
    // Multi-letter words like Corr, Real, Market are notation → keep
  }
  // Custom shorthand macros used ONLY as typographic/structural helpers
  if (/^\\(?:dv|dr|pdv|odv|dd|dvD|odvD|pdvD)$/.test(raw)) return true;
  // \d, \D — custom differential 'd' (typographic choice, notation is dW_t etc)
  if (/^\\[dD]$/.test(raw)) return true;
  // \k, \c — single lowercase letter macros commonly used as kerning/shorthand
  if (/^\\[kc]$/.test(raw)) return true;
  return false;
}

// ─── Main scan + fix logic ─────────────────────────────────────

function scanAndFix(slidesPath, dryRun, analysisPath = "") {
  const canon = loadCanonModule();
  const { textContainsSymbolCandidate, symbolCandidatesFromNotationEntry } = canon;

  const raw = JSON.parse(fs.readFileSync(slidesPath, "utf8"));
  const slides = raw.slides || [];
  const notationCoverage = Array.isArray(raw.notation_coverage) ? raw.notation_coverage : [];

  // Build slide text cache
  const slideTextCache = new Map();
  for (const s of slides) {
    slideTextCache.set(s.slide_id, slideVisibleTextFromPlan(s));
  }

  // ─── Phase 1: Correct existing entries ───────────────────────
  let fixes = 0;
  for (const entry of notationCoverage) {
    const symbol = entry.symbol || "";
    if (!symbol) continue;

    const candidates = symbolCandidatesFromNotationEntry(symbol);
    if (candidates.length === 0) {
      console.log(`[skip] ${symbol}: no candidates generated`);
      continue;
    }

    // Verify & fix first_defined_slide_ids
    const currentFirst = (Array.isArray(entry.first_defined_slide_ids)
      ? entry.first_defined_slide_ids : []).map(s => String(s).trim()).filter(Boolean);
    const validFirst = [];
    const invalidFirst = [];
    for (const sid of currentFirst) {
      const text = slideTextCache.get(sid) || "";
      const visible = candidates.some(c => textContainsSymbolCandidate(c, text));
      if (visible) validFirst.push(sid);
      else invalidFirst.push(sid);
    }
    if (invalidFirst.length > 0) {
      // Try to find the earliest slide where symbol is actually visible
      const visibleSlides = [];
      for (const s of slides) {
        const text = slideTextCache.get(s.slide_id) || "";
        if (candidates.some(c => textContainsSymbolCandidate(c, text))) {
          visibleSlides.push(s.slide_id);
        }
      }
      if (visibleSlides.length > 0) {
        entry.first_defined_slide_ids = [visibleSlides[0]];
        if (dryRun) {
          console.log(`[fix] ${symbol}: first_defined ${currentFirst.join(",")} → ${visibleSlides[0]} (${invalidFirst.join(",")} not visible)`);
        }
        fixes++;
      } else {
        if (dryRun) console.log(`[warn] ${symbol}: not visible on ANY slide, keeping ${currentFirst.join(",")}`);
      }
    }

    // Verify & fix used_slide_ids
    const currentUsed = (Array.isArray(entry.used_slide_ids)
      ? entry.used_slide_ids : []).map(s => String(s).trim()).filter(Boolean);
    const validUsed = [];
    let usedChanged = false;
    for (const sid of currentUsed) {
      const text = slideTextCache.get(sid) || "";
      const visible = candidates.some(c => textContainsSymbolCandidate(c, text));
      if (visible) validUsed.push(sid);
      else usedChanged = true;
    }
    if (usedChanged) {
      entry.used_slide_ids = validUsed;
      if (dryRun) console.log(`[fix] ${symbol}: used_slide_ids filtered to ${validUsed.length} visible`);
      fixes++;
    }
  }

  // ─── Phase 2: Add missing symbols from equation_blocks ───────
  const trackedSymbols = new Set(notationCoverage.map(e => e.symbol).filter(Boolean));
  const missingEntries = [];

  for (const slide of slides) {
    const eqs = Array.isArray(slide.equation_blocks) ? slide.equation_blocks : [];
    for (const eq of eqs) {
      const latex = typeof eq?.latex === "string" ? eq.latex.trim() : "";
      if (!latex) continue;

      // Extract LaTeX macro candidates: \alpha_1, \beta, \mathrm{Corr}, etc.
      const macroPattern = /\\[a-zA-Z]+(?:\{[^}]*\})?(?:_\{[^}]*\})?(?:\^\{[^}]*\})?/g;
      let macroMatch;
      while ((macroMatch = macroPattern.exec(latex)) !== null) {
        const raw = macroMatch[0];
        // Skip structural/typographic commands (not mathematical notation)
        if (isStructuralLatexCommand(raw)) continue;
        if (!trackedSymbols.has(raw)) {
          trackedSymbols.add(raw);
          // Find all slides where this symbol is visible
          const candidates = symbolCandidatesFromNotationEntry(raw);
          const visibleSlides = [];
          for (const s of slides) {
            const text = slideTextCache.get(s.slide_id) || "";
            if (candidates.some(c => textContainsSymbolCandidate(c, text))) {
              visibleSlides.push(s.slide_id);
            }
          }
          if (visibleSlides.length > 0) {
            missingEntries.push({
              symbol: raw,
              status: "defined",
              first_defined_slide_ids: [visibleSlides[0]],
              used_slide_ids: visibleSlides,
              meaning: awaitMeaning(raw, latex),  // basic heuristic
              source_paragraph_ids: [],
              source_quote: "",
              source_definition_summary: "",
              defined_on_first_visible_use: true,
            });
            if (dryRun) console.log(`[add] ${raw}: first on ${visibleSlides[0]}, used on ${visibleSlides.length} slides`);
            fixes++;
          }
        }
      }
    }
  }

  // ─── Phase 3: Scan analysis.json for symbols missed by Phase 2 ───────
  // Phase 2 only scans equation_blocks. Symbols appearing only in bullets/core_message
  // or in the source paper's equations but not tagged as equation_blocks get caught here.
  if (analysisPath && fs.existsSync(analysisPath)) {
    try {
      const analysisDoc = JSON.parse(fs.readFileSync(analysisPath, "utf8"));
      const eqs = Array.isArray(analysisDoc.equations) ? analysisDoc.equations : [];
      const ledger = Array.isArray(analysisDoc.paragraph_ledger) ? analysisDoc.paragraph_ledger : [];

      // Collect all LaTeX source text
      const sourceTextParts = [];
      for (const eq of eqs) {
        const latex = typeof eq?.latex === "string" ? eq.latex.trim() : "";
        if (latex) sourceTextParts.push(latex);
        const explanation = typeof eq?.explanation === "string" ? eq.explanation.trim() : "";
        if (explanation) sourceTextParts.push(explanation);
      }
      for (const p of ledger) {
        const text = typeof p?.text === "string" ? p.text : "";
        if (text) sourceTextParts.push(text);
      }
      const sourceText = sourceTextParts.join(" ");

      const macroPattern2 = /\\[a-zA-Z]+(?:\{[^}]*\})?(?:_\{[^}]*\})?(?:\^\{[^}]*\})?/g;
      let srcMacro;
      while ((srcMacro = macroPattern2.exec(sourceText)) !== null) {
        const raw = srcMacro[0];
        if (isStructuralLatexCommand(raw)) continue;
        if (trackedSymbols.has(raw)) continue;

        trackedSymbols.add(raw);
        const candidates = symbolCandidatesFromNotationEntry(raw);
        const visibleSlides = [];
        for (const s of slides) {
          const text = slideTextCache.get(s.slide_id) || "";
          if (candidates.some(c => textContainsSymbolCandidate(c, text))) {
            visibleSlides.push(s.slide_id);
          }
        }

        if (visibleSlides.length > 0) {
          missingEntries.push({
            symbol: raw,
            status: "defined",
            first_defined_slide_ids: [visibleSlides[0]],
            used_slide_ids: visibleSlides,
            meaning: awaitMeaning(raw, sourceText),
            source_paragraph_ids: [],
            source_quote: "",
            source_definition_summary: "",
            defined_on_first_visible_use: true,
          });
          if (dryRun) console.log(`[add:analysis] ${raw}: first on ${visibleSlides[0]}, used on ${visibleSlides.length} slides`);
          fixes++;
        } else {
          if (dryRun) console.log(`[warn:analysis] ${raw}: found in analysis.json but not visible in any slide (will need post-compile main.tex scan)`);
        }
      }
    } catch (err) {
      console.warn(`[warn] Phase 3 analysis.json scan failed: ${err.message}`);
    }
  }

  raw.notation_coverage = [...notationCoverage, ...missingEntries];
  raw.notation_coverage_last_fixed_by = "slide_symbol_scanner";
  raw.notation_coverage_last_fixed_at = new Date().toISOString();

  if (!dryRun && fixes > 0) {
    fs.writeFileSync(slidesPath, JSON.stringify(raw, null, 2), "utf8");
  }

  console.log(`\n[scan] ${notationCoverage.length} entries scanned, ${missingEntries.length} added, ${fixes} total fixes${dryRun ? " (dry-run)" : " (applied)"}`);
  return fixes;
}

function awaitMeaning(symbol, contextLatex) {
  // Simple heuristics
  const map = {
    "\\alpha": "风险中性参数/系数",
    "\\beta": "均值回复速度",
    "\\gamma": "波动率参数",
    "\\delta": "利率参数/贴现因子",
    "\\epsilon": "误差项",
    "\\theta": "长期均值",
    "\\kappa": "均值回复速度",
    "\\lambda": "特征值/强度参数",
    "\\mu": "漂移项/均值",
    "\\sigma": "波动率",
    "\\rho": "相关系数",
    "\\tau": "到期时间",
    "\\phi": "特征函数",
    "\\psi": "特征函数/辅助函数",
    "\\omega": "参数/权重",
    "\\xi": "辅助变量",
    "\\Sigma": "协方差矩阵",
    "\\Omega": "参数空间/矩阵",
  };
  return map[symbol] || `符号 ${symbol}`;
}

// ─── CLI ───────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  let dryRun = false;
  let targetPath = "";
  let analysisPath = "";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--check") dryRun = true;
    else if (args[i] === "--fix") dryRun = false;
    else if (args[i] === "--analysis" && i + 1 < args.length) { analysisPath = args[i + 1]; i++; }
    else if (!args[i].startsWith("--")) targetPath = args[i];
  }

  if (!targetPath) {
    console.error("Usage: node slide_symbol_scanner.js [--check|--fix] <path-to-slides.json>");
    process.exit(1);
  }

  if (!fs.existsSync(targetPath)) {
    console.error("File not found:", targetPath);
    process.exit(1);
  }

  scanAndFix(targetPath, dryRun, analysisPath);
}

main();
