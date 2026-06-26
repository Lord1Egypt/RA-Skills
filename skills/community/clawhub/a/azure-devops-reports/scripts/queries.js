#!/usr/bin/env node
const { createClient } = require('./ado-client');
const { validatePathPart, requireNonEmpty } = require('./validators');
const { parseArgs } = require('./utils');

function flattenQueries(nodes, depth = 0, bucket = []) {
  for (const node of nodes || []) {
    bucket.push({
      id: node.id || '',
      name: node.name || '',
      path: node.path || '',
      isFolder: node.isFolder === true,
      hasChildren: Array.isArray(node.children) && node.children.length > 0,
      depth,
      url: node.url || '',
    });
    if (Array.isArray(node.children) && node.children.length) {
      flattenQueries(node.children, depth + 1, bucket);
    }
  }
  return bucket;
}

async function listQueries(project, depth) {
  const client = createClient();
  const data = await client.get(`/${encodeURIComponent(project)}/_apis/wit/queries?$depth=${depth}&$expand=all&api-version=7.1`);
  const queries = flattenQueries(data.value || []);
  return { project, count: queries.length, queries };
}

async function getQuery(project, id) {
  const client = createClient();
  const data = await client.get(`/${encodeURIComponent(project)}/_apis/wit/queries/${encodeURIComponent(id)}?$expand=all&api-version=7.1`);
  return data;
}

async function main() {
  const command = process.argv[2];
  const args = parseArgs(process.argv.slice(3));
  const project = validatePathPart(args.project, 'project');

  if (command === 'list') {
    const depth = Number(args.depth || 2);
    const result = await listQueries(project, Number.isFinite(depth) ? depth : 2);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'get') {
    const id = requireNonEmpty(args.id, 'id');
    const result = await getQuery(project, id);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  throw new Error('Usage: node scripts/queries.js <list|get> --project "Project" [--depth 2] [--id query-guid]');
}

if (require.main === module) {
  main().catch(err => {
    console.error(err.message);
    process.exit(1);
  });
}

module.exports = { listQueries, getQuery };
