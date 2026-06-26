'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import dynamic from 'next/dynamic';
import ActivityPanel from '@/components/ActivityPanel';
import { AgentState, ActivityItem, SystemStats, AGENTS } from '@/lib/agents';
import { generateChatMessage } from '@/lib/agent-chat';

const PixelOffice = dynamic(() => import('@/components/PixelOffice'), { ssr: false });

type ArenaMode = 'live' | 'demo' | null;

// Agent personality taglines for spotlight
const AGENT_TAGLINES: Record<string, string> = {
  main: 'Calm under pressure. Will challenge your worst ideas.',
  dev: 'Ships first, asks questions never.',
  trader: 'Everything is a market opportunity.',
  research: 'Will bring receipts. All of them.',
  creative: 'If the spacing is wrong, everything is wrong.',
  audit: 'Trust no one. Audit everything.',
  social: 'Third draft is the charm.',
  growth: "What's the CAC on that?",
  rook: 'The spec said 3 columns. I built 3 columns.',
  pm: "We're behind schedule. Just saying.",
  finance: 'That cost $0.03. Was it necessary?',
};

export default function Home() {
  const [agents, setAgents] = useState<AgentState[]>([]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [mode, setMode] = useState<ArenaMode>(null);
  const [showIntro, setShowIntro] = useState(false);
  const [introFading, setIntroFading] = useState(false);
  const [spotlightAgent, setSpotlightAgent] = useState<AgentState | null>(null);
  const chatTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const [statusRes, activityRes, statsRes] = await Promise.all([
        fetch('/api/agents/status'),
        fetch('/api/agents/activity'),
        fetch('/api/agents/stats'),
      ]);

      if (statusRes.ok) {
        const data = await statusRes.json();
        setAgents(data.agents || []);
        if (data.mode) setMode(data.mode);
      }
      if (activityRes.ok) {
        const data = await activityRes.json();
        setActivities(prev => {
          // Merge real activities with chat messages (keep chat messages that are newer)
          const realActivities: ActivityItem[] = data.activities || [];
          const chatMessages = prev.filter(a => a.type === 'chat');
          const merged = [...realActivities, ...chatMessages]
            .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
            .slice(-60);
          return merged;
        });
      }
      if (statsRes.ok) {
        const data = await statsRes.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to fetch data:', err);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, [fetchData]);

  // Welcome intro — once per session
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const seen = sessionStorage.getItem('agency-intro-seen');
    if (!seen) {
      setShowIntro(true);
      sessionStorage.setItem('agency-intro-seen', '1');
      // Start fade after 1.5s
      setTimeout(() => setIntroFading(true), 1500);
      // Remove after 2.5s
      setTimeout(() => setShowIntro(false), 2500);
    }
  }, []);

  // Chat message generator — every 30-60 seconds
  useEffect(() => {
    const scheduleNext = () => {
      const delay = 30000 + Math.random() * 30000; // 30-60s
      chatTimerRef.current = setTimeout(() => {
        const chatMsg = generateChatMessage();
        // Override type to 'chat'
        const chatActivity: ActivityItem = { ...chatMsg, type: 'chat' };
        setActivities(prev => [...prev, chatActivity].slice(-60));
        scheduleNext();
      }, delay);
    };

    // Start with a shorter initial delay so users see chat quickly
    chatTimerRef.current = setTimeout(() => {
      const chatMsg = generateChatMessage();
      const chatActivity: ActivityItem = { ...chatMsg, type: 'chat' };
      setActivities(prev => [...prev, chatActivity].slice(-60));
      scheduleNext();
    }, 5000 + Math.random() * 10000);

    return () => {
      if (chatTimerRef.current) clearTimeout(chatTimerRef.current);
    };
  }, []);

  // Handle agent click from PixelOffice
  const handleAgentClick = useCallback((agentId: string) => {
    const agent = agents.find(a => a.id === agentId);
    if (agent) {
      setSpotlightAgent(agent);
    }
  }, [agents]);

  const dismissSpotlight = useCallback(() => {
    setSpotlightAgent(null);
  }, []);

  // Get last activity for spotlight agent
  const getLastActivity = (agentId: string): string | null => {
    const agentActivities = activities.filter(a => a.agentId === agentId);
    if (agentActivities.length === 0) return null;
    return agentActivities[agentActivities.length - 1].message;
  };

  const ROOM_NAMES: Record<string, string> = {
    main_office: 'Main Office',
    meeting_room: 'Meeting Room',
    kitchen: 'Kitchen',
    game_room: 'Game Room',
    server_room: 'Server Room',
    rest_room: 'Rest Room',
  };

  return (
    <main className="h-screen w-screen bg-[#0a0a0f] flex flex-col md:flex-row overflow-hidden relative">
      {/* Top (mobile) / Left (desktop): Pixel Office */}
      <div className="w-full md:flex-[7] h-[55vh] md:h-full p-1 md:p-2 flex items-center justify-center min-w-0 shrink-0">
        <PixelOffice agents={agents} activities={activities} onAgentClick={handleAgentClick} />
      </div>

      {/* Bottom (mobile) / Right (desktop): Activity Panel */}
      <div className="w-full md:flex-[3] flex-1 md:h-full border-t md:border-t-0 md:border-l border-[#2a2a3e] flex flex-col md:max-w-[380px] md:min-w-[260px] overflow-hidden">
        <ActivityPanel agents={agents} activities={activities} stats={stats} />
      </div>

      {/* Mode Badge — top-left */}
      {mode && (
        <div className={`absolute top-3 left-3 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5 z-50 ${
          mode === 'live'
            ? 'bg-green-500/20 text-green-400 border border-green-500/30'
            : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${
            mode === 'live' ? 'bg-green-400 animate-pulse' : 'bg-amber-400'
          }`} />
          {mode === 'live' ? 'Live' : 'Demo'}
        </div>
      )}

      {/* Welcome Intro Overlay */}
      {showIntro && (
        <div
          className={`fixed inset-0 z-[100] flex flex-col items-center justify-center transition-opacity duration-1000 ${
            introFading ? 'opacity-0' : 'opacity-100'
          }`}
          style={{ backgroundColor: '#0a0a0f' }}
        >
          <h1
            className="text-3xl sm:text-5xl md:text-8xl font-bold text-white tracking-widest mb-4 px-4 text-center"
            style={{
              fontFamily: 'monospace',
              textShadow: '0 0 40px rgba(147,51,234,0.5), 0 0 80px rgba(147,51,234,0.2)',
            }}
          >
            THE AGENCY
          </h1>
          <p className="text-sm sm:text-lg md:text-2xl text-[#9ca3af] tracking-wide" style={{ fontFamily: 'monospace' }}>
            11 AI Agents. One Office.
          </p>
        </div>
      )}

      {/* Agent Spotlight Overlay */}
      {spotlightAgent && (
        <div
          className="fixed inset-0 z-[90] cursor-pointer"
          onClick={dismissSpotlight}
          style={{ backgroundColor: 'rgba(0,0,0,0.6)' }}
        >
          <div
            className="absolute bg-[#12121f] border rounded-xl p-4 shadow-2xl max-w-[280px] sm:max-w-[300px] cursor-default left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 md:left-[35%] md:top-1/2 w-[calc(100vw-2rem)] sm:w-auto mx-auto"
            onClick={(e) => e.stopPropagation()}
            style={{
              borderColor: spotlightAgent.color + '66',
              boxShadow: `0 0 40px ${spotlightAgent.color}22`,
            }}
          >
            {/* Agent header */}
            <div className="flex items-center gap-3 mb-3">
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center text-2xl"
                style={{ backgroundColor: spotlightAgent.color + '22', border: `2px solid ${spotlightAgent.color}44` }}
              >
                {spotlightAgent.emoji}
              </div>
              <div>
                <h2 className="text-lg font-bold text-white">{spotlightAgent.name}</h2>
                <p className="text-xs" style={{ color: spotlightAgent.color }}>{spotlightAgent.role}</p>
              </div>
            </div>

            {/* Tagline */}
            <p className="text-sm text-[#9ca3af] italic mb-3 border-l-2 pl-2" style={{ borderColor: spotlightAgent.color + '66' }}>
              "{AGENT_TAGLINES[spotlightAgent.id] || 'Ready for action.'}"
            </p>

            {/* Details */}
            <div className="space-y-1.5 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-[#6b7280]">Model</span>
                <span className="text-[#b0b0c0] font-mono">{spotlightAgent.model}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#6b7280]">Status</span>
                <span className="flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full ${
                    spotlightAgent.status === 'active' ? 'bg-green-500' :
                    spotlightAgent.status === 'idle' ? 'bg-yellow-500' : 'bg-gray-600'
                  }`} />
                  <span className="text-[#b0b0c0] capitalize">{spotlightAgent.status}</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#6b7280]">Room</span>
                <span className="text-[#b0b0c0]">{ROOM_NAMES[spotlightAgent.room] || spotlightAgent.room}</span>
              </div>
              {spotlightAgent.currentTask && (
                <div className="pt-1.5 border-t border-[#1e1e30]">
                  <span className="text-[#6b7280]">Current Task</span>
                  <p className="text-[#b0b0c0] mt-0.5">{spotlightAgent.currentTask}</p>
                </div>
              )}
              {getLastActivity(spotlightAgent.id) && (
                <div className="pt-1.5 border-t border-[#1e1e30]">
                  <span className="text-[#6b7280]">Last Activity</span>
                  <p className="text-[#b0b0c0] mt-0.5 truncate">{getLastActivity(spotlightAgent.id)}</p>
                </div>
              )}
            </div>

            {/* Click to dismiss hint */}
            <p className="text-[9px] text-[#4b5563] text-center mt-3">Tap outside to dismiss</p>
          </div>
        </div>
      )}
    </main>
  );
}
