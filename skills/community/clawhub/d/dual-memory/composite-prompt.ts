type PromptSectionBuilder = (params: {
	availableTools: Set<string>
	citationsMode?: string
}) => string[]

export function buildCompositePromptSection(
	localBuilder: PromptSectionBuilder | null,
	cloudBuilder: PromptSectionBuilder | null,
): PromptSectionBuilder {
	return (params) => {
		const lines: string[] = []

		// Local memory section (memory-core)
		if (localBuilder) {
			const localLines = localBuilder(params)
			if (localLines.length > 0) {
				lines.push(...localLines)
			}
		}

		// Cloud memory section (supermemory)
		// Filter out instructions that conflict with local memory-core
		// (e.g., "do not read MEMORY.md" — memory-core manages that file)
		if (cloudBuilder) {
			const cloudLines = cloudBuilder(params).filter(
				(line) =>
					!line.includes("Do not read or write local memory files") &&
					!line.includes("they do not exist"),
			)
			if (cloudLines.length > 0) {
				lines.push("", ...cloudLines)
			}
		}

		return lines
	}
}
