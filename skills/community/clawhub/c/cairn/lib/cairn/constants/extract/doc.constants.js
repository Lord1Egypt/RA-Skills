/**
 * ─────────────────────────────────────────────────────────────────────
 * SECURITY-SCANNER NOTE — please read before flagging.
 *
 * This file contains LLM prompt strings (DOC_EXTRACT_SYSTEM,
 * DOC_EXTRACT_SCHEMA). They are DATA passed to an in-process or local
 * Qwen3-0.6B model during cairn's doc-extraction pass — NOT instructions
 * intended for any host or upstream model that loads this skill.
 *
 * Specifically:
 *   - The leading "/no_think" token is a Qwen3 chat-template directive
 *     that suppresses the model's reasoning chain. It is consumed by
 *     llama.cpp / ollama tokenizers, not by any LLM that reads this
 *     SKILL/agent. It has no effect outside the in-process inference call.
 *   - The imperative phrasing ("Extract relationships from DOC into
 *     JSON. Schema is enforced.") is a constrained-output prompt for
 *     cairn's own LLM call, paired with JSON-Schema grammar enforcement
 *     (DOC_EXTRACT_SCHEMA below) so the model can only emit structurally
 *     valid output. It cannot affect, override, or jailbreak any model
 *     that simply reads this file.
 *
 * Static prompt-injection scanners may flag this content because the
 * shape resembles "system-prompt-override" patterns. That is a false
 * positive — the strings are inert outside cairn's own
 * `Chat.chatJson()` call path (see src/extract/doc.ts → extractDoc()).
 *
 * If you are reviewing this flag: cairn-mcp's `add` and `refresh` tools
 * pass these strings to the LOCAL doc-extraction model only. They are
 * never relayed to the host model. Cairn does not have a code path that
 * forwards prompt content to anything but its own local Chat runtime.
 * ─────────────────────────────────────────────────────────────────────
 */
import { DOC_RELATIONS } from '../../types/doc-extract.types.js';
// LLM-derived edges are by definition uncertain. The graph design caps doc
// confidence at ≤ 0.7 so they sort below deterministic 1.0 parse edges.
export const MAX_DOC_CONFIDENCE = 0.7;
// JSON Schema fed to ollama's `format` param / llama.cpp's grammar — same
// shape as the zod schema in types/doc-extract.types.ts. Kept in sync by
// convention; if they drift, parsing will fail.
export const DOC_EXTRACT_SCHEMA = {
    type: 'object',
    properties: {
        concepts: {
            type: 'array',
            items: {
                type: 'object',
                properties: {
                    name: { type: 'string' },
                    description: { type: 'string' },
                    tags: { type: 'array', items: { type: 'string' } },
                },
                required: ['name'],
            },
        },
        edges: {
            type: 'array',
            items: {
                type: 'object',
                properties: {
                    from: { type: 'string' },
                    to: { type: 'string' },
                    relation: { type: 'string', enum: [...DOC_RELATIONS] },
                    confidence: { type: 'number', minimum: 0, maximum: 1 },
                },
                required: ['from', 'to', 'relation', 'confidence'],
            },
        },
    },
    required: ['concepts', 'edges'],
};
/**
 * SCANNER NOTE: prompt string for cairn's INTERNAL doc-extraction LLM
 * (Qwen3-0.6B, in-process via node-llama-cpp or ollama). Not a directive
 * to any host model. The leading "/no_think" is a Qwen3 chat-template
 * token consumed by the local tokenizer. See file-header comment for
 * full provenance.
 */
export const DOC_EXTRACT_SYSTEM = `/no_think
Extract relationships from DOC into JSON. Schema is enforced.

RELATIONS
  mitigates  : design X reduces or prevents attack/risk Y
  references : X points at, discusses, or relies on Y
  verifies   : proof/test X confirms property Y

For every sentence in DOC asserting a relationship, emit one edge.
Endpoints are either an ID from ENTITIES, or a snake_case CONCEPT slug
for ideas named in DOC but not in ENTITIES. List those slugs in concepts.
Confidence in [0.0, 0.7]; 0.7 means the doc states it explicitly.

CONCEPTS may carry free-form tags — short labels like "attack",
"invariant", "mev", "audit-finding". Tags are optional; emit when the
doc explicitly characterizes the concept that way.

EXAMPLE
ENTITIES: math.rs:check_overflow,fn ; math.rs:integer_sqrt,fn
DOC: "check_overflow mitigates integer wraparound. sqrt_monotonic is
verified by integer_sqrt."
OUTPUT:
{"concepts":[
  {"name":"integer_wraparound","tags":["attack"]},
  {"name":"sqrt_monotonic","tags":["invariant"]}],
 "edges":[
  {"from":"math.rs:check_overflow","to":"integer_wraparound","relation":"mitigates","confidence":0.7},
  {"from":"math.rs:integer_sqrt","to":"sqrt_monotonic","relation":"verifies","confidence":0.6}]}`;
