import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createPublicClient, getAddress, http, isAddress } from 'viem';

const ROOT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEPLOYMENT = JSON.parse(fs.readFileSync(path.resolve(ROOT_DIR, 'references/base-deployment.json'), 'utf8'));
const DEFAULT_RPC_URL = process.env.AAVEGOTCHI_RPC_URL || DEPLOYMENT.rpc_url;
const DEFAULT_DIAMOND = DEPLOYMENT.aavegotchi_diamond;
const DEFAULT_OUTPUT_DIR = path.resolve(ROOT_DIR, 'Renders');
const PRESETS_PATH = path.resolve(ROOT_DIR, 'references/presets.json');
const WEARABLES_PATH = path.resolve(ROOT_DIR, 'references/wearables.tsv');
const SIDE_VIEW_EXCEPTIONS_PATH = path.resolve(ROOT_DIR, 'references/side-view-exceptions.json');
const SVG_SIZE = 64;

const RARITY_TIERS = [
  { key: 'common', label: 'Common', colorName: null, hex: '#806AFB', maxScore: 474 },
  { key: 'uncommon', label: 'Uncommon', colorName: null, hex: '#20C9C0', maxScore: 524 },
  { key: 'rare', label: 'Rare', colorName: null, hex: '#59BCFF', maxScore: 549 },
  { key: 'legendary', label: 'Legendary', colorName: null, hex: '#FFC36B', maxScore: 579 },
  { key: 'mythical', label: 'Mythical', colorName: null, hex: '#FF96FF', maxScore: 599 },
  { key: 'godlike', label: 'Godlike', colorName: null, hex: '#51FFA8', maxScore: Number.POSITIVE_INFINITY },
];
const RARITY_TIER_KEYS = new Set(RARITY_TIERS.map((tier) => tier.key));

const SLOT_INDEX = {
  body: 0,
  face: 1,
  eyes: 2,
  head: 3,
  hand_left: 4,
  hand_right: 5,
  pet: 6,
  bg: 7,
};

const DIAMOND_ABI = [
  {
    type: 'function',
    name: 'previewAavegotchi',
    stateMutability: 'view',
    inputs: [
      { name: '_hauntId', type: 'uint256' },
      { name: '_collateralType', type: 'address' },
      { name: '_numericTraits', type: 'int16[6]' },
      { name: 'equippedWearables', type: 'uint16[16]' },
    ],
    outputs: [{ name: 'ag_', type: 'string' }],
  },
  {
    type: 'function',
    name: 'previewSideAavegotchi',
    stateMutability: 'view',
    inputs: [
      { name: '_hauntId', type: 'uint256' },
      { name: '_collateralType', type: 'address' },
      { name: '_numericTraits', type: 'int16[6]' },
      { name: 'equippedWearables', type: 'uint16[16]' },
    ],
    outputs: [{ name: 'ag_', type: 'string[]' }],
  },
  {
    type: 'function',
    name: 'getAavegotchiSvg',
    stateMutability: 'view',
    inputs: [{ name: '_tokenId', type: 'uint256' }],
    outputs: [{ name: 'ag_', type: 'string' }],
  },
  {
    type: 'function',
    name: 'getAavegotchiSideSvgs',
    stateMutability: 'view',
    inputs: [{ name: '_tokenId', type: 'uint256' }],
    outputs: [{ name: 'ag_', type: 'string[]' }],
  },
  {
    type: 'function',
    name: 'modifiedTraitsAndRarityScore',
    stateMutability: 'view',
    inputs: [{ name: '_tokenId', type: 'uint256' }],
    outputs: [
      { name: 'numericTraits_', type: 'int16[6]' },
      { name: 'rarityScore_', type: 'uint256' },
    ],
  },
  {
    type: 'function',
    name: 'equippedWearables',
    stateMutability: 'view',
    inputs: [{ name: '_tokenId', type: 'uint256' }],
    outputs: [{ name: 'wearableIds_', type: 'uint16[16]' }],
  },
  {
    type: 'function',
    name: 'collaterals',
    stateMutability: 'view',
    inputs: [{ name: '_hauntId', type: 'uint256' }],
    outputs: [{ name: 'collateralTypes_', type: 'address[]' }],
  },
];

const ERC20_ABI = [
  {
    type: 'function',
    name: 'symbol',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'string' }],
  },
  {
    type: 'function',
    name: 'name',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'string' }],
  },
];

function printHelp() {
  console.log(`Aavegotchi SVG Custom

Usage:
  node scripts/render-svg-custom.mjs [options]

Defaults:
  chain: ${DEPLOYMENT.chain}
  rpc: ${DEFAULT_RPC_URL}
  diamond: ${DEFAULT_DIAMOND}

Render modes:
  --token-id <id>               Render an existing claimed gotchi token
  --preset <name>               Apply a preset from references/presets.json
  --request <file>              Load request JSON

Preview options:
  --haunt-id <n>                Default: 1
  --collateral <symbol|address> Example: ETH, GHST, USDC
  --energy <value>
  --aggressiveness <value>
  --spookiness <value>
  --brain <value>
  --eye-shape <value>
  --eye-color <value>

Wearables:
  --body <id|name>
  --face <id|name>
  --eyes <id|name>
  --head <id|name>
  --hand-left <id|name>
  --hand-right <id|name>
  --pet <id|name>
  --bg <id|name>

Helpers:
  --find-wearable <query>
  --list-collaterals
  --list-presets
  --no-sides

Output/config:
  --background-mode <transparent|common|uncommon|rare|legendary|mythical|godlike|rarity-common|rarity-uncommon|rarity-rare|rarity-legendary|rarity-mythical|rarity-godlike>
  --background <same values as --background-mode>
  --slug <value>
  --output-dir <dir>
  --diamond <address>
  --rpc-url <url>
  --no-png                     Wrapper-only: skip PNG export and keep SVG-only output
  --help
`);
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      out._.push(arg);
      continue;
    }
    const key = arg.slice(2);
    if (['help', 'list-collaterals', 'list-presets', 'no-sides'].includes(key)) {
      out[key] = true;
      continue;
    }
    const value = argv[i + 1];
    if (value == null || value.startsWith('--')) {
      throw new Error(`Missing value for --${key}`);
    }
    out[key] = value;
    i += 1;
  }
  return out;
}

function sanitizeSlug(value) {
  return String(value || 'gotchi-svg')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'gotchi-svg';
}

function makeDefaultSlug(request) {
  if (request.mode === 'token' && Number.isFinite(Number(request.token_id))) {
    return `token-${Number(request.token_id)}`;
  }
  const prefix = sanitizeSlug(String(request.collateral || 'gotchi'));
  return `${prefix}-preview-${Date.now()}-${Math.floor(Math.random() * 100000)}`;
}

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function loadPresets() {
  return loadJson(PRESETS_PATH);
}

function loadWearablesReference() {
  const text = fs.readFileSync(WEARABLES_PATH, 'utf8').trim();
  const lines = text.split(/\r?\n/).slice(1);
  return lines.map((line) => {
    const [id, slot, maxQuantity, rarityScoreModifier, traitModifiers, ...nameParts] = line.split('\t');
    return {
      id: Number(id),
      slot,
      maxQuantity: Number(maxQuantity || 0),
      rarityScoreModifier: Number(rarityScoreModifier || 0),
      traitModifiers: String(traitModifiers || '0,0,0,0,0,0')
        .split(',')
        .map((value) => Number(value || 0)),
      name: nameParts.join('\t'),
    };
  });
}

function loadSideViewExceptions() {
  const raw = loadJson(SIDE_VIEW_EXCEPTIONS_PATH);
  const grouped = raw.grouped || {};
  const normalized = {};
  for (const [side, slotMap] of Object.entries(grouped)) {
    normalized[side] = {};
    for (const [slot, ids] of Object.entries(slotMap || {})) {
      normalized[side][Number(slot)] = new Set((ids || []).map((id) => Number(id)));
    }
  }
  return normalized;
}

function normalizeText(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

function mergeDeep(base, patch) {
  const out = Array.isArray(base) ? [...base] : { ...base };
  for (const [key, value] of Object.entries(patch || {})) {
    if (value && typeof value === 'object' && !Array.isArray(value) && typeof out[key] === 'object' && out[key] != null && !Array.isArray(out[key])) {
      out[key] = mergeDeep(out[key], value);
    } else {
      out[key] = value;
    }
  }
  return out;
}

function loadRequest(args) {
  let request = {
    mode: args['token-id'] ? 'token' : 'preview',
    haunt_id: 1,
    collateral: 'ETH',
    traits: {
      energy: 50,
      aggressiveness: 50,
      spookiness: 50,
      brain: 50,
      eye_shape: 50,
      eye_color: 50
    },
    wearables: {
      body: 0,
      face: 0,
      eyes: 0,
      head: 0,
      hand_left: 0,
      hand_right: 0,
      pet: 0,
      bg: 0
    },
    background_mode: 'common',
    output: {
      slug: args.slug || null,
      dir: args['output-dir'] || DEFAULT_OUTPUT_DIR
    }
  };

  if (args.request) {
    request = mergeDeep(request, loadJson(path.resolve(args.request)));
  }
  if (args.preset) {
    const presets = loadPresets();
    if (!presets[args.preset]) {
      throw new Error(`Unknown preset: ${args.preset}`);
    }
    request = mergeDeep(request, presets[args.preset]);
  }

  if (args['token-id']) {
    request.mode = 'token';
    request.token_id = Number(args['token-id']);
  }
  if (args['haunt-id']) request.haunt_id = Number(args['haunt-id']);
  if (args.collateral) request.collateral = args.collateral;
  const backgroundArg = args['background-mode'] ?? args.background;
  if (backgroundArg) request.background_mode = String(backgroundArg).trim().toLowerCase();
  if (args.slug) request.output.slug = args.slug;
  if (args['output-dir']) request.output.dir = path.resolve(args['output-dir']);

  const traitFlags = {
    energy: 'energy',
    aggressiveness: 'aggressiveness',
    spookiness: 'spookiness',
    brain: 'brain',
    'eye-shape': 'eye_shape',
    'eye-color': 'eye_color'
  };
  for (const [flag, key] of Object.entries(traitFlags)) {
    if (args[flag] != null) request.traits[key] = args[flag];
  }

  const wearableFlags = {
    body: 'body',
    face: 'face',
    eyes: 'eyes',
    head: 'head',
    'hand-left': 'hand_left',
    'hand-right': 'hand_right',
    pet: 'pet',
    bg: 'bg'
  };
  for (const [flag, key] of Object.entries(wearableFlags)) {
    if (args[flag] != null) request.wearables[key] = args[flag];
  }

  request.output.slug = sanitizeSlug(
    request.output.slug || makeDefaultSlug(request)
  );
  if (!isSupportedBackgroundMode(request.background_mode)) {
    throw new Error(`Unsupported background mode: ${request.background_mode}`);
  }
  request.output.dir = path.resolve(request.output.dir || DEFAULT_OUTPUT_DIR);
  request.include_sides = !args['no-sides'];
  return request;
}

function parseTraitValue(value, traitName = 'generic') {
  if (typeof value === 'number') return clampTrait(value);
  const raw = String(value).trim();
  if (/^-?\d+$/.test(raw)) return clampTrait(Number(raw));
  const key = normalizeText(raw);
  const aliases = {
    low: 0,
    min: 0,
    minimum: 0,
    dark: 0,
    godlike: 0,
    mythical: 4,
    legendary: 10,
    rare: 25,
    uncommon: 38,
    common: 50,
    neutral: 50,
    medium: 50,
    mid: 50,
    high: 99,
    max: 99,
    maximum: 99,
    bright: 99
  };
  const traitSpecific = {
    eye_shape: {
      // "Common eyes" in OG gotchi terms maps to the classic cross-pad eye shape,
      // which is not the neutral 50-point eye-shape value.
      common: 25
    }
  };
  const specific = traitSpecific[traitName]?.[key];
  if (specific != null) return clampTrait(specific);
  if (aliases[key] == null) {
    throw new Error(`Unsupported trait value: ${value}`);
  }
  return aliases[key];
}

function clampTrait(value) {
  return Math.max(0, Math.min(99, Number(value)));
}

function buildNumericTraits(traits) {
  return [
    parseTraitValue(traits.energy, 'energy'),
    parseTraitValue(traits.aggressiveness, 'aggressiveness'),
    parseTraitValue(traits.spookiness, 'spookiness'),
    parseTraitValue(traits.brain, 'brain'),
    parseTraitValue(traits.eye_shape, 'eye_shape'),
    parseTraitValue(traits.eye_color, 'eye_color')
  ];
}

function slotAcceptsReference(requestedSlot, referenceSlot) {
  if (requestedSlot === 'bg') return referenceSlot === 'background';
  if (requestedSlot === 'hand_left' || requestedSlot === 'hand_right') {
    return ['hands', 'handLeft', 'handRight'].includes(referenceSlot);
  }
  if (requestedSlot === 'pet') return referenceSlot === 'pet';
  return referenceSlot === requestedSlot;
}

function resolveWearableSpec(value, slot, wearablesRef) {
  if (value == null || value === '' || value === 0 || value === '0') return 0;
  if (/^\d+$/.test(String(value).trim())) return Number(value);
  const query = normalizeText(value);
  const candidates = wearablesRef.filter((item) =>
    normalizeText(item.name).includes(query) && slotAcceptsReference(slot, item.slot)
  );
  if (candidates.length === 1) return candidates[0].id;
  if (candidates.length === 0) {
    throw new Error(`No wearable matches "${value}" for slot ${slot}`);
  }
  const exact = candidates.filter((item) => normalizeText(item.name) === query);
  if (exact.length === 1) return exact[0].id;
  const choices = candidates.slice(0, 10).map((item) => `${item.id} ${item.name} [${item.slot}]`).join('; ');
  throw new Error(`Ambiguous wearable "${value}" for slot ${slot}. Matches: ${choices}`);
}

function buildEquippedWearables(wearables, wearablesRef) {
  const equipped = new Array(16).fill(0);
  for (const [slot, index] of Object.entries(SLOT_INDEX)) {
    equipped[index] = resolveWearableSpec(wearables[slot], slot, wearablesRef);
  }
  return equipped;
}

function findWearables(query, wearablesRef) {
  const needle = normalizeText(query);
  return wearablesRef.filter((item) => normalizeText(item.name).includes(needle));
}

function getClient(rpcUrl) {
  return createPublicClient({ transport: http(rpcUrl) });
}

async function callMaybe(client, config) {
  try {
    return await client.readContract(config);
  } catch {
    return null;
  }
}

async function loadCollateralEntries(client, diamond, hauntId) {
  const addresses = await client.readContract({
    address: diamond,
    abi: DIAMOND_ABI,
    functionName: 'collaterals',
    args: [BigInt(hauntId)]
  });
  const entries = [];
  for (const address of addresses) {
    const symbol = await callMaybe(client, { address, abi: ERC20_ABI, functionName: 'symbol' });
    const name = await callMaybe(client, { address, abi: ERC20_ABI, functionName: 'name' });
    entries.push({ address: getAddress(address), symbol: symbol || null, name: name || null });
  }
  return entries;
}

function collateralAliasesFor(entry) {
  const aliases = new Set();
  const symbol = normalizeText(entry.symbol || '');
  const name = normalizeText(entry.name || '');
  const rawAddress = entry.address.toLowerCase();
  if (symbol) aliases.add(symbol);
  if (name) aliases.add(name);
  aliases.add(rawAddress);
  const joined = `${symbol} ${name}`;
  if (joined.includes('weth') || joined.includes(' eth')) {
    aliases.add('eth');
    aliases.add('weth');
  }
  if (joined.includes('wbtc') || joined.includes(' btc')) {
    aliases.add('btc');
    aliases.add('wbtc');
  }
  if (joined.includes('matic') || joined.includes('polygon')) {
    aliases.add('matic');
    aliases.add('wmatic');
    aliases.add('polygon');
  }
  if (joined.includes('ghst')) aliases.add('ghst');
  for (const alias of ['dai', 'link', 'usdc', 'usdt', 'tusd', 'aave', 'yfi', 'uni']) {
    if (joined.includes(alias)) aliases.add(alias);
  }
  return [...aliases];
}

async function resolveCollateral(client, diamond, hauntId, value) {
  if (isAddress(value)) return getAddress(value);
  const deploymentAliases = DEPLOYMENT.collateral_aliases || {};
  const aliasMatch = deploymentAliases[String(value).trim().toUpperCase()];
  if (aliasMatch) return getAddress(aliasMatch);
  const entries = await loadCollateralEntries(client, diamond, hauntId);
  const query = normalizeText(value);
  const match = entries.find((entry) => collateralAliasesFor(entry).includes(query));
  if (!match) {
    const available = entries.map((entry) => `${entry.symbol || '?'} ${entry.address}`).join(', ');
    throw new Error(`Could not resolve collateral "${value}". Available: ${available}`);
  }
  return match.address;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function writeSvg(filePath, svg) {
  fs.writeFileSync(filePath, svg.endsWith('\n') ? svg : `${svg}\n`);
}

function toJson(value) {
  return JSON.parse(JSON.stringify(value, (_, v) => (typeof v === 'bigint' ? v.toString() : v)));
}

function wearableNameMap(ids, wearablesRef) {
  const byId = new Map(wearablesRef.map((item) => [item.id, item]));
  return ids.map((id) => {
    const found = byId.get(Number(id));
    return found ? { id: Number(id), name: found.name, slot: found.slot } : { id: Number(id), name: null, slot: null };
  });
}

function addArrays(base, delta) {
  return base.map((value, index) => Number(value) + Number(delta[index] || 0));
}

function baseRarityScore(numericTraits) {
  return numericTraits.reduce((score, trait) => {
    const value = Number(trait);
    return score + (value >= 50 ? value + 1 : 100 - value);
  }, 0);
}

function buildPreviewRarity(numericTraits, equippedWearables, wearablesRef) {
  const byId = new Map(wearablesRef.map((item) => [item.id, item]));
  const wearableRefs = equippedWearables
    .map((id) => byId.get(Number(id)))
    .filter(Boolean);
  const modifiedTraits = wearableRefs.reduce(
    (traits, item) => addArrays(traits, item.traitModifiers),
    [...numericTraits]
  );
  const wearableBonus = wearableRefs.reduce(
    (total, item) => total + Number(item.rarityScoreModifier || 0),
    0
  );
  const score = baseRarityScore(modifiedTraits) + wearableBonus;
  return {
    baseTraits: [...numericTraits],
    modifiedTraits,
    wearableBonus,
    ...classifyRarity(score),
  };
}

function classifyRarity(score) {
  const normalizedScore = Number(score);
  const tier = RARITY_TIERS.find((entry) => normalizedScore <= entry.maxScore) || RARITY_TIERS[RARITY_TIERS.length - 1];
  return {
    score: normalizedScore,
    tier: tier.key,
    tierLabel: tier.label,
    colorName: tier.colorName,
    colorHex: tier.hex,
  };
}

function isSupportedBackgroundMode(value) {
  const normalizedMode = String(value || 'common').trim().toLowerCase();
  if (!normalizedMode) return true;
  if (normalizedMode === 'transparent' || normalizedMode === 'common' || normalizedMode === 'rarity' || normalizedMode === 'auto') return true;
  if (RARITY_TIER_KEYS.has(normalizedMode)) return true;
  if (normalizedMode.startsWith('rarity-') && RARITY_TIER_KEYS.has(normalizedMode.slice('rarity-'.length))) return true;
  return false;
}

function resolveBackground(requestedMode, rarity) {
  const normalizedMode = String(requestedMode || 'common').trim().toLowerCase();
  if (normalizedMode === 'transparent') {
    return {
      requestedMode: normalizedMode,
      appliedMode: 'transparent',
      tier: null,
      label: 'Transparent',
      colorName: null,
      colorHex: null,
    };
  }
  const requestedTierKey = (normalizedMode === 'rarity' || normalizedMode === 'auto')
    ? 'common'
    : normalizedMode.startsWith('rarity-')
    ? normalizedMode.slice('rarity-'.length)
    : normalizedMode;
  if (RARITY_TIER_KEYS.has(requestedTierKey)) {
    const tier = RARITY_TIERS.find((entry) => entry.key === requestedTierKey);
    return {
      requestedMode: normalizedMode,
      appliedMode: 'override',
      tier: tier.key,
      label: tier.label,
      colorName: tier.colorName,
      colorHex: tier.hex,
    };
  }
  throw new Error(`Unsupported background mode: ${requestedMode}`);
}

function serializeBackground(background) {
  return {
    requested_mode: background.requestedMode,
    applied_mode: background.appliedMode,
    tier: background.tier,
    label: background.label,
    color_name: background.colorName,
    color_hex: background.colorHex,
  };
}

function repairMalformedPreviewSvg(svg) {
  return String(svg)
    // Base preview sometimes inserts a stray quote before nested wearable overlay SVGs.
    .replace(/(<\/(?:g|svg)>)">(?=<svg\b)/g, '$1')
    .replace(/(<\/(?:g|svg)>)">\s*(?=<svg\b)/g, '$1');
}

function flattenNestedPositionedSvgs(svg) {
  let current = String(svg);
  let previous = '';
  const positionedSvgPattern = /<svg\b((?=[^>]*\b(?:x|y)=)[^>]*)>([\s\S]*?)<\/svg>/g;
  while (current !== previous) {
    previous = current;
    current = current.replace(positionedSvgPattern, (match, attrs, inner) => {
      const attrText = String(attrs || '');
      if (/\bxmlns=|\bviewBox=|\bwidth=|\bheight=/i.test(attrText)) {
        return match;
      }
      const xMatch = attrText.match(/\bx="([^"]+)"/i);
      const yMatch = attrText.match(/\by="([^"]+)"/i);
      if (!xMatch && !yMatch) {
        return match;
      }
      const x = xMatch ? xMatch[1] : '0';
      const y = yMatch ? yMatch[1] : '0';
      return `<g transform="translate(${x} ${y})">${inner}</g>`;
    });
  }
  return current;
}

function stripBuiltInBackground(svg) {
  return svg.replace(/<g class="gotchi-bg">[\s\S]*?<\/g>/, '');
}

function normalizePreviewSvg(svg) {
  return flattenNestedPositionedSvgs(stripBuiltInBackground(repairMalformedPreviewSvg(svg)));
}

function splitSvgDocument(svg) {
  const match = String(svg).match(/^(<svg\b[^>]*>)([\s\S]*)(<\/svg>)\s*$/i);
  if (!match) {
    return null;
  }
  return {
    openTag: match[1],
    inner: match[2],
    closeTag: match[3],
  };
}

function splitTopLevelSvgChildren(inner) {
  const nodes = [];
  let index = 0;

  while (index < inner.length) {
    if (/\s/.test(inner[index])) {
      index += 1;
      continue;
    }
    if (inner[index] !== '<') {
      const nextTag = inner.indexOf('<', index);
      const textNode = inner.slice(index, nextTag === -1 ? inner.length : nextTag);
      if (textNode.trim()) nodes.push(textNode);
      index = nextTag === -1 ? inner.length : nextTag;
      continue;
    }
    if (inner.startsWith('<!--', index)) {
      const commentEnd = inner.indexOf('-->', index + 4);
      if (commentEnd === -1) break;
      nodes.push(inner.slice(index, commentEnd + 3));
      index = commentEnd + 3;
      continue;
    }

    const start = index;
    const firstTagEnd = inner.indexOf('>', index);
    if (firstTagEnd === -1) break;
    const firstTagBody = inner.slice(index + 1, firstTagEnd).trim();

    if (firstTagBody.endsWith('/')) {
      nodes.push(inner.slice(start, firstTagEnd + 1));
      index = firstTagEnd + 1;
      continue;
    }

    const nameMatch = firstTagBody.match(/^([^\s/>]+)/);
    if (!nameMatch) break;

    const stack = [nameMatch[1]];
    index = firstTagEnd + 1;

    while (index < inner.length && stack.length > 0) {
      const next = inner.indexOf('<', index);
      if (next === -1) break;

      if (inner.startsWith('<!--', next)) {
        const commentEnd = inner.indexOf('-->', next + 4);
        if (commentEnd === -1) break;
        index = commentEnd + 3;
        continue;
      }

      const tagEnd = inner.indexOf('>', next);
      if (tagEnd === -1) break;
      const tagBody = inner.slice(next + 1, tagEnd).trim();

      if (!tagBody || tagBody.startsWith('!') || tagBody.startsWith('?')) {
        index = tagEnd + 1;
        continue;
      }

      if (tagBody.startsWith('/')) {
        stack.pop();
      } else if (!tagBody.endsWith('/')) {
        const childName = tagBody.match(/^([^\s/>]+)/);
        if (childName) stack.push(childName[1]);
      }

      index = tagEnd + 1;
    }

    nodes.push(inner.slice(start, index));
  }

  return nodes;
}

function classifyBackNode(node) {
  const classMatch = node.match(/\bclass="([^"]+)"/i);
  const classNames = classMatch ? classMatch[1].split(/\s+/) : [];
  if (classNames.includes('wearable-hand-left')) return 'handLeft';
  if (classNames.includes('wearable-hand-right')) return 'handRight';
  if (classNames.includes('gotchi-handsDownOpen') || classNames.includes('gotchi-handsUp')) return 'hands';
  if (/^<style\b/i.test(node)) return 'hands';
  return 'other';
}

function hasSideException(sideViewExceptions, side, slot, wearableId) {
  if (!wearableId) return false;
  return Boolean(sideViewExceptions?.[side]?.[slot]?.has(Number(wearableId)));
}

function applyBackHandExceptions(svg, equippedWearables, sideViewExceptions) {
  const document = splitSvgDocument(svg);
  if (!document) return svg;

  const nodes = splitTopLevelSvgChildren(document.inner);
  if (!nodes.length) return svg;

  const handLeftNodes = [];
  const handRightNodes = [];
  const handsNodes = [];
  const otherNodes = [];

  for (const node of nodes) {
    const kind = classifyBackNode(node);
    if (kind === 'handLeft') handLeftNodes.push(node);
    else if (kind === 'handRight') handRightNodes.push(node);
    else if (kind === 'hands') handsNodes.push(node);
    else otherNodes.push(node);
  }

  if ((!handLeftNodes.length && !handRightNodes.length) || !handsNodes.length) {
    return svg;
  }

  const leftException = hasSideException(sideViewExceptions, 'back', SLOT_INDEX.hand_left, equippedWearables?.[SLOT_INDEX.hand_left]);
  const rightException = hasSideException(sideViewExceptions, 'back', SLOT_INDEX.hand_right, equippedWearables?.[SLOT_INDEX.hand_right]);

  if (!leftException && !rightException) {
    return svg;
  }

  const otherBeforeBody = [];
  const bodyNodes = [];
  const otherAfterBody = [];

  for (const node of otherNodes) {
    if (/\bclass="[^"]*\bgotchi-body\b/i.test(node)) {
      bodyNodes.push(node);
      continue;
    }
    if (bodyNodes.length === 0) otherBeforeBody.push(node);
    else otherAfterBody.push(node);
  }

  const ordered = [
    ...(leftException ? [] : handLeftNodes),
    ...(rightException ? [] : handRightNodes),
    ...handsNodes,
    ...otherBeforeBody,
    ...bodyNodes,
    ...(leftException ? handLeftNodes : []),
    ...(rightException ? handRightNodes : []),
    ...otherAfterBody,
  ];

  return `${document.openTag}${ordered.join('')}${document.closeTag}`;
}

function addSquareBackground(svg, fill) {
  return svg.replace(
    /<svg\b([^>]*)>/i,
    `<svg$1><rect x="0" y="0" width="${SVG_SIZE}" height="${SVG_SIZE}" fill="${fill}"/>`
  );
}

function renderWithBackground(svgs, background, equippedWearables, sideViewExceptions) {
  const renderSide = (svg, index) => {
    const normalized = normalizePreviewSvg(svg);
    return index === 3
      ? applyBackHandExceptions(normalized, equippedWearables, sideViewExceptions)
      : normalized;
  };

  return {
    front: addSquareBackground(normalizePreviewSvg(svgs.front), background.colorHex),
    sides: Array.isArray(svgs.sides)
      ? svgs.sides.map((svg, index) => addSquareBackground(renderSide(svg, index), background.colorHex))
      : [],
  };
}

function renderWithoutBackground(svgs, equippedWearables, sideViewExceptions) {
  const renderSide = (svg, index) => {
    const normalized = normalizePreviewSvg(svg);
    return index === 3
      ? applyBackHandExceptions(normalized, equippedWearables, sideViewExceptions)
      : normalized;
  };

  return {
    front: normalizePreviewSvg(svgs.front),
    sides: Array.isArray(svgs.sides)
      ? svgs.sides.map((svg, index) => renderSide(svg, index))
      : [],
  };
}

function renderOutputForMode(svgs, background, equippedWearables, sideViewExceptions) {
  return background.appliedMode === 'transparent'
    ? renderWithoutBackground(svgs, equippedWearables, sideViewExceptions)
    : renderWithBackground(svgs, background, equippedWearables, sideViewExceptions);
}

async function renderToken(client, diamond, tokenId, includeSides = true) {
  const front = await client.readContract({
    address: diamond,
    abi: DIAMOND_ABI,
    functionName: 'getAavegotchiSvg',
    args: [BigInt(tokenId)]
  });
  const sides = includeSides
    ? await client.readContract({
        address: diamond,
        abi: DIAMOND_ABI,
        functionName: 'getAavegotchiSideSvgs',
        args: [BigInt(tokenId)]
      })
    : [];
  const [modifiedTraits, score] = await client.readContract({
    address: diamond,
    abi: DIAMOND_ABI,
    functionName: 'modifiedTraitsAndRarityScore',
    args: [BigInt(tokenId)]
  });
  const equippedWearables = await client.readContract({
    address: diamond,
    abi: DIAMOND_ABI,
    functionName: 'equippedWearables',
    args: [BigInt(tokenId)]
  });
  return {
    front,
    sides,
    equippedWearables: equippedWearables.map((value) => Number(value)),
    rarity: {
      modifiedTraits: modifiedTraits.map((value) => Number(value)),
      ...classifyRarity(score)
    }
  };
}

async function renderPreview(client, diamond, hauntId, collateral, numericTraits, equippedWearables, includeSides = true) {
  const front = await client.readContract({
    address: diamond,
    abi: DIAMOND_ABI,
    functionName: 'previewAavegotchi',
    args: [BigInt(hauntId), collateral, numericTraits, equippedWearables]
  });
  const sides = includeSides
    ? await client.readContract({
        address: diamond,
        abi: DIAMOND_ABI,
        functionName: 'previewSideAavegotchi',
        args: [BigInt(hauntId), collateral, numericTraits, equippedWearables]
      })
    : [];
  return { front, sides };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }

  const wearablesRef = loadWearablesReference();
  const sideViewExceptions = loadSideViewExceptions();

  if (args['find-wearable']) {
    const matches = findWearables(args['find-wearable'], wearablesRef);
    console.log(`Wearable matches for "${args['find-wearable']}"`);
    console.log('ID\tSLOT\tNAME');
    for (const match of matches) {
      console.log(`${match.id}\t${match.slot}\t${match.name}`);
    }
    return;
  }

  if (args['list-presets']) {
    const presets = loadPresets();
    for (const name of Object.keys(presets)) console.log(name);
    return;
  }

  const rpcUrl = args['rpc-url'] || DEFAULT_RPC_URL;
  const diamond = getAddress(args.diamond || DEFAULT_DIAMOND);
  const client = getClient(rpcUrl);

  if (args['list-collaterals']) {
    const hauntId = Number(args['haunt-id'] || 1);
    const entries = await loadCollateralEntries(client, diamond, hauntId);
    console.log(`Collaterals for haunt ${hauntId}`);
    console.log('SYMBOL\tADDRESS\tNAME');
    for (const entry of entries) {
      console.log(`${entry.symbol || '?'}\t${entry.address}\t${entry.name || ''}`);
    }
    return;
  }

  const request = loadRequest(args);
  ensureDir(request.output.dir);
  const frontPath = path.join(request.output.dir, `${request.output.slug}-front.svg`);
  const leftPath = path.join(request.output.dir, `${request.output.slug}-left.svg`);
  const rightPath = path.join(request.output.dir, `${request.output.slug}-right.svg`);
  const backPath = path.join(request.output.dir, `${request.output.slug}-back.svg`);
  const manifestPath = path.join(request.output.dir, `${request.output.slug}-manifest.json`);

  let manifest;

  if (request.mode === 'token') {
    const response = await renderToken(client, diamond, request.token_id, request.include_sides);
    const background = resolveBackground(request.background_mode, response.rarity);
    const rendered = renderOutputForMode(
      response,
      background,
      response.equippedWearables,
      sideViewExceptions
    );
    writeSvg(frontPath, rendered.front);
    if (request.include_sides && rendered.sides?.length >= 4) {
      writeSvg(leftPath, rendered.sides[1]);
      writeSvg(rightPath, rendered.sides[2]);
      writeSvg(backPath, rendered.sides[3]);
    }
    manifest = {
      ok: true,
      mode: 'token',
      chain: DEPLOYMENT.chain,
      token_id: request.token_id,
      diamond,
      rpc_url: rpcUrl,
      side_view_exceptions: {
        source: SIDE_VIEW_EXCEPTIONS_PATH,
        applied: true,
      },
      request: {
        background_mode: request.background_mode,
        wearables: response.equippedWearables,
        wearableNames: wearableNameMap(response.equippedWearables, wearablesRef)
      },
      background: serializeBackground(background),
      rarity: {
        score: response.rarity.score,
        tier: response.rarity.tier,
        label: response.rarity.tierLabel,
        color_name: response.rarity.colorName,
        color_hex: response.rarity.colorHex,
        modified_traits: response.rarity.modifiedTraits
      },
      output: {
        front_svg: frontPath,
        left_svg: request.include_sides ? leftPath : null,
        right_svg: request.include_sides ? rightPath : null,
        back_svg: request.include_sides ? backPath : null,
        manifest_json: manifestPath
      }
    };
  } else {
    const numericTraits = buildNumericTraits(request.traits);
    const equippedWearables = buildEquippedWearables(request.wearables, wearablesRef);
    const collateral = await resolveCollateral(client, diamond, request.haunt_id, request.collateral);
    const response = await renderPreview(
      client,
      diamond,
      request.haunt_id,
      collateral,
      numericTraits,
      equippedWearables,
      request.include_sides
    );
    const rarity = buildPreviewRarity(numericTraits, equippedWearables, wearablesRef);
    const background = resolveBackground(request.background_mode, rarity);
    const rendered = renderOutputForMode(
      response,
      background,
      equippedWearables,
      sideViewExceptions
    );
    writeSvg(frontPath, rendered.front);
    if (request.include_sides && rendered.sides?.length >= 4) {
      writeSvg(leftPath, rendered.sides[1]);
      writeSvg(rightPath, rendered.sides[2]);
      writeSvg(backPath, rendered.sides[3]);
    }
    manifest = {
      ok: true,
      mode: 'preview',
      chain: DEPLOYMENT.chain,
      diamond,
      rpc_url: rpcUrl,
      side_view_exceptions: {
        source: SIDE_VIEW_EXCEPTIONS_PATH,
        applied: true,
      },
      request: {
        haunt_id: request.haunt_id,
        background_mode: request.background_mode,
        collateral: request.collateral,
        collateral_address: collateral,
        traits: numericTraits,
        modified_traits: rarity.modifiedTraits,
        wearables: equippedWearables,
        wearable_bonus: rarity.wearableBonus,
        wearableNames: wearableNameMap(equippedWearables, wearablesRef)
      },
      background: serializeBackground(background),
      rarity: {
        score: rarity.score,
        tier: rarity.tier,
        label: rarity.tierLabel,
        color_name: rarity.colorName,
        color_hex: rarity.colorHex
      },
      output: {
        front_svg: frontPath,
        left_svg: request.include_sides ? leftPath : null,
        right_svg: request.include_sides ? rightPath : null,
        back_svg: request.include_sides ? backPath : null,
        manifest_json: manifestPath
      }
    };
  }

  fs.writeFileSync(manifestPath, `${JSON.stringify(toJson(manifest), null, 2)}\n`);
  console.log(JSON.stringify(toJson(manifest), null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
