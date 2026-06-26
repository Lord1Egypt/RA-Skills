#!/usr/bin/env node
// Claude Code Buddy Algorithm — exact replica from leaked source (v2.1.88)
// Usage: node buddy-algorithm.js <accountUuid>

const SPECIES = ['duck','goose','blob','cat','dragon','octopus','owl','penguin','turtle','snail','ghost','axolotl','capybara','cactus','robot','rabbit','mushroom','chonk'];
const SPECIES_CN = {duck:'鸭子',goose:'鹅',blob:'果冻',cat:'猫',dragon:'龙',octopus:'章鱼',owl:'猫头鹰',penguin:'企鹅',turtle:'乌龟',snail:'蜗牛',ghost:'幽灵',axolotl:'美西螈',capybara:'水豚',cactus:'仙人掌',robot:'机器人',rabbit:'兔子',mushroom:'蘑菇',chonk:'胖墩'};
const SPECIES_EMOJI = {duck:'🦆',goose:'🪿',blob:'🫧',cat:'🐱',dragon:'🐉',octopus:'🐙',owl:'🦉',penguin:'🐧',turtle:'🐢',snail:'🐌',ghost:'👻',axolotl:'🦎',capybara:'🦫',cactus:'🌵',robot:'🤖',rabbit:'🐰',mushroom:'🍄',chonk:'🐡'};
const EYES = ['·','✦','×','◉','@','°'];
const HATS = ['none','crown','tophat','propeller','halo','wizard','beanie','tinyduck'];
const HATS_CN = {none:'无',crown:'王冠',tophat:'礼帽',propeller:'螺旋桨帽',halo:'光晕',wizard:'巫师帽',beanie:'棉帽',tinyduck:'小鸭子'};
const RARITIES = ['common','uncommon','rare','epic','legendary'];
const RARITY_WEIGHTS = {common:60,uncommon:25,rare:10,epic:4,legendary:1};
const RARITY_CN = {common:'普通',uncommon:'不凡',rare:'稀有',epic:'史诗',legendary:'传奇'};
const RARITY_STARS = {common:'★',uncommon:'★★',rare:'★★★',epic:'★★★★',legendary:'★★★★★'};
const RARITY_COLORS = {common:'#8a8a8a',uncommon:'#4ade80',rare:'#60a5fa',epic:'#c084fc',legendary:'#fbbf24'};
const STAT_NAMES = ['DEBUGGING','PATIENCE','CHAOS','WISDOM','SNARK'];
const STAT_CN = {DEBUGGING:'调试力',PATIENCE:'耐心值',CHAOS:'混乱度',WISDOM:'智慧值',SNARK:'毒舌值'};
const RARITY_FLOOR = {common:5,uncommon:15,rare:25,epic:35,legendary:50};
const SALT = 'friend-2026-401';

function mulberry32(seed) {
  let a = seed >>> 0;
  return function() { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

function hashString(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }

function pick(rng, arr) { return arr[Math.floor(rng() * arr.length)]; }

function rollRarity(rng) { let roll = rng() * 100; for (const r of RARITIES) { roll -= RARITY_WEIGHTS[r]; if (roll < 0) return r; } return 'common'; }

function rollStats(rng, rarity) {
  const floor = RARITY_FLOOR[rarity];
  const peak = pick(rng, STAT_NAMES); let dump = pick(rng, STAT_NAMES);
  while (dump === peak) dump = pick(rng, STAT_NAMES);
  const stats = {};
  for (const name of STAT_NAMES) {
    if (name === peak) stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    else if (name === dump) stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15));
    else stats[name] = floor + Math.floor(rng() * 40);
  }
  return { stats, peak, dump };
}

function generate(userId) {
  const key = userId + SALT;
  const hash = hashString(key);
  const rng = mulberry32(hash);
  const rarity = rollRarity(rng);
  const species = pick(rng, SPECIES);
  const eye = pick(rng, EYES);
  const hat = rarity === 'common' ? 'none' : pick(rng, HATS);
  const shiny = rng() < 0.01;
  const { stats, peak, dump } = rollStats(rng, rarity);
  const inspirationSeed = Math.floor(rng() * 1e9);

  return {
    userId: userId.substring(0, 8) + '...',
    hash: '0x' + hash.toString(16).toUpperCase(),
    species, speciesCn: SPECIES_CN[species], speciesEmoji: SPECIES_EMOJI[species],
    rarity, rarityCn: RARITY_CN[rarity], rarityStars: RARITY_STARS[rarity], rarityColor: RARITY_COLORS[rarity],
    eye, hat, hatCn: HATS_CN[hat],
    shiny,
    stats, peak, dump,
    statsCn: STAT_CN,
    inspirationSeed,
    cardNumber: Math.floor(hash % 7128) + 1,
  };
}

const userId = process.argv[2];
if (!userId) { console.error('Usage: node buddy-algorithm.js <accountUuid>'); process.exit(1); }
console.log(JSON.stringify(generate(userId), null, 2));
