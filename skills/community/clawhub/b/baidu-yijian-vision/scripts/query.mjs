#!/usr/bin/env node

import { httpsRequest, getApiKey, routerQueryUrl, truncateBody } from './utils.mjs';
import { fileURLToPath } from 'url';

/**
 * Parse and validate the router query response.
 * Returns array of skills sorted by confidence (highest first).
 */
export function parseQueryResponse(response) {
  // Handle internal API response format
  if (response?.data?.candidates && Array.isArray(response.data.candidates)) {
    return response.data.candidates
      .filter(s => s.skillId && typeof s.score === 'number')
      .map(s => ({
        epId: s.skillId,
        name: s.displayName,
        description: s.description,
        confidence: s.score
      }))
      .sort((a, b) => b.confidence - a.confidence);
  }
  // Fallback to empty array
  return [];
}

/**
 * Query skills by intent text.
 * @param {string} intent - User's intent text
 * @param {object} options - Optional parameters
 * @param {number} options.topK - Maximum number of results (default: 5)
 * @returns {Promise<Array>} Array of matching skills with confidence scores
 */
export async function querySkills(intent, options = {}) {
  const apiKey = getApiKey();
  const { topK = 5 } = options;

  const requestBody = JSON.stringify({
    query: intent,
    topK
  });

  const response = await httpsRequest(routerQueryUrl(), {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: requestBody,
  });

  if (response.statusCode !== 200) {
    throw new Error(`Query failed with status ${response.statusCode}: ${truncateBody(response.body)}`);
  }

  let result;
  try {
    result = JSON.parse(response.body);
  } catch (err) {
    throw new Error(`Failed to parse query response: ${err.message}`);
  }

  return parseQueryResponse(result);
}

/**
 * CLI entry point for testing query functionality.
 */
async function main() {
  const intent = process.argv[2];
  const topK = parseInt(process.argv[3], 10) || 5;

  if (!intent) {
    console.error('Usage: node query.mjs <intent> [topK]');
    console.error('Example: node query.mjs "detect person falling" 3');
    process.exit(1);
  }

  try {
    const skills = await querySkills(intent, { topK });
    console.log(JSON.stringify({
      success: true,
      intent,
      count: skills.length,
      skills
    }, null, 2));
  } catch (err) {
    console.error(JSON.stringify({
      success: false,
      error: err.message
    }, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
