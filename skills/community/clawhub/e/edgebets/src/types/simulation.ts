/**
 * Elo rating system data
 */
export interface EloRatings {
  /** Home team Elo rating */
  homeElo: number;
  /** Away team Elo rating */
  awayElo: number;
  /** Win probability based on Elo */
  eloHomeWinProb: number;
  /** Predicted spread from Elo */
  eloSpread: number;
}

/**
 * Four Factors basketball analytics (NBA)
 */
export interface FourFactors {
  home: {
    /** Effective field goal percentage */
    efg_pct: number;
    /** Turnover percentage */
    tov_pct: number;
    /** Offensive rebound percentage */
    oreb_pct: number;
    /** Free throw rate */
    ft_rate: number;
  };
  away: {
    efg_pct: number;
    tov_pct: number;
    oreb_pct: number;
    ft_rate: number;
  };
  /** Composite score for home team */
  homeComposite: number;
  /** Composite score for away team */
  awayComposite: number;
}

/**
 * Edge analysis vs market odds
 */
export interface EdgeAnalysis {
  /** Whether market odds are available */
  hasOdds: boolean;
  /** Edge on home moneyline (positive = value) */
  homeEdge: number;
  /** Edge on away moneyline */
  awayEdge: number;
  /** Home bet is value */
  homeIsValue: boolean;
  /** Away bet is value */
  awayIsValue: boolean;
  /** Edge on spread bet */
  spreadEdge: number;
  /** Edge on total (over/under) */
  totalEdge?: number;
  /** Kelly fraction for home bet */
  homeKelly?: number;
  /** Kelly fraction for away bet */
  awayKelly?: number;
}

/**
 * Human-readable betting insights
 */
export interface BettingInsights {
  /** Fair home moneyline (American odds) */
  fairHomeMoneyline: number;
  /** Fair away moneyline */
  fairAwayMoneyline: number;
  /** Fair spread */
  fairSpread: number;
  /** Fair total */
  fairTotal: number;
  /** Summary bullet points */
  summary: string[];
}

/**
 * Histogram bucket for score distribution
 */
export interface HistogramBucket {
  /** Range label (e.g., "100-104") */
  label: string;
  /** Number of simulations in this bucket */
  count: number;
  /** Percentage of total */
  pct: number;
}

/**
 * Distribution statistics
 */
export interface DistributionStats {
  mean: number;
  std: number;
  min: number;
  max: number;
  median: number;
  histogram: HistogramBucket[];
}

/**
 * Score distribution from Monte Carlo simulations
 */
export interface ScoreDistribution {
  homeScores: DistributionStats;
  awayScores: DistributionStats;
  totals: DistributionStats;
  spreads: DistributionStats;
}

/**
 * Factor impact analysis
 */
export interface FactorBreakdown {
  /** Factor name */
  name: string;
  /** Direction of impact: home, away, or neutral */
  direction: 'home' | 'away' | 'neutral' | 'total';
  /** Point impact */
  impact: number;
  /** Category: critical, high, medium, contextual */
  category: 'critical' | 'high' | 'medium' | 'contextual';
  /** Human-readable explanation */
  explanation: string;
}

/**
 * Full simulation result
 */
export interface SimulationResult {
  /** Game identifier */
  gameId: string;
  /** Number of Monte Carlo iterations */
  simulationCount: number;

  // Teams
  homeTeamName: string;
  awayTeamName: string;
  homeTeamAbbr: string;
  awayTeamAbbr: string;

  // Win Probabilities
  /** Home win probability (0-1) */
  homeWinProbability: number;
  /** Away win probability (0-1) */
  awayWinProbability: number;

  // Score Projections
  /** Average projected home score */
  averageHomeScore: number;
  /** Average projected away score */
  averageAwayScore: number;
  /** Average projected total points */
  averageTotalPoints: number;
  /** Predicted spread (positive = away favored) */
  predictedSpread: number;
  /** Standard deviation of spread */
  spreadStdDev?: number;
  /** Standard deviation of total */
  totalStdDev?: number;

  // Rare Events
  /** Probability of overtime */
  overtimeProbability?: number;

  // Advanced Analytics (optional based on sport)
  elo?: EloRatings;
  fourFactors?: FourFactors;
  edgeAnalysis?: EdgeAnalysis;
  bettingInsights?: BettingInsights;
  scoreDistribution?: ScoreDistribution;
  factorBreakdown?: FactorBreakdown[];
}

/**
 * Simulation job status
 */
export type JobStatus = 'processing' | 'complete' | 'error';

/**
 * Simulation job response (for polling)
 */
export interface SimulationJob {
  /** Unique job identifier */
  jobId: string;
  /** Current status */
  status: JobStatus;
  /** URL to poll for results */
  pollUrl: string;
  /** Simulation result (when complete) */
  result?: SimulationResult;
  /** Error message (when error) */
  error?: string;
  /** Estimated completion time in seconds */
  estimatedTime?: number;
}

/**
 * Options for simulate() method
 */
export interface SimulateOptions {
  /** Number of Monte Carlo iterations (default: 10000) */
  count?: number;
  /** Auto-poll until complete (default: true) */
  autoPoll?: boolean;
  /** Callback for status updates during polling */
  onStatus?: (status: string, job?: SimulationJob) => void;
  /** Polling interval in ms (default: 3000) */
  pollingInterval?: number;
  /** Polling timeout in ms (default: 120000) */
  pollingTimeout?: number;
}
