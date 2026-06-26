#!/usr/bin/env node
const { createClient } = require('./ado-client');

async function main() {
  const command = process.argv[2] || 'list';
  if (command !== 'list') throw new Error('Only supported command: list');
  const client = createClient();
  const data = await client.get('/_apis/projects?api-version=7.1');
  const projects = (data.value || []).map(p => ({
    id: p.id,
    name: p.name,
    description: p.description || '',
    state: p.state || '',
    visibility: p.visibility || '',
  }));
  console.log(JSON.stringify({ count: projects.length, projects }, null, 2));
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
