/**
 * Demo data for when running on Vercel or without OpenClaw.
 * Returns realistic-looking agent statuses and activity feed.
 */

import { AGENTS, AgentState, ActivityItem, SystemStats, AgentStatus, RoomId } from './agents';

// Deterministic but varied statuses for demo mode
// Demo scenario: "Build a landing page for a dog accessories brand"
// Shows agents in different rooms working on a realistic mission
const DEMO_STATUSES: { status: AgentStatus; room: RoomId; idleMinutes: number; task: string | null }[] = [
  // Spock — coordinating from meeting room, briefing the team
  { status: 'active', room: 'meeting_room', idleMinutes: 0, task: 'Briefing team: "Build a landing page for a pet accessories brand"' },
  // Scotty — at his desk, building the site
  { status: 'active', room: 'main_office', idleMinutes: 0, task: 'Scaffolding Next.js 15 landing page — hero section + product grid' },
  // Gordon — at trading terminal, scanning markets between tasks
  { status: 'active', room: 'main_office', idleMinutes: 0, task: 'Scanning 301 prediction markets — NBA + CS2 + politics' },
  // Watson — in meeting room with Spock, presenting research
  { status: 'active', room: 'meeting_room', idleMinutes: 0, task: 'Presenting competitor analysis: 3 competitors found, market gaps identified' },
  // Nova — at design desk, creating the visual spec
  { status: 'active', room: 'main_office', idleMinutes: 0, task: 'Designing hero mockup — warm tones, dog photos, Sunshine Coast vibe' },
  // Cipher — in server room, auditing the deploy
  { status: 'active', room: 'server_room', idleMinutes: 0, task: 'Pre-deploy audit: checking dependencies + XSS vectors' },
  // Oscar — at content desk, writing copy
  { status: 'active', room: 'main_office', idleMinutes: 0, task: 'Writing hero headline: "Let their true personality shine" — v3 draft' },
  // Rex — in meeting room, planning the growth strategy
  { status: 'active', room: 'meeting_room', idleMinutes: 0, task: 'SEO keyword map: "dog necklace australia" + Etsy listing optimization' },
  // Rook — in server room with Cipher, checking infrastructure
  { status: 'active', room: 'server_room', idleMinutes: 0, task: 'Configuring Vercel deploy + checking Shopify API integration' },
  // Atlas — at PM desk, tracking progress
  { status: 'idle', room: 'kitchen', idleMinutes: 8, task: 'Sprint board updated — 4/7 tasks done, on track for 30-min deadline' },
  // Ledger — on a break, finished cost analysis
  { status: 'idle', room: 'game_room', idleMinutes: 15, task: 'Completed cost analysis: $0 infra cost, Shopify + Vercel free tiers' },
];

function getRelativeTime(minutes: number): string {
  if (minutes === 0) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function getDemoAgentStates(): AgentState[] {
  return AGENTS.map((agent, i) => {
    const demo = DEMO_STATUSES[i % DEMO_STATUSES.length];
    const lastActiveDate = new Date(Date.now() - demo.idleMinutes * 60000);

    return {
      id: agent.id,
      name: agent.name,
      emoji: agent.emoji,
      role: agent.role,
      model: agent.model,
      color: agent.color,
      desk: agent.desk,
      accessory: agent.accessory,
      status: demo.status,
      lastActive: lastActiveDate.toISOString(),
      lastActiveRelative: getRelativeTime(demo.idleMinutes),
      currentTask: demo.task,
      idleMinutes: demo.idleMinutes,
      room: demo.room,
    };
  });
}

const DEMO_ACTIVITIES: { agentIndex: number; message: string; type: ActivityItem['type']; minutesAgo: number }[] = [
  { agentIndex: 0, message: 'Assigned 3 new tasks to Scotty and Nova from the backlog', type: 'regular', minutesAgo: 2 },
  { agentIndex: 1, message: 'Deployed The Agency v1.2 to production 🚀', type: 'deploy', minutesAgo: 5 },
  { agentIndex: 5, message: '🛡️ Security scan complete — no vulnerabilities found', type: 'security', minutesAgo: 8 },
  { agentIndex: 4, message: 'Finished hero section redesign with new animations', type: 'task_complete', minutesAgo: 12 },
  { agentIndex: 2, message: 'BTC broke $95k resistance — watching for confirmation', type: 'regular', minutesAgo: 15 },
  { agentIndex: 8, message: 'Hotfix deployed: fixed WebSocket reconnection bug', type: 'deploy', minutesAgo: 18 },
  { agentIndex: 3, message: 'Research report: Top 10 AI agent frameworks compared', type: 'task_complete', minutesAgo: 22 },
  { agentIndex: 9, message: 'Sprint velocity up 15% — team is shipping faster', type: 'regular', minutesAgo: 30 },
  { agentIndex: 6, message: 'Published blog post: "How We Built The Agency"', type: 'task_complete', minutesAgo: 35 },
  { agentIndex: 1, message: 'Using tool: exec — running npm run build', type: 'scanning', minutesAgo: 40 },
  { agentIndex: 5, message: '⚠️ Unusual SSH login attempt from unknown IP blocked', type: 'alert', minutesAgo: 45 },
  { agentIndex: 0, message: 'Code review complete on PR #42 — approved with comments', type: 'task_complete', minutesAgo: 50 },
  { agentIndex: 4, message: 'Generated 5 color palette variations for dark mode', type: 'regular', minutesAgo: 55 },
  { agentIndex: 8, message: 'Database migration applied — added indexes for performance', type: 'deploy', minutesAgo: 65 },
  { agentIndex: 7, message: 'MRR growth tracking dashboard updated for Q1', type: 'regular', minutesAgo: 80 },
];

export function getDemoActivities(): ActivityItem[] {
  return DEMO_ACTIVITIES.map(item => {
    const agent = AGENTS[item.agentIndex];
    return {
      timestamp: new Date(Date.now() - item.minutesAgo * 60000).toISOString(),
      agentId: agent.id,
      agentName: agent.name,
      agentEmoji: agent.emoji,
      agentColor: agent.color,
      message: item.message,
      type: item.type,
    };
  });
}

export function getDemoStats(): SystemStats {
  return {
    cpuLoad: 1.2,
    ramUsed: 6144,
    ramTotal: 16384,
    diskUsed: 45,
    diskTotal: 200,
    activeAgents: DEMO_STATUSES.filter(s => s.status === 'active').length,
    sessionsToday: 23,
    uptime: '14 days, 7 hours',
  };
}

/**
 * Check if we should run in demo mode.
 * Demo mode is active when:
 * 1. ARENA_MODE=demo is explicitly set, OR
 * 2. Running on Vercel (process.env.VERCEL is set) AND ARENA_MODE is not 'live'
 */
export function isDemoMode(): boolean {
  if (process.env.ARENA_MODE === 'demo') return true;
  if (process.env.ARENA_MODE === 'live') return false;
  if (process.env.VERCEL) return true;
  return false;
}
