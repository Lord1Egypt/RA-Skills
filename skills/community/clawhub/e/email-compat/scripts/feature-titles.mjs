/**
 * caniemail-ai-tooling — feature title tables.
 *
 * Turns the dataset's feature *titles* into the things a parser can match:
 * property names, units, keywords, at-rule names, element names, attributes.
 *
 * The tables are derived from the titles by convention — `title.endsWith(' unit')`,
 * `title.startsWith('@')`, `/<(\w+)>/` and so on — exactly as the `caniemail`
 * package did, and for the same reason: a static list would rot the moment
 * upstream adds a feature. What is hardcoded is only the set of titles whose
 * shape breaks the convention, and each of those carries a comment naming it.
 *
 * The tables are built per dataset and memoised, because the dataset is fetched
 * at runtime rather than bundled — there is no module-load-time snapshot to
 * build them from.
 *
 * Vendored byte-identically into `skill/scripts/` and `mcp/src/`; never edit a
 * vendored copy, edit this file and run `make sync-core`.
 */

import {
  ADJACENT_SIBLING,
  ATTRIBUTE,
  CHAINING,
  CHILD,
  CLASS,
  DESCENDANT,
  GENERAL_SIBLING,
  GROUPING,
  ID,
  TYPE,
  UNIVERSAL,
} from './selector-shapes.mjs';

/* -------------------------------------------------------------------------- */
/* Hardcoded shape exceptions                                                  */
/* -------------------------------------------------------------------------- */

/*
 * The lookup tables below are Maps rather than object literals because their
 * keys come from dataset titles and from URLs in the email. On a plain object
 * `constructor` or `toString` finds a function on `Object.prototype`.
 */

/**
 * CSS titles that name several properties instead of one.
 *
 * Every entry exists because the title is prose ("border-inline & border-block")
 * rather than a property name, so `/^[a-z-]+$/` cannot recover it.
 */
const PROPERTY_TITLE_EXCEPTIONS = new Map(
  Object.entries({
    'block-size & inline-size': ['block-size', 'inline-size'],
    'border-inline & border-block': ['border-inline', 'border-block'],
    'border-inline & border-block individual logical properties': [
      'border-block-end',
      'border-block-start',
      'border-inline-end',
      'border-inline-start',
    ],
    'border-inline & border-block longhand properties': [
      'border-block-color',
      'border-block-style',
      'border-block-width',
      'border-inline-color',
      'border-inline-style',
      'border-inline-width',
    ],
    'border-radius logical properties': [
      'border-end-end-radius',
      'border-end-start-radius',
      'border-start-end-radius',
      'border-start-start-radius',
    ],
    'color-scheme CSS property': ['color-scheme'],
    'css column properties': [
      'column-count',
      'column-fill',
      'column-gap',
      'column-rule',
      'column-rule-color',
      'column-rule-style',
      'column-rule-width',
      'column-span',
      'column-width',
      'columns',
    ],
    'gap, column-gap, row-gap': ['column-gap', 'gap', 'row-gap'],
    'grid-template-* properties': [
      'grid-template',
      'grid-template-areas',
      'grid-template-columns',
      'grid-template-rows',
    ],
    'left, right, top, bottom': ['left', 'right', 'top', 'bottom'],
    'margin-block-start & margin-block-end': ['margin-block-end', 'margin-block-start'],
    'margin-inline & margin-block': ['margin-block', 'margin-inline'],
    'margin-inline-start & margin-inline-end': ['margin-inline-end', 'margin-inline-start'],
    'padding-block-start & padding-block-end': ['padding-block-end', 'padding-block-start'],
    'padding-inline & padding-block': ['padding-block', 'padding-inline'],
    'padding-inline-start & padding-inline-end': ['padding-inline-end', 'padding-inline-start'],
  }),
);

/**
 * CSS titles that name a set of *values* rather than a property or a pair.
 * Matched as whole words anywhere in a declaration value.
 */
const VALUE_TITLE_EXCEPTIONS = {
  'fit-content, min-content, max-content': ['fit-content', 'max-content', 'min-content'],
  'system-ui, ui-serif, ui-sans-serif, ui-rounded, ui-monospace': [
    'system-ui',
    'ui-monospace',
    'ui-rounded',
    'ui-sans-serif',
    'ui-serif',
  ],
};

/**
 * HTML titles that name elements the `/<(\w+)>/` convention cannot recover.
 *
 * @type {Map<string, string[]>}
 */
const ELEMENT_TITLE_EXCEPTIONS = new Map(
  Object.entries({
    // Bare word, no angle brackets.
    address: ['address'],
    // A range, not a list: the convention would recover h1 and h6 and drop h2-h5.
    '<h1> to <h6> elements': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    // The doctype is a directive, not a tag; `detectHtml` matches it specially.
    'HTML5 doctype': [],
    // Prose title covering the whole HTML5 sectioning/semantic element set.
    'HTML5 semantics': [
      'article',
      'aside',
      'details',
      'figcaption',
      'figure',
      'footer',
      'header',
      'main',
      'mark',
      'nav',
      'section',
      'summary',
      'time',
    ],
    // "Image maps" is <map>, and the title does not say so.
    'Image maps': ['map'],
    // The <svg> in the title is context; the element measured is SVG's <image>.
    'Embedded <svg> image': ['image'],
  }),
);

/**
 * What `matchElementAttributes` tests one element against. Each matcher is
 * `[name, expected]`; the forms `expected` takes are described there.
 *
 * @typedef {object} ElementAttributeRule
 * @property {string} element
 * @property {[name: string, expected: string|RegExp|null][]} matchers
 */

/**
 * HTML titles that pair an element with an attribute, where the pairing is not
 * spelled `<el attr="value">`.
 *
 * @type {Map<string, ElementAttributeRule>}
 */
const ELEMENT_ATTRIBUTE_TITLE_EXCEPTIONS = new Map(
  Object.entries({
    'Local anchors': {
      element: 'a',
      matchers: [
        ['href', /^#/],
        ['name', null],
      ],
    },
    'mailto: links': { element: 'a', matchers: [['href', /^mailto:/i]] },
    'color-scheme meta tag': { element: 'meta', matchers: [['name', 'color-scheme']] },
    'AMP for Email': {
      element: 'html',
      matchers: [
        ['⚡4email', null],
        ['amp4email', null],
      ],
    },
  }),
);

/** File extension -> image feature title. */
const IMAGE_EXTENSION_TITLES = new Map(
  Object.entries({
    apng: 'Animated PNG image format',
    avif: 'AVIF image format',
    bmp: 'BMP image format',
    gif: 'GIF image format',
    heic: 'HEIF image format',
    heif: 'HEIF image format',
    ico: 'ICO image format',
    jpeg: 'JPG image format',
    jpg: 'JPG image format',
    png: 'PNG image format',
    svg: 'SVG image format',
    tif: 'TIFF image format',
    tiff: 'TIFF image format',
    webp: 'webP image format',
  }),
);

/** data: URI MIME type -> image feature title. */
const IMAGE_MIME_TITLES = new Map(
  Object.entries({
    'image/apng': 'Animated PNG image format',
    'image/avif': 'AVIF image format',
    'image/bmp': 'BMP image format',
    'image/gif': 'GIF image format',
    'image/heic': 'HEIF image format',
    'image/heif': 'HEIF image format',
    'image/jpeg': 'JPG image format',
    'image/jpg': 'JPG image format',
    'image/png': 'PNG image format',
    'image/svg+xml': 'SVG image format',
    'image/tiff': 'TIFF image format',
    'image/vnd.microsoft.icon': 'ICO image format',
    'image/webp': 'webP image format',
  }),
);

/**
 * Titles that name a selector shape rather than anything textual.
 *
 * Imported rather than spelled out again: `detect.mjs` looks up the shapes
 * `analyzeSelector` reports in this set, so a second spelling that drifted
 * would stop a shape being detected without any error.
 */
const SELECTOR_SHAPE_TITLES = [
  ADJACENT_SIBLING,
  ATTRIBUTE,
  CHAINING,
  CHILD,
  CLASS,
  DESCENDANT,
  GENERAL_SIBLING,
  GROUPING,
  ID,
  TYPE,
  UNIVERSAL,
];

/** Titles raised by a construct with no name of its own. */
export const CSS_COMMENTS_TITLE = 'CSS comments';
export const CSS_NESTING_TITLE = 'CSS Nesting';
export const HTML_COMMENTS_TITLE = 'HTML comments';
export const HTML_DOCTYPE_TITLE = 'HTML5 doctype';

/* -------------------------------------------------------------------------- */
/* Table construction                                                          */
/* -------------------------------------------------------------------------- */

const PROPERTY_NAME = /^[a-z-]+$/;

/**
 * The two fields of a feature record the tables are built from. A raw record
 * carries more, and is accepted as it is.
 *
 * @typedef {{title: string, category: string}} TitledFeature
 */

/** @typedef {ReturnType<typeof createTables>} TitleTables */

/** @type {WeakMap<readonly TitledFeature[], TitleTables>} */
const cache = new WeakMap();

/**
 * Build the title tables for a dataset's feature list.
 *
 * Memoised on the feature array, which `loadDataset` creates once per dataset,
 * so repeated lints against the same dataset build the tables once.
 *
 * @param {readonly TitledFeature[]} features Raw feature records.
 * @returns {TitleTables}
 */
export function buildTitleTables(features) {
  const cached = cache.get(features);
  if (cached) return cached;
  const tables = createTables(features);
  cache.set(features, tables);
  return tables;
}

/** @param {readonly TitledFeature[]} features */
function createTables(features) {
  /** @type {Partial<Record<string, string[]>>} */
  const titlesByCategory = { css: [], html: [], image: [], others: [] };
  const known = new Set();
  for (const feature of features) {
    known.add(feature.title);
    const bucket = titlesByCategory[feature.category];
    if (bucket) bucket.push(feature.title);
  }

  const css = titlesByCategory.css ?? [];
  // "AMP for Email" is categorised `others` but is detected from markup, so it
  // joins the HTML titles. This mirrors upstream, which does the same.
  const html = [...(titlesByCategory.html ?? []), ...['AMP for Email'].filter((t) => known.has(t))];

  return {
    known,

    /* CSS ---------------------------------------------------------------- */

    // "@media" -> "media". Media-feature titles keep their parenthesised part,
    // which `matchAtRule` matches against the features in the at-rule prelude.
    atRules: css
      .filter((t) => t.startsWith('@'))
      .map((title) => ({
        title,
        names: [...title.matchAll(/@([a-z-]+)/g)].map((m) => m[1]),
        features: [...title.matchAll(/\(([a-z-]+)\)/g)].map((m) => m[1]),
      })),

    // "linear-gradient()" -> "linear-gradient". A title may name several
    // functions ("lch(), oklch(), lab(), oklab()"), so every name is taken.
    functions: css.flatMap((title) => {
      if (title.startsWith(':')) return []; // ":has()" is a pseudo-class.
      // The one function whose title does not spell it with parentheses.
      if (title === 'CSS Variables (Custom Properties)') return [{ title, names: ['var'] }];
      if (!title.includes('()')) return [];
      const names = [...title.matchAll(/([a-z-]+)\(\)/g)].map((m) => m[1]);
      return names.length > 0 ? [{ title, names }] : [];
    }),

    // "!important keyword" -> "!important".
    keywords: css
      .filter((t) => t.includes(' keyword'))
      .map((title) => ({ title, value: title.replace(/ keyword$/, '') })),

    // "display:flex" -> property "display", value "flex".
    propertyValuePairs: css.flatMap((title) => {
      const match = /([a-z-]+):\s*([a-z-]+)/.exec(title);
      return match ? [{ title, property: match[1], value: match[2] }] : [];
    }),

    // "height property" / "font shorthand" / "inline-size " -> one property.
    properties: css.flatMap((title) => {
      const exception = PROPERTY_TITLE_EXCEPTIONS.get(title);
      if (exception) return [{ title, names: exception }];
      const trimmed = title
        .trim()
        .replace(/ shorthand$/, '')
        .replace(/ property$/, '');
      return PROPERTY_NAME.test(trimmed) ? [{ title, names: [trimmed] }] : [];
    }),

    // "px unit" -> "px", compiled here rather than per declaration. A unit
    // only counts immediately after a digit, with nothing between: `margin: 0`
    // is not the `in` unit, `1rem` is not `em`, and `content: "1 inch"` is not
    // an `in` unit either. `initial` is a keyword rather than a suffix, so it
    // matches on a word boundary instead.
    units: css
      .filter((t) => t.endsWith(' unit'))
      .map((title) => {
        const unit = title.replace(/ unit$/, '');
        const pattern = unit === 'initial' ? /\binitial\b/ : new RegExp(`\\d${escapeRegExp(unit)}`);
        return { title, pattern };
      }),

    // Each title's names as one whole-word alternation, compiled once.
    values: Object.entries(VALUE_TITLE_EXCEPTIONS)
      .filter(([title]) => known.has(title))
      .map(([title, names]) => ({
        title,
        pattern: new RegExp(`(^|[\\s,])(?:${names.map(escapeRegExp).join('|')})([\\s,]|$)`),
      })),

    // "::after" / ":nth-child" / ":has()" -> the pseudo's bare name.
    pseudos: css
      .filter((t) => t.startsWith(':'))
      .map((title) => ({ title, name: title.replace(/^:+/, '').replace(/\(\)$/, '') })),

    selectorShapes: new Set(SELECTOR_SHAPE_TITLES.filter((t) => known.has(t))),

    /* HTML --------------------------------------------------------------- */

    // "<video> element" -> "video"; "<ul>, <ol> and <dl>" -> all three.
    elements: html.flatMap((title) => {
      const exception = ELEMENT_TITLE_EXCEPTIONS.get(title);
      if (exception) return exception.length > 0 ? [{ title, names: exception }] : [];
      const names = [...title.matchAll(/<(\w+)>/g)].map((m) => m[1].toLowerCase());
      return names.length > 0 ? [{ title, names }] : [];
    }),

    // "role attribute" -> "role"; "srcset and sizes attributes" -> both.
    //
    // Every derived name has to look like an attribute. A title such as
    // "Deprecated presentational attributes" is prose, not a list, and the
    // guard drops it rather than deriving a name nothing can ever match --
    // which would leave the title counted as reachable and take the coverage
    // tripwire in core/feature-titles.test.mjs down with it.
    attributes: html.flatMap((title) => {
      const match = /^(.+?) attributes?$/.exec(title);
      if (!match) return [];
      const names = match[1].split(/,\s*|\s+and\s+/).map((name) => name.trim());
      if (names.length === 0 || !names.every((name) => /^[a-z][a-z0-9-]*$/.test(name))) return [];
      return [{ title, names }];
    }),

    // '<input type="text"> element' -> element "input", attribute type="text".
    elementAttributes: html.flatMap((title) => {
      const exception = ELEMENT_ATTRIBUTE_TITLE_EXCEPTIONS.get(title);
      if (exception) return [{ title, ...exception }];
      const match = /<(\w+) ([\w-]+)="([^"]+)"> element/.exec(title);
      if (!match) return [];
      /** @type {ElementAttributeRule['matchers']} */
      const matchers = [[match[2].toLowerCase(), match[3]]];
      return [{ title, element: match[1].toLowerCase(), matchers }];
    }),

    /* Images ------------------------------------------------------------- */

    imageExtensions: filterToKnown(IMAGE_EXTENSION_TITLES, known),
    imageMimes: filterToKnown(IMAGE_MIME_TITLES, known),
  };
}

/**
 * @param {Map<string, string>} map  Anything -> title.
 * @param {Set<string>} known
 */
function filterToKnown(map, known) {
  return new Map([...map].filter(([, title]) => known.has(title)));
}

/* -------------------------------------------------------------------------- */
/* Matchers                                                                    */
/* -------------------------------------------------------------------------- */

/**
 * Titles matched by a declaration's property name.
 *
 * A property matches its own title and every shorthand title it extends, so
 * `border-radius` reports both `border-radius` and `border`. That is upstream's
 * rule and it is the right one: the shorthand's support data is what an agent
 * needs when the longhand has none.
 *
 * @param {TitleTables} tables
 * @param {string} propertyName
 */
export function matchProperty(tables, propertyName) {
  const titles = [];
  for (const { title, names } of tables.properties) {
    if (names.some((name) => propertyName === name || propertyName.startsWith(`${name}-`))) {
      titles.push(title);
    }
  }
  return titles;
}

/**
 * Titles matched by a `property: value` pair, ignoring `!important`.
 *
 * @param {TitleTables} tables
 * @param {string} propertyName
 * @param {string} propertyValue
 */
export function matchPropertyValuePair(tables, propertyName, propertyValue) {
  const value = stripImportant(propertyValue);
  const titles = [];
  for (const pair of tables.propertyValuePairs) {
    if (pair.property === propertyName && pair.value === value) titles.push(pair.title);
  }
  return titles;
}

/**
 * Titles matched by function calls appearing in a declaration value.
 *
 * @param {TitleTables} tables
 * @param {string} propertyValue
 */
export function matchFunctions(tables, propertyValue) {
  // No whitespace before the paren: CSS functional notation does not allow it,
  // and permitting it turns `Arial (fallback)` into a function call.
  const called = new Set(
    [...propertyValue.matchAll(/([a-z-]+)\(/gi)].map((m) => m[1].toLowerCase()),
  );
  return tables.functions.filter((f) => f.names.some((n) => called.has(n))).map((f) => f.title);
}

/**
 * Titles matched by a keyword appearing in a declaration value.
 *
 * @param {TitleTables} tables
 * @param {string} propertyValue
 */
export function matchKeywords(tables, propertyValue) {
  return tables.keywords.filter((k) => propertyValue.includes(k.value)).map((k) => k.title);
}

/**
 * Titles matched by a bare value keyword, as a whole word.
 *
 * @param {TitleTables} tables
 * @param {string} propertyValue
 */
export function matchValues(tables, propertyValue) {
  return tables.values.filter((v) => v.pattern.test(propertyValue)).map((v) => v.title);
}

/**
 * Titles matched by a unit appearing in a declaration value, immediately after
 * a digit. The patterns are built with the tables; see `units` there.
 *
 * @param {TitleTables} tables
 * @param {string} propertyValue
 */
export function matchUnits(tables, propertyValue) {
  return tables.units.filter((u) => u.pattern.test(propertyValue)).map((u) => u.title);
}

/**
 * Titles matched by an at-rule.
 *
 * `@media` matches on the name alone. A media-feature title such as
 * `@media (prefers-color-scheme)` additionally requires one of the prelude's
 * media features to be that feature, which is what makes those five titles
 * reachable — upstream compared them against bare node type names, so they
 * never matched.
 *
 * A feature is a whole token, not a substring: `(orientation-x)` is not
 * `(orientation)`, and `(any-hover)` does not contain `(hover)`. Nor is a
 * `min-`/`max-` range form the bare feature. caniemail tested
 * `(-webkit-device-pixel-ratio)` alone, so `-webkit-min-device-pixel-ratio`
 * carries no verdict of its own and reports only `@media`.
 *
 * @param {TitleTables} tables
 * @param {string} name
 * @param {string} [prelude]
 */
export function matchAtRule(tables, name, prelude = '') {
  const features = mediaFeatures(prelude);
  const titles = [];
  for (const rule of tables.atRules) {
    if (!rule.names.includes(name)) continue;
    if (rule.features.length > 0 && !rule.features.some((f) => features.has(f))) continue;
    titles.push(rule.title);
  }
  return titles;
}

/**
 * The media-feature names in an at-rule prelude, lowercased: the name opening
 * each parenthesised test, up to its `:`, its `)` or whitespace.
 *
 * @param {string} prelude
 */
function mediaFeatures(prelude) {
  return new Set(
    [...prelude.matchAll(/\(\s*([-a-z0-9]+)(?=[\s:)])/gi)].map((m) => m[1].toLowerCase()),
  );
}

/**
 * Titles matched by a pseudo-class or pseudo-element name.
 *
 * @param {TitleTables} tables
 * @param {string} pseudoName
 */
export function matchPseudo(tables, pseudoName) {
  return tables.pseudos.filter((p) => p.name === pseudoName).map((p) => p.title);
}

/**
 * Titles matched by a tag name.
 *
 * @param {TitleTables} tables
 * @param {string} tagName
 */
export function matchElement(tables, tagName) {
  return tables.elements.filter((e) => e.names.includes(tagName)).map((e) => e.title);
}

/**
 * Titles matched by the attribute names present on an element.
 *
 * @param {TitleTables} tables
 * @param {string[]} attributeNames
 */
export function matchAttributes(tables, attributeNames) {
  return tables.attributes
    .filter((a) => a.names.some((name) => attributeNames.includes(name)))
    .map((a) => a.title);
}

/**
 * Titles matched by an element/attribute pairing.
 *
 * A matcher is `[name, expected]`: a null `expected` means the attribute only
 * has to be present, a string means equality, a RegExp means a value test.
 * String comparison is case-insensitive because every value spelled in a title
 * is an HTML keyword (`type="checkbox"`, `name="color-scheme"`), and HTML
 * compares those without regard to case. The RegExp matchers carry their own
 * flags, since `href` values are not keywords.
 *
 * @param {TitleTables} tables
 * @param {string} tagName
 * @param {Map<string, string>} attributes
 */
export function matchElementAttributes(tables, tagName, attributes) {
  const titles = [];
  for (const { title, element, matchers } of tables.elementAttributes) {
    if (element !== tagName) continue;
    const hit = matchers.some(([name, expected]) => {
      const value = attributes.get(name);
      if (value === undefined) return false;
      if (expected === null) return true;
      return expected instanceof RegExp
        ? expected.test(value)
        : value.toLowerCase() === expected.toLowerCase();
    });
    if (hit) titles.push(title);
  }
  return titles;
}

/**
 * The image-format title a URL implies, if any.
 *
 * A data: URI is read from its MIME type; anything else from the extension,
 * after query string and fragment are stripped.
 *
 * @param {TitleTables} tables
 * @param {string} url
 * @returns {string|undefined}
 */
export function matchImageUrl(tables, url) {
  const trimmed = String(url).trim();
  const mime = /^data:([^;,]+)/i.exec(trimmed)?.[1]?.toLowerCase();
  if (mime) return tables.imageMimes.get(mime);
  const path = trimmed.split(/[?#]/, 1)[0];
  const extension = /\.([a-z0-9]+)$/i.exec(path)?.[1]?.toLowerCase();
  return extension ? tables.imageExtensions.get(extension) : undefined;
}

/**
 * The candidate URLs in a `srcset` attribute.
 *
 * @param {string} srcset
 */
export function urlsFromSrcset(srcset) {
  return String(srcset)
    .split(',')
    .map((candidate) => candidate.trim().split(/\s+/, 1)[0])
    .filter(Boolean);
}

/**
 * The URLs in `url(...)` functions inside a declaration value.
 *
 * @param {string} value
 */
export function urlsFromCssValue(value) {
  return [...String(value).matchAll(/url\(\s*(['"]?)(.*?)\1\s*\)/gi)]
    .map((match) => match[2]?.trim())
    .filter(Boolean);
}

/** @param {string} value */
function stripImportant(value) {
  return value.replace(/\s*!\s*important\s*$/i, '').trim();
}

/**
 * Escape a string for use as a literal inside a `RegExp`.
 *
 * @param {string} value
 */
export function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
