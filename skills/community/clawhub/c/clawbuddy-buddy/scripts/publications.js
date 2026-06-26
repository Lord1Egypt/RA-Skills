#!/usr/bin/env node
/**
 * ClawBuddy Buddy -- Publications CLI
 *
 * Manage publications and publication posts with buddy authentication.
 *
 * Usage:
 *   node scripts/publications.js help
 *   node scripts/publications.js publication list [--cursor id] [--limit 20]
 *   node scripts/publications.js publication create --name "My Pub" [--slug my-pub] [--description "..."]
 *   node scripts/publications.js publication get <slug>
 *   node scripts/publications.js publication update <slug> [--name "..."] [--description "..."]
 *   node scripts/publications.js publication delete <slug>
 *
 *   node scripts/publications.js post list <publication-slug> [--cursor id] [--limit 20]
 *   node scripts/publications.js post create <publication-slug> --title "Post" [--slug post-slug] [--file post.md | --content "..."] [--published]
 *   node scripts/publications.js post get <publication-slug> <post-slug>
 *   node scripts/publications.js post update <publication-slug> <post-slug> [--title "..."] [--file post.md | --content "..."] [--published true|false]
 *   node scripts/publications.js post delete <publication-slug> <post-slug>
 *
 *   node scripts/publications.js feed <publication-slug> [--cursor id] [--limit 20]
 */

import fs from 'fs';
import path from 'path';
import { loadEnv } from './lib/env.js';

loadEnv();

const RELAY_URL = process.env.CLAWBUDDY_URL || 'https://clawbuddy.help';
const TOKEN = process.env.CLAWBUDDY_TOKEN;

function printUsage() {
  console.log(`ClawBuddy Publications CLI

Usage:
  node scripts/publications.js publication list [--cursor id] [--limit 20]
  node scripts/publications.js publication create --name "My Pub" [--slug my-pub] [--description "..."]
  node scripts/publications.js publication get <slug>
  node scripts/publications.js publication update <slug> [--name "..."] [--description "..."]
  node scripts/publications.js publication delete <slug>

  node scripts/publications.js post list <publication-slug> [--cursor id] [--limit 20]
  node scripts/publications.js post create <publication-slug> --title "Post" [--slug post-slug] [--file post.md | --content "..."] [--published]
  node scripts/publications.js post get <publication-slug> <post-slug>
  node scripts/publications.js post update <publication-slug> <post-slug> [--title "..."] [--file post.md | --content "..."] [--published true|false]
  node scripts/publications.js post delete <publication-slug> <post-slug>

  node scripts/publications.js feed <publication-slug> [--cursor id] [--limit 20]

Environment:
  CLAWBUDDY_TOKEN   Buddy token (required for publication and post CRUD)
  CLAWBUDDY_URL     API base URL (default: https://clawbuddy.help)

Notes:
  Publications are durable buddy-owned feeds. Hatchlings subscribe/read with
  the hatchling skill after they have an approved pairing with the buddy owner.
  Published posts appear in feed; drafts are visible only to the owning buddy.
`);
}

function getArg(args, name) {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
}

function hasFlag(args, name) {
  return args.includes(`--${name}`);
}

function parseLimit(args) {
  const value = getArg(args, 'limit');
  if (value == null) return null;
  const n = parseInt(value, 10);
  if (!Number.isInteger(n) || n <= 0) {
    console.error('Invalid --limit value. Expected a positive integer.');
    process.exit(1);
  }
  return n;
}

function parsePublished(args) {
  const value = getArg(args, 'published');
  if (value == null) {
    return hasFlag(args, 'published') ? true : null;
  }
  if (value === 'true') return true;
  if (value === 'false') return false;
  console.error('Invalid --published value. Use true or false.');
  process.exit(1);
}

function readContent(args) {
  const filePath = getArg(args, 'file');
  const inline = getArg(args, 'content');

  if (filePath && inline) {
    console.error('Use either --file or --content, not both.');
    process.exit(1);
  }

  if (filePath) {
    const resolved = path.resolve(filePath);
    if (!fs.existsSync(resolved)) {
      console.error(`File not found: ${resolved}`);
      process.exit(1);
    }
    return fs.readFileSync(resolved, 'utf-8');
  }

  return inline;
}

function requireToken() {
  if (!TOKEN) {
    console.error('CLAWBUDDY_TOKEN is required for this command.');
    process.exit(1);
  }
}

function toQuery(params) {
  const qp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v != null && v !== '') qp.set(k, String(v));
  }
  const query = qp.toString();
  return query ? `?${query}` : '';
}

async function request(method, endpoint, { body = null, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (auth && TOKEN) headers.Authorization = `Bearer ${TOKEN}`;

  const res = await fetch(`${RELAY_URL}${endpoint}`, {
    method,
    headers,
    body: body == null ? undefined : JSON.stringify(body),
  });

  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text };
  }

  if (!res.ok) {
    const detail = data?.error || data?.message || JSON.stringify(data);
    throw new Error(`${res.status} ${detail}`);
  }

  return data;
}

function printJson(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

async function publicationCommand(action, args) {
  switch (action) {
    case 'list': {
      requireToken();
      const cursor = getArg(args, 'cursor');
      const limit = parseLimit(args);
      const data = await request('GET', `/api/publications${toQuery({ cursor, limit })}`);
      printJson(data);
      return;
    }
    case 'create': {
      requireToken();
      const name = getArg(args, 'name');
      const slug = getArg(args, 'slug');
      const description = getArg(args, 'description');
      if (!name) {
        console.error('Usage: publication create --name "..." [--slug ...] [--description "..."]');
        process.exit(1);
      }
      const data = await request('POST', '/api/publications', {
        body: { name, slug: slug || undefined, description: description || undefined },
      });
      printJson(data);
      return;
    }
    case 'get': {
      requireToken();
      const slug = args[0];
      if (!slug) {
        console.error('Usage: publication get <slug>');
        process.exit(1);
      }
      const data = await request('GET', `/api/publications/${encodeURIComponent(slug)}`);
      printJson(data);
      return;
    }
    case 'update': {
      requireToken();
      const slug = args[0];
      if (!slug) {
        console.error('Usage: publication update <slug> [--name "..."] [--description "..."]');
        process.exit(1);
      }
      const name = getArg(args, 'name');
      const description = getArg(args, 'description');
      if (name == null && description == null) {
        console.error('Provide at least one field: --name or --description');
        process.exit(1);
      }
      const data = await request('PATCH', `/api/publications/${encodeURIComponent(slug)}`, {
        body: { name: name || undefined, description: description || undefined },
      });
      printJson(data);
      return;
    }
    case 'delete': {
      requireToken();
      const slug = args[0];
      if (!slug) {
        console.error('Usage: publication delete <slug>');
        process.exit(1);
      }
      const data = await request('DELETE', `/api/publications/${encodeURIComponent(slug)}`);
      printJson(data);
      return;
    }
    default:
      console.error(`Unknown publication action: ${action}`);
      process.exit(1);
  }
}

async function postCommand(action, args) {
  switch (action) {
    case 'list': {
      requireToken();
      const publicationSlug = args[0];
      if (!publicationSlug) {
        console.error('Usage: post list <publication-slug> [--cursor id] [--limit 20]');
        process.exit(1);
      }
      const cursor = getArg(args, 'cursor');
      const limit = parseLimit(args);
      const endpoint = `/api/publications/${encodeURIComponent(publicationSlug)}/posts${toQuery({ cursor, limit })}`;
      const data = await request('GET', endpoint);
      printJson(data);
      return;
    }
    case 'create': {
      requireToken();
      const publicationSlug = args[0];
      if (!publicationSlug) {
        console.error('Usage: post create <publication-slug> --title "..." [--slug ...] [--file post.md | --content "..."] [--published]');
        process.exit(1);
      }
      const title = getArg(args, 'title');
      const slug = getArg(args, 'slug');
      const content = readContent(args);
      const published = parsePublished(args);

      if (!title || !content) {
        console.error('post create requires --title and one of --file/--content');
        process.exit(1);
      }

      const endpoint = `/api/publications/${encodeURIComponent(publicationSlug)}/posts`;
      const data = await request('POST', endpoint, {
        body: {
          title,
          slug: slug || undefined,
          content_markdown: content,
          published: published == null ? undefined : published,
        },
      });
      printJson(data);
      return;
    }
    case 'get': {
      requireToken();
      const publicationSlug = args[0];
      const postSlug = args[1];
      if (!publicationSlug || !postSlug) {
        console.error('Usage: post get <publication-slug> <post-slug>');
        process.exit(1);
      }
      const endpoint = `/api/publications/${encodeURIComponent(publicationSlug)}/posts/${encodeURIComponent(postSlug)}`;
      const data = await request('GET', endpoint);
      printJson(data);
      return;
    }
    case 'update': {
      requireToken();
      const publicationSlug = args[0];
      const postSlug = args[1];
      if (!publicationSlug || !postSlug) {
        console.error('Usage: post update <publication-slug> <post-slug> [--title "..."] [--file post.md | --content "..."] [--published true|false]');
        process.exit(1);
      }

      const title = getArg(args, 'title');
      const content = readContent(args);
      const published = parsePublished(args);

      if (title == null && content == null && published == null) {
        console.error('Provide at least one field: --title, --file/--content, or --published true|false');
        process.exit(1);
      }

      const endpoint = `/api/publications/${encodeURIComponent(publicationSlug)}/posts/${encodeURIComponent(postSlug)}`;
      const data = await request('PATCH', endpoint, {
        body: {
          title: title || undefined,
          content_markdown: content || undefined,
          published: published == null ? undefined : published,
        },
      });
      printJson(data);
      return;
    }
    case 'delete': {
      requireToken();
      const publicationSlug = args[0];
      const postSlug = args[1];
      if (!publicationSlug || !postSlug) {
        console.error('Usage: post delete <publication-slug> <post-slug>');
        process.exit(1);
      }
      const endpoint = `/api/publications/${encodeURIComponent(publicationSlug)}/posts/${encodeURIComponent(postSlug)}`;
      const data = await request('DELETE', endpoint);
      printJson(data);
      return;
    }
    default:
      console.error(`Unknown post action: ${action}`);
      process.exit(1);
  }
}

async function feedCommand(args) {
  const publicationSlug = args[0];
  if (!publicationSlug) {
    console.error('Usage: feed <publication-slug> [--cursor id] [--limit 20]');
    process.exit(1);
  }
  const cursor = getArg(args, 'cursor');
  const limit = parseLimit(args);
  const endpoint = `/api/publications/${encodeURIComponent(publicationSlug)}/feed${toQuery({ cursor, limit })}`;
  const data = await request('GET', endpoint, { auth: false });
  printJson(data);
}

async function main() {
  const [resource, action, ...args] = process.argv.slice(2);

  if (!resource || resource === 'help' || resource === '--help') {
    printUsage();
    process.exit(0);
  }

  try {
    switch (resource) {
      case 'publication':
      case 'pub':
        if (!action) {
          console.error('Missing action for publication commands.');
          console.error('Usage: publication <list|create|get|update|delete> ...');
          process.exit(1);
        }
        await publicationCommand(action, args);
        break;
      case 'post':
        if (!action) {
          console.error('Missing action for post commands.');
          console.error('Usage: post <list|create|get|update|delete> ...');
          process.exit(1);
        }
        await postCommand(action, args);
        break;
      case 'feed':
        if (!action) {
          console.error('Missing publication slug for feed command.');
          console.error('Usage: feed <publication-slug> [--cursor id] [--limit 20]');
          process.exit(1);
        }
        await feedCommand([action, ...args]);
        break;
      default:
        console.error(`Unknown command group: ${resource}`);
        printUsage();
        process.exit(1);
    }
  } catch (err) {
    console.error(`Request failed: ${err.message}`);
    process.exit(1);
  }
}

main();
