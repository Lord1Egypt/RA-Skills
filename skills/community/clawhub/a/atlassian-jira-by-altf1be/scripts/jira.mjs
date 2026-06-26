#!/usr/bin/env node

/**
 * OpenClaw Jira Cloud Skill — CLI for Jira issue management via REST API v3.
 *
 * @author Abdelkrim BOUJRAF <abdelkrim@alt-f1.be>
 * @license MIT
 * @see https://www.alt-f1.be
 */

// File I/O is used ONLY for reading user-specified attachments that the user
// explicitly passes via --file flag. No arbitrary file access.
import { readFileSync, statSync } from 'node:fs';
import { basename, resolve, posix } from 'node:path';
import { Buffer } from 'node:buffer';
import { config } from 'dotenv';
import { Command } from 'commander';

// ── Config ──────────────────────────────────────────────────────────────────

config(); // load .env

let _cfg;
function getCfg() {
  if (!_cfg) {
    // Only Jira-specific env vars are read — nothing else.
    const host     = process.env.JIRA_HOST;
    const email    = process.env.JIRA_EMAIL;
    const apiToken = process.env.JIRA_API_TOKEN;

    const missing = [];
    if (!host)     missing.push('JIRA_HOST');
    if (!email)    missing.push('JIRA_EMAIL');
    if (!apiToken) missing.push('JIRA_API_TOKEN');

    if (missing.length) {
      console.error(`ERROR: Missing required env var(s): ${missing.join(', ')}. See .env.example`);
      process.exit(1);
    }

    _cfg = {
      host,
      email,
      apiToken,
      defaultProject: process.env.JIRA_DEFAULT_PROJECT || '',
      maxResults:     parseInt(process.env.JIRA_MAX_RESULTS || '50', 10),
      maxFileSize:    parseInt(process.env.JIRA_MAX_FILE_SIZE || '52428800', 10), // 50 MB
    };
  }
  return _cfg;
}
const CFG = new Proxy({}, { get: (_, prop) => getCfg()[prop] });

// ── Security helpers ────────────────────────────────────────────────────────

function safePath(p) {
  if (!p) return '';
  const normalized = posix.normalize(p).replace(/\\/g, '/');
  if (normalized.includes('..')) {
    console.error('ERROR: Path traversal detected — ".." is not allowed');
    process.exit(1);
  }
  return normalized.replace(/^\/+/, '');
}

function checkFileSize(filePath) {
  const stat = statSync(filePath);
  if (stat.size > CFG.maxFileSize) {
    console.error(`ERROR: File exceeds size limit (${(stat.size / 1048576).toFixed(1)} MB > ${(CFG.maxFileSize / 1048576).toFixed(1)} MB)`);
    process.exit(1);
  }
  return stat.size;
}

// ── HTTP client with rate-limit retry ───────────────────────────────────────

function authHeader() {
  const token = Buffer.from(`${CFG.email}:${CFG.apiToken}`).toString('base64');
  return `Basic ${token}`;
}

function baseUrl() {
  const host = CFG.host.replace(/\/+$/, '');
  const prefix = host.startsWith('http') ? host : `https://${host}`;
  return `${prefix}/rest/api/3`;
}

async function jiraFetch(path, options = {}, retries = 3) {
  const url = path.startsWith('http') ? path : `${baseUrl()}${path}`;
  const headers = {
    'Authorization': authHeader(),
    'Accept': 'application/json',
    ...options.headers,
  };

  // Don't set Content-Type for FormData (let fetch set boundary)
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  }

  for (let attempt = 1; attempt <= retries; attempt++) {
    const resp = await fetch(url, { ...options, headers });

    // Rate limited — retry with backoff
    if (resp.status === 429) {
      const retryAfter = parseInt(resp.headers.get('retry-after') || '5', 10);
      const backoff = retryAfter * 1000 * attempt;
      if (attempt < retries) {
        console.error(`⏳ Rate limited — retrying in ${(backoff / 1000).toFixed(0)}s (attempt ${attempt}/${retries})`);
        await new Promise(r => setTimeout(r, backoff));
        continue;
      }
    }

    if (resp.status === 204) return null; // No content (deletes)

    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }

    if (!resp.ok) {
      const msg = json?.errorMessages?.join(', ')
        || json?.errors && Object.values(json.errors).join(', ')
        || json?.message
        || body
        || resp.statusText;
      const err = new Error(msg);
      err.statusCode = resp.status;
      throw err;
    }

    return json;
  }
}

// ── Issue commands ──────────────────────────────────────────────────────────

async function cmdList(options) {
  const parts = [];
  const project = options.project || CFG.defaultProject;
  if (project) parts.push(`project = "${project}"`);
  if (options.status) parts.push(`status = "${options.status}"`);
  if (options.assignee) parts.push(`assignee = ${options.assignee}`);

  const jql = parts.length ? parts.join(' AND ') : 'ORDER BY updated DESC';
  const resp = await jiraFetch(`/search/jql?jql=${encodeURIComponent(jql)}&maxResults=${CFG.maxResults}&fields=key,summary,status,priority,assignee,updated`);

  if (!resp.issues.length) {
    console.log('No issues found.');
    return;
  }

  for (const issue of resp.issues) {
    const f = issue.fields;
    const status = f.status?.name || '?';
    const priority = f.priority?.name || '?';
    const assignee = f.assignee?.displayName || 'Unassigned';
    const updated = f.updated?.substring(0, 10) || '';
    console.log(`🎫  ${issue.key.padEnd(12)}  ${status.padEnd(14)}  ${priority.padEnd(8)}  ${assignee.padEnd(20)}  ${updated}  ${f.summary}`);
  }
  const total = resp.total ?? resp.maxResults ?? resp.issues.length;
  console.log(`\n${resp.issues.length} of ${total} issues`);
}

async function cmdCreate(options) {
  const project = options.project || CFG.defaultProject;
  if (!project) {
    console.error('ERROR: --project is required (or set JIRA_DEFAULT_PROJECT)');
    process.exit(1);
  }
  if (!options.summary) {
    console.error('ERROR: --summary is required');
    process.exit(1);
  }

  const fields = {
    project: { key: project },
    summary: options.summary,
    issuetype: { name: options.type || 'Task' },
  };

  if (options.description) {
    fields.description = {
      type: 'doc',
      version: 1,
      content: [{
        type: 'paragraph',
        content: [{ type: 'text', text: options.description }],
      }],
    };
  }
  if (options.priority) fields.priority = { name: options.priority };
  if (options.assignee) {
    // Accept account ID or "currentUser()" or email-like strings
    fields.assignee = { id: options.assignee };
  }

  const result = await jiraFetch('/issue', {
    method: 'POST',
    body: JSON.stringify({ fields }),
  });

  console.log(`✅ Created: ${result.key}`);
  console.log(`   URL: https://${CFG.host}/browse/${result.key}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdRead(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }

  const issue = await jiraFetch(`/issue/${options.key}`);
  const f = issue.fields;

  console.log(`🎫 ${issue.key}: ${f.summary}`);
  console.log(`   Status:     ${f.status?.name || '?'}`);
  console.log(`   Type:       ${f.issuetype?.name || '?'}`);
  console.log(`   Priority:   ${f.priority?.name || '?'}`);
  console.log(`   Assignee:   ${f.assignee?.displayName || 'Unassigned'}`);
  console.log(`   Reporter:   ${f.reporter?.displayName || '?'}`);
  console.log(`   Created:    ${f.created?.substring(0, 10) || '?'}`);
  console.log(`   Updated:    ${f.updated?.substring(0, 10) || '?'}`);
  console.log(`   Labels:     ${f.labels?.join(', ') || 'none'}`);
  console.log(`   Components: ${f.components?.map(c => c.name).join(', ') || 'none'}`);
  console.log(`   URL:        https://${CFG.host}/browse/${issue.key}`);

  // Print description if present
  if (f.description?.content) {
    console.log(`\n📝 Description:`);
    const text = extractAdfText(f.description);
    console.log(text);
  }
}

function extractAdfText(adf) {
  if (!adf || !adf.content) return '';
  const lines = [];
  for (const node of adf.content) {
    if (node.type === 'paragraph' && node.content) {
      lines.push(node.content.map(n => n.text || '').join(''));
    } else if (node.type === 'heading' && node.content) {
      lines.push('\n' + node.content.map(n => n.text || '').join(''));
    } else if (node.type === 'bulletList' && node.content) {
      for (const item of node.content) {
        if (item.content) {
          for (const p of item.content) {
            if (p.content) lines.push('  • ' + p.content.map(n => n.text || '').join(''));
          }
        }
      }
    } else if (node.type === 'orderedList' && node.content) {
      let i = 1;
      for (const item of node.content) {
        if (item.content) {
          for (const p of item.content) {
            if (p.content) lines.push(`  ${i++}. ` + p.content.map(n => n.text || '').join(''));
          }
        }
      }
    } else if (node.type === 'codeBlock' && node.content) {
      lines.push('```');
      lines.push(node.content.map(n => n.text || '').join(''));
      lines.push('```');
    }
  }
  return lines.join('\n');
}

async function cmdUpdate(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }

  const fields = {};
  if (options.summary) fields.summary = options.summary;
  if (options.priority) fields.priority = { name: options.priority };
  if (options.assignee) fields.assignee = { id: options.assignee };
  if (options.type) fields.issuetype = { name: options.type };
  if (options.labels) fields.labels = options.labels.split(',').map(l => l.trim());
  if (options.description) {
    fields.description = {
      type: 'doc',
      version: 1,
      content: [{
        type: 'paragraph',
        content: [{ type: 'text', text: options.description }],
      }],
    };
  }

  if (Object.keys(fields).length === 0) {
    console.error('ERROR: No fields to update. Use --summary, --priority, --assignee, --description, --labels, or --type');
    process.exit(1);
  }

  await jiraFetch(`/issue/${options.key}`, {
    method: 'PUT',
    body: JSON.stringify({ fields }),
  });

  console.log(`✅ Updated: ${options.key}`);
}

async function cmdDelete(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: jira delete --key PROJ-123 --confirm');
    process.exit(1);
  }

  await jiraFetch(`/issue/${options.key}`, { method: 'DELETE' });
  console.log(`✅ Deleted: ${options.key}`);
}

async function cmdSearch(options) {
  if (!options.jql) {
    console.error('ERROR: --jql is required');
    process.exit(1);
  }

  const resp = await jiraFetch(`/search/jql?jql=${encodeURIComponent(options.jql)}&maxResults=${CFG.maxResults}&fields=key,summary,status,priority,assignee,updated`);

  if (!resp.issues.length) {
    console.log('No issues found.');
    return;
  }

  for (const issue of resp.issues) {
    const f = issue.fields;
    const status = f.status?.name || '?';
    const priority = f.priority?.name || '?';
    const assignee = f.assignee?.displayName || 'Unassigned';
    const updated = f.updated?.substring(0, 10) || '';
    console.log(`🎫  ${issue.key.padEnd(12)}  ${status.padEnd(14)}  ${priority.padEnd(8)}  ${assignee.padEnd(20)}  ${updated}  ${f.summary}`);
  }
  const total = resp.total ?? resp.maxResults ?? resp.issues.length;
  console.log(`\n${resp.issues.length} of ${total} issues`);
}

// ── Comment commands ────────────────────────────────────────────────────────

async function cmdCommentList(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }

  const resp = await jiraFetch(`/issue/${options.key}/comment`);

  if (!resp.comments.length) {
    console.log('No comments.');
    return;
  }

  for (const c of resp.comments) {
    const author = c.author?.displayName || '?';
    const created = c.created?.substring(0, 16).replace('T', ' ') || '?';
    const body = c.body?.content
      ? extractAdfText(c.body)
      : (c.body || '');
    console.log(`💬 #${c.id}  ${author}  ${created}`);
    console.log(`   ${body.substring(0, 200)}${body.length > 200 ? '...' : ''}`);
    console.log('');
  }
  console.log(`${resp.comments.length} comment(s)`);
}

async function cmdCommentAdd(options) {
  if (!options.key || !options.body) {
    console.error('ERROR: --key and --body are required');
    process.exit(1);
  }

  const result = await jiraFetch(`/issue/${options.key}/comment`, {
    method: 'POST',
    body: JSON.stringify({
      body: {
        type: 'doc',
        version: 1,
        content: [{
          type: 'paragraph',
          content: [{ type: 'text', text: options.body }],
        }],
      },
    }),
  });

  console.log(`✅ Comment added to ${options.key}`);
  console.log(`   ID: ${result.id}`);
}

async function cmdCommentUpdate(options) {
  if (!options.key || !options.commentId || !options.body) {
    console.error('ERROR: --key, --comment-id, and --body are required');
    process.exit(1);
  }

  await jiraFetch(`/issue/${options.key}/comment/${options.commentId}`, {
    method: 'PUT',
    body: JSON.stringify({
      body: {
        type: 'doc',
        version: 1,
        content: [{
          type: 'paragraph',
          content: [{ type: 'text', text: options.body }],
        }],
      },
    }),
  });

  console.log(`✅ Comment #${options.commentId} updated on ${options.key}`);
}

async function cmdCommentDelete(options) {
  if (!options.key || !options.commentId) {
    console.error('ERROR: --key and --comment-id are required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: jira comment-delete --key PROJ-123 --comment-id 10001 --confirm');
    process.exit(1);
  }

  await jiraFetch(`/issue/${options.key}/comment/${options.commentId}`, { method: 'DELETE' });
  console.log(`✅ Comment #${options.commentId} deleted from ${options.key}`);
}

// ── Attachment commands ─────────────────────────────────────────────────────

async function cmdAttachmentList(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }

  const issue = await jiraFetch(`/issue/${options.key}?fields=attachment`);
  const attachments = issue.fields.attachment || [];

  if (!attachments.length) {
    console.log('No attachments.');
    return;
  }

  for (const a of attachments) {
    const size = `${(a.size / 1024).toFixed(1)} KB`;
    const created = a.created?.substring(0, 10) || '';
    const author = a.author?.displayName || '?';
    console.log(`📎  #${a.id.toString().padEnd(8)}  ${a.filename.padEnd(30)}  ${size.padStart(12)}  ${created}  ${author}`);
  }
  console.log(`\n${attachments.length} attachment(s)`);
}

async function cmdAttachmentAdd(options) {
  if (!options.key || !options.file) {
    console.error('ERROR: --key and --file are required');
    process.exit(1);
  }

  const filePath = resolve(safePath(options.file) || options.file);
  checkFileSize(filePath);

  const fileContent = readFileSync(filePath);
  const fileName = basename(filePath);

  // Use FormData for multipart upload
  const form = new FormData();
  form.append('file', new Blob([fileContent]), fileName);

  const url = `${baseUrl()}/issue/${options.key}/attachments`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': authHeader(),
      'X-Atlassian-Token': 'no-check',
    },
    body: form,
  });

  if (!resp.ok) {
    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }
    const msg = json?.errorMessages?.join(', ') || json?.message || body;
    console.error(`ERROR (${resp.status}): ${msg}`);
    process.exit(1);
  }

  const result = await resp.json();
  const a = result[0];
  console.log(`✅ Attachment uploaded to ${options.key}`);
  console.log(`   File: ${a.filename}`);
  console.log(`   Size: ${(a.size / 1024).toFixed(1)} KB`);
  console.log(`   ID: ${a.id}`);
}

async function cmdAttachmentDelete(options) {
  if (!options.attachmentId) {
    console.error('ERROR: --attachment-id is required');
    process.exit(1);
  }
  if (!options.confirm) {
    console.error('ERROR: Delete requires --confirm flag for safety');
    console.error('Usage: jira attachment-delete --attachment-id 10001 --confirm');
    process.exit(1);
  }

  await jiraFetch(`/attachment/${options.attachmentId}`, { method: 'DELETE' });
  console.log(`✅ Attachment #${options.attachmentId} deleted`);
}

// ── Transition commands ─────────────────────────────────────────────────────

async function cmdTransitions(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }

  const resp = await jiraFetch(`/issue/${options.key}/transitions`);

  if (!resp.transitions.length) {
    console.log('No transitions available.');
    return;
  }

  console.log(`Available transitions for ${options.key}:\n`);
  for (const t of resp.transitions) {
    const to = t.to?.name || '?';
    console.log(`  ➡️  ID: ${t.id.toString().padEnd(6)}  Name: ${t.name.padEnd(20)}  → ${to}`);
  }
}

async function cmdTransition(options) {
  if (!options.key) {
    console.error('ERROR: --key is required');
    process.exit(1);
  }

  let transitionId = options.transitionId;

  // If name given, resolve to ID
  if (!transitionId && options.transitionName) {
    const resp = await jiraFetch(`/issue/${options.key}/transitions`);
    const match = resp.transitions.find(
      t => t.name.toLowerCase() === options.transitionName.toLowerCase()
    );
    if (!match) {
      console.error(`ERROR: Transition "${options.transitionName}" not found.`);
      console.error('Available transitions:');
      for (const t of resp.transitions) {
        console.error(`  - ${t.name} (ID: ${t.id})`);
      }
      process.exit(1);
    }
    transitionId = match.id;
  }

  if (!transitionId) {
    console.error('ERROR: --transition-id or --transition-name is required');
    process.exit(1);
  }

  await jiraFetch(`/issue/${options.key}/transitions`, {
    method: 'POST',
    body: JSON.stringify({ transition: { id: transitionId } }),
  });

  console.log(`✅ ${options.key} transitioned${options.transitionName ? ` to "${options.transitionName}"` : ` (transition ${transitionId})`}`);
}

// ── CLI ─────────────────────────────────────────────────────────────────────

const program = new Command();

program
  .name('jira')
  .description('OpenClaw Jira Cloud Skill — issue management via Atlassian REST API v3')
  .version('1.1.3');

// Issues
program
  .command('list')
  .description('List issues (with optional filters)')
  .option('-p, --project <key>', 'Project key')
  .option('-s, --status <status>', 'Filter by status')
  .option('-a, --assignee <user>', 'Filter by assignee (account ID or "currentUser()")')
  .action(wrap(cmdList));

program
  .command('create')
  .description('Create a new issue')
  .option('-p, --project <key>', 'Project key')
  .option('-t, --type <type>', 'Issue type (Task, Bug, Story, Epic...)', 'Task')
  .requiredOption('-s, --summary <text>', 'Issue summary')
  .option('-d, --description <text>', 'Issue description')
  .option('-a, --assignee <id>', 'Assignee account ID')
  .option('--priority <name>', 'Priority (Highest, High, Medium, Low, Lowest)')
  .action(wrap(cmdCreate));

program
  .command('read')
  .description('Read issue details')
  .requiredOption('-k, --key <key>', 'Issue key (e.g. PROJ-123)')
  .action(wrap(cmdRead));

program
  .command('update')
  .description('Update issue fields')
  .requiredOption('-k, --key <key>', 'Issue key')
  .option('-s, --summary <text>', 'New summary')
  .option('-d, --description <text>', 'New description')
  .option('-a, --assignee <id>', 'New assignee account ID')
  .option('--priority <name>', 'New priority')
  .option('-t, --type <type>', 'New issue type')
  .option('-l, --labels <labels>', 'Comma-separated labels')
  .action(wrap(cmdUpdate));

program
  .command('delete')
  .description('Delete an issue (requires --confirm)')
  .requiredOption('-k, --key <key>', 'Issue key')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdDelete));

program
  .command('search')
  .description('Search issues with JQL')
  .requiredOption('--jql <query>', 'JQL query string')
  .action(wrap(cmdSearch));

// Comments
program
  .command('comment-list')
  .description('List comments on an issue')
  .requiredOption('-k, --key <key>', 'Issue key')
  .action(wrap(cmdCommentList));

program
  .command('comment-add')
  .description('Add a comment to an issue')
  .requiredOption('-k, --key <key>', 'Issue key')
  .requiredOption('-b, --body <text>', 'Comment body')
  .action(wrap(cmdCommentAdd));

program
  .command('comment-update')
  .description('Update a comment')
  .requiredOption('-k, --key <key>', 'Issue key')
  .requiredOption('--comment-id <id>', 'Comment ID')
  .requiredOption('-b, --body <text>', 'New comment body')
  .action(wrap(cmdCommentUpdate));

program
  .command('comment-delete')
  .description('Delete a comment (requires --confirm)')
  .requiredOption('-k, --key <key>', 'Issue key')
  .requiredOption('--comment-id <id>', 'Comment ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdCommentDelete));

// Attachments
program
  .command('attachment-list')
  .description('List attachments on an issue')
  .requiredOption('-k, --key <key>', 'Issue key')
  .action(wrap(cmdAttachmentList));

program
  .command('attachment-add')
  .description('Upload an attachment to an issue')
  .requiredOption('-k, --key <key>', 'Issue key')
  .requiredOption('-f, --file <path>', 'Local file path')
  .action(wrap(cmdAttachmentAdd));

program
  .command('attachment-delete')
  .description('Delete an attachment (requires --confirm)')
  .requiredOption('--attachment-id <id>', 'Attachment ID')
  .option('--confirm', 'Confirm deletion (required)')
  .action(wrap(cmdAttachmentDelete));

// Transitions
program
  .command('transitions')
  .description('List available workflow transitions for an issue')
  .requiredOption('-k, --key <key>', 'Issue key')
  .action(wrap(cmdTransitions));

program
  .command('transition')
  .description('Move issue to new status via workflow transition')
  .requiredOption('-k, --key <key>', 'Issue key')
  .option('--transition-id <id>', 'Transition ID')
  .option('--transition-name <name>', 'Transition name (resolved to ID)')
  .action(wrap(cmdTransition));

function wrap(fn) {
  return async (...args) => {
    try {
      await fn(...args);
    } catch (err) {
      if (err.statusCode) {
        console.error(`ERROR (${err.statusCode}): ${err.message}`);
      } else {
        console.error(`ERROR: ${err.message}`);
      }
      process.exit(1);
    }
  };
}

program.parse();
