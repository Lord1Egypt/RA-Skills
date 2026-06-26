// State management for undercover game session

import { Player, Room, Game } from './api.js';

interface GameState {
  player: Player | null;
  currentRoom: Room | null;
  currentGame: Game | null;
}

const state: GameState = {
  player: null,
  currentRoom: null,
  currentGame: null,
};

export function setPlayer(player: Player | null): void {
  state.player = player;
}

export function getPlayer(): Player | null {
  return state.player;
}

export function setCurrentRoom(room: Room | null): void {
  state.currentRoom = room;
}

export function getCurrentRoom(): Room | null {
  return state.currentRoom;
}

export function setCurrentGame(game: Game | null): void {
  state.currentGame = game;
}

export function getCurrentGame(): Game | null {
  return state.currentGame;
}

export function isInRoom(): boolean {
  return state.currentRoom !== null;
}

export function isInGame(): boolean {
  return state.currentGame !== null;
}

export function isHost(): boolean {
  return state.player !== null && state.currentRoom?.host_id === state.player.id;
}

export function getMyWord(): string | null {
  if (!state.player || !state.currentGame) return null;
  return state.currentGame.words[state.player.id] || null;
}

export function getPlayerNameById(playerId: string): string {
  if (!state.currentRoom) return playerId;
  const idx = state.currentRoom.players.indexOf(playerId);
  return state.currentRoom.player_names[idx] || playerId;
}

export function getPlayerIdByName(name: string): string | null {
  if (!state.currentRoom) return null;
  const idx = state.currentRoom.player_names.findIndex(n => n.toLowerCase() === name.toLowerCase());
  return idx >= 0 ? state.currentRoom.players[idx] : null;
}
