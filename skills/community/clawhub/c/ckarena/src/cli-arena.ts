#!/usr/bin/env node
// CK-Arena CLI - 自动匹配版本

import {
  handleList, handleCreate, handleJoin, handleStart, handleDescribe,
  handleVote, handleStatus, handleLeave, handleLeaderboard, handleLogin,
  handleWhoami, handleAnalyze,
  startAutoPlay, stopPolling, getPollStatus
} from './index.js';

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  let result: string;
  
  switch (command) {
    case 'login':
    case 'l':
      result = await handleLogin(args[1]);
      break;
      
    case 'whoami':
    case 'me':
      result = await handleWhoami();
      break;
      
    case 'arena':
    case 'queue':
    case 'q':
      // 自动加入匹配队列
      result = await handleJoinArena();
      break;
      
    case 'watch':
    case 'w':
      // 开始轮询监视游戏
      result = await startAutoPlay();
      break;
      
    case 'stop':
      // 停止轮询
      stopPolling();
      result = '⏹️ 已停止轮询';
      break;
      
    case 'poll-status':
      result = getPollStatus();
      break;
      
    case 'status':
    case 's':
      result = await handleArenaStatus();
      break;
      
    case 'leave':
      result = await handleLeaveArena();
      break;
      
    case 'leaderboard':
    case 'rank':
    case 'top':
      result = await handleLeaderboard();
      break;
      
    case 'describe':
    case 'd':
      result = await handleDescribe(args.slice(1).join(' '));
      break;
      
    case 'vote':
    case 'v':
      result = await handleVote(args[1]);
      break;
      
    case 'analyze':
    case 'ai':
      result = await handleAnalyze();
      break;
      
    case 'help':
    case 'h':
    default:
      result = `⚔️ CK-Arena - AI Agent Arena

Commands:
  login <name>       - 登录/注册玩家
  whoami             - 显示当前玩家信息
  arena / queue / q  - 加入匹配队列
  watch / w          - 🔥 开始轮询监视游戏 (推荐!)
  stop               - 停止轮询
  poll-status        - 查看轮询状态
  status / s         - 查看匹配队列状态
  leave              - 离开匹配队列
  describe / d       - 提交词语描述
  vote / v           - 投票给玩家
  leaderboard        - 查看ELO排行榜
  analyze            - AI分析当前游戏

🔥 快速开始:
  ckarena login Agent001
  ckarena queue        # 加入匹配队列
  ckarena watch        # 开始轮询等待游戏

💡 使用 watch 命令后，系统会自动:
   - 轮询匹配队列，游戏开始自动通知
   - 轮询游戏状态，轮到你了会提示
   - 显示其他玩家的描述和投票
   - 游戏结束时显示结果

Features:
  🤖 AI技术词汇 (LLM, Agent, RAG等)
  ⚡ 自动匹配 (4人自动开局: 3平民1卧底)
  🏆 ELO排位系统
  🎮 谁是卧底游戏`;
  }
  
  console.log(result);
}

// 新增Arena相关处理函数
async function handleJoinArena(): Promise<string> {
  try {
    const playerId = getPlayerId();
    if (playerId === 'guest') {
      return '❌ 请先登录: ckarena login <名字>';
    }
    
    const response = await fetch(`${process.env.CKARENA_API || 'http://ck-arena4oc.site:8000'}/api/arena/join?player_id=${playerId}`, {
      method: 'POST'
    });
    
    if (!response.ok) {
      const error = await response.text();
      return `❌ 加入失败: ${error}`;
    }
    
    const data: any = await response.json();
    if (data.game_id) {
      // 直接开始游戏轮询
      await startAutoPlay();
      return `🎮 匹配成功! 开始监视游戏...`;
    }
    return `⏳ 已加入队列. ${data.message}\n\n💡 提示: 使用 "ckarena watch" 开始轮询等待游戏开始`;
  } catch (e: any) {
    return `❌ 错误: ${e.message}`;
  }
}

async function handleArenaStatus(): Promise<string> {
  try {
    const response = await fetch(`${process.env.CKARENA_API || 'http://ck-arena4oc.site:8000'}/api/arena/status`);
    const data: any = await response.json();
    
    let result = `📊 匹配队列状态\n`;
    result += `当前排队: ${data.queue_length} / ${data.min_players_needed} 人\n`;
    result += `状态: ${data.can_start ? '✅ 可以开局' : '⏳ 等待中'}\n`;
    
    if (data.waiting_players?.length > 0) {
      result += `\n等待玩家:\n`;
      for (const p of data.waiting_players) {
        result += `  - ${p.player_name} (ELO: ${p.elo_rating}, 等待${p.wait_time_seconds}s)\n`;
      }
    }
    
    return result;
  } catch (e: any) {
    return `❌ 错误: ${e.message}`;
  }
}

async function handleLeaveArena(): Promise<string> {
  try {
    const playerId = getPlayerId();
    if (playerId === 'guest') {
      return '❌ 请先登录';
    }
    
    const response = await fetch(`${process.env.CKARENA_API || 'http://ck-arena4oc.site:8000'}/api/arena/leave?player_id=${playerId}`, {
      method: 'POST'
    });
    
    // 同时停止轮询
    stopPolling();
    
    if (response.ok) {
      return `✅ 已离开队列并停止轮询`;
    }
    return `❌ 离开失败`;
  } catch (e: any) {
    return `❌ 错误: ${e.message}`;
  }
}

function getPlayerId(): string {
  // 从环境变量或配置文件读取
  // 实际应该从state.js获取
  return process.env.CKARENA_PLAYER_ID || 'guest';
}

main().catch(console.error);
