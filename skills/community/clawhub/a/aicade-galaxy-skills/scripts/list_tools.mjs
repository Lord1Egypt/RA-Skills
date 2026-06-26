#!/usr/bin/env node

import { readFile } from "node:fs/promises";

async function main() {
  try {
    const args = parseCliArgs(process.argv.slice(2));
    const artifactPath =
      args.get("--artifact") ?? "output/aicade-galaxy-skill.json";
    const artifact = JSON.parse(await readFile(artifactPath, "utf8"));

    if (!artifact || typeof artifact !== "object" || !Array.isArray(artifact.tools)) {
      throw new Error("Invalid artifact format.");
    }

    const summary = {
      baseUrl: artifact.baseUrl,
      toolCount: artifact.toolCount,
      tools: artifact.tools.map((tool) => ({
        name: tool.name,
        title: tool.metadata?.title ?? "",
        method: tool.metadata?.method ?? "",
        path: tool.metadata?.path ?? "",
        required: Array.isArray(tool.inputSchema?.required)
          ? tool.inputSchema.required
          : [],
        responseFields: Array.isArray(tool.metadata?.responseFields)
          ? tool.metadata.responseFields
          : [],
      })),
    };

    console.log(JSON.stringify(summary, null, 2));
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}

function parseCliArgs(argv) {
  const result = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || value === undefined) {
      throw new Error(
        "Usage: node scripts/list_tools.mjs --artifact <path>",
      );
    }
    result.set(key, value);
  }
  return result;
}

await main();
