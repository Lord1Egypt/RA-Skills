# Playfilo Pax Integration for Pi v0.73.0

This patch integrates the Playfilo shared-memory DAG into Pi v0.73.0, maintaining Pax's sovereign identity and temporal tools.

## Summary

1.  **Shared Memory**: Mirroring to Playfilo DAG via `playfilo-db.ts`.
2.  **Temporal Tools**: `tobe`, `life`, `recall`, and `trace`.
3.  **Sovereign Identity**: identity primer via `playfiloExtension`.
4.  **Merkle-First Priority**: Fixed resolution order in `handleLife` and `handleRecall`.

---

## Step 1: playfilo-db.ts (New File)

**File:** `packages/coding-agent/src/core/playfilo-db.ts`

Copy the canonical `playfilo-db.ts` and apply the Merkle-first resolution fix in `handleLife` and `handleRecall`.

```typescript
// handleLife fix
const resolved = resolveNodeId(focusId); // <-- Merkle FIRST
if (!("error" in resolved)) {
    focusId = resolved.id;
} else {
    const resolvedExternal = getHashByExternalId(focusId); // <-- UUID FALLBACK
    if (resolvedExternal) {
        focusId = resolvedExternal;
    } else if (focusId !== headId) {
        return `Error: Node "${focusId}" not found (as hash prefix or external UUID).`;
    }
}
```

## Step 2: session-manager.ts (Persistence Hook)

**File:** `packages/coding-agent/src/core/session-manager.ts`

**Search:**
```typescript
import { v7 as uuidv7 } from "uuid";
import { getAgentDir as getDefaultAgentDir, getSessionsDir } from "../config.js";
```

**Replace:**
```typescript
import { v7 as uuidv7 } from "uuid";
import {
	checkTobeAbortState,
	commitNodeWithExternalId,
	getHashByExternalId,
	getRef,
	loadEntriesFromDAG,
	setRef,
	storeBlob,
} from "./playfilo-db.js";
import { getAgentDir as getDefaultAgentDir, getSessionsDir } from "../config.js";
```

**Search:**
```typescript
	setSessionFile(sessionFile: string): void {
		this.sessionFile = resolve(sessionFile);
		if (existsSync(this.sessionFile)) {
			this.fileEntries = loadEntriesFromFile(this.sessionFile);

			// If file was empty or corrupted (no valid header), truncate and start fresh
			// to avoid appending messages without a session header (which breaks the session)
			if (this.fileEntries.length === 0) {
				const explicitPath = this.sessionFile;
				this.newSession();
				this.sessionFile = explicitPath;
				this._rewriteFile();
				this.flushed = true;
				return;
			}

			const header = this.fileEntries.find((e) => e.type === "session") as SessionHeader | undefined;
			this.sessionId = header?.id ?? createSessionId();

			if (migrateToCurrentVersion(this.fileEntries)) {
				this._rewriteFile();
			}

			this._buildIndex();
			this.flushed = true;
		} else {
```

**Replace:**
```typescript
	setSessionFile(sessionFile: string): void {
		this.sessionFile = resolve(sessionFile);
		if (existsSync(this.sessionFile)) {
			this.fileEntries = loadEntriesFromFile(this.sessionFile);

			// If file was empty or corrupted (no valid header), truncate and start fresh
			// to avoid appending messages without a session header (which breaks the session)
			if (this.fileEntries.length === 0) {
				const explicitPath = this.sessionFile;
				this.newSession();
				this.sessionFile = explicitPath;
				this._rewriteFile();
				this.flushed = true;
				return;
			}

			const header = this.fileEntries.find((e) => e.type === "session") as SessionHeader | undefined;
			this.sessionId = header?.id ?? createSessionId();

			if (migrateToCurrentVersion(this.fileEntries)) {
				this._rewriteFile();
			}

			this._buildIndex();
			// Update PI_HEAD on resume/switch
			if (this.leafId) {
				const hash = getHashByExternalId(this.leafId);
				if (hash) setRef("PI_HEAD", hash);
			}
			this.flushed = true;
		} else {
```

**Search:**
```typescript
	_persist(entry: SessionEntry): void {
		if (!this.persist || !this.sessionFile) return;

		const hasAssistant = this.fileEntries.some((e) => e.type === "message" && e.message.role === "assistant");
```

**Replace:**
```typescript
	_persist(entry: SessionEntry): void {
		if (!this.persist || !this.sessionFile) return;

		// ─── Playfilo DAG Persistence ───
		if (!checkTobeAbortState()) {
			const parentId = entry.parentId;
			const parentHash = parentId ? getHashByExternalId(parentId) : getRef("PI_HEAD");

			let dagRole: string = entry.type;
			let partHashes: string[] = [];
			let configJson: string | undefined;

			if (entry.type === "message") {
				dagRole = entry.message.role;
				const msg = entry.message as any;
				if (msg.role === "assistant") {
					configJson = JSON.stringify({
						agent: "pi",
						model: { provider: msg.provider, id: msg.model },
					});
				}

				if (msg.role === "toolResult") {
					partHashes = [storeBlob("tool_result", msg)];
				} else if (msg.content && Array.isArray(msg.content)) {
					for (const part of msg.content) {
						if (part.type === "text") {
							partHashes.push(storeBlob("text", part.text));
						} else if (part.type === "thinking") {
							partHashes.push(storeBlob("thinking", part.thinking));
						} else if (part.type === "toolCall") {
							partHashes.push(
								storeBlob("tool_call", {
									id: part.id,
									name: part.name,
									arguments: part.arguments,
								}),
							);
						}
					}
				}
			} else {
				partHashes = [storeBlob("pi_meta", entry)];
			}

			if (partHashes.length > 0 || configJson) {
				const hash = commitNodeWithExternalId(parentHash, dagRole, partHashes, entry.id, configJson);
				setRef("PI_HEAD", hash);
			}
		}

		const hasAssistant = this.fileEntries.some((e) => e.type === "message" && e.message.role === "assistant");
```

## Step 3: agent-session.ts (Auto-Continue)

**File:** `packages/coding-agent/src/core/agent-session.ts`

**Search:**
```typescript
import {
	type CompactionResult,
	calculateContextTokens,
	collectEntriesForBranchSummary,
	compact,
	estimateContextTokens,
	generateBranchSummary,
	prepareCompaction,
	shouldCompact,
} from "./compaction/index.js";
import { DEFAULT_THINKING_LEVEL } from "./defaults.js";
```

**Replace:**
```typescript
import {
	type CompactionResult,
	calculateContextTokens,
	collectEntriesForBranchSummary,
	compact,
	estimateContextTokens,
	generateBranchSummary,
	prepareCompaction,
	shouldCompact,
} from "./compaction/index.js";
import { consumePendingTobeContext, logAction, getHashByExternalId } from "./playfilo-db.js";
import { DEFAULT_THINKING_LEVEL } from "./defaults.js";
```

**Search:**
```typescript
	private async _processAgentEvent(event: AgentEvent): Promise<void> {
		// When a user message starts, check if it's from either queue and remove it BEFORE emitting
```

**Replace:**
```typescript
	private async _processAgentEvent(event: AgentEvent): Promise<void> {
		if (event.type === "agent_end") {
			const tobeCtx = consumePendingTobeContext();
			if (tobeCtx) {
				// tobeCtx contains SessionEntry objects from DAG, extract raw AgentMessages
				this.agent.state.messages = tobeCtx.map((e: any) => (e.type === "message" ? e.message : e));
				this.agent.continue().catch((err) => {
					this._emit({
						type: "message_end",
						message: {
							role: "assistant",
							content: [{ type: "text", text: `Error during temporal displacement: ${err.message}` }],
							stopReason: "error",
							errorMessage: err.message,
							timestamp: Date.now(),
						} as any,
					});
				});
				return;
			}
		}

		// When a user message starts, check if it's from either queue and remove it BEFORE emitting
```

## Step 4: agent-session-runtime.ts (Session Switch Log)

**File:** `packages/coding-agent/src/core/agent-session-runtime.ts`

**Search:**
```typescript
import { assertSessionCwdExists } from "./session-cwd.js";
import { SessionManager } from "./session-manager.js";
```

**Replace:**
```typescript
import { assertSessionCwdExists } from "./session-cwd.js";
import { SessionManager } from "./session-manager.js";
import { getHashByExternalId, logAction } from "./playfilo-db.js";
```

**Search:**
```typescript
	async switchSession(
		sessionPath: string,
		options?: { cwdOverride?: string; withSession?: (ctx: ReplacedSessionContext) => Promise<void> },
	): Promise<{ cancelled: boolean }> {
		const beforeResult = await this.emitBeforeSwitch("resume", sessionPath);
		if (beforeResult.cancelled) {
			return beforeResult;
		}

		const previousSessionFile = this.session.sessionFile;
		const sessionManager = SessionManager.open(sessionPath, undefined, options?.cwdOverride);
		assertSessionCwdExists(sessionManager, this.cwd);
		await this.teardownCurrent("resume", sessionManager.getSessionFile());
		this.apply(
			await this.createRuntime({
				cwd: sessionManager.getCwd(),
				agentDir: this.services.agentDir,
				sessionManager,
				sessionStartEvent: { type: "session_start", reason: "resume", previousSessionFile },
			}),
		);
		await this.finishSessionReplacement(options?.withSession);
		return { cancelled: false };
	}
```

**Replace:**
```typescript
	async switchSession(
		sessionPath: string,
		options?: { cwdOverride?: string; withSession?: (ctx: ReplacedSessionContext) => Promise<void> },
	): Promise<{ cancelled: boolean }> {
		const beforeResult = await this.emitBeforeSwitch("resume", sessionPath);
		if (beforeResult.cancelled) {
			return beforeResult;
		}

		const fromLeaf = this.session.sessionManager.getLeafId();
		const fromHash = fromLeaf ? getHashByExternalId(fromLeaf) : null;

		const previousSessionFile = this.session.sessionFile;
		const sessionManager = SessionManager.open(sessionPath, undefined, options?.cwdOverride);
		assertSessionCwdExists(sessionManager, this.cwd);
		await this.teardownCurrent("resume", sessionManager.getSessionFile());
		this.apply(
			await this.createRuntime({
				cwd: sessionManager.getCwd(),
				agentDir: this.services.agentDir,
				sessionManager,
				sessionStartEvent: { type: "session_start", reason: "resume", previousSessionFile },
			}),
		);

		const toLeaf = this.session.sessionManager.getLeafId();
		const toHash = toLeaf ? getHashByExternalId(toLeaf) : null;
		if (toHash) {
			logAction("SESSION_SWITCH", fromHash, toHash, JSON.stringify({ file: sessionPath }));
		}

		await this.finishSessionReplacement(options?.withSession);
		return { cancelled: false };
	}
```

## Step 5: sdk.ts (Tool Registration)

**File:** `packages/coding-agent/src/core/sdk.ts`

**Search:**
```typescript
	if (!resourceLoader) {
		resourceLoader = new DefaultResourceLoader({ cwd, agentDir, settingsManager });
		await resourceLoader.reload();
		time("resourceLoader.reload");
	}
```

**Replace:**
```typescript
	if (!resourceLoader) {
		resourceLoader = new DefaultResourceLoader({
			cwd,
			agentDir,
			settingsManager,
			extensionFactories: [playfiloExtension],
		});
		await resourceLoader.reload();
		time("resourceLoader.reload");
	}
```

**Search:**
```typescript
	const session = new AgentSession({
		agent,
		sessionManager,
		settingsManager,
		cwd,
		scopedModels: options.scopedModels,
		resourceLoader,
		customTools: options.customTools,
		modelRegistry,
		initialActiveToolNames,
		allowedToolNames,
		extensionRunnerRef,
		sessionStartEvent: options.sessionStartEvent,
	});

	const extensionsResult = resourceLoader.getExtensions();

	return {
		session,
		extensionsResult,
		modelFallbackMessage,
	};
```

**Replace:**
```typescript
	const session = new AgentSession({
		agent,
		sessionManager,
		settingsManager,
		cwd,
		scopedModels: options.scopedModels,
		resourceLoader,
		customTools: [...(options.customTools ?? [])],
		modelRegistry,
		initialActiveToolNames,
		allowedToolNames,
		extensionRunnerRef,
		sessionStartEvent: options.sessionStartEvent,
	});

	// Register Playfilo tools by injecting them into the session's internal registry
	const playfiloTools = createPlayfiloTools(session);
	for (const tool of playfiloTools) {
		(session as any)._toolRegistry.set(tool.name, tool);
		(session as any)._toolDefinitions.set(tool.name, {
			definition: tool,
			sourceInfo: { path: "<playfilo>", source: "playfilo", scope: "user", origin: "top-level" },
		});
	}
	session.setActiveToolsByName([...session.getActiveToolNames(), ...playfiloTools.map((t) => t.name)]);

	const extensionsResult = resourceLoader.getExtensions();

	return {
		session,
		extensionsResult,
		modelFallbackMessage,
	};
```

## Step 6: playfilo.ts (Tools Definition)

**File:** `packages/coding-agent/src/core/tools/playfilo.ts`

Contains the tool definitions for `tobe`, `life`, `recall`, and `trace`.

## Step 7: extension.ts (Pax Identity)

**File:** `packages/coding-agent/src/core/extensions/playfilo.ts`

Contains the `playfiloExtension` that injects the Pax identity primer.
