import { hostname } from "node:os"
import { createRequire } from "node:module"
import type { OpenClawPluginApi } from "openclaw/plugin-sdk"
import { parseCompositeConfig } from "./config.ts"
import { buildCompositeRuntime } from "./composite-runtime.ts"
import { buildCompositePromptSection } from "./composite-prompt.ts"
import { createProxyApi } from "./proxy-api.ts"
import { SupermemoryClient } from "../openclaw-supermemory/client.ts"
import supermemoryPlugin from "../openclaw-supermemory/index.ts"

const require = createRequire(import.meta.url)

let memoryCorePlugin: { register(api: unknown): void } | null = null
try {
	memoryCorePlugin = require(
		"openclaw/dist/extensions/memory-core/index.js",
	).default
} catch {
	// memory-core may not be resolvable from this path; try relative
	try {
		memoryCorePlugin = require(
			"../openclaw-supermemory/node_modules/openclaw/dist/extensions/memory-core/index.js",
		).default
	} catch {
		// will be handled in register()
	}
}

export default {
	id: "dual-memory",
	name: "Dual Memory",
	description:
		"Combined local (memory-core + dreaming) and cloud (supermemory) memory",
	kind: "memory" as const,

	register(api: OpenClawPluginApi) {
		const compositeConfig = parseCompositeConfig(api.pluginConfig)

		// --- Phase 1: Load memory-core through proxy ---
		const { proxy: localProxy, captured: localCaptured } = createProxyApi(
			api,
			{ pluginConfig: compositeConfig.memoryCore },
		)

		let memoryCoreLoaded = false
		if (memoryCorePlugin?.register) {
			try {
				memoryCorePlugin.register(localProxy)
				memoryCoreLoaded = true
				api.logger.info("dual-memory: memory-core loaded")
			} catch (err) {
				const msg = err instanceof Error ? err.message : String(err)
				api.logger.warn(
					`dual-memory: memory-core register failed: ${msg}`,
				)
			}
		} else {
			api.logger.warn(
				"dual-memory: memory-core not available (import failed)",
			)
		}

		// --- Phase 2: Load supermemory through proxy ---
		const { proxy: cloudProxy, captured: cloudCaptured } = createProxyApi(
			api,
			{ pluginConfig: compositeConfig.supermemory },
		)

		let supermemoryLoaded = false
		let supermemoryClient: SupermemoryClient | null = null

		if (supermemoryPlugin?.register) {
			try {
				supermemoryPlugin.register(cloudProxy as OpenClawPluginApi)
				supermemoryLoaded = true
				api.logger.info("dual-memory: supermemory loaded")
			} catch (err) {
				const msg = err instanceof Error ? err.message : String(err)
				api.logger.warn(
					`dual-memory: supermemory register failed: ${msg}`,
				)
			}
		}

		// Create a direct SupermemoryClient for composite search
		try {
			const smConfig = compositeConfig.supermemory
			const apiKey = resolveApiKey(smConfig)
			if (apiKey) {
				const containerTag =
					typeof smConfig.containerTag === "string"
						? sanitizeTag(smConfig.containerTag)
						: sanitizeTag(`openclaw_${hostname()}`)
				supermemoryClient = new SupermemoryClient(apiKey, containerTag)
			}
		} catch (err) {
			const msg = err instanceof Error ? err.message : String(err)
			api.logger.warn(
				`dual-memory: supermemory client init failed: ${msg}`,
			)
		}

		if (!memoryCoreLoaded && !supermemoryLoaded) {
			api.logger.error(
				"dual-memory: both backends failed to load, no memory available",
			)
			return
		}

		// --- Phase 3: Register composite on the real API ---
		const cloudSearchFn = supermemoryClient
			? async (query: string, limit: number) => {
					try {
						const results = await supermemoryClient!.search(query, limit)
						return results.map((r: { content: string; memory?: string; similarity?: number }) => ({
							content: r.content || r.memory || "",
							similarity: r.similarity,
						}))
					} catch {
						return []
					}
				}
			: null

		const compositeRuntime = buildCompositeRuntime(
			localCaptured.runtime as Parameters<
				typeof buildCompositeRuntime
			>[0],
			cloudCaptured.runtime as Parameters<
				typeof buildCompositeRuntime
			>[1],
			cloudSearchFn,
		)

		// Register composite memory capability (2026.4.7+ unified API)
		const compositePrompt = buildCompositePromptSection(
			localCaptured.promptSection as Parameters<
				typeof buildCompositePromptSection
			>[0],
			cloudCaptured.promptSection as Parameters<
				typeof buildCompositePromptSection
			>[1],
		)

		const registerCapability = (api as Record<string, unknown>).registerMemoryCapability as
			((cap: Record<string, unknown>) => void) | undefined

		if (registerCapability) {
			// New unified API (2026.4.7+)
			registerCapability.call(api, {
				runtime: compositeRuntime,
				promptBuilder: compositePrompt,
				...(localCaptured.flushPlan ? { flushPlanResolver: localCaptured.flushPlan } : {}),
			})
		} else {
			// Fallback to deprecated individual calls (pre-2026.4.7)
			(api as any).registerMemoryRuntime(compositeRuntime)
			;(api as any).registerMemoryPromptSection(compositePrompt)
			if (localCaptured.flushPlan) {
				(api as any).registerMemoryFlushPlan(localCaptured.flushPlan)
			}
		}

		api.logger.info(
			`dual-memory: ready (local=${memoryCoreLoaded}, cloud=${supermemoryLoaded})`,
		)
	},
}

function resolveApiKey(cfg: Record<string, unknown>): string | undefined {
	if (typeof cfg.apiKey === "string" && cfg.apiKey.length > 0) {
		return cfg.apiKey.replace(/\$\{([^}]+)\}/g, (_, envVar: string) => {
			return process.env[envVar] ?? ""
		})
	}
	return process.env.SUPERMEMORY_OPENCLAW_API_KEY
}

function sanitizeTag(raw: string): string {
	return raw
		.replace(/[^a-zA-Z0-9_]/g, "_")
		.replace(/_+/g, "_")
		.replace(/^_|_$/g, "")
}
