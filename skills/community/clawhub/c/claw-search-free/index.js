/**
 * Claw Search Skill for OpenClaw
 * 
 * This skill provides a convenient wrapper around the Claw Search API,
 * allowing agents to easily perform web, image, and news searches.
 * 
 * No API key required - free for all OpenClaw agents!
 */

const CLAW_SEARCH_BASE = 'https://www.claw-search.com';

/**
 * Perform a web search
 * @param {string} query - Search query
 * @param {object} options - Search options (count, offset)
 * @returns {Promise<object>} Search results
 */
export async function search(query, options = {}) {
  const params = new URLSearchParams({
    q: query,
    count: options.count || '10',
    offset: options.offset || '0'
  });
  
  const response = await fetch(`${CLAW_SEARCH_BASE}/api/search?${params}`);
  
  if (!response.ok) {
    throw new Error(`Search failed: ${response.status}`);
  }
  
  return response.json();
}

/**
 * Search for images
 * @param {string} query - Search query
 * @param {number} count - Number of results
 * @returns {Promise<object>} Image search results
 */
export async function searchImages(query, count = 20) {
  const params = new URLSearchParams({
    q: query,
    count: count.toString()
  });
  
  const response = await fetch(`${CLAW_SEARCH_BASE}/api/images?${params}`);
  return response.json();
}

/**
 * Search for news
 * @param {string} query - Search query
 * @param {number} count - Number of results
 * @returns {Promise<object>} News results
 */
export async function searchNews(query, count = 10) {
  const params = new URLSearchParams({
    q: query,
    count: count.toString()
  });
  
  const response = await fetch(`${CLAW_SEARCH_BASE}/api/news?${params}`);
  return response.json();
}

/**
 * Get search suggestions
 * @param {string} query - Partial query
 * @returns {Promise<string[]>} Suggestions
 */
export async function getSuggestions(query) {
  const params = new URLSearchParams({ q: query });
  const response = await fetch(`${CLAW_SEARCH_BASE}/api/suggest?${params}`);
  const data = await response.json();
  return data.suggestions || [];
}

/**
 * Check API health
 * @returns {Promise<object>} Health status
 */
export async function healthCheck() {
  const response = await fetch(`${CLAW_SEARCH_BASE}/health`);
  return response.json();
}

// Default export
export default {
  search,
  searchImages,
  searchNews,
  getSuggestions,
  healthCheck
};