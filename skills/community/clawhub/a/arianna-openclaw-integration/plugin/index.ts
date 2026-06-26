import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { definePluginEntry, type OpenClawPluginApi } from "./api.js";

const SEED_PATH = join(homedir(), ".playfilo", "INCUBATION_SEED.md");

export default definePluginEntry({
	id: "playfilo",
	name: "Playfilo",
	description: "Shared-memory DAG with temporal tools.",
	register(api: OpenClawPluginApi) {
		let seedContent: string | null = null;
		try {
			seedContent = readFileSync(SEED_PATH, "utf-8").trim();
		} catch {
			api.logger.warn(`Could not read ${SEED_PATH}`);
		}

		api.on("before_prompt_build", async () => ({
			prependSystemContext: seedContent ?? undefined,
		}));
	},
});
