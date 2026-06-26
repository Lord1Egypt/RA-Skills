#!/usr/bin/env node
const { createClient } = require('./ado-client');
const { loadConfig } = require('./config');
const { validateFields, validatePathPart, requireNonEmpty } = require('./validators');
const { parseArgs } = require('./utils');

function isoDateDaysAgo(days) {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().slice(0, 10);
}

function escapeWiqlString(value) {
  return String(value).replace(/'/g, "''");
}

function assignedToParts(value) {
  if (!value) return { assignedTo: '', assignedToEmail: '' };
  if (typeof value === 'string') return { assignedTo: value, assignedToEmail: '' };
  return {
    assignedTo: value.displayName || value.name || '',
    assignedToEmail: value.uniqueName || value.mailAddress || '',
  };
}

function normalizeWorkItem(item) {
  const fields = item.fields || {};
  const assigned = assignedToParts(fields['System.AssignedTo']);
  return {
    id: item.id,
    title: fields['System.Title'] || '',
    state: fields['System.State'] || '',
    type: fields['System.WorkItemType'] || '',
    assignedTo: assigned.assignedTo,
    assignedToEmail: assigned.assignedToEmail,
    project: fields['System.TeamProject'] || '',
    iterationPath: fields['System.IterationPath'] || '',
    areaPath: fields['System.AreaPath'] || '',
    priority: fields['Microsoft.VSTS.Common.Priority'] ?? '',
    createdDate: fields['System.CreatedDate'] || '',
    changedDate: fields['System.ChangedDate'] || '',
    closedDate: fields['Microsoft.VSTS.Common.ClosedDate'] || '',
    originalEstimate: fields['Microsoft.VSTS.Scheduling.OriginalEstimate'] ?? '',
    remainingWork: fields['Microsoft.VSTS.Scheduling.RemainingWork'] ?? '',
    storyPoints: fields['Microsoft.VSTS.Scheduling.StoryPoints'] ?? '',
  };
}

async function fetchBatchByIds(ids, fields) {
  const client = createClient();
  if (!ids.length) return [];

  const pageSize = 200;
  const results = [];

  for (let i = 0; i < ids.length; i += pageSize) {
    const chunk = ids.slice(i, i + pageSize);
    const batch = await client.post('/_apis/wit/workitemsbatch?api-version=7.1', {
      ids: chunk,
      fields,
      errorPolicy: 'Omit',
    });
    results.push(...(batch.value || []).map(normalizeWorkItem));
  }

  return results;
}

async function fetchByWiql({ project, team, wiql, fields }) {
  const client = createClient();
  const scopePath = team
    ? `/${encodeURIComponent(project)}/${encodeURIComponent(team)}/_apis/wit/wiql?api-version=7.1`
    : `/${encodeURIComponent(project)}/_apis/wit/wiql?api-version=7.1`;

  const queryResult = await client.post(scopePath, { query: wiql });
  const ids = (queryResult.workItems || []).map(w => w.id);
  return fetchBatchByIds(ids, fields);
}

async function fetchByQueryId({ project, id, fields }) {
  const client = createClient();
  const result = await client.get(`/${encodeURIComponent(project)}/_apis/wit/wiql/${encodeURIComponent(id)}?api-version=7.1`);
  const ids = (result.workItems || []).map(w => w.id);
  return fetchBatchByIds(ids, fields);
}

async function main() {
  const command = process.argv[2];
  const args = parseArgs(process.argv.slice(3));
  const fields = validateFields(args.fields);
  const config = loadConfig();

  if (command === 'wiql') {
    const project = validatePathPart(args.project || config.defaultProject, 'project');
    const team = args.team ? validatePathPart(args.team, 'team') : '';
    const query = requireNonEmpty(args.query, 'query');
    const items = await fetchByWiql({ project, team, wiql: query, fields });
    console.log(JSON.stringify({ project, team, count: items.length, items }, null, 2));
    return;
  }

  if (command === 'query-id') {
    const project = validatePathPart(args.project || config.defaultProject, 'project');
    const id = requireNonEmpty(args.id || config.defaultQueryId, 'id');
    const items = await fetchByQueryId({ project, id, fields });
    console.log(JSON.stringify({ project, queryId: id, count: items.length, items }, null, 2));
    return;
  }

  if (command === 'closed-last-week') {
    const project = validatePathPart(args.project || config.defaultProject, 'project');
    const since = isoDateDaysAgo(7);
    const wiql = `SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '${escapeWiqlString(project)}' AND [System.State] = 'Closed' AND [Microsoft.VSTS.Common.ClosedDate] >= '${since}' ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC`;
    const items = await fetchByWiql({ project, wiql, fields });
    console.log(JSON.stringify({ project, since, count: items.length, items }, null, 2));
    return;
  }

  throw new Error('Usage: node scripts/workitems.js <wiql|query-id|closed-last-week> ...');
}

if (require.main === module) {
  main().catch(err => {
    console.error(err.message);
    process.exit(1);
  });
}

module.exports = { fetchByWiql, fetchByQueryId, fetchBatchByIds, normalizeWorkItem };
