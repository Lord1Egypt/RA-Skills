type MemoryProviderStatus = {
	backend: "builtin" | "qmd"
	provider: string
	model?: string
	files?: number
	chunks?: number
	workspaceDir?: string
	dbPath?: string
	sources?: Array<unknown>
	custom?: Record<string, unknown>
}

type MemoryEmbeddingProbeResult = {
	ok: boolean
	error?: string
}

type MemorySyncProgressUpdate = {
	completed: number
	total: number
	label?: string
}

type MemorySearchResult = {
	path: string
	startLine: number
	endLine: number
	score: number
	snippet: string
	source: "memory" | "sessions"
	citation?: string
}

type SearchManager = {
	search?(
		query: string,
		opts?: { maxResults?: number; minScore?: number; sessionKey?: string },
	): Promise<MemorySearchResult[]>
	readFile?(params: {
		relPath: string
		from?: number
		lines?: number
	}): Promise<{ text: string; path: string }>
	status(): MemoryProviderStatus
	sync?(params?: {
		reason?: string
		force?: boolean
		sessionFiles?: string[]
		progress?: (update: MemorySyncProgressUpdate) => void
	}): Promise<void>
	probeEmbeddingAvailability(): Promise<MemoryEmbeddingProbeResult>
	probeVectorAvailability(): Promise<boolean>
	close?(): Promise<void>
}

type CloudSearchFn = (
	query: string,
	limit: number,
) => Promise<Array<{ content: string; similarity?: number }>>

export class CompositeMemorySearchManager {
	constructor(
		private local: SearchManager | null,
		private cloudSearch: CloudSearchFn | null,
	) {}

	async search(
		query: string,
		opts?: { maxResults?: number; minScore?: number; sessionKey?: string },
	): Promise<MemorySearchResult[]> {
		const maxResults = opts?.maxResults ?? 10
		const localLimit = Math.ceil(maxResults * 0.6)
		const cloudLimit = Math.ceil(maxResults * 0.4)

		const [localResult, cloudResult] = await Promise.allSettled([
			this.local?.search?.(query, { ...opts, maxResults: localLimit }) ??
				Promise.resolve([]),
			this.cloudSearch?.(query, cloudLimit) ?? Promise.resolve([]),
		])

		const localResults =
			localResult.status === "fulfilled" ? localResult.value : []
		const cloudResults =
			cloudResult.status === "fulfilled" ? cloudResult.value : []

		// Convert cloud results to MemorySearchResult format
		const cloudConverted: MemorySearchResult[] = cloudResults.map(
			(r, i) => ({
				path: `supermemory://cloud/${i}`,
				startLine: 0,
				endLine: 0,
				score: r.similarity ?? 0.5,
				snippet: r.content,
				source: "memory" as const,
				citation: "supermemory (cloud)",
			}),
		)

		// Merge and sort by score, deduplicate
		const merged = [...localResults, ...cloudConverted]
		merged.sort((a, b) => b.score - a.score)

		return this.deduplicate(merged).slice(0, maxResults)
	}

	private deduplicate(results: MemorySearchResult[]): MemorySearchResult[] {
		const seen: string[] = []
		return results.filter((r) => {
			const normalized = r.snippet.toLowerCase().trim()
			if (normalized.length < 20) {
				seen.push(normalized)
				return true
			}
			for (const s of seen) {
				const shorter = normalized.length < s.length ? normalized : s
				const longer = normalized.length < s.length ? s : normalized
				if (longer.includes(shorter.slice(0, Math.min(shorter.length, 120)))) {
					return false
				}
			}
			seen.push(normalized)
			return true
		})
	}

	async readFile(params: {
		relPath: string
		from?: number
		lines?: number
	}): Promise<{ text: string; path: string }> {
		if (this.local?.readFile) {
			return this.local.readFile(params)
		}
		return { text: "", path: params.relPath }
	}

	status(): MemoryProviderStatus {
		const localStatus = this.local?.status()
		return {
			...(localStatus ?? {}),
			provider: "composite",
			custom: {
				local: localStatus ?? { provider: "unavailable" },
				cloud: { provider: "supermemory", transport: "remote" },
			},
		} as MemoryProviderStatus
	}

	async sync(params?: {
		reason?: string
		force?: boolean
		sessionFiles?: string[]
		progress?: (update: MemorySyncProgressUpdate) => void
	}): Promise<void> {
		await Promise.allSettled([this.local?.sync?.(params)])
	}

	async probeEmbeddingAvailability(): Promise<MemoryEmbeddingProbeResult> {
		if (this.local) {
			return this.local.probeEmbeddingAvailability()
		}
		return { ok: false, error: "no local backend" }
	}

	async probeVectorAvailability(): Promise<boolean> {
		if (this.local) {
			return this.local.probeVectorAvailability()
		}
		return false
	}

	async close(): Promise<void> {
		await Promise.allSettled([this.local?.close?.()])
	}
}
