#!/usr/bin/env node

import { execSync } from "node:child_process";
import { existsSync } from "node:fs";
import { appendFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

const globalRoot = execSync("npm root -g", { encoding: "utf8" }).trim();
const sdkPath = join(globalRoot, "@anthropic-ai/claude-agent-sdk", "sdk.mjs");
if (!existsSync(sdkPath)) {
  console.error(
    "Claude Code execution failed: global @anthropic-ai/claude-agent-sdk not found at " +
      sdkPath +
      ". Install with: npm install -g @anthropic-ai/claude-agent-sdk",
  );
  process.exit(1);
}
const { query } = await import(pathToFileURL(sdkPath).href);

/** @param {object} msg */
async function appendAssistantTextToLog(msg, logFile) {
  const content = msg.message?.content;
  if (!Array.isArray(content)) return;
  for (const block of content) {
    if (
      block &&
      typeof block === "object" &&
      "type" in block &&
      block.type === "text" &&
      "text" in block &&
      typeof block.text === "string"
    ) {
      await appendFile(logFile, block.text + "\n\n");
    }
  }
}

async function main() {
  let values;
  try {
    ({ values } = parseArgs({
      args: process.argv.slice(2),
      options: {
        query: { type: "string" },
        cwd: { type: "string" },
        resume: { type: "string" },
        "log-file": { type: "string" },
        "append-system-prompt": { type: "string" },
      },
      allowPositionals: false,
      strict: true,
    }));
  } catch {
    console.error(
      "Usage: run_claude --query QUERY [--cwd CWD] [--resume RESUME] [--log-file PATH] [--append-system-prompt TEXT]",
    );
    process.exit(2);
  }

  const prompt = values.query;
  if (!prompt) {
    console.error("error: the following arguments are required: --query");
    process.exit(2);
  }

  const cwd = values.cwd;
  const resume = values.resume;
  const logFile = values["log-file"];
  const appendSystemPrompt = values["append-system-prompt"];

  /** @type {string | undefined} */
  let res;

  try {
    const options = {
      ...(cwd !== undefined ? { cwd } : {}),
      ...(appendSystemPrompt !== undefined
        ? { systemPrompt: appendSystemPrompt }
        : {}),
      settingSources: /** @type {const} */ (["user", "project"]),
      ...(resume !== undefined ? { resume } : {}),
      allowedTools: [
        "Read",
        "Edit",
        "Bash",
        "Write",
        "Glob",
        "Grep",
        "Skill",
      ],
    };

    for await (const message of query({ prompt, options })) {
      if (message.type === "system" && message.subtype === "init") {
        if (logFile) {
          const sessionId = message.session_id;
          await writeFile(logFile, `Session ID: ${sessionId}\n\n`);
        }
      } else if (message.type === "result") {
        if (message.subtype === "success") {
          res =
            message.result +
            "\nResume this session with id: " +
            message.session_id;
        } else {
          res =
            message.errors.join("\n") +
            "\nResume this session with id: " +
            message.session_id;
        }
      } else if (message.type === "assistant") {
        if (!logFile) continue;
        await appendAssistantTextToLog(message, logFile);
      }
    }
    console.log(res === undefined ? "None" : res);
  } catch (e) {
    console.log("Claude Code execution failed: " + String(e));
  }
}

await main();
