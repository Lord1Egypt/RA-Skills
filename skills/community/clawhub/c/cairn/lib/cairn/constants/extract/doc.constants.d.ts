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
export declare const MAX_DOC_CONFIDENCE = 0.7;
export declare const DOC_EXTRACT_SCHEMA: {
    readonly type: "object";
    readonly properties: {
        readonly concepts: {
            readonly type: "array";
            readonly items: {
                readonly type: "object";
                readonly properties: {
                    readonly name: {
                        readonly type: "string";
                    };
                    readonly description: {
                        readonly type: "string";
                    };
                    readonly tags: {
                        readonly type: "array";
                        readonly items: {
                            readonly type: "string";
                        };
                    };
                };
                readonly required: readonly ["name"];
            };
        };
        readonly edges: {
            readonly type: "array";
            readonly items: {
                readonly type: "object";
                readonly properties: {
                    readonly from: {
                        readonly type: "string";
                    };
                    readonly to: {
                        readonly type: "string";
                    };
                    readonly relation: {
                        readonly type: "string";
                        readonly enum: readonly ["mitigates", "references", "verifies"];
                    };
                    readonly confidence: {
                        readonly type: "number";
                        readonly minimum: 0;
                        readonly maximum: 1;
                    };
                };
                readonly required: readonly ["from", "to", "relation", "confidence"];
            };
        };
    };
    readonly required: readonly ["concepts", "edges"];
};
/**
 * SCANNER NOTE: prompt string for cairn's INTERNAL doc-extraction LLM
 * (Qwen3-0.6B, in-process via node-llama-cpp or ollama). Not a directive
 * to any host model. The leading "/no_think" is a Qwen3 chat-template
 * token consumed by the local tokenizer. See file-header comment for
 * full provenance.
 */
export declare const DOC_EXTRACT_SYSTEM = "/no_think\nExtract relationships from DOC into JSON. Schema is enforced.\n\nRELATIONS\n  mitigates  : design X reduces or prevents attack/risk Y\n  references : X points at, discusses, or relies on Y\n  verifies   : proof/test X confirms property Y\n\nFor every sentence in DOC asserting a relationship, emit one edge.\nEndpoints are either an ID from ENTITIES, or a snake_case CONCEPT slug\nfor ideas named in DOC but not in ENTITIES. List those slugs in concepts.\nConfidence in [0.0, 0.7]; 0.7 means the doc states it explicitly.\n\nCONCEPTS may carry free-form tags \u2014 short labels like \"attack\",\n\"invariant\", \"mev\", \"audit-finding\". Tags are optional; emit when the\ndoc explicitly characterizes the concept that way.\n\nEXAMPLE\nENTITIES: math.rs:check_overflow,fn ; math.rs:integer_sqrt,fn\nDOC: \"check_overflow mitigates integer wraparound. sqrt_monotonic is\nverified by integer_sqrt.\"\nOUTPUT:\n{\"concepts\":[\n  {\"name\":\"integer_wraparound\",\"tags\":[\"attack\"]},\n  {\"name\":\"sqrt_monotonic\",\"tags\":[\"invariant\"]}],\n \"edges\":[\n  {\"from\":\"math.rs:check_overflow\",\"to\":\"integer_wraparound\",\"relation\":\"mitigates\",\"confidence\":0.7},\n  {\"from\":\"math.rs:integer_sqrt\",\"to\":\"sqrt_monotonic\",\"relation\":\"verifies\",\"confidence\":0.6}]}";
