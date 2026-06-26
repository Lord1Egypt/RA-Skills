#!/usr/bin/env node
// ---------------------------------------------------------------------------
// Stop hook — Auto-capture: save session checkpoint after Claude responds
// Protocol: receives JSON on stdin, runs async (fire-and-forget)
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, getSessionId, apiPost, readStdin } = require("./shared");

async function main() {
  let input = {};
  try { input = await readStdin(); } catch { /* no stdin */ }

  // Only capture on meaningful completions (skip mid-conversation tool use)
  if ((input.stop_reason || input.stopReason) === "tool_use") process.exit(0);

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) process.exit(0);

  const sessionId = getSessionId();

  try {
    const parts = [];
    if (input.tool_name) parts.push(`Last tool: ${input.tool_name}`);
    const content = parts.length > 0 ? parts.join("\n") : "[session-checkpoint]";

    const headers = { "Content-Type": "application/json", Accept: "application/json" };
    if (ep.apiKey) headers.Authorization = `Bearer ${ep.apiKey}`;

    await fetch(`${ep.baseUrl}/mcp/events`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        memory_id: ep.memoryId,
        content,
        session_id: sessionId,
        agent_role: config.agentRole || undefined,
        event_type: "session_checkpoint",
        source: "awareness-skill",
      }),
      signal: AbortSignal.timeout(5000),
    });
  } catch (err) {
    process.stderr.write(`[awareness] capture failed: ${err.message}\n`);
  }
}

main().catch(() => process.exit(0));
