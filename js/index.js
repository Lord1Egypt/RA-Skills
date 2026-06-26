'use strict';
/*
 * ra-skills — search 90,896 Hermes Agent skills offline, download any on demand.
 * Zero dependencies (Node built-ins only).
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const REPO = 'Lord1Egypt/RA-Skills';
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/master`;
const GITHUB_API = `https://api.github.com/repos/${REPO}/contents`;

let _registry = null;

function _registryPath() {
  const bundled = path.join(__dirname, 'data', 'registry.json');
  if (fs.existsSync(bundled)) return bundled;
  const dev = path.join(__dirname, '..', 'registry.json'); // repo root fallback
  return dev;
}

function _load() {
  if (_registry === null) {
    const p = _registryPath();
    if (!fs.existsSync(p)) throw new Error('registry.json not found. Reinstall ra-skills.');
    _registry = JSON.parse(fs.readFileSync(p, 'utf8'));
  }
  return _registry;
}

function allSkills() {
  return _load().skills || [];
}

function stats() {
  const data = _load();
  const bySource = {};
  for (const s of data.skills || []) {
    const k = s.source || '?';
    bySource[k] = (bySource[k] || 0) + 1;
  }
  const sorted = Object.fromEntries(Object.entries(bySource).sort((a, b) => b[1] - a[1]));
  return {
    total: data.total || (data.skills || []).length,
    built_in: data.built_in || 0,
    optional: data.optional || 0,
    community: data.community || 0,
    by_source: sorted,
  };
}

function search(query, opts = {}) {
  const q = query ? String(query).toLowerCase() : null;
  const src = opts.source ? opts.source.toLowerCase() : null;
  const cat = opts.category ? opts.category.toLowerCase() : null;
  const limit = opts.limit === undefined ? 10 : opts.limit;
  const out = [];
  for (const s of allSkills()) {
    if (src && (s.source || '').toLowerCase() !== src) continue;
    if (cat && (s.category || '').toLowerCase() !== cat) continue;
    if (q) {
      const inName = (s.name || '').toLowerCase().includes(q) || (s.identifier || '').toLowerCase().includes(q);
      const inDesc = (s.description || '').toLowerCase().includes(q);
      const inTags = (s.tags || []).some((t) => String(t).toLowerCase().includes(q));
      if (!(inName || inDesc || inTags)) continue;
    }
    out.push(s);
  }
  return (limit === 0 || limit === null) ? out : out.slice(0, limit);
}

function show(nameOrId) {
  const key = String(nameOrId).toLowerCase();
  return (
    allSkills().find((s) => (s.name || '').toLowerCase() === key || (s.identifier || '').toLowerCase() === key) ||
    allSkills().find((s) => (s.name || '').toLowerCase().includes(key) || (s.identifier || '').toLowerCase().includes(key)) ||
    null
  );
}

function _sanitize(name, maxlen = 80) {
  return ((String(name).replace(/[^\w\-]/g, '_').toLowerCase()) || 'unknown').slice(0, maxlen);
}
function _partitionChar(name) {
  const clean = String(name).replace(/[^a-zA-Z0-9]/g, '');
  return clean ? clean[0].toLowerCase() : '_';
}
function _sourceSlug(source) {
  return String(source).replace(/[^\w]/g, '_').toLowerCase();
}

function _communityFolder(skill) {
  const san = _sanitize(skill.identifier || '');
  return `skills/community/${_sourceSlug(skill.source || '')}/${_partitionChar(san)}/${san}`;
}

function _candidateFolders(skill) {
  const source = skill.source || '';
  if (source === 'built-in' || source === 'optional') {
    const base = `skills/${source}`;
    const cands = [];
    for (const leaf of [skill.name, skill.identifier]) {
      if (skill.category) cands.push(`${base}/${skill.category}/${leaf}`);
      cands.push(`${base}/${leaf}`);
    }
    return cands;
  }
  return [_communityFolder(skill)];
}

function _get(url, json) {
  return new Promise((resolve) => {
    const headers = { 'User-Agent': 'ra-skills/1.0' };
    if (json) headers.Accept = 'application/vnd.github+json';
    if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
    https.get(url, { headers }, (res) => {
      if (res.statusCode >= 300) { res.resume(); return resolve(null); }
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        resolve(json ? JSON.parse(buf.toString('utf8')) : buf);
      });
    }).on('error', () => resolve(null));
  });
}

async function _collect(folder, root, depth = 0) {
  if (root === undefined) root = folder;
  if (depth > 8) return [];
  const items = await _get(`${GITHUB_API}/${encodeURIComponent(folder).replace(/%2F/g, '/')}`, true);
  if (!Array.isArray(items)) return [];
  const out = [];
  for (const it of items) {
    const rel = (it.path || '').slice(root.length).replace(/^\/+/, '');
    if (it.type === 'file' && it.download_url) out.push([rel, it.download_url]);
    else if (it.type === 'dir') out.push(...(await _collect(it.path, root, depth + 1)));
  }
  return out;
}

async function _listSkillFiles(skill) {
  for (const folder of _candidateFolders(skill)) {
    const files = await _collect(folder, folder);
    if (files.some(([rel]) => rel.toLowerCase() === 'skill.md')) return files;
  }
  return [];
}

async function fetchContent(nameOrId) {
  const skill = show(nameOrId);
  if (!skill) return null;
  if (skill.source !== 'built-in' && skill.source !== 'optional') {
    const data = await _get(`${RAW_BASE}/${_communityFolder(skill)}/SKILL.md`, false);
    if (data) return data.toString('utf8');
  }
  const files = await _listSkillFiles(skill);
  for (const [rel, dl] of files) {
    if (rel.toLowerCase() === 'skill.md') {
      const data = await _get(dl, false);
      return data ? data.toString('utf8') : null;
    }
  }
  return null;
}

async function download(nameOrId, dest = '.') {
  const skill = show(nameOrId);
  if (!skill) return null;
  const files = await _listSkillFiles(skill);
  if (!files.length) return null;
  const outDir = path.join(dest, _sanitize(skill.name || skill.identifier));
  let written = 0;
  for (const [rel, url] of files) {
    const data = await _get(url, false);
    if (!data) continue;
    const safe = rel.split('/').filter((p) => p && p !== '.' && p !== '..')
      .map((p) => p.replace(/[^\w.\-]/g, '_').slice(0, 80)).join('/');
    const target = path.join(outDir, safe);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, data);
    written++;
  }
  return written ? outDir : null;
}

module.exports = { search, stats, show, download, fetchContent, allSkills };
