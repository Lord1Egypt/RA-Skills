#!/usr/bin/env node

/**
 * E2E test for the full recommendation pipeline.
 * Calls refreshRecommendations() with a realistic identity and validates output.
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { refreshRecommendations } = require('./dist/recommendation-pipeline.js');

const TEST_IDENTITY = {
  personalityType: 'The Visionary',
  mainCategories: ['AI Tools', 'Agent Framework', 'Crypto'],
  subCategories: ['Productivity', 'Development'],
  dimensions: { conviction: 70, intuition: 60, contribution: 50 },
  tasteSpectrums: { learning: 35, decision: 55, novelty: 30, risk: 40 },
};

async function run() {
  console.log('=== E2E Recommendation Pipeline Test ===\n');
  console.log('Identity:', JSON.stringify(TEST_IDENTITY, null, 2), '\n');

  const start = Date.now();
  const results = await refreshRecommendations(TEST_IDENTITY);
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  console.log(`\n${'='.repeat(60)}`);
  console.log(`Pipeline returned ${results.length} recommendations in ${elapsed}s\n`);

  if (results.length === 0) {
    console.log('❌ FAIL — no recommendations returned');
    process.exit(1);
  }

  // Group by categoryGroup
  const groups = {};
  for (const r of results) {
    const g = r.categoryGroup || 'ungrouped';
    if (!groups[g]) groups[g] = [];
    groups[g].push(r);
  }

  for (const [cat, skills] of Object.entries(groups)) {
    console.log(`📂 ${cat} (${skills.length})`);
    for (const s of skills) {
      const src = s.source || '?';
      console.log(`   ${s.matchScore}pts  ${s.skillName}  [${src}]`);
      console.log(`           ${s.reason}`);
    }
    console.log('');
  }

  // Validate structure
  const first = results[0];
  const checks = [
    ['skillId', !!first.skillId],
    ['skillName', !!first.skillName],
    ['description', !!first.description],
    ['url', !!first.url],
    ['matchScore (number)', typeof first.matchScore === 'number'],
    ['categories (array)', Array.isArray(first.categories)],
    ['source (catalog|ClaudeCode|ClawHub)', ['catalog', 'ClaudeCode', 'ClawHub'].includes(first.source)],
    ['categoryGroup', !!first.categoryGroup],
    ['reason', !!first.reason],
    ['per-category <= 5', Object.values(groups).every(g => g.length <= 5)],
  ];

  console.log('Structure checks:');
  let allPass = true;
  for (const [name, ok] of checks) {
    console.log(`  ${ok ? '✅' : '❌'} ${name}`);
    if (!ok) allPass = false;
  }

  console.log(`\n${allPass ? '✅ ALL CHECKS PASSED' : '❌ SOME CHECKS FAILED'}`);
  process.exit(allPass ? 0 : 1);
}

run().catch(err => {
  console.error('❌ Pipeline crashed:', err);
  process.exit(1);
});
