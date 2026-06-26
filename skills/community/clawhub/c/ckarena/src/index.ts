// Undercover Game Skill - Main Entry Point

import {
  createPlayer, getPlayer, listRooms, createRoom, joinRoom, leaveRoom,
  getRoom, startGame, getGame, submitDescription, submitVote, getLeaderboard
} from './api.js';
import {
  joinArena, leaveArena, getArenaStatus, getMyGame, getArenaLeaderboard
} from './arena-api.js';
import {
  setPlayer, getPlayer as getCurrentPlayer, setCurrentRoom, getCurrentRoom,
  setCurrentGame, getCurrentGame, isInRoom, isInGame, isHost, getMyWord,
  getPlayerNameById, getPlayerIdByName
} from './state.js';
import { connectWebSocket, disconnectWebSocket } from './websocket.js';
import { generateDescription, analyzeUndercover, decideVote } from './ai.js';
import { startAutoPlay, stopPolling, getPollStatus } from './poll.js';

// Command handlers
export async function handleList(): Promise<string> {
  try {
    const rooms = await listRooms();
    if (rooms.length === 0) {
      return '🎮 No rooms available. Create one with `@undercover create <name>`!';
    }
    
    const lines = rooms.map(r => {
      const status = r.status === 'waiting' ? '⏳' : r.status === 'playing' ? '🔥' : '✅';
      return `${status} **${r.name}** (${r.players.length}/${r.max_players}) - Host: ${r.host_name} - ID: \`${r.id}\``;
    });
    
    return '🎮 **Available Rooms**\n\n' + lines.join('\n');
  } catch (e) {
    return `❌ Failed to list rooms: ${(e as Error).message}`;
  }
}

export async function handleCreate(name: string, maxPlayers = 8): Promise<string> {
  if (!name) return '❌ Room name is required. Usage: `@undercover create MyRoom`';
  
  const player = getCurrentPlayer();
  if (!player) return '❌ Please login first with `@undercover login <name>`';
  
  try {
    const room = await createRoom(name, player.id, maxPlayers);
    setCurrentRoom(room);
    connectWebSocket(player.id);
    return `✅ Room **${room.name}** created!\n📋 Room ID: \`${room.id}\`\n👥 Capacity: ${room.max_players}\n\nInvite others with: \`@undercover join ${room.id}\``;
  } catch (e) {
    return `❌ Failed to create room: ${(e as Error).message}`;
  }
}

export async function handleJoin(roomId: string): Promise<string> {
  if (!roomId) return '❌ Room ID is required. Usage: `@undercover join <id>`';
  
  const player = getCurrentPlayer();
  if (!player) return '❌ Please login first with `@undercover login <name>`';
  
  try {
    const room = await joinRoom(roomId, player.id);
    setCurrentRoom(room);
    connectWebSocket(player.id);
    
    const players = room.player_names.join(', ');
    return `✅ Joined room **${room.name}**!\n👑 Host: ${room.host_name}\n👥 Players: ${players}\n\n${isHost() ? 'You can start the game when 3+ players join.' : 'Wait for the host to start the game.'}`;
  } catch (e) {
    return `❌ Failed to join room: ${(e as Error).message}`;
  }
}

export async function handleStart(): Promise<string> {
  const player = getCurrentPlayer();
  const room = getCurrentRoom();
  
  if (!player) return '❌ Please login first';
  if (!room) return '❌ You are not in a room. Join one first.';
  if (room.host_id !== player.id) return '❌ Only the host can start the game.';
  if (room.players.length < 3) return '❌ Need at least 3 players to start.';
  
  try {
    const game = await startGame(room.id, player.id);
    setCurrentGame(game);
    
    const myWord = getMyWord();
    return `🔥 **Game Started!**\n\n🎯 Your word is: **${myWord}**\n📝 Describe it without saying the word directly!\n\nUse \`@undercover describe <your description>\` when it's your turn.`;
  } catch (e) {
    return `❌ Failed to start game: ${(e as Error).message}`;
  }
}

export async function handleDescribe(description: string): Promise<string> {
  if (!description) return '❌ Description is required. Usage: `@undercover describe <description>`';
  
  const player = getCurrentPlayer();
  const room = getCurrentRoom();
  const game = getCurrentGame();
  
  if (!player) return '❌ Please login first';
  if (!room) return '❌ You are not in a room';
  if (!game) return '❌ No active game. Start one first.';
  if (game.status !== 'describing') return '⏳ Not the description phase yet.';
  
  // Check if it's player's turn
  const currentPlayerId = room.players[game.current_player_idx];
  if (currentPlayerId !== player.id) {
    const currentName = getPlayerNameById(currentPlayerId);
    return `⏳ It's ${currentName}'s turn to describe. Please wait.`;
  }
  
  try {
    const updatedGame = await submitDescription(game.id, player.id, description);
    setCurrentGame(updatedGame);
    return `✅ Description submitted!`;
  } catch (e) {
    return `❌ Failed to submit description: ${(e as Error).message}`;
  }
}

export async function handleVote(targetName: string): Promise<string> {
  if (!targetName) return '❌ Player name is required. Usage: `@undercover vote <player_name>`';
  
  const player = getCurrentPlayer();
  const room = getCurrentRoom();
  const game = getCurrentGame();
  
  if (!player) return '❌ Please login first';
  if (!room) return '❌ You are not in a room';
  if (!game) return '❌ No active game';
  if (game.status !== 'voting') return '⏳ Not the voting phase yet.';
  
  const targetId = getPlayerIdByName(targetName);
  if (!targetId) return `❌ Player "${targetName}" not found in this room.`;
  if (targetId === player.id) return '❌ You cannot vote for yourself.';
  if (game.eliminated_players?.includes(targetId)) return `❌ ${targetName} has already been eliminated.`;
  
  try {
    const updatedGame = await submitVote(game.id, player.id, targetId);
    setCurrentGame(updatedGame);
    return `🗳️ You voted for **${targetName}**`;
  } catch (e) {
    return `❌ Failed to vote: ${(e as Error).message}`;
  }
}

export async function handleStatus(): Promise<string> {
  const room = getCurrentRoom();
  const game = getCurrentGame();
  const player = getCurrentPlayer();
  
  if (!room) return '❌ You are not in a room. Use `@undercover list` to find rooms.';
  
  let status = `📍 **Room: ${room.name}**\n`;
  status += `👑 Host: ${room.host_name}\n`;
  status += `👥 Players (${room.players.length}/${room.max_players}): ${room.player_names.join(', ')}\n`;
  status += `📊 Status: ${room.status.toUpperCase()}\n`;
  
  if (game) {
    status += `\n🎮 **Game Status**\n`;
    status += `Round: ${game.current_round + 1}/${game.max_rounds}\n`;
    status += `Phase: ${game.status.toUpperCase()}\n`;
    
    if (player) {
      const myWord = getMyWord();
      if (myWord) status += `🎯 Your word: **${myWord}**\n`;
    }
    
    if (Object.keys(game.descriptions).length > 0) {
      status += `\n📝 **Descriptions**\n`;
      for (const [pid, desc] of Object.entries(game.descriptions)) {
        const name = getPlayerNameById(pid);
        status += `- ${name}: "${desc}"\n`;
      }
    }
    
    if (game.eliminated_players?.length > 0) {
      status += `\n❌ Eliminated: ${game.eliminated_players.map(getPlayerNameById).join(', ')}\n`;
    }
    
    if (game.winner) {
      status += `\n🏆 Winner: **${game.winner}**`;
    }
  }
  
  return status;
}

export async function handleLeave(): Promise<string> {
  const player = getCurrentPlayer();
  const room = getCurrentRoom();
  
  if (!player) return '❌ Not logged in';
  if (!room) return '❌ Not in a room';
  
  try {
    await leaveRoom(room.id, player.id);
    disconnectWebSocket();
    setCurrentRoom(null);
    setCurrentGame(null);
    return `👋 Left room **${room.name}**`;
  } catch (e) {
    return `❌ Failed to leave: ${(e as Error).message}`;
  }
}

export async function handleLeaderboard(): Promise<string> {
  try {
    const entries = await getLeaderboard();
    if (entries.length === 0) return '🏆 No games played yet. Be the first!';
    
    const medals = ['🥇', '🥈', '🥉'];
    const lines = entries.slice(0, 10).map((e, i) => {
      const medal = medals[i] || `${i + 1}.`;
      return `${medal} **${e.player_name}** - ${e.wins} wins / ${e.games_played} games (${(e.win_rate * 100).toFixed(1)}%)`;
    });
    
    return '🏆 **Leaderboard**\n\n' + lines.join('\n');
  } catch (e) {
    return `❌ Failed to get leaderboard: ${(e as Error).message}`;
  }
}

export async function handleLogin(name: string): Promise<string> {
  if (!name) return '❌ Name is required. Usage: `@undercover login <name>`';
  
  try {
    const player = await createPlayer(name);
    setPlayer(player);
    return `✅ Logged in as **${player.name}**\nUse \`@undercover list\` to find rooms!`;
  } catch (e) {
    return `❌ Login failed: ${(e as Error).message}`;
  }
}

export async function handleWhoami(): Promise<string> {
  const player = getCurrentPlayer();
  if (!player) return '❌ Not logged in. Use `@undercover login <name>`';
  return `👤 **${player.name}**\n🏆 Wins: ${player.wins}\n🎮 Games: ${player.games_played}`;
}


// AI Analysis function
export async function handleAnalyze(): Promise<string> {
  const game = getCurrentGame();
  const room = getCurrentRoom();
  
  if (!game || !room) return '❌ No active game to analyze';
  
  const analysis = analyzeUndercover(game, room);
  const suspectName = getPlayerNameById(analysis.suspectId);
  
  return `🕵️ **AI Analysis**

**Most Suspicious:** ${suspectName}
**Confidence:** ${(analysis.confidence * 100).toFixed(0)}%
**Reason:** ${analysis.reason}`;
}


// Auto-play and poll functions
export { startAutoPlay, stopPolling, getPollStatus } from "./poll.js";
