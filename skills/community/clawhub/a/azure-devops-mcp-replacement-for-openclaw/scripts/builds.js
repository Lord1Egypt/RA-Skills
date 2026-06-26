#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node builds.js list <project> [limit]
//   node builds.js get <project> <build-id>

"use strict";

const { request, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, project, second, third] = process.argv;

function base(p) {
  return `https://dev.azure.com/${encodeURIComponent(ORG)}/${encodeURIComponent(p)}/_apis`;
}

function formatBuild(b) {
  return {
    id: b.id,
    buildNumber: b.buildNumber,
    status: b.status,
    result: b.result,
    definition: b.definition?.name,
    sourceBranch: b.sourceBranch,
    requestedBy: b.requestedBy?.displayName,
    queueTime: b.queueTime,
    startTime: b.startTime,
    finishTime: b.finishTime,
    url: b._links?.web?.href,
  };
}

async function main() {
  if (!project) { console.error("Usage: node builds.js <cmd> <project> [...]"); process.exit(1); }
  const p = validateSegment(project, "project");

  switch (cmd) {
    case "list": {
      const limit = Math.min(Number(second) || 20, 100);
      const data = await request(`${base(p)}/build/builds?api-version=7.1&$top=${limit}`);
      const builds = (data.value || []).map(formatBuild);
      output({ count: builds.length, builds });
      break;
    }
    case "get": {
      if (!second || isNaN(Number(second))) {
        console.error("Usage: node builds.js get <project> <build-id>");
        process.exit(1);
      }
      const data = await request(`${base(p)}/build/builds/${Number(second)}?api-version=7.1`);
      output(formatBuild(data));
      break;
    }
    default:
      console.error("Commands: list | get");
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });
