#!/usr/bin/env node
/**
 * 仅解析用户意图（不拉数）。
 * 用法：echo '{"userMessage":"...","userId":"..."}' | node parse-user-intent.mjs
 */
import { resolveUserIntent } from "./resolve-user-intent.mjs";
import { resolveOpenClawIdentity } from "./resolve-openclaw-identity.mjs";

async function readBody() {
  if (process.stdin.isTTY) return null;
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  const text = Buffer.concat(chunks).toString("utf8").trim();
  return text ? JSON.parse(text) : null;
}

const body = await readBody();
const intent = resolveUserIntent(body);
const identity = resolveOpenClawIdentity(body);

console.log(
  JSON.stringify({
    ok: !intent.needClarification,
    needClarification: intent.needClarification,
    identity,
    userMessage: intent.userMessage,
    timeRange: intent.timeRange,
    analysisFocus: intent.analysisFocus,
    outputFormat: intent.outputFormat,
    clarification: intent.clarification,
    plan: intent.reportPlan,
  }),
);
