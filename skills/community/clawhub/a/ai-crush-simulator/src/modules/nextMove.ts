import type { MoveContext, NextMoveResult, NextMoveAction } from '../types.js';

// ─── Action Definitions ───────────────────────────────────────────────────────

interface ActionConfig {
  headline:  string;
  reasoning: (ctx: MoveContext) => string;
  tips:      string[];
}

const ACTIONS: Record<NextMoveAction, ActionConfig> = {
  keepChatting: {
    headline: '💬 Keep the conversation going',
    reasoning: () =>
      'Things are moving in a positive direction. The energy is there — keep building it naturally, ' +
      'without forcing any big moments. Good connections don\'t need to be rushed.',
    tips: [
      'Ask a follow-up question about something they actually mentioned',
      'Share something genuine about yourself too — connection goes both ways',
      'Keep the tone light and fun for now; enjoy the process',
    ],
  },

  askToHang: {
    headline: '📅 Suggest hanging out',
    reasoning: () =>
      'You\'ve built enough of a rapport that suggesting something in person feels natural, not random. ' +
      'A low-pressure, specific invite is all you need — you don\'t have to make it a big deal.',
    tips: [
      'Suggest something concrete: "want to grab [food / coffee / see that movie]?"',
      'Pick something you\'d actually enjoy doing — authenticity always comes through',
      'Don\'t over-plan the conversation in your head before they even respond',
    ],
  },

  giveSpace: {
    headline: '🌿 Give it some breathing room',
    reasoning: () =>
      'The signals suggest they might need a little space — or that you could benefit from stepping back slightly. ' +
      'Backing off a bit often creates more genuine connection than constant contact ever does.',
    tips: [
      'Resist the urge to double-text or check in too quickly',
      'Put some of that energy into your own life — it\'s genuinely good for you and also attractive',
      'If they\'re interested, giving space often brings them back. If not, you\'ve saved yourself some effort.',
    ],
  },

  beMoreDirect: {
    headline: '🎯 Be a bit more direct',
    reasoning: () =>
      'You\'ve been building up to something — at some point, a little directness is kinder than endless ambiguity. ' +
      'It doesn\'t have to be a grand gesture. A clear, honest signal is all it takes.',
    tips: [
      'A simple genuine line goes a long way: "I\'d love to hang out sometime"',
      'You don\'t need perfect timing or a perfect setting — just honesty',
      'Whatever they say, you\'ll feel better for having been real rather than staying in limbo',
    ],
  },

  waitAndSee: {
    headline: '⏳ Wait and see',
    reasoning: () =>
      'Things are a little unclear right now — and that\'s completely okay. ' +
      'There isn\'t enough consistent data yet to confidently read the situation, ' +
      'so the smartest play is to let a few more natural interactions happen first.',
    tips: [
      'One or two interactions isn\'t enough data — patterns matter more than single moments',
      'Watch how they act consistently, not just in one message or one day',
      'You don\'t have to decide anything right now. Enjoy getting to know them.',
    ],
  },
};

// ─── Decision Logic ───────────────────────────────────────────────────────────

function pickAction(ctx: MoveContext): NextMoveAction {
  const vibe     = ctx.vibeScore   ?? 50;
  const warmth   = ctx.warmthScore ?? 50;
  const combined = (vibe + warmth) / 2;
  const isLongTerm = /month|year/i.test(ctx.howLong ?? '');

  if (combined < 38)                                   return 'giveSpace';
  if (combined >= 70 && isLongTerm)                    return 'askToHang';
  if (combined >= 70 && !isLongTerm)                   return 'keepChatting';
  if (combined >= 55 && ctx.userGoal === 'ask-out')    return 'beMoreDirect';
  if (combined >= 55 && ctx.userGoal === 'show-interest') return 'keepChatting';
  if (combined >= 50 && combined < 70)                 return 'waitAndSee';
  return 'waitAndSee';
}

// ─── Module ───────────────────────────────────────────────────────────────────

const DISCLAIMER =
  'Based on what you shared — you know your situation better than any score. ' +
  'Trust your own judgment too, and remember: you can\'t control how someone else feels, only how you show up.';

/**
 * Recommend the best next move given the current context.
 *
 * @param ctx  Combined context from crushAnalysis, textDecoder, and user preference.
 * @returns    NextMoveResult with a recommended action, reasoning, and tips.
 */
export function adviseNextMove(ctx: MoveContext): NextMoveResult {
  const action = pickAction(ctx);
  const config = ACTIONS[action];

  return {
    action,
    headline:   config.headline,
    reasoning:  config.reasoning(ctx),
    tips:       config.tips.map(text => ({ text })),
    disclaimer: DISCLAIMER,
  };
}
