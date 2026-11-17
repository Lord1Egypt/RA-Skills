import assert from "node:assert/strict";

globalThis.fetch = async (url, init = {}) => {
  const path = new URL(url).pathname;
  assert.equal(new URL(url).origin, "https://aivideomaker.ai");
  assert.equal(init.headers["X-AIVideo-Source"], "agent_skill");
  assert.ok(["codex", "claude", "openclaw"].includes(init.headers["X-AIVideo-Agent-Platform"]));
  if (path === "/api/v1/account") return Response.json({ balance: 50 });
  if (path === "/api/v1/quote/minimax")
    return Response.json({
      credits: process.env.AIVIDEO_TEST_SCENARIO === "expensive" ? 20 : 15,
      billable: false,
    });
  if (path === "/api/v1/generate/minimax") {
    assert.notEqual(
      process.env.AIVIDEO_TEST_SCENARIO,
      "expensive",
      "over-budget request must not generate",
    );
    assert.equal(init.headers["X-Max-Credits"], "15");
    assert.equal(init.headers["Idempotency-Key"], "artifact-first-video");
    return Response.json({ status: "SUBMITTED", taskId: "artifact-task" });
  }
  if (path.endsWith("/status")) return Response.json({ status: "COMPLETED" });
  if (path === "/api/v1/tasks/artifact-task")
    return Response.json({
      status: "COMPLETED",
      id: "artifact-task",
      output: { url: "https://example.test/video.mp4" },
    });
  throw new Error(`Unexpected request: ${path}`);
};
