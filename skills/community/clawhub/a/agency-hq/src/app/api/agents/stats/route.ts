import { NextResponse } from 'next/server';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import { SystemStats } from '@/lib/agents';
import { isDemoMode, getDemoStats } from '@/lib/demo-data';

function getUptime(): string {
  try {
    const uptime = execSync('uptime -p', { encoding: 'utf-8', timeout: 3000 }).trim();
    return uptime.replace('up ', '');
  } catch {
    return 'unknown';
  }
}

function getCpuLoad(): number {
  try {
    const load = execSync("cat /proc/loadavg | awk '{print $1}'", { encoding: 'utf-8', timeout: 3000 }).trim();
    return parseFloat(load);
  } catch {
    return 0;
  }
}

function getRam(): { used: number; total: number } {
  try {
    const info = execSync("free -m | awk 'NR==2{print $2,$3}'", { encoding: 'utf-8', timeout: 3000 }).trim();
    const [total, used] = info.split(' ').map(Number);
    return { total, used };
  } catch {
    return { total: 0, used: 0 };
  }
}

function getDisk(): { used: number; total: number } {
  try {
    const info = execSync("df -BG / | awk 'NR==2{print $2,$3}'", { encoding: 'utf-8', timeout: 3000 }).trim();
    const parts = info.split(/\s+/).map(s => parseInt(s));
    return { total: parts[0], used: parts[1] };
  } catch {
    return { total: 0, used: 0 };
  }
}

function getSessionsToday(): number {
  try {
    const home = process.env.HOME || '/home/user';
    const openclawHome = process.env.OPENCLAW_HOME || path.join(home, '.openclaw');
    const agentsDir = path.join(openclawHome, 'agents');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    let count = 0;

    const agents = fs.readdirSync(agentsDir);
    for (const agent of agents) {
      const sessionsDir = path.join(agentsDir, agent, 'sessions');
      if (!fs.existsSync(sessionsDir)) continue;
      const files = fs.readdirSync(sessionsDir).filter(f => f.endsWith('.jsonl'));
      for (const file of files) {
        const stat = fs.statSync(path.join(sessionsDir, file));
        if (stat.mtime >= today) count++;
      }
    }
    return count;
  } catch {
    return 0;
  }
}

export async function GET() {
  try {
    // Demo mode: return sample data
    if (isDemoMode()) {
      return NextResponse.json(getDemoStats());
    }

    const ram = getRam();
    const disk = getDisk();

    const stats: SystemStats = {
      cpuLoad: getCpuLoad(),
      ramUsed: ram.used,
      ramTotal: ram.total,
      diskUsed: disk.used,
      diskTotal: disk.total,
      activeAgents: 0,
      sessionsToday: getSessionsToday(),
      uptime: getUptime(),
    };

    return NextResponse.json(stats);
  } catch (err) {
    console.error('[api/agents/stats]', err);
    return NextResponse.json({ error: 'Failed to fetch stats' }, { status: 500 });
  }
}
