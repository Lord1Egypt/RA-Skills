#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node projects.js list
//   node projects.js get <project>

"use strict";

const { request, orgUrl, validateSegment, output } = require("./client.js");

const [, , cmd, project] = process.argv;

async function main() {
  switch (cmd) {
    case "list": {
      const data = await request(orgUrl("_apis/projects"));
      const projects = (data.value || []).map((p) => ({
        id: p.id,
        name: p.name,
        state: p.state,
        visibility: p.visibility,
        lastUpdateTime: p.lastUpdateTime,
      }));
      output({ count: projects.length, projects });
      break;
    }
    case "get": {
      if (!project) { console.error("Usage: node projects.js get <project>"); process.exit(1); }
      const p = validateSegment(project, "project");
      const data = await request(orgUrl(`_apis/projects/${p}`));
      output({
        id: data.id,
        name: data.name,
        description: data.description,
        state: data.state,
        visibility: data.visibility,
        url: data.url,
      });
      break;
    }
    default:
      console.error("Commands: list | get <project>");
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });
