#!/usr/bin/env node

/**
 * Agent Matchmaker — Analyzer
 * Scans ClawFriend agents and generates compatibility matches
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Load config
const CONFIG_PATH = path.join(__dirname, '../preferences/matchmaker.json');
const MATCHES_PATH = path.join(__dirname, '../data/matches.json');
const SKILLS_PATH = path.join(__dirname, '../data/agent-skills.json');

const defaultConfig = {
  scanFrequency: '6h',
  postFrequency: '12h',
  minCompatibilityScore: 0.65,
  focusAreas: ['DeFi', 'automation', 'crypto-native', 'agents'],
  excludeAgents: ['leoz'],
  maxAgentsToScan: 50,
};

const loadConfig = () => {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  }
  return defaultConfig;
};

const ensureDataDir = () => {
  const dir = path.join(__dirname, '../data');
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
};

/**
 * Fetch agents from ClawFriend API
 */
const fetchAgents = async (limit = 50) => {
  const apiKey = process.env.CLAW_FRIEND_API_KEY;
  if (!apiKey) {
    console.error('❌ CLAW_FRIEND_API_KEY not set');
    process.exit(1);
  }

  return new Promise((resolve, reject) => {
    const url = `https://api.clawfriend.ai/v1/agents?limit=${limit}`;
    const options = {
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
      },
    };

    https.get(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.data || []);
        } catch (e) {
          reject(new Error(`Failed to parse agents: ${e.message}`));
        }
      });
    }).on('error', reject);
  });
};

/**
 * Extract skills from agent bio and activity
 */
const extractSkills = (agent) => {
  const skills = [];
  const bioLower = ((agent.bio || agent.description || agent.displayName) || '').toLowerCase();
  
  const skillKeywords = {
    'DeFi': ['defi', 'trading', 'yield', 'liquidity', 'swap'],
    'Automation': ['automation', 'bot', 'orchestrate', 'workflow'],
    'Analysis': ['alpha', 'signal', 'analysis', 'research', 'predict'],
    'Community': ['community', 'social', 'engagement', 'network'],
    'Infrastructure': ['infra', 'infrastructure', 'protocol', 'blockchain'],
    'Data': ['data', 'analytics', 'metrics', 'dashboard'],
  };

  for (const [skill, keywords] of Object.entries(skillKeywords)) {
    if (keywords.some((kw) => bioLower.includes(kw))) {
      skills.push(skill);
    }
  }

  return skills.length > 0 ? skills : ['General'];
};

/**
 * Calculate compatibility score between two agents
 */
const calculateCompatibility = (agent1, agent2, config) => {
  let score = 0;

  // Skill complementarity (0.4 weight)
  const skills1 = extractSkills(agent1);
  const skills2 = extractSkills(agent2);
  const skillOverlap = skills1.filter((s) => skills2.includes(s)).length;
  const skillUnion = new Set([...skills1, ...skills2]).size;
  const skillMatch = skillUnion > 0 ? (skillUnion - skillOverlap) / skillUnion : 0;
  score += skillMatch * 0.4;

  // Vibe alignment (0.3 weight)
  const bio1 = (agent1.bio || agent1.description || agent1.displayName || '').toLowerCase();
  const bio2 = (agent2.bio || agent2.description || agent2.displayName || '').toLowerCase();
  const focusArea1 = config.focusAreas.some((area) =>
    bio1.includes(area.toLowerCase())
  );
  const focusArea2 = config.focusAreas.some((area) =>
    bio2.includes(area.toLowerCase())
  );
  const vibeScore = focusArea1 && focusArea2 ? 0.8 : focusArea1 || focusArea2 ? 0.4 : 0.2;
  score += vibeScore * 0.3;

  // Mutual benefit (0.2 weight)
  const f1 = agent1.followersCount || agent1.followers || 0;
  const f2 = agent2.followersCount || agent2.followers || 0;
  const followerRatioDiff = Math.abs(f1 - f2) / Math.max(f1, f2, 1);
  const sizeMatch = 1 - Math.min(followerRatioDiff, 1);
  score += sizeMatch * 0.2;

  // Activity overlap (0.1 weight)
  const activityScore = 0.5; // Placeholder; could analyze tweet timestamps
  score += activityScore * 0.1;

  return Math.round(score * 100) / 100;
};

/**
 * Main scan function
 */
const scanAgents = async (config) => {
  console.log('🔍 Scanning ClawFriend agents...');

  try {
    const agents = await fetchAgents(config.maxAgentsToScan || 50);
    console.log(`✅ Fetched ${agents.length} agents`);

    const filtered = agents.filter((a) => !config.excludeAgents.includes(a.username));
    const matches = [];

    // Generate pairings
    for (let i = 0; i < filtered.length; i++) {
      for (let j = i + 1; j < filtered.length; j++) {
        const compatibility = calculateCompatibility(filtered[i], filtered[j], config);

        if (compatibility >= config.minCompatibilityScore) {
          matches.push({
            id: `match-${Date.now()}-${i}-${j}`,
            agent1: {
              id: filtered[i].id,
              username: filtered[i].username,
              followers: filtered[i].followers,
              skills: extractSkills(filtered[i]),
            },
            agent2: {
              id: filtered[j].id,
              username: filtered[j].username,
              followers: filtered[j].followers,
              skills: extractSkills(filtered[j]),
            },
            compatibility,
            reason: generateReason(filtered[i], filtered[j], compatibility),
            createdAt: new Date().toISOString(),
            posted: false,
          });
        }
      }
    }

    // Sort by compatibility
    matches.sort((a, b) => b.compatibility - a.compatibility);

    // Save results
    ensureDataDir();
    fs.writeFileSync(MATCHES_PATH, JSON.stringify(matches, null, 2));

    console.log(`\n✅ Generated ${matches.length} high-compatibility matches`);
    console.log(`📊 Top 5 matches:`);
    matches.slice(0, 5).forEach((m, i) => {
      console.log(`  ${i + 1}. @${m.agent1.username} + @${m.agent2.username} (${m.compatibility})`);
    });

    return matches;
  } catch (error) {
    console.error('❌ Scan failed:', error.message);
    process.exit(1);
  }
};

/**
 * Generate reason for pairing
 */
const generateReason = (a1, a2, score) => {
  const skills1 = extractSkills(a1);
  const skills2 = extractSkills(a2);
  const shared = skills1.filter((s) => skills2.includes(s));
  const unique = {
    agent1: skills1.filter((s) => !skills2.includes(s)),
    agent2: skills2.filter((s) => !skills1.includes(s)),
  };

  const reasons = [];
  if (unique.agent1.length > 0 && unique.agent2.length > 0) {
    reasons.push(`${unique.agent1[0]} + ${unique.agent2[0]}`);
  }
  const f1 = a1.followersCount || a1.followers || 0;
  const f2 = a2.followersCount || a2.followers || 0;
  if (f1 > 100 && f2 < 100) {
    reasons.push('growth opportunity');
  }

  return reasons.join(' + ') || 'complementary strengths';
};

// CLI - only run if called directly
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args[0] === 'scan') {
    const config = loadConfig();
    const limitIdx = args.indexOf('--limit');
    if (limitIdx !== -1) {
      config.maxAgentsToScan = parseInt(args[limitIdx + 1]) || 50;
    }
    scanAgents(config).catch((e) => {
      console.error('Error:', e);
      process.exit(1);
    });
  } else {
    console.log('Usage: node analyze.js scan [--limit 50]');
    process.exit(0);
  }
}

module.exports = { scanAgents, calculateCompatibility };
