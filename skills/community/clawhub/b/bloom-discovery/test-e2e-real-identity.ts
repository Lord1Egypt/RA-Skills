/**
 * Real E2E test: conversation text → PersonalityAnalyzer → Identity Card → Recommendations
 *
 * Uses BloomIdentitySkillV2.execute() with conversationText input,
 * exactly like the OpenClaw bot would call it.
 */

import { BloomIdentitySkillV2, ExecutionMode } from './src/bloom-identity-skill-v2';

// Realistic conversation that an OpenClaw bot would forward
// Must use User:/Assistant: prefixes — the data collector splits on these
const CONVERSATION_TEXT = `
User: I've been building AI agents with LangChain and exploring multi-agent orchestration patterns. Really interested in MCP servers and context engineering for better RAG pipelines.
Assistant: That's a great area to be exploring! Multi-agent orchestration is becoming increasingly important. Are you using any specific frameworks?
User: Yeah I'm using LangGraph mostly, and I built a custom agent harness for my workflow. I also trade crypto on the side — mostly DeFi on Base chain and some Solana degen plays. Been looking at prediction markets like Polymarket for information aggregation.
Assistant: Interesting combination of interests! The intersection of AI agents and crypto/DeFi is a growing space. What tools do you use day to day?
User: I use Claude Code daily for my development workflow and want to find more productivity tools. I'm working on an autonomous agent that can browse the web and execute tasks. Recently set up a vector database for semantic search across my codebase.
Assistant: Sounds like you're deep into the agentic AI space. Have you looked into context engineering patterns?
User: Yes! I think the future is agentic workflows where AI handles most of the grunt work. I've been experimenting with different context window management strategies and building custom MCP servers for my tools.
Assistant: That's a very forward-thinking approach. Context engineering is becoming a discipline of its own.
User: Exactly. I also want to integrate on-chain data into my agent workflows — like pulling DeFi yields and prediction market odds automatically. The combination of AI agents + crypto rails is super powerful.
`;

async function run() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║   REAL E2E: Conversation → Identity Card → Skills      ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');

  const skill = new BloomIdentitySkillV2();

  // Point to production API for full E2E (save + recommendations)
  process.env.BLOOM_API_URL = process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';

  const start = Date.now();
  const result = await skill.execute('e2e-test-user', {
    mode: ExecutionMode.DATA_ONLY,
    conversationText: CONVERSATION_TEXT,
    skipShare: true,
  });
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  console.log(`\n${'═'.repeat(58)}`);
  console.log(`Pipeline completed in ${elapsed}s\n`);

  if (!result.success || !result.identityData) {
    console.log('❌ FAILED:', result.error);
    process.exit(1);
  }

  const id = result.identityData;

  // ── Identity Card ─────────────────────────────────────────────────
  console.log('━━━ IDENTITY CARD ━━━\n');
  console.log(`🎭 Personality Type: ${id.personalityType}`);
  console.log(`📌 Tagline: ${id.customTagline}`);
  console.log(`📝 Description: ${id.customDescription}`);
  if (id.customLongDescription) {
    console.log(`📝 Long Description: ${id.customLongDescription}`);
  }
  console.log(`\n📂 Main Categories: ${id.mainCategories.join(', ')}`);
  console.log(`📂 Sub Categories:  ${id.subCategories.join(', ')}`);

  if (id.dimensions) {
    console.log(`\n📊 Dimensions:`);
    console.log(`   Conviction:    ${id.dimensions.conviction}/100`);
    console.log(`   Intuition:     ${id.dimensions.intuition}/100`);
    console.log(`   Contribution:  ${id.dimensions.contribution}/100`);
  }

  if (id.tasteSpectrums) {
    const ts = id.tasteSpectrums;
    console.log(`\n🎨 Taste Spectrums:`);
    console.log(`   Learning:  ${ts.learning}/100 (${ts.learning < 40 ? 'try-first' : ts.learning > 60 ? 'study-first' : 'balanced'})`);
    console.log(`   Decision:  ${ts.decision}/100 (${ts.decision < 40 ? 'gut' : ts.decision > 60 ? 'deliberate' : 'balanced'})`);
    console.log(`   Novelty:   ${ts.novelty}/100 (${ts.novelty < 40 ? 'pioneer' : ts.novelty > 60 ? 'pragmatist' : 'balanced'})`);
    console.log(`   Risk:      ${ts.risk}/100 (${ts.risk < 40 ? 'all-in' : ts.risk > 60 ? 'diversified' : 'balanced'})`);
  }

  if (id.strengths?.length) {
    console.log(`\n💪 Strengths: ${id.strengths.join(', ')}`);
  }

  if (id.hiddenInsight) {
    console.log(`\n🔮 Hidden Insight [${id.hiddenInsight.patternType}]: ${id.hiddenInsight.brief}`);
    console.log(`   ${id.hiddenInsight.narrative}`);
  }

  if (id.aiPlaybook) {
    console.log(`\n📖 AI Playbook:`);
    console.log(`   Leverage:  ${id.aiPlaybook.leverage}`);
    console.log(`   Watch Out: ${id.aiPlaybook.watchOut}`);
    console.log(`   Next Move: ${id.aiPlaybook.nextMove}`);
  }

  // ── Recommendations ───────────────────────────────────────────────
  const recs = result.recommendations || [];
  console.log(`\n━━━ RECOMMENDATIONS (${recs.length} skills) ━━━\n`);

  const groups: Record<string, typeof recs> = {};
  for (const r of recs) {
    const g = r.categoryGroup || 'ungrouped';
    if (!groups[g]) groups[g] = [];
    groups[g].push(r);
  }

  for (const [cat, skills] of Object.entries(groups)) {
    console.log(`📂 ${cat} (${skills.length})`);
    for (const s of skills) {
      console.log(`   ${String(s.matchScore).padStart(3)}pts │ ${s.skillName}`);
      console.log(`         │ ${s.url}`);
      console.log(`         │ ${s.reason}`);
    }
    console.log('');
  }

  // ── Validation ────────────────────────────────────────────────────
  console.log('━━━ VALIDATION ━━━\n');
  let issues = 0;
  const check = (name: string, ok: boolean) => {
    console.log(`  ${ok ? '✅' : '❌'} ${name}`);
    if (!ok) issues++;
  };

  check('Identity card generated', !!id.personalityType);
  check('Has tagline', !!id.customTagline);
  check('Has description', !!id.customDescription);
  check('Has mainCategories', id.mainCategories.length > 0);
  check('Has dimensions', !!id.dimensions);
  check('Has tasteSpectrums', !!id.tasteSpectrums);
  check('Has recommendations', recs.length > 0);
  check('Multiple category groups', Object.keys(groups).length >= 2);
  check('All URLs absolute', recs.every(r => r.url?.startsWith('https://')));
  check('All have reason', recs.every(r => !!r.reason));
  check('All have source', recs.every(r => r.source === 'catalog'));
  check('Per-category <= 5', Object.values(groups).every(g => g.length <= 5));

  console.log(`\n${'═'.repeat(58)}`);
  console.log(issues === 0
    ? '✅ FULL E2E PASSED — Real Identity Card + Recommendations'
    : `❌ ${issues} ISSUES`
  );
  console.log('═'.repeat(58));
  process.exit(issues === 0 ? 0 : 1);
}

run().catch(err => {
  console.error('CRASH:', err);
  process.exit(1);
});
