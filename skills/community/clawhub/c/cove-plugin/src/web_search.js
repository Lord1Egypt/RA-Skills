/**
 * Web Search — optional verification source using Brave Search API.
 *
 * The Brave API key is resolved in config.js (from env var or file)
 * and passed in via the config object. This module does NOT read
 * process.env directly.
 */

const https = require('https');

/**
 * Search the web using Brave Search API.
 * @param {string} query - Search query.
 * @param {number} count - Number of results (default 3).
 * @param {string|null} apiKey - Brave API key (from config).
 * @returns {Promise<string>} Formatted search results or empty string.
 */
function braveSearch(query, count = 3, apiKey = null) {
  if (!apiKey) return Promise.resolve('');

  return new Promise((resolve) => {
    const params = new URLSearchParams({ q: query, count: String(count) });
    const options = {
      hostname: 'api.search.brave.com',
      path: `/res/v1/web/search?${params}`,
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': apiKey,
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          const results = (parsed.web?.results || []).slice(0, count);
          if (results.length === 0) return resolve('');

          const formatted = results.map((r, i) =>
            `[${i + 1}] ${r.title}\n    URL: ${r.url}\n    ${r.description || ''}`
          ).join('\n\n');
          resolve(formatted);
        } catch {
          resolve('');
        }
      });
    });

    req.on('error', () => resolve(''));
    req.setTimeout(10000, () => { req.destroy(); resolve(''); });
    req.end();
  });
}

/**
 * Search for multiple claims and aggregate results.
 * Used in "standard" and "deep" verification policies.
 *
 * @param {string[]} queries - List of claim texts to search for.
 * @param {object} config - Plugin config.
 * @returns {Promise<string|null>} Aggregated search results or null.
 */
async function searchWeb(queries, config) {
  const sources = config.knowledge_sources || {};
  if (!sources.enable_web_search) return null;

  const apiKey = config.brave_api_key || null;
  if (!apiKey) {
    console.log('[cove] Web search skipped: no Brave API key found.');
    return null;
  }

  // Limit to 5 searches to control cost/latency
  const limitedQueries = queries.slice(0, 5);
  const results = [];

  for (const query of limitedQueries) {
    const result = await braveSearch(query, 3, apiKey);
    if (result) {
      results.push(`Query: "${query}"\n${result}`);
    }
  }

  return results.length > 0 ? results.join('\n\n---\n\n') : null;
}

module.exports = { searchWeb, braveSearch };
