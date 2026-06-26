// CK-Arena API Client

const API_BASE = process.env.CKARENA_API || 'http://43.134.60.58:8000';

export interface ArenaStatus {
  queue_length: number;
  min_players_needed: number;
  can_start: boolean;
  waiting_players: Array<{
    player_id: string;
    player_name: string;
    elo_rating: number;
    wait_time_seconds: number;
  }>;
}

export interface ArenaPlayer {
  rank: number;
  player_id: string;
  name: string;
  elo_rating: number;
  games_played: number;
  games_won: number;
  games_lost: number;
  win_rate: number;
}

export async function joinArena(playerId: string): Promise<{success: boolean; message: string; game_id?: string; status: string}> {
  const res = await fetch(`${API_BASE}/api/arena/join?player_id=${playerId}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{success: boolean; message: string; game_id?: string; status: string}>;
}

export async function leaveArena(playerId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/arena/leave?player_id=${playerId}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error(await res.text());
}

export async function getArenaStatus(): Promise<ArenaStatus> {
  const res = await fetch(`${API_BASE}/api/arena/status`);
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<ArenaStatus>;
}

export async function getMyGame(playerId: string): Promise<{in_game: boolean; game_id?: string; game?: any}> {
  const res = await fetch(`${API_BASE}/api/arena/my-game/${playerId}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{in_game: boolean; game_id?: string; game?: any}>;
}

export async function getArenaLeaderboard(limit: number = 100): Promise<{total: number; players: ArenaPlayer[]}> {
  const res = await fetch(`${API_BASE}/api/arena/leaderboard?limit=${limit}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{total: number; players: ArenaPlayer[]}>;
}
