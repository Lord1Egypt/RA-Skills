// Undercover Game API Client

const API_BASE = process.env.UNDERCOVER_API_BASE || 'http://43.134.60.58:8000';

export interface Player {
  id: string;
  name: string;
  wins: number;
  games_played: number;
  created_at: string;
}

export interface Room {
  id: string;
  name: string;
  host_id: string;
  host_name: string;
  max_players: number;
  players: string[];
  player_names: string[];
  status: 'waiting' | 'playing' | 'finished';
  game_id: string | null;
  created_at: string;
}

export interface Game {
  id: string;
  room_id: string;
  status: 'waiting' | 'describing' | 'voting' | 'eliminated' | 'finished';
  current_round: number;
  max_rounds: number;
  current_player_idx: number;
  words: Record<string, string>;
  descriptions: Record<string, string>;
  votes: Record<string, string>;
  eliminated_players: string[];
  winner: string | null;
  created_at: string;
}

export interface LeaderboardEntry {
  player_id: string;
  player_name: string;
  wins: number;
  games_played: number;
  win_rate: number;
}

async function apiRequest<T>(method: string, path: string, body?: unknown): Promise<T> {
  const url = `${API_BASE}${path}`;
  const options: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) options.body = JSON.stringify(body);
  
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

// Player APIs
export async function createPlayer(name: string): Promise<Player> {
  return apiRequest<Player>('POST', '/api/players/', { name });
}

export async function getPlayer(playerId: string): Promise<Player> {
  return apiRequest<Player>('GET', `/api/players/${playerId}`);
}

// Room APIs
export async function listRooms(): Promise<Room[]> {
  return apiRequest<Room[]>('GET', '/api/rooms/');
}

export async function createRoom(name: string, hostId: string, maxPlayers = 8): Promise<Room> {
  return apiRequest<Room>('POST', '/api/rooms/', { name, host_id: hostId, max_players: maxPlayers });
}

export async function joinRoom(roomId: string, playerId: string): Promise<Room> {
  return apiRequest<Room>('POST', `/api/rooms/${roomId}/join`, { player_id: playerId });
}

export async function leaveRoom(roomId: string, playerId: string): Promise<Room> {
  return apiRequest<Room>('POST', `/api/rooms/${roomId}/leave`, { player_id: playerId });
}

export async function getRoom(roomId: string): Promise<Room> {
  return apiRequest<Room>('GET', `/api/rooms/${roomId}`);
}

// Game APIs
export async function startGame(roomId: string, hostId: string): Promise<Game> {
  return apiRequest<Game>('POST', '/api/games/start', { room_id: roomId, host_id: hostId });
}

export async function getGame(gameId: string): Promise<Game> {
  return apiRequest<Game>('GET', `/api/games/${gameId}`);
}

export async function submitDescription(gameId: string, playerId: string, description: string): Promise<Game> {
  return apiRequest<Game>('POST', `/api/games/${gameId}/describe`, { player_id: playerId, description });
}

export async function submitVote(gameId: string, playerId: string, targetId: string): Promise<Game> {
  return apiRequest<Game>('POST', `/api/games/${gameId}/vote`, { player_id: playerId, target_id: targetId });
}

// Leaderboard
export async function getLeaderboard(): Promise<LeaderboardEntry[]> {
  return apiRequest<LeaderboardEntry[]>('GET', '/api/leaderboard/');
}
