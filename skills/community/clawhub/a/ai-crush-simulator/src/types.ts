// ─── Shared Types ────────────────────────────────────────────────────────────

export type ConnectionDepth =
  | 'surface'
  | 'friendly'
  | 'warm'
  | 'potentially-romantic';

export type FlagColor = 'green' | 'yellow' | 'red';

export type UserGoal =
  | 'keep-talking'
  | 'show-interest'
  | 'play-cool'
  | 'ask-out';

export type ReplyTone = 'bold' | 'chill' | 'safe';

export type NextMoveAction =
  | 'keepChatting'
  | 'askToHang'
  | 'giveSpace'
  | 'beMoreDirect'
  | 'waitAndSee';

// ─── crushAnalysis ────────────────────────────────────────────────────────────

export interface Flag {
  color: FlagColor;
  label: string;
  reason: string;
}

export interface CrushSituation {
  howTheyMet: string;            // e.g. "class", "app", "mutual friend"
  howLong: string;               // e.g. "2 weeks", "6 months"
  interactionFrequency: string;  // e.g. "daily texts", "occasional likes"
  recentInteractions: string;    // free-text description
  yourFeelingConfidence: number; // 1–5: how sure you are you like them
}

export interface AnalysisResult {
  vibeScore: number;             // 0–100
  connectionDepth: ConnectionDepth;
  flags: Flag[];
  signals: string[];
  summary: string;
  disclaimer: string;
}

// ─── textDecoder ─────────────────────────────────────────────────────────────

export interface TextInput {
  messageFromCrush: string;
  contextNote?: string;          // optional: extra context about the convo
}

export interface TextReading {
  interpretation: string;
  confidence: 'low' | 'medium' | 'high';
  vibeTag: string;               // e.g. "playful", "warm", "neutral"
}

export interface DecodedText {
  readings: TextReading[];
  overallVibe: string;
  warmthScore: number;           // 0–100
  disclaimer: string;
}

// ─── replyGenerator ──────────────────────────────────────────────────────────

export interface ReplyContext {
  decodedText: DecodedText;
  userGoal: UserGoal;
  tonePref?: 'funny' | 'sincere' | 'neutral';
}

export interface ReplyOption {
  tone: ReplyTone;
  text: string;
  rationale: string;
}

export interface ReplyOptions {
  goal: UserGoal;
  replies: ReplyOption[];
  tip: string;
}

// ─── nextMove ────────────────────────────────────────────────────────────────

export interface MoveContext {
  vibeScore?: number;
  warmthScore?: number;
  userGoal?: UserGoal;
  howLong?: string;
  recentInteractions?: string;
}

export interface NextMoveTip {
  text: string;
}

export interface NextMoveResult {
  action: NextMoveAction;
  headline: string;
  reasoning: string;
  tips: NextMoveTip[];
  disclaimer: string;
}
