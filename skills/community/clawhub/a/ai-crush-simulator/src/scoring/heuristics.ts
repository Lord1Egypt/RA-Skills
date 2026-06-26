import type { Flag, FlagColor } from '../types.js';

// ─── Signal Dictionaries ──────────────────────────────────────────────────────

const POSITIVE_SIGNALS = [
  'texted first',
  'messaged first',
  'reached out first',
  'initiated',
  'double texted',
  'followed up',
  'kept the conversation going',
  'asked me a question',
  'asked about me',
  'remembered',
  'complimented',
  'said they miss',
  'invited me',
  'suggested hanging',
  'suggested plans',
  'made plans',
  'inside joke',
  'replied quickly',
  'replied fast',
  'quick replies',
  'fast replies',
  'laughed at my',
  'sends long messages',
  'long replies',
  'always responds',
  'always replies',
];

const NEGATIVE_SIGNALS = [
  'one word',
  'one-word',
  'left on read',
  'takes days to reply',
  'took days',
  'never replies',
  'rarely replies',
  'cancelled plans',
  'canceled plans',
  'cancelled on me',
  'ignored my',
  'short replies',
  'never asks questions',
  'always ends the conversation',
  'avoids hanging',
  'avoids meeting',
  'only responds sometimes',
  'ghosts',
  'ghosted',
];

const AMBIGUOUS_SIGNALS = [
  'busy',
  'might be shy',
  'hard to read',
  'neutral',
  'emoji only',
  'late reply',
  'late replies',
];

// ─── Text Analysis Markers ────────────────────────────────────────────────────

const ENTHUSIASM_MARKERS = [
  '!', 'haha', 'lol', 'lmao', 'omg', 'omgg', 'yess', 'yasss',
  'literally', 'fr fr', 'no way', 'wait what', 'seriously',
  '😊', '😂', '🥺', '❤️', '💕', '😍', '😭', '🙈', '✨', '💀',
];

// Exact-match cold words (whole word only)
const COLD_WORDS = new Set(['k', 'ok', 'sure', 'fine', 'whatever', 'idk', 'maybe', 'i guess']);

// ─── Scoring Functions ────────────────────────────────────────────────────────

/**
 * Score a free-text situation description based on positive/negative signal patterns.
 * Returns a 0–100 score; 50 is neutral.
 */
export function scoreSignals(input: string): number {
  const lower = input.toLowerCase();
  let score = 50;

  for (const signal of POSITIVE_SIGNALS) {
    if (lower.includes(signal)) score += 8;
  }
  for (const signal of NEGATIVE_SIGNALS) {
    if (lower.includes(signal)) score -= 10;
  }
  for (const signal of AMBIGUOUS_SIGNALS) {
    if (lower.includes(signal)) score -= 2;
  }

  return clamp(score, 0, 100);
}

/**
 * Score the warmth of a single text message.
 * Returns a 0–100 score; higher = warmer / more engaged.
 */
export function scoreTextWarmth(text: string): number {
  const lower = text.toLowerCase();
  let score = 40; // start slightly below neutral — a text needs to earn warmth

  // Enthusiasm markers
  for (const marker of ENTHUSIASM_MARKERS) {
    if (lower.includes(marker)) score += 5;
  }

  // Cold/dismissive single words (whole-word match)
  const words = lower.split(/\s+/);
  for (const word of words) {
    if (COLD_WORDS.has(word)) score -= 8;
  }

  // Questions back: each '?' is a strong engagement signal
  const questionCount = (text.match(/\?/g) ?? []).length;
  score += questionCount * 10;

  // Reply length signals effort
  if (text.length > 120) score += 10;
  else if (text.length > 60) score += 5;
  else if (text.length < 10) score -= 10;

  // Emoji count (each emoji adds a little warmth, capped)
  const emojiCount = Math.min((text.match(/\p{Emoji_Presentation}/gu) ?? []).length, 4);
  score += emojiCount * 3;

  return clamp(score, 0, 100);
}

// ─── Flag Detection ───────────────────────────────────────────────────────────

const GREEN_PATTERNS: Array<[string, string]> = [
  ['texted first',        'They initiated — a positive sign of interest'],
  ['messaged first',      'They reached out first — shows initiative'],
  ['reached out first',   'They reached out first — shows initiative'],
  ['double texted',       'They followed up — they wanted to connect'],
  ['followed up',         'Following up shows they were thinking about you'],
  ['asked me a question', 'Asking questions shows genuine curiosity about you'],
  ['asked about me',      'Shows they want to know more about you'],
  ['made plans',          'Concrete plans signal real interest, not just chat'],
  ['suggested hanging',   'Suggesting plans is a clear positive signal'],
  ['complimented',        'Compliments are a warm, encouraging sign'],
  ['remembered',          'Remembering details means they pay attention to you'],
  ['invited',             'An invitation to something is a strong positive signal'],
  ['inside joke',         'Inside jokes signal closeness and a real connection'],
  ['replied quickly',     'Quick replies suggest they look forward to hearing from you'],
  ['long replies',        'Long replies show effort and engagement'],
];

const YELLOW_PATTERNS: Array<[string, string]> = [
  ['busy',         'Could be genuinely busy — or creating distance. Watch the pattern.'],
  ['short replies','Short replies are ambiguous — style vs. disinterest depends on context'],
  ['emoji only',   'Emoji-only replies are friendly but hard to read deeper intent from'],
  ['late reply',   'Late replies could be life getting in the way, or hesitation'],
  ['might be shy', 'Shyness can look like disinterest — look for small warmth signals'],
  ['hard to read', 'Unclear signals — more interactions will give you a clearer picture'],
];

const RED_PATTERNS: Array<[string, string]> = [
  ['left on read',       'Consistently left on read is a signal to give it some space'],
  ['cancelled plans',    'Cancelling plans — especially repeatedly — is worth noticing'],
  ['canceled plans',     'Cancelling plans — especially repeatedly — is worth noticing'],
  ['ignored my',         'Being ignored is a sign to slow down and respect your own energy'],
  ['never asks questions','One-sided interest is tiring. Healthy connections are mutual.'],
  ['ghosted',            'Ghosting is a clear signal to redirect your energy elsewhere'],
  ['avoids hanging',     'Consistently avoiding in-person time is a pattern worth heeding'],
];

/**
 * Detect green / yellow / red flags in a situation description.
 */
export function detectFlags(input: string): Flag[] {
  const lower = input.toLowerCase();
  const flags: Flag[] = [];

  const addFlags = (patterns: Array<[string, string]>, color: FlagColor) => {
    for (const [pattern, reason] of patterns) {
      if (lower.includes(pattern)) {
        flags.push({ color, label: pattern, reason });
      }
    }
  };

  addFlags(GREEN_PATTERNS, 'green');
  addFlags(YELLOW_PATTERNS, 'yellow');
  addFlags(RED_PATTERNS, 'red');

  return flags;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}
