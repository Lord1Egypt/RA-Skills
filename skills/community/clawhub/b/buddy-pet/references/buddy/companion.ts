/**
 * BUDDY Companion Generator
 * Reference: Claude Code src/buddy/companion.ts
 * 
 * Deterministic generation using userId + fixed salt -> FNV-1a hash -> Mulberry32 PRNG
 *每人只有一只固定宠物，改配置也没用
 */

import type { Species, Rarity, HatStyle, Pet, Stats } from './types';

// Fixed salt for deterministic generation
const SALT = 'friend-2026-401';

// Species list
const SPECIES_LIST: Species[] = [
  'duck', 'goose', 'cat', 'dragon', 'octopus', 'owl', 'penguin', 'turtle',
  'snail', 'ghost', 'axolotl', 'capybara', 'cactus', 'robot', 'rabbit', 
  'mushroom', 'chonk', 'blob'
];

// FNV-1a hash implementation
function fnv1aHash(str: string): number {
  let hash = 2166136261;
  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

// Mulberry32 PRNG
function createRNG(seed: number): () => number {
  return () => {
    seed |= 0;
    seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Weighted random selection
function weightedRandom<T>(items: { item: T; weight: number }[], rng: () => number): T {
  const totalWeight = items.reduce((sum, i) => sum + i.weight, 0);
  let random = rng() * totalWeight;
  for (const { item, weight } of items) {
    random -= weight;
    if (random <= 0) return item;
  }
  return items[items.length - 1].item;
}

// Generate stats based on rarity min stats
function generateStats(minStats: number, rng: () => number): Stats {
  const statNames: (keyof Stats)[] = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK'];
  const stats = {} as Stats;
  
  // Pick peak and lowest stat
  const peakIdx = Math.floor(rng() * 5);
  const lowestIdx = Math.floor(rng() * 5);
  
  for (let i = 0; i < 5; i++) {
    if (i === peakIdx) {
      stats[statNames[i]] = minStats + 50 + Math.floor(rng() * 30);
    } else if (i === lowestIdx) {
      stats[statNames[i]] = Math.max(1, minStats - 10 + Math.floor(rng() * 15));
    } else {
      stats[statNames[i]] = minStats + Math.floor(rng() * 40);
    }
  }
  
  return stats;
}

// Main companion generator
export function generateCompanion(userId: string): Pet {
  const input = userId + SALT;
  const hash = fnv1aHash(input);
  const rng = createRNG(hash);
  
  // Species (uniform random across 18 species)
  const species = SPECIES_LIST[Math.floor(rng() * SPECIES_LIST.length)];
  
  // Eye style (6 types)
  const eyeStyles = ['·', '✦', '×', '◉', '@', '°'];
  const eye = eyeStyles[Math.floor(rng() * eyeStyles.length)];
  
  // Rarity (weighted probability)
  const rarity = weightedRandom([
    { item: 'common' as Rarity, weight: 0.60 },
    { item: 'uncommon' as Rarity, weight: 0.25 },
    { item: 'rare' as Rarity, weight: 0.10 },
    { item: 'epic' as Rarity, weight: 0.04 },
    { item: 'legendary' as Rarity, weight: 0.01 },
  ], rng);
  
  // Shiny (1% chance, independent of rarity)
  const shiny = rng() < 0.01;
  
  // Hat (common has none)
  const rarityInfo = {
    common: 0,
    uncommon: 1,
    rare: 2,
    epic: 3,
    legendary: 4,
  }[rarity];
  
  const hatStyles: HatStyle[] = ['none', 'crown', 'wizard', 'tophat', 'beanie', 'propeller', 'halo', 'tinyduck'];
  const hat = hatStyles[rarityInfo === 0 ? 0 : Math.floor(rng() * hatStyles.length)];
  
  // Stats based on rarity
  const rarityMinStats = { common: 5, uncommon: 15, rare: 25, epic: 35, legendary: 50 }[rarity];
  const stats = generateStats(rarityMinStats, rng);
  
  return {
    name: '小墨',  // Default name for all pets (as per screenshots)
    personality: '聪明、好奇、有点傲娇',
    hatchedAt: Date.now(),
    species,
    rarity,
    shiny,
    eye,
    hat,
    stats,
    muted: false,
  };
}

// Validate that generation is deterministic
export function validateCompanion(userId: string, pet: Pet): boolean {
  const generated = generateCompanion(userId);
  return (
    generated.species === pet.species &&
    generated.rarity === pet.rarity &&
    generated.shiny === pet.shiny &&
    generated.eye === pet.eye &&
    generated.hat === pet.hat
  );
}

// Generate PERFECT companion - Legendary + All Stats Maxed + Shiny
// For testing/demo purposes
const PERFECT_STATS: Stats = {
  DEBUGGING: 150,
  PATIENCE: 150,
  CHAOS: 150,
  WISDOM: 150,
  SNARK: 150,
};

export function generatePerfectCompanion(species?: Species): Pet {
  return {
    name: '小墨',
    personality: '完美无瑕的天才',
    hatchedAt: Date.now(),
    species: species || 'octopus',  // 默认章鱼，可指定任意18种物种
    rarity: 'legendary',  // 传说稀有
    shiny: true,          // 100% 闪光
    eye: '◉',            // 最好看的眼睛
    hat: 'halo',         // 光环
    stats: PERFECT_STATS,
    muted: false,
  };
}
