#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: team-config.json (same directory, no user input used in path)
//   Local files written: none
//
// Usage:
//   node people.js setup                                      — print config file location to edit
//   node people.js me <project> <team>                        — my items in active sprint
//   node people.js member <email> <project> <team>            — one member's items in active sprint
//   node people.js standup <project> <team>                   — full standup: everyone's items
//   node people.js capacity <project> <team>                  — capacity vs assigned workload per person
//   node people.js overloaded <project> <team>                — who has more work than capacity

"use strict";

const path = require("path");
const fs   = require("fs");
const { request, validateSegment, output, ORG } = require("./client.js");

// ── Load team config ─────────────────────────────────────────────────────────
const CONFIG_PATH = path.join(__dirname, "..", "team-config.json");

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error(`❌ team-config.json not found at: ${CONFIG_PATH}`);
    console.error("   Run: node people.js setup");
    process.exit(1);
  }
  try {
    const raw = fs.readFileSync(CONFIG_PATH, "utf8");
    return JSON.parse(raw);
  } catch (e) {
    console.error(`❌ Failed to parse team-config.json: ${e.message}`);
    process.exit(1);
  }
}

function allMembers(config) {
  // Returns [me, ...team] as a flat list
  return [config.me, ...(config.team || [])];
}

function findMemberByEmail(config, email) {
  return allMembers(config).find(
    (m) => m.email.toLowerCase() === email.toLowerCase()
  );
}

// ── ADO API helpers ──────────────────────────────────────────────────────────

function encSeg(val) {
  // Already encoded by validateSegment caller — used for raw values
  return encodeURIComponent(val);
}

async function getCurrentIteration(project, team) {
  const p = validateSegment(project, "project");
  const t = validateSegment(team, "team");
  const url = `https://dev.azure.com/${encSeg(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations?$timeframe=current&api-version=7.1`;
  const data = await request(url);
  return (data.value || [])[0] ?? null;
}

async function getSprintWorkItems(project, team, iterationId) {
  const p = validateSegment(project, "project");
  const t = validateSegment(team, "team");
  const url = `https://dev.azure.com/${encSeg(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations/${iterationId}/workitems?api-version=7.1`;
  const data = await request(url);
  return (data.workItemRelations || []).map((r) => r.target?.id).filter(Boolean);
}

async function fetchWorkItemDetails(ids) {
  if (!ids || ids.length === 0) return [];
  const idList = ids.slice(0, 200).join(",");
  const fields = [
    "System.Id",
    "System.Title",
    "System.WorkItemType",
    "System.State",
    "System.AssignedTo",
    "System.IterationPath",
    "System.AreaPath",
    "Microsoft.VSTS.Common.Priority",
    "Microsoft.VSTS.Scheduling.RemainingWork",
    "Microsoft.VSTS.Scheduling.OriginalEstimate",
    "Microsoft.VSTS.Scheduling.CompletedWork",
  ].join(",");
  const url = `https://dev.azure.com/${encSeg(ORG)}/_apis/wit/workitems?ids=${idList}&fields=${fields}&api-version=7.1`;
  const data = await request(url);
  return (data.value || []).map((wi) => {
    const f = wi.fields || {};
    return {
      id: wi.id,
      type: f["System.WorkItemType"],
      title: f["System.Title"],
      state: f["System.State"],
      assignedTo: f["System.AssignedTo"]?.displayName ?? null,
      assignedToEmail: f["System.AssignedTo"]?.uniqueName ?? null,
      priority: f["Microsoft.VSTS.Common.Priority"] ?? null,
      remainingWork: f["Microsoft.VSTS.Scheduling.RemainingWork"] ?? null,
      originalEstimate: f["Microsoft.VSTS.Scheduling.OriginalEstimate"] ?? null,
      completedWork: f["Microsoft.VSTS.Scheduling.CompletedWork"] ?? null,
      iterationPath: f["System.IterationPath"],
      url: `https://dev.azure.com/${ORG}/_workitems/edit/${wi.id}`,
    };
  });
}

// ── Build per-person summaries ───────────────────────────────────────────────

function groupByMember(items, members) {
  // Build a map: email (lowercase) → member profile + items
  const map = new Map();
  for (const m of members) {
    map.set(m.email.toLowerCase(), {
      name: m.name,
      email: m.email,
      capacityPerDay: m.capacityPerDay ?? null,
      items: [],
    });
  }

  // Also collect items assigned to people NOT in config (unrecognised assignees)
  const unknown = new Map();

  for (const item of items) {
    const emailKey = (item.assignedToEmail ?? "").toLowerCase();
    if (map.has(emailKey)) {
      map.get(emailKey).items.push(item);
    } else if (emailKey) {
      if (!unknown.has(emailKey)) {
        unknown.set(emailKey, { name: item.assignedTo, email: item.assignedToEmail, items: [] });
      }
      unknown.get(emailKey).items.push(item);
    }
  }

  return { known: [...map.values()], unknown: [...unknown.values()] };
}

function summariseMember(member, sprintDays) {
  const items = member.items;
  const done  = items.filter((i) => ["Done", "Closed", "Resolved", "Completed"].includes(i.state));
  const inProg = items.filter((i) => ["Active", "In Progress", "Testing in Progress", "Committed"].includes(i.state));
  const notStarted = items.filter((i) => ["New", "To Do", "Proposed"].includes(i.state));

  const totalRemaining = items.reduce((s, i) => s + (i.remainingWork ?? 0), 0);
  const totalEstimate  = items.reduce((s, i) => s + (i.originalEstimate ?? 0), 0);
  const totalCompleted = items.reduce((s, i) => s + (i.completedWork ?? 0), 0);

  const capacityHours = member.capacityPerDay != null && sprintDays != null
    ? Math.round(member.capacityPerDay * sprintDays * 10) / 10
    : null;

  const utilisation = capacityHours && totalEstimate
    ? Math.round((totalEstimate / capacityHours) * 100)
    : null;

  return {
    name: member.name,
    email: member.email,
    capacityPerDay: member.capacityPerDay,
    capacityHoursTotal: capacityHours,
    totalItems: items.length,
    doneCount: done.length,
    inProgressCount: inProg.length,
    notStartedCount: notStarted.length,
    totalEstimateHours: totalEstimate || null,
    totalRemainingHours: totalRemaining || null,
    totalCompletedHours: totalCompleted || null,
    utilisationPct: utilisation,
    items: items.map((i) => ({
      id: i.id,
      type: i.type,
      title: i.title,
      state: i.state,
      priority: i.priority,
      remainingWork: i.remainingWork,
      originalEstimate: i.originalEstimate,
      url: i.url,
    })),
  };
}

function sprintWorkDays(iter) {
  if (!iter?.attributes?.startDate || !iter?.attributes?.finishDate) return null;
  const start = new Date(iter.attributes.startDate);
  const end   = new Date(iter.attributes.finishDate);
  let days = 0;
  const cur = new Date(start);
  while (cur <= end) {
    const dow = cur.getDay();
    if (dow !== 0 && dow !== 6) days++;
    cur.setDate(cur.getDate() + 1);
  }
  return days;
}

// ── Command handlers ─────────────────────────────────────────────────────────

async function resolveSprintContext(project, team) {
  const iter = await getCurrentIteration(project, team);
  if (!iter) {
    output({ error: "No active sprint found for this team. Check sprint dates in ADO.", project, team });
    process.exit(0);
  }
  const ids   = await getSprintWorkItems(project, team, iter.id);
  const items = await fetchWorkItemDetails(ids);
  const days  = sprintWorkDays(iter);
  return { iter, items, days };
}

async function cmdMe(project, team) {
  const config = loadConfig();
  const me = config.me;
  if (!me?.email || me.email === "you@company.com") {
    console.error("❌ Please edit team-config.json and set your name and email under \"me\".");
    process.exit(1);
  }

  const { iter, items, days } = await resolveSprintContext(project, team);
  const myItems = items.filter(
    (i) => (i.assignedToEmail ?? "").toLowerCase() === me.email.toLowerCase()
  );
  const summary = summariseMember({ ...me, items: myItems }, days);

  output({
    sprint: { name: iter.name, startDate: iter.attributes?.startDate, finishDate: iter.attributes?.finishDate, workDays: days },
    me: summary,
  });
}

async function cmdMember(email, project, team) {
  const config = loadConfig();
  const member = findMemberByEmail(config, email);
  if (!member) {
    console.error(`❌ Email "${email}" not found in team-config.json. Add them under "team" and retry.`);
    process.exit(1);
  }

  const { iter, items, days } = await resolveSprintContext(project, team);
  const memberItems = items.filter(
    (i) => (i.assignedToEmail ?? "").toLowerCase() === email.toLowerCase()
  );
  const summary = summariseMember({ ...member, items: memberItems }, days);

  output({
    sprint: { name: iter.name, startDate: iter.attributes?.startDate, finishDate: iter.attributes?.finishDate, workDays: days },
    member: summary,
  });
}

async function cmdStandup(project, team) {
  const config = loadConfig();
  const members = allMembers(config);

  const { iter, items, days } = await resolveSprintContext(project, team);
  const { known, unknown } = groupByMember(items, members);

  const summaries = known.map((m) => summariseMember(m, days));

  // Sprint totals
  const totalItems     = items.length;
  const totalDone      = items.filter((i) => ["Done", "Closed", "Resolved", "Completed"].includes(i.state)).length;
  const totalRemaining = items.reduce((s, i) => s + (i.remainingWork ?? 0), 0);

  output({
    sprint: {
      name: iter.name,
      startDate: iter.attributes?.startDate,
      finishDate: iter.attributes?.finishDate,
      workDays: days,
      totalItems,
      totalDone,
      totalRemainingHours: totalRemaining || null,
      completionPct: totalItems ? Math.round((totalDone / totalItems) * 100) : 0,
    },
    team: summaries,
    unrecognisedAssignees: unknown.map((u) => ({
      name: u.name,
      email: u.email,
      itemCount: u.items.length,
      note: "Not in team-config.json — add them to track their capacity",
    })),
  });
}

async function cmdCapacity(project, team) {
  const config = loadConfig();
  const members = allMembers(config);

  const { iter, items, days } = await resolveSprintContext(project, team);
  const { known } = groupByMember(items, members);

  const rows = known.map((m) => {
    const s = summariseMember(m, days);
    return {
      name: s.name,
      email: s.email,
      capacityHoursTotal: s.capacityHoursTotal,
      estimatedHours: s.totalEstimateHours,
      remainingHours: s.totalRemainingHours,
      completedHours: s.totalCompletedHours,
      utilisationPct: s.utilisationPct,
      totalItems: s.totalItems,
      doneItems: s.doneCount,
      status: s.utilisationPct == null
        ? "no-estimate-data"
        : s.utilisationPct > 110 ? "⚠️  overloaded"
        : s.utilisationPct > 90  ? "✅ fully loaded"
        : s.utilisationPct > 50  ? "🟡 moderate"
        : "🔵 light load",
    };
  });

  output({
    sprint: { name: iter.name, workDays: days },
    capacity: rows,
  });
}

async function cmdOverloaded(project, team) {
  const config  = loadConfig();
  const members = allMembers(config);

  const { iter, items, days } = await resolveSprintContext(project, team);
  const { known } = groupByMember(items, members);

  const overloaded = known
    .map((m) => summariseMember(m, days))
    .filter((s) => s.utilisationPct != null && s.utilisationPct > 100)
    .map((s) => ({
      name: s.name,
      email: s.email,
      capacityHoursTotal: s.capacityHoursTotal,
      estimatedHours: s.totalEstimateHours,
      overByHours: s.totalEstimateHours != null && s.capacityHoursTotal != null
        ? Math.round((s.totalEstimateHours - s.capacityHoursTotal) * 10) / 10
        : null,
      utilisationPct: s.utilisationPct,
      items: s.items,
    }));

  if (overloaded.length === 0) {
    output({ sprint: iter.name, message: "✅ No team members are overloaded this sprint." });
  } else {
    output({ sprint: iter.name, overloadedCount: overloaded.length, overloaded });
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

const [, , cmd, ...args] = process.argv;

async function main() {
  switch (cmd) {

    case "setup": {
      console.log(`\n📝 Team config file location:\n   ${CONFIG_PATH}\n`);
      console.log("Edit that file to set your name, email, and team members.");
      console.log("Each person needs an 'email' that matches exactly what Azure DevOps shows");
      console.log("in the 'Assigned To' field on work items (usually firstname.lastname@company.com).\n");
      if (fs.existsSync(CONFIG_PATH)) {
        console.log("Current config:");
        console.log(fs.readFileSync(CONFIG_PATH, "utf8"));
      }
      break;
    }

    case "me": {
      const [project, team] = args;
      if (!project || !team) { console.error("Usage: node people.js me <project> <team>"); process.exit(1); }
      await cmdMe(project, team);
      break;
    }

    case "member": {
      const [email, project, team] = args;
      if (!email || !project || !team) { console.error("Usage: node people.js member <email> <project> <team>"); process.exit(1); }
      await cmdMember(email, project, team);
      break;
    }

    case "standup": {
      const [project, team] = args;
      if (!project || !team) { console.error("Usage: node people.js standup <project> <team>"); process.exit(1); }
      await cmdStandup(project, team);
      break;
    }

    case "capacity": {
      const [project, team] = args;
      if (!project || !team) { console.error("Usage: node people.js capacity <project> <team>"); process.exit(1); }
      await cmdCapacity(project, team);
      break;
    }

    case "overloaded": {
      const [project, team] = args;
      if (!project || !team) { console.error("Usage: node people.js overloaded <project> <team>"); process.exit(1); }
      await cmdOverloaded(project, team);
      break;
    }

    default:
      console.error(
        "Commands:\n" +
        "  setup                              — show config file location\n" +
        "  me <project> <team>                — my items in current sprint\n" +
        "  member <email> <project> <team>    — one member's items in current sprint\n" +
        "  standup <project> <team>           — everyone's items for standup\n" +
        "  capacity <project> <team>          — capacity vs workload per person\n" +
        "  overloaded <project> <team>        — who has more work than capacity"
      );
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });
