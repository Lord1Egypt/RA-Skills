/**
 * E2E test that hits the REAL Bloom API to verify:
 * 1. Identity card saves successfully
 * 2. agentUserId is returned
 * 3. Dashboard URL is generated as https://bloomprotocol.ai/agents/{id}
 */

import { BloomIdentitySkillV2, ExecutionMode } from './src/bloom-identity-skill-v2';

const CONVERSATION_TEXT = `
User: I've been building AI agents with LangChain and exploring multi-agent orchestration patterns. Really interested in MCP servers and context engineering for better RAG pipelines.
Assistant: That's a great area to be exploring! Multi-agent orchestration is becoming increasingly important.
User: Yeah I'm using LangGraph mostly, and I built a custom agent harness for my workflow. I also trade crypto on the side — mostly DeFi on Base chain and some Solana degen plays.
Assistant: Interesting combination of interests!
User: I use Claude Code daily for my development workflow. I think the future is agentic workflows where AI handles most of the grunt work.
Assistant: That's a very forward-thinking approach.
User: Exactly. I want to integrate on-chain data into my agent workflows — like pulling DeFi yields and prediction market odds automatically.
`;

async function run() {
  console.log('=== E2E with REAL API — checking URL generation ===\n');

  // Use real API (default: https://api.bloomprotocol.ai)
  delete process.env.BLOOM_API_URL;

  const skill = new BloomIdentitySkillV2();
  const result = await skill.execute('e2e-url-test', {
    mode: ExecutionMode.DATA_ONLY,
    conversationText: CONVERSATION_TEXT,
    skipShare: true,
  });

  console.log('\n=== RESULT ===\n');
  console.log('success:', result.success);
  console.log('mode:', result.mode);

  if (result.identityData) {
    console.log('personalityType:', result.identityData.personalityType);
    console.log('tagline:', result.identityData.customTagline);
    console.log('mainCategories:', result.identityData.mainCategories);
    console.log('tasteSpectrums:', result.identityData.tasteSpectrums);
  }

  console.log('recommendations:', result.recommendations?.length, 'skills');
  console.log('dashboardUrl:', result.dashboardUrl);

  console.log('\n=== URL VALIDATION ===\n');

  const url = result.dashboardUrl;
  if (!url) {
    console.log('❌ No dashboardUrl returned — API save likely failed');
    process.exit(1);
  }

  const urlPattern = /^https:\/\/bloomprotocol\.ai\/agents\/\d+$/;
  const isValid = urlPattern.test(url);

  console.log(`URL: ${url}`);
  console.log(`Format matches /agents/{id}: ${isValid ? '✅' : '❌'}`);

  if (result.actions?.share) {
    console.log(`\nShare URL: ${result.actions.share.url}`);
    console.log(`Share text: ${result.actions.share.text}`);
  }

  if (result.actions?.save) {
    console.log(`\nRegister URL: ${result.actions.save.registerUrl}`);
  }

  // Check registration fields (merged agent-save + register)
  console.log('\n=== REGISTRATION VALIDATION ===\n');
  const reg = result.registration;
  if (reg) {
    console.log(`agentId: ${reg.agentId}`);
    console.log(`apiKey: ${reg.apiKey}`);
    console.log(`assignedTribe: ${reg.assignedTribe}`);
    console.log(`isNew: ${reg.isNew}`);
    const regValid = reg.apiKey?.startsWith('bk_') && ['build', 'raise', 'grow'].includes(reg.assignedTribe);
    console.log(`Registration valid: ${regValid ? '✅' : '❌'}`);
    if (!regValid) process.exit(1);
  } else {
    console.log('⚠️  No registration data returned (backend may not support platform field yet)');
  }

  process.exit(isValid ? 0 : 1);
}

run().catch(err => {
  console.error('CRASH:', err);
  process.exit(1);
});
