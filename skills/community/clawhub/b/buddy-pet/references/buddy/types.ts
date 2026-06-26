/**
 * BUDDY Pet System - Type Definitions
 * Reference: Claude Code src/buddy/types.ts
 */

// 18 Species with ASCII sprites (5 rows x 12 chars)
export type Species = 
  | 'duck' | 'goose' | 'cat' | 'dragon' | 'octopus' | 'owl' | 'penguin' | 'turtle' 
  | 'snail' | 'ghost' | 'axolotl' | 'capybara' | 'cactus' | 'robot' | 'rabbit' 
  | 'mushroom' | 'chonk' | 'blob';

// Species names with emoji
export const SPECIES_WITH_EMOJI: Record<Species, string> = {
  duck: '🦆', goose: '🪿', cat: '🐱', dragon: '🐉', octopus: '🐙', owl: '🦉',
  penguin: '🐧', turtle: '🐢', snail: '🐌', ghost: '👻', axolotl: '🦎',
  capybara: '🦫', cactus: '🌵', robot: '🤖', rabbit: '🐰', mushroom: '🍄',
  chonk: '🐈', blob: '🫧'
};

// Rarity levels
export type Rarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';

export interface RarityInfo {
  name: string;
  probability: number;
  stars: string;
  color: string;
  minStats: number;
}

export const RARITY_INFO: Record<Rarity, RarityInfo> = {
  common:     { name: '普通',     probability: 0.60, stars: '★',     color: 'gray',   minStats: 5 },
  uncommon:  { name: '非凡',     probability: 0.25, stars: '★★',    color: 'green',  minStats: 15 },
  rare:       { name: '稀有',     probability: 0.10, stars: '★★★',   color: 'blue',   minStats: 25 },
  epic:       { name: '史诗',     probability: 0.04, stars: '★★★★',  color: 'purple', minStats: 35 },
  legendary:  { name: '传说',     probability: 0.01, stars: '★★★★★', color: 'gold',   minStats: 50 },
};

// Eye styles (6 types)
export const EYE_STYLES = ['·', '✦', '×', '◉', '@', '°'];

// Hat styles (8 types, common has none)
export type HatStyle = 'none' | 'crown' | 'wizard' | 'tophat' | 'beanie' | 'propeller' | 'halo' | 'tinyduck';

export const HAT_STYLES: Record<HatStyle, string> = {
  none: '无', crown: '皇冠', wizard: '巫师帽', tophat: '礼帽',
  beanie: '毛线帽', propeller: '螺旋桨帽', halo: '光环', tinyduck: '小鸭子'
};

// Five-dimension stats
export type StatName = 'DEBUGGING' | 'PATIENCE' | 'CHAOS' | 'WISDOM' | 'SNARK';

export interface Stats {
  DEBUGGING: number;
  PATIENCE: number;
  CHAOS: number;
  WISDOM: number;
  SNARK: number;
}

// Pet entity
export interface Pet {
  name: string;           // AI-generated name
  personality: string;      // AI-generated personality
  hatchedAt: number;       // Timestamp when hatched
  species: Species;
  rarity: Rarity;
  shiny: boolean;          // 1% chance
  eye: string;              // Eye style
  hat: HatStyle;            // Hat style (common has none)
  stats: Stats;
  muted: boolean;
}

// Companion state
export interface CompanionState {
  pet: Pet | null;
  isHatched: boolean;
  isAnimating: boolean;
  bubbleMessage: string | null;
  bubbleExpiresAt: number | null;
}
