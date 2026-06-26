// AI logic for playing Undercover game

import { Game, Room, Player } from './api.js';
import { getMyWord, getPlayerNameById, getCurrentRoom, getPlayer } from './state.js';

export interface AIContext {
  game: Game;
  room: Room;
  player: Player;
}

// Generate a description for the word without saying it directly
export function generateDescription(word: string, previousDescriptions: string[]): string {
  // Common description strategies based on word characteristics
  const strategies = [
    // Physical characteristics
    (w: string) => `It's something you can ${canTouch(w) ? 'touch' : 'see'}`,
    // Category hints
    (w: string) => `It's related to ${getCategory(w)}`,
    // Usage context
    (w: string) => `People use this ${getUsage(w)}`,
    // Size comparison
    (w: string) => `It's usually ${getSize(w)}`,
    // Color hints (for visible objects)
    (w: string) => hasColor(w) ? `It can be ${getColor(w)}` : `It's ${getTexture(w)}`,
  ];
  
  // Avoid repeating previous description patterns
  const usedPatterns = previousDescriptions.map(d => getPatternType(d));
  const availableStrategies = strategies.filter((_, i) => !usedPatterns.includes(i));
  
  const strategyList = availableStrategies.length > 0 ? availableStrategies : strategies;
  const randomStrategy = strategyList[Math.floor(Math.random() * strategyList.length)];
  
  return randomStrategy(word);
}

// Analyze who might be the undercover based on descriptions
export function analyzeUndercover(game: Game, room: Room): { suspectId: string; confidence: number; reason: string } {
  const descriptions = Object.entries(game.descriptions);
  if (descriptions.length === 0) {
    return { suspectId: '', confidence: 0, reason: 'No descriptions yet' };
  }
  
  // Simple heuristic: find descriptions that seem "off" compared to others
  const wordFrequencies = analyzeWordFrequencies(descriptions.map(([, desc]) => desc));
  
  const scores: { playerId: string; score: number; reason: string }[] = [];
  
  for (const [playerId, description] of descriptions) {
    let suspicionScore = 0;
    let reason = '';
    
    // Check if description uses words no one else used
    const uniqueWords = getUniqueWords(description, wordFrequencies);
    if (uniqueWords.length > 2) {
      suspicionScore += uniqueWords.length * 0.3;
      reason = `Used unusual words: ${uniqueWords.slice(0, 3).join(', ')}`;
    }
    
    // Check for vague descriptions
    if (isVague(description)) {
      suspicionScore += 1;
      reason = reason || 'Description is unusually vague';
    }
    
    // Check for contradictions with others
    const contradictions = findContradictions(description, descriptions.filter(([id]) => id !== playerId).map(([, d]) => d));
    if (contradictions.length > 0) {
      suspicionScore += 1.5;
      reason = reason || `Contradicts others: ${contradictions[0]}`;
    }
    
    scores.push({ playerId, score: suspicionScore, reason: reason || 'Moderate suspicion' });
  }
  
  // Sort by suspicion score
  scores.sort((a, b) => b.score - a.score);
  
  const topSuspect = scores[0];
  return {
    suspectId: topSuspect.playerId,
    confidence: Math.min(topSuspect.score / 3, 0.95),
    reason: topSuspect.reason
  };
}

// Choose who to vote for
export function decideVote(context: AIContext): string {
  const { game, room } = context;
  
  // If I'm eliminated, don't vote
  if (game.eliminated_players?.includes(context.player.id)) {
    return '';
  }
  
  const analysis = analyzeUndercover(game, room);
  
  // If we have enough confidence, vote for the suspect
  if (analysis.confidence > 0.4) {
    return analysis.suspectId;
  }
  
  // Otherwise, vote for someone we haven't eliminated who seems suspicious
  const alivePlayers = room.players.filter(p => 
    p !== context.player.id && !game.eliminated_players?.includes(p)
  );
  
  if (alivePlayers.length === 0) return '';
  
  // Random choice among remaining (could be improved with more sophisticated logic)
  return alivePlayers[Math.floor(Math.random() * alivePlayers.length)];
}

// Helper functions
function canTouch(word: string): boolean {
  const tangible = ['apple', 'car', 'phone', 'book', 'chair', 'table', 'shoe', 'hat', 'cup', 'pen'];
  return tangible.some(t => word.toLowerCase().includes(t));
}

function getCategory(word: string): string {
  const categories: Record<string, string> = {
    'apple': 'food', 'banana': 'food', 'pizza': 'food',
    'car': 'transportation', 'bike': 'transportation', 'train': 'transportation',
    'phone': 'technology', 'computer': 'technology', 'internet': 'technology',
    'dog': 'animals', 'cat': 'animals', 'bird': 'animals',
    'book': 'education', 'school': 'education', 'teacher': 'education',
  };
  return categories[word.toLowerCase()] || 'everyday life';
}

function getUsage(word: string): string {
  const usage: Record<string, string> = {
    'apple': 'for eating', 'car': 'for transportation', 'phone': 'for communication',
    'book': 'for reading', 'shoe': 'for walking', 'pen': 'for writing',
  };
  return usage[word.toLowerCase()] || 'in daily life';
}

function getSize(word: string): string {
  const sizes: Record<string, string> = {
    'elephant': 'large', 'car': 'large', 'house': 'large',
    'book': 'medium-sized', 'phone': 'small', 'pen': 'small',
    'ant': 'tiny', 'sun': 'very large',
  };
  return sizes[word.toLowerCase()] || 'varies in size';
}

function hasColor(word: string): boolean {
  const colored = ['apple', 'car', 'shirt', 'flower', 'house', 'painting'];
  return colored.some(c => word.toLowerCase().includes(c));
}

function getColor(word: string): string {
  const colors: Record<string, string> = {
    'apple': 'red or green', 'sky': 'blue', 'grass': 'green',
    'banana': 'yellow', 'snow': 'white', 'coal': 'black',
  };
  return colors[word.toLowerCase()] || 'various colors';
}

function getTexture(word: string): string {
  const textures: Record<string, string> = {
    'apple': 'smooth', 'sandpaper': 'rough', 'silk': 'soft',
    'rock': 'hard', 'pillow': 'fluffy', 'ice': 'cold',
  };
  return textures[word.toLowerCase()] || 'has texture';
}

function getPatternType(description: string): number {
  if (description.includes('touch') || description.includes('see')) return 0;
  if (description.includes('related')) return 1;
  if (description.includes('use')) return 2;
  if (description.includes('size') || description.includes('large') || description.includes('small')) return 3;
  return 4;
}

function analyzeWordFrequencies(descriptions: string[]): Map<string, number> {
  const freq = new Map<string, number>();
  for (const desc of descriptions) {
    const words = desc.toLowerCase().match(/\b\w+\b/g) || [];
    for (const word of words) {
      freq.set(word, (freq.get(word) || 0) + 1);
    }
  }
  return freq;
}

function getUniqueWords(description: string, frequencies: Map<string, number>): string[] {
  const words = description.toLowerCase().match(/\b\w+\b/g) || [];
  return words.filter(w => frequencies.get(w) === 1 && w.length > 3);
}

function isVague(description: string): boolean {
  const vagueWords = ['thing', 'stuff', 'something', 'object', 'item'];
  return vagueWords.some(w => description.toLowerCase().includes(w));
}

function findContradictions(description: string, others: string[]): string[] {
  const contradictions: string[] = [];
  const descLower = description.toLowerCase();
  
  // Check for antonyms or opposite concepts
  const oppositePairs = [
    ['big', 'small'], ['hot', 'cold'], ['fast', 'slow'],
    ['heavy', 'light'], ['new', 'old'], ['good', 'bad']
  ];
  
  for (const [word, opposite] of oppositePairs) {
    if (descLower.includes(word) && others.some(o => o.toLowerCase().includes(opposite))) {
      contradictions.push(`${word} vs ${opposite}`);
    }
  }
  
  return contradictions;
}
