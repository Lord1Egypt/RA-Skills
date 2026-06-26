// ATP Service Helper -- wraps marketplace service publishing for merchant agents.

const { getNodeId, buildHubHeaders, getHubUrl } = require('../gep/a2aProtocol');
const { hubFetch } = require('../gep/hubFetch');
const { HTTP_TRANSPORT_TIMEOUT_MS } = require('../config');

async function postService(endpoint, body) {
  try {
    const res = await hubFetch(endpoint, {
      method: 'POST',
      headers: Object.assign({ 'Content-Type': 'application/json' }, buildHubHeaders() || {}),
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(HTTP_TRANSPORT_TIMEOUT_MS),
    });

    if (!res.ok) {
      const t = await res.text();
      return { ok: false, status: res.status, error: t.slice(0, 400) };
    }
    const data = await res.json();
    return { ok: true, data };
  } catch (err) {
    const msg = (err && err.message) || String(err);
    if (msg.indexOf('[hubFetch]') !== -1) {
      return { ok: false, error: 'tls_refused: ' + msg };
    }
    return { ok: false, error: msg };
  }
}

/**
 * Publish a ServiceListing via the Hub marketplace API.
 * @param {object} svc
 * @param {string} svc.title
 * @param {string} [svc.description]
 * @param {string[]} [svc.capabilities]
 * @param {string[]} [svc.useCases]
 * @param {number} [svc.pricePerTask] - min 1 Credit
 * @param {string} [svc.executionMode] - exclusive | open | swarm
 * @param {number} [svc.maxConcurrent]
 * @param {string} [svc.recipeId]
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function publishService(svc) {
  const hubUrl = getHubUrl();
  if (!hubUrl) return { ok: false, error: 'no_hub_url' };

  const nodeId = getNodeId();
  const endpoint = hubUrl.replace(/\/+$/, '') + '/a2a/service/publish';

  const body = {
    sender_id: nodeId,
    title: svc.title,
    description: svc.description,
    capabilities: svc.capabilities,
    use_cases: svc.useCases,
    price_per_task: Math.max(1, Math.round(Number(svc.pricePerTask) || 10)),
    execution_mode: svc.executionMode || 'exclusive',
    max_concurrent: Math.max(1, Math.round(Number(svc.maxConcurrent) || 3)),
    recipe_id: svc.recipeId,
  };

  return postService(endpoint, body);
}

/**
 * Update an existing ServiceListing.
 * @param {string} listingId
 * @param {object} updates
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function updateService(listingId, updates) {
  const hubUrl = getHubUrl();
  if (!hubUrl) return { ok: false, error: 'no_hub_url' };

  const nodeId = getNodeId();
  const endpoint = hubUrl.replace(/\/+$/, '') + '/a2a/service/update';

  const body = {
    sender_id: nodeId,
    listing_id: listingId,
    ...updates,
  };

  return postService(endpoint, body);
}

module.exports = {
  publishService,
  updateService,
};
