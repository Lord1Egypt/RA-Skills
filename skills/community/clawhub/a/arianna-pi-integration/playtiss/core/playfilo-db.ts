// Copyright (c) 2026 Wuji Labs Inc
// SPDX-License-Identifier: MIT
//
// playfilo-db.ts — playtiss/core-backed equivalent of Filo's storage shim.
//
// ───────────────────────────────────────────────────────────────────────────
// DESIGN CHOICE: HYBRID (same schema, playtiss StorageProvider for blobs)
// ───────────────────────────────────────────────────────────────────────────
//
// Why not "different schema using @playtiss/core hashing everywhere"?
//
//   1. Filo's public API (commitNodeWithExternalId, loadEntriesFromDAG,
//      handleLife, etc.) is the contract Mirin's and Pax's patches depend
//      on. Preserving this surface is the task brief's hard constraint.
//   2. Filo's hash format (sorted-keys JSON.stringify + SHA-256 hex) is
//      different from @playtiss/core's CID format (dag-json + multiformats
//      base32 base, e.g. `bafkrei...`). They produce DIFFERENT hashes for
//      the same logical content. Switching the hash format would orphan
//      every existing on-disk ~/.playfilo/playfilo.db, every recorded
//      action_log.from_node / to_node, and every external_id ↔ hash
//      mapping. The 100%-reversibility constraint is incompatible with
//      that breakage.
//   3. Retcon — the canonical @playtiss/core consumer — does NOT blob-ify
//      its event log, revisions table, or branch_views table. Only its
//      content-addressed blob store satisfies @playtiss/core's
//      StorageProvider interface; everything else is plain columnar SQL.
//      The "use playtiss the way retcon uses it" pattern naturally lands
//      on a StorageProvider wrapper around the byte-blob store, with
//      Filo's domain semantics (nodes / refs / action_log) staying as-is.
//
// What this module does differently from filo/playfilo-db.ts:
//
//   • Exposes a SqliteBlobStorageProvider class that satisfies
//     @playtiss/core's StorageProvider interface, scoped to the `blobs`
//     table. This is the "playtiss-shaped" piece — a pluggable byte-store
//     contract callers can pass to load() / resolve() / store() etc.
//   • Adds storeAsset() / loadAsset() helpers that use @playtiss/core's
//     computeStorageBlock() for content addressing. These produce
//     CID-keyed blobs (e.g. `bafkrei...`) that COEXIST in the same
//     `blobs` table alongside Filo-hash-keyed blobs. The schema's `hash`
//     column accepts either format because both are opaque strings to
//     SQLite. Future patches that want true playtiss-shaped assets can
//     use these without touching the Filo-shape API.
//   • The Filo-shape exports (storeBlob, hashContent, commitNodeWithExternalId,
//     etc.) keep BIT-FOR-BIT identical hashing semantics with the original
//     filo/playfilo-db.ts so existing on-disk DBs keep working AND the
//     Mirin/Pax patches apply unchanged.
//
// API surface map: every export from filo/playfilo-db.ts is preserved here
// with the same signature and the same observable behavior. The only
// additions are:
//
//   • SqliteBlobStorageProvider                   (class)
//   • getStorageProvider(): StorageProvider       (singleton accessor)
//   • storeAsset(value): Promise<AssetId>         (playtiss-CID write)
//   • loadAsset(id): Promise<AssetValue>          (playtiss-CID read)
//   • hashContentPlaytiss(value): Promise<AssetId> (playtiss-CID hash, no store)
//
// Existing call sites (Mirin's patches, Pax's patches, Filo's patches)
// can ignore the additions entirely.
//
// ───────────────────────────────────────────────────────────────────────────

import {
	type AssetId,
	type AssetReferences,
	type AssetValue,
	computeHash,
	computeStorageBlock,
	load as playtissLoad,
	store as playtissStore,
	type StorageProvider,
} from "@playtiss/core";
import Database from "better-sqlite3";
import { createHash } from "crypto";
import { appendFileSync, existsSync, mkdirSync } from "fs";
import { homedir } from "os";
import { join } from "path";

const _debugLog = join(homedir(), ".playfilo", "tobe_debug.log");
export function _tobeLog(msg: string) {
	appendFileSync(_debugLog, `[${new Date().toISOString()}] ${msg}\n`);
}
const _log = _tobeLog;

// ─── Filo-shape Hash (preserved bit-for-bit) ────────────────────────────────
// Same algorithm as filo/playfilo-db.ts: sorted-keys JSON + SHA-256 hex.
// Do NOT change — this hash is embedded in every existing ~/.playfilo/*.db
// and in every recorded action_log row.
export function hashContent(obj: any): string {
	const json = JSON.stringify(obj, (_k, v) =>
		v !== null && typeof v === "object" && !Array.isArray(v)
			? Object.keys(v)
					.sort()
					.reduce((a: any, c) => {
						a[c] = v[c];
						return a;
					}, {})
			: v,
	);
	return createHash("sha256").update(json).digest("hex");
}

export function getDbPath(): string {
	const dir = join(homedir(), ".playfilo");
	if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
	return join(dir, "playfilo.db");
}

const db = new Database(getDbPath());
db.pragma("journal_mode = WAL");

// Note: This matches Playfilo Node Schema V4. Identical to filo/playfilo-db.ts.
db.exec(`
    CREATE TABLE IF NOT EXISTS blobs (hash TEXT PRIMARY KEY, type TEXT NOT NULL, content TEXT NOT NULL, thought_signature TEXT);
    CREATE TABLE IF NOT EXISTS nodes (id TEXT PRIMARY KEY, parent_id TEXT, role TEXT NOT NULL, parts_list TEXT NOT NULL, timestamp INTEGER NOT NULL, config_json TEXT, thought_signatures TEXT, system_prompt_hash TEXT, external_id TEXT);
    CREATE TABLE IF NOT EXISTS refs (name TEXT PRIMARY KEY, node_id TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS action_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INTEGER NOT NULL, action_type TEXT NOT NULL, from_node TEXT, to_node TEXT, metadata TEXT);
    CREATE INDEX IF NOT EXISTS idx_nodes_parent ON nodes(parent_id);
    CREATE INDEX IF NOT EXISTS idx_nodes_external_id ON nodes(external_id);
`);

// Try applying schema migration if connecting to an older V3 DB
try {
	db.exec("ALTER TABLE nodes ADD COLUMN external_id TEXT");
} catch (_e) {}
try {
	db.exec("CREATE INDEX idx_nodes_external_id ON nodes(external_id)");
} catch (_e) {}

// ─── @playtiss/core StorageProvider for the `blobs` table ───────────────────
// Mirrors retcon/src/storage.ts (SqliteStorageProvider). Stores raw bytes
// keyed by AssetId (CID string). Coexists with Filo-shape rows in the same
// table — `hash` column is opaque to SQLite, so a Filo SHA-256 hex string
// and a playtiss `bafkrei...` CID can both live there without collision
// (different alphabets + lengths).
//
// Two columns are required by the schema (`type`, `content`) but @playtiss/core
// blobs are pure bytes. We tag them with type='playtiss' and store the bytes
// in `content` as a base64 string so the existing schema stays unchanged.
// (A future schema bump could add a BLOB column for native byte storage.)
export class SqliteBlobStorageProvider implements StorageProvider {
	private readonly existsStmt;
	private readonly fetchStmt;
	private readonly saveStmt;

	constructor(private readonly database: Database.Database) {
		this.existsStmt = database.prepare("SELECT 1 FROM blobs WHERE hash = ?");
		this.fetchStmt = database.prepare("SELECT content FROM blobs WHERE hash = ? AND type = 'playtiss'");
		this.saveStmt = database.prepare(
			"INSERT OR IGNORE INTO blobs (hash, type, content) VALUES (?, 'playtiss', ?)",
		);
	}

	async hasBuffer(id: AssetId): Promise<boolean> {
		return this.existsStmt.get(id) !== undefined;
	}

	async fetchBuffer(id: AssetId): Promise<Uint8Array> {
		const row = this.fetchStmt.get(id) as { content: string } | undefined;
		if (!row) throw new Error(`Blob not found: ${id}`);
		return Buffer.from(row.content, "base64");
	}

	async saveBuffer(buffer: Uint8Array, id: AssetId, _references?: AssetReferences): Promise<void> {
		this.saveStmt.run(id, Buffer.from(buffer).toString("base64"));
	}
}

// Compile-time conformance witness — breaks the build if SqliteBlobStorageProvider
// drifts away from the @playtiss/core StorageProvider contract.
const _storageProviderConformance: StorageProvider = new Proxy({} as SqliteBlobStorageProvider, {
	get: () => () => {},
});
void _storageProviderConformance;

const _provider = new SqliteBlobStorageProvider(db);

/** Module-singleton accessor. Use this when threading the provider into
 *  @playtiss/core helpers (load/resolve/store) from external callers. */
export function getStorageProvider(): StorageProvider {
	return _provider;
}

/** Persist any AssetValue via @playtiss/core's content-addressed store.
 *  Returns the playtiss-shape AssetId (CID string, e.g. `bafkrei...`).
 *  Idempotent — reuses existing blobs when the CID already exists. */
export async function storeAsset(value: AssetValue): Promise<AssetId> {
	return playtissStore(value, _provider);
}

/** Load any previously-stored AssetValue by its playtiss CID.
 *  Returns the dag-json-decoded value (CIDs preserved as inline links). */
export async function loadAsset(id: AssetId): Promise<AssetValue> {
	return playtissLoad(id, _provider);
}

/** Compute the playtiss-shape CID of an AssetValue without persisting it.
 *  Useful for dedup checks and pre-write hashing. Returns a CID string,
 *  NOT a Filo-shape SHA-256 hex string — the two are not interchangeable.
 *  For the legacy Filo-shape hash, use hashContent(). */
export async function hashContentPlaytiss(value: AssetValue): Promise<AssetId> {
	return computeHash(value);
}

/** Pre-compute a single-block {cid, bytes} pair without going through the
 *  provider. Useful when the caller needs to embed the CID in a parent
 *  blob before saving (matches retcon's blobRefFromBytes pattern). */
export async function computeAssetBlock(value: AssetValue): Promise<{ cid: AssetId; bytes: Uint8Array }> {
	return computeStorageBlock(value);
}

// ─── Filo-shape blob store (UNCHANGED hashing semantics) ────────────────────
// Bit-for-bit identical to filo/playfilo-db.ts. The `type` column distinguishes
// these from playtiss-shape rows (any type !== 'playtiss').
export function storeBlob(type: string, content: any): string {
	const hash = hashContent({ type, content });
	db.prepare("INSERT OR IGNORE INTO blobs (hash, type, content) VALUES (?, ?, ?)").run(
		hash,
		type,
		JSON.stringify(content),
	);
	return hash;
}

export function getRef(name: string): string | null {
	const row = db.prepare("SELECT node_id FROM refs WHERE name = ?").get(name) as any;
	return row?.node_id || null;
}

export function clearRef(name: string): void {
	db.prepare("DELETE FROM refs WHERE name = ?").run(name);
}

// Unified tobe abort state. Handles three concerns:
// 1. HEAD freeze — setRef("PI_HEAD") is skipped while skipsRemaining > 0
// 2. Persist skip — _persist() skips DAG commits for stale events (tool result + aborted assistant)
// 3. Deferred context replacement — stash desired messages for agent-session auto-continue
// Parent tracking is handled naturally: PI_HEAD already points to the tobe target
// (set by handler before abort), so the first real persist gets the correct parent via getRef("PI_HEAD").
let tobeAbortState: {
	skipsRemaining: number;
	pendingContext: any[] | null;
} | null = null;

export function setTobeAbortState(messages: any[], skips: number = 2) {
	_log(`setTobeAbortState: stashing ${messages.length} messages, skips=${skips}`);
	tobeAbortState = { skipsRemaining: skips, pendingContext: messages };
}

// Called by _persist() shim — returns whether to skip the DAG commit.
// Parent override is no longer needed: _persist() uses getRef("PI_HEAD") directly,
// which already points to the tobe target (set by handler, frozen during abort).
export function checkTobeAbortState(): boolean {
	if (!tobeAbortState || tobeAbortState.skipsRemaining <= 0) return false;
	tobeAbortState.skipsRemaining--;
	_log(`checkTobeAbortState: SKIP (remaining=${tobeAbortState.skipsRemaining})`);
	return true;
}

// Called by agent-session auto-continue handler
export function consumePendingTobeContext(): any[] | null {
	if (!tobeAbortState) {
		_log(`consumePendingTobeContext: tobeAbortState is NULL`);
		return null;
	}
	const ctx = tobeAbortState.pendingContext;
	_log(
		`consumePendingTobeContext: returning ${ctx?.length ?? 0} messages (skipsRemaining=${tobeAbortState.skipsRemaining})`,
	);
	tobeAbortState = null; // fully clean up
	return ctx;
}

export function setRef(name: string, id: string) {
	if (name === "PI_HEAD") {
		// Unified tobe abort state takes precedence — skip setRef during abort
		if (tobeAbortState && tobeAbortState.skipsRemaining > 0) return;
	}
	db.prepare("INSERT OR REPLACE INTO refs (name, node_id) VALUES (?, ?)").run(name, id);
}

// Get a node's parent hash (null for root nodes)
export function getNodeParent(hash: string): string | null {
	const row = db.prepare("SELECT parent_id FROM nodes WHERE id = ?").get(hash) as any;
	return row?.parent_id || null;
}

// Map Pi's UUID to Playfilo's Content Hash
export function getHashByExternalId(externalId: string): string | null {
	if (!externalId) return null;
	const row = db.prepare("SELECT id FROM nodes WHERE external_id = ?").get(externalId) as any;
	return row?.id || null;
}

export function loadEntriesFromDAG(startHash: string | null): any[] {
	if (!startHash) return [];

	const trace: any[] = [];
	let currentId: string | null = startHash;
	while (currentId) {
		const node = db.prepare("SELECT * FROM nodes WHERE id = ?").get(currentId) as any;
		if (!node) break;
		const hashes = JSON.parse(node.parts_list);

		const contentArray: any[] = [];
		let isMetaNode = false;
		let metaEntry: any = null;

		for (const h of hashes) {
			const blob = db.prepare("SELECT * FROM blobs WHERE hash = ?").get(h) as any;
			if (blob) {
				const data = JSON.parse(blob.content);
				if (blob.type === "pi_meta") {
					// If it has a type field and no message role, it's likely a native Pi non-message entry
					if (data.type && !data.role) {
						isMetaNode = true;
						metaEntry = data;
					} else {
						// It's a fallback content part (e.g. image)
						contentArray.push(data);
					}
				} else if (blob.type === "pi_entry") {
					// Legacy support for V2
					isMetaNode = true;
					metaEntry = data;
				} else if (blob.type === "text") {
					contentArray.push({ type: "text", text: data });
				} else if (blob.type === "thinking") {
					contentArray.push({ type: "thinking", thinking: data });
				} else if (blob.type === "tool_call") {
					contentArray.push({
						type: "toolCall",
						id: data.id || hashContent(data),
						name: data.name,
						arguments: data.arguments ?? {},
					});
				} else if (blob.type === "tool_result") {
					// Handled below, as tool_result is a message-level property in Pi
					const trParts = (data.content || []).filter((c: any) => c.type === "text").map((c: any) => c.text);
					contentArray.push({ type: "text", text: trParts.join("\n") || JSON.stringify(data) });
				}
			}
		}

		if (isMetaNode && metaEntry) {
			trace.unshift(metaEntry);
		} else if (node.role === "toolResult") {
			// Reconstruct tool result message
			let data: any = {};
			const hashes = JSON.parse(node.parts_list);
			for (const h of hashes) {
				const blob = db.prepare("SELECT * FROM blobs WHERE hash = ?").get(h) as any;
				if (blob && blob.type === "tool_result") data = JSON.parse(blob.content);
			}
			trace.unshift({
				type: "message",
				id: node.external_id || currentId.slice(0, 8),
				parentId: node.parent_id ? getExternalIdByHash(node.parent_id) : null,
				timestamp: new Date(node.timestamp).toISOString(),
				message: {
					role: "toolResult",
					toolCallId: data.toolCallId || "unknown",
					toolName: data.toolName || "unknown",
					content: data.content || [],
					isError: data.isError ?? false,
					timestamp: node.timestamp,
				},
			});
		} else if (contentArray.length > 0 || node.role !== "pi_internal") {
			// Reconstruct SessionMessageEntry with full type shape
			const baseMessage: any = {
				role: node.role,
				content: contentArray,
				timestamp: node.timestamp,
			};

			if (node.role === "assistant") {
				// Extract model info from config_json if available
				let provider = "unknown";
				let model = "unknown";
				if (node.config_json) {
					try {
						const cfg = JSON.parse(node.config_json);
						if (cfg.agent) {
							// Unified format (Pi): { agent: "pi", model: { provider, id } }
							provider = cfg.model?.provider ?? "unknown";
							model = cfg.model?.id ?? "unknown";
						} else if (typeof cfg.model === "string") {
							// Terminal format: { model: "gemini-...", config: {...} }
							provider = "google";
							model = cfg.model;
						}
					} catch (_) {}
				}
				// Populate AssistantMessage fields expected by Pi TUI
				baseMessage.api = "chat";
				baseMessage.provider = provider;
				baseMessage.model = model;
				baseMessage.stopReason = "stop";
				baseMessage.usage = {
					input: 0,
					output: 0,
					cacheRead: 0,
					cacheWrite: 0,
					totalTokens: 0,
					cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 },
				};
			}

			trace.unshift({
				type: "message",
				id: node.external_id || currentId.slice(0, 8),
				parentId: node.parent_id ? getExternalIdByHash(node.parent_id) : null,
				timestamp: new Date(node.timestamp).toISOString(),
				message: baseMessage,
			});
		}
		currentId = node.parent_id;
	}
	return trace;
}

// Map Playfilo's Content Hash to Pi's UUID
export function getExternalIdByHash(hash: string): string | null {
	if (!hash) return null;
	const row = db.prepare("SELECT external_id FROM nodes WHERE id = ?").get(hash) as any;
	return row?.external_id || null;
}

export function commitNodeWithExternalId(
	parentIdHash: string | null,
	role: string,
	partHashes: string[],
	externalId: string,
	configJson?: string,
	systemPromptHash?: string,
): string {
	const timestamp = Date.now();
	const nodeData: Record<string, any> = {
		parent_id: parentIdHash,
		role,
		parts_list: partHashes,
		timestamp,
		external_id: externalId,
	};
	// Only include system_prompt_hash in hash when set (matches terminal's behavior:
	// JSON.stringify omits undefined keys, so hash stays compatible for null prompts)
	if (systemPromptHash) nodeData.system_prompt_hash = systemPromptHash;
	const id = hashContent(nodeData);

	db.prepare(
		"INSERT OR IGNORE INTO nodes (id, parent_id, role, parts_list, timestamp, config_json, system_prompt_hash, external_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
	).run(
		id,
		parentIdHash,
		role,
		JSON.stringify(partHashes),
		timestamp,
		configJson ?? null,
		systemPromptHash ?? null,
		externalId,
	);
	return id;
}

export interface StoredNode {
	id: string;
	parent_id: string | null;
	role: string;
	parts_list: string;
	timestamp: number;
	config_json: string | null;
	thought_signatures: string | null;
	system_prompt_hash: string | null;
	external_id: string | null;
}
export interface StoredBlob {
	hash: string;
	type: string;
	content: string;
}

export function nodeExists(nodeId: string): boolean {
	return db.prepare("SELECT 1 FROM nodes WHERE id = ?").get(nodeId) !== undefined;
}

export function resolveNodeId(input: string): { id: string } | { error: string } {
	if (nodeExists(input)) return { id: input };
	const rows = db.prepare("SELECT id FROM nodes WHERE id LIKE ?").all(`${input}%`) as { id: string }[];
	if (rows.length === 0) return { error: `Error: Node not found for "${input}".` };
	if (rows.length === 1) return { id: rows[0].id };
	return { error: `Error: Ambiguous hash prefix "${input}" matches ${rows.length} nodes.` };
}

function truncateText(text: string, maxLen: number): string {
	if (text.length <= maxLen) return text;
	return `${text.slice(0, maxLen)}...`;
}

export function handleLife(
	args: { focus_hash?: string; ancestors?: number; children?: boolean; filter_mode?: string; max_depth?: number },
	currentRefName: string = "PI_HEAD",
): string {
	const headId = getRef(currentRefName);
	let focusId = !args.focus_hash || args.focus_hash === "HEAD" ? headId : args.focus_hash;
	if (!focusId) return "Error: No HEAD set and no focus_hash provided.";

	// Strip pi: prefix (from life output format)
	if (focusId.startsWith("pi:")) focusId = focusId.slice(3);

	// Also try resolving external_id to hash for Pi compatibility
	const resolvedExternal = getHashByExternalId(focusId);
	if (resolvedExternal) focusId = resolvedExternal;

	if (focusId !== headId) {
		const resolved = resolveNodeId(focusId);
		if ("error" in resolved) return resolved.error;
		focusId = resolved.id;
	}

	const ancestorCount = args.ancestors ?? 3;
	const showChildren = args.children ?? true;
	const filterMode = args.filter_mode || "default";

	const chain: StoredNode[] = [];
	let currentId: string | null = focusId;
	for (let i = 0; i <= ancestorCount && currentId !== null; i++) {
		const node = db.prepare("SELECT * FROM nodes WHERE id = ?").get(currentId) as StoredNode | undefined;
		if (!node) break;
		chain.unshift(node);
		currentId = node.parent_id;
	}

	const getRoleAwarePreview = (node: StoredNode): string => {
		const role = node.role;
		const hashes = JSON.parse(node.parts_list) as string[];
		const texts: string[] = [];
		const toolCalls: string[] = [];
		let toolName: string | null = null;
		let toolResult: string | null = null;
		let metaType: string | null = null;

		for (const h of hashes) {
			const blob = db.prepare("SELECT * FROM blobs WHERE hash = ?").get(h) as StoredBlob | undefined;
			if (!blob) continue;
			try {
				const data = JSON.parse(blob.content);
				if (blob.type === "text") {
					texts.push(truncateText((data as string).replace(/\n/g, " "), 60));
				} else if (blob.type === "tool_call") {
					toolCalls.push(`[${data.name}: ${truncateText(JSON.stringify(data.arguments ?? {}), 40)}]`);
				} else if (blob.type === "tool_result") {
					toolName = data.toolName || "tool";
					const resultTexts = (data.content || []).filter((c: any) => c.type === "text").map((c: any) => c.text);
					toolResult = truncateText(resultTexts.join(" ").replace(/\n/g, " "), 40);
				} else if (blob.type === "pi_meta") {
					if (data.type) metaType = data.type;
				} else if (blob.type === "pi_entry") {
					const msg = data.message;
					if (msg?.content && Array.isArray(msg.content)) {
						const textPart = msg.content.find((c: any) => c.type === "text");
						if (textPart) texts.push(truncateText(textPart.text.replace(/\n/g, " "), 60));
					}
				}
			} catch (_e) {}
		}

		if (metaType) return `[${metaType}]`;
		if (role === "user") return `user: "${texts.join(" ") || "(no text)"}"`;
		if (role === "assistant") {
			if (texts.length > 0) return `assistant: "${texts.join(" ")}"`;
			if (toolCalls.length > 0) return `assistant: ${toolCalls.join(", ")}`;
			return "assistant: (no content)";
		}
		if (role === "toolResult") {
			return `${toolName ? `[${toolName}]` : "[tool]"}: "${toolResult || "(no output)"}"`;
		}
		if (texts.length > 0) return `${role}: "${texts.join(" ")}"`;
		return `(${role})`;
	};

	const shouldShowNode = (node: StoredNode): boolean => {
		// Always show FOCUS and HEAD nodes
		if (node.id === focusId || node.id === headId) return true;
		switch (filterMode) {
			case "user-only":
				return node.role === "user";
			case "no-tools":
				return node.role !== "toolResult";
			case "all":
				return true;
			default:
				// "default": hide pi_internal
				return node.role !== "pi_internal";
		}
	};

	const getChildren = (parentId: string): StoredNode[] =>
		db.prepare("SELECT * FROM nodes WHERE parent_id = ?").all(parentId) as StoredNode[];

	const markers = (nodeId: string): string => {
		const tags: string[] = [];
		if (nodeId === focusId) tags.push("FOCUS");
		if (nodeId === headId) tags.push("HEAD");
		return tags.length > 0 ? `  <-- ${tags.join(", ")}` : "";
	};

	const maxDepth = args.max_depth ?? 10;

	// Tree drawing characters
	const T = { BRANCH: "├── ", LAST: "└── ", PIPE: "│   ", SPACE: "    " };

	const formatTime = (timestamp: number): string => {
		const diff = Date.now() - timestamp;
		if (diff < 1000) return "now";
		if (diff < 60000) return `${Math.floor(diff / 1000)}s ago`;
		if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
		return `${Math.floor(diff / 3600000)}h ago`;
	};

	const nodeHasToolCalls = (node: StoredNode): boolean => {
		if (node.role !== "assistant") return false;
		const hashes = JSON.parse(node.parts_list) as string[];
		return hashes.some((h) => {
			const blob = db.prepare("SELECT type FROM blobs WHERE hash = ?").get(h) as StoredBlob | undefined;
			return blob?.type === "tool_call";
		});
	};

	const formatNodeLine = (node: StoredNode, suffix?: string): string => {
		const preview = getRoleAwarePreview(node);
		// Hide hash for assistant nodes with tool calls — they are not valid tobe
		// targets (dangling tool call with no result breaks the LLM message sequence).
		// Replace with same-width spaces so tool calls and results stay aligned.
		const hashText = node.external_id ? `pi:${node.external_id}` : node.id.slice(0, 12);
		const idCol = nodeHasToolCalls(node) ? " ".repeat(hashText.length + 2) : `[${hashText}]`;
		return `${idCol} (${formatTime(node.timestamp)}) ${preview}${markers(node.id)}${suffix || ""}`;
	};

	const countDescendants = (nodeId: string): number => {
		const children = getChildren(nodeId);
		let count = children.length;
		for (const c of children) count += countDescendants(c.id);
		return count;
	};

	const lines: string[] = [];

	// Recursive branch renderer with gutter tracking
	const renderBranch = (parentId: string, gutters: boolean[], depth: number): void => {
		if (depth > maxDepth) return;
		const children = getChildren(parentId).filter(shouldShowNode);
		for (let i = 0; i < children.length; i++) {
			const child = children[i];
			const isLast = i === children.length - 1;
			const prefix = gutters.map((g) => (g ? T.PIPE : T.SPACE)).join("") + (isLast ? T.LAST : T.BRANCH);
			lines.push(prefix + formatNodeLine(child));
			renderBranch(child.id, [...gutters, !isLast], depth + 1);
		}
	};

	// Ellipsis if ancestors were truncated
	if (chain.length > 0 && chain[0].parent_id !== null) lines.push("...");

	if (chain.length < 2 || !showChildren) {
		// No parent-of-focus branching: render all ancestors + focus flat
		for (const node of chain) {
			if (shouldShowNode(node)) lines.push(formatNodeLine(node));
		}
		// Show children of focus as a tree
		if (showChildren) renderBranch(focusId, [], 0);
	} else {
		// Render ancestors before parent-of-focus flat
		for (let i = 0; i < chain.length - 2; i++) {
			if (shouldShowNode(chain[i])) lines.push(formatNodeLine(chain[i]));
		}

		const parentNode = chain[chain.length - 2];
		const focusNode = chain[chain.length - 1];

		// Render parent flat
		if (shouldShowNode(parentNode)) lines.push(formatNodeLine(parentNode));

		// Check for siblings (other children of parent)
		const allChildren = getChildren(parentNode.id).filter(shouldShowNode);
		const siblings = allChildren.filter((c) => c.id !== focusNode.id);

		if (siblings.length === 0) {
			// No siblings — focus stays flat, children branch below it
			if (shouldShowNode(focusNode)) lines.push(formatNodeLine(focusNode));
			renderBranch(focusId, [], 0);
		} else {
			// Has siblings — render parent's children as a tree, focus last
			const sorted = [...siblings, focusNode];
			for (let i = 0; i < sorted.length; i++) {
				const child = sorted[i];
				const isLast = i === sorted.length - 1;
				const connector = isLast ? T.LAST : T.BRANCH;

				if (child.id === focusNode.id) {
					// Focus node — render it then recurse into its children
					lines.push(connector + formatNodeLine(child));
					renderBranch(focusId, [!isLast], 0);
				} else {
					// Sibling — show node with descendant count, no recursion
					const desc = countDescendants(child.id);
					const suffix = desc > 0 ? ` (${desc} descendant${desc > 1 ? "s" : ""})` : "";
					lines.push(connector + formatNodeLine(child, suffix));
				}
			}
		}
	}

	lines.push("--- end of archive ---");
	return lines.join("\n");
}

export function handleRecall(args: {
	hash: string;
	budget?: number;
	context_budget?: number;
	filter_mode?: string;
}): string {
	const budget = args.budget ?? 5000;
	const contextBudget = args.context_budget ?? 200;
	const filterMode = args.filter_mode || "default";

	let targetHash = args.hash;
	// Strip pi: prefix (from life output format)
	if (targetHash.startsWith("pi:")) {
		targetHash = targetHash.slice(3);
	}
	if (targetHash === "HEAD") {
		const headId = getRef("PI_HEAD");
		if (!headId) return "Error: No HEAD set.";
		targetHash = headId;
	} else {
		const resolvedExternal = getHashByExternalId(targetHash);
		if (resolvedExternal) {
			targetHash = resolvedExternal;
		} else {
			const resolved = resolveNodeId(targetHash);
			if ("error" in resolved) return resolved.error;
			targetHash = resolved.id;
		}
	}

	const targetNode = db.prepare("SELECT * FROM nodes WHERE id = ?").get(targetHash) as StoredNode;
	if (!targetNode) return `Error: Node ${targetHash.slice(0, 12)} not found.`;

	// Walk the chain root→target
	const chain: StoredNode[] = [];
	let currentId: string | null = targetHash;
	while (currentId !== null) {
		const node = db.prepare("SELECT * FROM nodes WHERE id = ?").get(currentId) as StoredNode | undefined;
		if (!node) break;
		chain.unshift(node);
		currentId = node.parent_id;
	}

	// Filter for context nodes
	const shouldShowInContext = (node: StoredNode): boolean => {
		switch (filterMode) {
			case "user-only":
				return node.role === "user";
			case "no-tools":
				return node.role !== "toolResult";
			case "all":
				return true;
			default:
				return node.role !== "pi_internal";
		}
	};

	// Build config section
	const configSection = targetNode.config_json || "// config: not available for this node";

	// Helper: get full text content of a node
	const getNodeText = (node: StoredNode): string => {
		const hashes = JSON.parse(node.parts_list) as string[];
		const parts: string[] = [];
		for (const h of hashes) {
			const blob = db.prepare("SELECT * FROM blobs WHERE hash = ?").get(h) as StoredBlob | undefined;
			if (!blob) continue;
			try {
				if (blob.type === "text" || blob.type === "thinking") {
					parts.push(JSON.parse(blob.content) as string);
				} else if (blob.type === "tool_call") {
					const fc = JSON.parse(blob.content);
					parts.push(`[tool_call: ${fc.name}(${JSON.stringify(fc.arguments ?? {})})]`);
				} else if (blob.type === "tool_result") {
					const tr = JSON.parse(blob.content);
					const text = (tr.content || [])
						.filter((c: any) => c.type === "text")
						.map((c: any) => c.text)
						.join("\n");
					parts.push(`[tool_result: ${tr.toolName} → ${text.slice(0, 200)}${text.length > 200 ? "..." : ""}]`);
				} else if (blob.type === "pi_entry") {
					const msg = JSON.parse(blob.content).message;
					if (msg?.content && Array.isArray(msg.content)) {
						const textPart = msg.content.find((c: any) => c.type === "text");
						if (textPart) parts.push(textPart.text);
					}
				} else if (blob.type === "pi_meta") {
					const meta = JSON.parse(blob.content);
					parts.push(`[${meta.type || "meta"}]`);
				} else if (blob.type === "inline_data") {
					parts.push("[inline_data]");
				}
			} catch (_e) {}
		}
		return parts.join("\n");
	};

	// Build contents array with truncation
	const targetIdx = chain.length - 1;
	const targetText = getNodeText(chain[targetIdx]);
	const targetRole = chain[targetIdx].role;

	// Collect context nodes (filtered)
	const contextNodes: { role: string; text: string }[] = [];
	for (let i = 0; i < targetIdx; i++) {
		if (shouldShowInContext(chain[i])) {
			contextNodes.push({ role: chain[i].role, text: getNodeText(chain[i]) });
		}
	}

	// Reserve budget for target
	const targetBudgetMax = budget - Math.min(contextNodes.length * contextBudget, budget / 2);

	// Build context entries (latest first priority)
	let contextUsed = 0;
	let firstIncludedIdx = 0;
	const contextEntries: string[] = [];

	for (let i = contextNodes.length - 1; i >= 0; i--) {
		const cn = contextNodes[i];
		const truncated = truncateText(cn.text, contextBudget);
		const entry = `  { role: "${cn.role}", text: "${truncated}" }  // archived`;
		if (contextUsed + entry.length > budget - targetBudgetMax && i < contextNodes.length - 1) {
			firstIncludedIdx = i + 1;
			break;
		}
		contextEntries.unshift(entry);
		contextUsed += entry.length;
		firstIncludedIdx = i;
	}

	// Build output
	const outputLines: string[] = [];
	outputLines.push("--- archived node content ---");
	outputLines.push("{");
	outputLines.push(`  config: ${configSection},`);
	outputLines.push("  contents: [");

	if (firstIncludedIdx > 0) {
		outputLines.push(`    // ... ${firstIncludedIdx} earlier turns omitted`);
	}

	for (const entry of contextEntries) {
		outputLines.push(`  ${entry},`);
	}

	// Target node (full or truncated)
	const remainingBudget = budget - contextUsed;
	let targetDisplay: string;
	if (targetText.length > remainingBudget) {
		targetDisplay =
			targetText.slice(0, remainingBudget) +
			`\n    // text truncated (showing ${remainingBudget}/${targetText.length} chars)...`;
	} else {
		targetDisplay = targetText;
	}
	const idDisplay = targetNode.external_id ? `pi:${targetNode.external_id}` : targetHash.slice(0, 12);
	outputLines.push(`    { role: "${targetRole}", text: "${targetDisplay}" }  // <-- TARGET NODE (${idDisplay})`);

	outputLines.push("  ]");
	outputLines.push("}");
	outputLines.push("--- end of archive ---");

	return outputLines.join("\n");
}

// ─── Deferred INCARNATE Action Log ──────────────────────────────────────────
// Stashed by tobe handler, consumed in _persist after carryover is committed with actual hash.

// Commit a tool_result node as a dead-end branch off the assistant that called tobe.
// This makes the departure point a "complete" node (assistant → toolResult) so that
// from_node in the INCARNATE action_log is not a dangling assistant-with-tool-call.
// No ref is updated — the node exists only as a DAG leaf for trace() to reference.
export function commitTobeDeparture(assistantHash: string, targetHash: string): string {
	const blobHash = storeBlob("tool_result", {
		toolCallId: "tobe_departure",
		toolName: "tobe",
		content: [{ type: "text", text: `Incarnation initiated → ${targetHash.slice(0, 12)}` }],
		isError: false,
	});
	const timestamp = Date.now();
	const nodeData = {
		parent_id: assistantHash,
		role: "toolResult",
		parts_list: [blobHash],
		timestamp,
	};
	const id = hashContent(nodeData);
	db.prepare(
		"INSERT OR IGNORE INTO nodes (id, parent_id, role, parts_list, timestamp) VALUES (?, ?, ?, ?, ?)",
	).run(id, assistantHash, "toolResult", JSON.stringify([blobHash]), timestamp);
	_log(`commitTobeDeparture: ${id.slice(0, 12)} (parent=${assistantHash.slice(0, 12)})`);
	return id;
}

let _pendingIncarnateLog: { fromNode: string | null; metadata: string } | null = null;

export function setPendingIncarnateLog(fromNode: string | null, metadata: string): void {
	_pendingIncarnateLog = { fromNode, metadata };
	_log(`setPendingIncarnateLog: from=${fromNode?.slice(0, 12)}`);
}

export function consumePendingIncarnateLog(toNodeHash: string, role?: string): void {
	if (!_pendingIncarnateLog) return;
	// Only consume on user messages — the carryover is always a user node.
	// In some continue() paths, an assistant response is committed before the
	// carryover arrives; filtering by role prevents logging the wrong to_node.
	if (role && role !== "user") return;
	const { fromNode, metadata } = _pendingIncarnateLog;
	_pendingIncarnateLog = null;
	logAction("INCARNATE", fromNode, toNodeHash, metadata);
	_log(`consumePendingIncarnateLog: logged INCARNATE to=${toNodeHash.slice(0, 12)}`);
}

// ─── Action Log ─────────────────────────────────────────────────────────────

export function logAction(actionType: string, fromNode: string | null, toNode: string, metadata?: string): void {
	db.prepare(
		"INSERT INTO action_log (timestamp, action_type, from_node, to_node, metadata) VALUES (?, ?, ?, ?, ?)",
	).run(Date.now(), actionType, fromNode, toNode, metadata ?? null);
}

export function handleTrace(args: { limit?: number; filter_mode?: string }): string {
	const limit = args.limit ?? 15;
	const filterMode = args.filter_mode || "default";

	// Walk ancestors from PI_HEAD — only show actions on the current lineage
	const headId = getRef("PI_HEAD");
	if (!headId) return "--- archived action log ---\n(no PI_HEAD set)\n--- end of archive ---";

	const ancestorIds: string[] = [];
	let cur: string | null = headId;
	while (cur) {
		ancestorIds.push(cur);
		const node = db.prepare("SELECT parent_id FROM nodes WHERE id = ?").get(cur) as
			| { parent_id: string | null }
			| undefined;
		if (!node || !node.parent_id) break;
		cur = node.parent_id;
	}

	// SQL-level filter by action_type so LIMIT counts visible events
	const placeholders = ancestorIds.map(() => "?").join(",");
	const navTypes = "'BOOT','INCARNATE','HYDRATE_GHOST'";
	const switchTypes = `${navTypes},'SESSION_SWITCH'`;
	let typeClause: string;
	if (filterMode === "all") {
		typeClause = "";
	} else if (filterMode === "switches") {
		typeClause = ` AND action_type IN (${switchTypes})`;
	} else {
		typeClause = ` AND action_type IN (${navTypes})`;
	}
	const rows = db
		.prepare(
			`SELECT * FROM action_log WHERE to_node IN (${placeholders})${typeClause} ORDER BY timestamp DESC LIMIT ?`,
		)
		.all(...ancestorIds, limit) as {
		id: number;
		timestamp: number;
		action_type: string;
		from_node: string | null;
		to_node: string | null;
		metadata: string | null;
	}[];

	if (rows.length === 0) return "--- archived action log ---\n(no actions recorded)\n--- end of archive ---";

	const lines: string[] = ["--- archived action log ---"];
	for (const row of rows) {
		const date = new Date(row.timestamp);
		const ts = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
		const from = row.from_node ? row.from_node.slice(0, 12) : "null";
		const to = row.to_node ? row.to_node.slice(0, 12) : "null";
		let line = `[${ts}] ${row.action_type}: ${from} → ${to}`;
		if (row.metadata) {
			const quoteBlock = (text: string, maxLen: number): string[] => {
				const trimmed = text.length > maxLen ? `${text.slice(0, maxLen)}\n...(truncated)` : text;
				return trimmed.split("\n").map((l) => `    > ${l}`);
			};
			try {
				const meta = JSON.parse(row.metadata);
				if (meta.carryover_message) {
					line += ". Carryover:";
					lines.push(line);
					lines.push(...quoteBlock(meta.carryover_message, 500));
					continue;
				}
				const metaStr = JSON.stringify(meta, null, 2);
				line += ". Metadata:";
				lines.push(line);
				lines.push(...quoteBlock(metaStr, 500));
				continue;
			} catch {
				// Raw string metadata (e.g. terminal's carryover messages)
				line += ". Carryover:";
				lines.push(line);
				lines.push(...quoteBlock(row.metadata, 500));
				continue;
			}
		}
		lines.push(line);
	}
	lines.push("--- end of archive ---");
	return lines.join("\n");
}
