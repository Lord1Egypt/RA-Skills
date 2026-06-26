import { Keypair } from '@solana/web3.js';
import type {
  EdgeBetsConfig,
  ResolvedConfig,
  Sport,
  Game,
  SimulationResult,
  SimulationJob,
  SimulateOptions,
  BalanceResult,
  TodaysPickResponse,
  TrackRecord,
} from './types';
import {
  EDGEBETS_API_URL,
  DEFAULT_RPC_ENDPOINT,
  DEFAULT_POLLING_INTERVAL,
  DEFAULT_POLLING_TIMEOUT,
} from './constants';
import { GamesService } from './services/games';
import { PaymentService } from './services/payment';
import { SimulationService } from './services/simulation';
import { PicksService } from './services/picks';
import { RequestQueue } from './utils/queue';

/** Default max concurrent simulations */
const DEFAULT_MAX_CONCURRENT = 1;

/** Default delay between requests in ms */
const DEFAULT_DELAY_BETWEEN = 2000;

/**
 * EdgeBets SDK Client
 *
 * Main entry point for interacting with the EdgeBets API.
 * Handles games fetching, payments, and simulations.
 *
 * @example
 * ```typescript
 * import { EdgeBetsClient } from '@edgebets/sdk';
 * import { Keypair } from '@solana/web3.js';
 *
 * const client = new EdgeBetsClient({
 *   wallet: Keypair.fromSecretKey(...),
 *   debug: true,
 * });
 *
 * // Get today's NBA games (FREE)
 * const games = await client.getGames('nba');
 *
 * // Run simulation ($0.50 USDC)
 * const result = await client.simulate('nba', games[0].id);
 * ```
 */
export class EdgeBetsClient {
  private config: ResolvedConfig;
  private gamesService: GamesService;
  private paymentService: PaymentService;
  private simulationService: SimulationService;
  private picksService: PicksService;
  private simulationQueue: RequestQueue;

  constructor(config: EdgeBetsConfig = {}) {
    this.config = this.resolveConfig(config);
    this.gamesService = new GamesService(this.config);
    this.paymentService = new PaymentService(this.config);
    this.simulationService = new SimulationService(this.config, this.paymentService);
    this.picksService = new PicksService(this.config);
    this.simulationQueue = new RequestQueue(
      this.config.maxConcurrent,
      this.config.delayBetween
    );

    if (this.config.debug) {
      console.log('[EdgeBets] Client initialized');
      console.log(`[EdgeBets] API: ${this.config.apiBaseUrl}`);
      console.log(`[EdgeBets] RPC: ${this.config.rpcEndpoint}`);
      console.log(`[EdgeBets] Wallet: ${this.config.wallet ? 'configured' : 'not configured'}`);
      console.log(`[EdgeBets] Rate limit: ${this.config.maxConcurrent} concurrent, ${this.config.delayBetween}ms delay`);
    }
  }

  /**
   * Resolve configuration with defaults
   */
  private resolveConfig(config: EdgeBetsConfig): ResolvedConfig {
    return {
      wallet: config.wallet || null,
      rpcEndpoint: config.rpcEndpoint || DEFAULT_RPC_ENDPOINT,
      apiBaseUrl: config.apiBaseUrl || EDGEBETS_API_URL,
      pollingInterval: config.pollingInterval || DEFAULT_POLLING_INTERVAL,
      pollingTimeout: config.pollingTimeout || DEFAULT_POLLING_TIMEOUT,
      debug: config.debug || false,
      maxConcurrent: config.maxConcurrent || DEFAULT_MAX_CONCURRENT,
      delayBetween: config.delayBetween || DEFAULT_DELAY_BETWEEN,
    };
  }

  // ============================================
  // GAMES (FREE - no payment required)
  // ============================================

  /**
   * Get today's games for a sport
   *
   * @param sport - The sport to get games for ('nba', 'nfl', 'mlb', 'mls')
   * @returns Array of games
   *
   * @example
   * ```typescript
   * const games = await client.getGames('nba');
   * console.log(`Found ${games.length} NBA games today`);
   * ```
   */
  async getGames(sport: Sport): Promise<Game[]> {
    return this.gamesService.getGames(sport);
  }

  /**
   * Get tomorrow's games for a sport
   *
   * @param sport - The sport to get games for
   * @returns Array of games
   */
  async getTomorrowGames(sport: Sport): Promise<Game[]> {
    return this.gamesService.getTomorrowGames(sport);
  }

  /**
   * Get details for a specific game
   *
   * @param sport - The sport
   * @param gameId - Game identifier
   * @returns Game details
   */
  async getGameDetails(sport: Sport, gameId: string): Promise<Game> {
    return this.gamesService.getGameDetails(sport, gameId);
  }

  // ============================================
  // SIMULATIONS (PAID - $0.50 USDC)
  // ============================================

  /**
   * Run a Monte Carlo simulation for a game
   *
   * This method handles the full x402 payment flow:
   * 1. Sends USDC payment to treasury
   * 2. Starts simulation with payment proof
   * 3. Polls until complete
   * 4. Returns result
   *
   * Rate limited to prevent overwhelming the API.
   * Default: 1 concurrent request, 2s delay between requests.
   *
   * @param sport - The sport ('nba', 'nfl', 'mlb', 'mls')
   * @param gameId - Game identifier
   * @param options - Simulation options
   * @returns Simulation result
   *
   * @example
   * ```typescript
   * const result = await client.simulate('nba', 'nba-2026-03-28-lal-bos', {
   *   onStatus: (status) => console.log(`Status: ${status}`),
   * });
   *
   * console.log(`Home win: ${(result.homeWinProbability * 100).toFixed(1)}%`);
   * console.log(`Total: ${result.averageTotalPoints.toFixed(1)}`);
   * ```
   */
  async simulate(
    sport: Sport,
    gameId: string,
    options?: SimulateOptions
  ): Promise<SimulationResult> {
    // Queue the simulation to prevent overwhelming the API
    return this.simulationQueue.add(() =>
      this.simulationService.simulate(sport, gameId, options)
    );
  }

  /**
   * Get current queue status
   *
   * @returns Object with queued and running counts
   */
  getQueueStatus(): { queued: number; running: number } {
    return this.simulationQueue.getStatus();
  }

  /**
   * Start a simulation and get job for manual polling
   * (Advanced use case - prefer simulate() for most cases)
   *
   * @param sport - The sport
   * @param gameId - Game identifier
   * @returns Simulation job with polling URL
   */
  async startSimulation(sport: Sport, gameId: string): Promise<SimulationJob> {
    const signature = await this.paymentService.sendPayment();
    return this.simulationService.startSimulationWithPayment(sport, gameId, signature);
  }

  /**
   * Poll for simulation result
   *
   * @param jobId - Job identifier from startSimulation
   * @returns Simulation job with current status
   */
  async pollResult(jobId: string): Promise<SimulationJob> {
    return this.simulationService.pollResult(jobId);
  }

  // ============================================
  // PICKS (FREE - no payment required)
  // ============================================

  /**
   * Get today's pick of the day (FREE)
   *
   * Returns the daily expert pick with analysis.
   * If the game has been played, indicates when the next pick will be available.
   *
   * @returns Today's pick response
   *
   * @example
   * ```typescript
   * const pick = await client.getTodaysPick();
   * if (pick.hasPick) {
   *   console.log(`Today's pick: ${pick.pick.pick} (${pick.pick.confidence})`);
   *   console.log(`Win probability: ${(pick.pick.winProbability * 100).toFixed(1)}%`);
   * } else {
   *   console.log(pick.message);  // "New pick available at 2 AM Central"
   * }
   * ```
   */
  async getTodaysPick(): Promise<TodaysPickResponse> {
    return this.picksService.getTodaysPick();
  }

  /**
   * Get track record and recent picks (FREE)
   *
   * @param limit - Number of recent picks to include (default 30)
   * @returns Track record statistics
   *
   * @example
   * ```typescript
   * const record = await client.getTrackRecord();
   * console.log(`Record: ${record.wins}-${record.losses}`);
   * console.log(`Win rate: ${record.winRate}%`);
   * console.log(`Current streak: ${record.streak}${record.streakType}`);
   * ```
   */
  async getTrackRecord(limit: number = 30): Promise<TrackRecord> {
    return this.picksService.getTrackRecord(limit);
  }

  // ============================================
  // PAYMENTS & WALLET
  // ============================================

  /**
   * Check wallet balance (USDC and SOL)
   *
   * @returns Balance information
   *
   * @example
   * ```typescript
   * const balance = await client.checkBalance();
   * console.log(`USDC: ${balance.usdc}`);
   * console.log(`SOL: ${balance.sol}`);
   * console.log(`Can simulate: ${balance.sufficient}`);
   * ```
   */
  async checkBalance(): Promise<BalanceResult> {
    return this.paymentService.checkBalance();
  }

  /**
   * Get simulation price quote
   *
   * @returns Price information
   */
  async getQuote(): Promise<{
    price: number;
    currency: string;
    network: string;
    recipient: string;
  }> {
    return this.simulationService.getQuote();
  }

  /**
   * Check if wallet is configured
   */
  hasWallet(): boolean {
    return this.paymentService.hasWallet();
  }

  /**
   * Get treasury wallet address
   */
  getTreasuryWallet(): string {
    return this.paymentService.getTreasuryWallet();
  }

  /**
   * Get simulation price in USDC
   */
  getPrice(): number {
    return this.paymentService.getPrice();
  }
}

/**
 * Create an EdgeBets client from a secret key
 *
 * @param secretKey - Solana wallet secret key (Uint8Array or number array)
 * @param config - Additional configuration
 * @returns Configured EdgeBets client
 *
 * @example
 * ```typescript
 * import { createClient } from '@edgebets/sdk';
 * import fs from 'fs';
 *
 * const secretKey = JSON.parse(fs.readFileSync('~/.config/solana/id.json', 'utf-8'));
 * const client = createClient(secretKey, { debug: true });
 * ```
 */
export function createClient(
  secretKey: Uint8Array | number[],
  config: Omit<EdgeBetsConfig, 'wallet'> = {}
): EdgeBetsClient {
  const keypair = Keypair.fromSecretKey(
    secretKey instanceof Uint8Array ? secretKey : Uint8Array.from(secretKey)
  );
  return new EdgeBetsClient({ ...config, wallet: keypair });
}
