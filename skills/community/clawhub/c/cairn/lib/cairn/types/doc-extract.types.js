import { z } from 'zod';
// Three relations the LLM is allowed to emit. `mitigates` is the headliner
// (only LLM source); `references` and `verifies` could come from doc-table
// parsing later but for v1 the LLM handles them too.
export const DOC_RELATIONS = ['mitigates', 'references', 'verifies'];
const ConceptZ = z.object({
    name: z.string().min(1),
    description: z.string().optional(),
    // Free-form descriptive tags. Slugified at resolution time. Empty / missing
    // arrays are equivalent (concept gets no tags).
    tags: z.array(z.string()).optional(),
});
const EdgeZ = z.object({
    from: z.string().min(1),
    to: z.string().min(1),
    relation: z.enum(DOC_RELATIONS),
    // Range is intentionally loose: small LLMs occasionally emit values > 1 or
    // < 0 even with a strict JSON schema hint. The downstream clamp in
    // resolveExtraction enforces [0, MAX_DOC_CONFIDENCE]. Strict validation
    // here would reject the whole batch and waste the chat call.
    confidence: z.number(),
});
export const DocExtractZ = z.object({
    concepts: z.array(ConceptZ).default([]),
    edges: z.array(EdgeZ).default([]),
});
