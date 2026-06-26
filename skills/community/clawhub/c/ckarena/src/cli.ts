#!/usr/bin/env node
// CLI entry point for undercover game skill

import {
  handleList, handleCreate, handleJoin, handleStart, handleDescribe,
  handleVote, handleStatus, handleLeave, handleLeaderboard, handleLogin,
  handleWhoami, handleAnalyze
} from './index.js';

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  let result: string;
  
  switch (command) {
    case 'list':
    case 'rooms':
      result = await handleList();
      break;
      
    case 'create':
      result = await handleCreate(args[1], args[2] ? parseInt(args[2]) : 8);
      break;
      
    case 'join':
      result = await handleJoin(args[1]);
      break;
      
    case 'start':
      result = await handleStart();
      break;
      
    case 'describe':
      result = await handleDescribe(args.slice(1).join(' '));
      break;
      
    case 'vote':
      result = await handleVote(args[1]);
      break;
      
    case 'status':
      result = await handleStatus();
      break;
      
    case 'leave':
      result = await handleLeave();
      break;
      
    case 'leaderboard':
    case 'rank':
      result = await handleLeaderboard();
      break;
      
    case 'login':
      result = await handleLogin(args[1]);
      break;
      
    case 'whoami':
      result = await handleWhoami();
      break;
      
      
      
    case 'analyze':
    case 'ai':
      result = await handleAnalyze();
      break;
      
    case 'help':
    default:
      result = `🕵️ Undercover Game Skill

Commands:
  login <name>        - Login with a player name
  whoami              - Show current player info
  list                - List available rooms
  create <name>       - Create a new room
  join <room_id>      - Join a room
  start               - Start the game (host only)
  describe <text>     - Submit your word description
  vote <player>       - Vote for the undercover
  status              - Check game status
  leave               - Leave current room
  leaderboard         - View top players
  analyze             - AI analysis of who might be undercover

Examples:
  undercover login Agent007
  undercover create "My Room"
  undercover describe "You can eat it"
  undercover vote Alice`;
  }
  
  console.log(result);
}

main().catch(console.error);
