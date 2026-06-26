#!/usr/bin/env node

/**
 * OpenClaw Bitbucket Cloud Skill — CLI for Bitbucket REST API 2.0.
 *
 * Covers ALL 335 endpoints across 23 API groups.
 *
 * @author Abdelkrim BOUJRAF <abdelkrim@alt-f1.be>
 * @license MIT
 * @see https://www.alt-f1.be
 */

import { readFileSync, statSync } from 'node:fs';
import { basename, resolve, posix } from 'node:path';
import { Buffer } from 'node:buffer';
import { config } from 'dotenv';
import { Command } from 'commander';

// ── Config ──────────────────────────────────────────────────────────────────

config();

let _cfg;
function getCfg() {
  if (!_cfg) {
    const email    = process.env.BITBUCKET_EMAIL;
    const apiToken = process.env.BITBUCKET_API_TOKEN;

    // Legacy fallback: support old BITBUCKET_USERNAME + BITBUCKET_APP_PASSWORD
    // until existing app passwords are disabled on June 9, 2026.
    const legacyUser = process.env.BITBUCKET_USERNAME;
    const legacyPass = process.env.BITBUCKET_APP_PASSWORD;

    const hasNew    = email && apiToken;
    const hasLegacy = legacyUser && legacyPass;

    if (!hasNew && !hasLegacy) {
      console.error('ERROR: Missing required env var(s): BITBUCKET_EMAIL + BITBUCKET_API_TOKEN. See .env.example');
      console.error('       (Legacy BITBUCKET_USERNAME + BITBUCKET_APP_PASSWORD also accepted until June 2026)');
      process.exit(1);
    }

    _cfg = {
      authUser:  hasNew ? email : legacyUser,
      authToken: hasNew ? apiToken : legacyPass,
      workspace:   process.env.BITBUCKET_WORKSPACE || '',
      maxResults:  parseInt(process.env.BITBUCKET_MAX_RESULTS || '50', 10),
      maxFileSize: 52428800, // 50 MB
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
  return `Basic ${Buffer.from(`${CFG.authUser}:${CFG.authToken}`).toString('base64')}`;
}

const BASE = 'https://api.bitbucket.org/2.0';

async function bbFetch(path, options = {}, retries = 3) {
  const url = path.startsWith('http') ? path : `${BASE}${path}`;
  const headers = {
    'Authorization': authHeader(),
    'Accept': 'application/json',
    ...options.headers,
  };

  if (!(options.body instanceof FormData) && !options.rawBody) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  }

  for (let attempt = 1; attempt <= retries; attempt++) {
    const resp = await fetch(url, { ...options, headers });

    if (resp.status === 429) {
      const retryAfter = parseInt(resp.headers.get('retry-after') || '5', 10);
      const backoff = retryAfter * 1000 * attempt;
      if (attempt < retries) {
        console.error(`⏳ Rate limited — retrying in ${(backoff / 1000).toFixed(0)}s (attempt ${attempt}/${retries})`);
        await new Promise(r => setTimeout(r, backoff));
        continue;
      }
    }

    if (resp.status === 204) return null;

    const body = await resp.text();
    let json;
    try { json = JSON.parse(body); } catch { json = null; }

    if (!resp.ok) {
      const msg = json?.error?.message
        || json?.error?.detail
        || (json?.error && typeof json.error === 'string' ? json.error : null)
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

// ── Helpers ─────────────────────────────────────────────────────────────────

const enc = encodeURIComponent;

function die(msg) {
  console.error(`ERROR: ${msg}`);
  process.exit(1);
}

function getWs(o) {
  const ws = o.workspace || CFG.workspace;
  if (!ws) die('--workspace is required (or set BITBUCKET_WORKSPACE)');
  return ws;
}

function reqOpt(o, name) {
  if (!o[name]) die(`--${name} is required`);
  return o[name];
}

function rp(o) {
  return `/repositories/${enc(getWs(o))}/${enc(reqOpt(o, 'repo'))}`;
}

function qs(o, extra = {}) {
  const p = new URLSearchParams();
  if (o.pagelen) p.set('pagelen', o.pagelen);
  if (o.page) p.set('page', o.page);
  if (o.q) p.set('q', o.q);
  if (o.sort) p.set('sort', o.sort);
  for (const [k, v] of Object.entries(extra)) {
    if (v !== undefined && v !== null) p.set(k, v);
  }
  const s = p.toString();
  return s ? `?${s}` : '';
}

function out(d) {
  console.log(JSON.stringify(d, null, 2));
}

function confirmOrDie(o) {
  if (!o.confirm) {
    die('--confirm flag is required for destructive operations');
  }
}

async function fetchAllPages(path, o, extra = {}) {
  if (!o.all) {
    return await bbFetch(`${path}${qs(o, extra)}`);
  }
  const allValues = [];
  let url = `${path}${qs(o, extra)}`;
  while (url) {
    const d = await bbFetch(url);
    if (d && d.values) allValues.push(...d.values);
    url = d && d.next ? d.next : null;
  }
  return { values: allValues, size: allValues.length };
}

function postBody(data) {
  return { method: 'POST', body: JSON.stringify(data) };
}

function putBody(data) {
  return { method: 'PUT', body: JSON.stringify(data) };
}

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

// Common option sets
function addWsOpts(c) {
  return c.option('-w, --workspace <slug>', 'Workspace slug');
}
function addRepoOpts(c) {
  return addWsOpts(c).option('-r, --repo <slug>', 'Repository slug');
}
function addPageOpts(c) {
  return c
    .option('--pagelen <n>', 'Results per page')
    .option('--page <n>', 'Page number')
    .option('--all', 'Fetch all pages');
}
function addFilterOpts(c) {
  return c
    .option('-q, --q <filter>', 'Filter query')
    .option('--sort <field>', 'Sort field');
}

// ── CLI Program ─────────────────────────────────────────────────────────────

const program = new Command();

program
  .name('bitbucket')
  .description('OpenClaw Bitbucket Cloud Skill — full CRUD via Atlassian REST API 2.0')
  .version('1.0.0');

// ═══════════════════════════════════════════════════════════════════════════
// 1. REPOSITORIES (26 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addFilterOpts(program
  .command('repo-list-public')
  .description('List public repositories')))
  .action(wrap(async (o) => { out(await fetchAllPages('/repositories', o)); }));

addPageOpts(addFilterOpts(addWsOpts(program
  .command('repo-list')
  .description('List repositories in a workspace'))))
  .action(wrap(async (o) => { out(await fetchAllPages(`/repositories/${enc(getWs(o))}`, o)); }));

addRepoOpts(program
  .command('repo-get')
  .description('Get a repository'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}`)); }));

addRepoOpts(program
  .command('repo-create')
  .description('Create a repository')
  .option('--scm <type>', 'SCM type (git)', 'git')
  .option('--is-private', 'Make repository private')
  .option('--project <key>', 'Project key')
  .option('--description <text>', 'Repository description')
  .option('--fork-policy <policy>', 'Fork policy (allow_forks, no_public_forks, no_forks)')
  .option('--language <lang>', 'Repository language'))
  .action(wrap(async (o) => {
    const body = { scm: o.scm };
    if (o.isPrivate) body.is_private = true;
    if (o.project) body.project = { key: o.project };
    if (o.description) body.description = o.description;
    if (o.forkPolicy) body.fork_policy = o.forkPolicy;
    if (o.language) body.language = o.language;
    out(await bbFetch(`${rp(o)}`, postBody(body)));
  }));

addRepoOpts(program
  .command('repo-update')
  .description('Update a repository')
  .option('--description <text>', 'New description')
  .option('--is-private', 'Make repository private')
  .option('--no-is-private', 'Make repository public')
  .option('--fork-policy <policy>', 'Fork policy')
  .option('--language <lang>', 'Language')
  .option('--project <key>', 'Project key'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.description !== undefined) body.description = o.description;
    if (o.isPrivate !== undefined) body.is_private = o.isPrivate;
    if (o.forkPolicy) body.fork_policy = o.forkPolicy;
    if (o.language) body.language = o.language;
    if (o.project) body.project = { key: o.project };
    out(await bbFetch(`${rp(o)}`, putBody(body)));
  }));

addRepoOpts(program
  .command('repo-delete')
  .description('Delete a repository (requires --confirm)')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}`, { method: 'DELETE' });
    console.log(`✅ Repository deleted`);
  }));

addPageOpts(addRepoOpts(program
  .command('repo-forks')
  .description('List repository forks')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/forks`, o)); }));

addRepoOpts(program
  .command('repo-fork-create')
  .description('Fork a repository')
  .option('--name <name>', 'Name for the fork'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.name) body.name = o.name;
    out(await bbFetch(`${rp(o)}/forks`, postBody(body)));
  }));

addPageOpts(addRepoOpts(program
  .command('repo-watchers')
  .description('List repository watchers')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/watchers`, o)); }));

// Repo webhooks
addPageOpts(addRepoOpts(program
  .command('hook-list')
  .description('List webhooks for a repository')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/hooks`, o)); }));

addRepoOpts(program
  .command('hook-get')
  .description('Get a webhook for a repository')
  .option('--uid <uid>', 'Webhook UID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/hooks/${enc(reqOpt(o, 'uid'))}`)); }));

addRepoOpts(program
  .command('hook-create')
  .description('Create a webhook for a repository')
  .option('--url <url>', 'Webhook URL')
  .option('--description <text>', 'Description')
  .option('--events <events>', 'Comma-separated event types')
  .option('--active', 'Set webhook active'))
  .action(wrap(async (o) => {
    const body = { url: reqOpt(o, 'url') };
    if (o.description) body.description = o.description;
    if (o.events) body.events = o.events.split(',').map(e => e.trim());
    if (o.active !== undefined) body.active = o.active;
    out(await bbFetch(`${rp(o)}/hooks`, postBody(body)));
  }));

addRepoOpts(program
  .command('hook-update')
  .description('Update a webhook for a repository')
  .option('--uid <uid>', 'Webhook UID')
  .option('--url <url>', 'Webhook URL')
  .option('--description <text>', 'Description')
  .option('--events <events>', 'Comma-separated event types')
  .option('--active', 'Set webhook active')
  .option('--no-active', 'Set webhook inactive'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.url) body.url = o.url;
    if (o.description) body.description = o.description;
    if (o.events) body.events = o.events.split(',').map(e => e.trim());
    if (o.active !== undefined) body.active = o.active;
    out(await bbFetch(`${rp(o)}/hooks/${enc(reqOpt(o, 'uid'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('hook-delete')
  .description('Delete a webhook for a repository (requires --confirm)')
  .option('--uid <uid>', 'Webhook UID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/hooks/${enc(reqOpt(o, 'uid'))}`, { method: 'DELETE' });
    console.log('✅ Webhook deleted');
  }));

// Override settings
addRepoOpts(program
  .command('repo-override-settings-get')
  .description('Retrieve the inheritance state for repository settings'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/override-settings`)); }));

addRepoOpts(program
  .command('repo-override-settings-update')
  .description('Set the inheritance state for repository settings')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/override-settings`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

// Repo permissions — groups
addPageOpts(addRepoOpts(program
  .command('repo-group-permission-list')
  .description('List explicit group permissions for a repository')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/permissions-config/groups`, o)); }));

addRepoOpts(program
  .command('repo-group-permission-get')
  .description('Get an explicit group permission for a repository')
  .option('--group-slug <slug>', 'Group slug'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/permissions-config/groups/${enc(reqOpt(o, 'groupSlug'))}`)); }));

addRepoOpts(program
  .command('repo-group-permission-update')
  .description('Update an explicit group permission for a repository')
  .option('--group-slug <slug>', 'Group slug')
  .option('--permission <perm>', 'Permission (read, write, admin)'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/permissions-config/groups/${enc(reqOpt(o, 'groupSlug'))}`, putBody({ permission: reqOpt(o, 'permission') })));
  }));

addRepoOpts(program
  .command('repo-group-permission-delete')
  .description('Delete an explicit group permission for a repository (requires --confirm)')
  .option('--group-slug <slug>', 'Group slug')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/permissions-config/groups/${enc(reqOpt(o, 'groupSlug'))}`, { method: 'DELETE' });
    console.log('✅ Group permission deleted');
  }));

// Repo permissions — users
addPageOpts(addRepoOpts(program
  .command('repo-user-permission-list')
  .description('List explicit user permissions for a repository')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/permissions-config/users`, o)); }));

addRepoOpts(program
  .command('repo-user-permission-get')
  .description('Get an explicit user permission for a repository')
  .option('--selected-user-id <id>', 'User ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/permissions-config/users/${enc(reqOpt(o, 'selectedUserId'))}`)); }));

addRepoOpts(program
  .command('repo-user-permission-update')
  .description('Update an explicit user permission for a repository')
  .option('--selected-user-id <id>', 'User ID')
  .option('--permission <perm>', 'Permission (read, write, admin)'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/permissions-config/users/${enc(reqOpt(o, 'selectedUserId'))}`, putBody({ permission: reqOpt(o, 'permission') })));
  }));

addRepoOpts(program
  .command('repo-user-permission-delete')
  .description('Delete an explicit user permission for a repository (requires --confirm)')
  .option('--selected-user-id <id>', 'User ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/permissions-config/users/${enc(reqOpt(o, 'selectedUserId'))}`, { method: 'DELETE' });
    console.log('✅ User permission deleted');
  }));

// User repo permissions
addPageOpts(program
  .command('user-repo-permissions')
  .description('List repository permissions for the current user'))
  .action(wrap(async (o) => { out(await fetchAllPages('/user/permissions/repositories', o)); }));

addPageOpts(addWsOpts(program
  .command('user-ws-repo-permissions')
  .description('List repository permissions in a workspace for the current user')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/user/workspaces/${enc(getWs(o))}/permissions/repositories`, o)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 2. PULL REQUESTS (36 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addFilterOpts(addRepoOpts(program
  .command('pr-list')
  .description('List pull requests')
  .option('--state <state>', 'State filter (OPEN, MERGED, DECLINED, SUPERSEDED)'))))
  .action(wrap(async (o) => {
    const extra = {};
    if (o.state) extra.state = o.state;
    out(await fetchAllPages(`${rp(o)}/pullrequests`, o, extra));
  }));

addRepoOpts(program
  .command('pr-create')
  .description('Create a pull request')
  .option('--title <title>', 'PR title')
  .option('--source <branch>', 'Source branch')
  .option('--destination <branch>', 'Destination branch')
  .option('--description <text>', 'PR description')
  .option('--close-source-branch', 'Close source branch on merge')
  .option('--reviewers <uuids>', 'Comma-separated reviewer UUIDs'))
  .action(wrap(async (o) => {
    const body = {
      title: reqOpt(o, 'title'),
      source: { branch: { name: reqOpt(o, 'source') } },
    };
    if (o.destination) body.destination = { branch: { name: o.destination } };
    if (o.description) body.description = o.description;
    if (o.closeSourceBranch) body.close_source_branch = true;
    if (o.reviewers) body.reviewers = o.reviewers.split(',').map(u => ({ uuid: u.trim() }));
    out(await bbFetch(`${rp(o)}/pullrequests`, postBody(body)));
  }));

addRepoOpts(program
  .command('pr-get')
  .description('Get a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}`)); }));

addRepoOpts(program
  .command('pr-update')
  .description('Update a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--title <title>', 'New title')
  .option('--description <text>', 'New description')
  .option('--destination <branch>', 'Destination branch')
  .option('--reviewers <uuids>', 'Comma-separated reviewer UUIDs'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.title) body.title = o.title;
    if (o.description) body.description = o.description;
    if (o.destination) body.destination = { branch: { name: o.destination } };
    if (o.reviewers) body.reviewers = o.reviewers.split(',').map(u => ({ uuid: u.trim() }));
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}`, putBody(body)));
  }));

addPageOpts(addRepoOpts(program
  .command('pr-activity')
  .description('List a pull request activity log')
  .option('--pr-id <id>', 'Pull request ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/activity`, o)); }));

addRepoOpts(program
  .command('pr-approve')
  .description('Approve a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/approve`, { method: 'POST' }));
  }));

addRepoOpts(program
  .command('pr-unapprove')
  .description('Unapprove a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/approve`, { method: 'DELETE' });
    console.log('✅ Approval removed');
  }));

// PR comments
addPageOpts(addRepoOpts(program
  .command('pr-comments')
  .description('List comments on a pull request')
  .option('--pr-id <id>', 'Pull request ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments`, o)); }));

addRepoOpts(program
  .command('pr-comment-create')
  .description('Create a comment on a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--body <text>', 'Comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments`, postBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addRepoOpts(program
  .command('pr-comment-get')
  .description('Get a comment on a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--comment-id <id>', 'Comment ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments/${enc(reqOpt(o, 'commentId'))}`)); }));

addRepoOpts(program
  .command('pr-comment-update')
  .description('Update a comment on a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--comment-id <id>', 'Comment ID')
  .option('--body <text>', 'New comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments/${enc(reqOpt(o, 'commentId'))}`, putBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addRepoOpts(program
  .command('pr-comment-delete')
  .description('Delete a comment on a pull request (requires --confirm)')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--comment-id <id>', 'Comment ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments/${enc(reqOpt(o, 'commentId'))}`, { method: 'DELETE' });
    console.log('✅ Comment deleted');
  }));

addRepoOpts(program
  .command('pr-comment-resolve')
  .description('Resolve a comment thread')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--comment-id <id>', 'Comment ID'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments/${enc(reqOpt(o, 'commentId'))}/resolve`, { method: 'POST' }));
  }));

addRepoOpts(program
  .command('pr-comment-reopen')
  .description('Reopen a comment thread')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--comment-id <id>', 'Comment ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/comments/${enc(reqOpt(o, 'commentId'))}/resolve`, { method: 'DELETE' });
    console.log('✅ Comment thread reopened');
  }));

// PR commits, diff, merge, decline
addPageOpts(addRepoOpts(program
  .command('pr-commits')
  .description('List commits on a pull request')
  .option('--pr-id <id>', 'Pull request ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/commits`, o)); }));

addRepoOpts(program
  .command('pr-decline')
  .description('Decline a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/decline`, { method: 'POST' }));
  }));

addRepoOpts(program
  .command('pr-diff')
  .description('List changes in a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/diff`)); }));

addPageOpts(addRepoOpts(program
  .command('pr-diffstat')
  .description('Get the diff stat for a pull request')
  .option('--pr-id <id>', 'Pull request ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/diffstat`, o)); }));

addRepoOpts(program
  .command('pr-merge')
  .description('Merge a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--merge-strategy <strategy>', 'Merge strategy (merge_commit, squash, fast_forward)')
  .option('--close-source-branch', 'Close source branch')
  .option('--message <msg>', 'Merge commit message'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.mergeStrategy) body.merge_strategy = o.mergeStrategy;
    if (o.closeSourceBranch) body.close_source_branch = true;
    if (o.message) body.message = o.message;
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/merge`, postBody(body)));
  }));

addRepoOpts(program
  .command('pr-merge-task-status')
  .description('Get the merge task status for a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--task-id <id>', 'Task ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/merge/task-status/${enc(reqOpt(o, 'taskId'))}`)); }));

addRepoOpts(program
  .command('pr-patch')
  .description('Get the patch for a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/patch`)); }));

addRepoOpts(program
  .command('pr-request-changes')
  .description('Request changes for a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/request-changes`, { method: 'POST' }));
  }));

addRepoOpts(program
  .command('pr-unrequest-changes')
  .description('Remove change request for a pull request')
  .option('--pr-id <id>', 'Pull request ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/request-changes`, { method: 'DELETE' });
    console.log('✅ Change request removed');
  }));

addPageOpts(addRepoOpts(program
  .command('pr-statuses')
  .description('List commit statuses for a pull request')
  .option('--pr-id <id>', 'Pull request ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/statuses`, o)); }));

// PR tasks
addPageOpts(addRepoOpts(program
  .command('pr-tasks')
  .description('List tasks on a pull request')
  .option('--pr-id <id>', 'Pull request ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/tasks`, o)); }));

addRepoOpts(program
  .command('pr-task-create')
  .description('Create a task on a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--content <text>', 'Task content'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/tasks`, postBody({ content: { raw: reqOpt(o, 'content') } })));
  }));

addRepoOpts(program
  .command('pr-task-get')
  .description('Get a task on a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--task-id <id>', 'Task ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/tasks/${enc(reqOpt(o, 'taskId'))}`)); }));

addRepoOpts(program
  .command('pr-task-update')
  .description('Update a task on a pull request')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--task-id <id>', 'Task ID')
  .option('--content <text>', 'New task content')
  .option('--state <state>', 'Task state (OPEN, RESOLVED)'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.content) body.content = { raw: o.content };
    if (o.state) body.state = o.state;
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/tasks/${enc(reqOpt(o, 'taskId'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('pr-task-delete')
  .description('Delete a task on a pull request (requires --confirm)')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--task-id <id>', 'Task ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/tasks/${enc(reqOpt(o, 'taskId'))}`, { method: 'DELETE' });
    console.log('✅ Task deleted');
  }));

// Default reviewers
addPageOpts(addRepoOpts(program
  .command('default-reviewer-list')
  .description('List default reviewers')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/default-reviewers`, o)); }));

addRepoOpts(program
  .command('default-reviewer-get')
  .description('Get a default reviewer')
  .option('--target-username <user>', 'Target username'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/default-reviewers/${enc(reqOpt(o, 'targetUsername'))}`)); }));

addRepoOpts(program
  .command('default-reviewer-add')
  .description('Add a user to the default reviewers')
  .option('--target-username <user>', 'Target username'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/default-reviewers/${enc(reqOpt(o, 'targetUsername'))}`, { method: 'PUT' }));
  }));

addRepoOpts(program
  .command('default-reviewer-delete')
  .description('Remove a user from the default reviewers (requires --confirm)')
  .option('--target-username <user>', 'Target username')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/default-reviewers/${enc(reqOpt(o, 'targetUsername'))}`, { method: 'DELETE' });
    console.log('✅ Default reviewer removed');
  }));

addPageOpts(addRepoOpts(program
  .command('effective-default-reviewers')
  .description('List effective default reviewers')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/effective-default-reviewers`, o)); }));

// PR for commit
addPageOpts(addRepoOpts(program
  .command('pr-for-commit')
  .description('List pull requests that contain a commit')
  .option('--commit <sha>', 'Commit SHA')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/pullrequests`, o)); }));

// PR activity (all)
addPageOpts(addRepoOpts(program
  .command('pr-activity-all')
  .description('List pull request activity log for a repository')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pullrequests/activity`, o)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 3. COMMITS (16 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addRepoOpts(program
  .command('commit-get')
  .description('Get a commit')
  .option('--commit <sha>', 'Commit SHA'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}`)); }));

addRepoOpts(program
  .command('commit-approve')
  .description('Approve a commit')
  .option('--commit <sha>', 'Commit SHA'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/approve`, { method: 'POST' }));
  }));

addRepoOpts(program
  .command('commit-unapprove')
  .description('Unapprove a commit')
  .option('--commit <sha>', 'Commit SHA'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/approve`, { method: 'DELETE' });
    console.log('✅ Commit approval removed');
  }));

// Commit comments
addPageOpts(addRepoOpts(program
  .command('commit-comments')
  .description("List a commit's comments")
  .option('--commit <sha>', 'Commit SHA')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/comments`, o)); }));

addRepoOpts(program
  .command('commit-comment-create')
  .description('Create comment for a commit')
  .option('--commit <sha>', 'Commit SHA')
  .option('--body <text>', 'Comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/comments`, postBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addRepoOpts(program
  .command('commit-comment-get')
  .description('Get a commit comment')
  .option('--commit <sha>', 'Commit SHA')
  .option('--comment-id <id>', 'Comment ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/comments/${enc(reqOpt(o, 'commentId'))}`)); }));

addRepoOpts(program
  .command('commit-comment-update')
  .description('Update a commit comment')
  .option('--commit <sha>', 'Commit SHA')
  .option('--comment-id <id>', 'Comment ID')
  .option('--body <text>', 'New comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/comments/${enc(reqOpt(o, 'commentId'))}`, putBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addRepoOpts(program
  .command('commit-comment-delete')
  .description('Delete a commit comment (requires --confirm)')
  .option('--commit <sha>', 'Commit SHA')
  .option('--comment-id <id>', 'Comment ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/comments/${enc(reqOpt(o, 'commentId'))}`, { method: 'DELETE' });
    console.log('✅ Commit comment deleted');
  }));

// Commit lists
addPageOpts(addRepoOpts(program
  .command('commit-list')
  .description('List commits')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commits`, o)); }));

addRepoOpts(program
  .command('commit-list-post')
  .description('List commits with include/exclude')
  .option('--include <refs>', 'Comma-separated refs to include')
  .option('--exclude <refs>', 'Comma-separated refs to exclude'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.include) body.include = o.include.split(',').map(r => r.trim());
    if (o.exclude) body.exclude = o.exclude.split(',').map(r => r.trim());
    out(await bbFetch(`${rp(o)}/commits`, postBody(body)));
  }));

addPageOpts(addRepoOpts(program
  .command('commit-list-revision')
  .description('List commits for revision')
  .option('--revision <rev>', 'Revision')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commits/${enc(reqOpt(o, 'revision'))}`, o)); }));

addRepoOpts(program
  .command('commit-list-revision-post')
  .description('List commits for revision using include/exclude')
  .option('--revision <rev>', 'Revision')
  .option('--include <refs>', 'Comma-separated refs to include')
  .option('--exclude <refs>', 'Comma-separated refs to exclude'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.include) body.include = o.include.split(',').map(r => r.trim());
    if (o.exclude) body.exclude = o.exclude.split(',').map(r => r.trim());
    out(await bbFetch(`${rp(o)}/commits/${enc(reqOpt(o, 'revision'))}`, postBody(body)));
  }));

// Diff, diffstat, patch, merge-base
addRepoOpts(program
  .command('diff')
  .description('Compare two commits')
  .option('--spec <spec>', 'Diff spec (e.g. branch1..branch2)'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/diff/${enc(reqOpt(o, 'spec'))}`)); }));

addPageOpts(addRepoOpts(program
  .command('diffstat')
  .description('Compare two commit diff stats')
  .option('--spec <spec>', 'Diff spec')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/diffstat/${enc(reqOpt(o, 'spec'))}`, o)); }));

addRepoOpts(program
  .command('merge-base')
  .description('Get the common ancestor between two commits')
  .option('--revspec <revspec>', 'Revision spec (e.g. branch1..branch2)'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/merge-base/${enc(reqOpt(o, 'revspec'))}`)); }));

addRepoOpts(program
  .command('patch')
  .description('Get a patch for two commits')
  .option('--spec <spec>', 'Patch spec'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/patch/${enc(reqOpt(o, 'spec'))}`)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 4. BRANCHES & TAGS — Refs (9 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addFilterOpts(addRepoOpts(program
  .command('ref-list')
  .description('List branches and tags'))))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/refs`, o)); }));

addPageOpts(addFilterOpts(addRepoOpts(program
  .command('branch-list')
  .description('List open branches'))))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/refs/branches`, o)); }));

addRepoOpts(program
  .command('branch-create')
  .description('Create a branch')
  .option('--name <name>', 'Branch name')
  .option('--target <sha>', 'Target commit SHA'))
  .action(wrap(async (o) => {
    const body = { name: reqOpt(o, 'name') };
    if (o.target) body.target = { hash: o.target };
    out(await bbFetch(`${rp(o)}/refs/branches`, postBody(body)));
  }));

addRepoOpts(program
  .command('branch-get')
  .description('Get a branch')
  .option('--name <name>', 'Branch name'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/refs/branches/${enc(reqOpt(o, 'name'))}`)); }));

addRepoOpts(program
  .command('branch-delete')
  .description('Delete a branch (requires --confirm)')
  .option('--name <name>', 'Branch name')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/refs/branches/${enc(reqOpt(o, 'name'))}`, { method: 'DELETE' });
    console.log('✅ Branch deleted');
  }));

addPageOpts(addFilterOpts(addRepoOpts(program
  .command('tag-list')
  .description('List tags'))))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/refs/tags`, o)); }));

addRepoOpts(program
  .command('tag-create')
  .description('Create a tag')
  .option('--name <name>', 'Tag name')
  .option('--target <sha>', 'Target commit SHA'))
  .action(wrap(async (o) => {
    const body = { name: reqOpt(o, 'name') };
    if (o.target) body.target = { hash: o.target };
    out(await bbFetch(`${rp(o)}/refs/tags`, postBody(body)));
  }));

addRepoOpts(program
  .command('tag-get')
  .description('Get a tag')
  .option('--name <name>', 'Tag name'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/refs/tags/${enc(reqOpt(o, 'name'))}`)); }));

addRepoOpts(program
  .command('tag-delete')
  .description('Delete a tag (requires --confirm)')
  .option('--name <name>', 'Tag name')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/refs/tags/${enc(reqOpt(o, 'name'))}`, { method: 'DELETE' });
    console.log('✅ Tag deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 5. BRANCH RESTRICTIONS (5 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addRepoOpts(program
  .command('restriction-list')
  .description('List branch restrictions')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/branch-restrictions`, o)); }));

addRepoOpts(program
  .command('restriction-get')
  .description('Get a branch restriction rule')
  .option('--restriction-id <id>', 'Restriction ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/branch-restrictions/${enc(reqOpt(o, 'restrictionId'))}`)); }));

addRepoOpts(program
  .command('restriction-create')
  .description('Create a branch restriction rule')
  .option('--kind <kind>', 'Restriction kind (e.g. push, force, delete, restrict_merges)')
  .option('--pattern <pattern>', 'Branch pattern')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { kind: reqOpt(o, 'kind'), pattern: o.pattern || '' };
    out(await bbFetch(`${rp(o)}/branch-restrictions`, postBody(body)));
  }));

addRepoOpts(program
  .command('restriction-update')
  .description('Update a branch restriction rule')
  .option('--restriction-id <id>', 'Restriction ID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/branch-restrictions/${enc(reqOpt(o, 'restrictionId'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('restriction-delete')
  .description('Delete a branch restriction rule (requires --confirm)')
  .option('--restriction-id <id>', 'Restriction ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/branch-restrictions/${enc(reqOpt(o, 'restrictionId'))}`, { method: 'DELETE' });
    console.log('✅ Branch restriction deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 6. BRANCHING MODEL (7 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addRepoOpts(program
  .command('branching-model-get')
  .description('Get the branching model for a repository'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/branching-model`)); }));

addRepoOpts(program
  .command('branching-model-settings-get')
  .description('Get the branching model config for a repository'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/branching-model/settings`)); }));

addRepoOpts(program
  .command('branching-model-settings-update')
  .description('Update the branching model config for a repository')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/branching-model/settings`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('branching-model-effective')
  .description('Get the effective branching model for a repository'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/effective-branching-model`)); }));

addWsOpts(program
  .command('project-branching-model-get')
  .description('Get the branching model for a project')
  .option('--project-key <key>', 'Project key'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/branching-model`)); }));

addWsOpts(program
  .command('project-branching-model-settings-get')
  .description('Get the branching model config for a project')
  .option('--project-key <key>', 'Project key'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/branching-model/settings`)); }));

addWsOpts(program
  .command('project-branching-model-settings-update')
  .description('Update the branching model config for a project')
  .option('--project-key <key>', 'Project key')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/branching-model/settings`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 7. PIPELINES (68 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

// Pipeline CRUD
addPageOpts(addFilterOpts(addRepoOpts(program
  .command('pipeline-list')
  .description('List pipelines'))))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines`, o)); }));

addRepoOpts(program
  .command('pipeline-get')
  .description('Get a pipeline')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}`)); }));

addRepoOpts(program
  .command('pipeline-create')
  .description('Run a pipeline')
  .option('--branch <name>', 'Branch to run on')
  .option('--data <json>', 'Full JSON body for advanced options'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { target: { ref_type: 'branch', type: 'pipeline_ref_target', ref_name: reqOpt(o, 'branch') } };
    out(await bbFetch(`${rp(o)}/pipelines`, postBody(body)));
  }));

addRepoOpts(program
  .command('pipeline-stop')
  .description('Stop a pipeline')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/stopPipeline`, { method: 'POST' });
    console.log('✅ Pipeline stopped');
  }));

// Pipeline steps
addPageOpts(addRepoOpts(program
  .command('pipeline-steps')
  .description('List steps for a pipeline')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps`, o)); }));

addRepoOpts(program
  .command('pipeline-step-get')
  .description('Get a step of a pipeline')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')
  .option('--step-uuid <uuid>', 'Step UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps/${enc(reqOpt(o, 'stepUuid'))}`)); }));

addRepoOpts(program
  .command('pipeline-step-log')
  .description('Get log file for a step')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')
  .option('--step-uuid <uuid>', 'Step UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps/${enc(reqOpt(o, 'stepUuid'))}/log`)); }));

addRepoOpts(program
  .command('pipeline-step-log-container')
  .description('Get the logs for a build/service container for a step')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')
  .option('--step-uuid <uuid>', 'Step UUID')
  .option('--log-uuid <uuid>', 'Log UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps/${enc(reqOpt(o, 'stepUuid'))}/logs/${enc(reqOpt(o, 'logUuid'))}`)); }));

// Pipeline test reports
addRepoOpts(program
  .command('pipeline-test-reports')
  .description('Get a summary of test reports for a step')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')
  .option('--step-uuid <uuid>', 'Step UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps/${enc(reqOpt(o, 'stepUuid'))}/test_reports`)); }));

addPageOpts(addRepoOpts(program
  .command('pipeline-test-cases')
  .description('Get test cases for a step')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')
  .option('--step-uuid <uuid>', 'Step UUID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps/${enc(reqOpt(o, 'stepUuid'))}/test_reports/test_cases`, o)); }));

addRepoOpts(program
  .command('pipeline-test-case-reasons')
  .description('Get test case reasons for a test case')
  .option('--pipeline-uuid <uuid>', 'Pipeline UUID')
  .option('--step-uuid <uuid>', 'Step UUID')
  .option('--test-case-uuid <uuid>', 'Test case UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines/${enc(reqOpt(o, 'pipelineUuid'))}/steps/${enc(reqOpt(o, 'stepUuid'))}/test_reports/test_cases/${enc(reqOpt(o, 'testCaseUuid'))}/test_case_reasons`)); }));

// Pipeline config
addRepoOpts(program
  .command('pipeline-config-get')
  .description('Get pipeline configuration'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines_config`)); }));

addRepoOpts(program
  .command('pipeline-config-update')
  .description('Update pipeline configuration')
  .option('--enabled', 'Enable pipelines')
  .option('--no-enabled', 'Disable pipelines')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { enabled: o.enabled !== false };
    out(await bbFetch(`${rp(o)}/pipelines_config`, putBody(body)));
  }));

addRepoOpts(program
  .command('pipeline-build-number-update')
  .description('Update the next build number')
  .option('--next <number>', 'Next build number'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pipelines_config/build_number`, putBody({ next: parseInt(reqOpt(o, 'next'), 10) })));
  }));

// Pipeline variables (repo-level)
addPageOpts(addRepoOpts(program
  .command('pipeline-var-list')
  .description('List variables for a repository')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines_config/variables`, o)); }));

addRepoOpts(program
  .command('pipeline-var-get')
  .description('Get a variable for a repository')
  .option('--variable-uuid <uuid>', 'Variable UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`)); }));

addRepoOpts(program
  .command('pipeline-var-create')
  .description('Create a variable for a repository')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured'))
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key'), value: reqOpt(o, 'value') };
    if (o.secured) body.secured = true;
    out(await bbFetch(`${rp(o)}/pipelines_config/variables`, postBody(body)));
  }));

addRepoOpts(program
  .command('pipeline-var-update')
  .description('Update a variable for a repository')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.key) body.key = o.key;
    if (o.value) body.value = o.value;
    if (o.secured !== undefined) body.secured = o.secured;
    out(await bbFetch(`${rp(o)}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('pipeline-var-delete')
  .description('Delete a variable for a repository (requires --confirm)')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`, { method: 'DELETE' });
    console.log('✅ Pipeline variable deleted');
  }));

// Pipeline schedules
addPageOpts(addRepoOpts(program
  .command('pipeline-schedule-list')
  .description('List schedules')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines_config/schedules`, o)); }));

addRepoOpts(program
  .command('pipeline-schedule-get')
  .description('Get a schedule')
  .option('--schedule-uuid <uuid>', 'Schedule UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines_config/schedules/${enc(reqOpt(o, 'scheduleUuid'))}`)); }));

addRepoOpts(program
  .command('pipeline-schedule-create')
  .description('Create a schedule')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pipelines_config/schedules`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('pipeline-schedule-update')
  .description('Update a schedule')
  .option('--schedule-uuid <uuid>', 'Schedule UUID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pipelines_config/schedules/${enc(reqOpt(o, 'scheduleUuid'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('pipeline-schedule-delete')
  .description('Delete a schedule (requires --confirm)')
  .option('--schedule-uuid <uuid>', 'Schedule UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines_config/schedules/${enc(reqOpt(o, 'scheduleUuid'))}`, { method: 'DELETE' });
    console.log('✅ Pipeline schedule deleted');
  }));

addPageOpts(addRepoOpts(program
  .command('pipeline-schedule-executions')
  .description('List executions of a schedule')
  .option('--schedule-uuid <uuid>', 'Schedule UUID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines_config/schedules/${enc(reqOpt(o, 'scheduleUuid'))}/executions`, o)); }));

// Pipeline SSH key pair
addRepoOpts(program
  .command('pipeline-ssh-keypair-get')
  .description('Get SSH key pair'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines_config/ssh/key_pair`)); }));

addRepoOpts(program
  .command('pipeline-ssh-keypair-update')
  .description('Update SSH key pair')
  .option('--private-key <key>', 'Private key')
  .option('--public-key <key>', 'Public key')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { private_key: reqOpt(o, 'privateKey'), public_key: reqOpt(o, 'publicKey') };
    out(await bbFetch(`${rp(o)}/pipelines_config/ssh/key_pair`, putBody(body)));
  }));

addRepoOpts(program
  .command('pipeline-ssh-keypair-delete')
  .description('Delete SSH key pair (requires --confirm)')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines_config/ssh/key_pair`, { method: 'DELETE' });
    console.log('✅ SSH key pair deleted');
  }));

// Pipeline known hosts
addPageOpts(addRepoOpts(program
  .command('pipeline-known-host-list')
  .description('List known hosts')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines_config/ssh/known_hosts`, o)); }));

addRepoOpts(program
  .command('pipeline-known-host-get')
  .description('Get a known host')
  .option('--known-host-uuid <uuid>', 'Known host UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines_config/ssh/known_hosts/${enc(reqOpt(o, 'knownHostUuid'))}`)); }));

addRepoOpts(program
  .command('pipeline-known-host-create')
  .description('Create a known host')
  .option('--hostname <host>', 'Hostname')
  .option('--public-key <key>', 'Public key')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { hostname: reqOpt(o, 'hostname') };
    if (o.publicKey && !o.data) body.public_key = { key: o.publicKey };
    out(await bbFetch(`${rp(o)}/pipelines_config/ssh/known_hosts`, postBody(body)));
  }));

addRepoOpts(program
  .command('pipeline-known-host-update')
  .description('Update a known host')
  .option('--known-host-uuid <uuid>', 'Known host UUID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pipelines_config/ssh/known_hosts/${enc(reqOpt(o, 'knownHostUuid'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('pipeline-known-host-delete')
  .description('Delete a known host (requires --confirm)')
  .option('--known-host-uuid <uuid>', 'Known host UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines_config/ssh/known_hosts/${enc(reqOpt(o, 'knownHostUuid'))}`, { method: 'DELETE' });
    console.log('✅ Known host deleted');
  }));

// Pipeline caches
addPageOpts(addRepoOpts(program
  .command('pipeline-cache-list')
  .description('List caches')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines-config/caches`, o)); }));

addRepoOpts(program
  .command('pipeline-cache-delete')
  .description('Delete caches (requires --confirm)')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines-config/caches`, { method: 'DELETE' });
    console.log('✅ Caches deleted');
  }));

addRepoOpts(program
  .command('pipeline-cache-delete-by-name')
  .description('Delete a cache (requires --confirm)')
  .option('--cache-uuid <uuid>', 'Cache UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines-config/caches/${enc(reqOpt(o, 'cacheUuid'))}`, { method: 'DELETE' });
    console.log('✅ Cache deleted');
  }));

addRepoOpts(program
  .command('pipeline-cache-content-uri')
  .description('Get cache content URI')
  .option('--cache-uuid <uuid>', 'Cache UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines-config/caches/${enc(reqOpt(o, 'cacheUuid'))}/content-uri`)); }));

// Pipeline runners (repo-level)
addPageOpts(addRepoOpts(program
  .command('pipeline-runner-list')
  .description('Get repository runners')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/pipelines-config/runners`, o)); }));

addRepoOpts(program
  .command('pipeline-runner-get')
  .description('Get repository runner')
  .option('--runner-uuid <uuid>', 'Runner UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pipelines-config/runners/${enc(reqOpt(o, 'runnerUuid'))}`)); }));

addRepoOpts(program
  .command('pipeline-runner-create')
  .description('Create repository runner')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pipelines-config/runners`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('pipeline-runner-update')
  .description('Update repository runner')
  .option('--runner-uuid <uuid>', 'Runner UUID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pipelines-config/runners/${enc(reqOpt(o, 'runnerUuid'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('pipeline-runner-delete')
  .description('Delete repository runner (requires --confirm)')
  .option('--runner-uuid <uuid>', 'Runner UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pipelines-config/runners/${enc(reqOpt(o, 'runnerUuid'))}`, { method: 'DELETE' });
    console.log('✅ Runner deleted');
  }));

// Environment (deployment) variables
addPageOpts(addRepoOpts(program
  .command('env-var-list')
  .description('List variables for an environment')
  .option('--environment-uuid <uuid>', 'Environment UUID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/deployments_config/environments/${enc(reqOpt(o, 'environmentUuid'))}/variables`, o)); }));

addRepoOpts(program
  .command('env-var-create')
  .description('Create a variable for an environment')
  .option('--environment-uuid <uuid>', 'Environment UUID')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured'))
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key'), value: reqOpt(o, 'value') };
    if (o.secured) body.secured = true;
    out(await bbFetch(`${rp(o)}/deployments_config/environments/${enc(reqOpt(o, 'environmentUuid'))}/variables`, postBody(body)));
  }));

addRepoOpts(program
  .command('env-var-update')
  .description('Update a variable for an environment')
  .option('--environment-uuid <uuid>', 'Environment UUID')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.key) body.key = o.key;
    if (o.value) body.value = o.value;
    if (o.secured !== undefined) body.secured = o.secured;
    out(await bbFetch(`${rp(o)}/deployments_config/environments/${enc(reqOpt(o, 'environmentUuid'))}/variables/${enc(reqOpt(o, 'variableUuid'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('env-var-delete')
  .description('Delete a variable for an environment (requires --confirm)')
  .option('--environment-uuid <uuid>', 'Environment UUID')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/deployments_config/environments/${enc(reqOpt(o, 'environmentUuid'))}/variables/${enc(reqOpt(o, 'variableUuid'))}`, { method: 'DELETE' });
    console.log('✅ Environment variable deleted');
  }));

// Team pipeline variables (deprecated)
addPageOpts(program
  .command('team-pipeline-var-list')
  .description('List variables for a team (deprecated)')
  .option('--username <name>', 'Team username'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/teams/${enc(reqOpt(o, 'username'))}/pipelines_config/variables`, o)); }));

program
  .command('team-pipeline-var-get')
  .description('Get a variable for a team (deprecated)')
  .option('--username <name>', 'Team username')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .action(wrap(async (o) => { out(await bbFetch(`/teams/${enc(reqOpt(o, 'username'))}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`)); }));

program
  .command('team-pipeline-var-create')
  .description('Create a variable for a team (deprecated)')
  .option('--username <name>', 'Team username')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured')
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key'), value: reqOpt(o, 'value') };
    if (o.secured) body.secured = true;
    out(await bbFetch(`/teams/${enc(reqOpt(o, 'username'))}/pipelines_config/variables`, postBody(body)));
  }));

program
  .command('team-pipeline-var-update')
  .description('Update a variable for a team (deprecated)')
  .option('--username <name>', 'Team username')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured')
  .action(wrap(async (o) => {
    const body = {};
    if (o.key) body.key = o.key;
    if (o.value) body.value = o.value;
    if (o.secured !== undefined) body.secured = o.secured;
    out(await bbFetch(`/teams/${enc(reqOpt(o, 'username'))}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`, putBody(body)));
  }));

program
  .command('team-pipeline-var-delete')
  .description('Delete a variable for a team (deprecated, requires --confirm)')
  .option('--username <name>', 'Team username')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/teams/${enc(reqOpt(o, 'username'))}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`, { method: 'DELETE' });
    console.log('✅ Team variable deleted');
  }));

// User pipeline variables
addPageOpts(program
  .command('user-pipeline-var-list')
  .description('List variables for a user')
  .option('--selected-user <user>', 'Username'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/users/${enc(reqOpt(o, 'selectedUser'))}/pipelines_config/variables`, o)); }));

program
  .command('user-pipeline-var-get')
  .description('Get a variable for a user')
  .option('--selected-user <user>', 'Username')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .action(wrap(async (o) => { out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`)); }));

program
  .command('user-pipeline-var-create')
  .description('Create a variable for a user')
  .option('--selected-user <user>', 'Username')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured')
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key'), value: reqOpt(o, 'value') };
    if (o.secured) body.secured = true;
    out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/pipelines_config/variables`, postBody(body)));
  }));

program
  .command('user-pipeline-var-update')
  .description('Update a variable for a user')
  .option('--selected-user <user>', 'Username')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured')
  .action(wrap(async (o) => {
    const body = {};
    if (o.key) body.key = o.key;
    if (o.value) body.value = o.value;
    if (o.secured !== undefined) body.secured = o.secured;
    out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`, putBody(body)));
  }));

program
  .command('user-pipeline-var-delete')
  .description('Delete a variable for a user (requires --confirm)')
  .option('--selected-user <user>', 'Username')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/pipelines_config/variables/${enc(reqOpt(o, 'variableUuid'))}`, { method: 'DELETE' });
    console.log('✅ User variable deleted');
  }));

// Workspace OIDC
addWsOpts(program
  .command('ws-oidc-config')
  .description('Get OpenID configuration for OIDC in Pipelines'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/identity/oidc/.well-known/openid-configuration`)); }));

addWsOpts(program
  .command('ws-oidc-keys')
  .description('Get keys for OIDC in Pipelines'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/identity/oidc/keys.json`)); }));

// Workspace runners
addPageOpts(addWsOpts(program
  .command('ws-runner-list')
  .description('Get workspace runners')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/pipelines-config/runners`, o)); }));

addWsOpts(program
  .command('ws-runner-get')
  .description('Get workspace runner')
  .option('--runner-uuid <uuid>', 'Runner UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/runners/${enc(reqOpt(o, 'runnerUuid'))}`)); }));

addWsOpts(program
  .command('ws-runner-create')
  .description('Create workspace runner')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/runners`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addWsOpts(program
  .command('ws-runner-update')
  .description('Update workspace runner')
  .option('--runner-uuid <uuid>', 'Runner UUID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/runners/${enc(reqOpt(o, 'runnerUuid'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addWsOpts(program
  .command('ws-runner-delete')
  .description('Delete workspace runner (requires --confirm)')
  .option('--runner-uuid <uuid>', 'Runner UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/runners/${enc(reqOpt(o, 'runnerUuid'))}`, { method: 'DELETE' });
    console.log('✅ Workspace runner deleted');
  }));

// Workspace pipeline variables
addPageOpts(addWsOpts(program
  .command('ws-pipeline-var-list')
  .description('List variables for a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/pipelines-config/variables`, o)); }));

addWsOpts(program
  .command('ws-pipeline-var-get')
  .description('Get variable for a workspace')
  .option('--variable-uuid <uuid>', 'Variable UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/variables/${enc(reqOpt(o, 'variableUuid'))}`)); }));

addWsOpts(program
  .command('ws-pipeline-var-create')
  .description('Create a variable for a workspace')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured'))
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key'), value: reqOpt(o, 'value') };
    if (o.secured) body.secured = true;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/variables`, postBody(body)));
  }));

addWsOpts(program
  .command('ws-pipeline-var-update')
  .description('Update variable for a workspace')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--key <key>', 'Variable key')
  .option('--value <value>', 'Variable value')
  .option('--secured', 'Mark as secured'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.key) body.key = o.key;
    if (o.value) body.value = o.value;
    if (o.secured !== undefined) body.secured = o.secured;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/variables/${enc(reqOpt(o, 'variableUuid'))}`, putBody(body)));
  }));

addWsOpts(program
  .command('ws-pipeline-var-delete')
  .description('Delete a variable for a workspace (requires --confirm)')
  .option('--variable-uuid <uuid>', 'Variable UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/pipelines-config/variables/${enc(reqOpt(o, 'variableUuid'))}`, { method: 'DELETE' });
    console.log('✅ Workspace variable deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 8. DEPLOYMENTS (16 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

// Deploy keys
addPageOpts(addRepoOpts(program
  .command('deploy-key-list')
  .description('List repository deploy keys')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/deploy-keys`, o)); }));

addRepoOpts(program
  .command('deploy-key-get')
  .description('Get a repository deploy key')
  .option('--key-id <id>', 'Key ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/deploy-keys/${enc(reqOpt(o, 'keyId'))}`)); }));

addRepoOpts(program
  .command('deploy-key-create')
  .description('Add a repository deploy key')
  .option('--key <key>', 'SSH public key')
  .option('--label <label>', 'Key label'))
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key') };
    if (o.label) body.label = o.label;
    out(await bbFetch(`${rp(o)}/deploy-keys`, postBody(body)));
  }));

addRepoOpts(program
  .command('deploy-key-update')
  .description('Update a repository deploy key')
  .option('--key-id <id>', 'Key ID')
  .option('--label <label>', 'New label')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : {};
    if (o.label && !o.data) body.label = o.label;
    out(await bbFetch(`${rp(o)}/deploy-keys/${enc(reqOpt(o, 'keyId'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('deploy-key-delete')
  .description('Delete a repository deploy key (requires --confirm)')
  .option('--key-id <id>', 'Key ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/deploy-keys/${enc(reqOpt(o, 'keyId'))}`, { method: 'DELETE' });
    console.log('✅ Deploy key deleted');
  }));

// Deployments
addPageOpts(addRepoOpts(program
  .command('deployment-list')
  .description('List deployments')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/deployments`, o)); }));

addRepoOpts(program
  .command('deployment-get')
  .description('Get a deployment')
  .option('--deployment-uuid <uuid>', 'Deployment UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/deployments/${enc(reqOpt(o, 'deploymentUuid'))}`)); }));

// Environments
addPageOpts(addRepoOpts(program
  .command('environment-list')
  .description('List environments')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/environments`, o)); }));

addRepoOpts(program
  .command('environment-get')
  .description('Get an environment')
  .option('--environment-uuid <uuid>', 'Environment UUID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/environments/${enc(reqOpt(o, 'environmentUuid'))}`)); }));

addRepoOpts(program
  .command('environment-create')
  .description('Create an environment')
  .option('--name <name>', 'Environment name')
  .option('--environment-type <type>', 'Type (Test, Staging, Production)')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { name: reqOpt(o, 'name') };
    if (o.environmentType && !o.data) body.environment_type = { name: o.environmentType };
    out(await bbFetch(`${rp(o)}/environments`, postBody(body)));
  }));

addRepoOpts(program
  .command('environment-update')
  .description('Update an environment')
  .option('--environment-uuid <uuid>', 'Environment UUID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/environments/${enc(reqOpt(o, 'environmentUuid'))}/changes`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('environment-delete')
  .description('Delete an environment (requires --confirm)')
  .option('--environment-uuid <uuid>', 'Environment UUID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/environments/${enc(reqOpt(o, 'environmentUuid'))}`, { method: 'DELETE' });
    console.log('✅ Environment deleted');
  }));

// Project deploy keys
addPageOpts(addWsOpts(program
  .command('project-deploy-key-list')
  .description('List project deploy keys')
  .option('--project-key <key>', 'Project key')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/deploy-keys`, o)); }));

addWsOpts(program
  .command('project-deploy-key-get')
  .description('Get a project deploy key')
  .option('--project-key <key>', 'Project key')
  .option('--key-id <id>', 'Key ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/deploy-keys/${enc(reqOpt(o, 'keyId'))}`)); }));

addWsOpts(program
  .command('project-deploy-key-create')
  .description('Create a project deploy key')
  .option('--project-key <key>', 'Project key')
  .option('--key <sshkey>', 'SSH public key')
  .option('--label <label>', 'Key label'))
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key') };
    if (o.label) body.label = o.label;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/deploy-keys`, postBody(body)));
  }));

addWsOpts(program
  .command('project-deploy-key-delete')
  .description('Delete a project deploy key (requires --confirm)')
  .option('--project-key <key>', 'Project key')
  .option('--key-id <id>', 'Key ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/deploy-keys/${enc(reqOpt(o, 'keyId'))}`, { method: 'DELETE' });
    console.log('✅ Project deploy key deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 9. COMMIT STATUSES (4 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addRepoOpts(program
  .command('status-list')
  .description('List commit statuses for a commit')
  .option('--commit <sha>', 'Commit SHA')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/statuses`, o)); }));

addRepoOpts(program
  .command('status-create')
  .description('Create a build status for a commit')
  .option('--commit <sha>', 'Commit SHA')
  .option('--state <state>', 'State (SUCCESSFUL, FAILED, INPROGRESS, STOPPED)')
  .option('--key <key>', 'Build key')
  .option('--url <url>', 'Build URL')
  .option('--name <name>', 'Build name')
  .option('--description <text>', 'Description'))
  .action(wrap(async (o) => {
    const body = { state: reqOpt(o, 'state'), key: reqOpt(o, 'key') };
    if (o.url) body.url = o.url;
    if (o.name) body.name = o.name;
    if (o.description) body.description = o.description;
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/statuses/build`, postBody(body)));
  }));

addRepoOpts(program
  .command('status-get')
  .description('Get a build status for a commit')
  .option('--commit <sha>', 'Commit SHA')
  .option('--key <key>', 'Build key'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/statuses/build/${enc(reqOpt(o, 'key'))}`)); }));

addRepoOpts(program
  .command('status-update')
  .description('Update a build status for a commit')
  .option('--commit <sha>', 'Commit SHA')
  .option('--key <key>', 'Build key')
  .option('--state <state>', 'State')
  .option('--url <url>', 'Build URL')
  .option('--name <name>', 'Build name')
  .option('--description <text>', 'Description'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.state) body.state = o.state;
    if (o.url) body.url = o.url;
    if (o.name) body.name = o.name;
    if (o.description) body.description = o.description;
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/statuses/build/${enc(reqOpt(o, 'key'))}`, putBody(body)));
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 10. ISSUE TRACKER (33 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addFilterOpts(addRepoOpts(program
  .command('issue-list')
  .description('List issues'))))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/issues`, o)); }));

addRepoOpts(program
  .command('issue-get')
  .description('Get an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}`)); }));

addRepoOpts(program
  .command('issue-create')
  .description('Create an issue')
  .option('--title <title>', 'Issue title')
  .option('--content <text>', 'Issue content (markdown)')
  .option('--kind <kind>', 'Kind (bug, enhancement, proposal, task)')
  .option('--priority <p>', 'Priority (trivial, minor, major, critical, blocker)'))
  .action(wrap(async (o) => {
    const body = { title: reqOpt(o, 'title') };
    if (o.content) body.content = { raw: o.content };
    if (o.kind) body.kind = o.kind;
    if (o.priority) body.priority = o.priority;
    out(await bbFetch(`${rp(o)}/issues`, postBody(body)));
  }));

addRepoOpts(program
  .command('issue-update')
  .description('Update an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--title <title>', 'New title')
  .option('--content <text>', 'New content')
  .option('--kind <kind>', 'Kind')
  .option('--priority <p>', 'Priority')
  .option('--state <state>', 'State (new, open, resolved, on hold, invalid, duplicate, wontfix, closed)'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.title) body.title = o.title;
    if (o.content) body.content = { raw: o.content };
    if (o.kind) body.kind = o.kind;
    if (o.priority) body.priority = o.priority;
    if (o.state) body.state = o.state;
    out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('issue-delete')
  .description('Delete an issue (requires --confirm)')
  .option('--issue-id <id>', 'Issue ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}`, { method: 'DELETE' });
    console.log('✅ Issue deleted');
  }));

// Issue comments
addPageOpts(addRepoOpts(program
  .command('issue-comment-list')
  .description('List comments on an issue')
  .option('--issue-id <id>', 'Issue ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/comments`, o)); }));

addRepoOpts(program
  .command('issue-comment-get')
  .description('Get a comment on an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--comment-id <id>', 'Comment ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/comments/${enc(reqOpt(o, 'commentId'))}`)); }));

addRepoOpts(program
  .command('issue-comment-create')
  .description('Create a comment on an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--body <text>', 'Comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/comments`, postBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addRepoOpts(program
  .command('issue-comment-update')
  .description('Update a comment on an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--comment-id <id>', 'Comment ID')
  .option('--body <text>', 'New comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/comments/${enc(reqOpt(o, 'commentId'))}`, putBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addRepoOpts(program
  .command('issue-comment-delete')
  .description('Delete a comment on an issue (requires --confirm)')
  .option('--issue-id <id>', 'Issue ID')
  .option('--comment-id <id>', 'Comment ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/comments/${enc(reqOpt(o, 'commentId'))}`, { method: 'DELETE' });
    console.log('✅ Issue comment deleted');
  }));

// Issue attachments
addPageOpts(addRepoOpts(program
  .command('issue-attachment-list')
  .description('List attachments for an issue')
  .option('--issue-id <id>', 'Issue ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/attachments`, o)); }));

addRepoOpts(program
  .command('issue-attachment-get')
  .description('Get attachment for an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--path <path>', 'Attachment path'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/attachments/${safePath(reqOpt(o, 'path'))}`)); }));

addRepoOpts(program
  .command('issue-attachment-upload')
  .description('Upload an attachment to an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--file <path>', 'Local file path'))
  .action(wrap(async (o) => {
    const filePath = resolve(safePath(reqOpt(o, 'file')) || reqOpt(o, 'file'));
    checkFileSize(filePath);
    const fileContent = readFileSync(filePath);
    const fileName = basename(filePath);
    const form = new FormData();
    form.append('files', new Blob([fileContent]), fileName);
    out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/attachments`, { method: 'POST', body: form, rawBody: true }));
  }));

addRepoOpts(program
  .command('issue-attachment-delete')
  .description('Delete an attachment for an issue (requires --confirm)')
  .option('--issue-id <id>', 'Issue ID')
  .option('--path <path>', 'Attachment path')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/attachments/${safePath(reqOpt(o, 'path'))}`, { method: 'DELETE' });
    console.log('✅ Issue attachment deleted');
  }));

// Issue changes
addPageOpts(addRepoOpts(program
  .command('issue-change-list')
  .description('List changes on an issue')
  .option('--issue-id <id>', 'Issue ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/changes`, o)); }));

addRepoOpts(program
  .command('issue-change-get')
  .description('Get issue change object')
  .option('--issue-id <id>', 'Issue ID')
  .option('--change-id <id>', 'Change ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/changes/${enc(reqOpt(o, 'changeId'))}`)); }));

addRepoOpts(program
  .command('issue-change-create')
  .description('Modify the state of an issue')
  .option('--issue-id <id>', 'Issue ID')
  .option('--data <json>', 'JSON body with changes'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/changes`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

// Issue vote
addRepoOpts(program
  .command('issue-vote-check')
  .description('Check if current user voted for an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/vote`)); }));

addRepoOpts(program
  .command('issue-vote')
  .description('Vote for an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/vote`, { method: 'PUT' });
    console.log('✅ Voted');
  }));

addRepoOpts(program
  .command('issue-unvote')
  .description('Remove vote for an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/vote`, { method: 'DELETE' });
    console.log('✅ Vote removed');
  }));

// Issue watch
addRepoOpts(program
  .command('issue-watch-check')
  .description('Check if current user is watching an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/watch`)); }));

addRepoOpts(program
  .command('issue-watch')
  .description('Watch an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/watch`, { method: 'PUT' });
    console.log('✅ Watching issue');
  }));

addRepoOpts(program
  .command('issue-unwatch')
  .description('Stop watching an issue')
  .option('--issue-id <id>', 'Issue ID'))
  .action(wrap(async (o) => {
    await bbFetch(`${rp(o)}/issues/${enc(reqOpt(o, 'issueId'))}/watch`, { method: 'DELETE' });
    console.log('✅ Stopped watching');
  }));

// Issue export/import
addRepoOpts(program
  .command('issue-export')
  .description('Export issues'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/issues/export`, { method: 'POST' }));
  }));

addRepoOpts(program
  .command('issue-export-status')
  .description('Check issue export status')
  .option('--repo-name <name>', 'Repository name')
  .option('--task-id <id>', 'Export task ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/export/${enc(reqOpt(o, 'repoName'))}-issues-${enc(reqOpt(o, 'taskId'))}.zip`)); }));

addRepoOpts(program
  .command('issue-import')
  .description('Import issues')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/issues/import`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('issue-import-status')
  .description('Check issue import status'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/issues/import`)); }));

// Components
addPageOpts(addRepoOpts(program
  .command('component-list')
  .description('List components')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/components`, o)); }));

addRepoOpts(program
  .command('component-get')
  .description('Get a component for issues')
  .option('--component-id <id>', 'Component ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/components/${enc(reqOpt(o, 'componentId'))}`)); }));

// Milestones
addPageOpts(addRepoOpts(program
  .command('milestone-list')
  .description('List milestones')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/milestones`, o)); }));

addRepoOpts(program
  .command('milestone-get')
  .description('Get a milestone')
  .option('--milestone-id <id>', 'Milestone ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/milestones/${enc(reqOpt(o, 'milestoneId'))}`)); }));

// Versions
addPageOpts(addRepoOpts(program
  .command('version-list')
  .description('List defined versions for issues')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/versions`, o)); }));

addRepoOpts(program
  .command('version-get')
  .description('Get a defined version for issues')
  .option('--version-id <id>', 'Version ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/versions/${enc(reqOpt(o, 'versionId'))}`)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 11. SNIPPETS (25 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(program
  .command('snippet-list')
  .description('List snippets'))
  .action(wrap(async (o) => { out(await fetchAllPages('/snippets', o)); }));

program
  .command('snippet-create')
  .description('Create a snippet')
  .option('--title <title>', 'Snippet title')
  .option('--is-private', 'Make private')
  .option('--data <json>', 'Full JSON body')
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { title: reqOpt(o, 'title') };
    if (o.isPrivate && !o.data) body.is_private = true;
    out(await bbFetch('/snippets', postBody(body)));
  }));

addPageOpts(addWsOpts(program
  .command('snippet-ws-list')
  .description('List snippets in a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/snippets/${enc(getWs(o))}`, o)); }));

addWsOpts(program
  .command('snippet-ws-create')
  .description('Create a snippet for a workspace')
  .option('--title <title>', 'Snippet title')
  .option('--is-private', 'Make private')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : { title: reqOpt(o, 'title') };
    if (o.isPrivate && !o.data) body.is_private = true;
    out(await bbFetch(`/snippets/${enc(getWs(o))}`, postBody(body)));
  }));

addWsOpts(program
  .command('snippet-get')
  .description('Get a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}`)); }));

addWsOpts(program
  .command('snippet-update')
  .description('Update a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--title <title>', 'New title')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : {};
    if (o.title && !o.data) body.title = o.title;
    out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}`, putBody(body)));
  }));

addWsOpts(program
  .command('snippet-delete')
  .description('Delete a snippet (requires --confirm)')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}`, { method: 'DELETE' });
    console.log('✅ Snippet deleted');
  }));

// Snippet revisions
addWsOpts(program
  .command('snippet-revision-get')
  .description('Get a previous revision of a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--node-id <id>', 'Node ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/${enc(reqOpt(o, 'nodeId'))}`)); }));

addWsOpts(program
  .command('snippet-revision-update')
  .description('Update a previous revision of a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--node-id <id>', 'Node ID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/${enc(reqOpt(o, 'nodeId'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addWsOpts(program
  .command('snippet-revision-delete')
  .description('Delete a previous revision of a snippet (requires --confirm)')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--node-id <id>', 'Node ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/${enc(reqOpt(o, 'nodeId'))}`, { method: 'DELETE' });
    console.log('✅ Snippet revision deleted');
  }));

// Snippet files
addWsOpts(program
  .command('snippet-file')
  .description("Get a snippet's raw file at HEAD")
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--path <path>', 'File path'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/files/${safePath(reqOpt(o, 'path'))}`)); }));

addWsOpts(program
  .command('snippet-file-revision')
  .description("Get a snippet's raw file at a revision")
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--node-id <id>', 'Node ID')
  .option('--path <path>', 'File path'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/${enc(reqOpt(o, 'nodeId'))}/files/${safePath(reqOpt(o, 'path'))}`)); }));

// Snippet diff/patch
addWsOpts(program
  .command('snippet-diff')
  .description('Get snippet changes between versions')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--revision <rev>', 'Revision'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/${enc(reqOpt(o, 'revision'))}/diff`)); }));

addWsOpts(program
  .command('snippet-patch')
  .description('Get snippet patch between versions')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--revision <rev>', 'Revision'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/${enc(reqOpt(o, 'revision'))}/patch`)); }));

// Snippet comments
addPageOpts(addWsOpts(program
  .command('snippet-comment-list')
  .description('List comments on a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/comments`, o)); }));

addWsOpts(program
  .command('snippet-comment-get')
  .description('Get a comment on a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--comment-id <id>', 'Comment ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/comments/${enc(reqOpt(o, 'commentId'))}`)); }));

addWsOpts(program
  .command('snippet-comment-create')
  .description('Create a comment on a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--body <text>', 'Comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/comments`, postBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addWsOpts(program
  .command('snippet-comment-update')
  .description('Update a comment on a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--comment-id <id>', 'Comment ID')
  .option('--body <text>', 'New comment body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/comments/${enc(reqOpt(o, 'commentId'))}`, putBody({ content: { raw: reqOpt(o, 'body') } })));
  }));

addWsOpts(program
  .command('snippet-comment-delete')
  .description('Delete a comment on a snippet (requires --confirm)')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--comment-id <id>', 'Comment ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/comments/${enc(reqOpt(o, 'commentId'))}`, { method: 'DELETE' });
    console.log('✅ Snippet comment deleted');
  }));

// Snippet commits
addPageOpts(addWsOpts(program
  .command('snippet-commit-list')
  .description('List snippet changes')
  .option('--encoded-id <id>', 'Snippet encoded ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/commits`, o)); }));

addWsOpts(program
  .command('snippet-commit-get')
  .description('Get a previous snippet change')
  .option('--encoded-id <id>', 'Snippet encoded ID')
  .option('--revision <rev>', 'Revision'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/commits/${enc(reqOpt(o, 'revision'))}`)); }));

// Snippet watch
addWsOpts(program
  .command('snippet-watch-check')
  .description('Check if the current user is watching a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/watch`)); }));

addWsOpts(program
  .command('snippet-watch')
  .description('Watch a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID'))
  .action(wrap(async (o) => {
    await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/watch`, { method: 'PUT' });
    console.log('✅ Watching snippet');
  }));

addWsOpts(program
  .command('snippet-unwatch')
  .description('Stop watching a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID'))
  .action(wrap(async (o) => {
    await bbFetch(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/watch`, { method: 'DELETE' });
    console.log('✅ Stopped watching snippet');
  }));

addPageOpts(addWsOpts(program
  .command('snippet-watchers')
  .description('List users watching a snippet')
  .option('--encoded-id <id>', 'Snippet encoded ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/snippets/${enc(getWs(o))}/${enc(reqOpt(o, 'encodedId'))}/watchers`, o)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 12. WORKSPACES (17 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(program
  .command('workspace-list')
  .description('List workspaces for user'))
  .action(wrap(async (o) => { out(await fetchAllPages('/workspaces', o)); }));

addPageOpts(program
  .command('workspace-list-for-user')
  .description('List workspaces for the current user'))
  .action(wrap(async (o) => { out(await fetchAllPages('/user/workspaces', o)); }));

addPageOpts(program
  .command('workspace-permissions-for-user')
  .description('List workspaces for the current user (via permissions)'))
  .action(wrap(async (o) => { out(await fetchAllPages('/user/permissions/workspaces', o)); }));

addWsOpts(program
  .command('workspace-user-permission')
  .description('Get user permission on a workspace'))
  .action(wrap(async (o) => { out(await bbFetch(`/user/workspaces/${enc(getWs(o))}/permission`)); }));

addWsOpts(program
  .command('workspace-get')
  .description('Get a workspace'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}`)); }));

// Workspace webhooks
addPageOpts(addWsOpts(program
  .command('workspace-hook-list')
  .description('List webhooks for a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/hooks`, o)); }));

addWsOpts(program
  .command('workspace-hook-get')
  .description('Get a webhook for a workspace')
  .option('--uid <uid>', 'Webhook UID'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/hooks/${enc(reqOpt(o, 'uid'))}`)); }));

addWsOpts(program
  .command('workspace-hook-create')
  .description('Create a webhook for a workspace')
  .option('--url <url>', 'Webhook URL')
  .option('--description <text>', 'Description')
  .option('--events <events>', 'Comma-separated event types')
  .option('--active', 'Set webhook active'))
  .action(wrap(async (o) => {
    const body = { url: reqOpt(o, 'url') };
    if (o.description) body.description = o.description;
    if (o.events) body.events = o.events.split(',').map(e => e.trim());
    if (o.active !== undefined) body.active = o.active;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/hooks`, postBody(body)));
  }));

addWsOpts(program
  .command('workspace-hook-update')
  .description('Update a webhook for a workspace')
  .option('--uid <uid>', 'Webhook UID')
  .option('--url <url>', 'Webhook URL')
  .option('--description <text>', 'Description')
  .option('--events <events>', 'Comma-separated event types')
  .option('--active', 'Set webhook active')
  .option('--no-active', 'Set webhook inactive'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.url) body.url = o.url;
    if (o.description) body.description = o.description;
    if (o.events) body.events = o.events.split(',').map(e => e.trim());
    if (o.active !== undefined) body.active = o.active;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/hooks/${enc(reqOpt(o, 'uid'))}`, putBody(body)));
  }));

addWsOpts(program
  .command('workspace-hook-delete')
  .description('Delete a webhook for a workspace (requires --confirm)')
  .option('--uid <uid>', 'Webhook UID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/hooks/${enc(reqOpt(o, 'uid'))}`, { method: 'DELETE' });
    console.log('✅ Workspace webhook deleted');
  }));

// Workspace members
addPageOpts(addWsOpts(program
  .command('workspace-member-list')
  .description('List users in a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/members`, o)); }));

addWsOpts(program
  .command('workspace-member-get')
  .description('Get user membership for a workspace')
  .option('--member <id>', 'Member ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/members/${enc(reqOpt(o, 'member'))}`)); }));

// Workspace permissions
addPageOpts(addWsOpts(program
  .command('workspace-permission-list')
  .description('List user permissions in a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/permissions`, o)); }));

addPageOpts(addWsOpts(program
  .command('workspace-repo-permissions')
  .description('List all repository permissions for a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/permissions/repositories`, o)); }));

addWsOpts(program
  .command('workspace-repo-permission-get')
  .description('List a repository permissions for a workspace')
  .option('--repo <slug>', 'Repository slug'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/permissions/repositories/${enc(reqOpt(o, 'repo'))}`)); }));

// Workspace projects
addPageOpts(addWsOpts(program
  .command('workspace-project-list')
  .description('List projects in a workspace')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/projects`, o)); }));

// Workspace user PRs
addPageOpts(addWsOpts(program
  .command('workspace-user-prs')
  .description('List workspace pull requests for a user')
  .option('--selected-user <user>', 'Username')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/pullrequests/${enc(reqOpt(o, 'selectedUser'))}`, o)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 13. PROJECTS (16 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addWsOpts(program
  .command('project-create')
  .description('Create a project in a workspace')
  .option('--name <name>', 'Project name')
  .option('--key <key>', 'Project key')
  .option('--description <text>', 'Description')
  .option('--is-private', 'Make private'))
  .action(wrap(async (o) => {
    const body = { name: reqOpt(o, 'name'), key: reqOpt(o, 'key') };
    if (o.description) body.description = o.description;
    if (o.isPrivate) body.is_private = true;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects`, postBody(body)));
  }));

addWsOpts(program
  .command('project-get')
  .description('Get a project for a workspace')
  .option('--project-key <key>', 'Project key'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}`)); }));

addWsOpts(program
  .command('project-update')
  .description('Update a project for a workspace')
  .option('--project-key <key>', 'Project key')
  .option('--name <name>', 'New name')
  .option('--description <text>', 'New description')
  .option('--is-private', 'Make private')
  .option('--no-is-private', 'Make public'))
  .action(wrap(async (o) => {
    const body = {};
    if (o.name) body.name = o.name;
    if (o.description !== undefined) body.description = o.description;
    if (o.isPrivate !== undefined) body.is_private = o.isPrivate;
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}`, putBody(body)));
  }));

addWsOpts(program
  .command('project-delete')
  .description('Delete a project for a workspace (requires --confirm)')
  .option('--project-key <key>', 'Project key')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}`, { method: 'DELETE' });
    console.log('✅ Project deleted');
  }));

// Project default reviewers
addPageOpts(addWsOpts(program
  .command('project-default-reviewer-list')
  .description('List the default reviewers in a project')
  .option('--project-key <key>', 'Project key')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/default-reviewers`, o)); }));

addWsOpts(program
  .command('project-default-reviewer-get')
  .description('Get a default reviewer')
  .option('--project-key <key>', 'Project key')
  .option('--selected-user <user>', 'Username'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/default-reviewers/${enc(reqOpt(o, 'selectedUser'))}`)); }));

addWsOpts(program
  .command('project-default-reviewer-add')
  .description('Add a user as default reviewer for a project')
  .option('--project-key <key>', 'Project key')
  .option('--selected-user <user>', 'Username'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/default-reviewers/${enc(reqOpt(o, 'selectedUser'))}`, { method: 'PUT' }));
  }));

addWsOpts(program
  .command('project-default-reviewer-delete')
  .description('Remove a user from project default reviewers (requires --confirm)')
  .option('--project-key <key>', 'Project key')
  .option('--selected-user <user>', 'Username')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/default-reviewers/${enc(reqOpt(o, 'selectedUser'))}`, { method: 'DELETE' });
    console.log('✅ Default reviewer removed from project');
  }));

// Project permissions — groups
addPageOpts(addWsOpts(program
  .command('project-group-permission-list')
  .description('List explicit group permissions for a project')
  .option('--project-key <key>', 'Project key')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/groups`, o)); }));

addWsOpts(program
  .command('project-group-permission-get')
  .description('Get an explicit group permission for a project')
  .option('--project-key <key>', 'Project key')
  .option('--group-slug <slug>', 'Group slug'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/groups/${enc(reqOpt(o, 'groupSlug'))}`)); }));

addWsOpts(program
  .command('project-group-permission-update')
  .description('Update an explicit group permission for a project')
  .option('--project-key <key>', 'Project key')
  .option('--group-slug <slug>', 'Group slug')
  .option('--permission <perm>', 'Permission'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/groups/${enc(reqOpt(o, 'groupSlug'))}`, putBody({ permission: reqOpt(o, 'permission') })));
  }));

addWsOpts(program
  .command('project-group-permission-delete')
  .description('Delete an explicit group permission for a project (requires --confirm)')
  .option('--project-key <key>', 'Project key')
  .option('--group-slug <slug>', 'Group slug')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/groups/${enc(reqOpt(o, 'groupSlug'))}`, { method: 'DELETE' });
    console.log('✅ Project group permission deleted');
  }));

// Project permissions — users
addPageOpts(addWsOpts(program
  .command('project-user-permission-list')
  .description('List explicit user permissions for a project')
  .option('--project-key <key>', 'Project key')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/users`, o)); }));

addWsOpts(program
  .command('project-user-permission-get')
  .description('Get an explicit user permission for a project')
  .option('--project-key <key>', 'Project key')
  .option('--selected-user-id <id>', 'User ID'))
  .action(wrap(async (o) => { out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/users/${enc(reqOpt(o, 'selectedUserId'))}`)); }));

addWsOpts(program
  .command('project-user-permission-update')
  .description('Update an explicit user permission for a project')
  .option('--project-key <key>', 'Project key')
  .option('--selected-user-id <id>', 'User ID')
  .option('--permission <perm>', 'Permission'))
  .action(wrap(async (o) => {
    out(await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/users/${enc(reqOpt(o, 'selectedUserId'))}`, putBody({ permission: reqOpt(o, 'permission') })));
  }));

addWsOpts(program
  .command('project-user-permission-delete')
  .description('Delete an explicit user permission for a project (requires --confirm)')
  .option('--project-key <key>', 'Project key')
  .option('--selected-user-id <id>', 'User ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/workspaces/${enc(getWs(o))}/projects/${enc(reqOpt(o, 'projectKey'))}/permissions-config/users/${enc(reqOpt(o, 'selectedUserId'))}`, { method: 'DELETE' });
    console.log('✅ Project user permission deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 14. USERS (4 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

program
  .command('user-get-current')
  .description('Get current user')
  .action(wrap(async () => { out(await bbFetch('/user')); }));

addPageOpts(program
  .command('user-emails')
  .description('List email addresses for current user'))
  .action(wrap(async (o) => { out(await fetchAllPages('/user/emails', o)); }));

program
  .command('user-email-get')
  .description('Get an email address for current user')
  .option('--email <email>', 'Email address')
  .action(wrap(async (o) => { out(await bbFetch(`/user/emails/${enc(reqOpt(o, 'email'))}`)); }));

program
  .command('user-get')
  .description('Get a user')
  .option('--selected-user <user>', 'Username')
  .action(wrap(async (o) => { out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}`)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 15. SSH KEYS (5 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(program
  .command('ssh-key-list')
  .description('List SSH keys')
  .option('--selected-user <user>', 'Username'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/users/${enc(reqOpt(o, 'selectedUser'))}/ssh-keys`, o)); }));

program
  .command('ssh-key-get')
  .description('Get a SSH key')
  .option('--selected-user <user>', 'Username')
  .option('--key-id <id>', 'Key ID')
  .action(wrap(async (o) => { out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/ssh-keys/${enc(reqOpt(o, 'keyId'))}`)); }));

program
  .command('ssh-key-create')
  .description('Add a new SSH key')
  .option('--selected-user <user>', 'Username')
  .option('--key <key>', 'SSH public key')
  .option('--label <label>', 'Key label')
  .action(wrap(async (o) => {
    const body = { key: reqOpt(o, 'key') };
    if (o.label) body.label = o.label;
    out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/ssh-keys`, postBody(body)));
  }));

program
  .command('ssh-key-update')
  .description('Update a SSH key')
  .option('--selected-user <user>', 'Username')
  .option('--key-id <id>', 'Key ID')
  .option('--label <label>', 'New label')
  .option('--data <json>', 'Full JSON body')
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : {};
    if (o.label && !o.data) body.label = o.label;
    out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/ssh-keys/${enc(reqOpt(o, 'keyId'))}`, putBody(body)));
  }));

program
  .command('ssh-key-delete')
  .description('Delete a SSH key (requires --confirm)')
  .option('--selected-user <user>', 'Username')
  .option('--key-id <id>', 'Key ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/ssh-keys/${enc(reqOpt(o, 'keyId'))}`, { method: 'DELETE' });
    console.log('✅ SSH key deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 16. GPG KEYS (4 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(program
  .command('gpg-key-list')
  .description('List GPG keys')
  .option('--selected-user <user>', 'Username'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/users/${enc(reqOpt(o, 'selectedUser'))}/gpg-keys`, o)); }));

program
  .command('gpg-key-get')
  .description('Get a GPG key')
  .option('--selected-user <user>', 'Username')
  .option('--fingerprint <fp>', 'Key fingerprint')
  .action(wrap(async (o) => { out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/gpg-keys/${enc(reqOpt(o, 'fingerprint'))}`)); }));

program
  .command('gpg-key-create')
  .description('Add a new GPG key')
  .option('--selected-user <user>', 'Username')
  .option('--key <key>', 'GPG public key (ASCII armored)')
  .action(wrap(async (o) => {
    out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/gpg-keys`, postBody({ key: reqOpt(o, 'key') })));
  }));

program
  .command('gpg-key-delete')
  .description('Delete a GPG key (requires --confirm)')
  .option('--selected-user <user>', 'Username')
  .option('--fingerprint <fp>', 'Key fingerprint')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/gpg-keys/${enc(reqOpt(o, 'fingerprint'))}`, { method: 'DELETE' });
    console.log('✅ GPG key deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 17. SOURCE / FILE BROWSING (4 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addRepoOpts(program
  .command('src-history')
  .description('List commits that modified a file')
  .option('--commit <sha>', 'Commit SHA or branch')
  .option('--path <path>', 'File path')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/filehistory/${enc(reqOpt(o, 'commit'))}/${safePath(reqOpt(o, 'path'))}`, o)); }));

addRepoOpts(program
  .command('src-root')
  .description('Get the root directory of the main branch'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/src`)); }));

addRepoOpts(program
  .command('src-create')
  .description('Create a commit by uploading a file')
  .option('--file <path>', 'Local file to upload')
  .option('--remote-path <path>', 'Destination path in repo')
  .option('--message <msg>', 'Commit message')
  .option('--branch <branch>', 'Target branch'))
  .action(wrap(async (o) => {
    const filePath = resolve(safePath(reqOpt(o, 'file')) || reqOpt(o, 'file'));
    checkFileSize(filePath);
    const fileContent = readFileSync(filePath);
    const remotePath = safePath(reqOpt(o, 'remotePath'));
    const form = new FormData();
    form.append(remotePath, new Blob([fileContent]), basename(filePath));
    if (o.message) form.append('message', o.message);
    if (o.branch) form.append('branch', o.branch);
    out(await bbFetch(`${rp(o)}/src`, { method: 'POST', body: form, rawBody: true }));
  }));

addRepoOpts(program
  .command('src-get')
  .description('Get file or directory contents')
  .option('--commit <sha>', 'Commit SHA or branch')
  .option('--path <path>', 'File or directory path'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/src/${enc(reqOpt(o, 'commit'))}/${safePath(reqOpt(o, 'path'))}`)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 18. DOWNLOADS (4 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addRepoOpts(program
  .command('download-list')
  .description('List download artifacts')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/downloads`, o)); }));

addRepoOpts(program
  .command('download-get')
  .description('Get a download artifact link')
  .option('--filename <name>', 'Filename'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/downloads/${enc(reqOpt(o, 'filename'))}`)); }));

addRepoOpts(program
  .command('download-upload')
  .description('Upload a download artifact')
  .option('--file <path>', 'Local file path'))
  .action(wrap(async (o) => {
    const filePath = resolve(safePath(reqOpt(o, 'file')) || reqOpt(o, 'file'));
    checkFileSize(filePath);
    const fileContent = readFileSync(filePath);
    const fileName = basename(filePath);
    const form = new FormData();
    form.append('files', new Blob([fileContent]), fileName);
    out(await bbFetch(`${rp(o)}/downloads`, { method: 'POST', body: form, rawBody: true }));
  }));

addRepoOpts(program
  .command('download-delete')
  .description('Delete a download artifact (requires --confirm)')
  .option('--filename <name>', 'Filename')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/downloads/${enc(reqOpt(o, 'filename'))}`, { method: 'DELETE' });
    console.log('✅ Download deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 19. WEBHOOKS (2 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

program
  .command('webhook-events')
  .description('Get a webhook resource')
  .action(wrap(async () => { out(await bbFetch('/hook_events')); }));

program
  .command('webhook-event-types')
  .description('List subscribable webhook types')
  .option('--subject-type <type>', 'Subject type (workspace, user, repository, team)')
  .action(wrap(async (o) => { out(await bbFetch(`/hook_events/${enc(reqOpt(o, 'subjectType'))}`)); }));

// ═══════════════════════════════════════════════════════════════════════════
// 20. SEARCH (3 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addWsOpts(program
  .command('search-code')
  .description('Search for code in a workspace')
  .option('--search-query <query>', 'Search query')))
  .action(wrap(async (o) => { out(await fetchAllPages(`/workspaces/${enc(getWs(o))}/search/code`, o, { search_query: reqOpt(o, 'searchQuery') })); }));

addPageOpts(program
  .command('search-account')
  .description('Search for code in a user\'s repositories')
  .option('--selected-user <user>', 'Username')
  .option('--search-query <query>', 'Search query'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/users/${enc(reqOpt(o, 'selectedUser'))}/search/code`, o, { search_query: reqOpt(o, 'searchQuery') })); }));

addPageOpts(program
  .command('search-team')
  .description("Search for code in a team's repositories")
  .option('--username <name>', 'Team username')
  .option('--search-query <query>', 'Search query'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/teams/${enc(reqOpt(o, 'username'))}/search/code`, o, { search_query: reqOpt(o, 'searchQuery') })); }));

// ═══════════════════════════════════════════════════════════════════════════
// 21. REPORTS (9 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

addPageOpts(addRepoOpts(program
  .command('report-list')
  .description('List reports')
  .option('--commit <sha>', 'Commit SHA')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports`, o)); }));

addRepoOpts(program
  .command('report-get')
  .description('Get a report')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}`)); }));

addRepoOpts(program
  .command('report-create')
  .description('Create or update a report')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')
  .option('--title <title>', 'Report title')
  .option('--report-type <type>', 'Report type (SECURITY, COVERAGE, TEST, BUG)')
  .option('--data <json>', 'Full JSON body'))
  .action(wrap(async (o) => {
    const body = o.data ? JSON.parse(o.data) : {};
    if (o.title && !o.data) body.title = o.title;
    if (o.reportType && !o.data) body.report_type = o.reportType;
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}`, putBody(body)));
  }));

addRepoOpts(program
  .command('report-delete')
  .description('Delete a report (requires --confirm)')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}`, { method: 'DELETE' });
    console.log('✅ Report deleted');
  }));

// Report annotations
addPageOpts(addRepoOpts(program
  .command('report-annotation-list')
  .description('List annotations')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')))
  .action(wrap(async (o) => { out(await fetchAllPages(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}/annotations`, o)); }));

addRepoOpts(program
  .command('report-annotation-get')
  .description('Get an annotation')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')
  .option('--annotation-id <id>', 'Annotation ID'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}/annotations/${enc(reqOpt(o, 'annotationId'))}`)); }));

addRepoOpts(program
  .command('report-annotation-create')
  .description('Create or update an annotation')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')
  .option('--annotation-id <id>', 'Annotation ID')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}/annotations/${enc(reqOpt(o, 'annotationId'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('report-annotation-bulk-create')
  .description('Bulk create or update annotations')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')
  .option('--data <json>', 'JSON array of annotations'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}/annotations`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('report-annotation-delete')
  .description('Delete an annotation (requires --confirm)')
  .option('--commit <sha>', 'Commit SHA')
  .option('--report-id <id>', 'Report ID')
  .option('--annotation-id <id>', 'Annotation ID')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/reports/${enc(reqOpt(o, 'reportId'))}/annotations/${enc(reqOpt(o, 'annotationId'))}`, { method: 'DELETE' });
    console.log('✅ Annotation deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 22. PROPERTIES (12 endpoints)
// ═══════════════════════════════════════════════════════════════════════════

// Commit properties
addRepoOpts(program
  .command('commit-property-get')
  .description('Get a commit application property')
  .option('--commit <sha>', 'Commit SHA')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`)); }));

addRepoOpts(program
  .command('commit-property-update')
  .description('Update a commit application property')
  .option('--commit <sha>', 'Commit SHA')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('commit-property-delete')
  .description('Delete a commit application property (requires --confirm)')
  .option('--commit <sha>', 'Commit SHA')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/commit/${enc(reqOpt(o, 'commit'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, { method: 'DELETE' });
    console.log('✅ Commit property deleted');
  }));

// Repository properties
addRepoOpts(program
  .command('repo-property-get')
  .description('Get a repository application property')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`)); }));

addRepoOpts(program
  .command('repo-property-update')
  .description('Update a repository application property')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('repo-property-delete')
  .description('Delete a repository application property (requires --confirm)')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, { method: 'DELETE' });
    console.log('✅ Repository property deleted');
  }));

// Pull request properties
addRepoOpts(program
  .command('pr-property-get')
  .description('Get a pull request application property')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name'))
  .action(wrap(async (o) => { out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`)); }));

addRepoOpts(program
  .command('pr-property-update')
  .description('Update a pull request application property')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--data <json>', 'JSON body'))
  .action(wrap(async (o) => {
    out(await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addRepoOpts(program
  .command('pr-property-delete')
  .description('Delete a pull request application property (requires --confirm)')
  .option('--pr-id <id>', 'Pull request ID')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--confirm', 'Confirm deletion'))
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`${rp(o)}/pullrequests/${enc(reqOpt(o, 'prId'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, { method: 'DELETE' });
    console.log('✅ Pull request property deleted');
  }));

// User properties
program
  .command('user-property-get')
  .description('Get a user application property')
  .option('--selected-user <user>', 'Username')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .action(wrap(async (o) => { out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`)); }));

program
  .command('user-property-update')
  .description('Update a user application property')
  .option('--selected-user <user>', 'Username')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--data <json>', 'JSON body')
  .action(wrap(async (o) => {
    out(await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

program
  .command('user-property-delete')
  .description('Delete a user application property (requires --confirm)')
  .option('--selected-user <user>', 'Username')
  .option('--app-key <key>', 'Application key')
  .option('--property-name <name>', 'Property name')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/users/${enc(reqOpt(o, 'selectedUser'))}/properties/${enc(reqOpt(o, 'appKey'))}/${enc(reqOpt(o, 'propertyName'))}`, { method: 'DELETE' });
    console.log('✅ User property deleted');
  }));

// ═══════════════════════════════════════════════════════════════════════════
// 23. ADDON (10 endpoints) — Note: JWT auth only for most
// ═══════════════════════════════════════════════════════════════════════════

program
  .command('addon-delete')
  .description('Delete an app (JWT auth required)')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch('/addon', { method: 'DELETE' });
    console.log('✅ Addon deleted');
  }));

program
  .command('addon-update')
  .description('Update an installed app (JWT auth required)')
  .option('--data <json>', 'JSON body')
  .action(wrap(async (o) => {
    out(await bbFetch('/addon', putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

addPageOpts(program
  .command('addon-linkers')
  .description('List linkers for an app (JWT auth required)'))
  .action(wrap(async (o) => { out(await fetchAllPages('/addon/linkers', o)); }));

program
  .command('addon-linker-get')
  .description('Get a linker for an app (JWT auth required)')
  .option('--linker-key <key>', 'Linker key')
  .action(wrap(async (o) => { out(await bbFetch(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}`)); }));

program
  .command('addon-linker-values-delete')
  .description('Delete all linker values (JWT auth required, requires --confirm)')
  .option('--linker-key <key>', 'Linker key')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}/values`, { method: 'DELETE' });
    console.log('✅ All linker values deleted');
  }));

addPageOpts(program
  .command('addon-linker-values')
  .description('List linker values for a linker (JWT auth required)')
  .option('--linker-key <key>', 'Linker key'))
  .action(wrap(async (o) => { out(await fetchAllPages(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}/values`, o)); }));

program
  .command('addon-linker-value-create')
  .description('Create a linker value (JWT auth required)')
  .option('--linker-key <key>', 'Linker key')
  .option('--data <json>', 'JSON body')
  .action(wrap(async (o) => {
    out(await bbFetch(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}/values`, postBody(JSON.parse(reqOpt(o, 'data')))));
  }));

program
  .command('addon-linker-value-update')
  .description('Update a linker value (JWT auth required)')
  .option('--linker-key <key>', 'Linker key')
  .option('--data <json>', 'JSON body')
  .action(wrap(async (o) => {
    out(await bbFetch(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}/values`, putBody(JSON.parse(reqOpt(o, 'data')))));
  }));

program
  .command('addon-linker-value-delete')
  .description('Delete a linker value (JWT auth required, requires --confirm)')
  .option('--linker-key <key>', 'Linker key')
  .option('--value-id <id>', 'Value ID')
  .option('--confirm', 'Confirm deletion')
  .action(wrap(async (o) => {
    confirmOrDie(o);
    await bbFetch(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}/values/${enc(reqOpt(o, 'valueId'))}`, { method: 'DELETE' });
    console.log('✅ Linker value deleted');
  }));

program
  .command('addon-linker-value-get')
  .description('Get a linker value (JWT auth required)')
  .option('--linker-key <key>', 'Linker key')
  .option('--value-id <id>', 'Value ID')
  .action(wrap(async (o) => { out(await bbFetch(`/addon/linkers/${enc(reqOpt(o, 'linkerKey'))}/values/${enc(reqOpt(o, 'valueId'))}`)); }));

// ── Parse ───────────────────────────────────────────────────────────────────

program.parse();
