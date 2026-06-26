#!/usr/bin/env node
const { createClient } = require('./ado-client');
const { validatePathPart } = require('./validators');

async function main() {
  const command = process.argv[2];
  const project = validatePathPart(process.argv[3], 'project');
  const team = validatePathPart(process.argv[4], 'team');
  const client = createClient();

  let path;
  if (command === 'list') {
    path = `/${encodeURIComponent(project)}/${encodeURIComponent(team)}/_apis/work/teamsettings/iterations?api-version=7.1-preview.1`;
  } else if (command === 'current') {
    path = `/${encodeURIComponent(project)}/${encodeURIComponent(team)}/_apis/work/teamsettings/iterations?$timeframe=current&api-version=7.1-preview.1`;
  } else {
    throw new Error('Usage: node scripts/iterations.js <list|current> "Project Name" "Team Name"');
  }

  const data = await client.get(path);
  const iterations = (data.value || []).map(i => ({
    id: i.id,
    name: i.name,
    path: i.path,
    attributes: i.attributes || {},
    url: i.url,
  }));
  console.log(JSON.stringify({ project, team, count: iterations.length, iterations }, null, 2));
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
