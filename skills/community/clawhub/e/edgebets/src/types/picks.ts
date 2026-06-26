/**
 * Pick of the day data
 */
export interface DailyPick {
  /** Pick date (YYYY-MM-DD) */
  date: string;
  /** Sport (nba, nfl, mlb, mls) */
  sport: string;
  /** Game ID */
  gameId: string;
  /** Home team name */
  homeTeam: string;
  /** Away team name */
  awayTeam: string;
  /** Pick type: moneyline, spread, or total */
  pickType: 'moneyline' | 'spread' | 'total';
  /** The actual pick (team name for ML/spread, "over"/"under" for total) */
  pick: string;
  /** Pick value (spread points or total line) */
  pickValue?: number;
  /** Odds for the pick (American format) */
  odds?: number;
  /** Win probability from simulation */
  winProbability: number;
  /** Edge vs market */
  edge?: number;
  /** Confidence level */
  confidence: 'high' | 'medium' | 'low';
  /** Brief analysis */
  analysis?: string;
  /** Game start time */
  gameTime?: string;
  /** Result after game: win, loss, push, or pending */
  result?: 'win' | 'loss' | 'push' | 'pending';
  /** Actual final score */
  finalScore?: string;
}

/**
 * Response from getTodaysPick()
 */
export interface TodaysPickResponse {
  /** Whether a pick is available */
  hasPick: boolean;
  /** Whether this is today's pick (vs yesterday's) */
  isTodaysPick?: boolean;
  /** The pick data */
  pick?: DailyPick;
  /** Status message */
  message?: string;
  /** When the next pick will be available */
  nextPickTime?: string;
}

/**
 * Track record statistics
 */
export interface TrackRecord {
  /** Total wins */
  wins: number;
  /** Total losses */
  losses: number;
  /** Total pushes */
  pushes: number;
  /** Total picks made */
  totalPicks: number;
  /** Win rate percentage */
  winRate: number;
  /** Current streak (positive = wins, negative = losses) */
  streak: number;
  /** Streak type: "W" or "L" */
  streakType: 'W' | 'L';
  /** Recent picks */
  recentPicks: DailyPick[];
}
