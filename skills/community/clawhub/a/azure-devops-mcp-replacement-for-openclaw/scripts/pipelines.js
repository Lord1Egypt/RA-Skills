#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node pipelines.js list <project>
//   node pipelines.js runs <project> <pipeline-id> [limit]

"use strict";

const { request, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, project, pipelineId, limitArg] = process.argv;

function base(p) {
  return `https://dev.azure.com/${encodeURIComponent(ORG)}/${encodeURIComponent(p)}/_apis`;
}

async function main() {
  if (!project) { console.error("Usage: node pipelines.js <cmd> <project> [...]"); process.exit(1); }
  const p = validateSegment(project, "project");

  switch (cmd) {
    case "list": {
      const data = await request(`${base(p)}/pipelines?api-version=7.1`);
      const pipelines = (data.value || []).map((pl) => ({
        id: pl.id,
        name: pl.name,
        folder: pl.folder,
        revision: pl.revision,
        url: pl._links?.web?.href,
      }));
      output({ count: pipelines.length, pipelines });
      break;
    }
    case "runs": {
      if (!pipelineId || isNaN(Number(pipelineId))) {
        console.error("Usage: node pipelines.js runs <project> <pipeline-id> [limit]");
        process.exit(1);
      }
      const limit = Math.min(Number(limitArg) || 10, 50);
      const data = await request(`${base(p)}/pipelines/${Number(pipelineId)}/runs?api-version=7.1&$top=${limit}`);
      const runs = (data.value || []).map((r) => ({
        id: r.id,
        name: r.name,
        state: r.state,
        result: r.result,
        createdDate: r.createdDate,
        finishedDate: r.finishedDate,
        url: r._links?.web?.href,
      }));
      output({ count: runs.length, pipelineId: Number(pipelineId), runs });
      break;
    }
    default:
      console.error("Commands: list | runs");
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });
