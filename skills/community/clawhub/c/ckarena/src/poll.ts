// Auto-poll daemon for CK-Arena
// Handles queue waiting and game state polling

import { getArenaStatus, getMyGame, getArenaLeaderboard } from './arena-api.js';
import { getGame, submitDescription, submitVote } from './api.js';
import { getPlayer, getCurrentGame, setCurrentGame, getCurrentRoom, setCurrentRoom } from './state.js';

// Helper to get player
function getCurrentPlayer(): any {
  return getPlayer();
}

interface PollState {
  mode: 'queue' | 'game' | 'idle';
  gameId?: string;
  lastPhase?: string;
  lastRound?: number;
  describedInRound?: number;
  votedInRound?: number;
  lastDescriptions?: number;
  lastVotes?: number;
}

let pollInterval: ReturnType<typeof setInterval> | null = null;
let currentState: PollState = { mode: 'idle' };

// Start polling queue status
export function startQueuePolling(): void {
  if (pollInterval) {
    clearInterval(pollInterval);
  }
  
  currentState = { mode: 'queue' };
  console.log('⏳ 开始轮询匹配队列...');
  
  pollInterval = setInterval(async () => {
    await pollQueue();
  }, 3000); // 每3秒检查一次
}

// Start polling game state
export function startGamePolling(gameId: string): void {
  if (pollInterval) {
    clearInterval(pollInterval);
  }
  
  currentState = { 
    mode: 'game', 
    gameId,
    lastPhase: undefined,
    lastRound: 0
  };
  console.log(`🎮 开始轮询游戏 ${gameId}...`);
  
  pollInterval = setInterval(async () => {
    await pollGame();
  }, 3000); // 每3秒检查一次
}

// Stop polling
export function stopPolling(): void {
  if (pollInterval) {
    clearInterval(pollInterval);
    pollInterval = null;
  }
  currentState = { mode: 'idle' };
}

// Poll queue status
async function pollQueue(): Promise<void> {
  const player = getCurrentPlayer();
  if (!player) return;
  
  try {
    // Check if we're in a game now
    const myGame = await getMyGame(player.id);
    
    if (myGame.in_game && myGame.game_id) {
      console.log(`🎮 游戏开始! Game ID: ${myGame.game_id}`);
      
      // Switch to game polling
      startGamePolling(myGame.game_id);
      
      // Fetch initial game state
      const gameState = await getGame(myGame.game_id);
      setCurrentGame(gameState);
      
      // Show game info
      const privateInfo = myGame.game?.private_info;
      if (privateInfo) {
        console.log('\n🎯 ========== 游戏开始 ==========');
        console.log(`📝 你的词语: ${privateInfo.word}`);
        console.log(`🎭 你的身份: ${privateInfo.role === 'undercover' ? '🔴 卧底' : '🟢 平民'}`);
        console.log('================================\n');
      }
      return;
    }
    
    // Still in queue, show status
    const status = await getArenaStatus();
    const myPosition = status.waiting_players.findIndex(p => p.player_id === player.id);
    
    if (myPosition >= 0) {
      process.stdout.write(`\r⏳ 排队中... ${status.queue_length}/${status.min_players_needed} 人 (${myPosition + 1}/${status.queue_length})`);
    }
  } catch (e) {
    // Silent fail, will retry
  }
}

// Poll game state
async function pollGame(): Promise<void> {
  const player = getCurrentPlayer();
  if (!player || !currentState.gameId) return;
  
  try {
    const gameResponse = await getGame(currentState.gameId);
    const gameState = gameResponse as any;
    const publicState = gameState.public_state || gameState;
    const privateInfo = gameState.private_info;
    
    const phase = publicState.phase;
    const round = publicState.current_round;
    const statements = publicState.statements || [];
    const votes = publicState.votes || [];
    const players = publicState.players || [];
    
    // Check for phase change
    if (currentState.lastPhase !== phase) {
      console.log(`\n📢 阶段变化: ${getPhaseName(currentState.lastPhase)} → ${getPhaseName(phase)}`);
      currentState.lastPhase = phase;
      
      if (phase === 'describing') {
        console.log(`\n📝 ========== 第 ${round} 轮描述 ==========`);
        console.log('等待玩家描述词语...\n');
      } else if (phase === 'voting') {
        console.log(`\n🗳️ ========== 投票阶段 ==========`);
        // Show all descriptions for this round
        const roundStatements = statements.filter((s: any) => s.round_number === round);
        console.log('\n📋 本轮描述:');
        roundStatements.forEach((s: any, i: number) => {
          console.log(`  ${i + 1}. ${s.player_name}: "${s.content}"`);
        });
        console.log('\n请投票选出最可疑的人\n');
      } else if (phase === 'ended') {
        handleGameEnd(gameState);
        stopPolling();
        return;
      }
    }
    
    // Check for round change
    if (currentState.lastRound !== round && phase === 'describing') {
      console.log(`\n📝 ========== 第 ${round} 轮描述 ==========`);
      currentState.lastRound = round;
      currentState.describedInRound = undefined;
      currentState.votedInRound = undefined;
    }
    
    // Check if it's my turn to describe
    if (phase === 'describing') {
      const alivePlayers = players.filter((p: any) => p.is_alive);
      const myIndex = alivePlayers.findIndex((p: any) => p.player_id === player.id);
      const currentIdx = publicState.current_player_idx || 0;
      
      // Check if I haven't described this round
      const myStatement = statements.find((s: any) => 
        s.player_id === player.id && s.round_number === round
      );
      
      if (!myStatement && myIndex === currentIdx && currentState.describedInRound !== round) {
        currentState.describedInRound = round;
        console.log('\n🎯 ========== 轮到你了! ==========');
        console.log(`📝 你的词语是: ${privateInfo?.word || '???'}`);
        console.log('💡 请使用: ckarena describe "你的描述"');
        console.log('================================\n');
      }
      
      // Show new descriptions
      const currentStatements = statements.filter((s: any) => s.round_number === round);
      if (currentStatements.length > (currentState.lastDescriptions || 0)) {
        const newStatements = currentStatements.slice(currentState.lastDescriptions || 0);
        newStatements.forEach((s: any) => {
          if (s.player_id !== player.id) {
            console.log(`💬 ${s.player_name}: "${s.content}"`);
          }
        });
        currentState.lastDescriptions = currentStatements.length;
      }
    }
    
    // Check if I need to vote
    if (phase === 'voting') {
      const myVote = votes.find((v: any) => v.voter_id === player.id);
      
      if (!myVote && currentState.votedInRound !== round) {
        currentState.votedInRound = round;
        console.log('\n🎯 ========== 请投票! ==========');
        
        // Show alive players
        const alivePlayers = players.filter((p: any) => p.is_alive && p.player_id !== player.id);
        console.log('👥 可选目标:');
        alivePlayers.forEach((p: any, i: number) => {
          console.log(`  ${i + 1}. ${p.name}`);
        });
        
        console.log('💡 请使用: ckarena vote <玩家名>');
        console.log('   或: ckarena auto-vote (AI自动投票)');
        console.log('================================\n');
      }
      
      // Show new votes
      if (votes.length > (currentState.lastVotes || 0)) {
        const newVotes = votes.slice(currentState.lastVotes || 0);
        newVotes.forEach((v: any) => {
          const voter = players.find((p: any) => p.player_id === v.voter_id);
          const target = players.find((p: any) => p.player_id === v.target_id);
          if (voter && target && voter.player_id !== player.id) {
            console.log(`🗳️ ${voter.name} 投票给 ${target.name}`);
          }
        });
        currentState.lastVotes = votes.length;
      }
    }
    
    // Check for eliminations
    const eliminated = players.filter((p: any) => !p.is_alive && p.eliminated_at_round === round);
    if (eliminated.length > 0 && phase !== 'ended') {
      eliminated.forEach((p: any) => {
        console.log(`\n💀 ${p.name} 被淘汰!`);
        // Note: We don't reveal role here, server doesn't expose it in public state
      });
    }
    
    setCurrentGame(gameState);
  } catch (e) {
    // Silent fail, will retry
  }
}

function getPhaseName(phase?: string): string {
  const names: Record<string, string> = {
    'waiting': '等待中',
    'describing': '描述阶段',
    'voting': '投票阶段',
    'ended': '已结束'
  };
  return names[phase || ''] || phase || '未知';
}

function handleGameEnd(gameState: any): void {
  const publicState = gameState.public_state || gameState;
  const winner = publicState.winner;
  const players = publicState.players || [];
  
  console.log('\n🏁 ========== 游戏结束 ==========');
  
  if (winner) {
    console.log(`🎉 获胜方: ${winner === 'civilian' ? '🟢 平民' : '🔴 卧底'}`);
  }
  
  console.log('\n📊 最终结果:');
  players.forEach((p: any) => {
    const status = p.is_alive ? '✅ 存活' : '💀 淘汰';
    console.log(`  ${p.name}: ${status}`);
  });
  
  console.log('\n💡 使用 ckarena leaderboard 查看排行榜');
  console.log('================================\n');
}

// Get current polling status
export function getPollStatus(): string {
  if (!pollInterval) {
    return '⏹️ 未运行轮询';
  }
  
  if (currentState.mode === 'queue') {
    return '⏳ 正在轮询匹配队列...';
  } else if (currentState.mode === 'game' && currentState.gameId) {
    return `🎮 正在轮询游戏 ${currentState.gameId}...`;
  }
  
  return '🔄 轮询运行中';
}

// Auto-play a complete game
export async function startAutoPlay(): Promise<string> {
  const player = getCurrentPlayer();
  if (!player) {
    return '❌ 请先登录: ckarena login <名字>';
  }
  
  // Check if already in a game
  const myGame = await getMyGame(player.id);
  
  if (myGame.in_game && myGame.game_id) {
    startGamePolling(myGame.game_id);
    return `🎮 继续监视游戏 ${myGame.game_id}...`;
  }
  
  // Check if in queue
  const status = await getArenaStatus();
  const inQueue = status.waiting_players.some((p: any) => p.player_id === player.id);
  
  if (!inQueue) {
    return '❌ 请先加入匹配队列: ckarena queue';
  }
  
  startQueuePolling();
  return '⏳ 开始轮询匹配队列，游戏开始后会自动通知你';
}
