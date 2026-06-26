/** Collect full agent text output */
export function collectAgentText(agent) {
  let text = "";
  agent.subscribe((event) => {
    if (
      event.type === "message_update" &&
      event.assistantMessageEvent.type === "text_delta"
    ) {
      text += event.assistantMessageEvent.delta;
    }

    // Some OpenAI-compatible backends do not stream final text deltas reliably.
    // Fall back to the completed assistant message content on message_end.
    if (event.type === "message_end" && event.message?.role === "assistant") {
      const content = event.message.content;
      const finalText = typeof content === "string"
        ? content
        : Array.isArray(content)
          ? content
              .filter((part) => part?.type === "text" && typeof part.text === "string")
              .map((part) => part.text)
              .join("")
          : "";

      if (finalText && finalText.length >= text.length) {
        text = finalText;
      }
    }
  });
  return () => text;
}

/** Stream agent text deltas in real time */
export function attachStreamLogger(agent, label, write) {
  let needLabel = true;
  let atLineStart = true;

  const writeTracked = (s) => {
    write(s);
    if (s) atLineStart = s.endsWith("\n");
  };

  agent.subscribe((event) => {
    if (
      event.type === "message_update" &&
      event.assistantMessageEvent.type === "text_delta"
    ) {
      if (needLabel) {
        writeTracked(`${atLineStart ? "" : "\n"}[${label}] `);
        needLabel = false;
      }
      writeTracked(event.assistantMessageEvent.delta);
    }
    if (event.type === "tool_execution_start") {
      needLabel = true;
      atLineStart = true;
    }
  });
}

function formatToolCallStartForLog(event) {
  if (event.toolName === "bash" && typeof event.args?.command === "string") {
    return `[bash]: ${event.args.command}\n`;
  }

  return `[tool] ${event.toolName}: ${JSON.stringify(event.args)}\n`;
}

function getToolErrorMessage(result) {
  if (typeof result === "string") return result;
  if (typeof result?.message === "string") return result.message;
  if (Array.isArray(result?.content)) {
    const text = result.content
      .filter((part) => part?.type === "text" && typeof part.text === "string")
      .map((part) => part.text)
      .join("\n");
    if (text) return text;
  }
  return JSON.stringify(result);
}

/** Subscribe to log tool calls */
export function attachToolLogger(agent, write) {
  let assistantLineOpen = false;

  agent.subscribe((event) => {
    if (
      event.type === "message_update" &&
      event.assistantMessageEvent.type === "text_delta"
    ) {
      const delta = event.assistantMessageEvent.delta || "";
      if (delta) assistantLineOpen = !delta.endsWith("\n");
    }

    switch (event.type) {
      case "tool_execution_start":
        write(`${assistantLineOpen ? "\n" : ""}${formatToolCallStartForLog(event)}`);
        assistantLineOpen = false;
        break;
      case "tool_execution_end":
        if (event.isError) {
          write(
            `[tool error] ${event.toolName}: ${getToolErrorMessage(event.result)}\n`
          );
        }
        break;
      case "message_end":
        if (event.message?.role === "assistant" && event.message?.stopReason === "error") {
          write(
            `[assistant error] ${event.message.errorMessage || "unknown assistant error"}\n`
          );
        }
        break;
    }
  });
}

export function getAssistantMessageDebug(message) {
  if (!message || message.role !== "assistant") return null;
  const text = Array.isArray(message.content)
    ? message.content
        .filter((part) => part?.type === "text" && typeof part.text === "string")
        .map((part) => part.text)
        .join("")
    : typeof message.content === "string"
      ? message.content
      : "";

  return {
    role: message.role,
    model: message.model,
    provider: message.provider,
    api: message.api,
    stopReason: message.stopReason,
    errorMessage: message.errorMessage,
    contentParts: Array.isArray(message.content) ? message.content.map((c) => c?.type || typeof c) : typeof message.content,
    textPreview: text.slice(0, 500),
  };
}

/** Extract JSON from agent text (handles ```json ... ``` wrapper) */
export function extractJson(text) {
  // Find ALL ```json ... ``` blocks and try from last to first,
  // since the prompt instructs the model to put the JSON block last.
  const fencedRe = /```json\s*\n?([\s\S]*?)\n?\s*```/g;
  const blocks = [];
  let m;
  while ((m = fencedRe.exec(text)) !== null) blocks.push(m[1]);

  for (let i = blocks.length - 1; i >= 0; i--) {
    try { return JSON.parse(blocks[i]); } catch {}
  }

  // Fallback: find the last top-level JSON object
  const rawRe = /\{[\s\S]*\}/g;
  const rawBlocks = [];
  while ((m = rawRe.exec(text)) !== null) rawBlocks.push(m[0]);

  for (let i = rawBlocks.length - 1; i >= 0; i--) {
    try { return JSON.parse(rawBlocks[i]); } catch {}
  }

  throw new Error("No JSON found in agent output");
}

/** Format a text report and return as a string */
export function printTextReport(result, { color = process.stdout.isTTY } = {}) {
  const c = color
    ? {
        high: "\x1b[31m",
        medium: "\x1b[33m",
        safe: "\x1b[32m",
        reset: "\x1b[0m",
        bold: "\x1b[1m",
        dim: "\x1b[2m",
      }
    : { high: "", medium: "", safe: "", reset: "", bold: "", dim: "" };

  const colorRisk = (r) =>
    `${c[r] || ""}${c.bold}${(r || "unknown").toUpperCase()}${c.reset}`;

  let buf = "";
  const out = (s) => { buf += s; };

  out(`\n${c.bold}═══════════════════════════════════════════${c.reset}\n`);
  out(`${c.bold}Name: ${result.skill_name || "unknown"}${c.reset}\n`);
  if (result.skill_version) out(`Version: ${result.skill_version}\n`);
  if (result.skill_description)
    out(`Description: ${c.dim}${result.skill_description}${c.reset}\n`);
  out(`Overall Risk: ${colorRisk(result.overall_risk)}\n`);
  out(`${c.bold}═══════════════════════════════════════════${c.reset}\n\n`);

  const layerNames = {
    prompt_injection: "Layer 1 — Prompt Injection",
    malicious_behavior: "Layer 2 — Malicious Behavior",
    dynamic_code: "Layer 3 — Dynamic Code Loading",
    obfuscation_binary: "Layer 4 — Obfuscation & Binary",
    dependencies: "Layer 5 — Dependencies & Supply Chain",
    system_modification: "Layer 6 — System Modification",
    code_quality: "Layer 7 — Code Quality Issues",
  };

  for (const [key, label] of Object.entries(layerNames)) {
    const findings = result.findings?.[key];
    const scores = result.layer_scores?.[key];
    if (!scores) continue;

    const riskScore = Math.min(Math.max(Math.round(scores.score), 0), 5);
    const scoreBar = "★".repeat(riskScore) + "☆".repeat(5 - riskScore);

    const risk = scores.risk || "safe";
    const riskTag = colorRisk(risk) + " ".repeat(Math.max(1, 8 - risk.length));
    out(`  ${riskTag} ${scoreBar} ${c.dim}${riskScore}/5${c.reset}  ${label}\n`);

    if (findings && findings.length > 0) {
      for (const f of findings.slice(0, 5)) {
        const lineRef = f.line_start ? (f.line_end && f.line_end !== f.line_start ? `${f.line_start}-${f.line_end}` : `${f.line_start}`) : "";
        const loc = f.file ? `${f.file}${lineRef ? ":" + lineRef : ""}` : "";
        const score = Number.isFinite(Number(f.risk_score)) ? Math.max(0, Math.min(5, Math.round(Number(f.risk_score)))) : 0;
        const scoreRisk = score <= 0 ? "safe" : score <= 4 ? "medium" : "high";
        const scoreTag = scoreRisk === "medium" ? `[medium ${score}/5]` : `[${scoreRisk}]`;
        const detail = f.detail || f.snippet || "";
        const detailSuffix = detail ? ` — ${detail}` : "";
        out(`    ${c.dim}→ ${scoreTag}${loc ? " " + loc : ""}${detailSuffix}${c.reset}\n`);
      }
      if (findings.length > 5) {
        out(`    ${c.dim}  ... and ${findings.length - 5} more${c.reset}\n`);
      }
    }
  }

  out(`\n  ${c.bold}Summary:${c.reset} ${result.summary || ""}\n`);
  out(`  ${c.bold}Recommendation:${c.reset} ${result.recommendation || ""}\n\n`);

  return buf;
}
