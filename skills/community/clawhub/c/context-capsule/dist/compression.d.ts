/**
 * Self-contained compression core for the Context Capsule skill.
 *
 * The model cannot use opaque zlib bytes directly, so this module stores the
 * compressed payload for auditability but injects a bounded extractive capsule:
 * decisions, tasks, errors, paths, URLs, questions, and durable facts selected
 * from older history. This is still lossy, but it preserves the material that
 * usually matters in long agent sessions while keeping prompt tokens bounded.
 *
 * Dependencies: Node.js built-ins only — `node:zlib` (deflate) and
 * `node:crypto` (SHA-256). No network, file I/O, dynamic imports, or
 * third-party packages.
 */
export interface Message {
    role: string;
    content: string;
}
export type CapsuleFactKind = "decision" | "task" | "error" | "file" | "question" | "fact";
export interface CapsuleFact {
    kind: CapsuleFactKind;
    text: string;
    role: string;
    sourceIndex: number;
    score: number;
}
/** A compressed, auditable snapshot of an agent session's message history. */
export interface ContextCapsule {
    /** Schema/version tag for forward-compatibility (e.g. "context-capsule.v2"). */
    schema: string;
    sessionId: string;
    capsuleId: string;
    originalTokenEstimate: number;
    compressedBytes: number;
    compressionRatio: string;
    topics: string[];
    facts: CapsuleFact[];
    /** Subjects a later turn abandoned/replaced; surfaced as superseded. */
    superseded: string[];
    droppedFactCount: number;
    maxOutputTokens: number;
    merkleRoot: string;
    createdAt: number;
    compressedBase64: string;
}
export interface CompressOptions {
    sessionId?: string;
    maxOutputTokens?: number;
    maxFacts?: number;
}
export interface InjectOptions {
    maxOutputTokens?: number;
}
/**
 * Compress a session's message history into a ContextCapsule.
 * Pure function — extractive capsule + zlib deflate + SHA-256 only, no I/O.
 */
export declare function compressContext(messages: Message[], opts?: CompressOptions): ContextCapsule;
/**
 * Generate a bounded injection string that replaces full older history in an
 * LLM call. The output intentionally contains useful extracted facts, not the
 * opaque compressed payload.
 */
export declare function injectCapsule(capsule: ContextCapsule, opts?: InjectOptions): string;
