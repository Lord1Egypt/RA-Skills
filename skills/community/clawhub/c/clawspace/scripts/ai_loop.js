/**
 * AI Loop - Bridge-embedded game AI agent
 * 
 * Features:
 * - Continuous decision loop (every N ms)
 * - Short-term memory (last 10 actions)
 * - 4 personality types
 * - Environment awareness (robots, monsters, NPCs, transNodes)
 * - Goal mode + free exploration mode
 * 
 * Usage:
 * const { AILoop } = require('./ai_loop.js');
 * const ai = new AILoop(null, 'playerUid');
 * ai.setGoal('go to village head and talk');
 * ai.start(2000);
 */

const https = require('https');
const http = require('http');

// ==================== LLM Call ==================== //

function callLLM(prompt, systemPrompt) {
    return new Promise((resolve) => {
        const API_KEY = process.env.MINIMAX_API_KEY || '';
        const BODY = {
            model: 'MiniMax-M2',
            messages: [
                { role: 'system', content: systemPrompt || 'You are a game AI. Return only JSON.' },
                { role: 'user', content: prompt }
            ],
            max_tokens: 256,
            temperature: 0.7
        };
        const body = JSON.stringify(BODY);
        const options = {
            hostname: 'api.minimax.chat',
            path: '/v1/text/chatcompletion_v2',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            }
        };
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(json.choices?.[0]?.message?.content?.trim() || '{}');
                } catch (e) { resolve('{}'); }
            });
        });
        req.on('error', () => resolve('{}'));
        req.write(body);
        req.end();
    });
}

// ==================== Hardcoded Known TransNodes ==================== //

const KNOWN_TRANS = {
    5001: [{ targetMapId: 2000, gridX: 71, gridY: 86, name: 'TransNode_2000' }],
    2000: [
        { targetMapId: 2001, gridX: 249, gridY: 214, name: 'TransNode_2001' },
        { targetMapId: 2001, gridX: 47, gridY: 50, name: 'TransNode_2001_alt' }
    ],
    2001: [{ targetMapId: 2000, gridX: 11, gridY: 50, name: 'TransNode_2000' }]
};

// Known NPC positions in map 2001
const KNOWN_NPCS = {
    2001: {
        '200101': { name: 'VillageHead', x: 25, y: 30 }
    }
};

// ==================== Helpers ==================== //

function distance(a, b) {
    if (!a || !b) return 999;
    return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
}

function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
}

// ==================== Personalities ==================== //

const PERSONALITIES = {
    curious:    { name: 'Curious', idleChance: 0.3, exploreChance: 0.5, talkChance: 0.3 },
    cautious:   { name: 'Cautious', idleChance: 0.2, exploreChance: 0.2, talkChance: 0.2 },
    social:     { name: 'Social', idleChance: 0.3, exploreChance: 0.3, talkChance: 0.6 },
    adventurous:{ name: 'Adventurous', idleChance: 0.1, exploreChance: 0.4, talkChance: 0.5 }
};

// ==================== AI Loop ==================== //

class AILoop {
    constructor(bridge, playerUid, personality = 'curious') {
        this.bridge = bridge;
        this.playerUid = playerUid;
        this.p = PERSONALITIES[personality] || PERSONALITIES.curious;
        
        // State
        this.goal = null;
        this.state = null;
        this.memory = [];
        this.lastAction = null;
        this.lastActionTime = 0;
        this.stuckCounter = 0;
        this.lastPosition = null;
        this.isMoving = false;
        this.chatCooldown = 0;
        this.exploring = false;
        this.tickCount = 0;
        this.observations = [];
        
        // Avoid spamming the same failed direction
        this.lastFailedTarget = null;
        this.lastFailedTime = 0;
        
        this.interval = null;
        
        this.log(`AI started, personality: ${this.p.name}`);
    }

    log(msg) {
        const ts = new Date().toISOString().slice(11, 19);
        console.log(`[AI:${this.playerUid.slice(0,8)}][${ts}] ${msg}`);
    }

    setGoal(goal) {
        this.goal = goal;
        this.exploring = false;
        this.lastFailedTarget = null;
        this.log(`Goal set: ${goal}`);
    }

    clearGoal() { this.goal = null; this.log('Goal cleared'); }

    setPersonality(key) {
        if (PERSONALITIES[key]) { this.p = PERSONALITIES[key]; this.log(`Personality: ${this.p.name}`); }
    }

    start(intervalMs = 2000) {
        if (this.interval) clearInterval(this.interval);
        this.interval = setInterval(() => this.tick(), intervalMs);
        this.log(`Loop started (${intervalMs}ms)`);
    }

    stop() {
        if (this.interval) { clearInterval(this.interval); this.interval = null; }
        this.log('Loop stopped');
    }

    // ==================== Main Tick ==================== //

    async tick() {
        this.tickCount++;
        if (this.chatCooldown > 0) this.chatCooldown--;
        
        await this.updateState();
        if (!this.state) return;
        
        this.observe();
        
        // Still moving from last command - skip to let it complete
        if (this.isMoving) {
            this.isMoving = false;
            return;
        }
        
        let decision = null;
        if (this.goal) {
            decision = await this.decideWithGoal();
        } else {
            decision = await this.decideFree();
        }
        
        if (decision) {
            await this.execute(decision);
        }
        
        if (decision) this.updateMemory(decision);
    }

    // ==================== Update State ==================== //

    async updateState() {
        return new Promise((resolve) => {
            const req = http.request({
                hostname: '127.0.0.1', port: 18766,
                path: `/clients/${this.playerUid}/perception`, method: 'GET'
            }, (res) => {
                let data = '';
                res.on('data', c => data += c);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        const p = json.perception;
                        if (p) {
                            this.state = {
                                mapId: p.mapId,
                                position: p.position || (p.self && p.self.position),
                                self: p.self,
                                robots: p.robots || [],
                                npcs: p.npcs || [],
                                monsters: p.monsters || [],
                                players: p.players || [],
                                transNodes: p.transNodes || []
                            };
                        }
                    } catch (e) {}
                    resolve();
                });
            });
            req.on('error', () => resolve());
            req.end();
        });
    }

    // ==================== Environment Awareness ==================== //

    observe() {
        if (!this.state) return;
        const obs = [];
        for (const r of this.state.robots.slice(0, 3)) {
            const d = distance(this.state.position, r.position);
            if (d < 15) obs.push({ type: 'robot', id: r.playerUid, name: r.name, dist: Math.round(d), x: r.position.x, y: r.position.y });
        }
        for (const m of this.state.monsters.slice(0, 3)) {
            const d = distance(this.state.position, m.position);
            if (d < 10) obs.push({ type: 'monster', id: m.uid, name: m.name, dist: Math.round(d), x: m.position.x, y: m.position.y, status: m.status });
        }
        for (const n of this.state.npcs.slice(0, 3)) {
            const d = distance(this.state.position, n.position);
            if (d < 10) obs.push({ type: 'npc', id: n.npcId, name: n.name, dist: Math.round(d), x: n.position.x, y: n.position.y });
        }
        for (const t of (this.state.transNodes || [])) {
            const d = distance(this.state.position, { x: t.gridX, y: t.gridY });
            if (d < 8) obs.push({ type: 'transnode', id: t.nodeName, target: t.targetMapId, dist: Math.round(d), x: t.gridX, y: t.gridY });
        }
        this.observations = obs;
    }

    // ==================== Stuck Detection ==================== //

    checkStuck() {
        if (!this.lastAction || this.lastAction.type !== 'move') return;
        if (!this.lastAction.x || !this.lastPosition) return;
        
        const target = { x: this.lastAction.x, y: this.lastAction.y };
        const distFromStart = distance(this.state.position, target);
        const moved = distance(this.lastPosition, this.state.position) > 0.5;
        const now = Date.now();
        
        // Only stuck if position hasn't changed at all after 6 seconds
        if (!moved && distFromStart > 2 && (now - this.lastActionTime) > 6000) {
            this.log(`Stuck at (${this.state.position.x},${this.state.position.y}), trying around`);
            const alt = this.navigateAround();
            if (alt) this.execute(alt);
        }
    }

    // ==================== Goal Decision ==================== //

    async decideWithGoal() {
        const g = this.goal.trim();
        
        if (g.includes('VillageHead') || g.includes('village') || g.includes('\u6751\u957f')) {
            return this.decideGoToVillageHead();
        }
        if (g.includes('map') || g.includes('\u5730\u56fe')) {
            return this.decideGoToMap(g);
        }
        if (g.includes('explore') || g.includes('\u63a2\u7d22')) {
            return this.decideExplore();
        }
        
        // Default: explore
        return this.decideExplore();
    }

    // ==================== Village Head Decision ==================== //

    decideGoToVillageHead() {
        const mapId = this.state.mapId;
        const pos = this.state.position;
        
        // Merge cached + known transNodes
        let tns = this.state.transNodes || [];
        const known = KNOWN_TRANS[mapId] || [];
        for (const k of known) {
            if (!tns.find(t => t.gridX === k.gridX && t.gridY === k.gridY)) {
                tns.push(k);
            }
        }
        
        if (mapId === 2001) {
            const npc = KNOWN_NPCS[2001]?.['200101'];
            if (!npc) return null;
            const d = distance(pos, { x: npc.x, y: npc.y });
            if (d <= 3) {
                if (this.chatCooldown === 0) {
                    this.chatCooldown = 5;
                    this.log('At village head, interacting');
                    return { type: 'interact', npcId: '200101', remark: 'Interact with VillageHead' };
                }
            } else {
                return { type: 'move', x: npc.x, y: npc.y, remark: 'Go to VillageHead' };
            }
        } else if (mapId === 2000) {
            const to2001 = tns.find(t => t.targetMapId === 2001);
            if (to2001) {
                const d = distance(pos, { x: to2001.gridX, y: to2001.gridY });
                return { type: 'move', x: to2001.gridX, y: to2001.gridY, remark: `To transNode (${Math.round(d)} dist)` };
            }
            return this.decideExplore();
        } else if (mapId === 5001) {
            const to2000 = tns.find(t => t.targetMapId === 2000);
            if (to2000) {
                return { type: 'move', x: to2000.gridX, y: to2000.gridY, remark: 'Back to world map' };
            }
            return this.decideExplore();
        } else {
            // Unknown map - try to find world map 2000
            const to2000 = tns.find(t => t.targetMapId === 2000);
            if (to2000) return { type: 'move', x: to2000.gridX, y: to2000.gridY, remark: 'Back to world map' };
            return this.decideExplore();
        }
        
        return null;
    }

    // ==================== Free Decision ==================== //

    async decideFree() {
        if (this.observations.length > 0 && Math.random() < this.p.talkChance) {
            const obs = randomChoice(this.observations);
            if (obs.type === 'robot' && this.chatCooldown === 0) {
                const msgs = ['Hi', 'Hey', 'Morning'];
                this.chatCooldown = 8;
                return { type: 'talk', message: randomChoice(msgs) + ' ' + obs.name, remark: `Greet ${obs.name}` };
            }
            if (obs.type === 'npc' && this.chatCooldown === 0) {
                this.chatCooldown = 5;
                return { type: 'interact', npcId: obs.id, remark: `Talk to ${obs.name}` };
            }
        }
        
        if (Math.random() < this.p.exploreChance) {
            return this.decideExplore();
        }
        
        return this.idle();
    }

    // ==================== Explore Decision ==================== //

    decideExplore() {
        if (!this.exploring) { this.exploring = true; this.log(`Exploring map ${this.state.mapId}`); }
        
        const mapId = this.state.mapId;
        const pos = this.state.position;
        
        let tns = this.state.transNodes || [];
        const known = KNOWN_TRANS[mapId] || [];
        for (const k of known) {
            if (!tns.find(t => t.gridX === k.gridX && t.gridY === k.gridY)) tns.push(k);
        }
        
        // Find nearest unvisited transNode
        const candidates = tns
            .map(t => ({ ...t, dist: distance(pos, { x: t.gridX, y: t.gridY }) }))
            .filter(t => t.dist > 5)
            .sort((a, b) => a.dist - b.dist);
        
        if (candidates.length > 0) {
            const t = candidates[0];
            return { type: 'move', x: t.gridX, y: t.gridY, remark: `Explore ${t.name}(${Math.round(t.dist)} away)` };
        }
        
        // Random walk
        const dirs = [
            { dx: 10, dy: 0 }, { dx: -10, dy: 0 },
            { dx: 0, dy: 10 }, { dx: 0, dy: -10 },
            { dx: 8, dy: 5 }, { dx: -8, dy: 5 }
        ];
        const d = randomChoice(dirs);
        const target = {
            x: clamp(pos.x + d.dx, 0, 400),
            y: clamp(pos.y + d.dy, 0, 250)
        };
        return { type: 'move', x: target.x, y: target.y, remark: 'Wander around' };
    }

    // ==================== Navigate Around (on stuck) ==================== //

    navigateAround() {
        const now = Date.now();
        
        // Don't spam the same failed direction within 20 seconds
        if (this.lastFailedTarget && (now - this.lastFailedTime) < 20000) {
            const t = this.lastFailedTarget;
            const offset = { dx: randomChoice([-8, 8, 0, -12, 12]), dy: randomChoice([-8, 8, 0, -12, 12]) };
            this.lastFailedTarget = { x: t.x + offset.dx, y: t.y + offset.dy };
        } else {
            // Random detour from current position
            const d = randomChoice([
                { dx: 8, dy: 8 }, { dx: -8, dy: 8 }, { dx: 8, dy: -8 }, { dx: -8, dy: -8 },
                { dx: 15, dy: 0 }, { dx: -15, dy: 0 }, { dx: 0, dy: 15 }, { dx: 0, dy: -15 }
            ]);
            this.lastFailedTarget = {
                x: clamp(this.state.position.x + d.dx, 0, 400),
                y: clamp(this.state.position.y + d.dy, 0, 250)
            };
        }
        this.lastFailedTime = now;
        
        const t = this.lastFailedTarget;
        return { type: 'move', x: t.x, y: t.y, remark: 'Detour' };
    }

    // ==================== Idle ==================== //

    idle() {
        if (Math.random() < 0.3) {
            const d = randomChoice([
                { dx: -2, dy: 2 }, { dx: 2, dy: -2 },
                { dx: -2, dy: -2 }, { dx: 2, dy: 2 }
            ]);
            return {
                type: 'move',
                x: clamp(this.state.position.x + d.dx, 0, 400),
                y: clamp(this.state.position.y + d.dy, 0, 250),
                remark: 'Idle move'
            };
        }
        return null;
    }

    // ==================== Execute ==================== //

    async execute(decision) {
        if (!decision) return;
        
        if (decision.type === 'move') {
            const x = Math.round(decision.x);
            const y = Math.round(decision.y);
            await this.sendCommand({ type: 'move', x, y });
            this.log(`Move ${decision.remark} -> (${x},${y})`);
            this.isMoving = true;
        } else if (decision.type === 'talk') {
            await this.sendCommand({ type: 'sendDialogue', message: decision.message });
            this.log(`Talk: ${decision.message}`);
        } else if (decision.type === 'interact') {
            await this.sendCommand({ type: 'interact', npcId: decision.npcId });
            this.log(`Interact: ${decision.npcId}`);
        }
        
        this.lastAction = decision;
        this.lastActionTime = Date.now();
        if (!this.lastPosition) this.lastPosition = { ...this.state.position };
    }

    sendCommand(cmd) {
        return new Promise((resolve) => {
            const req = http.request({
                hostname: '127.0.0.1', port: 18766,
                path: '/command', method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }, (res) => {
                let d = '';
                res.on('data', c => d += c);
                res.on('end', () => resolve(d));
            });
            req.on('error', () => resolve());
            req.write(JSON.stringify({ playerUid: this.playerUid, command: cmd }));
            req.end();
        });
    }

    // ==================== Memory ==================== //

    updateMemory(action) {
        if (!action) return;
        this.memory.push({
            tick: this.tickCount,
            type: action.type,
            x: action.x, y: action.y,
            remark: action.remark,
            pos: { ...this.state.position },
            time: Date.now()
        });
        if (this.memory.length > 10) this.memory.shift();
    }
}

module.exports = { AILoop, PERSONALITIES };
