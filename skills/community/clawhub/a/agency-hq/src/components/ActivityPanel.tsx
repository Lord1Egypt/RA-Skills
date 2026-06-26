'use client';

import { useEffect, useRef, useState } from 'react';
import { AgentState, ActivityItem, SystemStats, RoomId, ActivityType } from '@/lib/agents';

interface ActivityPanelProps {
  agents: AgentState[];
  activities: ActivityItem[];
  stats: SystemStats | null;
}

const ROOM_LABELS: Record<RoomId, { emoji: string; name: string }> = {
  main_office: { emoji: '🏢', name: 'Office' },
  meeting_room: { emoji: '🤝', name: 'Meeting' },
  kitchen: { emoji: '☕', name: 'Kitchen' },
  game_room: { emoji: '🎮', name: 'Game' },
  server_room: { emoji: '🖥️', name: 'Server' },
  rest_room: { emoji: '😴', name: 'Rest' },
};

const TYPE_CONFIG: Record<ActivityType, { borderColor: string; icon: string; dimmed?: boolean }> = {
  regular:       { borderColor: 'transparent', icon: '💬' },
  task_complete: { borderColor: '#22c55e', icon: '✅' },
  deploy:        { borderColor: '#3b82f6', icon: '🚀' },
  alert:         { borderColor: '#ef4444', icon: '⚠️' },
  scanning:      { borderColor: 'transparent', icon: '🔄', dimmed: true },
  security:      { borderColor: '#f59e0b', icon: '🛡️' },
  interaction:   { borderColor: '#8b5cf6', icon: '🤝' },
  chat:          { borderColor: '#6366f1', icon: '💬' },
};

function relativeTime(iso: string): string {
  try {
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'now';
    if (mins < 60) return `${mins}m`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h`;
    return `${Math.floor(hrs / 24)}d`;
  } catch { return ''; }
}

function groupByRoom(agents: AgentState[]): Record<RoomId, number> {
  const counts: Record<RoomId, number> = {
    main_office: 0, meeting_room: 0, kitchen: 0, game_room: 0, server_room: 0, rest_room: 0,
  };
  for (const a of agents) {
    if (counts[a.room] !== undefined) counts[a.room]++;
    else counts.main_office++;
  }
  return counts;
}

function CompactMessage({ item }: { item: ActivityItem }) {
  const config = TYPE_CONFIG[item.type] || TYPE_CONFIG.regular;
  const agentColor = item.agentColor || '#9ca3af';
  const hasBorder = config.borderColor !== 'transparent';
  const isChat = item.type === 'chat';

  return (
    <div
      className="flex items-start gap-1.5 py-1 px-2 hover:bg-[#1a1a2e]/60 rounded transition-colors"
      style={{
        borderLeft: hasBorder ? `2px solid ${config.borderColor}` : '2px solid transparent',
        opacity: config.dimmed ? 0.5 : 1,
      }}
    >
      <span className="text-[10px] shrink-0 mt-px">{isChat ? '💬' : item.agentEmoji}</span>
      <div className="flex-1 min-w-0">
        <span className="font-bold text-[10px]" style={{ color: agentColor }}>{item.agentName} </span>
        {isChat ? (
          <span className="text-[11px] text-[#8b8bc0] leading-tight italic">{item.message}</span>
        ) : (
          <span className="text-[11px] text-[#b0b0c0] leading-tight">{item.message}</span>
        )}
      </div>
      <span className="shrink-0 text-[9px] text-[#4b5563] font-mono mt-0.5">{relativeTime(item.timestamp)}</span>
    </div>
  );
}

// ===== "Now" tab — one-line summary per active agent =====
function NowTab({ agents }: { agents: AgentState[] }) {
  const activeAgents = agents.filter(a => a.status === 'active');
  const idleAgents = agents.filter(a => a.status === 'idle');

  return (
    <div className="py-1">
      {activeAgents.length === 0 && idleAgents.length === 0 && (
        <p className="text-[10px] text-[#4b5563] text-center py-6">All agents resting 😴</p>
      )}
      {activeAgents.map(agent => (
        <div key={agent.id} className="flex items-center gap-2 px-3 py-1.5 hover:bg-[#1a1a2e]/60 rounded">
          <span className="text-xs">{agent.emoji}</span>
          <span className="font-bold text-[10px]" style={{ color: agent.color }}>{agent.name}</span>
          <span className="text-[10px] text-[#b0b0c0] truncate flex-1">
            {agent.currentTask ? agent.currentTask : 'working...'}
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0" />
        </div>
      ))}
      {idleAgents.length > 0 && (
        <div className="px-3 pt-2 pb-1">
          <span className="text-[9px] text-[#4b5563] uppercase tracking-wider">Idle</span>
        </div>
      )}
      {idleAgents.map(agent => (
        <div key={agent.id} className="flex items-center gap-2 px-3 py-1 hover:bg-[#1a1a2e]/60 rounded opacity-60">
          <span className="text-xs">{agent.emoji}</span>
          <span className="font-bold text-[10px]" style={{ color: agent.color }}>{agent.name}</span>
          <span className="text-[10px] text-[#6b7280] truncate flex-1">
            {ROOM_LABELS[agent.room]?.emoji} {ROOM_LABELS[agent.room]?.name} · {agent.lastActiveRelative}
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-yellow-500 shrink-0" />
        </div>
      ))}
    </div>
  );
}

// ===== Stats tab — Leaderboard + Mission History =====
function StatsTab({ agents, activities, stats }: { agents: AgentState[]; activities: ActivityItem[]; stats: SystemStats | null }) {
  // Count activities per agent today
  const agentStats = agents.map(agent => {
    const agentActivities = activities.filter(a => a.agentId === agent.id);
    const completions = agentActivities.filter(a => a.type === 'task_complete' || a.type === 'deploy').length;
    return {
      ...agent,
      activityCount: agentActivities.length,
      completions,
    };
  }).sort((a, b) => b.activityCount - a.activityCount);

  const maxActivity = Math.max(...agentStats.map(a => a.activityCount), 1);

  // Recent completed tasks
  const completedTasks = activities
    .filter(a => a.type === 'task_complete' || a.type === 'deploy')
    .slice(-8)
    .reverse();

  return (
    <div className="py-1 overflow-y-auto">
      {/* Leaderboard */}
      <div className="px-3 pb-1">
        <span className="text-[9px] text-[#4b5563] uppercase tracking-wider">🏆 Leaderboard</span>
      </div>
      {agentStats.slice(0, 8).map((agent, i) => (
        <div key={agent.id} className="flex items-center gap-2 px-3 py-1">
          <span className="text-[10px] text-[#4b5563] w-3">{i + 1}</span>
          <span className="text-xs">{agent.emoji}</span>
          <span className="font-bold text-[10px] w-14 truncate" style={{ color: agent.color }}>{agent.name}</span>
          <div className="flex-1 h-2 bg-[#1a1a2e] rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                width: `${(agent.activityCount / maxActivity) * 100}%`,
                backgroundColor: agent.color + 'aa',
              }}
            />
          </div>
          <span className="text-[9px] text-[#6b7280] w-6 text-right">{agent.activityCount}</span>
        </div>
      ))}

      {/* Mission History */}
      {completedTasks.length > 0 && (
        <>
          <div className="px-3 pt-3 pb-1">
            <span className="text-[9px] text-[#4b5563] uppercase tracking-wider">📋 Recent Missions</span>
          </div>
          {completedTasks.map((task, i) => (
            <div key={i} className="px-3 py-1.5 hover:bg-[#1a1a2e]/60 rounded">
              <div className="flex items-center gap-1.5">
                <span className="text-[10px]">{task.agentEmoji}</span>
                <span className="text-[10px] text-[#b0b0c0] truncate flex-1">{task.message}</span>
              </div>
              <div className="flex items-center gap-1 mt-0.5">
                <span className="text-[9px]" style={{ color: task.agentColor }}>{task.agentName}</span>
                <span className="text-[9px] text-[#4b5563]">· {relativeTime(task.timestamp)}</span>
              </div>
            </div>
          ))}
        </>
      )}

      {/* System Stats */}
      {stats && (
        <div className="px-3 pt-3 pb-1">
          <span className="text-[9px] text-[#4b5563] uppercase tracking-wider">⚙️ System</span>
          <div className="grid grid-cols-2 gap-1 mt-1">
            <div className="text-[10px] text-[#6b7280]">Sessions: <span className="text-[#b0b0c0]">{stats.sessionsToday}</span></div>
            <div className="text-[10px] text-[#6b7280]">Active: <span className="text-[#22c55e]">{stats.activeAgents}</span></div>
            <div className="text-[10px] text-[#6b7280]">CPU: <span className="text-[#b0b0c0]">{stats.cpuLoad.toFixed(1)}</span></div>
            <div className="text-[10px] text-[#6b7280]">RAM: <span className="text-[#b0b0c0]">{Math.round(stats.ramUsed / 1024)}G/{Math.round(stats.ramTotal / 1024)}G</span></div>
          </div>
        </div>
      )}
    </div>
  );
}

// ===== Timeline Bar (Feature 7) =====
function TimelineBar({ activities }: { activities: ActivityItem[] }) {
  const now = new Date();
  const hours: { hour: number; count: number; agents: string[] }[] = [];

  for (let i = 23; i >= 0; i--) {
    const hourStart = new Date(now);
    hourStart.setHours(now.getHours() - i, 0, 0, 0);
    const hourEnd = new Date(hourStart);
    hourEnd.setHours(hourStart.getHours() + 1);

    const hourActivities = activities.filter(a => {
      const t = new Date(a.timestamp).getTime();
      return t >= hourStart.getTime() && t < hourEnd.getTime();
    });

    const uniqueAgents = [...new Set(hourActivities.map(a => a.agentName))];
    hours.push({ hour: hourStart.getHours(), count: hourActivities.length, agents: uniqueAgents });
  }

  const [hoveredHour, setHoveredHour] = useState<number | null>(null);

  return (
    <div className="px-2 py-1 border-t border-[#1e1e30]">
      <div className="flex items-end gap-px h-4">
        {hours.map((h, i) => {
          const isNow = i === 23;
          const color = h.count > 3 ? '#22c55e' : h.count > 0 ? '#eab308' : '#1e1e30';
          return (
            <div
              key={i}
              className="flex-1 relative cursor-pointer"
              onMouseEnter={() => setHoveredHour(i)}
              onMouseLeave={() => setHoveredHour(null)}
              style={{
                height: '100%',
                backgroundColor: color + (isNow ? '' : '88'),
                borderRadius: 1,
                border: isNow ? '1px solid #22c55e55' : 'none',
              }}
            >
              {hoveredHour === i && (
                <div className="absolute bottom-5 left-1/2 -translate-x-1/2 bg-[#1a1a2eee] border border-[#3a3a5e] rounded px-2 py-1 text-[9px] text-[#b0b0c0] whitespace-nowrap z-50">
                  {h.hour}:00 — {h.agents.length > 0 ? h.agents.join(', ') : 'quiet'}
                </div>
              )}
            </div>
          );
        })}
      </div>
      <div className="flex justify-between text-[8px] text-[#4b5563] mt-0.5">
        <span>-24h</span>
        <span>now</span>
      </div>
    </div>
  );
}

type TabId = 'now' | 'feed' | 'stats';

export default function ActivityPanel({ agents, activities, stats }: ActivityPanelProps) {
  const feedRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabId>('now');
  const prevCountRef = useRef(0);
  const activeCount = agents.filter(a => a.status === 'active').length;
  const idleCount = agents.filter(a => a.status === 'idle').length;
  const offlineCount = agents.filter(a => a.status === 'offline').length;
  const roomCounts = groupByRoom(agents);

  const sortedActivities = [...activities]
    .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
    .slice(-40);

  useEffect(() => {
    if (autoScroll && feedRef.current && activities.length !== prevCountRef.current) {
      feedRef.current.scrollTo({ top: feedRef.current.scrollHeight, behavior: 'smooth' });
    }
    prevCountRef.current = activities.length;
  }, [activities.length, autoScroll]);

  useEffect(() => {
    const el = feedRef.current;
    if (!el) return;
    const onScroll = () => {
      const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 60;
      setAutoScroll(atBottom);
    };
    el.addEventListener('scroll', onScroll);
    return () => el.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <div className="flex flex-col h-full overflow-hidden" style={{ backgroundColor: '#0f0f1a' }}>
      {/* Compact Header */}
      <div className="px-3 py-2 border-b border-[#1e1e30] flex items-center justify-between">
        <h1 className="text-sm font-bold text-white tracking-wide flex items-center gap-1.5">
          ⚡ The Agency
        </h1>
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] bg-[#22c55e22] text-[#22c55e] px-1.5 py-0.5 rounded-full">{activeCount}</span>
          {idleCount > 0 && <span className="text-[10px] bg-[#eab30822] text-[#eab308] px-1.5 py-0.5 rounded-full">{idleCount}</span>}
          {offlineCount > 0 && <span className="text-[10px] bg-[#6b728022] text-[#6b7280] px-1.5 py-0.5 rounded-full">{offlineCount}</span>}
        </div>
      </div>

      {/* Room counts */}
      <div className="px-3 py-1 border-b border-[#1e1e30] flex items-center gap-2 text-[10px] text-[#6b7280]">
        {Object.entries(roomCounts).map(([roomId, count]) => {
          if (count === 0) return null;
          const room = ROOM_LABELS[roomId as RoomId];
          return <span key={roomId}>{room.emoji}{count}</span>;
        })}
        <span className="ml-auto flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
          <span className="text-[9px] text-[#22c55e]">LIVE</span>
        </span>
      </div>

      {/* Agent strip — larger touch targets on mobile */}
      <div className="px-2 py-1.5 border-b border-[#1e1e30] flex items-center gap-1.5 md:gap-1 overflow-x-auto scrollbar-none">
        {agents.map(agent => {
          const isActive = agent.status === 'active';
          const isIdle = agent.status === 'idle';
          const dotColor = isActive ? 'bg-green-500' : isIdle ? 'bg-yellow-500' : 'bg-gray-600';
          const isExpanded = expandedAgent === agent.id;

          return (
            <button
              key={agent.id}
              onClick={() => setExpandedAgent(isExpanded ? null : agent.id)}
              className="relative shrink-0 flex items-center gap-1 px-2 md:px-1.5 py-1.5 md:py-0.5 rounded-full transition-all hover:bg-[#1a1a2e] min-w-[36px] min-h-[36px] md:min-w-0 md:min-h-0 justify-center"
              style={{
                backgroundColor: isExpanded ? agent.color + '22' : 'transparent',
                border: isExpanded ? `1px solid ${agent.color}44` : '1px solid transparent',
              }}
            >
              <span className="text-sm md:text-xs">{agent.emoji}</span>
              <span className={`absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 md:w-2 md:h-2 rounded-full ${dotColor} border border-[#0f0f1a]`} />
              {isExpanded && (
                <span className="text-[11px] md:text-[10px] font-medium text-[#d0d0d0]">{agent.name}</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Expanded agent detail */}
      {expandedAgent && (() => {
        const agent = agents.find(a => a.id === expandedAgent);
        if (!agent) return null;
        const room = ROOM_LABELS[agent.room];
        return (
          <div className="px-3 py-2 border-b border-[#1e1e30] bg-[#12121f]">
            <div className="flex items-center gap-2">
              <span>{agent.emoji}</span>
              <span className="text-xs font-bold text-white">{agent.name}</span>
              <span className="text-[10px] text-[#6b7280]">{agent.role}</span>
              <span className="text-[10px] ml-auto" style={{ color: agent.color }}>{room?.emoji} {room?.name}</span>
            </div>
            {agent.currentTask && (
              <p className="text-[10px] text-[#9ca3af] mt-1 truncate">📝 {agent.currentTask}</p>
            )}
            <p className="text-[9px] text-[#4b5563] mt-0.5">{agent.model} · {agent.lastActiveRelative}</p>
          </div>
        );
      })()}

      {/* Tab Bar — touch-friendly on mobile (44px tap targets) */}
      <div className="px-3 py-1 border-b border-[#1e1e30] flex items-center gap-1 md:gap-3">
        {([
          { id: 'now' as TabId, label: '🔥 Now' },
          { id: 'feed' as TabId, label: '💬 Feed' },
          { id: 'stats' as TabId, label: '📊 Stats' },
        ]).map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`text-xs md:text-[10px] font-bold py-2 md:py-0.5 px-3 md:px-0 min-h-[44px] md:min-h-0 transition-colors ${
              activeTab === tab.id
                ? 'text-white border-b-2 md:border-b border-white'
                : 'text-[#6b7280] hover:text-[#9ca3af]'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto" ref={activeTab === 'feed' ? feedRef : undefined}>
        {activeTab === 'now' && <NowTab agents={agents} />}
        {activeTab === 'feed' && (
          <div className="py-1">
            {sortedActivities.length === 0 ? (
              <p className="text-[10px] text-[#4b5563] text-center py-6">Waiting for activity...</p>
            ) : (
              sortedActivities.map((item, i) => <CompactMessage key={i} item={item} />)
            )}
          </div>
        )}
        {activeTab === 'stats' && <StatsTab agents={agents} activities={activities} stats={stats} />}
      </div>

      {/* Timeline Bar */}
      <TimelineBar activities={activities} />

      {/* System Stats — minimal footer */}
      {stats && (
        <div className="px-3 py-1.5 border-t border-[#1e1e30] flex items-center gap-3 text-[9px] text-[#4b5563] bg-[#0a0a14]">
          <span>CPU {stats.cpuLoad.toFixed(1)}</span>
          <span>RAM {Math.round(stats.ramUsed / 1024)}G/{Math.round(stats.ramTotal / 1024)}G</span>
          <span className="ml-auto">Up {stats.uptime}</span>
        </div>
      )}
    </div>
  );
}
