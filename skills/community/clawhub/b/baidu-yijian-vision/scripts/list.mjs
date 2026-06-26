#!/usr/bin/env node

import { querySkills } from './query.mjs';
import { fileURLToPath } from 'url';

/**
 * Format skills list as JSON result.
 * @param {string} intent - The query intent
 * @param {Array} skills - Array of skill objects
 * @returns {object} JSON-serializable result
 */
export function formatListResult(intent, skills) {
  return {
    success: true,
    intent,
    count: skills.length,
    skills: skills.map(s => ({
      epId: s.epId,
      name: s.name || null,
      description: s.description || null,
      confidence: s.confidence,
    })),
  };
}

async function main() {
  const intent = process.argv[2];
  const topK = parseInt(process.argv[3], 10) || 10;

  if (!intent) {
    console.error('Usage: node list.mjs <intent> [topK]');
    console.error('Example: node list.mjs "detect people falling" 5');
    process.exit(1);
  }

  try {
    const skills = await querySkills(intent, { topK });
    const result = formatListResult(intent, skills);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message }, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
