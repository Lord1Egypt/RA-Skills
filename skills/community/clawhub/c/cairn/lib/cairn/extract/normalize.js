// Slugify is load-bearing in two paths:
//   1. concept ID construction (`<source_id>:<docPath>:<slug>`) in extract/doc.ts
//   2. tag normalization on doc-extract emission (v1.1+)
// Lifted into its own module so the rule lives in one place.
export const slugify = (name) => name
    .trim()
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s-]+/g, '_')
    .replace(/^_+|_+$/g, '');
// Normalize + dedupe a list of raw tag strings. Drops empty slugs (e.g.
// emoji-only or punctuation-only inputs collapse to '').
export const normalizeTags = (raw) => [
    ...new Set(raw.map(slugify).filter((s) => s.length > 0)),
];
