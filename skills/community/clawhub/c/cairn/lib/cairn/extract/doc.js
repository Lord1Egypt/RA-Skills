import { DOC_EXTRACT_SCHEMA, DOC_EXTRACT_SYSTEM, MAX_DOC_CONFIDENCE, } from '../constants/extract/doc.constants.js';
import { DocExtractZ, } from '../types/doc-extract.types.js';
import { normalizeTags, slugify } from './normalize.js';
// Re-export so existing import sites (`from '.../extract/doc'`) keep working.
export { slugify };
// Concept entities are owned by the doc that defines them. ID format mirrors
// code entities — `<source_id>:<docPath>:<slug>` when source_id is present.
export const conceptId = (docPath, slug, source_id) => {
    const base = `${docPath}:${slugify(slug)}`;
    return source_id !== undefined ? `${source_id}:${base}` : base;
};
// Strip a `<digits>:` source_id prefix when present. Used for pretty-printing
// entity ids in the LLM prompt and for parsing LLM output that elided it.
const stripSourcePrefix = (id) => {
    const m = id.match(/^\d+:(.+)$/);
    return m ? m[1] : id;
};
const kindCode = (kind) => {
    switch (kind) {
        case 'function':
            return 'fn';
        case 'struct':
            return 'st';
        case 'enum':
            return 'en';
        case 'constant':
            return 'co';
        case 'concept':
            return 'cn';
        default:
            return '?';
    }
};
export const buildUserPrompt = (ctx) => {
    // Show bare `<filepath>:<name>` ids in the prompt — the LLM doesn't need
    // (and gets confused by) the `<source_id>:` prefix. resolveExtraction maps
    // bare ids back to their namespaced form when the LLM echoes them.
    const entityRows = ctx.codeEntities
        .map((e) => `${stripSourcePrefix(e.id)},${kindCode(e.kind)},${e.name}`)
        .join('\n');
    const entityBlock = entityRows.length > 0 ? entityRows : '(none)';
    return `ENTITIES (use as edge endpoints)
ID,KIND,NAME
${entityBlock}

DOC: ${ctx.docPath}
---
${ctx.docContent}
---

OUTPUT
{ "concepts": [...], "edges": [...] }
>`;
};
// Turn the raw LLM output into entity IDs the DB can ingest.
// - Concepts get namespaced: bare name → `${docPath}:${slug(name)}`.
// - Edge endpoints resolve in priority order:
//   1. Exact match against a known code entity ID.
//   2. Exact match against a bare `<filepath>:<name>` form.
//   3. Exact match against a known code entity NAME (LLM dropped prefix).
//   4. Exact match against a concept slug declared in `concepts`.
//   Otherwise the edge is dropped — better silence than hallucinated edges.
export const resolveExtraction = (raw, docPath, codeEntities, source_id) => {
    const codeIds = new Set(codeEntities.map((e) => e.id));
    const codeByBareId = new Map();
    const codeByName = new Map();
    for (const e of codeEntities) {
        const bare = stripSourcePrefix(e.id);
        if (bare !== e.id && !codeByBareId.has(bare))
            codeByBareId.set(bare, e.id);
        if (!codeByName.has(e.name))
            codeByName.set(e.name, e.id);
    }
    const concepts = [];
    const conceptBySlug = new Map();
    for (const c of raw.concepts) {
        const slug = slugify(c.name);
        if (slug.length === 0)
            continue;
        if (conceptBySlug.has(slug))
            continue;
        const id = conceptId(docPath, slug, source_id);
        concepts.push({
            id,
            name: c.name,
            description: c.description ?? null,
            tags: normalizeTags(c.tags ?? []),
        });
        conceptBySlug.set(slug, id);
    }
    // Code matches always win over concept matches: when the LLM emits "Pool",
    // the struct named Pool is the right target, not a concept slug also called
    // "pool".
    const resolveEndpoint = (raw) => {
        if (codeIds.has(raw))
            return raw;
        const bareHit = codeByBareId.get(raw);
        if (bareHit)
            return bareHit;
        const namedCodeHit = codeByName.get(raw);
        if (namedCodeHit)
            return namedCodeHit;
        const slug = slugify(raw);
        const conceptHit = conceptBySlug.get(slug);
        if (conceptHit)
            return conceptHit;
        return null;
    };
    const edges = [];
    let dropped = 0;
    for (const e of raw.edges) {
        const from = resolveEndpoint(e.from);
        const to = resolveEndpoint(e.to);
        if (!from || !to || from === to) {
            dropped++;
            continue;
        }
        edges.push({
            from_id: from,
            to_id: to,
            relation: e.relation,
            confidence: Math.min(MAX_DOC_CONFIDENCE, Math.max(0, e.confidence)),
        });
    }
    // Keep all concepts the LLM emitted, even orphans. Small models often emit
    // concept nodes without linking them to edges; the standalone entity is
    // still useful for graph queries and gets a vec embedding so KNN finds it.
    return { concepts, edges, dropped };
};
export const extractDoc = async (chat, ctx) => {
    const userPrompt = buildUserPrompt(ctx);
    const out = await chat.chatJson({
        system: DOC_EXTRACT_SYSTEM,
        user: userPrompt,
        schema: DOC_EXTRACT_SCHEMA,
    });
    const raw = DocExtractZ.parse(out);
    const resolved = resolveExtraction(raw, ctx.docPath, ctx.codeEntities, ctx.source_id);
    return { raw, resolved };
};
