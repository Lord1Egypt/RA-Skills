#!/usr/bin/env node

/**
 * buzz-scan.mjs — Token Discovery Scanner for Buzz BD OpenClaw Skill
 * 
 * Scans DexScreener API for trending tokens across Solana, Ethereum, and BSC.
 * Scores each token on a 100-point system and returns top prospects.
 * 
 * Usage:
 *   node scripts/buzz-scan.mjs                    # Scan all chains
 *   node scripts/buzz-scan.mjs --chain solana      # Scan specific chain
 *   node scripts/buzz-scan.mjs --token <address>   # Score specific token
 *   node scripts/buzz-scan.mjs --top 10            # Return top 10 per chain
 *   node scripts/buzz-scan.mjs --min-score 70      # Only show score >= 70
 * 
 * Environment:
 *   DEXSCREENER_ENABLED=true (required by skill metadata)
 * 
 * ERC-8004: BuzzBD — ETH #25045, Base #17483
 * License: MIT
 */

const CHAINS = {
  solana: { tag: '[SOL]', dexId: 'solana', listingFee: '$5,000' },
  ethereum: { tag: '[ETH]', dexId: 'ethereum', listingFee: '$7,500' },
  bsc: { tag: '[BSC]', dexId: 'bsc', listingFee: '$7,500' }
};

const DEXSCREENER_API = 'https://api.dexscreener.com';

// --- Scoring Weights ---
const WEIGHTS = {
  marketCap: 0.20,
  liquidity: 0.25,
  volume24h: 0.20,
  social: 0.15,
  age: 0.10,
  team: 0.10
};

// --- Score Thresholds ---
function scoreMarketCap(mc) {
  if (!mc || mc <= 0) return 0;
  if (mc >= 10_000_000) return 100;
  if (mc >= 5_000_000) return 85;
  if (mc >= 1_000_000) return 70;
  if (mc >= 500_000) return 50;
  return 25;
}

function scoreLiquidity(liq) {
  if (!liq || liq <= 0) return 0;
  if (liq >= 500_000) return 100;
  if (liq >= 200_000) return 80;
  if (liq >= 100_000) return 60;
  if (liq >= 50_000) return 40;
  return 20;
}

function scoreVolume(vol) {
  if (!vol || vol <= 0) return 0;
  if (vol >= 1_000_000) return 100;
  if (vol >= 500_000) return 80;
  if (vol >= 100_000) return 60;
  if (vol >= 50_000) return 40;
  return 20;
}

function scoreSocial(pair) {
  let score = 0;
  const info = pair.info || {};
  if (info.websites && info.websites.length > 0) score += 30;
  if (info.socials) {
    const socials = info.socials;
    if (socials.find(s => s.type === 'twitter')) score += 30;
    if (socials.find(s => s.type === 'telegram')) score += 20;
    if (socials.find(s => s.type === 'discord')) score += 10;
    if (socials.length >= 3) score += 10;
  }
  return Math.min(score, 100);
}

function scoreAge(pairCreatedAt) {
  if (!pairCreatedAt) return 30; // unknown = moderate
  const ageMs = Date.now() - pairCreatedAt;
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  if (ageDays >= 180) return 100;  // 6+ months
  if (ageDays >= 90) return 80;
  if (ageDays >= 30) return 60;
  if (ageDays >= 7) return 40;
  return 20; // very new
}

function scoreTeam(pair) {
  // Heuristic: if token has website + multiple socials + not a meme indicator
  let score = 50; // baseline
  const info = pair.info || {};
  if (info.websites && info.websites.length > 0) score += 20;
  if (info.socials && info.socials.length >= 2) score += 15;
  if (info.imageUrl) score += 15;
  return Math.min(score, 100);
}

function computeScore(pair) {
  const mc = parseFloat(pair.marketCap) || 0;
  const liq = parseFloat(pair.liquidity?.usd) || 0;
  const vol = parseFloat(pair.volume?.h24) || 0;

  const scores = {
    marketCap: scoreMarketCap(mc),
    liquidity: scoreLiquidity(liq),
    volume24h: scoreVolume(vol),
    social: scoreSocial(pair),
    age: scoreAge(pair.pairCreatedAt),
    team: scoreTeam(pair)
  };

  const total = Math.round(
    scores.marketCap * WEIGHTS.marketCap +
    scores.liquidity * WEIGHTS.liquidity +
    scores.volume24h * WEIGHTS.volume24h +
    scores.social * WEIGHTS.social +
    scores.age * WEIGHTS.age +
    scores.team * WEIGHTS.team
  );

  return { total, breakdown: scores };
}

function getCategory(score) {
  if (score >= 85) return '🔥 HOT';
  if (score >= 70) return '✅ Qualified';
  if (score >= 50) return '👀 Watch';
  return '❌ Skip';
}

function formatUsd(n) {
  if (!n || n <= 0) return '$0';
  if (n >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(2)}B`;
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(1)}K`;
  return `$${n.toFixed(0)}`;
}

// --- API Calls ---
async function fetchTrending(chainId) {
  const url = `${DEXSCREENER_API}/token-boosts/top/v1`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`DexScreener API error: ${res.status}`);
  const data = await res.json();
  // Filter by chain
  return (data || []).filter(t => t.chainId === chainId);
}

async function fetchTokenPairs(chainId, address) {
  const url = `${DEXSCREENER_API}/tokens/v1/${chainId}/${address}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`DexScreener API error: ${res.status}`);
  return await res.json();
}

async function fetchLatestPairs(chainId) {
  const url = `${DEXSCREENER_API}/token-profiles/latest/v1`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`DexScreener API error: ${res.status}`);
  const data = await res.json();
  return (data || []).filter(t => t.chainId === chainId);
}

// --- Main ---
async function scanChain(chainKey, topN = 5, minScore = 50) {
  const chain = CHAINS[chainKey];
  if (!chain) throw new Error(`Unknown chain: ${chainKey}`);

  console.log(`\n🐝 Scanning ${chain.tag} via DexScreener...`);

  try {
    // Get boosted tokens (trending)
    const boosted = await fetchTrending(chain.dexId);
    
    if (!boosted || boosted.length === 0) {
      console.log(`  No trending tokens found on ${chainKey}`);
      return [];
    }

    // Score each — fetch pair data for detailed scoring
    const scored = [];
    const seen = new Set();

    for (const token of boosted.slice(0, 20)) {
      if (seen.has(token.tokenAddress)) continue;
      seen.add(token.tokenAddress);

      try {
        const pairs = await fetchTokenPairs(chain.dexId, token.tokenAddress);
        if (!pairs || pairs.length === 0) continue;

        // Use highest-liquidity pair
        const bestPair = pairs.sort((a, b) => 
          (parseFloat(b.liquidity?.usd) || 0) - (parseFloat(a.liquidity?.usd) || 0)
        )[0];

        const { total, breakdown } = computeScore(bestPair);
        
        if (total >= minScore) {
          scored.push({
            name: bestPair.baseToken?.name || 'Unknown',
            symbol: bestPair.baseToken?.symbol || '???',
            chain: chainKey,
            tag: chain.tag,
            contract: bestPair.baseToken?.address || token.tokenAddress,
            pairAddress: bestPair.pairAddress,
            score: total,
            breakdown,
            category: getCategory(total),
            marketCap: parseFloat(bestPair.marketCap) || 0,
            liquidity: parseFloat(bestPair.liquidity?.usd) || 0,
            volume24h: parseFloat(bestPair.volume?.h24) || 0,
            priceChange24h: parseFloat(bestPair.priceChange?.h24) || 0,
            pairCreatedAt: bestPair.pairCreatedAt,
            url: bestPair.url || `https://dexscreener.com/${chain.dexId}/${bestPair.pairAddress}`,
            socials: bestPair.info?.socials || [],
            websites: bestPair.info?.websites || [],
            listingFee: chain.listingFee
          });
        }
      } catch (e) {
        // Skip individual token errors
        continue;
      }
    }

    // Sort by score descending
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, topN);
  } catch (e) {
    console.error(`  Error scanning ${chainKey}: ${e.message}`);
    return [];
  }
}

function printResults(results, chain) {
  const tag = CHAINS[chain]?.tag || chain;
  
  if (results.length === 0) {
    console.log(`\n${tag} — No qualifying tokens found`);
    return;
  }

  console.log(`\n🐝 BUZZ SCAN — ${tag}`);
  console.log('━'.repeat(60));

  results.forEach((t, i) => {
    const change = t.priceChange24h >= 0 ? `+${t.priceChange24h.toFixed(1)}%` : `${t.priceChange24h.toFixed(1)}%`;
    console.log(`\n${i + 1}. ${t.symbol} (${t.name}) | ${t.category} — ${t.score}/100`);
    console.log(`   MC: ${formatUsd(t.marketCap)} | Liq: ${formatUsd(t.liquidity)} | Vol: ${formatUsd(t.volume24h)} | 24h: ${change}`);
    console.log(`   Contract: ${t.contract}`);
    console.log(`   DexScreener: ${t.url}`);
    if (t.socials.length > 0) {
      const socialStr = t.socials.map(s => `${s.type}: ${s.url}`).join(' | ');
      console.log(`   Socials: ${socialStr}`);
    }
    console.log(`   Listing fee: ${t.listingFee}`);
  });

  console.log('\n' + '━'.repeat(60));
}

// --- CLI ---
async function main() {
  const args = process.argv.slice(2);
  
  let chainFilter = null;
  let tokenAddress = null;
  let topN = 5;
  let minScore = 50;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--chain' && args[i + 1]) chainFilter = args[++i].toLowerCase();
    if (args[i] === '--token' && args[i + 1]) tokenAddress = args[++i];
    if (args[i] === '--top' && args[i + 1]) topN = parseInt(args[++i]);
    if (args[i] === '--min-score' && args[i + 1]) minScore = parseInt(args[++i]);
  }

  console.log('🐝 BuzzBD Token Scanner v1.0.0');
  console.log(`   ERC-8004: ETH #25045 | Base #17483`);
  console.log(`   Chains: ${chainFilter || 'all'} | Top: ${topN} | Min Score: ${minScore}`);

  // Single token lookup
  if (tokenAddress) {
    const chain = chainFilter || 'solana';
    console.log(`\nLooking up ${tokenAddress} on ${chain}...`);
    const pairs = await fetchTokenPairs(CHAINS[chain].dexId, tokenAddress);
    if (pairs && pairs.length > 0) {
      const best = pairs[0];
      const { total, breakdown } = computeScore(best);
      console.log(`\n${best.baseToken?.symbol} | Score: ${total}/100 | ${getCategory(total)}`);
      console.log(`Breakdown:`, JSON.stringify(breakdown, null, 2));
    } else {
      console.log('Token not found on DexScreener');
    }
    return;
  }

  // Multi-chain scan
  const chains = chainFilter ? [chainFilter] : Object.keys(CHAINS);
  const allResults = {};
  const crossRef = {};

  for (const chain of chains) {
    const results = await scanChain(chain, topN, minScore);
    allResults[chain] = results;
    printResults(results, chain);

    // Track cross-references
    for (const t of results) {
      const key = t.symbol.toLowerCase();
      if (!crossRef[key]) crossRef[key] = [];
      crossRef[key].push({ chain, score: t.score, contract: t.contract });
    }
  }

  // High conviction (appears on multiple chains)
  const multiChain = Object.entries(crossRef).filter(([, v]) => v.length > 1);
  if (multiChain.length > 0) {
    console.log('\n⭐ HIGH CONVICTION — Multi-chain presence:');
    for (const [symbol, chains] of multiChain) {
      const chainsStr = chains.map(c => `${CHAINS[c.chain]?.tag} ${c.score}pts`).join(' + ');
      console.log(`   ${symbol.toUpperCase()} — ${chainsStr}`);
    }
  }

  // Summary
  const totalFound = Object.values(allResults).flat().length;
  const hotCount = Object.values(allResults).flat().filter(t => t.score >= 85).length;
  const qualCount = Object.values(allResults).flat().filter(t => t.score >= 70 && t.score < 85).length;

  console.log(`\n📊 SUMMARY: ${totalFound} tokens found | 🔥 HOT: ${hotCount} | ✅ Qualified: ${qualCount}`);
  console.log(`🐝 BuzzBD scan complete`);

  // Output JSON for piping
  if (args.includes('--json')) {
    console.log('\n--- JSON ---');
    console.log(JSON.stringify(allResults, null, 2));
  }
}

main().catch(e => {
  console.error('Fatal error:', e.message);
  process.exit(1);
});
