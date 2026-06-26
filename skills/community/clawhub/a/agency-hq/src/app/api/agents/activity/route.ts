import { NextResponse } from 'next/server';
import { AGENTS, ActivityItem, ActivityType } from '@/lib/agents';
import { isDemoMode, getDemoActivities } from '@/lib/demo-data';
import * as fs from 'fs';
import * as path from 'path';

function classifyMessage(message: string, toolName?: string): ActivityType {
  const lower = message.toLowerCase();
  if (toolName === 'exec' && (lower.includes('deploy') || lower.includes('push') || lower.includes('ship'))) return 'deploy';
  if (lower.includes('deploy') || lower.includes('shipped') || lower.includes('pushed to') || lower.includes('released')) return 'deploy';
  if (lower.includes('completed') || lower.includes('done') || lower.includes('finished') || lower.includes('✅') || lower.includes('merged')) return 'task_complete';
  if (lower.includes('error') || lower.includes('failed') || lower.includes('⚠') || lower.includes('crash') || lower.includes('alert') || lower.includes('down')) return 'alert';
  if (lower.includes('security') || lower.includes('audit') || lower.includes('vulnerability') || lower.includes('cipher') || lower.includes('🛡')) return 'security';
  if (lower.includes('scan') || lower.includes('checking') || lower.includes('monitoring') || lower.includes('heartbeat') || lower.includes('routine') || lower.includes('cron')) return 'scanning';
  if (toolName && !['exec', 'write', 'edit'].includes(toolName)) return 'scanning';
  return 'regular';
}

let cachedActivities: ActivityItem[] | null = null;
let cacheTime = 0;
const CACHE_TTL = 15000;

function extractActivities(): ActivityItem[] {
  const home = process.env.HOME || '/home/user';
  const openclawHome = process.env.OPENCLAW_HOME || path.join(home, '.openclaw');
  const agentsHome = path.join(openclawHome, 'agents');
  const cronRunsDir = path.join(openclawHome, 'cron', 'runs');
  const activities: ActivityItem[] = [];

  for (const agent of AGENTS) {
    try {
      const sessionsDir = path.join(agentsHome, agent.id, 'sessions');
      if (!fs.existsSync(sessionsDir)) continue;

      const files = fs.readdirSync(sessionsDir)
        .filter(f => f.endsWith('.jsonl'))
        .map(f => ({ name: f, mtime: fs.statSync(path.join(sessionsDir, f)).mtime }))
        .sort((a, b) => b.mtime.getTime() - a.mtime.getTime())
        .slice(0, 3);

      for (const file of files) {
        try {
          const content = fs.readFileSync(path.join(sessionsDir, file.name), 'utf-8');
          const lines = content.trim().split('\n').slice(-50);

          for (const line of lines) {
            try {
              const entry = JSON.parse(line);
              
              if (entry.role === 'user' && typeof entry.content === 'string' && entry.content.length > 15 && entry.content.length < 200) {
                const text = entry.content.replace(/\n/g, ' ').substring(0, 120);
                if (text.startsWith('[') || text.startsWith('Read ') || text.startsWith('HEARTBEAT')) continue;
                activities.push({
                  timestamp: entry.timestamp || file.mtime.toISOString(),
                  agentId: agent.id,
                  agentName: agent.name,
                  agentEmoji: agent.emoji,
                  agentColor: agent.color,
                  message: text,
                  type: classifyMessage(text),
                });
              }

              if (entry.role === 'assistant' && entry.tool_calls && Array.isArray(entry.tool_calls)) {
                for (const tc of entry.tool_calls) {
                  const fn = tc?.function?.name;
                  if (fn && !['read', 'Read'].includes(fn)) {
                    activities.push({
                      timestamp: entry.timestamp || file.mtime.toISOString(),
                      agentId: agent.id,
                      agentName: agent.name,
                      agentEmoji: agent.emoji,
                      agentColor: agent.color,
                      message: `Using tool: ${fn}`,
                      type: classifyMessage(`Using tool: ${fn}`, fn),
                    });
                  }
                }
              }
            } catch {
              continue;
            }
          }
        } catch {
          continue;
        }
      }
    } catch {
      continue;
    }
  }

  try {
    if (fs.existsSync(cronRunsDir)) {
      const cronFiles = fs.readdirSync(cronRunsDir)
        .filter(f => f.endsWith('.jsonl'))
        .map(f => ({ name: f, mtime: fs.statSync(path.join(cronRunsDir, f)).mtime }))
        .sort((a, b) => b.mtime.getTime() - a.mtime.getTime())
        .slice(0, 10);

      for (const file of cronFiles) {
        try {
          const content = fs.readFileSync(path.join(cronRunsDir, file.name), 'utf-8');
          const lines = content.trim().split('\n').slice(0, 5);
          for (const line of lines) {
            try {
              const entry = JSON.parse(line);
              if (entry.role === 'user' && typeof entry.content === 'string') {
                const text = entry.content.replace(/\n/g, ' ').substring(0, 120);
                activities.push({
                  timestamp: file.mtime.toISOString(),
                  agentId: 'cron',
                  agentName: 'Cron',
                  agentEmoji: '⏰',
                  agentColor: '#a78bfa',
                  message: text,
                  type: 'scanning',
                });
              }
            } catch { continue; }
          }
        } catch { continue; }
      }
    }
  } catch { /* ignore */ }

  activities.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  const seen = new Set<string>();
  const unique = activities.filter(a => {
    const key = `${a.agentId}:${a.message.substring(0, 50)}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  return unique.slice(0, 30);
}

export async function GET() {
  try {
    // Demo mode: return sample data
    if (isDemoMode()) {
      return NextResponse.json({
        activities: getDemoActivities(),
        timestamp: new Date().toISOString(),
        mode: 'demo',
      });
    }

    const now = Date.now();
    if (!cachedActivities || now - cacheTime > CACHE_TTL) {
      cachedActivities = extractActivities();
      cacheTime = now;
    }

    return NextResponse.json({ activities: cachedActivities, timestamp: new Date().toISOString(), mode: 'live' });
  } catch (err) {
    console.error('[api/agents/activity]', err);
    return NextResponse.json({ error: 'Failed to fetch activities' }, { status: 500 });
  }
}
