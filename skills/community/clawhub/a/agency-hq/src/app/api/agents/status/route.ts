import { NextResponse } from 'next/server';
import { AGENTS, AgentState, AgentStatus, getAgentRoom } from '@/lib/agents';
import { isDemoMode, getDemoAgentStates } from '@/lib/demo-data';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

function getRelativeTime(date: Date): string {
  const now = Date.now();
  const diff = now - date.getTime();
  const seconds = Math.floor(diff / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function getNewestFile(dir: string): { path: string; mtime: Date } | null {
  try {
    if (!fs.existsSync(dir)) return null;
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.jsonl'));
    if (files.length === 0) return null;

    let newest: { path: string; mtime: Date } | null = null;
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      if (!newest || stat.mtime > newest.mtime) {
        newest = { path: filePath, mtime: stat.mtime };
      }
    }
    return newest;
  } catch {
    return null;
  }
}

function getLastTaskFromFile(filePath: string): string | null {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.trim().split('\n');
    const recent = lines.slice(-30);
    for (let i = recent.length - 1; i >= 0; i--) {
      try {
        const entry = JSON.parse(recent[i]);
        if (entry.role === 'assistant' && typeof entry.content === 'string' && entry.content.length > 10) {
          const text = entry.content.substring(0, 80).replace(/\n/g, ' ');
          return text;
        }
        if (entry.role === 'assistant' && entry.tool_calls) {
          const toolName = entry.tool_calls[0]?.function?.name;
          if (toolName) return `Using ${toolName}...`;
        }
      } catch {
        continue;
      }
    }
    return null;
  } catch {
    return null;
  }
}

function isAgentRunning(agentId: string): boolean {
  try {
    const result = execSync(`ps aux | grep -i "agent.*${agentId}" | grep -v grep | head -1`, { encoding: 'utf-8', timeout: 3000 });
    return result.trim().length > 0;
  } catch {
    return false;
  }
}

// Track which agents were recently active together for meeting detection
function detectMeetings(states: AgentState[]): void {
  const recentlyActive = states.filter(a => a.status === 'active');
  if (recentlyActive.length >= 2) {
    for (const agent of recentlyActive) {
      agent.room = 'meeting_room';
    }
  }
}

export async function GET() {
  try {
    // Demo mode: return sample data
    if (isDemoMode()) {
      return NextResponse.json({
        agents: getDemoAgentStates(),
        timestamp: new Date().toISOString(),
        mode: 'demo',
      });
    }

    const openclawHome = process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/home/user', '.openclaw');
    const agentsHome = path.join(openclawHome, 'agents');

    const states: AgentState[] = AGENTS.map(agent => {
      const sessionsDir = path.join(agentsHome, agent.id, 'sessions');
      const newest = getNewestFile(sessionsDir);
      const running = isAgentRunning(agent.id);

      let status: AgentStatus = 'offline';
      let lastActiveRelative = 'unknown';
      let currentTask: string | null = null;
      let idleMinutes = 999;

      if (newest) {
        const diffMs = Date.now() - newest.mtime.getTime();
        const diffMin = diffMs / 60000;
        idleMinutes = Math.floor(diffMin);

        if (running || diffMin < 5) {
          status = 'active';
          idleMinutes = 0;
        } else if (diffMin < 60) {
          status = 'idle';
        } else {
          status = 'offline';
        }

        lastActiveRelative = getRelativeTime(newest.mtime);

        if (status === 'active' || status === 'idle') {
          currentTask = getLastTaskFromFile(newest.path);
        }
      }

      const room = getAgentRoom({ status, idleMinutes });

      return {
        id: agent.id,
        name: agent.name,
        emoji: agent.emoji,
        role: agent.role,
        model: agent.model,
        color: agent.color,
        desk: agent.desk,
        accessory: agent.accessory,
        status,
        lastActive: newest?.mtime.toISOString() || null,
        lastActiveRelative,
        currentTask,
        idleMinutes,
        room,
      };
    });

    detectMeetings(states);

    return NextResponse.json({ agents: states, timestamp: new Date().toISOString(), mode: 'live' });
  } catch (err) {
    console.error('[api/agents/status]', err);
    return NextResponse.json({ error: 'Failed to fetch agent status' }, { status: 500 });
  }
}
