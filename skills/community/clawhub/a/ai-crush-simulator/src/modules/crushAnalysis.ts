import { scoreSignals, detectFlags } from '../scoring/heuristics.js';
import type {
  CrushSituation,
  AnalysisResult,
  ConnectionDepth,
} from '../types.js';

// ─── Connection Depth ─────────────────────────────────────────────────────────

const DEPTH_LABELS: Record<ConnectionDepth, string> = {
  'surface':              'Still getting acquainted — early days, keep things light',
  'friendly':             'A solid friendly connection is forming',
  'warm':                 'There\'s real warmth and mutual interest here',
  'potentially-romantic': 'Strong connection with genuine romantic potential',
};

function determineDepth(score: number, howLong: string): ConnectionDepth {
  const isLongTerm = /month|year/i.test(howLong);
  if (score >= 72 && isLongTerm) return 'potentially-romantic';
  if (score >= 65)               return 'warm';
  if (score >= 45)               return 'friendly';
  return 'surface';
}

// ─── Module ───────────────────────────────────────────────────────────────────

const DISCLAIMER =
  'Based on what you shared — only they know what they truly feel. ' +
  'These observations are meant to help you think, not to predict another person.';

/**
 * Analyze a crush situation and return a structured vibe reading.
 *
 * @param situation  Structured description of the situation.
 * @returns          AnalysisResult with score, depth, flags, and summary.
 */
export function analyzeCrush(situation: CrushSituation): AnalysisResult {
  const combinedInput = [
    situation.howTheyMet,
    situation.interactionFrequency,
    situation.recentInteractions,
  ].join(' ');

  const vibeScore       = scoreSignals(combinedInput);
  const flags           = detectFlags(combinedInput);
  const connectionDepth = determineDepth(vibeScore, situation.howLong);

  const greenFlags = flags.filter(f => f.color === 'green');
  const yellowFlags = flags.filter(f => f.color === 'yellow');
  const redFlags   = flags.filter(f => f.color === 'red');

  // Build a readable signals list
  const signals: string[] = [];

  if (situation.yourFeelingConfidence >= 4) {
    signals.push('✓ You feel confident about your own feelings — that clarity is an asset');
  }
  for (const f of greenFlags)  signals.push(`✅ ${f.label}`);
  for (const f of yellowFlags) signals.push(`🟡 ${f.label}`);
  for (const f of redFlags)    signals.push(`🔴 ${f.label}`);

  const flagSummary =
    flags.length === 0
      ? 'No strong signals either way — totally normal at this stage.'
      : `${greenFlags.length} green, ${yellowFlags.length} yellow, ${redFlags.length} red flag(s) detected.`;

  const summary = [
    `Vibe score     : ${vibeScore}/100`,
    `Connection     : ${DEPTH_LABELS[connectionDepth]}`,
    `Flags          : ${flagSummary}`,
  ].join('\n');

  return {
    vibeScore,
    connectionDepth,
    flags,
    signals,
    summary,
    disclaimer: DISCLAIMER,
  };
}
