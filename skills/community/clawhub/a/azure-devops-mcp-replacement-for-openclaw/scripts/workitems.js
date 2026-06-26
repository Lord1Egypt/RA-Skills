#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node workitems.js list <project>
//   node workitems.js list <project> --team <team>
//   node workitems.js get <id>
//   node workitems.js current-sprint <project> <team>
//   node workitems.js sprint-items <project> <iterationId> [--team <team>]
//   node workitems.js create <project> <type> <title>
//   node workitems.js update <id> <field> <value>
//   node workitems.js query <project> "<WIQL>"
//   node workitems.js query <project> "<WIQL>" --team <team>

"use strict";

const { request, orgUrl, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, ...args] = process.argv;

// Parse --team <value> from an args array
function parseTeamFlag(arr) {
  const idx = arr.indexOf("--team");
  if (idx !== -1 && arr[idx + 1]) return arr[idx + 1];
  return null;
}

// Strip --team <value> from args array, return remaining positional args
function stripTeamFlag(arr) {
  const out = [];
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === "--team") { i++; continue; }
    out.push(arr[i]);
  }
  return out;
}

function formatWI(wi) {
  const f = wi.fields || {};
  return {
    id: wi.id,
    type: f["System.WorkItemType"],
    title: f["System.Title"],
    state: f["System.State"],
    assignedTo: f["System.AssignedTo"]?.displayName,
    priority: f["Microsoft.VSTS.Common.Priority"],
    iterationPath: f["System.IterationPath"],
    areaPath: f["System.AreaPath"],
    createdDate: f["System.CreatedDate"],
    changedDate: f["System.ChangedDate"],
    url: wi.url,
  };
}

async function fetchWorkItemDetails(ids) {
  if (!ids || ids.length === 0) return [];
  const idList = ids.slice(0, 200).join(",");
  const fields = [
    "System.Id", "System.Title", "System.WorkItemType", "System.State",
    "System.AssignedTo", "System.IterationPath", "System.AreaPath",
    "System.CreatedDate", "System.ChangedDate",
    "Microsoft.VSTS.Common.Priority",
  ].join(",");
  const url = orgUrl(`_apis/wit/workitems?ids=${idList}&fields=${fields}`);
  const data = await request(url);
  return (data.value || []).map(formatWI);
}

async function runWiql(wiql, project, team) {
  const p = validateSegment(project, "project");
  let url;
  if (team) {
    // Team-scoped WIQL: results respect team's area paths and iteration subscriptions
    const t = validateSegment(team, "team");
    url = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/${t}/_apis/wit/wiql?api-version=7.1&$top=100`;
  } else {
    url = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/_apis/wit/wiql?api-version=7.1&$top=100`;
  }
  const result = await request(url, "POST", { query: wiql });
  const ids = (result.workItems || []).map((w) => w.id);
  return fetchWorkItemDetails(ids);
}

async function main() {
  switch (cmd) {

    // ── List work items ──────────────────────────────────────────────────────
    // Without --team: all items in project ordered by last changed
    // With    --team: items scoped to that team's area paths
    case "list": {
      const team = parseTeamFlag(args);
      const [project] = stripTeamFlag(args);
      if (!project) { console.error("Usage: node workitems.js list <project> [--team <team>]"); process.exit(1); }
      const wiql = `SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '${project.replace(/'/g, "''")}' ORDER BY [System.ChangedDate] DESC`;
      const items = await runWiql(wiql, project, team);
      output({ count: items.length, project, team: team ?? null, workItems: items });
      break;
    }

    // ── Get a single work item by ID ─────────────────────────────────────────
    case "get": {
      const [id] = args;
      if (!id || isNaN(Number(id))) { console.error("Usage: node workitems.js get <numeric-id>"); process.exit(1); }
      const url = orgUrl(`_apis/wit/workitems/${Number(id)}`);
      const wi = await request(url);
      output(formatWI(wi));
      break;
    }

    // ── Work items in the current/active sprint for a team ───────────────────
    // Step 1: resolve current iteration via teamsettings/iterations?$timeframe=current
    // Step 2: fetch work item relations for that iteration
    // Endpoint: GET /{org}/{project}/{team}/_apis/work/teamsettings/iterations/{id}/workitems
    // PAT scope: vso.work
    case "current-sprint": {
      const team = parseTeamFlag(args);
      const [project, positionalTeam] = stripTeamFlag(args);
      const resolvedTeam = team ?? positionalTeam; // support both --team flag and positional
      if (!project || !resolvedTeam) {
        console.error("Usage: node workitems.js current-sprint <project> <team>\n       node workitems.js current-sprint <project> --team <team>");
        process.exit(1);
      }
      const p = validateSegment(project, "project");
      const t = validateSegment(resolvedTeam, "team");

      // Get current iteration
      const iterUrl = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations?$timeframe=current&api-version=7.1`;
      const iterData = await request(iterUrl);
      const iter = (iterData.value || [])[0];
      if (!iter) { output({ message: "No active sprint found for this team", project, team: resolvedTeam }); break; }

      // Get work item relations for that iteration
      const wiUrl = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations/${iter.id}/workitems?api-version=7.1`;
      const wiData = await request(wiUrl);
      const ids = (wiData.workItemRelations || []).map((r) => r.target?.id).filter(Boolean);
      const items = await fetchWorkItemDetails(ids);
      output({
        project,
        team: resolvedTeam,
        sprint: { id: iter.id, name: iter.name, startDate: iter.attributes?.startDate, finishDate: iter.attributes?.finishDate },
        count: items.length,
        workItems: items,
      });
      break;
    }

    // ── Work items in a specific sprint by iteration ID ──────────────────────
    // Useful when you already have the iteration ID from teams.js sprints
    // Without --team: fetches using project-level endpoint
    // With    --team: fetches using team-scoped endpoint (respects team board)
    case "sprint-items": {
      const team = parseTeamFlag(args);
      const positionals = stripTeamFlag(args);
      const [project, iterationId] = positionals;
      if (!project || !iterationId) {
        console.error("Usage: node workitems.js sprint-items <project> <iterationId> [--team <team>]");
        process.exit(1);
      }
      const p = validateSegment(project, "project");
      // iterationId is a GUID — validate format only
      if (!/^[0-9a-f-]{36}$/i.test(iterationId)) {
        console.error("❌ iterationId must be a valid GUID (e.g. a589a806-bf11-4d4f-a031-c19813331553)");
        process.exit(1);
      }

      let wiUrl;
      if (team) {
        const t = validateSegment(team, "team");
        wiUrl = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations/${iterationId}/workitems?api-version=7.1`;
      } else {
        // Project-level: use WIQL filtering by iteration path
        // First resolve iteration path from ID
        const iterInfoUrl = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/_apis/wit/classificationnodes/iterations?$depth=5&api-version=7.1`;
        const treeData = await request(iterInfoUrl);
        function findById(node, id) {
          if (!node) return null;
          if (node.id === id) return node;
          for (const child of (node.children || [])) {
            const found = findById(child, id);
            if (found) return found;
          }
          return null;
        }
        const iterNode = findById(treeData, iterationId);
        if (!iterNode) { output({ message: `Iteration ${iterationId} not found in project`, project }); break; }
        const iterPath = iterNode.path.replace(/^.*?\\/, `${project}\\`); // normalize path
        const wiql = `SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '${project.replace(/'/g, "''")}' AND [System.IterationPath] = '${iterPath.replace(/'/g, "''")}'`;
        const items = await runWiql(wiql, project, null);
        output({ project, team: null, iterationPath: iterPath, count: items.length, workItems: items });
        break;
      }

      const wiData = await request(wiUrl);
      const ids = (wiData.workItemRelations || []).map((r) => r.target?.id).filter(Boolean);
      const items = await fetchWorkItemDetails(ids);
      output({ project, team: team ?? null, iterationId, count: items.length, workItems: items });
      break;
    }

    // ── Create a work item ───────────────────────────────────────────────────
    case "create": {
      const [project, type, ...titleParts] = args;
      const title = titleParts.join(" ");
      if (!project || !type || !title) { console.error("Usage: node workitems.js create <project> <type> <title>"); process.exit(1); }
      const p = validateSegment(project, "project");
      const safeType = validateSegment(type, "work item type");
      const url = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/_apis/wit/workitems/$${safeType}?api-version=7.1`;
      const body = [{ op: "add", path: "/fields/System.Title", value: title }];
      const wi = await request(url, "POST", body);
      output(formatWI(wi));
      break;
    }

    // ── Update a work item field ─────────────────────────────────────────────
    case "update": {
      const [id, field, ...valueParts] = args;
      const value = valueParts.join(" ");
      if (!id || isNaN(Number(id)) || !field || !value) {
        console.error("Usage: node workitems.js update <id> <field> <value>\n  e.g. System.State, System.AssignedTo, Microsoft.VSTS.Common.Priority");
        process.exit(1);
      }
      const url = orgUrl(`_apis/wit/workitems/${Number(id)}`);
      const body = [{ op: "add", path: `/fields/${field}`, value }];
      const wi = await request(url, "PATCH", body);
      output(formatWI(wi));
      break;
    }

    // ── Raw WIQL query ───────────────────────────────────────────────────────
    // Without --team: project-scoped query
    // With    --team: team-scoped query (respects team's area paths)
    case "query": {
      const team = parseTeamFlag(args);
      const positionals = stripTeamFlag(args);
      const [project, ...queryParts] = positionals;
      const wiql = queryParts.join(" ");
      if (!project || !wiql) { console.error('Usage: node workitems.js query <project> "<WIQL>" [--team <team>]'); process.exit(1); }
      const items = await runWiql(wiql, project, team);
      output({ count: items.length, project, team: team ?? null, workItems: items });
      break;
    }

    default:
      console.error(
        "Commands:\n" +
        "  list <project> [--team <team>]                     — list work items\n" +
        "  get <id>                                           — get work item by ID\n" +
        "  current-sprint <project> <team>                    — active sprint items for a team\n" +
        "  sprint-items <project> <iterationId> [--team <t>]  — items in a specific sprint\n" +
        "  create <project> <type> <title>                    — create a work item\n" +
        "  update <id> <field> <value>                        — update a field\n" +
        "  query <project> \"<WIQL>\" [--team <team>]           — run WIQL query"
      );
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });
