/**
 * Supported sports leagues
 */
export type Sport = 'nba' | 'nfl' | 'mlb' | 'mls';

/**
 * Team information
 */
export interface Team {
  name: string;
  abbreviation: string;
  logoUrl?: string;
  record?: string;
}

/**
 * Betting odds for a game
 */
export interface GameOdds {
  /** Home team moneyline (American odds, e.g., -150) */
  homeMoneyline?: number;
  /** Away team moneyline (American odds, e.g., +130) */
  awayMoneyline?: number;
  /** Point spread (negative = home favored) */
  spread?: number;
  /** Home spread odds */
  homeSpreadOdds?: number;
  /** Away spread odds */
  awaySpreadOdds?: number;
  /** Over/under total points */
  total?: number;
  /** Over odds */
  overOdds?: number;
  /** Under odds */
  underOdds?: number;
}

/**
 * Game status
 */
export type GameStatus = 'scheduled' | 'in_progress' | 'final' | 'postponed' | 'cancelled';

/**
 * Game information
 */
export interface Game {
  /** Unique game identifier (e.g., "nba-2026-03-28-lal-bos") */
  id: string;
  /** Sport league */
  sport: Sport;
  /** Home team */
  homeTeam: Team;
  /** Away team */
  awayTeam: Team;
  /** Game start time (ISO 8601) */
  startTime: string;
  /** Current game status */
  status: GameStatus;
  /** Betting odds (if available) */
  odds?: GameOdds;
  /** Venue name */
  venue?: string;
  /** Home team score (if in_progress or final) */
  homeScore?: number;
  /** Away team score (if in_progress or final) */
  awayScore?: number;
}

/**
 * Response from getGames()
 */
export interface GamesResponse {
  games: Game[];
  sport: Sport;
  date: string;
}
