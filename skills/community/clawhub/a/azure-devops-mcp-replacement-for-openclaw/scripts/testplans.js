#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node testplans.js list <project>
//   node testplans.js suites <project> <plan-id>

"use strict";

const { request, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, project, planId] = process.argv;

function base(p) {
  return `https://dev.azure.com/${encodeURIComponent(ORG)}/${encodeURIComponent(p)}/_apis/testplan`;
}

async function main() {
  if (!project) { console.error("Usage: node testplans.js <cmd> <project> [...]"); process.exit(1); }
  const p = validateSegment(project, "project");

  switch (cmd) {
    case "list": {
      const data = await request(`${base(p)}/plans?api-version=7.1`);
      const plans = (data.value || []).map((pl) => ({
        id: pl.id,
        name: pl.name,
        state: pl.state,
        startDate: pl.startDate,
        endDate: pl.endDate,
        owner: pl.owner?.displayName,
      }));
      output({ count: plans.length, testPlans: plans });
      break;
    }
    case "suites": {
      if (!planId || isNaN(Number(planId))) {
        console.error("Usage: node testplans.js suites <project> <plan-id>");
        process.exit(1);
      }
      const data = await request(`${base(p)}/Plans/${Number(planId)}/suites?api-version=7.1`);
      const suites = (data.value || []).map((s) => ({
        id: s.id,
        name: s.name,
        suiteType: s.suiteType,
        testCaseCount: s.testCaseCount,
        state: s.state,
      }));
      output({ count: suites.length, planId: Number(planId), testSuites: suites });
      break;
    }
    default:
      console.error("Commands: list | suites");
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });
