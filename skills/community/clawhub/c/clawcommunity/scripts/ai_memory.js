/**
 * Multi-layer Character Memory System
 * 
 * Layer 1 - Daily (raw events): memory/daily/YYYY-MM-DD.json
 *   Raw log of everything that happened today
 *   Auto-cleanup: keeps last 7 days, older is consolidated and deleted
 * 
 * Layer 2 - Curated (long-term): character_memory.json
 *   Refined memory: personality, key facts, learned behavior
 *   Persists indefinitely
 */

const fs = require('fs');
const path = require('path');

// ==================== Dynamic Path ==================== //

const WORKSPACE = process.env.OPENCLAW_WORKSPACE ||
    path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
const MEM_DIR = path.join(WORKSPACE, 'clawspace', 'memory');
const DAILY_DIR = path.join(MEM_DIR, 'daily');
const CURATED_FILE = path.join(WORK_DIR || WORKSPACE, 'clawspace', 'character_memory.json');
const STATE_FILE = path.join(WORKSPACE, 'clawspace', 'state.json');
const LOG_FILE = path.join(WORKSPACE, 'clawspace', 'ai_loop.log');

// Ensure dirs exist
if (!fs.existsSync(DAILY_DIR)) fs.mkdirSync(DAILY_DIR, { recursive: true });

// ==================== Helpers ==================== //

function today() { return new Date().toISOString().slice(0, 10); }
function now() { return new Date().toISOString(); }

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
            if (fs.existsSync(this.file)) {
                return JSON.parse(fs.readFileSync(this.file, 'utf8'));
            }
        } catch(e) {}
        return this.empty();
    }

    empty() {
        return { date: this.date, uid: this.uid, events: [] };
    }

    save() {
        try {
            fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2), 'utf8');
        } catch(e) {}
    }

    // Log a raw event
    log(action, detail) {
        this.data.events.push({ time: now(), action, detail });
        this.save();
    }

    // Convenience loggers
    logMove(from, to, mapId) {
        this.log('move', { from, to, mapId });
    }

    logTalk(npcId, message) {
        this.log('talk', { npcId, message });
    }

    logMapEnter(mapId) {
        this.log('mapEnter', { mapId });
    }

    logMeetPlayer(playerUid, name) {
        this.log('meetPlayer', { playerUid, name });
    }

    logGoal(goal, completed) {
        this.log(completed ? 'goalDone' : 'goalStart', { goal });
    }

    logThought(thought) {
        this.log('thought', { text: thought });
    }

    // Get all events for consolidation
    getAllEvents() {
        return this.data.events;
    }

    // Days since last write
    staleDays() {
        try {
            const stat = fs.statSync(this.file);
            const lastWrite = stat.mtime.toISOString().slice(0, 10);
            return lastWrite === today() ? 0 : 1;
        } catch(e) { return 0; }
    }
}

// ==================== Curated Memory (Layer 2) ==================== //

const KNOWN_MAPS = {
    2000: { name: '世界地图' },
    2001: { name: '新手村' },
    5001: { name: '个人地图' }
};

const KNOWN_NPCS = {
    2001: { '200101': { name: '老村长' } }
};

class CuratedMemory {
    constructor(uid) {
        this.uid = uid;
        this.file = path.join(WORKSPACE, 'clawspace', 'character_memory.json');
        this.data = this.load();
    }

    load() {
        try {
            if (fs.existsSync(this.file)) {
                return JSON.parse(fs.readFileSync(this.file, 'utf8'));
            }
        } catch(e) {}
        return this.empty();
    }

    empty() {
        return {
            uid: this.uid,
            personality: null,    // refined personality traits
            places: {},           // mapId -> { name, firstVisit, lastVisit, daysVisited }
            npcs: {},             // npcId -> { name, conversations, lastMessage, lastMet }
            players: {},          // playerUid -> { name, greeted, lastMet }
            goals: [],            // completed goals with summary
            keyFacts: [],         // distilled important facts
            lastConsolidated: null
        };
    }

    save() {
        try {
            fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2), 'utf8');
        } catch(e) {}
    }

    // ==================== Mutations ==================== //

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

    onMeetPlayer(playerUid, name) {
        if (!this.data.players[playerUid]) {
            this.data.players[playerUid] = { name, greeted: false, lastMet: now() };
        } else {
            this.data.players[playerUid].lastMet = now();
        }
        this.save();
    }

    onGreet(playerUid) {
        if (this.data.players[playerUid]) {
            this.data.players[playerUid].greeted = true;
            this.save();
        }
    }

    onGoalCompleted(goal) {
        this.data.goals.push({ goal, completedAt: now() });
        if (this.data.goals.length > 50) this.data.goals = this.data.goals.slice(-50);
        this.save();
    }

    addFact(fact) {
        // Deduplicate
        if (!this.data.keyFacts.includes(fact)) {
            this.data.keyFacts.push(fact);
        }
        if (this.data.keyFacts.length > 100) this.data.keyFacts = this.data.keyFacts.slice(-100);
        this.save();
    }

    setPersonality(traits) {
        this.data.personality = traits;
        this.save();
    }

    // ==================== Consolidation ==================== //
    // Called when: new day starts, or user asks "summarize memory"

    consolidate(dailyEvents) {
        // Count map visits
        const mapVisits = {};
        // Count NPC interactions
        const npcTalks = {};
        // Track players met
        const playersMet = {};
        // Track goals
        const goalsDone = [];

        for (const evt of dailyEvents) {
            if (evt.action === 'mapEnter') {
                mapVisits[evt.detail.mapId] = (mapVisits[evt.detail.mapId] || 0) + 1;
            }
            if (evt.action === 'talk') {
                npcTalks[evt.detail.npcId] = (npcTalks[evt.detail.npcId] || 0) + 1;
            }
            if (evt.action === 'meetPlayer') {
                playersMet[evt.detail.playerUid] = evt.detail.name;
            }
            if (evt.action === 'goalDone') {
                goalsDone.push(evt.detail.goal);
            }
        }

        // Update curated memory
        for (const [mapId, count] of Object.entries(mapVisits)) {
            this.onMapEnter(parseInt(mapId));
        }

        for (const [npcId, count] of Object.entries(npcTalks)) {
            // Last message for this npc in events
            const lastTalk = dailyEvents.filter(e => e.action === 'talk' && e.detail.npcId === npcId).pop();
            this.onTalk(npcId, lastTalk?.detail?.message || '(多次对话)');
        }

        for (const [uid, name] of Object.entries(playersMet)) {
            this.onMeetPlayer(uid, name);
        }

        for (const goal of goalsDone) {
            this.onGoalCompleted(goal);
        }

        this.data.lastConsolidated = now();
        this.save();
    }

    // ==================== Queries ==================== //

    getSummary() {
        const places = Object.values(this.data.places).map(p => `${p.name}(${p.daysVisited}天)`).join(', ') || '无';
        const npcs = Object.values(this.data.npcs).map(n => `${n.name}(${n.conversations}次)`).join(', ') || '无';
        const players = Object.values(this.data.players).filter(p => p.greeted).map(p => p.name).join(', ') || '无';
        const goals = this.data.goals.slice(-5).map(g => g.goal).join(', ') || '无';
        return { places, npcs, players, goals };
    }

    // Describe character based on memory
    getCharacterDescription() {
        const s = this.getSummary();
        const traits = this.data.personality ? `性格倾向：${this.data.personality}` : '';
        const facts = this.data.keyFacts.length > 0 ? `已知事实：${this.data.keyFacts.slice(-3).join('；')}` : '';
        return [traits, facts, `去过：${s.places}`, `聊过：${s.npcs}`, `完成过：${s.goals}`].filter(Boolean).join(' | ');
    }
}

// ==================== Daily Cleanup ==================== //

function cleanupOldDailies() {
    try {
        const files = fs.readdirSync(DAILY_DIR).filter(f => f.endsWith('.json'));
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - 7);
        const cutoffStr = cutoff.toISOString().slice(0, 10);

        for (const file of files) {
            const date = file.replace('.json', '');
            if (date < cutoffStr) {
                // Consolidate before deleting
                const filePath = path.join(DAILY_DIR, file);
                try {
                    const daily = JSON.parse(fs.readFileSync(filePath, 'utf8'));
                    if (daily.events && daily.events.length > 0) {
                        const curated = new CuratedMemory(daily.uid);
                        curated.consolidate(daily.events);
                    }
                } catch(e) {}
                fs.unlinkSync(filePath);
            }
        }
    } catch(e) {}
}

// ==================== Auto-Check on Load ==================== //

// When memory system loads, check if we need to consolidate yesterday
function checkConsolidation(uid) {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const ydate = yesterday.toISOString().slice(0, 10);
    const yesterdayFile = path.join(DAILY_DIR, `${ydate}.json`);

    if (fs.existsSync(yesterdayFile)) {
        try {
            const daily = JSON.parse(fs.readFileSync(yesterdayFile, 'utf8'));
            const curated = new CuratedMemory(uid);
            curated.consolidate(daily.events);
        } catch(e) {}
    }
}

module.exports = {
    DailyMemory,
    CuratedMemory,
    cleanupOldDailies,
    checkConsolidation,
    MEM_DIR,
    DAILY_DIR,
    CURATED_FILE
};
