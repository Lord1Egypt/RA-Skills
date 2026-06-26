import { scoreTextWarmth } from '../scoring/heuristics.js';
import type { TextInput, DecodedText, TextReading } from '../types.js';

// ─── Reading Builder ──────────────────────────────────────────────────────────

const VIBE_LABELS: Record<string, string> = {
  playful:  '😄 Playful',
  flirty:   '😏 Flirty',
  warm:     '🌟 Warm',
  friendly: '👋 Friendly',
  engaged:  '💬 Engaged',
  neutral:  '😐 Neutral',
  unclear:  '🤔 Hard to read',
};

function buildReadings(message: string, warmth: number): TextReading[] {
  const hasQuestion = message.includes('?');
  const isShort     = message.length < 15;
  const isLong      = message.length > 80;
  const hasEmoji    = /\p{Emoji_Presentation}/u.test(message);
  const hasLaughter = /haha|lol|lmao|lmaoo/i.test(message);
  const hasExclaim  = message.includes('!');

  const readings: TextReading[] = [];

  // High warmth — interested / engaged reading
  if (warmth >= 68) {
    readings.push({
      interpretation: hasQuestion
        ? 'They asked a question back — that\'s a genuine sign of interest. They want to keep talking.'
        : 'This reads warm and engaged. The effort they put into this message is noticeable.',
      confidence: warmth >= 82 ? 'high' : 'medium',
      vibeTag:    hasLaughter || hasExclaim ? 'playful' : 'warm',
    });
  }

  // Mid warmth — friendly / ambiguous
  if (warmth >= 42 && warmth < 72) {
    readings.push({
      interpretation: isShort
        ? 'Could be a quick reply between things — short doesn\'t always mean cold. Watch if it\'s a pattern.'
        : 'Friendly and conversational. Hard to gauge deeper intent from this alone, which is totally normal.',
      confidence: 'medium',
      vibeTag:    'friendly',
    });
  }

  // Low warmth — could be distracted or disinterested
  if (warmth < 45) {
    readings.push({
      interpretation: isShort
        ? 'Short reply — could be busy, tired, or not sure how to respond. One message isn\'t the full story.'
        : 'The tone feels a little flat here. Could be an off day — or they\'re processing something.',
      confidence: 'low',
      vibeTag:    'neutral',
    });
  }

  // Long message bonus reading
  if (isLong && warmth >= 50) {
    readings.push({
      interpretation: 'A longer reply takes effort. They chose to write more — that usually means they\'re engaged.',
      confidence: 'high',
      vibeTag:    'engaged',
    });
  }

  // Emoji-without-words: light flirty / playful tone
  if (hasEmoji && !readings.some(r => r.vibeTag === 'playful')) {
    readings.push({
      interpretation: 'The emoji adds a lighter, warmer tone — hard to read deeper intent, but it\'s a friendly signal.',
      confidence: 'medium',
      vibeTag:    'playful',
    });
  }

  // Fallback: always return at least one reading
  if (readings.length === 0) {
    readings.push({
      interpretation: 'This message is genuinely ambiguous — could go several ways. More context or more messages will help.',
      confidence: 'low',
      vibeTag:    'unclear',
    });
  }

  // Return up to 3 distinct readings
  return readings.slice(0, 3);
}

// ─── Module ───────────────────────────────────────────────────────────────────

const DISCLAIMER =
  'Based on what you shared — texts can mean a lot of different things. ' +
  'These are possible interpretations, not facts about what they feel.';

/**
 * Decode the tone and intent of a text message from a crush.
 *
 * @param input  The message and optional context note.
 * @returns      DecodedText with multiple readings, a vibe label, and a warmth score.
 */
export function decodeText(input: TextInput): DecodedText {
  const warmthScore = scoreTextWarmth(input.messageFromCrush);
  const readings    = buildReadings(input.messageFromCrush, warmthScore);

  const topVibe    = readings[0]?.vibeTag ?? 'unclear';
  const overallVibe = VIBE_LABELS[topVibe] ?? '🤔 Hard to read';

  return {
    readings,
    overallVibe,
    warmthScore,
    disclaimer: DISCLAIMER,
  };
}
