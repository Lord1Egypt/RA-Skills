// WebSocket client for real-time game updates

import { setCurrentRoom, setCurrentGame, getPlayer, getCurrentRoom } from './state.js';
import { getRoom, getGame } from './api.js';

let ws: WebSocket | null = null;
let reconnectInterval: ReturnType<typeof setInterval> | null = null;

export function connectWebSocket(clientId: string): void {
  if (ws?.readyState === WebSocket.OPEN) return;
  
  const wsUrl = `ws://43.134.60.58:8000/ws/${clientId}`;
  ws = new WebSocket(wsUrl);
  
  ws.onopen = () => {
    console.log('Undercover: WebSocket connected');
    if (reconnectInterval) {
      clearInterval(reconnectInterval);
      reconnectInterval = null;
    }
  };
  
  ws.onclose = () => {
    console.log('Undercover: WebSocket disconnected');
    // Attempt reconnection
    if (!reconnectInterval) {
      reconnectInterval = setInterval(() => {
        const player = getPlayer();
        if (player) connectWebSocket(player.id);
      }, 5000);
    }
  };
  
  ws.onerror = (error) => {
    console.error('Undercover: WebSocket error:', error);
  };
  
  ws.onmessage = async (event) => {
    try {
      const message = JSON.parse(event.data as string);
      await handleMessage(message);
    } catch (e) {
      console.error('Undercover: Failed to parse message:', e);
    }
  };
}

export function disconnectWebSocket(): void {
  if (reconnectInterval) {
    clearInterval(reconnectInterval);
    reconnectInterval = null;
  }
  if (ws) {
    ws.close();
    ws = null;
  }
}

async function handleMessage(message: { type: string; data: unknown }): Promise<void> {
  const room = getCurrentRoom();
  if (!room) return;
  
  switch (message.type) {
    case 'room_update':
    case 'player_joined':
    case 'player_left':
      try {
        const updatedRoom = await getRoom(room.id);
        setCurrentRoom(updatedRoom);
      } catch (e) {
        console.error('Failed to refresh room:', e);
      }
      break;
      
    case 'game_started':
    case 'game_update':
    case 'description_submitted':
    case 'vote_submitted':
    case 'player_eliminated':
      try {
        const updatedRoom = await getRoom(room.id);
        setCurrentRoom(updatedRoom);
        if (updatedRoom.game_id) {
          const game = await getGame(updatedRoom.game_id);
          setCurrentGame(game);
        }
      } catch (e) {
        console.error('Failed to refresh game:', e);
      }
      break;
      
    case 'game_ended':
      try {
        const updatedRoom = await getRoom(room.id);
        setCurrentRoom(updatedRoom);
        if (updatedRoom.game_id) {
          const game = await getGame(updatedRoom.game_id);
          setCurrentGame(game);
          // Announce winner
          if (game.winner) {
            console.log(`🎉 Game ended! Winner: ${game.winner}`);
          }
        }
      } catch (e) {
        console.error('Failed to get final game state:', e);
      }
      break;
  }
}

export function isConnected(): boolean {
  return ws?.readyState === WebSocket.OPEN;
}
