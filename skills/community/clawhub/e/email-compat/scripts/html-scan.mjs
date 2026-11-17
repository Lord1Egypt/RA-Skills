/**
 * caniemail-ai-tooling — HTML scanner.
 *
 * A flat tokenizer, not a DOM. Feature detection examines every element in
 * isolation — tag name, attributes, the `style` attribute, image URLs — and
 * never asks about ancestors, siblings or descendants. Nothing here builds a
 * tree, and nothing downstream wants one.
 *
 * Offsets only. Line and column are the caller's problem, because CSS found in
 * a `<style>` block has to be measured against the document rather than against
 * the block, and that adjustment is easier on offsets than on coordinates.
 *
 * All offsets are 0-based indexes into `source`. `end` is the index of an
 * element's last character — the `>` of its closing tag — not one past it.
 *
 * Vendored byte-identically into `skill/scripts/` and `mcp/src/`; never edit a
 * vendored copy, edit this file and run `make sync-core`.
 */

import { isWhitespace } from './css-scan.mjs';

/** Elements that never have a closing tag. */
const VOID_ELEMENTS = new Set([
  'area',
  'base',
  'basefont',
  'br',
  'col',
  'command',
  'embed',
  'frame',
  'hr',
  'img',
  'input',
  'isindex',
  'keygen',
  'link',
  'meta',
  'param',
  'source',
  'track',
  'wbr',
]);

/**
 * Elements whose content is text, not markup.
 *
 * Getting this wrong is not cosmetic: `<script>` in an email routinely contains
 * `document.write("<div style='float:left'>")`, and treating that as markup
 * invents features the recipient will never see.
 */
const RAW_TEXT_ELEMENTS = new Set(['script', 'style', 'textarea', 'title', 'xmp']);

/**
 * @typedef {object} ScannedAttribute
 * @property {string} name        Lowercased.
 * @property {string} value       Empty string for a valueless attribute.
 * @property {number} valueStart  Offset of the value's first character.
 */

/**
 * @typedef {object} ScannedElement
 * @property {string} tagName                Lowercased.
 * @property {ScannedAttribute[]} attributes First occurrence wins on duplicates.
 * @property {number} start                  Offset of `<`.
 * @property {number} end                    Offset of the element's last character.
 */

/**
 * @typedef {object} HtmlScan
 * @property {ScannedElement[]} elements
 * @property {{start: number, end: number}[]} comments
 * @property {{start: number, end: number}[]} doctypes
 * @property {{textStart: number, textEnd: number}[]} styleBlocks  Half-open text ranges.
 */

/**
 * Scan HTML into a flat list of elements, comments, doctypes and style blocks.
 *
 * Tolerant by construction: unclosed tags, unquoted values, stray `<`, and
 * mismatched closing tags all degrade to something reasonable rather than
 * throwing. Malformed markup is the normal case in email.
 *
 * @param {string} source
 * @returns {HtmlScan}
 */
export function scanHtml(source) {
  /** @type {HtmlScan['elements']} */
  const elements = [];
  /** @type {HtmlScan['comments']} */
  const comments = [];
  /** @type {HtmlScan['doctypes']} */
  const doctypes = [];
  /** @type {HtmlScan['styleBlocks']} */
  const styleBlocks = [];

  /** @type {ScannedElement[]} */
  const open = [];
  const length = source.length;
  let i = 0;

  while (i < length) {
    const lt = source.indexOf('<', i);
    if (lt === -1) break;

    const next = source[lt + 1];

    if (next === '!') {
      if (source.startsWith('<!--', lt)) {
        // A conditional comment (`<!--[if mso]>…<![endif]-->`) is a comment
        // like any other. Its contents render in one client and must not be
        // reported as features of the document.
        const close = source.indexOf('-->', lt + 4);
        const end = close === -1 ? length - 1 : close + 2;
        comments.push({ start: lt, end });
        i = end + 1;
        continue;
      }
      const close = source.indexOf('>', lt);
      const end = close === -1 ? length - 1 : close;
      if (/^<!doctype/i.test(source.slice(lt, lt + 9))) doctypes.push({ start: lt, end });
      i = end + 1;
      continue;
    }

    if (next === '?') {
      const close = source.indexOf('>', lt);
      i = (close === -1 ? length - 1 : close) + 1;
      continue;
    }

    if (next === '/') {
      const nameEnd = readTagName(source, lt + 2);
      const tagName = source.slice(lt + 2, nameEnd).toLowerCase();
      const close = source.indexOf('>', nameEnd);
      const end = close === -1 ? length - 1 : close;
      closeElement(open, tagName, end, lt);
      i = end + 1;
      continue;
    }

    if (!isNameStart(next)) {
      // A bare `<` in text. Not a tag; step over it.
      i = lt + 1;
      continue;
    }

    const nameEnd = readTagName(source, lt + 1);
    const tagName = source.slice(lt + 1, nameEnd).toLowerCase();
    const tag = readAttributes(source, nameEnd);
    const element = { tagName, attributes: tag.attributes, start: lt, end: tag.tagEnd };

    if (RAW_TEXT_ELEMENTS.has(tagName) && !tag.selfClosing) {
      const textStart = tag.tagEnd + 1;
      const closeStart = findRawTextClose(source, tagName, textStart);
      const textEnd = closeStart === -1 ? length : closeStart;
      if (tagName === 'style') styleBlocks.push({ textStart, textEnd });
      if (closeStart === -1) {
        element.end = length - 1;
        i = length;
      } else {
        const close = source.indexOf('>', closeStart);
        element.end = close === -1 ? length - 1 : close;
        i = element.end + 1;
      }
      elements.push(element);
      continue;
    }

    if (tag.selfClosing || VOID_ELEMENTS.has(tagName)) {
      elements.push(element);
    } else {
      open.push(element);
      elements.push(element);
    }
    i = tag.tagEnd + 1;
  }

  // Anything still open ran to the end of the document.
  for (const element of open) element.end = Math.max(element.end, length - 1);

  return { elements, comments, doctypes, styleBlocks };
}

/**
 * Close the nearest matching open element, and everything nested inside it.
 *
 * No implied-end-tag table: `<p>a<p>b` simply nests. Only `end` offsets are
 * affected, every element is still reported with a correct `start`, and nothing
 * downstream reads the nesting.
 *
 * @param {ScannedElement[]} open  The elements still open, outermost first.
 * @param {string} tagName
 * @param {number} end  Offset of the closing tag's `>`.
 * @param {number} lt   Offset of the closing tag's `<`.
 */
function closeElement(open, tagName, end, lt) {
  for (let depth = open.length - 1; depth >= 0; depth -= 1) {
    if (open[depth].tagName !== tagName) continue;
    open[depth].end = end;
    // Elements left open inside it end where it ended.
    for (let inner = open.length - 1; inner > depth; inner -= 1) {
      open[inner].end = Math.max(open[inner].end, lt - 1);
    }
    open.length = depth;
    return;
  }
  // A closing tag with nothing open to match. Ignore it, as browsers do.
}

/** @param {string|undefined} char */
function isNameStart(char) {
  return char !== undefined && /[a-zA-Z]/.test(char);
}

/**
 * @param {string} source
 * @param {number} from
 * @returns {number} One past the tag name.
 */
function readTagName(source, from) {
  let i = from;
  while (i < source.length) {
    const char = source[i];
    if (isWhitespace(char) || char === '>' || char === '/') break;
    i += 1;
  }
  return i;
}

/**
 * Read an open tag's attributes, starting just after the tag name.
 *
 * @param {string} source
 * @param {number} from
 * @returns {{attributes: ScannedAttribute[], selfClosing: boolean, tagEnd: number}}
 *   `tagEnd` is the offset of the `>` closing the tag, or of the last character
 *   if the tag is never closed.
 */
function readAttributes(source, from) {
  /** @type {ScannedAttribute[]} */
  const attributes = [];
  const seen = new Set();
  const length = source.length;
  let i = from;

  while (i < length) {
    while (i < length && isWhitespace(source[i])) i += 1;
    if (i >= length) break;

    if (source[i] === '>') return { attributes, selfClosing: false, tagEnd: i };
    if (source[i] === '/') {
      if (source[i + 1] === '>') return { attributes, selfClosing: true, tagEnd: i + 1 };
      i += 1;
      continue;
    }

    const nameStart = i;
    while (i < length) {
      const char = source[i];
      if (isWhitespace(char) || char === '=' || char === '>' || char === '/') break;
      i += 1;
    }
    if (i === nameStart) {
      // A character that can start neither a name nor a tag end; skip it.
      i += 1;
      continue;
    }
    const name = source.slice(nameStart, i).toLowerCase();

    while (i < length && isWhitespace(source[i])) i += 1;

    let value = '';
    let valueStart = i;
    if (source[i] === '=') {
      i += 1;
      while (i < length && isWhitespace(source[i])) i += 1;
      const quote = source[i];
      if (quote === '"' || quote === "'") {
        valueStart = i + 1;
        const close = source.indexOf(quote, valueStart);
        const valueEnd = close === -1 ? length : close;
        value = source.slice(valueStart, valueEnd);
        i = close === -1 ? length : close + 1;
      } else {
        valueStart = i;
        while (i < length && !isWhitespace(source[i]) && source[i] !== '>') i += 1;
        value = source.slice(valueStart, i);
      }
    }

    // Browsers keep the first of a repeated attribute; so do we.
    if (!seen.has(name)) {
      seen.add(name);
      attributes.push({ name, value, valueStart });
    }
  }

  return { attributes, selfClosing: false, tagEnd: length - 1 };
}

/**
 * The closing-tag pattern for each raw-text element: `</style` and the like,
 * any case, followed by whitespace, `>`, `/` or the end of the document.
 *
 * A case-insensitive search rather than an `indexOf` on a lowercased copy. The
 * copy cost a full pass over the document per raw-text element, which is
 * quadratic in a template with hundreds of `<style>` blocks, and lowercasing
 * can change a string's length (`İ` becomes two code units), so offsets found
 * in the copy did not always point into the source.
 */
const RAW_TEXT_CLOSE = new Map(
  [...RAW_TEXT_ELEMENTS].map((tagName) => [
    tagName,
    new RegExp(`</${tagName}(?=[ \\t\\n\\r\\f>/]|$)`, 'gi'),
  ]),
);

/**
 * Offset of the `</tagName` that ends a raw-text element, or -1.
 *
 * @param {string} source
 * @param {string} tagName  One of `RAW_TEXT_ELEMENTS`, which every caller checks.
 * @param {number} from
 */
function findRawTextClose(source, tagName, from) {
  const pattern = /** @type {RegExp} */ (RAW_TEXT_CLOSE.get(tagName));
  pattern.lastIndex = from;
  const found = pattern.exec(source);
  return found === null ? -1 : found.index;
}
