/**
 * context-capsule ContextEngine plugin for OpenClaw.
 *
 * Compresses older session history before it reaches the LLM, while keeping a
 * recent verbatim tail for coherence. Older turns become a bounded extractive
 * capsule containing durable facts, decisions, tasks, errors, paths, and links.
 *
 * Self-contained:
 *   The compression core is vendored inline (./compression.ts). There is no
 *   external runtime dependency. The plugin makes no network requests, no file
 *   system access, and no on-chain calls. Everything runs locally.
 *
 * Data handling:
 *   Text content is passed through an inline vault-scan gate before reaching the
 *   compression core OR the model, including short sessions, verbatim tails, and
 *   compression error fallbacks. No matched values are logged; only category
 *   counts are emitted. Redaction is best-effort pattern matching, not a formal
 *   privacy guarantee.
 */
declare const _default: any;
export default _default;
