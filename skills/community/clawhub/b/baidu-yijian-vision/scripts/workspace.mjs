#!/usr/bin/env node

import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { httpsRequest, getApiKey, workspacesGetUrl, workspaceSkillsGetUrl, truncateBody } from './utils.mjs';
import { readCache, writeCache, clearCache, getCacheDir, keyHashedPath } from './cache.mjs';

const CACHE_DIR = getCacheDir();
const SKILLS_CACHE_TTL = 60 * 60 * 1000; // 1 hour in ms
export const MAX_PAGES = 100;

function workspaceCacheFile(apiKey) {
  return keyHashedPath(path.join(CACHE_DIR, 'workspace-cache.json'), apiKey);
}

function skillsCacheFile(apiKey, workspacesHash = '') {
  const suffix = workspacesHash ? `-${workspacesHash}` : '';
  return keyHashedPath(path.join(CACHE_DIR, `skills-cache${suffix}.json`), apiKey);
}

export function buildEpId(workspaceId, localName) {
  // localName format: c-sk-XXXXX → extract XXXXX part
  const suffix = localName.replace(/^c-sk-/, '');
  return `ep-${workspaceId}-${suffix}`;
}

// ── API Functions ────────────────────────────────────────────────────

/**
 * Get all workspace IDs the user has access to.
 * Uses long-lived cache (tied to API key).
 */
export async function getAllWorkspaceIds() {
  const apiKey = getApiKey();
  const cacheFile = workspaceCacheFile(apiKey);
  const cached = readCache(cacheFile);
  if (cached?.workspaceIds) return cached.workspaceIds;

  const url = workspacesGetUrl();
  const { statusCode, body } = await httpsRequest(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (statusCode !== 200) {
    throw new Error(`workspaces/get failed: HTTP ${statusCode} - ${truncateBody(body)}`);
  }

  let resp;
  try {
    resp = JSON.parse(body);
  } catch {
    throw new Error(`workspaces/get unexpected response: ${truncateBody(body)}`);
  }
  if (!resp.success || !resp.page?.result) {
    throw new Error(`workspaces/get unexpected response: ${truncateBody(body)}`);
  }

  const workspaceIds = resp.page.result.map(ws => ws.id);
  if (workspaceIds.length === 0) {
    throw new Error('No workspaces found');
  }

  writeCache(cacheFile, { workspaceIds, timestamp: Date.now() });
  return workspaceIds;
}

/**
 * Fetch released SkillApi skills from a single workspace with pagination.
 */
async function fetchWorkspaceSkills(apiKey, workspaceId) {
  const url = workspaceSkillsGetUrl(workspaceId);
  const allSkills = [];
  let pageNo = 1;
  const pageSize = 50;

  while (true) {
    if (pageNo > MAX_PAGES) {
      throw new Error(`Pagination exceeded ${MAX_PAGES} pages, aborting`);
    }
    const { statusCode, body } = await httpsRequest(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        workspaceID: workspaceId,
        orderBy: 'last_published_at',
        order: 'desc',
        pageNo,
        pageSize,
        publicationKinds: ['SkillApi'],
        status: 'Released',
      }),
    });

    if (statusCode !== 200) {
      throw new Error(`skills/get failed: HTTP ${statusCode} - ${truncateBody(body)}`);
    }

    let resp;
    try {
      resp = JSON.parse(body);
    } catch {
      throw new Error(`skills/get unexpected response: ${truncateBody(body)}`);
    }
    if (!resp.success || !resp.page?.result) {
      throw new Error(`skills/get unexpected response: ${truncateBody(body)}`);
    }

    const skills = resp.page.result.map(skill => ({
      epId: buildEpId(workspaceId, skill.localName),
      displayName: skill.displayName,
      description: skill.description || '',
      localName: skill.localName,
      workspaceId,
    }));

    allSkills.push(...skills);

    const totalCount = resp.page.totalCount || 0;
    if (allSkills.length >= totalCount || skills.length < pageSize) break;
    pageNo++;
  }

  return allSkills;
}

/**
 * Get all released SkillApi skills from all workspaces.
 * Uses file cache with 1-hour TTL. Cache key includes a hash of workspace IDs
 * so that newly assigned workspaces invalidate the cache automatically.
 *
 * @param {object} options
 * @param {boolean} options.forceRefresh - Bypass cache and re-fetch from API
 */
export async function getWorkspaceSkills(options = {}) {
  const { forceRefresh = false } = options;
  const apiKey = getApiKey();

  // Always fetch workspace IDs (cached) to build the cache key
  const workspaceIds = await getAllWorkspaceIds();
  const workspacesHash = crypto.createHash('sha256').update(workspaceIds.sort().join(',')).digest('hex').slice(0, 8);
  const cacheFile = skillsCacheFile(apiKey, workspacesHash);

  if (!forceRefresh) {
    const cached = readCache(cacheFile, SKILLS_CACHE_TTL);
    if (cached?.skills) return cached.skills;
  }

  // Fetch skills from all workspaces in parallel
  const results = await Promise.all(
    workspaceIds.map(id => fetchWorkspaceSkills(apiKey, id).catch(err => {
      console.error(`Failed to fetch skills for workspace ${id}: ${err.message}`);
      return [];
    }))
  );

  const allSkills = results.flat();

  writeCache(cacheFile, { workspaceIds, skills: allSkills, timestamp: Date.now() });
  return allSkills;
}

// ── CLI ──────────────────────────────────────────────────────────────

async function main() {
  const command = process.argv[2];

  if (command === 'list-skills') {
    const forceRefresh = process.argv.includes('--refresh');
    try {
      const skills = await getWorkspaceSkills({ forceRefresh });
      const result = {
        success: true,
        count: skills.length,
        skills: skills.map(s => ({
          epId: s.epId,
          displayName: s.displayName,
          description: s.description || null,
        })),
      };
      console.log(JSON.stringify(result, null, 2));
    } catch (err) {
      console.error(JSON.stringify({ success: false, error: err.message }, null, 2));
      process.exit(1);
    }
  } else if (command === 'refresh') {
    try {
      const apiKey = getApiKey();
      // Clear workspace cache to force re-fetch of workspace list
      clearCache(workspaceCacheFile(apiKey));
      // Fetch with forceRefresh to rebuild skills cache
      const skills = await getWorkspaceSkills({ forceRefresh: true });
      console.log(JSON.stringify({ success: true, count: skills.length, message: 'Cache refreshed' }, null, 2));
    } catch (err) {
      console.error(JSON.stringify({ success: false, error: err.message }, null, 2));
      process.exit(1);
    }
  } else {
    console.error('Usage: node workspace.mjs <list-skills|refresh> [--refresh]');
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
