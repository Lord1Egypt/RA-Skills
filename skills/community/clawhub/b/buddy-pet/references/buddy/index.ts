/**
 * BUDDY Pet System - Main Entry Point
 * Reference: Claude Code src/buddy/
 * 
 * An AI electronic pet companion system (拓麻歌子 style)
 * 18 species, 5 rarity levels, 1% shiny chance, 5-dimension stats
 */

export * from './types';
export * from './companion';
export * from './sprites';

// Pet name (from screenshots: 小墨)
export const DEFAULT_PET_NAME = '小墨';
export const DEFAULT_PET_SPECIES = 'octopus';
export const DEFAULT_PET_PERSONALITY = '聪明、好奇、有点傲娇';

// Slash commands
export const BUDDY_COMMANDS = {
  HATCH: 'buddy hatch',
  PET: 'buddy pet',
  CARD: 'buddy card',
  MUTE: 'buddy mute',
  UNMUTE: 'buddy unmute',
} as const;

// Bubble message duration (10 seconds = 20 ticks × 500ms)
export const BUBBLE_DURATION_MS = 10000;
export const BUBBLE_FADE_START_MS = 7000;

// Animation timing
export const FRAME_DURATION_MS = 500;
export const IDLE_SEQUENCE_LENGTH = 15;
