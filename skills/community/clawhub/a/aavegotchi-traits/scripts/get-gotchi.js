#!/usr/bin/env node

import { ethers } from 'ethers';
import fetch from 'node-fetch';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const wearablesData = JSON.parse(
  readFileSync(join(__dirname, 'wearables-data.json'), 'utf-8')
);

const AAVEGOTCHI_CONTRACT = '0xa99c4b08201f2913db8d28e71d020c4298f29dbf';
const DEFAULT_BASE_RPC = 'https://mainnet.base.org';
const DEFAULT_SUBGRAPH_URL =
  'https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn';

const BASE_RPC = process.env.AAVEGOTCHI_RPC_URL || DEFAULT_BASE_RPC;
const SUBGRAPH_URL = process.env.AAVEGOTCHI_SUBGRAPH_URL === ''
  ? null
  : (process.env.AAVEGOTCHI_SUBGRAPH_URL || DEFAULT_SUBGRAPH_URL);

function intEnv(name, fallback) {
  const raw = process.env[name];
  if (!raw) return fallback;
  const parsed = Number(raw);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : fallback;
}

const SEARCH_BATCH_SIZE = intEnv('AAVEGOTCHI_SEARCH_BATCH_SIZE', 25);
const RPC_RETRIES = intEnv('AAVEGOTCHI_RPC_RETRIES', 4);
const RPC_RETRY_DELAY_MS = intEnv('AAVEGOTCHI_RPC_RETRY_DELAY_MS', 250);

const AAVEGOTCHI_ABI = [
  'function getAavegotchi(uint256 _tokenId) view returns (tuple(uint256 tokenId, string name, address owner, uint256 randomNumber, uint256 status, int16[6] numericTraits, int16[6] modifiedNumericTraits, uint16[16] equippedWearables, address collateral, address escrow, uint256 stakedAmount, uint256 minimumStake, uint256 kinship, uint256 lastInteracted, uint256 experience, uint256 toNextLevel, uint256 usedSkillPoints, uint256 level, uint256 hauntId, uint256 baseRarityScore, uint256 modifiedRarityScore, bool locked))',
  'function tokenByIndex(uint256 _index) view returns (uint256)',
  'function totalSupply() view returns (uint256)'
];

const ERC20_ABI = [
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)'
];

const TRAIT_NAMES = [
  'Energy',
  'Aggression',
  'Spookiness',
  'Brain Size',
  'Eye Shape',
  'Eye Color'
];

const TRAIT_EMOJIS = {
  Energy: '⚡',
  Aggression: '💥',
  Spookiness: '👻',
  'Brain Size': '🧠',
  'Eye Shape': '👁️',
  'Eye Color': '🎨'
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeName(name) {
  return String(name || '')
    .replace(/\u0000/g, '')
    .trim()
    .toLowerCase();
}

function isRateLimitError(error) {
  const primary = String(error?.shortMessage || error?.message || '').toLowerCase();
  const nested = String(error?.info?.error?.message || '').toLowerCase();
  const code = error?.info?.error?.code;

  return (
    primary.includes('rate limit') ||
    primary.includes('429') ||
    nested.includes('rate limit') ||
    nested.includes('over rate limit') ||
    code === -32016
  );
}

async function callWithRetry(label, fn) {
  let lastError = null;

  for (let attempt = 1; attempt <= RPC_RETRIES; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (!isRateLimitError(error) || attempt === RPC_RETRIES) {
        throw error;
      }

      const delay = RPC_RETRY_DELAY_MS * Math.pow(2, attempt - 1);
      console.log(`Rate limited on ${label}, retry ${attempt}/${RPC_RETRIES} in ${delay}ms...`);
      await sleep(delay);
    }
  }

  throw lastError || new Error(`Unknown error calling ${label}`);
}

async function querySubgraphByName(name) {
  if (!SUBGRAPH_URL) {
    return null;
  }

  const normalizedSearch = normalizeName(name);
  const query = `
    query GetGotchiByName($name: String!) {
      aavegotchis(where: { name_contains_nocase: $name }, first: 20) {
        id
        name
      }
    }
  `;

  try {
    console.log(`Querying subgraph for "${name}"...`);

    const response = await fetch(SUBGRAPH_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, variables: { name } })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const result = await response.json();
    if (result.errors?.length) {
      console.log(`Subgraph query returned errors: ${result.errors[0].message}`);
      return null;
    }

    const candidates = result.data?.aavegotchis || [];
    if (candidates.length === 0) {
      return null;
    }

    const exact = candidates.find((g) => normalizeName(g.name) === normalizedSearch);
    if (exact) {
      console.log(`✓ Found exact subgraph match: Gotchi #${exact.id} (${exact.name})`);
      return exact.id;
    }

    const best = candidates[0];
    console.log(`~ No exact subgraph match; using closest: Gotchi #${best.id} (${best.name})`);
    return best.id;
  } catch (error) {
    console.log('Subgraph unavailable, falling back to on-chain search...');
    return null;
  }
}

async function searchGotchiByName(contract, searchName) {
  console.log(`Searching on-chain for Gotchi name: "${searchName}" (case-insensitive exact match)...`);

  try {
    const totalSupply = await callWithRetry('totalSupply()', () => contract.totalSupply());
    const total = Number(totalSupply);
    console.log(`Scanning ${total} gotchis in batches of ${SEARCH_BATCH_SIZE} (RPC-safe mode)...`);

    const searchLower = normalizeName(searchName);
    let checked = 0;

    for (let i = 0; i < total; i += SEARCH_BATCH_SIZE) {
      const end = Math.min(i + SEARCH_BATCH_SIZE, total);

      const tokenIndexPromises = [];
      for (let j = i; j < end; j++) {
        tokenIndexPromises.push(
          callWithRetry(`tokenByIndex(${j})`, () => contract.tokenByIndex(j)).catch(() => null)
        );
      }

      const tokenIds = (await Promise.all(tokenIndexPromises)).filter((id) => id !== null);

      const gotchiPromises = tokenIds.map((tokenId) =>
        callWithRetry(`getAavegotchi(${tokenId.toString()})`, () => contract.getAavegotchi(tokenId)).catch(() => null)
      );

      const gotchis = await Promise.all(gotchiPromises);
      checked += end - i;

      if (checked % 500 === 0 || checked === total) {
        console.log(`Progress: ${checked}/${total} (${Math.round((checked / total) * 100)}%)`);
      }

      for (const gotchi of gotchis) {
        if (gotchi && normalizeName(gotchi.name) === searchLower) {
          console.log(`\nFound on-chain: Gotchi #${gotchi.tokenId} (${gotchi.name})\n`);
          return gotchi;
        }
      }
    }

    console.error(`\nNo gotchi found with name "${searchName}"`);
    return null;
  } catch (error) {
    console.error('Error searching for gotchi:', error.message);
    return null;
  }
}

async function getTokenDecimals(provider, tokenAddress) {
  try {
    const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
    const decimals = await callWithRetry(`decimals(${tokenAddress})`, () => tokenContract.decimals());
    return Number(decimals);
  } catch (error) {
    console.log(`Warning: Could not fetch decimals for ${tokenAddress}, assuming 18`);
    return 18;
  }
}

async function getGotchiInfo(identifier) {
  try {
    const idOrName = String(identifier || '').trim();
    const provider = new ethers.JsonRpcProvider(BASE_RPC);
    const contract = new ethers.Contract(AAVEGOTCHI_CONTRACT, AAVEGOTCHI_ABI, provider);

    let gotchi = null;
    let tokenId = null;

    if (/^\d+$/.test(idOrName)) {
      tokenId = idOrName;
    } else {
      tokenId = await querySubgraphByName(idOrName);

      if (!tokenId) {
        console.log('Subgraph not available or no match found. Falling back to on-chain search...');
        gotchi = await searchGotchiByName(contract, idOrName);
        if (!gotchi) {
          process.exit(1);
        }
      }
    }

    if (!gotchi) {
      gotchi = await callWithRetry(`getAavegotchi(${tokenId})`, () => contract.getAavegotchi(tokenId));
    }

    let stakedAmountFormatted = '0.0';
    if (gotchi.stakedAmount !== 0n) {
      const tokenDecimals = await getTokenDecimals(provider, gotchi.collateral);
      stakedAmountFormatted = ethers.formatUnits(gotchi.stakedAmount, tokenDecimals);
    }

    const ageDays = Math.max(
      0,
      Math.floor((Date.now() / 1000 - Number(gotchi.lastInteracted)) / 86400)
    );

    const data = {
      tokenId: gotchi.tokenId.toString(),
      name: gotchi.name,
      owner: gotchi.owner,
      status: gotchi.status.toString(),
      hauntId: gotchi.hauntId.toString(),
      level: gotchi.level.toString(),
      kinship: gotchi.kinship.toString(),
      experience: gotchi.experience.toString(),
      baseRarityScore: gotchi.baseRarityScore.toString(),
      modifiedRarityScore: gotchi.modifiedRarityScore.toString(),
      traits: {},
      modifiedTraits: {},
      equippedWearables: [],
      collateral: gotchi.collateral,
      stakedAmount: stakedAmountFormatted,
      lastInteracted: new Date(Number(gotchi.lastInteracted) * 1000).toISOString(),
      age: ageDays
    };

    for (let i = 0; i < 6; i++) {
      data.traits[TRAIT_NAMES[i]] = gotchi.numericTraits[i].toString();
      data.modifiedTraits[TRAIT_NAMES[i]] = gotchi.modifiedNumericTraits[i].toString();
    }

    data.equippedWearables = gotchi.equippedWearables
      .map((w) => w.toString())
      .filter((w) => w !== '0');

    data.wearableNames = data.equippedWearables.map((id) => ({
      id,
      name: wearablesData[id] || 'Unknown Item'
    }));

    console.log('='.repeat(60));
    console.log(`AAVEGOTCHI #${data.tokenId}: ${data.name || '(unnamed)'}`);
    console.log('='.repeat(60));
    console.log(`Owner: ${data.owner}`);
    console.log(`Haunt: ${data.hauntId}`);
    console.log(`Level: ${data.level}`);
    console.log(`Age: ${data.age} days since last interaction`);
    console.log('');
    console.log('SCORES:');
    console.log(`  Base Rarity Score (BRS): ${data.baseRarityScore}`);
    console.log(`  Modified Rarity Score: ${data.modifiedRarityScore}`);
    console.log(`  Kinship: ${data.kinship}`);
    console.log(`  Experience: ${data.experience}`);
    console.log('');
    console.log('TRAITS:');
    for (const [trait, value] of Object.entries(data.traits)) {
      const modified = data.modifiedTraits[trait];
      const modifier = modified !== value ? ` (modified: ${modified})` : '';
      const emoji = TRAIT_EMOJIS[trait] || '';
      console.log(`  ${emoji} ${trait}: ${value}${modifier}`);
    }
    console.log('');
    console.log('WEARABLES:');
    if (data.equippedWearables.length > 0) {
      console.log(`  Equipped (${data.equippedWearables.length}):`);
      for (const wearableId of data.equippedWearables) {
        const name = wearablesData[wearableId] || 'Unknown Item';
        console.log(`    ${wearableId}: ${name}`);
      }
    } else {
      console.log('  None equipped');
    }
    console.log('');
    console.log('STAKING:');
    console.log(`  Collateral: ${data.collateral}`);
    console.log(`  Staked Amount: ${data.stakedAmount} tokens`);
    console.log(`  Last Interacted: ${data.lastInteracted}`);
    console.log('='.repeat(60));

    console.log('\nJSON OUTPUT:');
    console.log(JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error fetching Aavegotchi data:', error.message);
    const msg = String(error.message || '').toLowerCase();
    if (msg.includes('invalid token') || msg.includes('execution reverted') || msg.includes('missing revert data')) {
      console.error('This Gotchi ID may not exist on Base.');
    }
    process.exit(1);
  }
}

const identifier = process.argv.slice(2).join(' ').trim();
if (!identifier) {
  console.error('Usage: node get-gotchi.js <gotchi-id-or-name>');
  console.error('Examples: node get-gotchi.js 9638');
  console.error('          node get-gotchi.js "aaigotchi"');
  process.exit(1);
}

getGotchiInfo(identifier);
