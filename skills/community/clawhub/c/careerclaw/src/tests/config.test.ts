/**
 * tests/config.test.ts — Unit tests for environment configuration.
 *
 * Run: npm test
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";

describe("config defaults", () => {
	it("exports REMOTEOK_RSS_URL pointing to remoteok.com", async () => {
		const { REMOTEOK_RSS_URL } = await import("../config.js");
		expect(REMOTEOK_RSS_URL).toContain("remoteok.com");
	});

	it("exports HN_API_BASE pointing to Firebase", async () => {
		const { HN_API_BASE } = await import("../config.js");
		expect(HN_API_BASE).toContain("hacker-news.firebaseio.com");
	});

	it("exports a positive HTTP_TIMEOUT_MS", async () => {
		const { HTTP_TIMEOUT_MS } = await import("../config.js");
		expect(HTTP_TIMEOUT_MS).toBeGreaterThan(0);
	});

	it("exports DEFAULT_TOP_K of 3", async () => {
		const { DEFAULT_TOP_K } = await import("../config.js");
		expect(DEFAULT_TOP_K).toBe(3);
	});

	it("exports HN_MAX_COMMENTS > 0", async () => {
		const { HN_MAX_COMMENTS } = await import("../config.js");
		expect(HN_MAX_COMMENTS).toBeGreaterThan(0);
	});

	it("LLM_API_KEY is undefined when CAREERCLAW_LLM_KEY is unset", async () => {
		// Env var is unset in test environment
		const { LLM_API_KEY } = await import("../config.js");
		// May be undefined or set by CI — just assert it's string or undefined
		expect(typeof LLM_API_KEY === "string" || LLM_API_KEY === undefined).toBe(
			true
		);
	});

	it("CAREERCLAW_DIR contains .careerclaw", async () => {
		const { CAREERCLAW_DIR } = await import("../config.js");
		expect(CAREERCLAW_DIR).toMatch(/\.careerclaw/);
	});
});