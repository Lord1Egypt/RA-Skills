#!/usr/bin/env node

// Cavepony v0.3.0 Compression Engine - now with BIDIRECTIONAL token mapping 🐴
// why use many token when pony do trick... and undo trick too

const fs = require('fs');
const path = require('path');

// Load dictionaries
const ponyDict = JSON.parse(fs.readFileSync(path.join(__dirname, 'pony-dict.json'), 'utf8'));
const tokenDict = JSON.parse(fs.readFileSync(path.join(__dirname, 'token-dict.json'), 'utf8'));

let canterlotDict;
try {
  canterlotDict = JSON.parse(fs.readFileSync(path.join(__dirname, 'canterlot-dict.json'), 'utf8'));
} catch (error) {
  canterlotDict = { substitutions: [], prefixes: [], suffixes: [] };
}

// Build reverse lookup maps for expansion
const phraseToToken = new Map();
const tokenToPhrase = new Map();

tokenDict.mappings.forEach(({ phrase, token }) => {
  phraseToToken.set(phrase.toLowerCase(), token);
  // First phrase wins for token→phrase — prefer the primary variant
  if (!tokenToPhrase.has(token)) {
    tokenToPhrase.set(token, phrase);
  }
});

// Sort phrases by length descending for greedy matching
const sortedPhrases = [...phraseToToken.keys()].sort((a, b) => b.length - a.length);

// Sort tokens by length descending so multi-char tokens match first
const sortedTokens = [...tokenToPhrase.keys()].sort((a, b) => b.length - a.length);

/**
 * Apply a substitution, preserving case when possible
 */
function substitute(text, pattern, replacement) {
  const regex = new RegExp(pattern, 'gi');
  return text.replace(regex, (match) => {
    if (match[0] === match[0].toUpperCase()) {
      return replacement.charAt(0).toUpperCase() + replacement.slice(1);
    }
    return replacement;
  });
}

/**
 * Compress text using token substitution (bidirectional-safe)
 * Replaces phrases with short unicode tokens. Fully reversible with expand().
 * @param {string} text - Input text
 * @param {object} opts - { pony: bool, dropArticles: bool, dropFiller: bool, ultra: bool }
 * @returns {string} Token-compressed text
 */
function compressTokens(text, opts = {}) {
  if (!text || text.trim() === '') return text;
  let compressed = text;

  // Step 1: Pony substitutions (if enabled)
  if (opts.pony) {
    const sorted = [...ponyDict.substitutions].sort((a, b) =>
      b.pattern.length - a.pattern.length
    );
    sorted.forEach(({ pattern, replacement }) => {
      compressed = substitute(compressed, pattern, replacement);
    });
  }

  // Step 2: Token substitution (bidirectional-safe)
  // Use a sentinel to avoid replacing inside words
  sortedPhrases.forEach(phrase => {
    const token = phraseToToken.get(phrase);
    // Case-insensitive, whole phrase match
    const regex = new RegExp(`\\b${phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
    compressed = compressed.replace(regex, (match) => {
      // Wrap token in sentinels so expand can find it reliably
      return `\u0001${token}\u0001`;
    });
  });

  // Step 3: Destructive compression (only if requested — NOT reversible)
  if (opts.dropFiller) {
    const fillerPhrases = [
      "sure!", "absolutely!", "thank you", "thanks",
      "would you mind", "could you", "would you",
      "if you could", "if you would",
    ];
    fillerPhrases.forEach(phrase => {
      const regex = new RegExp(`\\b${phrase}\\b`, 'gi');
      compressed = compressed.replace(regex, '');
    });
  }

  if (opts.dropArticles) {
    compressed = compressed.replace(/\b([,;]?\s*)(a|an|the)\s+/gi, '$1');
    compressed = compressed.replace(/^the\s+/i, '');
    compressed = compressed.replace(/\bjust\b(?!\s*=)/gi, '');
  }

  if (opts.ultra) {
    // Ultra: drop forms of "to be", shorten common words
    compressed = compressed.replace(/\b(am|is|are|was|were|be|been|being)\s+/gi, '');
    const ultraReplacements = [
      [/because/gi, 'bc'], [/approximately/gi, '~'],
      [/important/gi, 'key'], [/problem/gi, 'bug'],
      [/issue/gi, 'bug'], [/configuration/gi, 'conf'],
      [/parameter/gi, 'param'], [/function/gi, 'fn'],
      [/variable/gi, 'var'], [/authentication/gi, 'auth'],
      [/information/gi, 'info'], [/application/gi, 'app'],
      [/environment/gi, 'env'], [/repository/gi, 'repo'],
      [/developer/gi, 'dev'], [/development/gi, 'dev'],
      [/production/gi, 'prod'], [/database/gi, 'db'],
      [/request/gi, 'req'], [/response/gi, 'res'],
      [/document/gi, 'doc'], [/reference/gi, 'ref'],
    ];
    ultraReplacements.forEach(([pattern, replacement]) => {
      compressed = compressed.replace(pattern, replacement);
    });
  }

  // Clean up whitespace, remove sentinels (they're invisible anyway but clean for display)
  compressed = compressed.replace(/\u0001/g, '');
  compressed = compressed.replace(/\s{2,}/g, ' ').trim();
  compressed = compressed.replace(/^[,;:\s]+/, '');

  return fixSentenceCase(compressed);
}

/**
 * Expand token-compressed text back to natural language
 * Reverses token substitution. Only works on token-compressed text.
 * Pony substitutions and destructive modes (dropArticles, ultra) are NOT reversible.
 * @param {string} text - Token-compressed text
 * @returns {string} Expanded natural language text
 */
function expand(text) {
  if (!text || text.trim() === '') return text;
  let expanded = text;

  // Replace tokens with their phrases — longest tokens first
  sortedTokens.forEach(token => {
    const phrase = tokenToPhrase.get(token);
    const isAlpha = /^[a-zA-Z0-9.]+$/.test(token);

    let regex;
    if (isAlpha) {
      // Alpha tokens: match as whole word only
      const escapedToken = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      regex = new RegExp(`\\b${escapedToken}\\b`, 'gu');
    } else {
      // Symbol tokens: match surrounded by non-alpha or boundaries
      const escapedToken = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      regex = new RegExp(`(?<=^|[\\s,;:!?])${escapedToken}(?=$|[\\s,.;:!?])`, 'gu');
    }

    expanded = expanded.replace(regex, () => phrase);
  });

  // Fix double spaces and sentence case
  expanded = expanded.replace(/\s{2,}/g, ' ').trim();
  return fixSentenceCase(expanded);
}

/**
 * Expand text into Canterlot fancy speech
 * @param {string} text - Input text
 * @returns {string} Canterlot expanded text
 */
function expandToCanterlot(text) {
  if (!text || text.trim() === '') return text;

  let expanded = text;

  // FIRST: Apply pony substitutions (Canterlot is fancy pony speech!)
  const sortedPony = [...ponyDict.substitutions].sort((a, b) =>
    b.pattern.length - a.pattern.length
  );

  sortedPony.forEach(({ pattern, replacement }) => {
    expanded = substitute(expanded, pattern, replacement);
  });

  // THEN: Apply fancy substitutions
  canterlotDict.substitutions.forEach(({ pattern, replacement }) => {
    const regex = new RegExp(pattern, 'gi');
    expanded = expanded.replace(regex, (match) => {
      if (match[0] === match[0].toUpperCase()) {
        return replacement.charAt(0).toUpperCase() + replacement.slice(1);
      }
      return replacement;
    });
  });

  // Add fancy prefixes occasionally
  const sentences = expanded.split(/(?<=[.!?])\s+/);
  if (sentences.length > 0 && canterlotDict.prefixes && canterlotDict.prefixes.length > 0) {
    const randomPrefix = canterlotDict.prefixes[Math.floor(Math.random() * canterlotDict.prefixes.length)];
    expanded = randomPrefix + ', ' + expanded.charAt(0).toLowerCase() + expanded.slice(1);
  }

  // Add fancy suffixes occasionally
  if (canterlotDict.suffixes && canterlotDict.suffixes.length > 0 && Math.random() > 0.7) {
    const randomSuffix = canterlotDict.suffixes[Math.floor(Math.random() * canterlotDict.suffixes.length)];
    expanded = expanded.replace(/[.!?]$/, '') + randomSuffix;
  }

  return fixSentenceCase(expanded);
}

/**
 * Compress text — main entry point
 * @param {string} text - Input text
 * @param {'lite'|'full'|'ultra'|'pony'|'canterlot'} mode - Compression mode
 * @returns {string} Compressed text
 */
function compress(text, mode = 'full') {
  if (!text || text.trim() === '') return text;

  // Canterlot: pure expansion, no compression
  if (mode === 'canterlot') {
    return expandToCanterlot(text);
  }

  // Map modes to options
  const opts = {
    pony: mode === 'pony',
    dropFiller: mode === 'lite' || mode === 'full' || mode === 'pony' || mode === 'ultra',
    dropArticles: mode === 'full' || mode === 'pony' || mode === 'ultra',
    ultra: mode === 'ultra',
  };

  return compressTokens(text, opts);
}

/**
 * Check if text contains cavepony tokens
 * @param {string} text - Text to check
 * @returns {bool} True if text contains tokens
 */
function hasTokens(text) {
  if (!text) return false;
  for (const token of tokenToPhrase.keys()) {
    if (text.includes(token)) return true;
  }
  return false;
}

/**
 * Get compression stats
 * @param {string} original - Original text
 * @param {string} compressed - Compressed text
 * @returns {object} Stats { originalWords, compressedWords, reduction }
 */
function stats(original, compressed) {
  const origWords = original.split(/\s+/).length;
  const newWords = compressed.split(/\s+/).length;
  const reduction = origWords > 0 ? Math.round((1 - newWords / origWords) * 100) : 0;
  return { originalWords: origWords, compressedWords: newWords, reduction };
}

/**
 * Try to fix sentence case after all the transformations
 */
function fixSentenceCase(text) {
  if (text && text.length > 0 && /^[a-z]/.test(text)) {
    const firstWord = text.split(/\s/)[0].toLowerCase();
    const capitalizeStart = ['i', 'a', 'an', 'the', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their'];
    if (!capitalizeStart.includes(firstWord.replace(/[^a-z]/g, ''))) {
      text = text.charAt(0).toUpperCase() + text.slice(1);
    }
  }
  text = text.replace(/([.!?])\s+([a-z])/g, (match, punct, letter) => {
    return punct + ' ' + letter.toUpperCase();
  });
  return text;
}

// Export for use as module
module.exports = {
  compress,
  expand,
  expandToCanterlot,
  hasTokens,
  stats,
  compressTokens,
};

// CLI mode
if (require.main === module) {
  const args = process.argv.slice(2);
  const mode = args[0] || 'full';
  const input = args.slice(1).join(' ');

  if (!input) {
    console.log("🏍️ Cavepony v0.3.0 Compression CLI");
    console.log("Usage: node compress.js <mode> <text>");
    console.log("Modes: lite, full, ultra, pony");
    console.log("Expand: node compress.js expand <compressed-text>");
    console.log("Example: node compress.js pony \"Hello human, how are you?\"");
    console.log("Round-trip: node compress.js roundtrip \"I would be happy to help\"");
    process.exit(0);
  }

  if (mode === 'expand') {
    const expanded = expand(input);
    console.log("[EXPANDED]");
    console.log("Input:", input);
    console.log("Output:", expanded);
  } else if (mode === 'roundtrip') {
    const compressed = compress(input, 'full');
    const expanded = expand(compressed);
    const s = stats(input, compressed);
    console.log("[ROUND-TRIP TEST]");
    console.log("Original:  ", input);
    console.log("Compressed:", compressed);
    console.log("Expanded:  ", expanded);
    console.log(`Stats: ${s.originalWords} → ${s.compressedWords} words (${s.reduction}% reduction)`);
    console.log("Match:", input.toLowerCase() === expanded.toLowerCase() ? '✅ EXACT' : '⚠️ PARTIAL (destructive modes strip content)');
  } else if (mode === 'demo') {
    console.log("\n🏍️ CAVEPONY v0.3.0 DEMO 🦄\n");
    const demos = [
      "I would be happy to help you with that. Let me take a look at the issue.",
      "Actually, it seems the authentication middleware has problems. I think we should fix it.",
      "For example, the configuration parameter for the database connection is wrong.",
      "On the other hand, the production environment basically works fine.",
    ];
    demos.forEach((text, i) => {
      const c = compress(text, 'full');
      const e = expand(c);
      const s = stats(text, c);
      console.log(`${i + 1}. Original:  "${text}"`);
      console.log(`   Compressed:"${c}"`);
      console.log(`   Expanded:  "${e}"`);
      console.log(`   Reduction: ${s.reduction}% (${s.originalWords}→${s.compressedWords} words)\n`);
    });
  } else {
    console.log(`[${mode.toUpperCase()} MODE]`);
    console.log("Input:", input);
    console.log("Output:", compress(input, mode));
  }
}
