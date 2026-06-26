#!/usr/bin/env node

/**
 * Detailed E2E test — dump full recommendation objects to inspect format.
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
  const results = await refreshRecommendations(TEST_IDENTITY);

  console.log('\n\n========== FULL OUTPUT DUMP ==========\n');
  console.log(`Total: ${results.length} recommendations\n`);

  for (const [i, r] of results.entries()) {
    console.log(`--- #${i + 1} ---`);
    console.log(JSON.stringify(r, null, 2));
    console.log('');
  }

  // Check for issues
  console.log('========== FORMAT AUDIT ==========\n');
  let issues = 0;
  for (const r of results) {
    if (!r.url || r.url === 'undefined') {
      console.log(`❌ Missing URL: ${r.skillName}`);
      issues++;
    }
    if (!r.skillId) {
      console.log(`❌ Missing skillId: ${r.skillName}`);
      issues++;
    }
    if (!r.description || r.description.length < 10) {
      console.log(`❌ Bad description: ${r.skillName} → "${r.description}"`);
      issues++;
    }
    if (!r.reason) {
      console.log(`❌ Missing reason: ${r.skillName}`);
      issues++;
    }
    if (!r.source) {
      console.log(`❌ Missing source: ${r.skillName}`);
      issues++;
    }
    if (r.url && !r.url.startsWith('http')) {
      console.log(`❌ Invalid URL: ${r.skillName} → ${r.url}`);
      issues++;
    }
  }
  console.log(issues === 0 ? '✅ No format issues found' : `\n❌ ${issues} issues found`);
}

run().catch(err => { console.error('CRASH:', err); process.exit(1); });
