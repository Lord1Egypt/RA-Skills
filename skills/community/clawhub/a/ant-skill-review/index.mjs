#!/usr/bin/env node
import { setMaxListeners } from "node:events";
setMaxListeners(0);
import { openSync, writeFileSync, writeSync } from "node:fs";
import { Agent } from "@mariozechner/pi-agent-core";
import { parseArgs } from "./src/cli.mjs";
import {
  makeBashTool,
  makeDeepAnalysisTool,
} from "./src/tools.mjs";
import { loadConfig, getConfig, getModelConfig } from "./src/config.mjs";
import { getExplorePrompt } from "./src/prompts.mjs";
import { prescan } from "./src/prescan.mjs";
import {
  collectAgentText,
  attachToolLogger,
  attachStreamLogger,
  extractJson,
  printTextReport,
  getAssistantMessageDebug,
} from "./src/report.mjs";
import { computeScores } from "./src/scoring.mjs";

const { configFile, pre, lang, jsonOutput, outputFile, logFile, verbose, skillDir } = parseArgs();
loadConfig(configFile);

const logWriters = [];
if (verbose) logWriters.push((s) => process.stderr.write(s));
if (logFile) {
  const logFd = openSync(logFile, "w");
  logWriters.push((s) => writeSync(logFd, typeof s === "string" ? s : Buffer.from(s)));
}
const log = logWriters.length > 0
  ? (s) => { for (const w of logWriters) w(s); }
  : null;
const status = (s) => process.stderr.write(s);

function getLastAssistantMessage(agent) {
  const assistantMessages = agent.state.messages.filter((m) => m.role === "assistant");
  return assistantMessages[assistantMessages.length - 1];
}

function createAgent({ prompt, tools }) {
  const agent = new Agent({
    initialState: {
      systemPrompt: prompt,
      model: getModelConfig(),
      tools,
    },
    getApiKey: async () => getConfig().apiKey,
  });

  const getText = collectAgentText(agent);
  if (log) {
    attachToolLogger(agent, log);
    attachStreamLogger(agent, "agent", log);
  }

  return { agent, getText };
}

async function promptForJson({ agent, getText, promptText, label }) {
  await runPrompt(agent, promptText, label);

  const firstAttempt = tryExtractJson(agent, getText(), label);
  if (firstAttempt) return firstAttempt;

  if (log) log(`${label}: first response missing JSON, requesting strict JSON retry...\n`);

  await runPrompt(
    agent,
    "Your previous response did not contain valid JSON. Output ONLY the final JSON block now, with no extra text. Do not call any tools. Do not add explanation before or after the JSON.",
    label
  );

  const secondAttempt = tryExtractJson(agent, getText(), label);
  if (secondAttempt) return secondAttempt;

  status(`\nFailed to parse ${label} JSON.\n`);
  process.exit(1);
}

async function runPrompt(agent, promptText, label) {
  try {
    await agent.prompt(promptText);
  } catch (err) {
    status(`Agent error (${label}): ${err.message}\n`);
    process.exit(1);
  }

  const lastAssistant = getLastAssistantMessage(agent);
  if (lastAssistant?.stopReason === "error") {
    status(`Agent error (${label}): ${lastAssistant.errorMessage || "unknown assistant error"}\n`);
    if (log) {
      log(`${label} assistant debug:\n${JSON.stringify(getAssistantMessageDebug(lastAssistant), null, 2)}\n`);
    }
    process.exit(1);
  }
}

function tryExtractJson(agent, text, label) {
  try {
    return extractJson(text);
  } catch {
    if (log) {
      log(`Raw output:\n${text}\n`);
      log(`${label} assistant debug:\n${JSON.stringify(getAssistantMessageDebug(getLastAssistantMessage(agent)), null, 2)}\n`);
    }
    return null;
  }
}


status(`Scanning: ${skillDir}\n`);
status(`Mode: ${pre ? "prescan-only" : "standard"}\n`);
if (verbose) {
  status(`apiBase: ${getConfig().apiBase || ""}\n`);
  status(`apiModel: ${getConfig().model || ""}\n`);
}
status(`\n--- Pre-scan ---\n`);

let prescanResult = prescan(skillDir);

if (pre) {
  const out = prescanResult + "\n";
  if (outputFile) {
    writeFileSync(outputFile, out);
    status(`\nReport saved to ${outputFile}\n`);
  } else {
    process.stdout.write(out);
  }
  process.exit(0);
}

if (logFile) {
  log(`Config: ${JSON.stringify({
    apiBase: getConfig().apiBase,
    model: getConfig().model,
    npmRegistryUrl: getConfig().npmRegistryUrl,
    pypiIndexUrl: getConfig().pypiIndexUrl,
  }, null, 2)}\n`);
}
if (log) {
  log(prescanResult + "\n");
}

status(`--- Explore ---\n`);
const explore = createAgent({
  prompt: getExplorePrompt(lang),
  tools: [makeBashTool(skillDir), makeDeepAnalysisTool(skillDir)],
});
const result = await promptForJson({
  ...explore,
  promptText: `Explore the skill package. Flag all potential security risks by layer.\n\n# Pre-scan Results\n\n${prescanResult}`,
  label: "explore",
});
computeScores(result);



const content = jsonOutput
  ? JSON.stringify(result, null, 2) + "\n"
  : printTextReport(result, outputFile ? { color: false } : undefined);

if (outputFile) {
  writeFileSync(outputFile, content);
  status(`\nReport saved to ${outputFile}\n`);
  process.exit(0);
}

process.stdout.write(content, () => process.exit(0));
