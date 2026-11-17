/**
 * caniemail-ai-tooling — selector shape detection.
 *
 * Answers the eleven structural questions the dataset asks about a selector —
 * does it use a child combinator, an attribute selector, chaining, and so on —
 * plus which pseudo-classes and pseudo-elements it names.
 *
 * This needs a tokenizer rather than a set of regexes, and the fixtures say why:
 * `[title="a > b"]` contains no child combinator and `.safe:not(.x + .y)` no
 * adjacent sibling combinator, but a regex reports both. A pseudo-class's
 * argument list is deliberately *not* descended into — `:not(a > b)` is one
 * simple selector, and the shapes inside it are not shapes of the selector.
 *
 * Vendored byte-identically into `skill/scripts/` and `mcp/src/`; never edit a
 * vendored copy, edit this file and run `make sync-core`.
 */

import { isWhitespace, skipString, skipWhitespace } from './css-scan.mjs';

export const ADJACENT_SIBLING = 'Adjacent sibling combinator';
export const ATTRIBUTE = 'Attribute selector';
export const CHAINING = 'Chaining selectors';
export const CHILD = 'Child combinator';
export const CLASS = 'Class selector';
export const DESCENDANT = 'Descendant combinator';
export const GENERAL_SIBLING = 'General sibling combinator';
export const GROUPING = 'Grouping selectors';
export const ID = 'ID selector';
export const TYPE = 'Type selector';
export const UNIVERSAL = 'Universal selector *';

/** @type {Partial<Record<string, string>>} */
const COMBINATOR_SHAPES = { '>': CHILD, '+': ADJACENT_SIBLING, '~': GENERAL_SIBLING };

/**
 * @typedef {object} SelectorAnalysis
 * @property {Set<string>} shapes  Feature titles for the shapes present.
 * @property {Set<string>} pseudos Bare pseudo names, e.g. `hover`, `nth-child`.
 * @property {boolean} nesting     Whether the selector uses `&`.
 */

/**
 * Analyse one complex selector — no commas; split the list first.
 *
 * @param {string} selector
 * @returns {SelectorAnalysis}
 */
export function analyzeSelector(selector) {
  const shapes = new Set();
  const pseudos = new Set();
  let nesting = false;

  const text = String(selector);
  const length = text.length;
  let i = 0;
  // Class tokens in the compound being read. Chaining is `.one.two` — two
  // classes on *one* element — so the count resets at every combinator.
  let classesInCompound = 0;
  let compoundHasSimple = false;

  while (i < length) {
    const char = text[i];

    if (isWhitespace(char)) {
      const next = skipWhitespace(text, i);
      // Whitespace is a descendant combinator only when it separates two
      // compounds. Around an explicit combinator it is just padding.
      if (compoundHasSimple && next < length && !'>+~'.includes(text[next])) {
        shapes.add(DESCENDANT);
        classesInCompound = 0;
        compoundHasSimple = false;
      }
      i = next;
      continue;
    }

    const combinator = COMBINATOR_SHAPES[char];
    if (combinator) {
      shapes.add(combinator);
      classesInCompound = 0;
      compoundHasSimple = false;
      i += 1;
      continue;
    }

    if (char === '&') {
      nesting = true;
      compoundHasSimple = true;
      i += 1;
      continue;
    }

    if (char === '*') {
      shapes.add(UNIVERSAL);
      compoundHasSimple = true;
      i += 1;
      continue;
    }

    if (char === '.') {
      i = readIdentifier(text, i + 1);
      shapes.add(CLASS);
      classesInCompound += 1;
      if (classesInCompound >= 2) shapes.add(CHAINING);
      compoundHasSimple = true;
      continue;
    }

    if (char === '#') {
      i = readIdentifier(text, i + 1);
      shapes.add(ID);
      compoundHasSimple = true;
      continue;
    }

    if (char === '[') {
      const close = skipBracketed(text, i);
      const name = attributeName(text.slice(i + 1, close - 1));
      // `[class~="x"]` is a class selector spelled the long way, and `[id=…]`
      // an ID selector; neither is what the dataset means by "attribute
      // selector", which is about non-class, non-id attributes.
      if (name === 'class') {
        shapes.add(CLASS);
        classesInCompound += 1;
        if (classesInCompound >= 2) shapes.add(CHAINING);
      } else if (name === 'id') {
        shapes.add(ID);
      } else {
        shapes.add(ATTRIBUTE);
      }
      compoundHasSimple = true;
      i = close;
      continue;
    }

    if (char === ':') {
      let j = i + 1;
      if (text[j] === ':') j += 1;
      const nameEnd = readIdentifier(text, j);
      const name = text.slice(j, nameEnd).toLowerCase();
      if (name) pseudos.add(name);
      // The argument list is a selector in its own right, and its shapes are
      // not this selector's shapes. Step over it without looking inside.
      i = text[nameEnd] === '(' ? skipParenthesised(text, nameEnd) : nameEnd;
      compoundHasSimple = true;
      continue;
    }

    if (isIdentifierChar(char) || char === '\\') {
      const end = readIdentifier(text, i);
      if (end > i) {
        shapes.add(TYPE);
        compoundHasSimple = true;
        i = end;
        continue;
      }
    }

    i += 1;
  }

  return { shapes, pseudos, nesting };
}

/**
 * Analyse a whole selector list, as written on one rule.
 *
 * Grouping lives here rather than in `analyzeSelector` because it is a property
 * of the list, not of any one selector in it. The previous implementation asked
 * each comma-separated selector whether it was a group, so the answer was
 * always no and `Grouping selectors` could never be reported.
 *
 * @param {string[]} selectors
 * @returns {SelectorAnalysis}
 */
export function analyzeSelectorList(selectors) {
  const shapes = new Set();
  const pseudos = new Set();
  let nesting = false;

  if (selectors.length >= 2) shapes.add(GROUPING);
  for (const selector of selectors) {
    const analysis = analyzeSelector(selector);
    for (const shape of analysis.shapes) shapes.add(shape);
    for (const pseudo of analysis.pseudos) pseudos.add(pseudo);
    nesting ||= analysis.nesting;
  }

  return { shapes, pseudos, nesting };
}

/**
 * The attribute name in the body of a `[...]`, before any operator.
 *
 * @param {string} body
 */
function attributeName(body) {
  const match = /^\s*([^\s~^|$*=\]]+)/.exec(body);
  return match ? match[1].replace(/^.*\|/, '').toLowerCase() : '';
}

/**
 * @param {string} text
 * @param {number} from
 */
function readIdentifier(text, from) {
  let i = from;
  while (i < text.length) {
    if (text[i] === '\\') {
      i = escapeEnd(text, i);
      continue;
    }
    if (!isIdentifierChar(text[i])) break;
    i += 1;
  }
  return i;
}

/**
 * One past the escape starting at the backslash at `from`.
 *
 * A hex escape is up to six hex digits and then one optional whitespace, which
 * belongs to the escape: `.\\31 0` is the class `10`, not a class `1` with a
 * descendant `0`. Any other escape is the backslash and one character. Only
 * identifiers need this; everywhere else an escape is stepped over inside a
 * string, group or bracket where the whitespace after it is not syntax.
 *
 * @param {string} text
 * @param {number} from
 */
function escapeEnd(text, from) {
  let i = from + 1;
  const digitsEnd = Math.min(i + 6, text.length);
  while (i < digitsEnd && /[0-9a-f]/i.test(text[i])) i += 1;
  if (i === from + 1) return from + 2;
  if (text[i] === '\r' && text[i + 1] === '\n') return i + 2;
  return isWhitespace(text[i] ?? '') ? i + 1 : i;
}

/** @param {string} char */
function isIdentifierChar(char) {
  return /[^\s.#[\]():+>~*,'"\\]/.test(char);
}

/**
 * @param {string} text
 * @param {number} from
 */
function skipParenthesised(text, from) {
  let depth = 0;
  let i = from;
  while (i < text.length) {
    const char = text[i];
    if (char === '\\') {
      i += 2;
      continue;
    }
    if (char === '"' || char === "'") {
      i = skipString(text, i);
      continue;
    }
    if (char === '(') depth += 1;
    else if (char === ')') {
      depth -= 1;
      if (depth === 0) return i + 1;
    }
    i += 1;
  }
  return text.length;
}

/**
 * @param {string} text
 * @param {number} from
 */
function skipBracketed(text, from) {
  let i = from + 1;
  while (i < text.length) {
    const char = text[i];
    if (char === '\\') {
      i += 2;
      continue;
    }
    if (char === '"' || char === "'") {
      i = skipString(text, i);
      continue;
    }
    if (char === ']') return i + 1;
    i += 1;
  }
  return text.length;
}
