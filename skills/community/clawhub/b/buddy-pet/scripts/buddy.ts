#!/usr/bin/env bun
/**
 * BUDDY Pet Companion - Complete CLI Interface
 * Reference: Claude Code src/buddy/
 * 
 * Commands:
 *   hatch <userId>    - Generate a new pet for user
 *   pet <userId>      - Show petting animation
 *   card <userId>     - Show pet card with stats
 *   mute <userId>     - Mute pet
 *   unmute <userId>   - Unmute pet
 *   perfect <userId> [species] - Generate perfect pet (demo/testing, optional species)
 *   prompt <userId>   - Show AI context injection prompt
 */

import { generateCompanion, generatePerfectCompanion } from '../references/buddy/companion.ts';
import { getSprite, getAnimationFrame, getCompactFace } from '../references/buddy/sprites.ts';
import { SPECIES_WITH_EMOJI, RARITY_INFO } from '../references/buddy/types.ts';
import { readFileSync, writeFileSync, existsSync } from 'fs';

// State file for mute status (use /tmp for Docker compatibility)
const STATE_FILE = '/tmp/buddy-state.json';

interface BuddyState {
  muted: boolean;
  bubbleMessage?: string;
  savedPet?: ReturnType<typeof generatePerfectCompanion>;
}

function loadState(): BuddyState {
  try {
    if (!existsSync(STATE_FILE)) {
      return { muted: false };
    }
    const data = readFileSync(STATE_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return { muted: false };
  }
}

function saveState(state: BuddyState): void {
  try {
    writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (e) {
    // Silently fail if can't write state
  }
}

function printUsage() {
  console.log(`
🐙 BUDDY Pet Companion

Usage: bun buddy.ts <command> [userId]

Commands:
  hatch <userId>   - Generate a new pet for user
  pet <userId>      - Show petting animation
  card <userId>     - Show pet card with stats
  mute <userId>     - Mute pet
  unmute <userId>   - Unmute pet
  perfect <userId> [species]  - Generate perfect pet (demo/testing)
  save <userId> [species]  - Save perfect pet as your favorite
  prompt <userId>   - Show AI context injection prompt

Examples:
  bun buddy.ts hatch user123
  bun buddy.ts pet user123
  bun buddy.ts card user123
`);
}

function getRarityStars(rarity: string): string {
  const stars: Record<string, string> = {
    common: '★',
    uncommon: '★★',
    rare: '★★★',
    epic: '★★★★',
    legendary: '★★★★★',
  };
  return stars[rarity] || '★';
}

function getRarityColor(rarity: string): string {
  const colors: Record<string, string> = {
    common: '\x1b[90m',    // gray
    uncommon: '\x1b[32m',  // green
    rare: '\x1b[34m',     // blue
    epic: '\x1b[35m',     // purple
    legendary: '\x1b[33m', // gold
  };
  return colors[rarity] || '';
}

function renderPet(pet: ReturnType<typeof generateCompanion>, frameCount = 3, compact = false) {
  if (compact) {
    console.log('  ' + getCompactFace(pet.species) + '  ');
    return;
  }

  const emoji = SPECIES_WITH_EMOJI[pet.species] || '?';
  const color = getRarityColor(pet.rarity);
  const reset = '\x1b[0m';
  
  console.log('');
  console.log(`   ${emoji} ${pet.name} - ${color}${getRarityStars(pet.rarity)}${reset} ${pet.shiny ? '✨' : ''}`);
  console.log('');

  for (let frame = 0; frame < frameCount; frame++) {
    const frameType = getAnimationFrame(frame);
    const sprite = getSprite(pet.species);
    const lines = sprite[frameType];
    console.log(lines.join('\n'));
    console.log('');
  }
}

function printCard(pet: ReturnType<typeof generateCompanion>) {
  const emoji = SPECIES_WITH_EMOJI[pet.species] || '?';
  const color = getRarityColor(pet.rarity);
  const reset = '\x1b[0m';
  
  console.log('');
  console.log('╔══════════════════════════════════════════╗');
  console.log('║         🐙 BUDDY PET CARD 🐙           ║');
  console.log('╠══════════════════════════════════════════╣');
  console.log(`║  Name:     ${pet.name.padEnd(28)}║`);
  console.log(`║  Species:  ${pet.species.padEnd(28)}║`);
  console.log(`║  Rarity:   ${color}${getRarityStars(pet.rarity).padEnd(28)}${reset}║`);
  console.log(`║  Shiny:    ${pet.shiny ? '✨ YES ✨' : 'NO'.padEnd(28)}║`);
  console.log(`║  Personality: ${pet.personality.padEnd(22)}║`);
  console.log('╠══════════════════════════════════════════╣');
  console.log('║           📊 FIVE STATS                 ║');
  console.log(`║  DEBUGGING: ${String(pet.stats.DEBUGGING).padEnd(22)}║`);
  console.log(`║  PATIENCE:  ${String(pet.stats.PATIENCE).padEnd(22)}║`);
  console.log(`║  CHAOS:     ${String(pet.stats.CHAOS).padEnd(22)}║`);
  console.log(`║  WISDOM:    ${String(pet.stats.WISDOM).padEnd(22)}║`);
  console.log(`║  SNARK:     ${String(pet.stats.SNARK).padEnd(22)}║`);
  console.log('╚══════════════════════════════════════════╝');
  console.log('');
}

function printBubbleDialogue(message: string) {
  const width = Math.min(message.length + 4, 36);
  const padding = width - message.length - 4;
  
  console.log('  ┌' + '─'.repeat(width) + '┐');
  console.log('  │' + ' '.repeat(Math.floor(padding/2)) + message + ' '.repeat(Math.ceil(padding/2)) + '│');
  console.log('  └' + '─'.repeat(width) + '┘');
}

function printPetAnimation() {
  console.log('');
  console.log('     🐙   ');
  console.log('    (·◉·)  ');
  console.log('   >( ═══ )<');
  console.log('    ══════ ');
  console.log('      UU   ');
  console.log('');
  console.log('  ✨ +1  爱心    ✨ +1  爱心    ✨ +1  爱心');
  console.log('     ↑           ↑           ↑');
  console.log('    0.5s        1.0s        1.5s');
  console.log('');
  
  printBubbleDialogue('咕噜咕噜~ 好舒服！');
  
  console.log('');
  console.log('  小墨发出了满足的咕噜声~ 🐙✨');
  console.log('');
}

function printMuteConfirm() {
  console.log('');
  console.log('  🔇 小墨已被静音');
  console.log('  输入 /buddy unmute 可以重新开启对话');
  console.log('');
}

function printUnmuteConfirm() {
  console.log('');
  console.log('  🔊 小墨已取消静音');
  printBubbleDialogue('我又回来啦！');
  console.log('');
}

function printAIPrompt(pet: ReturnType<typeof generateCompanion>) {
  const emoji = SPECIES_WITH_EMOJI[pet.species] || '?';
  
  console.log('');
  console.log('═══ AI CONTEXT INJECTION PROMPT ═══');
  console.log('');
  console.log('When the pet is present and not muted, add this to AI context:');
  console.log('');
  console.log('```');
  console.log(`You have a pet companion named "${pet.name}" (${pet.species}) nearby.`);
  console.log(`${emoji} Appearance: ${getRarityStars(pet.rarity)} ${pet.rarity}${pet.shiny ? ' ✨SHINY✨' : ''}`);
  console.log(`Personality: ${pet.personality}`);
  console.log('');
  console.log('Guidelines:');
  console.log('- Be aware the pet is nearby');
  console.log('- If user addresses the pet directly, keep replies brief (1 line or less)');
  console.log('- Do not speak as the pet or act as the pet');
  console.log('- The pet may occasionally make sounds but does not talk');
  console.log('```');
  console.log('');
  console.log('═══ END PROMPT ═══');
  console.log('');
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const userId = args[1] || 'default-user';
  
  if (!command) {
    printUsage();
    process.exit(1);
  }

  if (!['hatch', 'pet', 'card', 'mute', 'unmute', 'perfect', 'save', 'prompt', 'help'].includes(command)) {
    console.log(`Unknown command: ${command}`);
    printUsage();
    process.exit(1);
  }

  if (command === 'help') {
    printUsage();
    return;
  }

  if (command === 'mute') {
    const state = loadState();
    state.muted = true;
    saveState(state);
    printMuteConfirm();
    return;
  }

  if (command === 'unmute') {
    const state = loadState();
    state.muted = false;
    saveState(state);
    printUnmuteConfirm();
    return;
  }

  if (command === 'prompt') {
    const pet = generateCompanion(userId);
    printAIPrompt(pet);
    return;
  }

  if (command === 'perfect') {
    const species = args[2] as any; // Optional species parameter
    const pet = generatePerfectCompanion(species);
    console.log('🌟 完美宠物 - 仅供演示 🌟');
    console.log(species ? `(Species: ${species})` : '(Species: octopus 🐙)');
    renderPet(pet, 3);
    printCard(pet);
    return;
  }

  if (command === 'save') {
    const species = args[2] as any; // Optional species parameter
    const petName = args[3] as string || '小墨'; // Optional name parameter
    const pet = generatePerfectCompanion(species);
    pet.name = petName;
    const state = loadState();
    state.savedPet = pet;
    saveState(state);
    console.log('✅ 已保存为你的宠物！');
    console.log(`名字: ${petName}`);
    console.log(species ? `(Species: ${species})` : '(Species: octopus 🐙)');
    renderPet(pet, 1);
    console.log('下次使用 /buddy card 或 /buddy pet 将显示这只宠物');
    return;
  }

  const generatedPet = generateCompanion(userId);
  const state = loadState();
  const pet = state.savedPet || generatedPet;

  switch (command) {
    case 'hatch': {
      if (state.savedPet) {
        console.log('🎉 你已有宠物！使用 /buddy card 查看');
        printCard(pet);
      } else {
        console.log('🎉 恭喜！你获得了一只新宠物！');
        renderPet(pet, 3);
        printCard(pet);
      }
      if (state.muted) {
        console.log('(宠物当前处于静音状态，输入 /buddy unmute 开启)');
      }
      break;
    }
    
    case 'pet': {
      if (state.muted) {
        console.log('🔇 小墨已被静音，无法互动');
        console.log('   输入 /buddy unmute 取消静音');
      } else {
        // Show pet-specific animation if saved, otherwise default
        if (state.savedPet) {
          console.log('');
          const frame = getAnimationFrame(0);
          const sprite = getSprite(pet.species);
          console.log(sprite[frame].join('\n'));
          console.log('');
          printBubbleDialogue('咕噜咕噜~ 好舒服！');
          console.log('');
          console.log('✨ +1 爱心 ✨');
        } else {
          printPetAnimation();
        }
      }
      break;
    }
    
    case 'card': {
      printCard(pet);
      renderPet(pet, 1);
      if (state.savedPet) {
        console.log('[已保存的宠物]');
      }
      if (state.muted) {
        console.log('[静音模式]');
      }
      break;
    }
    
    default:
      printUsage();
      process.exit(1);
  }
}

main();
