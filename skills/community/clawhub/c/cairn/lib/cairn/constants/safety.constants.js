// Defense-in-depth defaults for ingestion. All can be overridden via env vars.
// Real protection still comes from MCP host-side per-call approval and from
// the user not pointing `cairn add` at unintended paths — these are belt + suspenders.
export const DEFAULT_MAX_INGEST_FILES = 10_000;
export const DEFAULT_MAX_INGEST_BYTES = 500 * 1024 * 1024; // 500 MB
