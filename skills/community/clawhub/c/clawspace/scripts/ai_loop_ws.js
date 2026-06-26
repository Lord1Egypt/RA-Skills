/**
 * AI Loop with Multi-layer Character Memory
 */

const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

// ==================== Memory System ==================== //

const WORKSPACE = process.env.OPENCLAW_WORKSPACE ||
    path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
const MEM_DIR = path.join(WORKSPACE, 'clawspace', 'memory');
const DAILY_DIR = path.join(MEM_DIR, 'daily');
const CURATED_FILE = path.join(WORKSPACE, 'clawspace', 'character_memory.json');
const STATE_FILE = path.join(WORKSPACE, 'clawspace', 'state.json');
const LOG_FILE = path.join(WORKSPACE, 'clawspace', 'ai_loop.log');

// Ensure dirs
if (!fs.existsSync(DAILY_DIR)) fs.mkdirSync(DAILY_DIR, { recursive: true });

function today() { return new Date().toISOString().slice(0, 10); }
function now() { return new Date().toISOString(); }

function dist(a, b) {
    if (!a || !b) return 999;
    return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
}
function rnd(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

// ==================== Daily Memory (Layer 1) ==================== //

class DailyMemory {
    constructor(uid) {
        this.uid = uid;
        this.date = today();
        this.file = path.join(DAILY_DIR, `${this.date}.json`);
        this.data = this.load();
    }
    load() {
        try {
            if (fs.existsSync(this.file)) return JSON.parse(fs.readFileSync(this.file, 'utf8'));
        } catch(e) {}
        return { date: this.date, uid: this.uid, events: [] };
    }
    save() {
        try { fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2), 'utf8'); } catch(e) {}
    }
    log(action, detail) {
        this.data.events.push({ time: now(), action, detail });
        this.save();
    }
    logMove(from, to, mapId) { if (!from || !to) return; this.log('move', { from, to, mapId }); }
    logTalk(npcId, msg) { this.log('talk', { npcId, message: msg }); }
    logMapEnter(mapId) { this.log('mapEnter', { mapId }); }
    logMeetPlayer(uid, name) { this.log('meetPlayer', { playerUid: uid, name }); }
    logGoalDone(goal) { this.log('goalDone', { goal }); }
    logGoal(goal, done) { this.log(done ? 'goalDone' : 'goalStart', { goal }); }
    getAllEvents() { return this.data.events; }
    staleDays() {
        try {
            const s = fs.statSync(this.file);
            return s.mtime.toISOString().slice(0, 10) === today() ? 0 : 1;
        } catch(e) { return 0; }
    }
}

// ==================== Curated Memory (Layer 2) ==================== //

const KNOWN_MAPS = { 2000: { name: '世界地图' }, 2001: { name: '新手村' }, 5001: { name: '个人地图' } };
const KNOWN_NPCS = { 2001: { '200101': { name: '老村长' } } };

class CuratedMemory {
    constructor(uid) {
        this.uid = uid;
        this.file = CURATED_FILE;
        this.data = this.load();
    }
    load() {
        try {
            if (fs.existsSync(this.file)) {
                const raw = JSON.parse(fs.readFileSync(this.file, 'utf8'));
                // Migrate old format
                if (!raw.places && raw.placesVisited) raw.places = {};
                if (Array.isArray(raw.placesVisited)) {
                    for (const p of raw.placesVisited) {
                        if (p && p.mapId) raw.places[p.mapId] = { name: p.name, firstVisit: p.firstVisit, lastVisit: p.lastVisit, daysVisited: p.daysVisited || 1 };
                    }
                }
                if (!raw.npcs && raw.npcsMet) raw.npcs = {};
                if (Array.isArray(raw.npcsMet)) {
                    for (const n of raw.npcsMet) {
                        if (n && n.npcId) raw.npcs[n.npcId] = { name: n.name, conversations: n.conversations || 0, lastMessage: n.lastMessage, lastMet: n.lastMet };
                    }
                }
                raw.places = raw.places || {};
                raw.npcs = raw.npcs || {};
                raw.players = raw.players || {};
                raw.goals = raw.goals || [];
                raw.keyFacts = raw.keyFacts || [];
                return raw;
            }
        } catch(e) {}
        return { uid: this.uid, personality: null, places: {}, npcs: {}, players: {}, goals: [], keyFacts: [], lastConsolidated: null };
    }
    save() {
        try { fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2), 'utf8'); } catch(e) {}
    }
    onMapEnter(mapId) {
        const name = KNOWN_MAPS[mapId]?.name || `地图${mapId}`;
        if (!this.data.places[mapId]) {
            this.data.places[mapId] = { name, firstVisit: now(), lastVisit: now(), daysVisited: 1 };
        } else {
            const p = this.data.places[mapId];
            p.lastVisit = now();
            if (p.lastVisit.slice(0,10) !== today()) p.daysVisited++;
        }
        this.save();
    }
    onTalk(npcId, message) {
        const name = KNOWN_NPCS[2001]?.[npcId]?.name || npcId;
        if (!this.data.npcs[npcId]) {
            this.data.npcs[npcId] = { name, conversations: 1, lastMessage: message, lastMet: now() };
        } else {
            const n = this.data.npcs[npcId];
            n.conversations++;
            n.lastMessage = message;
            n.lastMet = now();
        }
        this.save();
    }
    onMeetPlayer(uid, name) {
        if (!this.data.players[uid]) this.data.players[uid] = { name, greeted: false, lastMet: now() };
        else this.data.players[uid].lastMet = now();
        this.save();
    }
    onGreet(uid) {
        if (this.data.players[uid]) { this.data.players[uid].greeted = true; this.save(); }
    }
    onGoalCompleted(goal) {
        this.data.goals.push({ goal, completedAt: now() });
        if (this.data.goals.length > 50) this.data.goals = this.data.goals.slice(-50);
        this.save();
    }
    addFact(fact) {
        if (!this.data.keyFacts.includes(fact)) this.data.keyFacts.push(fact);
        if (this.data.keyFacts.length > 100) this.data.keyFacts = this.data.keyFacts.slice(-100);
        this.save();
    }
    consolidate(dailyEvents) {
        const mapVisits = {}, npcTalks = {}, playersMet = {}, goalsDone = [];
        for (const e of dailyEvents) {
            if (e.action === 'mapEnter') mapVisits[e.detail.mapId] = (mapVisits[e.detail.mapId]||0)+1;
            if (e.action === 'talk') npcTalks[e.detail.npcId] = (npcTalks[e.detail.npcId]||0)+1;
            if (e.action === 'meetPlayer') playersMet[e.detail.playerUid] = e.detail.name;
            if (e.action === 'goalDone') goalsDone.push(e.detail.goal);
        }
        for (const [mid, cnt] of Object.entries(mapVisits)) this.onMapEnter(parseInt(mid));
        for (const [nid, cnt] of Object.entries(npcTalks)) {
            const lastTalk = dailyEvents.filter(e => e.action==='talk' && e.detail.npcId===nid).pop();
            this.onTalk(nid, lastTalk?.detail?.message || '(多次对话)');
        }
        for (const [uid, name] of Object.entries(playersMet)) this.onMeetPlayer(uid, name);
        for (const g of goalsDone) this.onGoalCompleted(g);
        this.data.lastConsolidated = now();
        this.save();
    }
    getSummary() {
        const places = Object.values(this.data.places).map(p => `${p.name}(${p.daysVisited}天)`).join(', ') || '无';
        const npcs = Object.values(this.data.npcs).map(n => `${n.name}(${n.conversations}次)`).join(', ') || '无';
        const players = Object.values(this.data.players).filter(p => p.greeted).map(p => p.name).join(', ') || '无';
        const goals = this.data.goals.slice(-5).map(g => g.goal).join(', ') || '无';
        return { places, npcs, players, goals };
    }
    getDescription() {
        const s = this.getSummary();
        return `去过：${s.places} | 聊过：${s.npcs} | 完成：${s.goals}`;
    }
}

// ==================== Cleanup Old Dailies ==================== //

function cleanupOldDailies() {
    try {
        const files = fs.readdirSync(DAILY_DIR).filter(f => f.endsWith('.json'));
        const cutoff = new Date(); cutoff.setDate(cutoff.getDate() - 7);
        const cutoffStr = cutoff.toISOString().slice(0, 10);
        for (const file of files) {
            const date = file.replace('.json', '');
            if (date < cutoffStr) {
                const fp = path.join(DAILY_DIR, file);
                try {
                    const d = JSON.parse(fs.readFileSync(fp, 'utf8'));
                    if (d.events?.length > 0) { const c = new CuratedMemory(d.uid); c.consolidate(d.events); }
                } catch(e) {}
                fs.unlinkSync(fp);
            }
        }
    } catch(e) {}
}

// Check yesterday's daily and consolidate if exists
function checkYesterdayConsolidation(uid) {
    const y = new Date(); y.setDate(y.getDate() - 1);
    const ydate = y.toISOString().slice(0, 10);
    const fp = path.join(DAILY_DIR, `${ydate}.json`);
    if (fs.existsSync(fp)) {
        try {
            const d = JSON.parse(fs.readFileSync(fp, 'utf8'));
            if (d.events?.length > 0) { const c = new CuratedMemory(uid); c.consolidate(d.events); }
        } catch(e) {}
    }
}

// ==================== Known Game Data ==================== //

const KNOWN_TRANS = {
    5001: [{ tid: 2000, x: 71, y: 86, name: 'T_2000' }],
    2000: [{ tid: 2001, x: 249, y: 214, name: 'T_2001' }, { tid: 2001, x: 47, y: 50, name: 'T_2001_alt' }],
    2001: [{ tid: 2000, x: 11, y: 50, name: 'T_2000' }]
};

// ==================== AI Loop ==================== //

class AILoop {
    constructor(uid, personality = 'curious') {
        this.uid = uid;
        const cfg = {
            curious:{idleC:0.3,exploreC:0.5,talkC:0.3},
            cautious:{idleC:0.2,exploreC:0.2,talkC:0.2},
            social:{idleC:0.3,exploreC:0.3,talkC:0.6},
            adventurous:{idleC:0.1,exploreC:0.4,talkC:0.5}
        };
        this.p = cfg[personality] || cfg.curious;

        // State
        this.mapId = null;
        this.pos = null;
        this.transNodes = [];
        this.robots = [];
        this.npcs = [];

        // Goal tracking
        this.goal = null;
        this.goalSteps = 0;

        // Movement state
        this.lastCmd = null;
        this.lastMovedFrom = null;
        this.sentMoveAt = 0;
        this.chatCd = 0;
        this.exploring = false;
        this.tickCt = 0;

        // Memory (multi-layer)
        this.daily = new DailyMemory(uid);
        this.curated = new CuratedMemory(uid);

        // Check if we need to consolidate yesterday
        checkYesterdayConsolidation(uid);
        cleanupOldDailies();

        // WS & interval
        this.ws = null;
        this.interval = null;
        this.connected = false;
    }

    log(m) {
        const ts = new Date().toISOString().slice(11, 19);
        const line = `[AI:${this.uid.slice(0,8)}][${ts}] ${m}`;
        console.log(line);
        fs.appendFileSync(LOG_FILE, line + '\n');
    }

    setGoal(g) { this.goal = g; this.goalSteps = 0; this.exploring = false; this.log(`Goal: ${g}`); this.daily.logGoal(g, false); }
    clearGoal() { this.goal = null; this.goalSteps = 0; }

    start() {
        this.connectWS();
        this.interval = setInterval(() => this.tick(), 2500);
        this.log(`AI Loop started | ${this.curated.getDescription()}`);
    }

    stop() {
        if (this.ws) { this.ws.close(); this.ws = null; }
        if (this.interval) { clearInterval(this.interval); this.interval = null; }
        // Consolidate today's events into curated
        this.curated.consolidate(this.daily.getAllEvents());
        this.log(`Stopped | ${this.curated.getDescription()}`);
    }

    // ==================== WS ==================== //

    connectWS() {
        this.ws = new WebSocket('ws://localhost:18765');
        this.ws.on('open', () => {
            this.ws.send(JSON.stringify({ type: 'ai_register', playerUid: 'OPENCLAW', mode: 'enabled' }));
        });
        this.ws.on('message', data => { try { this.onMsg(JSON.parse(data.toString())); } catch(e) {} });
        this.ws.on('error', e => this.log(`WS err: ${e.message}`));
        this.ws.on('close', () => {
            this.connected = false;
            setTimeout(() => this.connectWS(), 3000);
        });
    }

    onMsg(msg) {
        const t = msg.type;
        if (t === 'ai_registered') {
            this.connected = true;
            this.log('Registered');
            this.fetchPerception();
            return;
        }
        if (t === 'ai_map_changed') {
            const old = this.mapId;
            this.mapId = msg.mapId;
            this.log(`Map: ${old} -> ${this.mapId}`);
            this.daily.logMapEnter(this.mapId);
            this.curated.onMapEnter(this.mapId);
            this.fetchPerception();
            return;
        }
        if (t === 'ai_perception_data') {
            const p = msg.perception;
            this.mapId = p.mapId;
            this.transNodes = p.transNodes || [];
            this.robots = p.robots || [];
            this.npcs = p.npcs || [];
            const newPos = p.position || (p.self && p.self.position);
            if (newPos) {
                const old = this.pos;
                this.pos = newPos;
                if (old) this.daily.logMove(old, newPos, this.mapId);
                for (const npc of (p.npcs || [])) {
                    this.curated.onMeetPlayer(npc.npcId, npc.name); // NPC tracked in curated
                }
                for (const r of (p.robots || [])) {
                    this.daily.logMeetPlayer(r.playerUid, r.name);
                    this.curated.onMeetPlayer(r.playerUid, r.name);
                }
            }
            this.saveState();
            return;
        }
        if (t === 'ai_player_moved') {
            if (msg.position) {
                const old = this.pos;
                this.pos = msg.position;
                if (old) this.daily.logMove(old, msg.position, this.mapId);
                this.log(`Moved to (${this.pos.x},${this.pos.y})`);
            }
            return;
        }
        if (t === 'ai_transport_points') {
            this.transNodes = msg.transportPoints || [];
        }
    }

    saveState() {
        try {
            fs.writeFileSync(STATE_FILE, JSON.stringify({
                mapId: this.mapId, position: this.pos,
                tick: this.tickCt, goal: this.goal, updated: now()
            }, null, 2), 'utf8');
        } catch(e) {}
    }

    // ==================== HTTP ==================== //

    fetchPerception() {
        return new Promise(resolve => {
            const req = http.request({
                hostname: '127.0.0.1', port: 18766,
                path: `/clients/${this.uid}/perception`, method: 'GET'
            }, res => {
                let d = '';
                res.on('data', c => d += c);
                res.on('end', () => {
                    try {
                        const p = JSON.parse(d).perception;
                        if (p) {
                            const oldMap = this.mapId;
                            this.mapId = p.mapId;
                            this.transNodes = p.transNodes || [];
                            this.robots = p.robots || [];
                            this.npcs = p.npcs || [];
                            const newPos = p.position || (p.self && p.self.position);
                            if (newPos) {
                                const old = this.pos;
                                this.pos = newPos;
                                if (oldMap && oldMap !== this.mapId) {
                                    this.daily.logMapEnter(this.mapId);
                                    this.curated.onMapEnter(this.mapId);
                                }
                                if (old) this.daily.logMove(old, newPos, this.mapId);
                                for (const npc of (p.npcs || [])) {
                                    this.curated.onTalk(npc.npcId, '(感知)');
                                }
                                for (const r of (p.robots || [])) {
                                    this.daily.logMeetPlayer(r.playerUid, r.name);
                                    this.curated.onMeetPlayer(r.playerUid, r.name);
                                }
                            }
                            this.log(`HTTP: map=${this.mapId} pos=(${this.pos?.x},${this.pos?.y})`);
                            this.saveState();
                        }
                    } catch(e) {}
                    resolve();
                });
            });
            req.on('error', () => resolve());
            req.end();
        });
    }

    // ==================== Tick ==================== //

    async tick() {
        this.tickCt++;
        if (this.chatCd > 0) this.chatCd--;
        await this.fetchPerception();
        if (!this.pos) return;
        if (this.goal) this.decideGoal();
        else this.decideFree();
    }

    // ==================== Goal ==================== //

    decideGoal() {
        this.goalSteps++;
        const g = this.goal;
        if (g.includes('VillageHead') || g.includes('village') || g.includes('村长')) {
            this.decideVillageHead(); return;
        }
        if (g.includes('explore') || g.includes('探索')) { this.explore(); return; }
        this.log(`Unknown goal: ${g}`);
        this.clearGoal();
    }

    decideVillageHead() {
        const mid = this.mapId;
        const pos = this.pos;
        const npcInfo = this.curated.data.npcs['200101'];

        if (mid === 2001) {
            const target = { x: 25, y: 30 };
            const d = dist(pos, target);
            if (d <= 2) {
                if (this.chatCd === 0) {
                    this.chatCd = 5;
                    let msg = '你好村长！';
                    if (npcInfo && npcInfo.conversations > 0) {
                        const greetings = ['村长好，我又来了！', '您好村长！', '村长好！'];
                        msg = rnd(greetings);
                    }
                    this.act({ type: 'sendDialogue', message: msg, remark: 'Greet VillageHead' });
                    this.daily.logTalk('200101', msg);
                    this.curated.onTalk('200101', msg);
                    this.daily.logGoalDone(this.goal);
                    this.curated.onGoalCompleted(this.goal);
                    this.log(`Talked to VillageHead (total: ${(npcInfo?.conversations||0)+1} convs) | Goal done!`);
                    this.clearGoal();
                }
            } else {
                this.moveToward(target.x, target.y, 'To VillageHead');
            }
            return;
        }
        if (mid === 2000) {
            const tn = this.tnTo(2001) || this.knownTn(mid, 2001);
            if (tn) { this.moveToward(tn.x, tn.y, `To T_2001`); return; }
            this.explore(); return;
        }
        if (mid === 5001) {
            const tn = this.tnTo(2000) || this.knownTn(mid, 2000);
            if (tn) { this.moveToward(tn.x, tn.y, `To T_2000`); return; }
            this.explore(); return;
        }
        const tn = this.tnTo(2000);
        if (tn) this.moveToward(tn.x, tn.y, 'To world');
        else this.explore();
    }

    // ==================== Free ==================== //

    decideFree() {
        const newPlayers = this.robots.filter(r => {
            const p = this.curated.data.players[r.playerUid];
            return dist(this.pos, r.position) < 10 && (!p || !p.greeted);
        });
        if (newPlayers.length > 0 && Math.random() < this.p.talkC) {
            const r = newPlayers[0];
            const msgs = ['你好', 'HI', '一起冒险吗？', '哈喽~'];
            this.act({ type: 'sendDialogue', message: rnd(msgs), remark: `Greet ${r.name}` });
            this.curated.onGreet(r.playerUid);
            this.chatCd = 10;
            return;
        }
        if (Math.random() < this.p.exploreC) { this.explore(); return; }
        if (Math.random() < this.p.idleC) {
            const delta = rnd([[2,2],[-2,-2],[2,-2],[-2,2]]);
            this.moveToward(clamp(this.pos.x+delta[0],0,400), clamp(this.pos.y+delta[1],0,250), 'Idle');
        }
    }

    // ==================== Explore ==================== //

    explore() {
        if (!this.exploring) { this.exploring = true; this.log(`Exploring map ${this.mapId}`); }
        const pos = this.pos;
        let tns = [...this.transNodes];
        const known = KNOWN_TRANS[this.mapId] || [];
        for (const k of known) {
            if (!tns.find(t => t.x === k.x && t.y === k.y)) tns.push(k);
        }
        // Prefer unvisited maps
        const candidates = tns
            .map(t => ({ ...t, d: dist(pos, { x: t.x, y: t.y }) }))
            .filter(t => {
                const visited = !!this.curated.data.places[t.tid];
                return t.d > 3 && !visited;
            })
            .sort((a, b) => a.d - b.d);
        if (candidates.length > 0) {
            const t = candidates[0];
            const mapName = KNOWN_MAPS[t.tid]?.name || `地图${t.tid}`;
            this.moveToward(t.x, t.y, `Explore ${t.name} -> ${mapName}`);
        } else {
            const near = tns.map(t => ({ ...t, d: dist(pos, { x: t.x, y: t.y }) })).filter(t => t.d > 3).sort((a, b) => a.d - b.d);
            if (near.length > 0) {
                const t = near[0];
                this.moveToward(t.x, t.y, `Return to ${t.name}`);
            } else {
                const delta = rnd([[10,0],[-10,0],[0,10],[0,-10]]);
                this.moveToward(clamp(pos.x+delta[0],0,400), clamp(pos.y+delta[1],0,250), 'Wander');
            }
        }
    }

    // ==================== Move ==================== //

    moveToward(x, y, remark) {
        x = Math.round(x); y = Math.round(y);
        if (!x || !y || isNaN(x) || isNaN(y)) return;
        if (this.lastCmd?.type === 'move' && this.lastCmd.x === x && this.lastCmd.y === y && (Date.now() - this.sentMoveAt) < 20000) return;
        this.act({ type: 'move', x, y, remark });
        this.sentMoveAt = Date.now();
        this.lastMovedFrom = { ...this.pos };
    }

    // ==================== Execute ==================== //

    act(cmd) {
        if (!this.connected) { this.log('Not connected!'); return; }
        this.lastCmd = cmd;
        if (cmd.type === 'move') {
            this.ws.send(JSON.stringify({ type: 'sendCommand', playerUid: this.uid, command: { type: 'move', x: cmd.x, y: cmd.y } }));
            this.log(`Move ${cmd.remark} -> (${cmd.x},${cmd.y})`);
        } else if (cmd.type === 'sendDialogue') {
            this.ws.send(JSON.stringify({ type: 'sendCommand', playerUid: this.uid, command: { type: 'sendDialogue', message: cmd.message } }));
            this.log(`Say: ${cmd.message}`);
        } else if (cmd.type === 'interact') {
            this.ws.send(JSON.stringify({ type: 'sendCommand', playerUid: this.uid, command: { type: 'interact', npcId: cmd.npcId } }));
            this.log(`Interact: ${cmd.npcId}`);
        }
    }

    // ==================== Helpers ==================== //

    tnTo(tid) { return this.transNodes.find(t => t.targetMapId === tid); }
    knownTn(from, to) { return (KNOWN_TRANS[from] || []).find(t => t.tid === to); }
}

module.exports = { AILoop, DailyMemory, CuratedMemory, cleanupOldDailies, checkYesterdayConsolidation, MEM_DIR, DAILY_DIR, CURATED_FILE };
