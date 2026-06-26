#!/usr/bin/env tsx
/**
 * AI Crush Simulator — Local CLI
 * Run with: npm run cli
 */

import * as readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

import { analyzeCrush }    from '../src/modules/crushAnalysis.js';
import { decodeText }      from '../src/modules/textDecoder.js';
import { generateReplies } from '../src/modules/replyGenerator.js';
import { adviseNextMove }  from '../src/modules/nextMove.js';

import type {
  CrushSituation,
  UserGoal,
  DecodedText,
  AnalysisResult,
} from '../src/types.js';

// ─── Display Helpers ──────────────────────────────────────────────────────────

const DIVIDER = '─'.repeat(52);
const HEADER  = '═'.repeat(52);

function print(text: string = '') { console.log(text); }
function section(title: string)   { print(`\n${DIVIDER}\n  ${title}\n${DIVIDER}`); }
function header(title: string)    { print(`\n${HEADER}\n  ${title}\n${HEADER}`); }

function printAnalysis(result: AnalysisResult) {
  section('🔍 Crush Analysis');
  print(result.summary);
  if (result.signals.length > 0) {
    print('\nSignals detected:');
    for (const s of result.signals) print(`  ${s}`);
  }
  print(`\n💡 ${result.disclaimer}`);
}

function printDecoded(decoded: DecodedText) {
  section('💬 Text Decoded');
  print(`Overall vibe : ${decoded.overallVibe}`);
  print(`Warmth score : ${decoded.warmthScore}/100\n`);
  print('Possible readings:');
  for (const [i, r] of decoded.readings.entries()) {
    print(`\n  ${i + 1}. [${r.confidence.toUpperCase()} confidence] — ${r.vibeTag}`);
    print(`     ${r.interpretation}`);
  }
  print(`\n💡 ${decoded.disclaimer}`);
}

function printReplies(options: ReturnType<typeof generateReplies>) {
  section('✏️  Reply Options');
  for (const reply of options.replies) {
    const label = reply.tone === 'bold'  ? '🔥 Bold'
                : reply.tone === 'chill' ? '😎 Chill'
                :                          '🙂 Safe';
    print(`\n${label}`);
    print(`  "${reply.text}"`);
    print(`  → ${reply.rationale}`);
  }
  print(`\n💡 Tip: ${options.tip}`);
}

function printNextMove(result: ReturnType<typeof adviseNextMove>) {
  section('🧭 Next Move');
  print(result.headline);
  print(`\n${result.reasoning}\n`);
  print('Practical tips:');
  for (const tip of result.tips) print(`  • ${tip.text}`);
  print(`\n💡 ${result.disclaimer}`);
}

// ─── Prompts ──────────────────────────────────────────────────────────────────

async function askGoal(rl: readline.Interface): Promise<UserGoal> {
  print('\nWhat\'s your goal right now?');
  print('  1. Keep the conversation going');
  print('  2. Show I\'m interested');
  print('  3. Play it cool');
  print('  4. Ask them out');
  const ans = await rl.question('\nChoose (1–4): ');
  const map: Record<string, UserGoal> = {
    '1': 'keep-talking',
    '2': 'show-interest',
    '3': 'play-cool',
    '4': 'ask-out',
  };
  return map[ans.trim()] ?? 'keep-talking';
}

// ─── Flows ────────────────────────────────────────────────────────────────────

async function runFullCheck(rl: readline.Interface) {
  header('💘 FULL CRUSH CHECK');

  print('\n--- Tell me about your situation ---');
  const howTheyMet            = await rl.question('How did you meet? ');
  const howLong               = await rl.question('How long have you known each other? ');
  const interactionFrequency  = await rl.question('How often do you interact? ');
  const recentInteractions    = await rl.question('What have recent interactions been like? ');
  const confStr               = await rl.question('How sure are you about your feelings? (1–5): ');
  const yourFeelingConfidence = Math.min(5, Math.max(1, parseInt(confStr, 10) || 3));

  const situation: CrushSituation = {
    howTheyMet, howLong, interactionFrequency,
    recentInteractions, yourFeelingConfidence,
  };
  const analysis = analyzeCrush(situation);
  printAnalysis(analysis);

  print('\n--- Their last text ---');
  const messageFromCrush = await rl.question('What did they say? ');
  const decoded = decodeText({ messageFromCrush });
  printDecoded(decoded);

  const userGoal = await askGoal(rl);
  const replies  = generateReplies({ decodedText: decoded, userGoal });
  printReplies(replies);

  const nextMove = adviseNextMove({
    vibeScore:   analysis.vibeScore,
    warmthScore: decoded.warmthScore,
    userGoal,
    howLong:     situation.howLong,
    recentInteractions: situation.recentInteractions,
  });
  printNextMove(nextMove);
}

async function runAnalysisOnly(rl: readline.Interface) {
  header('🔍 CRUSH ANALYSIS');
  const howTheyMet           = await rl.question('How did you meet? ');
  const howLong              = await rl.question('How long have you known each other? ');
  const interactionFrequency = await rl.question('How often do you interact? ');
  const recentInteractions   = await rl.question('What have recent interactions been like? ');
  const confStr              = await rl.question('How sure are you about your feelings? (1–5): ');
  const yourFeelingConfidence = Math.min(5, Math.max(1, parseInt(confStr, 10) || 3));

  const result = analyzeCrush({
    howTheyMet, howLong, interactionFrequency,
    recentInteractions, yourFeelingConfidence,
  });
  printAnalysis(result);
}

async function runDecodeOnly(rl: readline.Interface) {
  header('💬 TEXT DECODER');
  const messageFromCrush = await rl.question('Paste their message: ');
  const contextNote      = await rl.question('Any context? (press enter to skip): ');
  const decoded = decodeText({
    messageFromCrush,
    ...(contextNote.trim() ? { contextNote } : {}),
  });
  printDecoded(decoded);
}

async function runReplyOnly(rl: readline.Interface) {
  header('✏️  REPLY GENERATOR');
  const messageFromCrush = await rl.question('Paste their message: ');
  const decoded  = decodeText({ messageFromCrush });
  const userGoal = await askGoal(rl);
  const replies  = generateReplies({ decodedText: decoded, userGoal });
  printReplies(replies);
}

async function runNextMoveOnly(rl: readline.Interface) {
  header('🧭 NEXT MOVE ADVISOR');
  const vibeStr   = await rl.question('Vibe score (0–100, or press enter for 50): ');
  const warmthStr = await rl.question('Warmth score (0–100, or press enter for 50): ');
  const howLong   = await rl.question('How long have you known each other? ');
  const userGoal  = await askGoal(rl);

  const result = adviseNextMove({
    vibeScore:   parseInt(vibeStr, 10)   || 50,
    warmthScore: parseInt(warmthStr, 10) || 50,
    howLong,
    userGoal,
  });
  printNextMove(result);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const rl = readline.createInterface({ input, output });

  header('💘 AI CRUSH SIMULATOR');
  print('  A fun, safe, youth-friendly crush advisor.');
  print('  Powered by vibes, heuristics, and good sense.\n');

  let running = true;
  while (running) {
    print('\nWhat would you like to do?');
    print('  1. Full Crush Check  (all modules)');
    print('  2. Analyze a Situation');
    print('  3. Decode a Text');
    print('  4. Generate Reply Options');
    print('  5. Get Next Move Advice');
    print('  0. Exit\n');

    const choice = await rl.question('Choose (0–5): ');
    print('');

    switch (choice.trim()) {
      case '1': await runFullCheck(rl);    break;
      case '2': await runAnalysisOnly(rl); break;
      case '3': await runDecodeOnly(rl);   break;
      case '4': await runReplyOnly(rl);    break;
      case '5': await runNextMoveOnly(rl); break;
      case '0':
        print('Good luck out there 💘');
        running = false;
        break;
      default:
        print('Please enter a number from 0 to 5.');
    }
  }

  rl.close();
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
