#!/usr/bin/env node
// Calls one ATSPrep MCP tool over plain HTTPS (JSON-RPC 2.0, MCP streamable HTTP).
// No dependencies; needs Node 18+. Nothing is stored by ATSPrep.
//
//   node atsprep.mjs list
//   node atsprep.mjs <tool> [key=value] [key=@file.txt] [--json '{"key":"value"}']
//
// key=@file reads the value from a file (good for resume text). Values that look like
// numbers or true/false are sent as such. Set ATSPREP_MCP_URL to use another endpoint.
import { readFileSync } from "node:fs";

const URL_ = process.env.ATSPREP_MCP_URL || "https://atsprep.com/mcp";
const [, , tool, ...rest] = process.argv;

if (!tool || tool === "-h" || tool === "--help") {
  console.log("usage: node atsprep.mjs list | <tool> [key=value] [key=@file] [--json '{...}']");
  process.exit(tool ? 0 : 1);
}

function parseValue(raw) {
  if (raw.startsWith("@")) return readFileSync(raw.slice(1), "utf8");
  if (raw === "true" || raw === "false") return raw === "true";
  if (/^-?\d+$/.test(raw)) return Number(raw);
  return raw;
}

const args = {};
for (let i = 0; i < rest.length; i += 1) {
  const part = rest[i];
  if (part === "--json") {
    Object.assign(args, JSON.parse(rest[++i] ?? "{}"));
    continue;
  }
  const eq = part.indexOf("=");
  if (eq < 1) {
    console.error(`Expected key=value, got "${part}"`);
    process.exit(1);
  }
  args[part.slice(0, eq)] = parseValue(part.slice(eq + 1));
}

async function rpc(method, params) {
  const res = await fetch(URL_, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      accept: "application/json, text/event-stream",
      "user-agent": "atsprep-skills/1.0",
    },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`ATSPrep answered ${res.status}: ${text.slice(0, 300)}`);
  // The server may answer as JSON or as a single server-sent event.
  const json = text.trim().startsWith("{") ? text : text.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5)).join("");
  const body = JSON.parse(json);
  if (body.error) throw new Error(body.error.message || JSON.stringify(body.error));
  return body.result;
}

try {
  if (tool === "list") {
    const { tools } = await rpc("tools/list", {});
    for (const t of tools) console.log(`${t.name}\t${t.annotations?.title ?? ""}`);
  } else {
    const result = await rpc("tools/call", { name: tool, arguments: args });
    const out = result.structuredContent ?? result.content?.map((c) => c.text).join("\n");
    console.log(typeof out === "string" ? out : JSON.stringify(out, null, 2));
    if (result.isError) process.exit(2);
  }
} catch (error) {
  console.error(String(error.message || error));
  process.exit(1);
}
