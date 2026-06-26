import { CompositeMemorySearchManager } from "./composite-search-manager.ts"

type MemoryRuntimeBackendConfig =
	| { backend: "builtin" }
	| { backend: "qmd"; qmd?: { command?: string } }

type MemoryPluginRuntime = {
	getMemorySearchManager(params: {
		cfg: unknown
		agentId: string
		purpose?: "default" | "status"
	}): Promise<{
		manager: unknown | null
		error?: string
	}>
	resolveMemoryBackendConfig(params: {
		cfg: unknown
		agentId: string
	}): MemoryRuntimeBackendConfig
	closeAllMemorySearchManagers?(): Promise<void>
}

type CloudSearchFn = (
	query: string,
	limit: number,
) => Promise<Array<{ content: string; similarity?: number }>>

export function buildCompositeRuntime(
	localRuntime: MemoryPluginRuntime | null,
	cloudRuntime: MemoryPluginRuntime | null,
	cloudSearchFn: CloudSearchFn | null,
): MemoryPluginRuntime {
	return {
		async getMemorySearchManager(params) {
			const [localResult, cloudResult] = await Promise.allSettled([
				localRuntime?.getMemorySearchManager(params) ??
					Promise.resolve({ manager: null }),
				cloudRuntime?.getMemorySearchManager(params) ??
					Promise.resolve({ manager: null }),
			])

			const localManager =
				localResult.status === "fulfilled"
					? (localResult.value?.manager as Record<string, unknown> | null)
					: null
			const _cloudManager =
				cloudResult.status === "fulfilled"
					? cloudResult.value?.manager
					: null

			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			const composite = new CompositeMemorySearchManager(
				localManager as any,
				cloudSearchFn,
			)

			return { manager: composite }
		},

		resolveMemoryBackendConfig(params) {
			// Delegate to local runtime — this drives the builtin/qmd decision
			if (localRuntime) {
				return localRuntime.resolveMemoryBackendConfig(params)
			}
			return { backend: "builtin" as const }
		},

		async closeAllMemorySearchManagers() {
			await Promise.allSettled([
				localRuntime?.closeAllMemorySearchManagers?.(),
				cloudRuntime?.closeAllMemorySearchManagers?.(),
			])
		},
	}
}
