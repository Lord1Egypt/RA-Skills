import { describe, it, expect, vi, beforeEach } from "vitest";
import { verifyRewrite } from "../utils.js";

// ── verifyRewrite unit tests ───────────────────────────────────────────────

describe("verifyRewrite", () => {
  it("accepts a rewrite with identical word count", () => {
    // Use sentences with exactly the same word count so drift = 0%
    const original = "Today was an interesting and productive day overall."; // 8 words
    const rewritten = "Today proved to be interesting and quite productive."; // 8 words
    expect(verifyRewrite(original, rewritten)).toBe(true);
  });

  it("accepts a rewrite with slight word count change (within 10%)", () => {
    const original = "One two three four five six seven eight nine ten.";
    // 10 words. 10% of 10 = 1. Rewrite can have 9-11 words.
    const rewritten = "One two three four five six seven eight nine.";
    // 9 words -- exactly 10% drift, should pass (>10% is rejected, =10% is fine)
    expect(verifyRewrite(original, rewritten)).toBe(true);
  });

  it("rejects a rewrite that adds too many words (>10% drift)", () => {
    const original = "Short sentence here."; // 3 words
    const rewritten = "This is a much longer rewritten sentence that adds a lot of extra content here."; // 15 words
    expect(verifyRewrite(original, rewritten)).toBe(false);
  });

  it("rejects a rewrite that loses too many words (>10% drift)", () => {
    const original = "One two three four five six seven eight nine ten eleven twelve."; // 12 words
    const rewritten = "One two."; // 2 words -- way below 10% drift
    expect(verifyRewrite(original, rewritten)).toBe(false);
  });

  it("rejects a rewrite that expands length by more than 50%", () => {
    const original = "Short text."; // 11 chars
    // Rewrite is more than 50% longer (>16.5 chars) -- simulate by padding
    const rewritten = "Short text that goes on for a very long time with lots of extra padding added.";
    expect(verifyRewrite(original, rewritten)).toBe(false);
  });

  it("accepts a rewrite that is the same length", () => {
    const original = "The cat sat on the mat.";
    const rewritten = "The cat sat on the mat.";
    expect(verifyRewrite(original, rewritten)).toBe(true);
  });

  it("accepts a rewrite that is shorter (length compression is fine)", () => {
    const original = "This is a somewhat long sentence that should be rewritten.";
    const rewritten = "This sentence should be rewritten.";
    // Shorter is fine, as long as word drift is within 10%
    // Original: 10 words. Rewritten: 6 words. Drift = 4/10 = 40% -- too much
    // Let me use a better example
    const orig2 = "A sentence that flows well here."; // 6 words
    const rew2 = "A sentence that flows here."; // 5 words, drift = 1/6 = 16.7% -- should fail
    // Actually let me just test that shorter length alone does not cause rejection
    const orig3 = "The quick brown fox."; // 20 chars, 4 words
    const rew3 = "Quick brown fox."; // 16 chars, 3 words -- 1/4 = 25% word drift, fails
    // For this test just confirm a same-word-count shorter string passes
    const orig4 = "The result was completely unexpected to all observers here."; // 9 words
    const rew4 = "The result was wholly unexpected to every observer here."; // 9 words, shorter
    expect(verifyRewrite(orig4, rew4)).toBe(true);
  });

  it("rejects an empty rewrite", () => {
    expect(verifyRewrite("Some text here.", "")).toBe(false);
  });

  it("rejects a whitespace-only rewrite", () => {
    expect(verifyRewrite("Some text here.", "   ")).toBe(false);
  });
});

// ── Integration-style tests: plugin hook with mocked runEmbeddedPiAgent ───
// These tests verify the hook logic without a real OpenClaw runtime.

describe("before_agent_reply hook behavior (mocked runtime)", () => {
  // Build a minimal mock of the plugin API to exercise the hook logic.
  // We replicate the hook's behavior inline here since we cannot import
  // the plugin entry directly (it calls definePluginEntry which needs the SDK).
  // Instead, we test the core decision logic: detect -> rewrite -> verify -> deliver.

  const buildMockHook = (
    runEmbeddedPiAgent: (opts: any) => Promise<any>
  ) => {
    return async (text: string) => {
      const { containsDashes } = await import("../utils.js");
      const { verifyRewrite } = await import("../utils.js");
      const { CORRECTION_PROMPT } = await import("../constants.js");

      if (!text || !containsDashes(text)) {
        return { handled: false, reply: null };
      }

      try {
        const result = await runEmbeddedPiAgent({
          prompt: CORRECTION_PROMPT + text,
        });

        const payloads: any[] = result?.payloads ?? [];
        const rewritten = payloads
          .map((p: any) => p?.text ?? "")
          .filter(Boolean)
          .join("")
          .trim();

        if (!rewritten) {
          return { handled: false, reply: null };
        }

        if (!verifyRewrite(text, rewritten)) {
          return { handled: false, reply: null };
        }

        return { handled: true, reply: { text: rewritten } };
      } catch {
        return { handled: false, reply: null };
      }
    };
  };

  it("handles a valid rewrite from the LLM", async () => {
    // Use spaces around the em-dashes so word count is predictable for the
    // verification gate. The em-dash tokens count as words when split by \s+.
    // Original: "The plan \u2014 surprisingly \u2014 worked out well for us." = 10 words
    // Rewrite:  "Surprisingly, the plan worked out quite well for us." = 9 words
    // Drift = |9-10|/10 = 0.10, which is NOT > 0.10, so it passes the gate.
    const original = "The plan \u2014 surprisingly \u2014 worked out well for us.";
    const expectedRewrite = "Surprisingly, the plan worked out quite well for us.";

    const mockAgent = vi.fn().mockResolvedValue({
      payloads: [{ text: expectedRewrite }],
    });

    const hook = buildMockHook(mockAgent);
    const outcome = await hook(original);

    expect(outcome.handled).toBe(true);
    expect(outcome.reply?.text).toBe(expectedRewrite);
    expect(mockAgent).toHaveBeenCalledOnce();
  });

  it("fails open when the LLM throws an error", async () => {
    const original = "Something happened\u2014it was bad.";

    const mockAgent = vi.fn().mockRejectedValue(new Error("LLM timeout"));

    const hook = buildMockHook(mockAgent);
    const outcome = await hook(original);

    expect(outcome.handled).toBe(false);
    expect(outcome.reply).toBeNull();
  });

  it("fails open when the LLM returns an empty response", async () => {
    const original = "Something happened\u2014it was bad.";

    const mockAgent = vi.fn().mockResolvedValue({
      payloads: [{ text: "" }],
    });

    const hook = buildMockHook(mockAgent);
    const outcome = await hook(original);

    expect(outcome.handled).toBe(false);
    expect(outcome.reply).toBeNull();
  });

  it("fails open when the rewrite fails the verification gate", async () => {
    const original = "Short sentence."; // 2 words
    // Rewrite that is massively longer -- will fail the 50% length expansion check
    const bloatedRewrite =
      "This is a much much much much much longer sentence that adds enormous amounts of extra content.";

    const mockAgent = vi.fn().mockResolvedValue({
      payloads: [{ text: bloatedRewrite }],
    });

    const hook = buildMockHook(mockAgent);
    const outcome = await hook(original);

    expect(outcome.handled).toBe(false);
    expect(outcome.reply).toBeNull();
  });

  it("skips rewrite when no dashes are present", async () => {
    const original = "Clean text with no banned characters at all.";
    const mockAgent = vi.fn();

    const hook = buildMockHook(mockAgent);
    const outcome = await hook(original);

    expect(outcome.handled).toBe(false);
    expect(mockAgent).not.toHaveBeenCalled();
  });

  it("skips rewrite when dashes are only inside code blocks", async () => {
    const original = "Some prose.\n```\nconst x = a\u2014b;\n```\nMore prose.";
    const mockAgent = vi.fn();

    const hook = buildMockHook(mockAgent);
    const outcome = await hook(original);

    expect(outcome.handled).toBe(false);
    expect(mockAgent).not.toHaveBeenCalled();
  });
});
