type CapturedSlotRegistrations = {
	runtime: unknown | null
	promptSection: ((params: unknown) => string[]) | null
	flushPlan: ((params: unknown) => unknown | null) | null
}

/**
 * Creates a proxy around the real OpenClawPluginApi that intercepts
 * memory-slot registrations and captures them instead of forwarding.
 *
 * Intercepts both the new unified API (registerMemoryCapability, 2026.4.7+)
 * and the deprecated individual calls (registerMemoryRuntime, etc.)
 * for backward compatibility.
 *
 * All other API calls pass through to the real API.
 */
export function createProxyApi(
	realApi: unknown,
	overrides: { pluginConfig?: unknown } = {},
): { proxy: unknown; captured: CapturedSlotRegistrations } {
	const captured: CapturedSlotRegistrations = {
		runtime: null,
		promptSection: null,
		flushPlan: null,
	}

	const proxy = new Proxy(realApi as Record<string, unknown>, {
		get(target, prop, receiver) {
			// Intercept new unified API (2026.4.7+)
			if (prop === "registerMemoryCapability") {
				return (capability: Record<string, unknown>) => {
					if (capability.runtime) captured.runtime = capability.runtime
					if (capability.promptBuilder) captured.promptSection = capability.promptBuilder as (params: unknown) => string[]
					if (capability.flushPlanResolver) captured.flushPlan = capability.flushPlanResolver as (params: unknown) => unknown | null
					// Pass through publicArtifacts and other fields to the real API
					const realFn = Reflect.get(target, prop, receiver)
					if (typeof realFn === "function") {
						const passthrough = { ...capability }
						delete passthrough.runtime
						delete passthrough.promptBuilder
						delete passthrough.flushPlanResolver
						if (Object.keys(passthrough).length > 0) {
							realFn.call(target, passthrough)
						}
					}
				}
			}

			// Intercept deprecated individual calls (backward compat)
			if (prop === "registerMemoryRuntime") {
				return (rt: unknown) => {
					captured.runtime = rt
				}
			}
			if (prop === "registerMemoryPromptSection") {
				return (builder: (params: unknown) => string[]) => {
					captured.promptSection = builder
				}
			}
			if (prop === "registerMemoryFlushPlan") {
				return (resolver: (params: unknown) => unknown | null) => {
					captured.flushPlan = resolver
				}
			}

			// Override pluginConfig so each sub-plugin gets its own namespaced config
			if (prop === "pluginConfig" && overrides.pluginConfig !== undefined) {
				return overrides.pluginConfig
			}

			// Everything else passes through to the real API
			const value = Reflect.get(target, prop, receiver)
			if (typeof value === "function") {
				return value.bind(target)
			}
			return value
		},
	})

	return { proxy, captured }
}
