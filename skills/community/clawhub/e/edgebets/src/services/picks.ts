import type { ResolvedConfig, TodaysPickResponse, TrackRecord, DailyPick } from '../types';
import { ApiError, NetworkError } from '../utils/errors';

/**
 * Picks service for getting daily picks and track record
 */
export class PicksService {
  constructor(private config: ResolvedConfig) {}

  /**
   * Get today's pick of the day (FREE)
   *
   * If the game has already been played, suggests checking back at 2 AM Central.
   */
  async getTodaysPick(): Promise<TodaysPickResponse> {
    const url = `${this.config.apiBaseUrl}/picks/today`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch pick: ${response.status}`,
          response.status,
          errorData
        );
      }

      const data = await response.json();
      return this.normalizePickResponse(data);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        'Failed to fetch today\'s pick',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Get track record and recent picks (FREE)
   */
  async getTrackRecord(limit: number = 30): Promise<TrackRecord> {
    const url = `${this.config.apiBaseUrl}/picks/track-record?limit=${limit}`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch track record: ${response.status}`,
          response.status,
          errorData
        );
      }

      const data = await response.json();
      return this.normalizeTrackRecord(data);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        'Failed to fetch track record',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Normalize pick response from API
   */
  private normalizePickResponse(data: Record<string, unknown>): TodaysPickResponse {
    const hasPick = Boolean(data.has_pick);
    const isTodaysPick = Boolean(data.is_todays_pick);
    const pick = data.pick ? this.normalizePick(data.pick as Record<string, unknown>) : undefined;

    // Check if game has been played
    let message = data.message as string | undefined;
    let nextPickTime: string | undefined;

    if (pick && pick.result && pick.result !== 'pending') {
      // Game already played
      message = `Today's pick (${pick.pick}) has already been graded: ${pick.result.toUpperCase()}. New pick available at 2 AM Central.`;
      nextPickTime = '2:00 AM Central';
    } else if (!isTodaysPick && hasPick) {
      message = message || "Showing yesterday's pick. New pick available at 2 AM Central.";
      nextPickTime = '2:00 AM Central';
    }

    return {
      hasPick,
      isTodaysPick,
      pick,
      message,
      nextPickTime,
    };
  }

  /**
   * Normalize a single pick
   */
  private normalizePick(data: Record<string, unknown>): DailyPick {
    return {
      date: String(data.date || ''),
      sport: String(data.sport || ''),
      gameId: String(data.game_id || data.gameId || ''),
      homeTeam: String(data.home_team || data.homeTeam || ''),
      awayTeam: String(data.away_team || data.awayTeam || ''),
      pickType: (data.pick_type || data.pickType || 'moneyline') as DailyPick['pickType'],
      pick: String(data.pick || ''),
      pickValue: typeof data.pick_value === 'number' ? data.pick_value : undefined,
      odds: typeof data.odds === 'number' ? data.odds : undefined,
      winProbability: Number(data.win_probability || data.winProbability || 0),
      edge: typeof data.edge === 'number' ? data.edge : undefined,
      confidence: (data.confidence || 'medium') as DailyPick['confidence'],
      analysis: data.analysis as string | undefined,
      gameTime: data.game_time || data.gameTime as string | undefined,
      result: data.result as DailyPick['result'] | undefined,
      finalScore: data.final_score || data.finalScore as string | undefined,
    };
  }

  /**
   * Normalize track record from API
   */
  private normalizeTrackRecord(data: Record<string, unknown>): TrackRecord {
    const recentPicks = Array.isArray(data.recent_picks || data.recentPicks)
      ? (data.recent_picks || data.recentPicks as unknown[]).map(
          (p) => this.normalizePick(p as Record<string, unknown>)
        )
      : [];

    return {
      wins: Number(data.wins || 0),
      losses: Number(data.losses || 0),
      pushes: Number(data.pushes || 0),
      totalPicks: Number(data.total_picks || data.totalPicks || 0),
      winRate: Number(data.win_rate || data.winRate || 0),
      streak: Number(data.streak || 0),
      streakType: (data.streak_type || data.streakType || 'W') as 'W' | 'L',
      recentPicks,
    };
  }
}
