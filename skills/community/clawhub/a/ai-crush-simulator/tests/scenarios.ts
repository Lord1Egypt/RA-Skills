#!/usr/bin/env tsx
/**
 * AI Crush Simulator — Sample Test Scenarios
 * Run with: npm test
 *
 * Three realistic scenarios that exercise all four modules.
 * Output is formatted for easy reading / screenshot sharing.
 */

import { analyzeCrush }    from '../src/modules/crushAnalysis.js';
import { decodeText }      from '../src/modules/textDecoder.js';
import { generateReplies } from '../src/modules/replyGenerator.js';
import { adviseNextMove }  from '../src/modules/nextMove.js';

import type {
  CrushSituation,
  TextInput,
  ReplyContext,
  MoveContext,
} from '../src/types.js';

// ─── Display ──────────────────────────────────────────────────────────────────

const D = '─'.repeat(56);
const H = '═'.repeat(56);

function log(s = '')    { console.log(s); }
function header(t: string) { log(`\n${H}\n  ${t}\n${H}`); }
function section(t: string){ log(`\n${D}\n  ${t}\n${D}`); }

function renderAnalysis(r: ReturnType<typeof analyzeCrush>) {
  section('🔍 Crush Analysis');
  log(r.summary);
  if (r.signals.length) {
    log('\nSignals:');
    r.signals.forEach(s => log(`  ${s}`));
  }
  log(`\n  ℹ️  ${r.disclaimer}`);
}

function renderDecoded(d: ReturnType<typeof decodeText>) {
  section('💬 Text Decoded');
  log(`  Overall vibe : ${d.overallVibe}`);
  log(`  Warmth score : ${d.warmthScore}/100`);
  log('\n  Readings:');
  d.readings.forEach((r, i) => {
    log(`    ${i + 1}. [${r.confidence}] ${r.vibeTag} — ${r.interpretation}`);
  });
  log(`\n  ℹ️  ${d.disclaimer}`);
}

function renderReplies(r: ReturnType<typeof generateReplies>) {
  section('✏️  Reply Options');
  r.replies.forEach(reply => {
    const label = reply.tone === 'bold' ? '🔥 Bold' : reply.tone === 'chill' ? '😎 Chill' : '🙂 Safe';
    log(`\n  ${label}`);
    log(`    "${reply.text}"`);
    log(`    → ${reply.rationale}`);
  });
  log(`\n  💡 Tip: ${r.tip}`);
}

function renderNextMove(r: ReturnType<typeof adviseNextMove>) {
  section('🧭 Next Move');
  log(`  ${r.headline}`);
  log(`\n  ${r.reasoning}`);
  log('\n  Tips:');
  r.tips.forEach(t => log(`    • ${t.text}`));
  log(`\n  ℹ️  ${r.disclaimer}`);
}

// ─── Scenario Definitions ─────────────────────────────────────────────────────

interface Scenario {
  name:        string;
  description: string;
  situation:   CrushSituation;
  textInput:   TextInput;
  replyGoal:   ReplyContext['userGoal'];
}

const SCENARIOS: Scenario[] = [
  {
    name:        'Scenario 1 — The Encouraging Signs',
    description: 'Met in class, they texted first, always asks questions back, sent a long enthusiastic reply.',
    situation: {
      howTheyMet:            'We sit next to each other in chemistry class',
      howLong:               '3 months',
      interactionFrequency:  'they texted first a few times, we talk almost every day',
      recentInteractions:    'They remembered my favourite band, complimented my notes, invited me to a study group, asked me a question about my weekend',
      yourFeelingConfidence: 5,
    },
    textInput: {
      messageFromCrush: 'Omg yes I love that show!! Have you seen season 2? The finale literally had me crying 😭😭 we should watch it together sometime haha',
    },
    replyGoal: 'show-interest',
  },

  {
    name:        'Scenario 2 — The Mixed Signals',
    description: 'Met on an app, replies are inconsistent — sometimes warm, sometimes one word.',
    situation: {
      howTheyMet:            'Dating app, matched about 6 weeks ago',
      howLong:               '6 weeks',
      interactionFrequency:  'short replies some days, then suddenly long replies the next',
      recentInteractions:    'Hard to read. Sometimes they reply quickly with emoji, other times short replies or late reply. Never really asked me a question.',
      yourFeelingConfidence: 3,
    },
    textInput: {
      messageFromCrush: 'haha yeah',
    },
    replyGoal: 'keep-talking',
  },

  {
    name:        'Scenario 3 — The Ready-to-Ask-Out',
    description: 'Known each other for over a year, obvious mutual interest, user wants to take the next step.',
    situation: {
      howTheyMet:            'Mutual friend introduced us at a birthday party',
      howLong:               '14 months',
      interactionFrequency:  'text almost every day, see each other in the friend group regularly',
      recentInteractions:    'They texted first this week, we have a bunch of inside jokes, they remembered a random thing I said 3 weeks ago, suggested hanging out one-on-one',
      yourFeelingConfidence: 5,
    },
    textInput: {
      messageFromCrush: 'Wait I was literally just thinking about you 😂 remember when you said that thing about the arcade? We should actually go, I\'m free Friday or Saturday!',
    },
    replyGoal: 'ask-out',
  },
];

// ─── Runner ───────────────────────────────────────────────────────────────────

function runScenario(scenario: Scenario) {
  header(`💘 ${scenario.name}`);
  log(`  ${scenario.description}`);

  // Module 1: Crush Analysis
  const analysis = analyzeCrush(scenario.situation);
  renderAnalysis(analysis);

  // Module 2: Text Decoder
  const decoded = decodeText(scenario.textInput);
  renderDecoded(decoded);

  // Module 3: Reply Generator
  const replies = generateReplies({ decodedText: decoded, userGoal: scenario.replyGoal });
  renderReplies(replies);

  // Module 4: Next Move
  const moveCtx: MoveContext = {
    vibeScore:          analysis.vibeScore,
    warmthScore:        decoded.warmthScore,
    userGoal:           scenario.replyGoal,
    howLong:            scenario.situation.howLong,
    recentInteractions: scenario.situation.recentInteractions,
  };
  const nextMove = adviseNextMove(moveCtx);
  renderNextMove(nextMove);
}

function main() {
  header('💘 AI CRUSH SIMULATOR — TEST SCENARIOS');
  log('  Running all 3 sample scenarios across all 4 modules.\n');

  for (const scenario of SCENARIOS) {
    runScenario(scenario);
    log('\n');
  }

  header('✅ ALL SCENARIOS COMPLETE');
  log('  All modules ran without errors.\n');
}

main();
