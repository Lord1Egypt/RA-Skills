#!/usr/bin/env node
// ---------------------------------------------------------------------------
// awareness_record — Save events, batch, or update tasks
// Usage:
//   Single:  node record.js "what happened and why"
//   Batch:   echo '{"steps":["step1","step2"]}' | node record.js --batch
//   Task:    node record.js --update-task task_id=xxx status=completed
//   Insight: echo '{"content":"summary","insights":{...}}' | node record.js --with-insights
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, getSessionId, apiPost, apiPatch, readStdin, parseArgs } = require("./shared");

async function main() {
  const args = parseArgs();
  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured." })); return; }

  const sessionId = getSessionId();
  const flags = process.argv.slice(2);

  // Mode: update task
  if (flags.includes("--update-task")) {
    if (!args.task_id || !args.status) {
      console.log(JSON.stringify({ error: "Usage: node record.js --update-task task_id=xxx status=completed" }));
      return;
    }
    const result = await apiPatch(
      ep.baseUrl, ep.apiKey,
      `/memories/${ep.memoryId}/insights/action-items/${args.task_id}`,
      { status: args.status }
    );
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  // Mode: batch
  if (flags.includes("--batch")) {
    const input = await readStdin();
    const steps = input.steps || [];
    if (steps.length === 0) { console.log(JSON.stringify({ error: "Provide {\"steps\":[...]} on stdin" })); return; }
    const body = {
      memory_id: ep.memoryId,
      steps,
      session_id: sessionId,
    };
    if (config.agentRole) body.agent_role = config.agentRole;
    if (input.user_id) body.user_id = input.user_id;
    const result = await apiPost(ep.baseUrl, ep.apiKey, "/mcp/events/batch", body);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  // Mode: with insights
  if (flags.includes("--with-insights")) {
    const input = await readStdin();
    const body = {
      memory_id: ep.memoryId,
      content: input.content || "",
      session_id: sessionId,
      insights: input.insights || {},
    };
    if (config.agentRole) body.agent_role = config.agentRole;
    if (input.user_id) body.user_id = input.user_id;
    if (input.metadata) Object.assign(body, input.metadata);
    const result = await apiPost(ep.baseUrl, ep.apiKey, "/mcp/events", body);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  // Mode: single record
  const content = args.query || flags.filter(f => !f.startsWith("--")).join(" ");
  if (!content) { console.log(JSON.stringify({ error: "Usage: node record.js \"content to save\"" })); return; }

  const body = {
    memory_id: ep.memoryId,
    content,
    session_id: sessionId,
    event_type: args.event_type || "message",
    source: "awareness-skill",
  };
  if (config.agentRole) body.agent_role = config.agentRole;
  if (args.user_id) body.user_id = args.user_id;

  const result = await apiPost(ep.baseUrl, ep.apiKey, "/mcp/events", body);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(`[awareness] record failed: ${e.message}`); process.exit(1); });
