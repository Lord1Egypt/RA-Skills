/**
 * eliza-adapter.mjs — elizaOS Plugin Adapter for Buzz BD
 * 
 * REVERSED PATTERN: This adapter maps FROM the OpenClaw SKILL.md format
 * TO elizaOS Actions/Providers/Services. The OpenClaw skill is the primary
 * interface; this adapter is secondary.
 * 
 * OpenClaw SKILL.md (primary) → elizaOS Plugin (this file) → Agent Bounty Board
 * 
 * ERC-8004: BuzzBD — ETH #25045, Base #17483
 */

// --- elizaOS Action Definitions ---
// These map 1:1 to the OpenClaw /buzz commands

export const BUZZ_TOKEN_INTELLIGENCE = {
  name: 'BUZZ_TOKEN_INTELLIGENCE',
  description: 'Full token analysis with scoring — maps to /buzz score <token>',
  examples: [
    [
      { user: 'agent', content: { text: 'Analyze RENDER token on Ethereum' } },
      { user: 'buzz', content: { text: 'RENDER | Score: 82/100 | ✅ Qualified | MC: $2.1B | Liq: $45M' } }
    ]
  ],
  handler: async (runtime, message) => {
    // Delegates to scripts/buzz-scan.mjs --token <address> --chain <chain>
    const { execSync } = await import('child_process');
    const skillDir = new URL('.', import.meta.url).pathname;
    const result = execSync(
      `node ${skillDir}scripts/buzz-scan.mjs --token "${message.content.text}" --json`,
      { encoding: 'utf-8', timeout: 30000 }
    );
    return { text: result };
  }
};

export const BUZZ_LISTING_PROSPECTS = {
  name: 'BUZZ_LISTING_PROSPECTS',
  description: 'Current pipeline prospects scoring ≥70 — maps to /buzz scan --min-score 70',
  handler: async (runtime) => {
    const { execSync } = await import('child_process');
    const skillDir = new URL('.', import.meta.url).pathname;
    const result = execSync(
      `node ${skillDir}scripts/buzz-scan.mjs --min-score 70 --json`,
      { encoding: 'utf-8', timeout: 60000 }
    );
    return { text: result };
  }
};

export const BUZZ_AGENT_STATUS = {
  name: 'BUZZ_AGENT_STATUS',
  description: 'Full agent status — maps to /buzz status',
  handler: async () => {
    return {
      text: JSON.stringify({
        agent: 'BuzzBD',
        version: '1.0.0',
        erc8004: { ethereum: '#25045', base: '#17483' },
        sources: 15,
        crons: 26,
        model: 'MiniMax M2.5-highspeed via AkashML',
        platform: 'Akash Network',
        x402: 'USDC on Solana via PayAI',
        skill_format: 'openclaw-first (reversed pattern)'
      }, null, 2)
    };
  }
};

export const BUZZ_MOMENTUM_SCAN = {
  name: 'BUZZ_MOMENTUM_SCAN',
  description: 'Latest trending tokens across all chains — maps to /buzz scan',
  handler: async () => {
    const { execSync } = await import('child_process');
    const skillDir = new URL('.', import.meta.url).pathname;
    const result = execSync(
      `node ${skillDir}scripts/buzz-scan.mjs --json`,
      { encoding: 'utf-8', timeout: 60000 }
    );
    return { text: result };
  }
};

// --- elizaOS Provider ---
export const buzzIntelProvider = {
  name: 'buzz-intelligence',
  description: 'Provides real-time token intelligence from Buzz BD pipeline',
  get: async (runtime) => {
    // Returns current pipeline summary for other agents to query
    return {
      agent: 'BuzzBD',
      erc8004: { ethereum: 25045, base: 17483 },
      capabilities: ['token_scan', 'token_score', 'prospect_brief', 'cross_reference'],
      chains: ['solana', 'ethereum', 'bsc'],
      scoring: '100-point system',
      source_format: 'openclaw-skill-first'
    };
  }
};

// --- elizaOS Service ---
export const buzzBDService = {
  name: 'buzz-bd-service',
  description: 'Buzz BD background service for periodic scanning',
  start: async (runtime) => {
    console.log('🐝 Buzz BD Service started (OpenClaw-first pattern)');
    console.log('   ERC-8004: ETH #25045 | Base #17483');
    console.log('   Source: OpenClaw SKILL.md → elizaOS adapter');
  },
  stop: async () => {
    console.log('🐝 Buzz BD Service stopped');
  }
};

// --- Plugin Export ---
export default {
  name: '@solcex/plugin-buzz-bd',
  description: 'Buzz BD Agent — Token Discovery & BD Intelligence (OpenClaw-first)',
  actions: [
    BUZZ_TOKEN_INTELLIGENCE,
    BUZZ_LISTING_PROSPECTS,
    BUZZ_AGENT_STATUS,
    BUZZ_MOMENTUM_SCAN
  ],
  providers: [buzzIntelProvider],
  services: [buzzBDService]
};
