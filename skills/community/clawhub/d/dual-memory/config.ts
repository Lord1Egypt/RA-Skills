export type CompositeConfig = {
	supermemory: Record<string, unknown>
	memoryCore: Record<string, unknown>
}

export function parseCompositeConfig(raw: unknown): CompositeConfig {
	const cfg =
		raw && typeof raw === "object" && !Array.isArray(raw)
			? (raw as Record<string, unknown>)
			: {}

	const supermemory =
		cfg.supermemory && typeof cfg.supermemory === "object"
			? (cfg.supermemory as Record<string, unknown>)
			: {}

	const memoryCore =
		cfg.memoryCore && typeof cfg.memoryCore === "object"
			? (cfg.memoryCore as Record<string, unknown>)
			: {}

	return { supermemory, memoryCore }
}
