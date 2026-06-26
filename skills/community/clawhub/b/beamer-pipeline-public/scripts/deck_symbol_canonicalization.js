"use strict";

function uniqueStrings(values) {
  return [...new Set((Array.isArray(values) ? values : []).filter(Boolean))];
}

function normalizeSimpleSubscriptNotation(symbol) {
  return String(symbol || "").replace(
    /^((?:\\[A-Za-z]+)|[A-Za-z]|[ΔΩωγθαβφνδμξεϵ])_([A-Za-z0-9]+)$/u,
    "$1_{$2}",
  );
}

function normalizeLooseSubscriptBraces(symbol) {
  return String(symbol || "")
    .replace(/^((?:\\[A-Za-z]+)|[A-Za-z]+|[ΔΩωγθαβφνδμξεϵ])_([A-Za-z0-9]+)\}+$/u, "$1_{$2}")
    .replace(/^((?:\\[A-Za-z]+)|[A-Za-z]+|[ΔΩωγθαβφνδμξεϵ])_\{([^{}]+)\}\}+$/u, "$1_{$2}");
}

const STYLED_LATIN_LETTER_MAP = new Map([
  ...[..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].map((letter, index) => [String.fromCodePoint(0x1d4d0 + index), letter]),
  ...[..."abcdefghijklmnopqrstuvwxyz"].map((letter, index) => [String.fromCodePoint(0x1d4ea + index), letter]),
  ...[
    ["𝒜", "A"], ["ℬ", "B"], ["𝒞", "C"], ["𝒟", "D"], ["ℰ", "E"], ["ℱ", "F"], ["𝒢", "G"],
    ["ℋ", "H"], ["ℐ", "I"], ["𝒥", "J"], ["𝒦", "K"], ["ℒ", "L"], ["ℳ", "M"], ["𝒩", "N"],
    ["𝒪", "O"], ["𝒫", "P"], ["𝒬", "Q"], ["ℛ", "R"], ["𝒮", "S"], ["𝒯", "T"], ["𝒰", "U"],
    ["𝒱", "V"], ["𝒲", "W"], ["𝒳", "X"], ["𝒴", "Y"], ["𝒵", "Z"],
    ["𝒶", "a"], ["𝒷", "b"], ["𝒸", "c"], ["𝒹", "d"], ["ℯ", "e"], ["𝒻", "f"], ["ℊ", "g"],
    ["𝒽", "h"], ["𝒾", "i"], ["𝒿", "j"], ["𝓀", "k"], ["𝓁", "l"], ["𝓂", "m"], ["𝓃", "n"],
    ["ℴ", "o"], ["𝓅", "p"], ["𝓆", "q"], ["𝓇", "r"], ["𝓈", "s"], ["𝓉", "t"], ["𝓊", "u"],
    ["𝓋", "v"], ["𝓌", "w"], ["𝓍", "x"], ["𝓎", "y"], ["𝓏", "z"],
  ],
]);

function normalizeStyledLatinLetters(text) {
  return [...String(text || "")].map((char) => STYLED_LATIN_LETTER_MAP.get(char) || char).join("");
}

function stripTexStyleWrappers(text) {
  let normalized = String(text || "");
  let previous = "";
  while (normalized !== previous) {
    previous = normalized;
    normalized = normalized
      .replace(/\\(?:mathrm|mathit|mathbf|mathsf|mathtt|operatorname|texttt|textrm|boldsymbol|bm|mathcal|mathscr|mathbb|mathfrak)\{([^{}]*)\}/g, "$1")
      .replace(/\\(?:mathrm|mathit|mathbf|mathsf|mathtt|operatorname|texttt|textrm|boldsymbol|bm|mathcal|mathscr|mathbb|mathfrak)\s*(\\[A-Za-z]+(?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z])/g, "$1")
      .replace(/\\text\{([^{}]*)\}/g, "$1");
  }
  return normalizeStyledLatinLetters(normalized);
}

function normalizeNotationSymbolText(symbol) {
  let normalized = String(symbol || "").trim();
  if (!normalized) return "";
  if (
    (normalized.startsWith("`") && normalized.endsWith("`"))
    || (normalized.startsWith('"') && normalized.endsWith('"'))
    || (normalized.startsWith("'") && normalized.endsWith("'"))
  ) {
    normalized = normalized.slice(1, -1).trim();
  }
  let changed = true;
  while (changed) {
    changed = false;
    if (/^\$([\s\S]+)\$$/.test(normalized)) {
      normalized = normalized.replace(/^\$([\s\S]+)\$$/, "$1").trim();
      changed = true;
    }
    if (/^\\\(([\s\S]+)\\\)$/.test(normalized)) {
      normalized = normalized.replace(/^\\\(([\s\S]+)\\\)$/, "$1").trim();
      changed = true;
    }
    if (/^\\\[([\s\S]+)\\\]$/.test(normalized)) {
      normalized = normalized.replace(/^\\\[([\s\S]+)\\\]$/, "$1").trim();
      changed = true;
    }
    const strippedFontWrappers = stripTexStyleWrappers(normalized);
    if (strippedFontWrappers !== normalized) {
      normalized = strippedFontWrappers.trim();
      changed = true;
    }
  }
  return normalized
    .replace(/\\_/g, "_")
    .replace(/\\\{/g, "{")
    .replace(/\\\}/g, "}")
    .trim();
}

const STRUCTURED_ARTIFACT_FIELD_SYMBOLS = new Set([
  "artifact_paths",
  "body_appendix_split",
  "conclusion_preview_page",
  "equation_blocks",
  "equation_coverage",
  "figure_coverage",
  "formal_statement_inventory",
  "notation_coverage",
  "paragraph_ledger",
  "roadmap_page",
  "speaker_notes",
  "table_coverage",
  "timing_plan",
  "visible_equation_blocks",
]);

function isStructuredArtifactFieldSymbol(symbol) {
  const normalized = String(symbol || "")
    .trim()
    .replace(/\\_/g, "_")
    .replace(/[^A-Za-z0-9_]+/g, "")
    .toLowerCase();
  return STRUCTURED_ARTIFACT_FIELD_SYMBOLS.has(normalized);
}

function canonicalizeSymbolToken(symbol) {
  const greekMap = new Map([
    ["∂Ω", "\\partial\\Omega"],
    ["Δ", "\\Delta"],
    ["Ω", "\\Omega"],
    ["ω", "\\omega"],
    ["γ", "\\gamma"],
    ["θ", "\\theta"],
    ["α", "\\alpha"],
    ["β", "\\beta"],
    ["φ", "\\phi"],
    ["ν", "\\nu"],
    ["δ", "\\delta"],
    ["μ", "\\mu"],
    ["ξ", "\\xi"],
    ["ε", "\\varepsilon"],
    ["ϵ", "\\varepsilon"],
  ]);
  const combiningAccentMap = new Map([
    ["\u0300", "grave"],
    ["\u0301", "acute"],
    ["\u0302", "hat"],
    ["\u0303", "tilde"],
    ["\u0304", "bar"],
    ["\u0306", "breve"],
    ["\u0307", "dot"],
    ["\u0308", "ddot"],
    ["\u030c", "check"],
    ["\u20d7", "vec"],
  ]);
  let normalized = normalizeStyledLatinLetters(String(symbol || ""))
    .replace(/ℝ/g, "R")
    .replace(/∈/g, "\\in")
    .replace(/×/g, "\\times")
    .replace(/\s+/g, "")
    .trim();
  if (!normalized) return "";
  normalized = normalizeLooseSubscriptBraces(normalized);
  const decoratedMatch = normalized.normalize("NFD").match(/^(.+?)([\u0300-\u036f\u20d7]+)$/u);
  if (decoratedMatch) {
    let [, baseToken, combiningMarks] = decoratedMatch;
    baseToken = normalizeSimpleSubscriptNotation(baseToken);
    for (const [source, replacement] of greekMap.entries()) {
      baseToken = baseToken.split(source).join(replacement);
    }
    if (baseToken) {
      let accented = baseToken;
      let supported = true;
      for (const mark of [...combiningMarks]) {
        const accentMacro = combiningAccentMap.get(mark);
        if (!accentMacro) {
          supported = false;
          break;
        }
        const simpleAccentTarget = /^\\[A-Za-z]+(?:_\{[A-Za-z0-9]+\})?$/.test(accented);
        accented = simpleAccentTarget ? `\\${accentMacro}${accented}` : `\\${accentMacro}{${accented}}`;
      }
      if (supported) {
        normalized = accented;
      }
    }
  }
  normalized = normalizeSimpleSubscriptNotation(normalized);
  for (const [source, replacement] of greekMap.entries()) {
    normalized = normalized.split(source).join(replacement);
  }
  if (normalized.startsWith("\\epsilon")) {
    normalized = `\\varepsilon${normalized.slice("\\epsilon".length)}`;
  }
  if (/^g\([A-Za-z]\)$/.test(normalized)) {
    return normalized;
  }
  return normalized;
}

function splitNotationSymbolPieces(symbol) {
  const raw = normalizeNotationSymbolText(symbol);
  if (!raw) return [];
  const pieces = [];
  let current = "";
  let depth = 0;
  for (const char of raw) {
    if (char === "(" || char === "[" || char === "{") {
      depth += 1;
      current += char;
      continue;
    }
    if (char === ")" || char === "]" || char === "}") {
      depth = Math.max(0, depth - 1);
      current += char;
      continue;
    }
    if (depth === 0 && (char === "/" || char === "," || char === ";")) {
      const piece = current.trim();
      if (piece) pieces.push(piece);
      current = "";
      continue;
    }
    current += char;
  }
  const tail = current.trim();
  if (tail) pieces.push(tail);
  return pieces;
}

function symbolCandidatesFromNotationEntry(symbol) {
  const raw = normalizeNotationSymbolText(symbol);
  if (!raw || /UNKNOWN_RECOVERED_SYMBOL/i.test(raw)) return [];
  if (isStructuredArtifactFieldSymbol(raw)) return [];
  const pieces = splitNotationSymbolPieces(raw);
  const expanded = [];
  const greekWithIndexMap = {
    "Δ": "\\Delta",
    "Ω": "\\Omega",
    "ω": "\\omega",
    "γ": "\\gamma",
    "θ": "\\theta",
    "α": "\\alpha",
    "β": "\\beta",
    "φ": "\\phi",
    "ν": "\\nu",
    "δ": "\\delta",
    "μ": "\\mu",
    "ξ": "\\xi",
    "ε": "\\varepsilon",
    "ϵ": "\\varepsilon",
  };
  for (const piece of pieces) {
    expanded.push(piece);
    if (/^\\[A-Za-z]+$/.test(piece)) {
      expanded.push(piece.replace(/^\\/, ""));
    }
    const macroWithArgs = piece.match(/^(\\[A-Za-z]+)(\(.+\))$/);
    if (macroWithArgs) {
      expanded.push(macroWithArgs[1]);
    }
    const indexedSymbol = piece.match(/^((?:\\[A-Za-z]+)|[A-Za-z]|[ΔΩωγθαβφνδμξεϵ])_(\{[^}]+\}|[A-Za-z0-9]+)(\(.+\))?$/u);
    if (indexedSymbol) {
      const [, baseSymbol, , suffix = ""] = indexedSymbol;
      expanded.push(baseSymbol);
      if (suffix) {
        expanded.push(`${baseSymbol}${suffix}`);
      }
    }
    if (/^g\([A-Za-z]\)$/.test(piece)) {
      expanded.push(piece.replace(/\([A-Za-z]\)$/, ""));
    }
    const greekNameWithIndex = piece.match(/^(Delta|Omega|omega|gamma|theta|alpha|beta|phi|nu|delta|mu|xi|epsilon|varepsilon)_(\{[^}]+\}|[A-Za-z0-9]+)$/);
    if (greekNameWithIndex) {
      const [, greekName, index] = greekNameWithIndex;
      const macroName = greekName === "epsilon" ? "varepsilon" : greekName;
      expanded.push(`\\${macroName}_${index}`);
      if (!/^\{[^}]+\}$/.test(index)) expanded.push(`\\${macroName}_{${index}}`);
    }
    const greekWithIndex = piece.match(/^([ΔΩωγθαβφνδμξεϵ])(\d+)$/u);
    if (greekWithIndex) {
      const [, greek, index] = greekWithIndex;
      expanded.push(`${greek}_${index}`);
      expanded.push(`${greek}_{${index}}`);
      if (greekWithIndexMap[greek]) {
        expanded.push(`${greekWithIndexMap[greek]}_${index}`);
        expanded.push(`${greekWithIndexMap[greek]}_{${index}}`);
      }
    }
    const indexedFunction = piece.match(/^([A-Za-z])(\d+)(\(.+\))$/);
    if (indexedFunction) {
      const [, base, index, suffix] = indexedFunction;
      expanded.push(`${base}_${index}${suffix}`);
      expanded.push(`${base}_{${index}}${suffix}`);
    }
  }
  return uniqueStrings(expanded.map(canonicalizeSymbolToken));
}

function escapeNonSubscriptUnderscores(text) {
  let normalized = String(text || "");
  let previous = "";
  while (normalized !== previous) {
    previous = normalized;
    normalized = normalized.replace(/([A-Za-z0-9])_([A-Za-z0-9])/g, "$1\\\\_$2");
  }
  return normalized;
}

function normalizeTexSymbolHaystack(text) {
  const normalized = stripTexStyleWrappers(text);
  return normalized
    .replace(/\\_/g, "_")
    .replace(/\\\{/g, "{")
    .replace(/\\\}/g, "}")
    .replace(/\\([,:;!])/g, "$1");
}

function textContainsSymbolCandidate(candidate, text) {
  const haystack = String(text || "");
  const unescapedHaystack = haystack.includes("\\\\") ? haystack.replace(/\\\\/g, "\\") : haystack;
  const normalizedHaystack = normalizeTexSymbolHaystack(haystack);
  const normalizedUnescapedHaystack = normalizeTexSymbolHaystack(unescapedHaystack);
  const needle = canonicalizeSymbolToken(normalizeNotationSymbolText(candidate));
  if (!needle || !haystack) return false;
  const variants = new Set([needle]);
  const unicodeMap = {
    "Δ": "\\Delta",
    "\\Delta": "Δ",
    "\\Omega": "Ω",
    "\\omega": "ω",
    "\\gamma": "γ",
    "\\theta": "θ",
    "\\alpha": "α",
    "\\beta": "β",
    "\\phi": "φ",
    "\\nu": "ν",
    "\\delta": "δ",
    "\\mu": "μ",
    "\\xi": "ξ",
    "\\epsilon": "ε",
    "\\varepsilon": "ε",
    "\\partial\\Omega": "∂Ω",
  };
  if (unicodeMap[needle]) variants.add(unicodeMap[needle]);
  if (needle.startsWith("\\")) variants.add(needle.replace(/^\\/, ""));
  if (!needle.startsWith("\\") && /^[A-Za-z]+(?:_\{?[A-Za-z0-9]+\}?)?$/.test(needle)) variants.add(`\\${needle}`);
  if (needle.includes("_{")) variants.add(needle.replace(/_\{([^}]+)\}/g, "_$1"));
  if (/_[A-Za-z0-9]+/.test(needle)) variants.add(needle.replace(/_([A-Za-z0-9]+)/g, "_{$1}"));
  if (needle.includes("_")) variants.add(escapeNonSubscriptUnderscores(needle));
  if (/^g\([A-Za-z]\)$/.test(needle)) variants.add(needle.replace(/\([A-Za-z]\)$/, ""));
  const accentNoBraceMatch = needle.match(/^\\(tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)(\\[A-Za-z]+(?:_\{[A-Za-z0-9]+\})?)$/);
  if (accentNoBraceMatch) variants.add(`\\${accentNoBraceMatch[1]}{${accentNoBraceMatch[2]}}`);
  const accentBracedMatch = needle.match(/^\\(tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)\{(.+)\}$/);
  if (accentBracedMatch) variants.add(`\\${accentBracedMatch[1]}${accentBracedMatch[2]}`);
  // Handle accent braces embedded inside a larger symbol, e.g.
  // \\hat{r}_t vs \\hat r_t, and W_t^{\\hat{r}} vs W_t^{\\hat r}.
  for (const variant of [...variants]) {
    if (/\\(?:tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)\{[^{}]+\}/.test(variant)) {
      variants.add(variant.replace(/\\(tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)\{([^{}]+)\}/g, "\\$1$2"));
      variants.add(variant.replace(/\\(tilde|hat|bar|breve|acute|grave|dot|ddot|check|vec)\{([^{}]+)\}/g, "\\$1 $2"));
    }
  }
  if (needle.includes(";")) variants.add(needle.replace(/;/g, "\\;"));
  for (const variant of [...variants]) {
    if (variant.includes("_")) {
      variants.add(escapeNonSubscriptUnderscores(variant));
    }
  }
  for (const variant of [...variants]) {
    if (variant.startsWith("\\varepsilon")) {
      variants.add(`\\epsilon${variant.slice("\\varepsilon".length)}`);
    }
    if (variant.startsWith("\\epsilon")) {
      variants.add(`\\varepsilon${variant.slice("\\epsilon".length)}`);
    }
  }
  const haystacks = [
    haystack,
    haystack.replace(/\s+/g, ""),
    unescapedHaystack,
    unescapedHaystack.replace(/\s+/g, ""),
    normalizedHaystack,
    normalizedHaystack.replace(/\s+/g, ""),
    normalizedUnescapedHaystack,
    normalizedUnescapedHaystack.replace(/\s+/g, ""),
  ];
  return [...variants].some((variant) => {
    if (!variant) return false;
    const compactVariant = String(variant).replace(/\s+/g, "");
    return haystacks.some((entry) => entry.includes(variant) || entry.includes(compactVariant));
  });
}

function isGenericDifferentialToken(token) {
  const value = String(token || "").trim();
  // Differential terms such as dv_t, dr_t, and dW_t are operators attached to
  // state/Brownian variables in SDEs, not standalone notation entries that
  // should be forced into notation_coverage.
  return /^d[A-Za-z]+_\{?[A-Za-z0-9]+\}?$/i.test(value);
}

function isLikelyDerivativeSubscriptToken(token) {
  const value = String(token || "").trim();
  // Terms such as f_{vv}, f_{rr}, f_{\zeta\zeta} denote partial derivatives
  // of a covered function, not independent notation items.
  return /^[A-Za-z]_\{?(?:[A-Za-z]{2,}|\\[A-Za-z]+\\[A-Za-z]+)\}?$/.test(value);
}

function extractLikelyMathSymbolsFromEquationText(text) {
  const raw = String(text || "");
  const sanitized = stripTexStyleWrappers(raw)
    .replace(/\\(?:label|ref|eqref|autoref|cref|Cref)\{[^}]*\}/g, " ")
    .replace(/\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}/g, " ");
  const tokens = new Set();
  for (const match of sanitized.matchAll(/\\partial\s*\\Omega/g)) tokens.add("\\partial\\Omega");
  for (const match of sanitized.matchAll(/\\Omega/g)) tokens.add("\\Omega");
  for (const match of sanitized.matchAll(/\\(?:theta|omega|gamma|alpha|beta|phi|nu|delta|mu|xi|varepsilon|epsilon)(?:_\{[A-Za-z0-9]+\}|_[A-Za-z0-9])?/g)) tokens.add(match[0]);
  for (const match of sanitized.matchAll(/\b[a-zA-Z]+_\{[a-zA-Z0-9]+\}/g)) {
    const startIndex = Number(match.index || 0);
    if (startIndex > 0 && sanitized[startIndex - 1] === "\\") continue;
    tokens.add(match[0]);
  }
  for (const match of sanitized.matchAll(/\b[a-zA-Z]+_[a-zA-Z0-9]\b/g)) {
    const startIndex = Number(match.index || 0);
    if (startIndex > 0 && sanitized[startIndex - 1] === "\\") continue;
    tokens.add(match[0]);
  }
  for (const match of sanitized.matchAll(/\bg\([A-Za-z]\)/g)) tokens.add(match[0]);
  const ignore = new Set([
    "\\alpha",
    "\\phi",
    "\\nu",
    "equation_blocks",
    "r_l",
    "z_l",
    "x_l",
    "\\theta_l",
  ]);
  return uniqueStrings([...tokens]
    .map(canonicalizeSymbolToken)
    .filter((token) => token
      && !ignore.has(token)
      && !isStructuredArtifactFieldSymbol(token)
      && !isGenericDifferentialToken(token)
      && !isLikelyDerivativeSubscriptToken(token)));
}

module.exports = {
  canonicalizeSymbolToken,
  escapeNonSubscriptUnderscores,
  extractLikelyMathSymbolsFromEquationText,
  isStructuredArtifactFieldSymbol,
  normalizeLooseSubscriptBraces,
  normalizeNotationSymbolText,
  normalizeSimpleSubscriptNotation,
  normalizeTexSymbolHaystack,
  splitNotationSymbolPieces,
  stripTexStyleWrappers,
  symbolCandidatesFromNotationEntry,
  textContainsSymbolCandidate,
};
