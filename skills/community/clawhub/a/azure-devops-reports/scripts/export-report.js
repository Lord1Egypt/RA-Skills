#!/usr/bin/env node
const fs = require('fs');
const { createClient } = require('./ado-client');
const { loadConfig } = require('./config');
const { fetchByWiql, fetchByQueryId } = require('./workitems');
const { parseArgs, toCsv, summarizeBy } = require('./utils');
const { safeOutputPath, validatePathPart, requireNonEmpty } = require('./validators');

async function getCurrentIteration(project, team) {
  const client = createClient();
  const data = await client.get(`/${encodeURIComponent(project)}/${encodeURIComponent(team)}/_apis/work/teamsettings/iterations?$timeframe=current&api-version=7.1-preview.1`);
  return (data.value || [])[0] || null;
}

function buildSummary(items) {
  return {
    totals: { workItems: items.length },
    byState: summarizeBy(items, 'state'),
    byAssignee: summarizeBy(items, 'assignedTo'),
    byType: summarizeBy(items, 'type'),
  };
}

async function runSprintSummary(args) {
  const project = validatePathPart(args.project, 'project');
  const team = validatePathPart(args.team, 'team');
  const current = await getCurrentIteration(project, team);
  if (!current) throw new Error('No current iteration found for the team');
  const iterationPath = current.path;
  const escapedIteration = iterationPath.replace(/'/g, "''");
  const escapedProject = project.replace(/'/g, "''");
  const wiql = `SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '${escapedProject}' AND [System.IterationPath] = '${escapedIteration}' ORDER BY [System.ChangedDate] DESC`;
  const items = await fetchByWiql({ project, team, wiql });
  return {
    reportType: 'sprint-summary',
    project,
    team,
    iteration: {
      id: current.id,
      name: current.name,
      path: current.path,
      attributes: current.attributes || {},
    },
    items,
    summary: buildSummary(items),
  };
}

async function runWiql(args) {
  const project = validatePathPart(args.project, 'project');
  const team = args.team ? validatePathPart(args.team, 'team') : '';
  const query = requireNonEmpty(args.query, 'query');
  const items = await fetchByWiql({ project, team, wiql: query });
  return {
    reportType: 'wiql',
    project,
    team,
    query,
    items,
    summary: buildSummary(items),
  };
}

async function runQueryId(args) {
  const config = loadConfig();
  const project = validatePathPart(args.project || config.defaultProject, 'project');
  const id = requireNonEmpty(args.id || config.defaultQueryId, 'id');
  const items = await fetchByQueryId({ project, id });
  return {
    reportType: 'query-id',
    project,
    queryId: id,
    items,
    summary: buildSummary(items),
  };
}

function writeOutput(bundle, format, outFile) {
  const config = loadConfig();
  const outputPath = safeOutputPath(config.outputDir, outFile);

  if (format === 'json') {
    fs.writeFileSync(outputPath, JSON.stringify(bundle, null, 2));
  } else if (format === 'csv') {
    fs.writeFileSync(outputPath, toCsv(bundle.items));
    const summaryPath = outputPath.replace(/\.csv$/i, '.summary.json');
    fs.writeFileSync(summaryPath, JSON.stringify(bundle.summary, null, 2));
  } else {
    throw new Error('Unsupported format. Use json or csv for now.');
  }

  return outputPath;
}

async function main() {
  const firstArg = process.argv[2];
  const knownCommands = new Set(['sprint-summary', 'wiql', 'query-id', 'default']);
  const command = knownCommands.has(firstArg) ? firstArg : 'default';
  const argOffset = command === 'default' && firstArg !== 'default' ? 2 : 3;
  const args = parseArgs(process.argv.slice(argOffset));
  const format = (args.format || 'json').toLowerCase();
  const defaultOut = command === 'default' || command === 'query-id'
    ? (format === 'csv' ? 'query-data.csv' : 'query-data.json')
    : (format === 'csv' ? `${command}.csv` : `${command}.json`);
  const out = args.out || defaultOut;

  let bundle;
  if (command === 'sprint-summary') {
    bundle = await runSprintSummary(args);
  } else if (command === 'wiql') {
    bundle = await runWiql(args);
  } else if (command === 'query-id' || command === 'default') {
    bundle = await runQueryId(args);
  } else {
    throw new Error('Usage: node scripts/export-report.js [sprint-summary|wiql|query-id|default] ...');
  }

  const outputPath = writeOutput(bundle, format, out);
  console.log(JSON.stringify({
    ok: true,
    reportType: bundle.reportType,
    outputPath,
    count: bundle.items.length,
    summary: bundle.summary,
  }, null, 2));
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
