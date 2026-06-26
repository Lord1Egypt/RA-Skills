/**
 * @edgebets/sdk
 *
 * TypeScript SDK for the EdgeBets sports simulation API.
 * Supports NBA, NFL, MLB, and MLS with x402 USDC payments on Solana.
 *
 * @packageDocumentation
 */

// Main client
export { EdgeBetsClient, createClient } from './client';

// Types
export type {
  // Config
  EdgeBetsConfig,
  WalletAdapter,
  BalanceResult,
  // Games
  Sport,
  Game,
  Team,
  GameOdds,
  GameStatus,
  GamesResponse,
  // Simulation
  SimulationResult,
  SimulationJob,
  SimulateOptions,
  JobStatus,
  EloRatings,
  FourFactors,
  EdgeAnalysis,
  BettingInsights,
  ScoreDistribution,
  DistributionStats,
  HistogramBucket,
  FactorBreakdown,
  // Picks
  DailyPick,
  TodaysPickResponse,
  TrackRecord,
} from './types';

// Errors
export {
  EdgeBetsError,
  PaymentRequiredError,
  InsufficientBalanceError,
  WalletNotConfiguredError,
  PollingTimeoutError,
  SimulationFailedError,
  ApiError,
  NetworkError,
} from './utils/errors';

// Constants (for advanced use cases)
export {
  EDGEBETS_API_URL,
  TREASURY_WALLET,
  USDC_MINT,
  PRICE_USDC,
  PRICE_USDC_RAW,
} from './constants';
