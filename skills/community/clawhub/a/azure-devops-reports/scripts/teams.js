#!/usr/bin/env node
const { createClient } = require('./ado-client');
const { validatePathPart } = require('./validators');

async function listTeams(project) {
  const client = createClient();
  const data = await client.get(`/_apis/projects/${encodeURIComponent(project)}/teams?api-version=7.1-preview.3`);
  const teams = (data.value || []).map(t => ({ id: t.id, name: t.name, description: t.description || '' }));
  return { project, count: teams.length, teams };
}

async function listMembers(project, team) {
  const client = createClient();
  const data = await client.get(`/_apis/projects/${encodeURIComponent(project)}/teams/${encodeURIComponent(team)}/members?api-version=7.1-preview.1`);
  const members = (data.value || []).map(m => ({
    id: m.identity?.id || m.id || '',
    displayName: m.identity?.displayName || m.displayName || '',
    uniqueName: m.identity?.uniqueName || m.uniqueName || '',
    url: m.identity?.url || m.url || '',
  }));
  return { project, team, count: members.length, members };
}

async function main() {
  const command = process.argv[2];
  const project = validatePathPart(process.argv[3], 'project');

  if (command === 'list') {
    const result = await listTeams(project);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'members') {
    const team = validatePathPart(process.argv[4], 'team');
    const result = await listMembers(project, team);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  throw new Error('Usage: node scripts/teams.js <list|members> "Project Name" ["Team Name"]');
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
