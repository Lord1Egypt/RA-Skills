import type {
  ReplyContext,
  ReplyOptions,
  ReplyOption,
  ReplyTone,
  UserGoal,
} from '../types.js';

// ─── Reply Templates ──────────────────────────────────────────────────────────

interface TemplateSet {
  bold:  { text: string; rationale: string };
  chill: { text: string; rationale: string };
  safe:  { text: string; rationale: string };
  tip:   string;
}

const TEMPLATES: Record<UserGoal, TemplateSet> = {
  'keep-talking': {
    bold: {
      text:      'Ok wait — I need to know more about that. Tell me everything 😄',
      rationale: 'Shows you were actually listening and signals real enthusiasm without pressure.',
    },
    chill: {
      text:      'Haha okay that\'s actually so funny — how did that even happen?',
      rationale: 'Casual follow-up that invites them to share more without feeling intense.',
    },
    safe: {
      text:      'That\'s cool! So is that something you\'re really into, or more of a one-time thing?',
      rationale: 'Safe and natural — turns the conversation back to them in an easy way.',
    },
    tip: 'A genuine follow-up question is almost always the smoothest move. It shows you\'re listening.',
  },

  'show-interest': {
    bold: {
      text:      'Honestly, I always look forward to your messages — just saying 😊',
      rationale: 'Direct without being overwhelming. Lets them know you\'re into the conversation, not just being polite.',
    },
    chill: {
      text:      'You always have the best takes, not gonna lie',
      rationale: 'A genuine compliment that feels natural mid-convo rather than out of nowhere.',
    },
    safe: {
      text:      'This is lowkey one of my favourite conversations lately',
      rationale: 'Warm and positive, but still leaves room for them to respond however they feel comfortable.',
    },
    tip: 'Showing interest doesn\'t need to be dramatic. Small, genuine compliments land better than big declarations.',
  },

  'play-cool': {
    bold: {
      text:      'Lol okay I\'ll allow it 😏',
      rationale: 'Playful and confident. Engages without signalling you\'re waiting around.',
    },
    chill: {
      text:      'Ha, fair enough. What else you got?',
      rationale: 'Light banter that keeps things fun without over-investing.',
    },
    safe: {
      text:      'That\'s actually a solid point 😄 who knew',
      rationale: 'Low-stakes and friendly — keeps the conversation going casually.',
    },
    tip: 'Playing it cool works best when it feels natural. Avoid artificial delays or leaving someone on read on purpose — that\'s not cool, it\'s just unkind.',
  },

  'ask-out': {
    bold: {
      text:      'Okay I have to ask — we should hang sometime. You free this week?',
      rationale: 'Direct, confident, and specific. Much better than a vague "we should hang someday".',
    },
    chill: {
      text:      'Hey random thought — do you want to [grab food / watch that / check out that place] sometime? No pressure, just thought it\'d be fun',
      rationale: 'Keeps the stakes low by framing it casually and including "no pressure". Replace the brackets with something real.',
    },
    safe: {
      text:      'We\'ve been talking about [that thing] forever — we should actually just do it sometime',
      rationale: 'Ties the ask to something organic from your conversation, so it doesn\'t come out of nowhere.',
    },
    tip: 'The best ask-out texts are specific (suggest something real) and low-pressure. You don\'t need a perfect moment — just an honest one.',
  },
};

// ─── Module ───────────────────────────────────────────────────────────────────

/**
 * Generate three reply options (bold / chill / safe) for a given goal.
 *
 * @param context  Decoded text and the user's goal.
 * @returns        ReplyOptions with three replies and a coaching tip.
 */
export function generateReplies(context: ReplyContext): ReplyOptions {
  const template = TEMPLATES[context.userGoal];
  const tones: ReplyTone[] = ['bold', 'chill', 'safe'];

  const replies: ReplyOption[] = tones.map(tone => ({
    tone,
    text:      template[tone].text,
    rationale: template[tone].rationale,
  }));

  return {
    goal: context.userGoal,
    replies,
    tip: template.tip,
  };
}
