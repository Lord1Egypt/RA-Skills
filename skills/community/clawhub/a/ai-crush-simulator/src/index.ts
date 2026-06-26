// ─── AI Crush Simulator — Public API ─────────────────────────────────────────
// Re-export all modules and types for external use or ClawHub integration.

export { analyzeCrush }   from './modules/crushAnalysis.js';
export { decodeText }     from './modules/textDecoder.js';
export { generateReplies} from './modules/replyGenerator.js';
export { adviseNextMove } from './modules/nextMove.js';

export type {
  // Shared
  ConnectionDepth,
  FlagColor,
  UserGoal,
  ReplyTone,
  NextMoveAction,
  Flag,

  // crushAnalysis
  CrushSituation,
  AnalysisResult,

  // textDecoder
  TextInput,
  TextReading,
  DecodedText,

  // replyGenerator
  ReplyContext,
  ReplyOption,
  ReplyOptions,

  // nextMove
  MoveContext,
  NextMoveTip,
  NextMoveResult,
} from './types.js';
