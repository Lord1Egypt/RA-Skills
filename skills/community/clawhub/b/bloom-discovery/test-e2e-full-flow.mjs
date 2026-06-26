#!/usr/bin/env node

/**
 * Full E2E test: Identity Card generation → Recommendation Pipeline
 *
 * Simulates the OpenClaw bot flow:
 *   conversationText → PersonalityAnalyzer → Identity Card → refreshRecommendations → output
 *
 * Skips API save (no real userId) but validates the entire local pipeline.
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// We need to import the built skill class — build with tsc first won't work
// because of transitive deps. Instead, call the pipeline + analyzer directly.
// But the real test is through execute(). Let's use tsx to run .ts directly.

// Actually, let's test both layers:
// Layer 1: PersonalityAnalyzer + category detection (the identity card)
// Layer 2: refreshRecommendations (the pipeline)

const { refreshRecommendations } = require('./dist/recommendation-pipeline.js');

// ── Simulate what PersonalityAnalyzer produces ──────────────────────

// Realistic conversation text (what an OpenClaw bot would forward)
const CONVERSATION_TEXT = `
I've been building AI agents with LangChain and exploring multi-agent orchestration patterns.
Really interested in MCP servers and context engineering for better RAG pipelines.
I also trade crypto on the side — mostly DeFi on Base chain and some Solana degen plays.
Been looking at prediction markets like Polymarket for information aggregation.
I use Claude Code daily for my development workflow and want to find more productivity tools.
`;

// This is what the PersonalityAnalyzer would produce from the above conversation
const MOCK_IDENTITY = {
  personalityType: 'The Visionary',
  customTagline: 'The Agent Architect',
  customDescription: 'You are building the future of AI agent infrastructure. Your deep interest in multi-agent orchestration, context engineering, and MCP ecosystems reveals a systems thinker who sees connections others miss.',
  customLongDescription: 'You are building the future of AI agent infrastructure. Your deep interest in multi-agent orchestration, context engineering, and MCP ecosystems reveals a systems thinker who sees connections others miss. Your crypto engagement on Base and Solana shows you back your convictions with real capital, while your use of prediction markets signals a data-driven approach to decision-making.',
  mainCategories: ['Agent Framework', 'Crypto', 'Coding Assistant'],
  subCategories: ['MCP Ecosystem', 'Context Engineering', 'Prediction Market'],
  dimensions: {
    conviction: 72,
    intuition: 65,
    contribution: 48,
  },
  tasteSpectrums: {
    learning: 30,   // try-first
    decision: 45,   // balanced
    novelty: 25,    // early-adopter
    risk: 35,       // bold
  },
  strengths: ['Systems Thinking', 'Early Adoption', 'Cross-Domain Integration'],
};

async function run() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║   FULL E2E: Identity Card → Recommendation Pipeline    ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');

  // ── Step 1: Display the Identity Card ─────────────────────────────
  console.log('━━━ STEP 1: Identity Card ━━━\n');
  console.log(`🎭 Personality: ${MOCK_IDENTITY.personalityType}`);
  console.log(`📌 Tagline: ${MOCK_IDENTITY.customTagline}`);
  console.log(`📝 Description: ${MOCK_IDENTITY.customDescription}`);
  console.log(`\n📂 Main Categories: ${MOCK_IDENTITY.mainCategories.join(', ')}`);
  console.log(`📂 Sub Categories:  ${MOCK_IDENTITY.subCategories.join(', ')}`);
  console.log(`\n📊 Dimensions:`);
  console.log(`   Conviction:    ${MOCK_IDENTITY.dimensions.conviction}/100`);
  console.log(`   Intuition:     ${MOCK_IDENTITY.dimensions.intuition}/100`);
  console.log(`   Contribution:  ${MOCK_IDENTITY.dimensions.contribution}/100`);
  console.log(`\n🎨 Taste Spectrums:`);
  console.log(`   Learning:  ${MOCK_IDENTITY.tasteSpectrums.learning}/100 (${MOCK_IDENTITY.tasteSpectrums.learning < 40 ? 'try-first' : 'study-first'})`);
  console.log(`   Decision:  ${MOCK_IDENTITY.tasteSpectrums.decision}/100 (${MOCK_IDENTITY.tasteSpectrums.decision < 40 ? 'gut' : 'balanced'})`);
  console.log(`   Novelty:   ${MOCK_IDENTITY.tasteSpectrums.novelty}/100 (${MOCK_IDENTITY.tasteSpectrums.novelty < 40 ? 'early-adopter' : 'wait-and-see'})`);
  console.log(`   Risk:      ${MOCK_IDENTITY.tasteSpectrums.risk}/100 (${MOCK_IDENTITY.tasteSpectrums.risk < 40 ? 'bold' : 'cautious'})`);
  console.log(`\n💪 Strengths: ${MOCK_IDENTITY.strengths.join(', ')}`);

  // ── Step 2: Run Recommendation Pipeline ───────────────────────────
  console.log('\n━━━ STEP 2: Recommendation Pipeline ━━━\n');

  const pipelineInput = {
    mainCategories: MOCK_IDENTITY.mainCategories,
    subCategories: MOCK_IDENTITY.subCategories,
    personalityType: MOCK_IDENTITY.personalityType,
    dimensions: MOCK_IDENTITY.dimensions,
    tasteSpectrums: MOCK_IDENTITY.tasteSpectrums,
  };

  const start = Date.now();
  const recommendations = await refreshRecommendations(pipelineInput);
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  // ── Step 3: Display Recommendations ───────────────────────────────
  console.log(`\n━━━ STEP 3: Results (${recommendations.length} skills in ${elapsed}s) ━━━\n`);

  // Group by categoryGroup
  const groups = {};
  for (const r of recommendations) {
    const g = r.categoryGroup || 'ungrouped';
    if (!groups[g]) groups[g] = [];
    groups[g].push(r);
  }

  for (const [cat, skills] of Object.entries(groups)) {
    console.log(`\n📂 ${cat} (${skills.length} skills)`);
    console.log('─'.repeat(50));
    for (const s of skills) {
      console.log(`  ${String(s.matchScore).padStart(3)}pts │ ${s.skillName}`);
      console.log(`        │ ${s.url}`);
      console.log(`        │ ${s.reason}`);
      console.log(`        │ Source: ${s.source} │ Categories: ${s.categories.join(', ')}`);
    }
  }

  // ── Step 4: Simulate what gets saved to Bloom API ─────────────────
  console.log('\n━━━ STEP 4: API Payload (what gets POST to /x402/agent-save) ━━━\n');

  const apiPayload = {
    agentName: 'Bloom Discovery Agent',
    userId: 'test-user-123',
    identityData: {
      personalityType: MOCK_IDENTITY.personalityType,
      tagline: MOCK_IDENTITY.customTagline,
      description: MOCK_IDENTITY.customDescription,
      longDescription: MOCK_IDENTITY.customLongDescription,
      mainCategories: MOCK_IDENTITY.mainCategories,
      subCategories: MOCK_IDENTITY.subCategories,
      confidence: 78,
      mode: 'data',
      dimensions: MOCK_IDENTITY.dimensions,
      tasteSpectrums: MOCK_IDENTITY.tasteSpectrums,
      strengths: MOCK_IDENTITY.strengths,
      recommendations,
    },
  };

  // Print summary, not full payload
  console.log(`  agentName: ${apiPayload.agentName}`);
  console.log(`  userId: ${apiPayload.userId}`);
  console.log(`  identityData.personalityType: ${apiPayload.identityData.personalityType}`);
  console.log(`  identityData.tagline: ${apiPayload.identityData.tagline}`);
  console.log(`  identityData.mainCategories: [${apiPayload.identityData.mainCategories.join(', ')}]`);
  console.log(`  identityData.recommendations: ${apiPayload.identityData.recommendations.length} skills`);

  // ── Step 5: Validation ────────────────────────────────────────────
  console.log('\n━━━ STEP 5: Validation ━━━\n');

  let issues = 0;
  const check = (name, ok) => {
    console.log(`  ${ok ? '✅' : '❌'} ${name}`);
    if (!ok) issues++;
  };

  check('Has recommendations', recommendations.length > 0);
  check('Multiple categories covered', Object.keys(groups).length >= 2);
  check('Per-category <= 5', Object.values(groups).every(g => g.length <= 5));

  for (const r of recommendations) {
    if (!r.url || !r.url.startsWith('http')) {
      check(`URL valid: ${r.skillName}`, false);
    }
    if (!r.skillId) {
      check(`skillId present: ${r.skillName}`, false);
    }
    if (!r.reason) {
      check(`reason present: ${r.skillName}`, false);
    }
    if (!r.source || !['ClaudeCode', 'ClawHub'].includes(r.source)) {
      check(`source valid: ${r.skillName} (got: ${r.source})`, false);
    }
    if (!Array.isArray(r.categories) || r.categories.length === 0) {
      check(`categories present: ${r.skillName}`, false);
    }
  }

  // Check categories are canonical
  const { CANONICAL_CATEGORIES } = require('./dist/recommendation-pipeline.js');
  // CANONICAL_CATEGORIES might not be exported, check manually
  const knownCats = [
    'Agent Framework', 'Context Engineering', 'MCP Ecosystem',
    'Coding Assistant', 'AI Tools', 'Productivity', 'Wellness',
    'Education', 'Crypto', 'Lifestyle', 'Design', 'Development',
    'Marketing', 'Finance', 'Prediction Market', 'General',
  ];
  for (const r of recommendations) {
    for (const cat of r.categories) {
      if (!knownCats.includes(cat)) {
        check(`Canonical category: "${cat}" in ${r.skillName}`, false);
      }
    }
  }

  check('All URLs are absolute https://', recommendations.every(r => r.url?.startsWith('https://')));
  check('All skillIds are slug format', recommendations.every(r => /^[a-z0-9-]+$/.test(r.skillId)));
  check('All have categoryGroup', recommendations.every(r => !!r.categoryGroup));

  console.log(`\n${'═'.repeat(58)}`);
  console.log(issues === 0
    ? '✅ FULL E2E PIPELINE PASSED — Identity Card → Recommendations OK'
    : `❌ ${issues} ISSUES FOUND`
  );
  console.log('═'.repeat(58));

  process.exit(issues === 0 ? 0 : 1);
}

run().catch(err => {
  console.error('CRASH:', err);
  process.exit(1);
});
