"use strict";

const { spawnSync } = require("child_process");
const { requireConfig } = require("./config");
const { ask } = require("./prompt");
const { listen } = require("./stt");
const { speak } = require("./speak");
const { spentSinceUsd } = require("./spend");

function runAgent(agentCommand, text) {
  const result = spawnSync("/bin/sh", ["-c", agentCommand], {
    input: text,
    encoding: "utf8",
    timeout: 180000,
    maxBuffer: 10 * 1024 * 1024,
  });
  if (result.status !== 0) {
    const stderr = (result.stderr || "").trim().slice(0, 300);
    console.error(`Agent command failed (exit ${result.status})${stderr ? `: ${stderr}` : ""}`);
    return null;
  }
  return (result.stdout || "").trim();
}

async function talk({ agent, approve, model } = {}) {
  const config = requireConfig();
  const agentCommand = agent || config.conversation?.agentCommand;
  if (!agentCommand) {
    console.error("No agent command configured. Your agent reads your words on stdin and prints its reply.");
    console.error('Set it in ~/.x402-agent-voice/config.json, e.g. "conversation": { "agentCommand": "claude -p" }');
    console.error('or pass it once: x402-agent-voice talk --agent "claude -p"');
    process.exit(1);
  }

  const whisperModel = model || config.conversation?.whisperModel || "base";
  const sessionStart = new Date().toISOString();
  const sessionCap = parseFloat(config.x402Policy?.sessionCapUsd || "0");
  let capWarned = false;

  console.log("Conversation mode — push-to-talk. (Wake word and always-on listening: coming soon.)");
  console.log(`Agent: ${agentCommand}`);

  for (;;) {
    const typed = await ask("\n⏎ to talk · or type a message · 'exit' to quit\n> ");
    if (typed === null || ["exit", "quit", "q"].includes(typed.toLowerCase())) break;

    let text = typed;
    if (!text) {
      try {
        const heard = await listen({ model: whisperModel });
        text = (heard.text || "").trim();
        if (text) console.log(`You: ${text}`);
      } catch (err) {
        console.error(`Could not hear you: ${err.message}`);
        continue;
      }
    }
    if (!text) {
      console.log("(heard nothing — try again)");
      continue;
    }

    const reply = runAgent(agentCommand, text);
    if (!reply) {
      console.log("(agent returned nothing)");
      continue;
    }
    console.log(`Agent: ${reply}`);

    const sessionSpent = spentSinceUsd(sessionStart);
    const overSessionCap = sessionCap > 0 && sessionSpent >= sessionCap;
    if (overSessionCap && !capWarned) {
      console.log(`Session spend cap reached ($${sessionSpent.toFixed(4)} >= $${sessionCap}) — hosted voice disabled for this session.`);
      capWarned = true;
    }
    await speak(reply, { approve, soft: true, noHosted: overSessionCap });
  }

  console.log("Conversation ended.");
}

module.exports = { talk };
