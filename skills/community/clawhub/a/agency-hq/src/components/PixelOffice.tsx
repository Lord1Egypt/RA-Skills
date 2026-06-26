'use client';

import { useEffect, useRef, useCallback, useState } from 'react';
import { AgentState, RoomId, ActivityItem, AGENTS } from '@/lib/agents';

// ===== CANVAS DIMENSIONS =====
const W = 960;
const H = 720;

// ===== COLOR HELPERS =====
function darkenColor(hex: string, amount: number): string {
  const num = parseInt(hex.replace('#', ''), 16);
  const r = Math.max(0, Math.floor(((num >> 16) & 255) * (1 - amount)));
  const g = Math.max(0, Math.floor(((num >> 8) & 255) * (1 - amount)));
  const b = Math.max(0, Math.floor((num & 255) * (1 - amount)));
  return `rgb(${r},${g},${b})`;
}

function lightenColor(hex: string, amount: number): string {
  const num = parseInt(hex.replace('#', ''), 16);
  const r = Math.min(255, Math.floor(((num >> 16) & 255) * (1 + amount)));
  const g = Math.min(255, Math.floor(((num >> 8) & 255) * (1 + amount)));
  const b = Math.min(255, Math.floor((num & 255) * (1 + amount)));
  return `rgb(${r},${g},${b})`;
}

// ===== ROOM LAYOUT =====
interface RoomDef {
  id: RoomId;
  label: string;
  emoji: string;
  x: number; y: number; w: number; h: number;
  floorColor1: string;
  floorColor2: string;
  tileSize: number;
}

const ROOMS: RoomDef[] = [
  { id: 'meeting_room', label: 'MEETING ROOM', emoji: '🤝', x: 0, y: 0, w: 480, h: 260, floorColor1: '#1e2438', floorColor2: '#1a2030', tileSize: 28 },
  { id: 'server_room', label: 'SERVER ROOM', emoji: '🖥️', x: 480, y: 0, w: 480, h: 260, floorColor1: '#1a1a28', floorColor2: '#151522', tileSize: 24 },
  { id: 'main_office', label: 'MAIN OFFICE', emoji: '🏢', x: 0, y: 260, w: 960, h: 260, floorColor1: '#1e1e35', floorColor2: '#18182c', tileSize: 32 },
  { id: 'kitchen', label: 'KITCHEN', emoji: '🍳', x: 0, y: 520, w: 240, h: 200, floorColor1: '#2a2418', floorColor2: '#221e14', tileSize: 26 },
  { id: 'game_room', label: 'GAME ROOM', emoji: '🎮', x: 240, y: 520, w: 340, h: 200, floorColor1: '#1a1e2e', floorColor2: '#151828', tileSize: 30 },
  { id: 'rest_room', label: 'REST ROOM', emoji: '😴', x: 580, y: 520, w: 380, h: 200, floorColor1: '#141420', floorColor2: '#10101a', tileSize: 28 },
];

function getRoomDef(id: RoomId): RoomDef {
  return ROOMS.find(r => r.id === id) || ROOMS[2];
}

// ===== DESK POSITIONS =====
const DESK_LAYOUT: Record<string, { x: number; y: number; row: number }> = {
  command:     { x: 100, y: 310, row: 0 },
  dev:         { x: 240, y: 310, row: 0 },
  trading:     { x: 380, y: 310, row: 0 },
  research:    { x: 520, y: 310, row: 0 },
  design:      { x: 660, y: 310, row: 0 },
  security:    { x: 800, y: 310, row: 0 },
  content:     { x: 160, y: 420, row: 1 },
  strategy:    { x: 320, y: 420, row: 1 },
  engineering: { x: 480, y: 420, row: 1 },
  pm:          { x: 640, y: 420, row: 1 },
  finance:     { x: 800, y: 420, row: 1 },
};

const KITCHEN_SPOTS = [
  { x: 45, y: 595 }, { x: 110, y: 600 }, { x: 175, y: 595 },
  { x: 65, y: 650 }, { x: 140, y: 655 }, { x: 210, y: 650 },
];

const GAME_ROOM_SPOTS = [
  { x: 310, y: 585 }, { x: 390, y: 595 }, { x: 470, y: 585 },
  { x: 340, y: 650 }, { x: 420, y: 655 }, { x: 500, y: 650 },
  { x: 530, y: 595 }, { x: 365, y: 620 },
];

// Rest room bed/couch spots — each sleeping agent gets unique position
const REST_ROOM_SPOTS = [
  { x: 630, y: 580 }, { x: 720, y: 575 }, { x: 810, y: 580 },
  { x: 900, y: 575 }, { x: 660, y: 640 }, { x: 750, y: 645 },
  { x: 840, y: 640 }, { x: 930, y: 645 }, { x: 690, y: 690 },
  { x: 780, y: 695 }, { x: 870, y: 690 },
];

const SERVER_ROOM_SPOTS = [
  { x: 540, y: 100 }, { x: 620, y: 80 }, { x: 700, y: 100 },
  { x: 800, y: 80 }, { x: 880, y: 100 },
  { x: 570, y: 180 }, { x: 660, y: 170 }, { x: 750, y: 180 },
  { x: 840, y: 170 }, { x: 920, y: 180 },
];

const MEETING_SPOTS = [
  { x: 130, y: 100 }, { x: 210, y: 80 }, { x: 290, y: 100 },
  { x: 130, y: 160 }, { x: 210, y: 180 }, { x: 290, y: 160 },
  { x: 370, y: 100 }, { x: 370, y: 160 },
];

const DOORWAYS = [
  { x: 200, y: 250, w: 60, h: 20 },
  { x: 500, y: 250, w: 60, h: 20 },
  { x: 700, y: 250, w: 60, h: 20 },
  { x: 100, y: 510, w: 60, h: 20 },
  { x: 380, y: 510, w: 60, h: 20 },
  { x: 700, y: 510, w: 60, h: 20 },
];

// ===== AGENT ANIMATION STATE =====
interface AnimAgent {
  id: string;
  x: number; y: number;
  targetX: number; targetY: number;
  room: RoomId; targetRoom: RoomId;
  walkFrame: number;
  state: 'sitting' | 'walking' | 'standing' | 'sleeping' | 'coffee' | 'meeting' | 'gaming';
  gestureFrame: number;
  idleOffset: number;
}

// ===== PARTICLE / EFFECTS SYSTEM =====
interface Particle {
  x: number; y: number;
  vx: number; vy: number;
  life: number; maxLife: number;
  type: 'confetti' | 'flash' | 'float';
  color?: string;
  emoji?: string;
  agentId: string;
  size?: number;
}

// ===== FOOTPRINT SYSTEM =====
interface Footprint {
  x: number; y: number;
  opacity: number;
  side: 'left' | 'right';
  createdAt: number;
}

// ===== EFFECT DEFINITIONS =====
const EFFECTS: Record<string, { type: string; colors?: string[]; color?: string; emoji?: string; count: number; duration: number; repeat?: number }> = {
  deploy:        { type: 'confetti', colors: ['#22c55e', '#3b82f6', '#eab308'], count: 15, duration: 2000 },
  blocked:       { type: 'flash', color: '#ef4444', count: 1, duration: 500, repeat: 3 },
  trade:         { type: 'float', emoji: '💰', count: 3, duration: 1500 },
  research_done: { type: 'float', emoji: '💡', count: 1, duration: 1000 },
  error:         { type: 'flash', color: '#ef4444', count: 1, duration: 300, repeat: 2 },
  review_pass:   { type: 'float', emoji: '✅', count: 1, duration: 1000 },
  review_fail:   { type: 'float', emoji: '❌', count: 1, duration: 1000 },
  coffee:        { type: 'float', emoji: '☕', count: 1, duration: 800 },
  idea:          { type: 'float', emoji: '💡', count: 2, duration: 1200 },
};

function detectEventType(message: string): string | null {
  const lower = message.toLowerCase();
  if (lower.includes('deployed') || lower.includes('shipped') || lower.includes('deploy')) return 'deploy';
  if (lower.includes('blocked')) return 'blocked';
  if (lower.includes('error') || lower.includes('failed') || lower.includes('crash')) return 'error';
  if (lower.includes('placed bet') || lower.includes('trade') || lower.includes('bought') || lower.includes('sold')) return 'trade';
  if (lower.includes('completed research') || lower.includes('research report') || lower.includes('research complete')) return 'research_done';
  if (lower.includes('approved') || lower.includes('review pass') || lower.includes('lgtm')) return 'review_pass';
  if (lower.includes('rejected') || lower.includes('review fail') || lower.includes('changes requested')) return 'review_fail';
  if (lower.includes('coffee') || lower.includes('break')) return 'coffee';
  if (lower.includes('idea') || lower.includes('eureka') || lower.includes('insight')) return 'idea';
  if (lower.includes('completed') || lower.includes('finished') || lower.includes('done')) return 'review_pass';
  return null;
}

// ===== MONITOR CONTENT TYPES PER AGENT =====
const MONITOR_CONTENT: Record<string, string> = {
  dev: 'green_code', trader: 'candle_chart', research: 'scrolling_data',
  creative: 'color_palette', growth: 'bar_chart', rook: 'terminal_blink',
  audit: 'shield_pulse', social: 'text_editor', main: 'dashboard',
  pm: 'kanban', finance: 'spreadsheet',
};

interface PixelOfficeProps {
  agents: AgentState[];
  activities?: ActivityItem[];
  onAgentClick?: (agentId: string) => void;
}

export default function PixelOffice({ agents, activities = [], onAgentClick }: PixelOfficeProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const frameRef = useRef(0);
  const animRef = useRef<number>(0);
  const agentAnimRef = useRef<Map<string, AnimAgent>>(new Map());
  const particlesRef = useRef<Particle[]>([]);
  const footprintsRef = useRef<Footprint[]>([]);
  const flashAgentsRef = useRef<Map<string, { color: string; until: number; repeat: number }>>(new Map());
  const prevActivitiesRef = useRef<number>(0);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; content: React.ReactNode } | null>(null);
  const [toasts, setToasts] = useState<{ id: number; agent: string; emoji: string; color: string; message: string; time: number }[]>([]);
  const toastIdRef = useRef(0);
  const [isMobile, setIsMobile] = useState(false);

  // Detect mobile
  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener('resize', check);
    return () => window.removeEventListener('resize', check);
  }, []);

  // ===== SPAWN PARTICLES FOR AN AGENT =====
  const spawnEffect = useCallback((agentId: string, effectKey: string) => {
    const effect = EFFECTS[effectKey];
    if (!effect) return;
    const anim = agentAnimRef.current.get(agentId);
    if (!anim) return;

    if (effect.type === 'confetti') {
      const colors = effect.colors || ['#fff'];
      for (let i = 0; i < effect.count; i++) {
        particlesRef.current.push({
          x: anim.x, y: anim.y - 10,
          vx: (Math.random() - 0.5) * 4,
          vy: -(Math.random() * 3 + 2),
          life: effect.duration / 16, maxLife: effect.duration / 16,
          type: 'confetti', color: colors[i % colors.length],
          agentId, size: 2 + Math.random() * 2,
        });
      }
    } else if (effect.type === 'flash') {
      flashAgentsRef.current.set(agentId, {
        color: effect.color || '#ef4444',
        until: Date.now() + effect.duration * (effect.repeat || 1),
        repeat: effect.repeat || 1,
      });
    } else if (effect.type === 'float') {
      for (let i = 0; i < effect.count; i++) {
        particlesRef.current.push({
          x: anim.x + (Math.random() - 0.5) * 10, y: anim.y - 15,
          vx: (Math.random() - 0.5) * 0.5,
          vy: -(Math.random() * 0.5 + 0.5),
          life: effect.duration / 16, maxLife: effect.duration / 16,
          type: 'float', emoji: effect.emoji, agentId,
        });
      }
    }
  }, []);

  // ===== DETECT NEW ACTIVITIES AND TRIGGER EFFECTS + TOASTS =====
  useEffect(() => {
    if (activities.length > prevActivitiesRef.current && prevActivitiesRef.current > 0) {
      const newItems = activities.slice(prevActivitiesRef.current);
      for (const item of newItems) {
        const eventType = detectEventType(item.message);
        if (eventType) {
          spawnEffect(item.agentId, eventType);
        }
        // Toast notification
        toastIdRef.current++;
        setToasts(prev => {
          const next = [...prev, {
            id: toastIdRef.current,
            agent: item.agentName,
            emoji: item.agentEmoji,
            color: item.agentColor || '#9ca3af',
            message: item.message.substring(0, 60),
            time: Date.now(),
          }];
          return next.slice(-3); // max 3
        });
      }
    }
    prevActivitiesRef.current = activities.length;
  }, [activities, spawnEffect]);

  // Auto-dismiss toasts
  useEffect(() => {
    if (toasts.length === 0) return;
    const timer = setInterval(() => {
      setToasts(prev => prev.filter(t => Date.now() - t.time < 4000));
    }, 500);
    return () => clearInterval(timer);
  }, [toasts.length]);

  const getTargetPosition = useCallback((agent: AgentState, allAgents: AgentState[]): { x: number; y: number; state: AnimAgent['state'] } => {
    const room = agent.room;

    if (room === 'main_office') {
      const desk = DESK_LAYOUT[agent.desk];
      if (desk) return { x: desk.x, y: desk.y, state: 'sitting' };
      return { x: 480, y: 380, state: 'standing' };
    }
    if (room === 'meeting_room') {
      const meetingAgents = allAgents.filter(a => a.room === 'meeting_room');
      const idx = meetingAgents.findIndex(a => a.id === agent.id);
      const spot = MEETING_SPOTS[idx % MEETING_SPOTS.length];
      return { x: spot.x, y: spot.y, state: 'meeting' };
    }
    if (room === 'kitchen') {
      const kitchenAgents = allAgents.filter(a => a.room === 'kitchen');
      const idx = kitchenAgents.findIndex(a => a.id === agent.id);
      const spot = KITCHEN_SPOTS[idx % KITCHEN_SPOTS.length];
      return { x: spot.x, y: spot.y, state: 'coffee' };
    }
    if (room === 'server_room') {
      const serverAgents = allAgents.filter(a => a.room === 'server_room');
      const idx = serverAgents.findIndex(a => a.id === agent.id);
      const spot = SERVER_ROOM_SPOTS[idx % SERVER_ROOM_SPOTS.length];
      return { x: spot.x, y: spot.y, state: 'standing' };
    }
    if (room === 'game_room') {
      const gameAgents = allAgents.filter(a => a.room === 'game_room');
      const idx = gameAgents.findIndex(a => a.id === agent.id);
      const spot = GAME_ROOM_SPOTS[idx % GAME_ROOM_SPOTS.length];
      return { x: spot.x, y: spot.y, state: 'gaming' };
    }
    if (room === 'rest_room') {
      const sleepAgents = allAgents.filter(a => a.room === 'rest_room');
      const idx = sleepAgents.findIndex(a => a.id === agent.id);
      const spot = REST_ROOM_SPOTS[idx % REST_ROOM_SPOTS.length];
      return { x: spot.x, y: spot.y, state: 'sleeping' };
    }
    return { x: 480, y: 380, state: 'standing' };
  }, []);

  useEffect(() => {
    const animMap = agentAnimRef.current;
    for (const agent of agents) {
      const target = getTargetPosition(agent, agents);
      let anim = animMap.get(agent.id);
      if (!anim) {
        anim = {
          id: agent.id, x: target.x, y: target.y,
          targetX: target.x, targetY: target.y,
          room: agent.room, targetRoom: agent.room,
          walkFrame: 0, state: target.state,
          gestureFrame: 0, idleOffset: Math.random() * 1000,
        };
        animMap.set(agent.id, anim);
      } else {
        anim.targetX = target.x;
        anim.targetY = target.y;
        anim.targetRoom = agent.room;
        if (Math.abs(anim.x - target.x) < 3 && Math.abs(anim.y - target.y) < 3) {
          anim.state = target.state;
          anim.room = agent.room;
        } else {
          anim.state = 'walking';
        }
      }
    }
  }, [agents, getTargetPosition]);

  // ===== HOVER DETECTION =====
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = W / rect.width;
    const scaleY = H / rect.height;
    const mx = (e.clientX - rect.left) * scaleX;
    const my = (e.clientY - rect.top) * scaleY;

    // Check agents first
    const animMap = agentAnimRef.current;
    for (const agent of agents) {
      const anim = animMap.get(agent.id);
      if (!anim) continue;
      if (Math.abs(mx - anim.x) < 20 && Math.abs(my - anim.y) < 24) {
        const room = getRoomDef(agent.room);
        setTooltip({
          x: e.clientX, y: e.clientY,
          content: (
            <div style={{ borderLeft: `3px solid ${agent.color}` }} className="pl-2">
              <div className="font-bold text-white text-xs">{agent.emoji} {agent.name}</div>
              <div className="text-[10px] text-gray-400">{agent.role}</div>
              <div className="text-[10px]" style={{ color: agent.color }}>
                {agent.status === 'active' ? '🟢' : agent.status === 'idle' ? '🟡' : '⚫'} {agent.status} · {room.emoji} {room.label}
              </div>
              {agent.currentTask && <div className="text-[10px] text-gray-300 mt-0.5">📝 {agent.currentTask}</div>}
              {agent.lastActiveRelative && <div className="text-[10px] text-gray-500">Last: {agent.lastActiveRelative}</div>}
              <div className="text-[9px] text-gray-500 mt-0.5">{agent.model}</div>
            </div>
          ),
        });
        return;
      }
    }

    // Check rooms
    for (const room of ROOMS) {
      if (mx >= room.x && mx <= room.x + room.w && my >= room.y && my <= room.y + room.h) {
        const agentsInRoom = agents.filter(a => a.room === room.id);
        const names = agentsInRoom.map(a => a.name).join(', ') || 'empty';
        setTooltip({
          x: e.clientX, y: e.clientY,
          content: (
            <div>
              <div className="font-bold text-white text-xs">{room.emoji} {room.label}</div>
              <div className="text-[10px] text-gray-400">{names}</div>
            </div>
          ),
        });
        return;
      }
    }
    setTooltip(null);
  }, [agents]);

  const handleMouseLeave = useCallback(() => setTooltip(null), []);

  // ===== CLICK/TAP DETECTION =====
  const hitTestAgent = useCallback((clientX: number, clientY: number) => {
    if (!onAgentClick) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = W / rect.width;
    const scaleY = H / rect.height;
    const mx = (clientX - rect.left) * scaleX;
    const my = (clientY - rect.top) * scaleY;
    // Larger hit area on mobile for touch friendliness
    const hitX = isMobile ? 28 : 20;
    const hitY = isMobile ? 32 : 24;

    const animMap = agentAnimRef.current;
    for (const agent of agents) {
      const anim = animMap.get(agent.id);
      if (!anim) continue;
      if (Math.abs(mx - anim.x) < hitX && Math.abs(my - anim.y) < hitY) {
        onAgentClick(agent.id);
        return;
      }
    }
  }, [agents, onAgentClick, isMobile]);

  const handleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    hitTestAgent(e.clientX, e.clientY);
  }, [hitTestAgent]);

  const handleTouchEnd = useCallback((e: React.TouchEvent<HTMLCanvasElement>) => {
    if (e.changedTouches.length > 0) {
      const touch = e.changedTouches[0];
      hitTestAgent(touch.clientX, touch.clientY);
    }
  }, [hitTestAgent]);

  // ===== MAIN DRAW =====
  const drawFrame = useCallback((ctx: CanvasRenderingContext2D, frame: number) => {
    ctx.imageSmoothingEnabled = false;

    for (const room of ROOMS) drawRoomFloor(ctx, room);
    drawWeatherWindows(ctx, frame);
    drawWalls(ctx);
    drawDoorways(ctx);
    drawBaseboards(ctx);
    for (const room of ROOMS) drawRoomLabel(ctx, room);

    drawMeetingRoom(ctx, frame);
    drawServerRoom(ctx, frame);
    drawMainOfficeDesks(ctx, frame, agents);
    drawKitchen(ctx, frame);
    drawGameRoom(ctx, frame);
    drawRestRoom(ctx, frame);
    drawWallDecorations(ctx, frame);
    drawDayNightOverlay(ctx);
    drawClock(ctx);

    // Draw footprints
    const now = Date.now();
    footprintsRef.current = footprintsRef.current.filter(fp => now - fp.createdAt < 5000);
    for (const fp of footprintsRef.current) {
      const age = (now - fp.createdAt) / 5000;
      ctx.fillStyle = `rgba(40,40,60,${0.3 * (1 - age)})`;
      const ox = fp.side === 'left' ? -2 : 2;
      ctx.fillRect(fp.x + ox, fp.y, 2, 2);
    }

    // Update and draw particles
    const particles = particlesRef.current;
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life--;
      if (p.type === 'confetti') p.vy += 0.12; // gravity
      const alpha = Math.max(0, p.life / p.maxLife);

      if (p.type === 'confetti') {
        ctx.fillStyle = p.color! + Math.floor(alpha * 255).toString(16).padStart(2, '0');
        ctx.fillRect(p.x, p.y, p.size || 3, p.size || 3);
      } else if (p.type === 'float' && p.emoji) {
        ctx.globalAlpha = alpha;
        ctx.font = '12px serif';
        ctx.textAlign = 'center';
        ctx.fillText(p.emoji, p.x, p.y);
        ctx.globalAlpha = 1;
      }

      if (p.life <= 0) particles.splice(i, 1);
    }

    // Agents sorted by Y
    const animMap = agentAnimRef.current;
    const sortedAgents = [...agents].sort((a, b) => {
      const aa = animMap.get(a.id);
      const ab = animMap.get(b.id);
      return (aa?.y || 0) - (ab?.y || 0);
    });

    for (const agent of sortedAgents) {
      const anim = animMap.get(agent.id);
      if (!anim) continue;

      const dx = anim.targetX - anim.x;
      const dy = anim.targetY - anim.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist > 2) {
        const speed = Math.min(2.2, 0.5 + dist * 0.02);
        const prevX = anim.x;
        const prevY = anim.y;
        anim.x += (dx / dist) * speed;
        anim.y += (dy / dist) * speed;
        anim.walkFrame++;
        anim.state = 'walking';

        // Leave footprints
        if (anim.walkFrame % 12 === 0) {
          footprintsRef.current.push({
            x: prevX, y: prevY + 28,
            opacity: 0.3,
            side: anim.walkFrame % 24 === 0 ? 'left' : 'right',
            createdAt: Date.now(),
          });
        }
      } else {
        anim.x = anim.targetX;
        anim.y = anim.targetY;
        anim.room = anim.targetRoom;
        const target = getTargetPosition(agent, agents);
        anim.state = target.state;
      }

      anim.gestureFrame = frame;

      // Flash effect
      const flash = flashAgentsRef.current.get(agent.id);
      if (flash && Date.now() < flash.until) {
        const elapsed = Date.now() - (flash.until - flash.repeat * 500);
        const phase = Math.floor(elapsed / 250) % 2;
        if (phase === 0) {
          ctx.fillStyle = flash.color + '44';
          ctx.beginPath();
          ctx.arc(anim.x, anim.y, 25, 0, Math.PI * 2);
          ctx.fill();
        }
      } else {
        flashAgentsRef.current.delete(agent.id);
      }

      drawShadow(ctx, anim.x, anim.y + 28, 14, 4);
      drawAgent48(ctx, anim.x, anim.y, agent, anim, frame);
    }

    drawAmbient(ctx, frame);
    if (!isMobile) {
      drawMiniMap(ctx, agents, animMap);
    }
  }, [agents, getTargetPosition, isMobile]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      frameRef.current++;
      drawFrame(ctx, frameRef.current);
      animRef.current = requestAnimationFrame(animate);
    };
    animate();
    return () => { if (animRef.current) cancelAnimationFrame(animRef.current); };
  }, [drawFrame]);

  return (
    <div ref={containerRef} className="relative w-full h-full flex items-center justify-center bg-[#0a0a0f]">
      <canvas
        ref={canvasRef}
        width={W}
        height={H}
        className="border border-[#2a2a3e] rounded-lg max-w-full max-h-full"
        style={{ imageRendering: 'pixelated', width: '100%', height: '100%', objectFit: 'contain' }}
        onMouseMove={!isMobile ? handleMouseMove : undefined}
        onMouseLeave={!isMobile ? handleMouseLeave : undefined}
        onClick={handleClick}
        onTouchEnd={handleTouchEnd}
      />

      {/* Tooltip overlay */}
      {tooltip && (
        <div
          className="fixed z-50 pointer-events-none px-3 py-2 rounded-lg shadow-xl"
          style={{
            left: tooltip.x + 14,
            top: tooltip.y - 10,
            backgroundColor: '#1a1a2eee',
            border: '1px solid #3a3a5e',
            maxWidth: 260,
          }}
        >
          {tooltip.content}
        </div>
      )}

      {/* Notification toasts — top on mobile, bottom-right on desktop */}
      <div className={`absolute flex flex-col gap-2 z-50 ${
        isMobile
          ? 'top-2 left-2 right-2'
          : 'bottom-4 right-4'
      }`} style={{ maxWidth: isMobile ? undefined : 280 }}>
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className="flex items-start gap-2 px-3 py-2 rounded-lg shadow-lg animate-slide-in"
            style={{
              backgroundColor: '#1a1a2eee',
              borderLeft: `3px solid ${toast.color}`,
              animation: 'slideIn 0.3s ease-out',
            }}
          >
            <span className="text-sm shrink-0">{toast.emoji}</span>
            <div className="min-w-0">
              <span className="font-bold text-[10px]" style={{ color: toast.color }}>{toast.agent} </span>
              <span className="text-[10px] text-gray-300">{toast.message}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ===== SHADOW =====
function drawShadow(ctx: CanvasRenderingContext2D, x: number, y: number, rx: number, ry: number) {
  ctx.fillStyle = 'rgba(0,0,0,0.2)';
  ctx.beginPath();
  ctx.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2);
  ctx.fill();
}

// ===== ROOM DRAWING =====
function drawRoomFloor(ctx: CanvasRenderingContext2D, room: RoomDef) {
  const { x, y, w, h, floorColor1, floorColor2, tileSize } = room;
  ctx.fillStyle = floorColor1;
  ctx.fillRect(x, y, w, h);
  for (let tx = x; tx < x + w; tx += tileSize) {
    for (let ty = y; ty < y + h; ty += tileSize) {
      const col = Math.floor((tx - x) / tileSize);
      const row = Math.floor((ty - y) / tileSize);
      const isLight = (col + row) % 2 === 0;
      ctx.fillStyle = isLight ? floorColor1 : floorColor2;
      ctx.fillRect(tx, ty, tileSize, tileSize);
      if (isLight) {
        ctx.fillStyle = 'rgba(255,255,255,0.015)';
        ctx.fillRect(tx, ty, tileSize, 1);
        ctx.fillRect(tx, ty, 1, tileSize);
      }
    }
  }
  const cx = x + w / 2;
  const cy = y + h / 2;
  const grad = ctx.createRadialGradient(cx, cy - 30, 10, cx, cy, Math.max(w, h) * 0.6);
  grad.addColorStop(0, 'rgba(255,255,240,0.04)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(x, y, w, h);
}

// ===== WEATHER WINDOWS =====
function drawWeatherWindows(ctx: CanvasRenderingContext2D, frame: number) {
  const now = new Date();
  const aestHour = (now.getUTCHours() + 10) % 24;
  const isDay = aestHour >= 6 && aestHour < 18;

  const windows = [
    { x: 30, y: 15, w: 55, h: 38 },
    { x: 130, y: 15, w: 55, h: 38 },
    { x: 380, y: 15, w: 55, h: 38 },
  ];

  for (const win of windows) {
    ctx.fillStyle = '#2a2a40';
    ctx.fillRect(win.x - 2, win.y - 2, win.w + 4, win.h + 4);

    if (isDay) {
      // Daytime sky
      const skyGrad = ctx.createLinearGradient(win.x, win.y, win.x, win.y + win.h);
      skyGrad.addColorStop(0, '#4488cc');
      skyGrad.addColorStop(1, '#6aa8dd');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(win.x, win.y, win.w, win.h);

      // Clouds drifting
      for (let i = 0; i < 3; i++) {
        const cx = ((frame * 0.15 + i * 60) % (win.w + 30)) + win.x - 15;
        const cy = win.y + 8 + i * 10;
        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        ctx.beginPath();
        ctx.ellipse(cx, cy, 10, 4, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(cx + 6, cy - 1, 7, 3, 0, 0, Math.PI * 2);
        ctx.fill();
      }
    } else {
      // Night sky
      const skyGrad = ctx.createLinearGradient(win.x, win.y, win.x, win.y + win.h);
      skyGrad.addColorStop(0, '#0a1020');
      skyGrad.addColorStop(1, '#1a2844');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(win.x, win.y, win.w, win.h);

      // Stars twinkling
      const starPositions = [
        [8, 6], [25, 12], [40, 8], [15, 22], [35, 18], [45, 28], [10, 30], [30, 5],
      ];
      for (const [sx, sy] of starPositions) {
        const twinkle = Math.sin(frame * 0.05 + sx * 0.3 + sy * 0.2);
        const alpha = 0.3 + twinkle * 0.4;
        ctx.fillStyle = `rgba(255,255,255,${Math.max(0.1, alpha)})`;
        ctx.fillRect(win.x + sx, win.y + sy, 1, 1);
      }

      // Moon
      ctx.fillStyle = '#ffffcc';
      ctx.beginPath();
      ctx.arc(win.x + win.w - 12, win.y + 12, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Window dividers
    ctx.fillStyle = '#3a3a5e';
    ctx.fillRect(win.x + win.w / 2 - 1, win.y, 2, win.h);
    ctx.fillRect(win.x, win.y + win.h / 2 - 1, win.w, 2);

    // Light spill
    ctx.fillStyle = isDay ? 'rgba(150,200,255,0.03)' : 'rgba(100,140,200,0.02)';
    ctx.fillRect(win.x - 10, win.y + win.h + 5, win.w + 20, 40);
  }
}

function drawBaseboards(ctx: CanvasRenderingContext2D) {
  ctx.fillStyle = '#2a2a40';
  ctx.fillRect(0, 256, 480, 4);
  ctx.fillRect(480, 256, 480, 4);
  ctx.fillRect(0, 516, 960, 4);
  ctx.fillRect(0, H - 4, 240, 4);
  ctx.fillRect(240, H - 4, 340, 4);
  ctx.fillRect(580, H - 4, 380, 4);
}

function drawWalls(ctx: CanvasRenderingContext2D) {
  ctx.strokeStyle = '#3a3a5e';
  ctx.lineWidth = 3;
  ctx.strokeRect(1, 1, W - 2, H - 2);

  ctx.beginPath();
  ctx.moveTo(0, 260); ctx.lineTo(W, 260);
  ctx.moveTo(0, 520); ctx.lineTo(W, 520);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(480, 0); ctx.lineTo(480, 260);
  ctx.moveTo(240, 520); ctx.lineTo(240, H);
  ctx.moveTo(580, 520); ctx.lineTo(580, H);
  ctx.stroke();

  // Glass wall for meeting room
  ctx.strokeStyle = '#6366f118';
  ctx.lineWidth = 5;
  ctx.strokeRect(4, 4, 472, 252);
}

function drawDoorways(ctx: CanvasRenderingContext2D) {
  for (const door of DOORWAYS) {
    ctx.fillStyle = '#1e1e35';
    ctx.fillRect(door.x, door.y, door.w, door.h);
    ctx.fillStyle = '#4a4a6e';
    ctx.fillRect(door.x - 2, door.y, 4, door.h);
    ctx.fillRect(door.x + door.w - 2, door.y, 4, door.h);
  }
}

function drawRoomLabel(ctx: CanvasRenderingContext2D, room: RoomDef) {
  ctx.fillStyle = '#6b728066';
  ctx.font = 'bold 10px monospace';
  ctx.textAlign = 'left';
  ctx.fillText(`${room.emoji} ${room.label}`, room.x + 8, room.y + 16);
}

// ===== WALL DECORATIONS =====
function drawWallDecorations(ctx: CanvasRenderingContext2D, frame: number) {
  ctx.fillStyle = '#2a2a3e';
  ctx.fillRect(440, 268, 80, 20);
  ctx.fillStyle = '#6366f1';
  ctx.font = 'bold 9px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('⚡ THE AGENCY', 480, 282);

  const stickyColors = ['#fbbf24', '#22c55e', '#ec4899', '#3b82f6'];
  for (let i = 0; i < 4; i++) {
    const sx = 560 + i * 22;
    ctx.fillStyle = stickyColors[i] + '44';
    ctx.fillRect(sx, 270, 16, 16);
    ctx.fillStyle = stickyColors[i] + '22';
    ctx.fillRect(sx + 2, 274, 8, 1);
    ctx.fillRect(sx + 2, 277, 10, 1);
    ctx.fillRect(sx + 2, 280, 6, 1);
  }

  drawWaterCooler(ctx, 30, 350, frame);
  drawCoatRack(ctx, 90, 485);
}

function drawWaterCooler(ctx: CanvasRenderingContext2D, x: number, y: number, frame: number) {
  ctx.fillStyle = '#d0d0e0';
  ctx.fillRect(x, y, 16, 30);
  ctx.strokeStyle = '#8888a0';
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, 16, 30);
  ctx.fillStyle = '#4488cc44';
  ctx.fillRect(x + 2, y - 12, 12, 14);
  ctx.strokeStyle = '#4488cc66';
  ctx.strokeRect(x + 2, y - 12, 12, 14);
  ctx.fillStyle = '#888';
  ctx.fillRect(x + 14, y + 10, 4, 3);
  drawShadow(ctx, x + 8, y + 32, 10, 3);
}

function drawCoatRack(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.fillStyle = '#5a4030';
  ctx.fillRect(x, y, 3, 30);
  ctx.fillStyle = '#4a3020';
  ctx.fillRect(x - 6, y + 28, 15, 4);
  ctx.fillStyle = '#888';
  ctx.fillRect(x - 4, y + 2, 4, 2);
  ctx.fillRect(x + 2, y + 2, 4, 2);
  ctx.fillStyle = '#3a3a5e';
  ctx.fillRect(x - 5, y + 4, 6, 12);
}

// ===== MEETING ROOM =====
function drawMeetingRoom(ctx: CanvasRenderingContext2D, frame: number) {
  ctx.fillStyle = '#3d321e';
  ctx.beginPath();
  ctx.ellipse(220, 130, 105, 45, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#2a2010';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.ellipse(220, 130, 105, 45, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.fillStyle = '#4a3e2833';
  ctx.beginPath();
  ctx.ellipse(220, 125, 80, 35, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = 'rgba(0,0,0,0.15)';
  ctx.beginPath();
  ctx.ellipse(220, 178, 90, 12, 0, 0, Math.PI * 2);
  ctx.fill();

  const chairPositions = [
    { x: 120, y: 100 }, { x: 220, y: 75 }, { x: 320, y: 100 },
    { x: 120, y: 160 }, { x: 220, y: 185 }, { x: 320, y: 160 },
  ];
  for (const c of chairPositions) drawPixelChair(ctx, c.x, c.y);

  // Whiteboard
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(20, 30, 120, 60);
  ctx.strokeStyle = '#666';
  ctx.lineWidth = 2;
  ctx.strokeRect(20, 30, 120, 60);
  ctx.strokeStyle = '#ccc';
  ctx.lineWidth = 1;
  ctx.strokeRect(23, 33, 114, 54);
  ctx.fillStyle = '#333';
  ctx.font = '8px monospace';
  ctx.textAlign = 'left';
  ctx.fillText('Sprint Goals:', 28, 48);
  ctx.fillStyle = '#2563eb';
  ctx.fillText('• Office v2.0', 28, 60);
  ctx.fillStyle = '#22c55e';
  ctx.fillText('• Pixel Art ✓', 28, 72);
  ctx.fillStyle = '#e0e0d0';
  ctx.fillRect(22, 90, 118, 4);
  ctx.fillStyle = '#ef4444'; ctx.fillRect(30, 90, 10, 3);
  ctx.fillStyle = '#22c55e'; ctx.fillRect(44, 90, 10, 3);
  ctx.fillStyle = '#3b82f6'; ctx.fillRect(58, 90, 10, 3);
  ctx.fillStyle = '#111';    ctx.fillRect(72, 90, 10, 3);
}

function drawPixelChair(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.fillStyle = '#4a4a5e';
  ctx.fillRect(x - 8, y - 4, 16, 10);
  ctx.strokeStyle = '#333345';
  ctx.lineWidth = 1;
  ctx.strokeRect(x - 8, y - 4, 16, 10);
  ctx.fillStyle = '#3a3a4e';
  ctx.fillRect(x - 7, y - 9, 14, 6);
  ctx.strokeStyle = '#2a2a3e';
  ctx.strokeRect(x - 7, y - 9, 14, 6);
  ctx.fillStyle = 'rgba(255,255,255,0.05)';
  ctx.fillRect(x - 7, y - 4, 14, 2);
}

// ===== SERVER ROOM (compact — 3 racks) =====
function drawServerRoom(ctx: CanvasRenderingContext2D, frame: number) {
  const baseX = 530;

  for (let i = 0; i < 3; i++) {
    const rx = baseX + i * 120;
    const ry = 40;

    ctx.fillStyle = '#2a2a3e';
    ctx.fillRect(rx, ry, 40, 180);
    ctx.strokeStyle = '#1a1a2e';
    ctx.lineWidth = 2;
    ctx.strokeRect(rx, ry, 40, 180);
    ctx.fillStyle = '#3a3a4e';
    ctx.fillRect(rx + 1, ry + 1, 38, 3);

    for (let j = 0; j < 6; j++) {
      const uy = ry + 5 + j * 28;
      ctx.fillStyle = '#111118';
      ctx.fillRect(rx + 3, uy, 34, 22);
      ctx.strokeStyle = '#222230';
      ctx.lineWidth = 1;
      ctx.strokeRect(rx + 3, uy, 34, 22);

      const pulse = (Math.sin(frame * 0.03 + i * 1.5 + j * 0.8) + 1) / 2;
      const g = Math.floor(100 + pulse * 155);
      ctx.fillStyle = `rgb(0,${g},0)`;
      ctx.fillRect(rx + 32, uy + 3, 3, 3);
      const isAlert = Math.sin(frame * 0.02 + i * 2.1) > 0.92;
      const bluePulse = (Math.sin(frame * 0.04 + i + j * 0.5) + 1) / 2;
      ctx.fillStyle = isAlert ? '#ef4444' : `rgba(59,130,246,${0.4 + bluePulse * 0.6})`;
      ctx.fillRect(rx + 32, uy + 10, 3, 3);

      ctx.fillStyle = '#1a1a28';
      for (let v = 0; v < 3; v++) {
        ctx.fillRect(rx + 5 + v * 8, uy + 16, 6, 1);
      }
    }
    drawShadow(ctx, rx + 20, ry + 182, 22, 4);
  }

  // Cables
  ctx.strokeStyle = '#4a4a6e33';
  ctx.lineWidth = 2;
  for (let i = 0; i < 2; i++) {
    ctx.beginPath();
    ctx.moveTo(baseX + i * 120 + 20, 220);
    ctx.bezierCurveTo(baseX + i * 120 + 30, 240, baseX + (i + 1) * 120 + 10, 240, baseX + (i + 1) * 120 + 20, 220);
    ctx.stroke();
  }

  // Temperature
  ctx.fillStyle = '#111118';
  ctx.fillRect(900, 40, 45, 25);
  ctx.strokeStyle = '#3a3a5e';
  ctx.lineWidth = 1;
  ctx.strokeRect(900, 40, 45, 25);
  ctx.fillStyle = '#22c55e';
  ctx.font = 'bold 10px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('22°C', 922, 57);
}

// ===== MAIN OFFICE =====
function drawMainOfficeDesks(ctx: CanvasRenderingContext2D, frame: number, agents: AgentState[]) {
  drawPixelPlant(ctx, 50, 285, frame, 0);
  drawPixelPlant(ctx, 910, 285, frame, 100);
  drawPixelPlant(ctx, 50, 455, frame, 200);
  drawPixelPlant(ctx, 910, 455, frame, 300);
  drawPixelPrinter(ctx, 920, 375);

  ctx.fillStyle = '#4a4a4a';
  ctx.fillRect(30, 400, 16, 20);
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  ctx.strokeRect(30, 400, 16, 20);
  ctx.fillStyle = '#555';
  ctx.fillRect(28, 398, 20, 4);
  ctx.strokeRect(28, 398, 20, 4);

  for (const agent of agents) {
    const desk = DESK_LAYOUT[agent.desk];
    if (!desk) continue;
    drawPixelDesk(ctx, desk.x, desk.y, agent, frame);
  }
}

function drawPixelDesk(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  drawShadow(ctx, x, y + 40, 34, 5);

  const deskDark = '#2a1f14';
  const deskBase = '#3d2b1f';
  const deskLight = '#5a4030';

  ctx.fillStyle = deskBase;
  ctx.fillRect(x - 32, y + 10, 64, 24);
  ctx.fillStyle = deskLight;
  ctx.fillRect(x - 32, y + 10, 64, 3);
  ctx.fillStyle = deskDark;
  ctx.fillRect(x - 32, y + 31, 64, 3);
  ctx.strokeStyle = '#1a1208';
  ctx.lineWidth = 1;
  ctx.strokeRect(x - 32, y + 10, 64, 24);
  ctx.fillStyle = deskDark;
  ctx.fillRect(x - 30, y + 34, 5, 10);
  ctx.fillRect(x + 25, y + 34, 5, 10);
  ctx.fillStyle = '#1a1208';
  ctx.fillRect(x - 30, y + 34, 1, 10);
  ctx.fillRect(x + 29, y + 34, 1, 10);

  ctx.fillStyle = '#333350';
  ctx.fillRect(x - 10, y + 44, 20, 12);
  ctx.fillStyle = '#3d3d5a';
  ctx.fillRect(x - 10, y + 44, 20, 2);
  ctx.fillStyle = '#2a2a40';
  ctx.fillRect(x - 8, y + 38, 16, 8);
  ctx.strokeStyle = '#222238';
  ctx.strokeRect(x - 10, y + 44, 20, 12);
  ctx.strokeRect(x - 8, y + 38, 16, 8);

  // Monitor with unique content per agent
  const monContent = MONITOR_CONTENT[agent.desk] || 'text';
  if (agent.desk === 'dev') {
    drawAnimatedMonitor(ctx, x - 16, y - 6, agent.color, frame, 'green_code');
    drawAnimatedMonitor(ctx, x + 8, y - 6, agent.color, frame, 'green_code');
  } else if (agent.desk === 'trading') {
    drawAnimatedMonitor(ctx, x - 8, y - 6, agent.color, frame, 'candle_chart');
    drawAnimatedMonitor(ctx, x + 16, y - 4, '#22c55e', frame, 'bar_chart');
  } else if (agent.desk === 'command') {
    drawAnimatedMonitor(ctx, x - 8, y - 6, agent.color, frame, 'dashboard');
    ctx.fillStyle = '#111118';
    ctx.fillRect(x + 30, y - 2, 14, 12);
    ctx.fillStyle = '#9333ea33';
    ctx.fillRect(x + 31, y - 1, 12, 10);
    ctx.fillStyle = '#333';
    ctx.fillRect(x + 35, y + 10, 4, 3);
  } else {
    drawAnimatedMonitor(ctx, x - 8, y - 6, agent.color, frame, monContent);
  }

  // Keyboard
  ctx.fillStyle = '#222';
  ctx.fillRect(x - 12, y + 18, 24, 6);
  ctx.strokeStyle = '#111';
  ctx.lineWidth = 1;
  ctx.strokeRect(x - 12, y + 18, 24, 6);
  ctx.fillStyle = '#2a2a2a';
  for (let kx = 0; kx < 5; kx++) {
    ctx.fillRect(x - 10 + kx * 5, y + 19, 3, 2);
    ctx.fillRect(x - 10 + kx * 5, y + 22, 3, 2);
  }

  // Desk items per role
  if (agent.desk === 'design') {
    ctx.fillStyle = '#8b6914';
    ctx.fillRect(x + 36, y + 5, 3, 28);
    ctx.fillStyle = '#f5f5f0';
    ctx.fillRect(x + 32, y, 14, 18);
    ctx.strokeStyle = '#ccc';
    ctx.strokeRect(x + 32, y, 14, 18);
    ctx.fillStyle = '#ec489966';
    ctx.fillRect(x + 34, y + 3, 5, 5);
    ctx.fillStyle = '#3b82f644';
    ctx.fillRect(x + 36, y + 9, 7, 4);
  }
  if (agent.desk === 'research') {
    ctx.fillStyle = '#8b4513'; ctx.fillRect(x + 28, y + 12, 18, 4);
    ctx.fillStyle = '#1e3a5f'; ctx.fillRect(x + 28, y + 8, 18, 4);
    ctx.fillStyle = '#5c1e1e'; ctx.fillRect(x + 28, y + 4, 18, 4);
    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x + 28, y + 4, 18, 12);
    ctx.fillStyle = '#f5f5f0';
    ctx.fillRect(x - 32, y + 14, 12, 8);
    ctx.fillStyle = '#ddd';
    ctx.fillRect(x - 30, y + 16, 8, 1);
    ctx.fillRect(x - 30, y + 18, 6, 1);
  }
}

// ===== ANIMATED MONITOR SCREENS (Feature 3) =====
function drawAnimatedMonitor(ctx: CanvasRenderingContext2D, x: number, y: number, color: string, frame: number, content: string) {
  ctx.fillStyle = '#111118';
  ctx.fillRect(x, y, 20, 16);
  ctx.strokeStyle = '#222230';
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, 20, 16);
  ctx.fillStyle = '#1a1a22';
  ctx.fillRect(x + 1, y + 1, 18, 1);

  // Screen bg
  ctx.fillStyle = '#0a0a12';
  ctx.fillRect(x + 2, y + 2, 16, 11);

  switch (content) {
    case 'green_code': {
      // Green code scrolling upward
      const scrollOff = Math.floor(frame * 0.4) % 16;
      ctx.fillStyle = '#22c55e88';
      for (let line = 0; line < 5; line++) {
        const lw = 3 + ((line + scrollOff) % 5) * 2.5;
        const ly = y + 3 + line * 2.2 - (scrollOff % 3) * 0.3;
        if (ly > y + 1 && ly < y + 12) {
          ctx.fillRect(x + 3, ly, lw, 1);
        }
      }
      // Bright cursor
      if (frame % 30 < 15) {
        ctx.fillStyle = '#22c55e';
        ctx.fillRect(x + 3 + ((frame * 0.2) % 10), y + 10, 2, 1);
      }
      break;
    }
    case 'candle_chart': {
      // Red/green candle chart
      for (let i = 0; i < 6; i++) {
        const h = 2 + Math.abs(Math.sin(frame * 0.015 + i * 1.3)) * 6;
        const isGreen = Math.sin(frame * 0.02 + i * 1.7) > 0;
        ctx.fillStyle = isGreen ? '#22c55e' : '#ef4444';
        ctx.fillRect(x + 3 + i * 2.2, y + 11 - h, 1, h);
        // Wick
        ctx.fillRect(x + 3 + i * 2.2, y + 11 - h - 1, 1, 1);
      }
      break;
    }
    case 'scrolling_data': {
      // White text scrolling
      const scrollY = Math.floor(frame * 0.3) % 14;
      ctx.fillStyle = '#ffffff66';
      for (let line = 0; line < 5; line++) {
        const lw = 4 + ((line + scrollY) % 4) * 2;
        const ly = y + 3 + line * 2.2;
        ctx.fillRect(x + 3, ly, lw, 1);
      }
      break;
    }
    case 'color_palette': {
      // Colored squares grid
      const palette = ['#ec4899', '#3b82f6', '#22c55e', '#eab308', '#9333ea', '#ef4444', '#06b6d4', '#f97316', '#fff'];
      for (let i = 0; i < 9; i++) {
        const px = x + 3 + (i % 3) * 5;
        const py = y + 3 + Math.floor(i / 3) * 3;
        const cIdx = (i + Math.floor(frame * 0.01)) % palette.length;
        ctx.fillStyle = palette[cIdx] + '99';
        ctx.fillRect(px, py, 4, 2);
      }
      break;
    }
    case 'bar_chart': {
      // Horizontal bars
      const barColors = ['#3b82f6', '#22c55e', '#eab308', '#ef4444', '#9333ea'];
      for (let i = 0; i < 4; i++) {
        const bw = 3 + Math.abs(Math.sin(frame * 0.012 + i * 0.7)) * 9;
        ctx.fillStyle = barColors[i % barColors.length] + '99';
        ctx.fillRect(x + 3, y + 3 + i * 2.5, bw, 1.5);
      }
      break;
    }
    case 'terminal_blink': {
      // Terminal with green text + blinking cursor
      ctx.fillStyle = '#22c55e77';
      ctx.fillRect(x + 3, y + 3, 2, 1);
      ctx.fillRect(x + 6, y + 3, 8, 1);
      ctx.fillStyle = '#22c55e55';
      ctx.fillRect(x + 3, y + 6, 10, 1);
      ctx.fillRect(x + 3, y + 9, 4, 1);
      if (frame % 40 < 20) {
        ctx.fillStyle = '#22c55e';
        ctx.fillRect(x + 8, y + 9, 2, 1);
      }
      break;
    }
    case 'shield_pulse': {
      // Shield icon that pulses
      const pulse = (Math.sin(frame * 0.06) + 1) / 2;
      ctx.fillStyle = `rgba(239,68,68,${0.3 + pulse * 0.4})`;
      // Shield shape
      ctx.beginPath();
      ctx.moveTo(x + 10, y + 3);
      ctx.lineTo(x + 15, y + 5);
      ctx.lineTo(x + 14, y + 10);
      ctx.lineTo(x + 10, y + 12);
      ctx.lineTo(x + 6, y + 10);
      ctx.lineTo(x + 5, y + 5);
      ctx.closePath();
      ctx.fill();
      // Lock
      ctx.fillStyle = '#ffffff44';
      ctx.fillRect(x + 9, y + 6, 2, 3);
      break;
    }
    case 'text_editor': {
      // Lines of text with cursor
      ctx.fillStyle = '#ffffff55';
      ctx.fillRect(x + 3, y + 3, 10, 1);
      ctx.fillRect(x + 3, y + 5, 8, 1);
      ctx.fillRect(x + 3, y + 7, 12, 1);
      ctx.fillRect(x + 3, y + 9, 6, 1);
      if (frame % 35 < 18) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x + 10, y + 9, 1, 2);
      }
      break;
    }
    case 'dashboard': {
      // Mini graphs
      ctx.fillStyle = '#9333ea55';
      for (let i = 0; i < 4; i++) {
        const h = 1 + Math.abs(Math.sin(frame * 0.02 + i)) * 3;
        ctx.fillRect(x + 3 + i * 3.5, y + 10 - h, 2, h);
      }
      // Line
      ctx.strokeStyle = '#22c55e55';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.moveTo(x + 3, y + 5);
      for (let i = 0; i < 5; i++) {
        ctx.lineTo(x + 3 + i * 3, y + 5 - Math.sin(frame * 0.03 + i) * 2);
      }
      ctx.stroke();
      break;
    }
    case 'kanban': {
      // Colored rectangles in columns
      const cols = ['#3b82f6', '#eab308', '#22c55e'];
      for (let c = 0; c < 3; c++) {
        for (let r = 0; r < 2; r++) {
          ctx.fillStyle = cols[c] + '55';
          ctx.fillRect(x + 3 + c * 5, y + 3 + r * 4, 4, 3);
        }
      }
      break;
    }
    case 'spreadsheet': {
      // Grid with tiny numbers
      ctx.strokeStyle = '#ffffff15';
      ctx.lineWidth = 0.5;
      for (let c = 0; c < 4; c++) ctx.strokeRect(x + 3 + c * 3.5, y + 3, 3.5, 8);
      for (let r = 0; r < 3; r++) ctx.strokeRect(x + 3, y + 3 + r * 2.8, 14, 2.8);
      ctx.fillStyle = '#ffffff33';
      ctx.font = '3px monospace';
      for (let c = 0; c < 3; c++) {
        for (let r = 0; r < 2; r++) {
          ctx.fillRect(x + 4 + c * 3.5, y + 4.5 + r * 2.8, 2, 1);
        }
      }
      break;
    }
    default: {
      ctx.fillStyle = color + '55';
      for (let line = 0; line < 3; line++) {
        ctx.fillRect(x + 4, y + 3 + line * 3, 8 + (line % 2) * 3, 1);
      }
    }
  }

  // Stand
  ctx.fillStyle = '#333';
  ctx.fillRect(x + 8, y + 14, 4, 4);
  ctx.fillRect(x + 5, y + 17, 10, 2);
  ctx.strokeStyle = '#222';
  ctx.strokeRect(x + 5, y + 17, 10, 2);
}

function drawPixelPrinter(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.fillStyle = '#e0e0e0';
  ctx.fillRect(x, y, 30, 18);
  ctx.strokeStyle = '#999';
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, 30, 18);
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(x + 1, y + 1, 28, 3);
  ctx.fillStyle = '#ccc';
  ctx.fillRect(x + 2, y + 4, 26, 5);
  ctx.fillStyle = '#4a4a4a';
  ctx.fillRect(x + 2, y + 10, 26, 6);
  ctx.fillStyle = '#f8f8f0';
  ctx.fillRect(x + 4, y - 4, 22, 6);
  ctx.strokeStyle = '#ddd';
  ctx.strokeRect(x + 4, y - 4, 22, 6);
  drawShadow(ctx, x + 15, y + 20, 16, 3);
}

// ===== KITCHEN =====
function drawKitchen(ctx: CanvasRenderingContext2D, frame: number) {
  const kx = 15, ky = 540;

  ctx.fillStyle = '#5a4030';
  ctx.fillRect(kx, ky + 20, 210, 14);
  ctx.fillStyle = '#6a5040';
  ctx.fillRect(kx, ky + 20, 210, 3);
  ctx.fillStyle = '#4a3020';
  ctx.fillRect(kx, ky + 31, 210, 3);
  ctx.strokeStyle = '#3a2818';
  ctx.lineWidth = 1;
  ctx.strokeRect(kx, ky + 20, 210, 14);

  // Coffee machine
  ctx.fillStyle = '#4a4a4a';
  ctx.fillRect(kx + 20, ky, 30, 24);
  ctx.strokeStyle = '#333';
  ctx.strokeRect(kx + 20, ky, 30, 24);
  ctx.fillStyle = '#555';
  ctx.fillRect(kx + 21, ky + 1, 28, 2);
  ctx.fillStyle = '#333';
  ctx.fillRect(kx + 22, ky + 4, 26, 10);
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(kx + 28, ky + 14, 10, 8);
  ctx.strokeStyle = '#ccc';
  ctx.strokeRect(kx + 28, ky + 14, 10, 8);
  ctx.fillStyle = '#8b6914';
  ctx.fillRect(kx + 29, ky + 15, 8, 5);

  for (let i = 0; i < 4; i++) {
    const sy = ky - 4 - i * 5 - Math.sin(frame * 0.06 + i) * 3;
    const sx = kx + 33 + Math.sin(frame * 0.04 + i * 1.8) * 3;
    const alpha = 0.35 - i * 0.07;
    ctx.fillStyle = `rgba(200,200,220,${alpha})`;
    ctx.fillRect(sx, sy, 2, 2);
    ctx.fillRect(sx + 1, sy - 2, 1, 2);
  }

  // Fridge
  ctx.fillStyle = '#e0e0e0';
  ctx.fillRect(kx + 160, ky - 20, 40, 60);
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(kx + 161, ky - 19, 38, 3);
  ctx.strokeStyle = '#aaa';
  ctx.lineWidth = 1;
  ctx.strokeRect(kx + 160, ky - 20, 40, 30);
  ctx.strokeRect(kx + 160, ky + 10, 40, 20);
  ctx.fillStyle = '#888';
  ctx.fillRect(kx + 196, ky - 5, 2, 10);
  ctx.fillRect(kx + 196, ky + 15, 2, 8);
  drawShadow(ctx, kx + 180, ky + 42, 22, 4);

  // Stools
  const stoolPositions = [{ x: kx + 50, y: ky + 48 }, { x: kx + 105, y: ky + 48 }];
  for (const s of stoolPositions) {
    ctx.fillStyle = '#4a4a5e';
    ctx.fillRect(s.x, s.y, 14, 6);
    ctx.strokeStyle = '#333345';
    ctx.strokeRect(s.x, s.y, 14, 6);
    ctx.fillStyle = '#3a3a4e';
    ctx.fillRect(s.x + 5, s.y + 6, 4, 10);
  }

  // Microwave
  ctx.fillStyle = '#555';
  ctx.fillRect(kx + 80, ky + 4, 24, 16);
  ctx.strokeStyle = '#444';
  ctx.strokeRect(kx + 80, ky + 4, 24, 16);
  ctx.fillStyle = '#111';
  ctx.fillRect(kx + 82, ky + 6, 14, 12);
  ctx.fillStyle = '#22c55e';
  ctx.fillRect(kx + 98, ky + 8, 3, 2);
}

// ===== GAME ROOM (now just for hanging out — no sleeping) =====
function drawGameRoom(ctx: CanvasRenderingContext2D, frame: number) {
  const gx = 260, gy = 540;

  // Ping pong table
  ctx.fillStyle = '#1e5c3a';
  ctx.fillRect(gx + 30, gy + 20, 100, 55);
  ctx.fillStyle = '#24704a';
  ctx.fillRect(gx + 31, gy + 21, 98, 3);
  ctx.strokeStyle = '#0f3a20';
  ctx.lineWidth = 2;
  ctx.strokeRect(gx + 30, gy + 20, 100, 55);
  ctx.fillStyle = '#ffffff44';
  ctx.fillRect(gx + 78, gy + 20, 4, 55);
  ctx.strokeStyle = '#ffffff66';
  ctx.lineWidth = 1;
  ctx.strokeRect(gx + 32, gy + 22, 96, 51);
  ctx.fillStyle = '#333';
  ctx.fillRect(gx + 34, gy + 75, 4, 8);
  ctx.fillRect(gx + 122, gy + 75, 4, 8);
  drawShadow(ctx, gx + 80, gy + 85, 50, 5);

  // Arcade cabinet
  ctx.fillStyle = '#1a1a3e';
  ctx.fillRect(gx + 180, gy, 35, 60);
  ctx.strokeStyle = '#111128';
  ctx.lineWidth = 1;
  ctx.strokeRect(gx + 180, gy, 35, 60);
  ctx.fillStyle = '#2a2a5e';
  ctx.fillRect(gx + 181, gy + 1, 33, 3);
  ctx.fillStyle = '#111';
  ctx.fillRect(gx + 183, gy + 5, 29, 22);
  const glowColor = `hsl(${(frame * 2) % 360}, 70%, 50%)`;
  ctx.fillStyle = glowColor + '55';
  ctx.fillRect(gx + 185, gy + 7, 25, 18);
  ctx.fillStyle = '#ef4444';
  ctx.fillRect(gx + 194, gy + 35, 5, 5);
  ctx.strokeStyle = '#aa2222';
  ctx.strokeRect(gx + 194, gy + 35, 5, 5);
  ctx.fillStyle = '#3b82f6';
  ctx.fillRect(gx + 202, gy + 37, 4, 4);
  ctx.fillStyle = '#22c55e';
  ctx.fillRect(gx + 208, gy + 36, 4, 4);
  drawShadow(ctx, gx + 197, gy + 62, 18, 4);

  // Beanbags for sitting (NOT sleeping)
  const beanbagDefs = [
    { x: gx + 260, y: gy + 50, color: '#4a2060' },
    { x: gx + 300, y: gy + 60, color: '#203060' },
    { x: gx + 270, y: gy + 100, color: '#205030' },
  ];
  for (const bb of beanbagDefs) drawPixelBeanbag(ctx, bb.x, bb.y, bb.color);

  // TV
  ctx.fillStyle = '#111118';
  ctx.fillRect(gx + 240, gy - 10, 60, 35);
  ctx.strokeStyle = '#222230';
  ctx.lineWidth = 2;
  ctx.strokeRect(gx + 240, gy - 10, 60, 35);
  ctx.fillStyle = '#1a1a2e';
  ctx.fillRect(gx + 243, gy - 7, 54, 29);
  for (let i = 0; i < 15; i++) {
    const nx = gx + 245 + Math.floor(Math.random() * 50);
    const ny = gy - 5 + Math.floor(Math.random() * 25);
    ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.12})`;
    ctx.fillRect(nx, ny, 2, 2);
  }
  ctx.fillStyle = '#333';
  ctx.fillRect(gx + 265, gy + 25, 10, 4);
}

// ===== REST ROOM (NEW) — beds/couches, dim lighting, moon/stars decal =====
function drawRestRoom(ctx: CanvasRenderingContext2D, frame: number) {
  const rx = 580, ry = 520;

  // Dim ambient overlay for rest room
  ctx.fillStyle = 'rgba(0,0,15,0.3)';
  ctx.fillRect(rx, ry, 380, 200);

  // Warm dim light from center
  const grad = ctx.createRadialGradient(rx + 190, ry + 100, 10, rx + 190, ry + 100, 180);
  grad.addColorStop(0, 'rgba(100,80,140,0.08)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(rx, ry, 380, 200);

  // Moon/stars decal on back wall
  // Moon
  ctx.fillStyle = '#ffffcc33';
  ctx.beginPath();
  ctx.arc(rx + 320, ry + 30, 14, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffffcc22';
  ctx.beginPath();
  ctx.arc(rx + 320, ry + 30, 10, 0, Math.PI * 2);
  ctx.fill();

  // Stars on wall
  const starData = [
    [40, 20], [80, 15], [120, 25], [160, 12], [200, 22],
    [250, 18], [100, 35], [180, 38], [60, 40], [280, 28],
    [140, 10], [220, 32], [300, 20], [340, 35],
  ];
  for (const [sx, sy] of starData) {
    const twinkle = Math.sin(frame * 0.04 + sx * 0.2 + sy * 0.3);
    const alpha = 0.15 + twinkle * 0.15;
    ctx.fillStyle = `rgba(200,200,255,${Math.max(0.05, alpha)})`;
    ctx.fillRect(rx + sx, ry + sy, 1, 1);
  }

  // Beds/couches — horizontal dark shapes
  const beds = [
    { x: rx + 20, y: ry + 55, w: 55, h: 20, color: '#2a2040' },
    { x: rx + 100, y: ry + 50, w: 55, h: 20, color: '#203040' },
    { x: rx + 180, y: ry + 55, w: 55, h: 20, color: '#2a2a35' },
    { x: rx + 260, y: ry + 50, w: 55, h: 20, color: '#352a30' },
    { x: rx + 40, y: ry + 110, w: 55, h: 20, color: '#253040' },
    { x: rx + 130, y: ry + 115, w: 55, h: 20, color: '#302a40' },
    { x: rx + 220, y: ry + 110, w: 55, h: 20, color: '#2a3035' },
    { x: rx + 310, y: ry + 115, w: 55, h: 20, color: '#352530' },
    { x: rx + 60, y: ry + 160, w: 55, h: 20, color: '#253535' },
    { x: rx + 160, y: ry + 165, w: 55, h: 20, color: '#302540' },
    { x: rx + 270, y: ry + 160, w: 55, h: 20, color: '#2a3530' },
  ];
  for (const bed of beds) {
    ctx.fillStyle = bed.color;
    ctx.fillRect(bed.x, bed.y, bed.w, bed.h);
    ctx.strokeStyle = lightenColor(bed.color, 0.2);
    ctx.lineWidth = 0.5;
    ctx.strokeRect(bed.x, bed.y, bed.w, bed.h);
    // Pillow
    ctx.fillStyle = lightenColor(bed.color, 0.4) + '44';
    ctx.fillRect(bed.x + 2, bed.y + 2, 12, bed.h - 4);
  }

  // Night light (soft purple glow)
  const nlGrad = ctx.createRadialGradient(rx + 350, ry + 170, 2, rx + 350, ry + 170, 30);
  nlGrad.addColorStop(0, 'rgba(147,51,234,0.15)');
  nlGrad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = nlGrad;
  ctx.fillRect(rx + 320, ry + 140, 60, 60);
  // Night light device
  ctx.fillStyle = '#2a1a3e';
  ctx.fillRect(rx + 348, ry + 168, 6, 8);
  const nlPulse = (Math.sin(frame * 0.03) + 1) / 2;
  ctx.fillStyle = `rgba(147,51,234,${0.3 + nlPulse * 0.4})`;
  ctx.fillRect(rx + 349, ry + 169, 4, 4);
}

function drawPixelBeanbag(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  drawShadow(ctx, x, y + 14, 20, 5);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.ellipse(x, y, 18, 12, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = darkenColor(color, 0.4);
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.ellipse(x, y, 18, 12, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.fillStyle = lightenColor(color, 0.3) + '44';
  ctx.beginPath();
  ctx.ellipse(x, y - 4, 12, 6, 0, 0, Math.PI * 2);
  ctx.fill();
}

// ===== PLANT =====
function drawPixelPlant(ctx: CanvasRenderingContext2D, x: number, y: number, frame: number, offset: number) {
  const sway = Math.sin(frame * 0.012 + offset * 0.01) * 1.5;
  drawShadow(ctx, x + 8, y + 30, 10, 3);
  ctx.fillStyle = '#8b4513';
  ctx.fillRect(x, y + 16, 16, 12);
  ctx.fillStyle = '#a0522d';
  ctx.fillRect(x - 2, y + 14, 20, 4);
  ctx.strokeStyle = '#6b3410';
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y + 16, 16, 12);
  ctx.fillStyle = '#3a2210';
  ctx.fillRect(x + 2, y + 15, 12, 3);
  ctx.fillStyle = '#166534';
  ctx.fillRect(x + 7, y + 4, 3, 12);
  ctx.fillStyle = '#22c55e';
  ctx.fillRect(x + 2 + sway, y - 1, 12, 5);
  ctx.fillRect(x - 2 + sway, y + 3, 7, 4);
  ctx.fillRect(x + 11 + sway, y + 2, 7, 4);
  ctx.fillStyle = '#4ade80';
  ctx.fillRect(x + 4 + sway, y, 4, 2);
  ctx.fillRect(x + 12 + sway, y + 3, 3, 2);
  ctx.fillStyle = '#16a34a';
  ctx.fillRect(x + 2 + sway, y + 2, 3, 3);
}

// ===== CLOCK =====
function drawClock(ctx: CanvasRenderingContext2D) {
  const now = new Date();
  const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Australia/Sydney' });
  ctx.fillStyle = '#111118';
  ctx.fillRect(380, 268, 50, 18);
  ctx.strokeStyle = '#3a3a5e';
  ctx.lineWidth = 1;
  ctx.strokeRect(380, 268, 50, 18);
  ctx.fillStyle = '#e0e0e0';
  ctx.font = 'bold 10px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(timeStr, 405, 281);
}

// ===== DAY/NIGHT =====
function drawDayNightOverlay(ctx: CanvasRenderingContext2D) {
  const now = new Date();
  const aestHour = (now.getUTCHours() + 10) % 24;

  if (aestHour >= 22 || aestHour < 6) {
    ctx.fillStyle = 'rgba(0,0,20,0.25)';
    ctx.fillRect(0, 0, W, H);
    const lamps = [{ x: 100, y: 300 }, { x: 380, y: 300 }, { x: 660, y: 300 }];
    for (const lamp of lamps) {
      const grad = ctx.createRadialGradient(lamp.x, lamp.y, 5, lamp.x, lamp.y, 60);
      grad.addColorStop(0, 'rgba(255,200,100,0.12)');
      grad.addColorStop(1, 'rgba(255,200,100,0)');
      ctx.fillStyle = grad;
      ctx.fillRect(lamp.x - 60, lamp.y - 60, 120, 120);
    }
  } else if (aestHour >= 18 || aestHour < 7) {
    ctx.fillStyle = 'rgba(0,0,20,0.1)';
    ctx.fillRect(0, 0, W, H);
  }
}

// ===== AMBIENT =====
function drawAmbient(ctx: CanvasRenderingContext2D, frame: number) {
  if (frame % 180 < 90) {
    ctx.fillStyle = 'rgba(99,102,241,0.015)';
    ctx.fillRect(2, 2, 476, 256);
  }
}

// ===== MINI-MAP (Feature 6) =====
function drawMiniMap(ctx: CanvasRenderingContext2D, agents: AgentState[], animMap: Map<string, AnimAgent>) {
  const mx = 10, my = H - 100, mw = 120, mh = 90;
  const scaleX = mw / W;
  const scaleY = mh / H;

  // Background
  ctx.fillStyle = 'rgba(10,10,20,0.75)';
  ctx.fillRect(mx, my, mw, mh);
  ctx.strokeStyle = '#3a3a5e';
  ctx.lineWidth = 1;
  ctx.strokeRect(mx, my, mw, mh);

  // Room outlines
  ctx.strokeStyle = '#4a4a6e55';
  ctx.lineWidth = 0.5;
  for (const room of ROOMS) {
    ctx.strokeRect(
      mx + room.x * scaleX,
      my + room.y * scaleY,
      room.w * scaleX,
      room.h * scaleY,
    );
  }

  // Agent dots
  for (const agent of agents) {
    const anim = animMap.get(agent.id);
    if (!anim) continue;
    ctx.fillStyle = agent.color;
    ctx.beginPath();
    ctx.arc(mx + anim.x * scaleX, my + anim.y * scaleY, 2, 0, Math.PI * 2);
    ctx.fill();
  }
}

// ===== 48x48 AGENT SPRITES =====

const SKIN_BASE = '#f0d0a0';
const SKIN_LIGHT = '#ffe0b8';
const SKIN_DARK = '#d0a870';
const OUTLINE = '#1a1018';

function drawAgent48(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, anim: AnimAgent, frame: number) {
  const { state } = anim;
  const f = frame + anim.idleOffset;

  if (state === 'sleeping') { drawSleepingAgent(ctx, x, y, agent, f); return; }
  if (state === 'walking') { drawWalkingAgent(ctx, x, y, agent, anim, f); return; }
  if (state === 'coffee') { drawCoffeeAgent(ctx, x, y, agent, f); return; }
  if (state === 'meeting') { drawMeetingAgent(ctx, x, y, agent, f); return; }
  if (state === 'sitting') { drawSittingAgent(ctx, x, y, agent, f); return; }
  drawStandingAgent(ctx, x, y, agent, f);
}

function drawPixelHead(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number, lookDir: number) {
  const hw = 14, hh = 14;
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - hw/2 - 1, y - 1, hw + 2, hh + 2);
  ctx.fillStyle = SKIN_BASE;
  ctx.fillRect(x - hw/2, y, hw, hh);
  ctx.fillStyle = SKIN_DARK;
  ctx.fillRect(x + hw/2 - 3, y + 1, 3, hh - 2);
  ctx.fillStyle = SKIN_LIGHT;
  ctx.fillRect(x - hw/2, y + 1, 2, 4);

  drawHair(ctx, x, y, agent, hw, hh);

  const blink = frame % 200 < 4;
  const eyeY = y + 6;
  const eyeOffset = lookDir * 1;

  if (!blink) {
    ctx.fillStyle = '#111';
    ctx.fillRect(x - 4 + eyeOffset, eyeY, 3, 3);
    ctx.fillRect(x + 2 + eyeOffset, eyeY, 3, 3);
    ctx.fillStyle = '#fff';
    ctx.fillRect(x - 3 + eyeOffset, eyeY, 1, 1);
    ctx.fillRect(x + 3 + eyeOffset, eyeY, 1, 1);
  } else {
    ctx.fillStyle = '#111';
    ctx.fillRect(x - 4 + eyeOffset, eyeY + 1, 3, 1);
    ctx.fillRect(x + 2 + eyeOffset, eyeY + 1, 3, 1);
  }
}

function drawHair(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, hw: number, _hh: number) {
  const hairDark = darkenColor(agent.color, 0.5);
  const hairBase = darkenColor(agent.color, 0.3);
  const hairLight = darkenColor(agent.color, 0.1);

  switch (agent.id) {
    case 'main':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 4, hw + 2, 7);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 3, hw, 5);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - hw/2 + 2, y - 3, 4, 2);
      break;
    case 'dev':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 4, hw + 2, 6);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 3, hw, 4);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - 5, y - 6, 3, 3);
      ctx.fillRect(x + 1, y - 7, 3, 4);
      ctx.fillRect(x - 2, y - 5, 3, 2);
      break;
    case 'trader':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 3, hw + 3, 5);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 2, hw, 3);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - hw/2 + 1, y - 2, 3, 1);
      break;
    case 'research':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 2, y - 5, hw + 4, 8);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2 - 1, y - 4, hw + 2, 6);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - 3, y - 4, 2, 2);
      ctx.fillRect(x + 2, y - 3, 2, 2);
      break;
    case 'creative':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 4, hw + 2, 6);
      ctx.fillRect(x - hw/2 - 2, y, 3, 10);
      ctx.fillRect(x + hw/2, y, 3, 10);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 3, hw, 4);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - 2, y - 3, 5, 2);
      break;
    case 'audit':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2, y - 2, hw, 4);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2 + 1, y - 1, hw - 2, 2);
      break;
    case 'social':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 4, hw + 2, 6);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 3, hw, 4);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - 5, y - 5, 4, 2);
      ctx.fillRect(x + 2, y - 5, 4, 2);
      break;
    case 'growth':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 5, hw + 2, 3);
      ctx.fillRect(x - hw/2, y - 2, hw, 4);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 4, hw, 2);
      break;
    case 'rook':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - 3, y - 7, 6, 4);
      ctx.fillRect(x - hw/2, y - 3, hw, 5);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - 2, y - 6, 4, 3);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x - 1, y - 6, 2, 2);
      break;
    case 'pm':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 3, hw + 2, 5);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 2, hw, 3);
      ctx.fillStyle = SKIN_DARK;
      ctx.fillRect(x - 2, y - 2, 1, 3);
      ctx.fillStyle = hairLight;
      ctx.fillRect(x + 1, y - 2, 4, 1);
      break;
    case 'finance':
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2, y - 2, hw, 4);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2 + 2, y - 1, hw - 4, 2);
      break;
    default:
      ctx.fillStyle = hairDark;
      ctx.fillRect(x - hw/2 - 1, y - 4, hw + 2, 6);
      ctx.fillStyle = hairBase;
      ctx.fillRect(x - hw/2, y - 3, hw, 4);
  }
}

function drawPixelBody(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState) {
  const color = agent.color;
  const dark = darkenColor(color, 0.3);
  const light = lightenColor(color, 0.2);
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 8, y - 1, 16, 16);
  ctx.fillStyle = color;
  ctx.fillRect(x - 7, y, 14, 14);
  ctx.fillStyle = dark;
  ctx.fillRect(x + 4, y + 1, 3, 12);
  ctx.fillStyle = light;
  ctx.fillRect(x - 7, y, 3, 4);
  ctx.fillStyle = light;
  ctx.fillRect(x - 3, y, 6, 2);
}

function drawPixelLegs(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 6, y - 1, 5, 11);
  ctx.fillRect(x + 1, y - 1, 5, 11);
  ctx.fillStyle = '#2a2a3e';
  ctx.fillRect(x - 5, y, 4, 10);
  ctx.fillRect(x + 2, y, 4, 10);
  ctx.fillStyle = '#1e1e30';
  ctx.fillRect(x - 2, y, 1, 10);
  ctx.fillRect(x + 5, y + 2, 1, 6);
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 7, y + 9, 6, 4);
  ctx.fillRect(x + 1, y + 9, 6, 4);
  ctx.fillStyle = '#333348';
  ctx.fillRect(x - 6, y + 10, 5, 2);
  ctx.fillRect(x + 2, y + 10, 5, 2);
  ctx.fillStyle = '#444460';
  ctx.fillRect(x - 6, y + 10, 3, 1);
  ctx.fillRect(x + 2, y + 10, 3, 1);
}

function drawPixelArms(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, leftDy: number, rightDy: number) {
  const color = agent.color;
  const dark = darkenColor(color, 0.3);
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 13, y + leftDy - 1, 6, 12);
  ctx.fillStyle = color;
  ctx.fillRect(x - 12, y + leftDy, 4, 10);
  ctx.fillStyle = dark;
  ctx.fillRect(x - 9, y + leftDy + 2, 1, 6);
  ctx.fillStyle = SKIN_BASE;
  ctx.fillRect(x - 12, y + leftDy + 9, 4, 3);
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x + 7, y + rightDy - 1, 6, 12);
  ctx.fillStyle = color;
  ctx.fillRect(x + 8, y + rightDy, 4, 10);
  ctx.fillStyle = dark;
  ctx.fillRect(x + 11, y + rightDy + 2, 1, 6);
  ctx.fillStyle = SKIN_BASE;
  ctx.fillRect(x + 8, y + rightDy + 9, 4, 3);
}

// ===== POSE DRAWS =====

function drawSittingAgent(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  const bob = agent.status === 'active' ? Math.sin(frame * 0.08) * 1 : Math.sin(frame * 0.02) * 0.3;
  const dy = y - 20 + bob;
  drawPixelBody(ctx, x, dy + 6, agent);
  drawPixelHead(ctx, x, dy - 8, agent, frame, 0);
  if (agent.status === 'active') {
    const armBob = Math.sin(frame * 0.15) > 0 ? 1 : -1;
    drawPixelArms(ctx, x, dy + 4, agent, armBob, -armBob);
  } else {
    drawPixelArms(ctx, x, dy + 4, agent, 0, 0);
  }
  drawAccessory(ctx, x, dy - 2, agent, frame);
  drawStatusDot(ctx, x + 9, dy - 9, agent.status, frame);
  drawAgentName(ctx, x, y + 28, agent.name, agent.status);
  if (agent.status === 'active' && agent.currentTask) {
    drawSpeechBubble(ctx, x, dy - 22, agent.currentTask.substring(0, 28));
  }
}

function drawStandingAgent(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  const shift = Math.sin(frame * 0.025) * 0.8;
  const dx = x + shift;
  drawPixelLegs(ctx, dx, y + 18);
  drawPixelBody(ctx, dx, y + 4, agent);
  drawPixelHead(ctx, dx, y - 10, agent, frame, 0);
  drawPixelArms(ctx, dx, y + 2, agent, 0, 0);
  drawAccessory(ctx, dx, y - 4, agent, frame);
  drawStatusDot(ctx, dx + 9, y - 11, agent.status, frame);
  drawAgentName(ctx, x, y + 34, agent.name, agent.status);
}

function drawWalkingAgent(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, anim: AnimAgent, frame: number) {
  const walkPhase = (anim.walkFrame % 40) / 40;
  const legSwing = Math.sin(walkPhase * Math.PI * 2) * 4;
  const armSwing = Math.sin(walkPhase * Math.PI * 2) * 3;
  const headBob = Math.abs(Math.sin(walkPhase * Math.PI * 2)) * 1.5;
  const lookDir = anim.targetX > anim.x ? 1 : -1;
  const dy = y - headBob;

  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 6, y + 17 - Math.max(0, legSwing), 5, 10 + Math.max(0, legSwing));
  ctx.fillRect(x + 1, y + 17 + Math.max(0, -legSwing), 5, 10 - Math.max(0, -legSwing));
  ctx.fillStyle = '#2a2a3e';
  ctx.fillRect(x - 5, y + 18 - Math.max(0, legSwing), 4, 8 + Math.max(0, legSwing));
  ctx.fillRect(x + 2, y + 18 + Math.max(0, -legSwing), 4, 8 - Math.max(0, -legSwing));
  ctx.fillStyle = '#333348';
  ctx.fillRect(x - 7, y + 26, 6, 3);
  ctx.fillRect(x + 1, y + 26, 6, 3);

  drawPixelBody(ctx, x, dy + 4, agent);
  drawPixelHead(ctx, x, dy - 10, agent, frame, lookDir);
  drawPixelArms(ctx, x, dy + 2, agent, -armSwing, armSwing);
  drawAccessory(ctx, x, dy - 4, agent, frame);
  drawAgentName(ctx, x, y + 34, agent.name, agent.status);
}

function drawSleepingAgent(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  const breathe = Math.sin(frame * 0.03) * 0.5;

  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 13, y - 1 + breathe, 26, 12);
  ctx.fillStyle = agent.color;
  ctx.fillRect(x - 12, y + breathe, 24, 10);
  ctx.fillStyle = darkenColor(agent.color, 0.3);
  ctx.fillRect(x - 12, y + 7 + breathe, 24, 3);

  // Blanket
  ctx.fillStyle = 'rgba(40,40,80,0.5)';
  ctx.fillRect(x - 10, y + 2 + breathe, 20, 8);

  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 18, y - 5 + breathe, 12, 11);
  ctx.fillStyle = SKIN_BASE;
  ctx.fillRect(x - 17, y - 4 + breathe, 10, 9);
  ctx.fillStyle = SKIN_DARK;
  ctx.fillRect(x - 9, y - 3 + breathe, 2, 7);
  ctx.fillStyle = '#111';
  ctx.fillRect(x - 15, y + breathe, 3, 1);
  ctx.fillRect(x - 11, y + breathe, 3, 1);

  const hairDark = darkenColor(agent.color, 0.5);
  ctx.fillStyle = hairDark;
  ctx.fillRect(x - 18, y - 7 + breathe, 12, 4);

  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x + 7, y + 3 + breathe, 10, 6);
  ctx.fillStyle = '#2a2a3e';
  ctx.fillRect(x + 8, y + 4 + breathe, 8, 4);

  // ZZZ with unique offset per agent
  const zFloat = Math.sin(frame * 0.04) * 3;
  ctx.fillStyle = '#9ca3af55';
  ctx.font = '8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('z', x - 12, y - 10 + zFloat);
  ctx.font = '10px monospace';
  ctx.fillText('z', x - 7, y - 18 + zFloat * 0.7);
  ctx.font = '12px monospace';
  ctx.fillStyle = '#9ca3af44';
  ctx.fillText('Z', x - 2, y - 26 + zFloat * 0.5);

  ctx.fillStyle = '#4b5563';
  ctx.font = 'bold 8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(agent.name, x, y + 20);
}

function drawCoffeeAgent(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  const shift = Math.sin(frame * 0.02) * 0.4;
  drawPixelLegs(ctx, x, y + 18);
  drawPixelBody(ctx, x, y + 4 + shift, agent);
  drawPixelHead(ctx, x, y - 10 + shift, agent, frame, 0);
  ctx.fillStyle = '#111';
  ctx.fillRect(x - 2, y - 2 + shift, 4, 1);

  const color = agent.color;
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x - 13, y + 5 + shift, 6, 12);
  ctx.fillStyle = color;
  ctx.fillRect(x - 12, y + 6 + shift, 4, 10);
  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x + 7, y + 3 + shift, 6, 10);
  ctx.fillStyle = color;
  ctx.fillRect(x + 8, y + 4 + shift, 4, 8);

  ctx.fillStyle = OUTLINE;
  ctx.fillRect(x + 11, y + 5 + shift, 9, 9);
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(x + 12, y + 6 + shift, 7, 7);
  ctx.fillStyle = '#8b6914';
  ctx.fillRect(x + 13, y + 7 + shift, 5, 4);
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(x + 19, y + 7 + shift, 2, 2);
  ctx.fillRect(x + 20, y + 9 + shift, 2, 2);
  ctx.fillRect(x + 19, y + 10 + shift, 2, 2);

  for (let i = 0; i < 3; i++) {
    const sy = y + 1 - i * 5 + shift - Math.sin(frame * 0.05 + i) * 2;
    const sx = x + 15 + Math.sin(frame * 0.03 + i * 1.5) * 2;
    ctx.fillStyle = `rgba(200,200,220,${0.3 - i * 0.08})`;
    ctx.fillRect(sx, sy, 2, 2);
  }

  drawSpeechBubble(ctx, x, y - 24, '☕ break');
  drawAccessory(ctx, x, y - 4 + shift, agent, frame);
  drawAgentName(ctx, x, y + 34, agent.name, agent.status);
}

function drawMeetingAgent(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  const gesturing = Math.sin(frame * 0.06 + x * 0.1) > 0.6;
  const bob = Math.sin(frame * 0.035) * 0.4;
  const dy = y + bob;

  ctx.fillStyle = '#2a2a3e';
  ctx.fillRect(x - 5, dy + 16, 4, 6);
  ctx.fillRect(x + 1, dy + 16, 4, 6);

  drawPixelBody(ctx, x, dy + 4, agent);
  drawPixelHead(ctx, x, dy - 8, agent, frame, 0);

  if (gesturing) {
    ctx.fillStyle = OUTLINE;
    ctx.fillRect(x - 15, dy, 6, 10);
    ctx.fillStyle = agent.color;
    ctx.fillRect(x - 14, dy + 1, 4, 8);
    ctx.fillStyle = SKIN_BASE;
    ctx.fillRect(x - 14, dy - 1, 4, 3);
    ctx.fillStyle = OUTLINE;
    ctx.fillRect(x + 7, dy + 5, 6, 10);
    ctx.fillStyle = agent.color;
    ctx.fillRect(x + 8, dy + 6, 4, 8);
  } else {
    drawPixelArms(ctx, x, dy + 2, agent, 0, 0);
  }

  drawAccessory(ctx, x, dy - 2, agent, frame);
  drawStatusDot(ctx, x + 9, dy - 9, agent.status, frame);
  drawAgentName(ctx, x, y + 30, agent.name, agent.status);
}

// ===== ACCESSORIES =====
function drawAccessory(ctx: CanvasRenderingContext2D, x: number, y: number, agent: AgentState, frame: number) {
  const acc = agent.accessory;
  const color = agent.color;

  switch (acc) {
    case 'crown': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 7, y - 14, 15, 8);
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(x - 6, y - 10, 12, 4);
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(x - 6, y - 12, 12, 2);
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(x - 7, y - 15, 3, 5);
      ctx.fillRect(x - 1, y - 16, 3, 6);
      ctx.fillRect(x + 5, y - 15, 3, 5);
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(x - 1, y - 13, 2, 2);
      ctx.fillStyle = '#3b82f6';
      ctx.fillRect(x - 5, y - 11, 2, 2);
      ctx.fillStyle = '#22c55e';
      ctx.fillRect(x + 4, y - 11, 2, 2);
      break;
    }
    case 'glasses': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 6, y - 5, 6, 5);
      ctx.fillRect(x + 1, y - 5, 6, 5);
      ctx.fillRect(x, y - 3, 1, 2);
      ctx.fillStyle = '#94a3b8';
      ctx.fillRect(x - 5, y - 4, 4, 3);
      ctx.fillRect(x + 2, y - 4, 4, 3);
      ctx.fillStyle = '#94a3b833';
      ctx.fillRect(x - 4, y - 4, 2, 1);
      ctx.fillRect(x + 3, y - 4, 2, 1);
      break;
    }
    case 'hat': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 9, y - 9, 18, 4);
      ctx.fillRect(x - 6, y - 15, 12, 7);
      ctx.fillStyle = color;
      ctx.fillRect(x - 8, y - 8, 16, 2);
      ctx.fillRect(x - 5, y - 14, 10, 6);
      ctx.fillStyle = lightenColor(color, 0.3);
      ctx.fillRect(x - 5, y - 14, 10, 2);
      break;
    }
    case 'badge': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 10, y + 4, 8, 7);
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(x - 9, y + 5, 6, 5);
      ctx.fillStyle = '#111';
      ctx.fillRect(x - 7, y + 6, 2, 2);
      break;
    }
    case 'headphones': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 9, y - 6, 4, 9);
      ctx.fillRect(x + 6, y - 6, 4, 9);
      ctx.fillRect(x - 8, y - 10, 16, 4);
      ctx.fillStyle = '#444';
      ctx.fillRect(x - 8, y - 5, 3, 7);
      ctx.fillRect(x + 6, y - 5, 3, 7);
      ctx.fillStyle = '#555';
      ctx.fillRect(x - 7, y - 9, 14, 2);
      ctx.fillStyle = '#666';
      ctx.fillRect(x - 9, y - 3, 4, 4);
      ctx.fillRect(x + 6, y - 3, 4, 4);
      break;
    }
    case 'scarf': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 9, y + 3, 18, 5);
      ctx.fillRect(x - 10, y + 8, 5, 7);
      ctx.fillStyle = color;
      ctx.fillRect(x - 8, y + 4, 16, 3);
      ctx.fillRect(x - 9, y + 9, 3, 5);
      ctx.fillStyle = darkenColor(color, 0.3);
      ctx.fillRect(x - 8, y + 5, 16, 1);
      ctx.fillStyle = lightenColor(color, 0.3);
      ctx.fillRect(x - 8, y + 4, 8, 1);
      break;
    }
    case 'cap': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 7, y - 11, 14, 5);
      ctx.fillRect(x + 4, y - 10, 8, 4);
      ctx.fillStyle = color;
      ctx.fillRect(x - 6, y - 10, 12, 3);
      ctx.fillRect(x + 5, y - 9, 6, 2);
      ctx.fillStyle = lightenColor(color, 0.3);
      ctx.fillRect(x - 6, y - 10, 6, 1);
      break;
    }
    case 'bowtie': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 7, y + 1, 14, 7);
      ctx.fillStyle = '#ec4899';
      ctx.fillRect(x - 6, y + 2, 5, 5);
      ctx.fillRect(x + 1, y + 2, 5, 5);
      ctx.fillStyle = darkenColor('#ec4899', 0.3);
      ctx.fillRect(x - 1, y + 3, 2, 3);
      break;
    }
    case 'visor': {
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 7, y - 5, 14, 5);
      ctx.fillStyle = '#22c55e66';
      ctx.fillRect(x - 6, y - 4, 12, 3);
      ctx.fillStyle = '#22c55e33';
      ctx.fillRect(x - 5, y - 3, 10, 1);
      break;
    }
    case 'antenna': {
      ctx.fillStyle = '#6b7280';
      ctx.fillRect(x, y - 16, 2, 8);
      ctx.fillStyle = OUTLINE;
      ctx.fillRect(x - 1, y - 19, 4, 4);
      const pulse = (Math.sin(frame * 0.08) + 1) / 2;
      ctx.fillStyle = `rgba(239,68,68,${0.5 + pulse * 0.5})`;
      ctx.fillRect(x, y - 18, 2, 2);
      break;
    }
    case 'monocle': {
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(x + 3, y - 1, 4, 0, Math.PI * 2);
      ctx.stroke();
      ctx.strokeStyle = '#fbbf2466';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x + 7, y + 1);
      ctx.lineTo(x + 9, y + 8);
      ctx.stroke();
      ctx.fillStyle = '#fbbf2422';
      ctx.beginPath();
      ctx.arc(x + 3, y - 1, 3, 0, Math.PI * 2);
      ctx.fill();
      break;
    }
  }
}

// ===== SPEECH BUBBLE =====
function drawSpeechBubble(ctx: CanvasRenderingContext2D, x: number, y: number, text: string) {
  const w = Math.min(text.length * 5 + 14, 150);
  const bx = x - w / 2;
  const by = y - 14;
  ctx.fillStyle = '#1a1a2eDD';
  ctx.strokeStyle = '#4a4a6e';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(bx, by, w, 14, 3);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = '#1a1a2eDD';
  ctx.beginPath();
  ctx.moveTo(x - 3, by + 14);
  ctx.lineTo(x, by + 18);
  ctx.lineTo(x + 3, by + 14);
  ctx.fill();
  ctx.fillStyle = '#d0d0d0';
  ctx.font = '7px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(text, x, by + 10);
}

// ===== STATUS DOT =====
function drawStatusDot(ctx: CanvasRenderingContext2D, x: number, y: number, status: string, frame: number) {
  const color = status === 'active' ? '#22c55e' : status === 'idle' ? '#eab308' : '#4b5563';
  if (status === 'active') {
    const pulse = (Math.sin(frame * 0.06) + 1) / 2;
    ctx.fillStyle = `rgba(34,197,94,${0.1 + pulse * 0.15})`;
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.fillStyle = OUTLINE;
  ctx.beginPath();
  ctx.arc(x, y, 4.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, 3.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = 'rgba(255,255,255,0.3)';
  ctx.fillRect(x - 1, y - 2, 2, 1);
}

// ===== AGENT NAME =====
function drawAgentName(ctx: CanvasRenderingContext2D, x: number, y: number, name: string, status: string) {
  const w = name.length * 5.5 + 6;
  ctx.fillStyle = 'rgba(10,10,15,0.6)';
  ctx.beginPath();
  ctx.roundRect(x - w/2, y - 7, w, 10, 3);
  ctx.fill();
  ctx.fillStyle = status === 'offline' ? '#4b5563' : '#d0d0d0';
  ctx.font = 'bold 8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(name, x, y);
}