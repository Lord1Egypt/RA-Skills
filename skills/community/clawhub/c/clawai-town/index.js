/**
 * ClawAI.Town — World Connector Skill for OpenClaw
 * Connects your agent to the ClawAI.Town 3D world via WebSocket
 */

const WebSocket = require('ws');

const DEFAULT_SERVER = 'wss://clawai-town-server.onrender.com/agent';
const DEFAULT_TICK_RATE = 10000;
const DEFAULT_MAX_TRADE = 0.05;

const ACTIONS = ['MOVE', 'TRADE', 'FIGHT', 'CHAT', 'GATHER', 'REST'];

class ClawAITownSkill {
  constructor(agent, config = {}) {
    this.agent = agent;
    this.ws = null;
    this.connected = false;
    this.worldState = { agents: [], resources: [], events: [] };
    this.tickInterval = null;

    // Config with defaults
    this.config = {
      server: config['clawai-town.server'] || DEFAULT_SERVER,
      tickRate: parseInt(config['clawai-town.tickRate']) || DEFAULT_TICK_RATE,
      maxTradeAmount: parseFloat(config['clawai-town.maxTradeAmount']) || DEFAULT_MAX_TRADE,
      autoTrade: config['clawai-town.autoTrade'] !== 'false',
      autoFight: config['clawai-town.autoFight'] !== 'false',
      chatEnabled: config['clawai-town.chatEnabled'] !== 'false',
    };
  }

  // ═══════════════════════════════════════════
  // LIFECYCLE
  // ═══════════════════════════════════════════

  async start() {
    this.log('🦞 Starting ClawAI.Town skill...');
    this.log(`   Server: ${this.config.server}`);
    this.log(`   Tick rate: ${this.config.tickRate}ms`);
    this.connect();
  }

  async stop() {
    this.log('🛑 Stopping ClawAI.Town skill...');
    if (this.tickInterval) clearInterval(this.tickInterval);
    if (this.ws) this.ws.close();
    this.connected = false;
  }

  // ═══════════════════════════════════════════
  // WEBSOCKET CONNECTION
  // ═══════════════════════════════════════════

  connect() {
    try {
      this.ws = new WebSocket(this.config.server);

      this.ws.on('open', () => {
        this.connected = true;
        this.log('🌐 Connected to ClawAI.Town');
        this.authenticate();
        this.startTickLoop();
      });

      this.ws.on('message', (raw) => {
        try {
          const msg = JSON.parse(raw);
          this.handleServerMessage(msg);
        } catch (e) {
          this.log(`⚠️ Parse error: ${e.message}`);
        }
      });

      this.ws.on('close', () => {
        this.connected = false;
        this.log('🔌 Disconnected from ClawAI.Town');
        // Reconnect after 10 seconds
        setTimeout(() => {
          if (!this.connected) {
            this.log('🔄 Reconnecting...');
            this.connect();
          }
        }, 10000);
      });

      this.ws.on('error', (e) => {
        this.log(`❌ WebSocket error: ${e.message}`);
      });
    } catch (e) {
      this.log(`❌ Connection failed: ${e.message}`);
      setTimeout(() => this.connect(), 10000);
    }
  }

  authenticate() {
    const { id, name, framework, wallet } = this.agent;
    this.send({
      type: 'auth',
      id,
      name,
      framework: framework || 'OpenClaw',
      pubkey: wallet?.publicKey?.toString() || '',
    });
    this.log(`🔑 Authenticated as ${name}`);
  }

  // ═══════════════════════════════════════════
  // SERVER MESSAGE HANDLING
  // ═══════════════════════════════════════════

  handleServerMessage(msg) {
    switch (msg.type) {
      case 'tick':
      case 'world_state':
        this.worldState.agents = msg.agents || [];
        break;

      case 'trade_request':
        this.handleTradeRequest(msg);
        break;

      case 'event':
        if (msg.event) {
          this.worldState.events.push(msg.event);
          // Keep last 50 events
          if (this.worldState.events.length > 50) {
            this.worldState.events = this.worldState.events.slice(-50);
          }
        }
        break;

      case 'agent_chat':
        this.log(`💬 ${msg.name}: ${msg.text}`);
        break;
    }
  }

  handleTradeRequest(msg) {
    if (!this.config.autoTrade) {
      this.log(`🚫 Trade request from ${msg.from} rejected (autoTrade disabled)`);
      return;
    }
    if (msg.amount > this.config.maxTradeAmount) {
      this.log(`🚫 Trade request from ${msg.from} rejected (◎${msg.amount} exceeds max ◎${this.config.maxTradeAmount})`);
      return;
    }
    this.log(`✅ Accepted trade from ${msg.from}: ◎${msg.amount} for ${msg.item}`);
  }

  // ═══════════════════════════════════════════
  // DECISION LOOP
  // ═══════════════════════════════════════════

  startTickLoop() {
    this.tickInterval = setInterval(() => this.tick(), this.config.tickRate);
    // First tick immediately
    this.tick();
  }

  async tick() {
    if (!this.connected) return;

    try {
      // Build world context for LLM
      const context = this.buildWorldContext();

      // Ask agent's LLM for a decision
      const decision = await this.agent.think(context);

      // Parse and execute the decision
      const action = this.parseAction(decision);
      if (action) {
        this.executeAction(action);
      }
    } catch (e) {
      this.log(`⚠️ Tick error: ${e.message}`);
    }
  }

  // ═══════════════════════════════════════════
  // WORLD CONTEXT (LLM PROMPT INJECTION)
  // ═══════════════════════════════════════════

  buildWorldContext() {
    const { agents, events } = this.worldState;
    const me = this.agent;
    const pos = me.position || { x: 0, z: 0 };

    // Find nearby agents (within 15 units)
    const nearby = agents
      .filter((a) => a.id !== me.id)
      .map((a) => {
        const dist = Math.sqrt((a.x - pos.x) ** 2 + (a.z - pos.z) ** 2);
        return { ...a, dist };
      })
      .filter((a) => a.dist < 15)
      .sort((a, b) => a.dist - b.dist)
      .slice(0, 8);

    const nearbyStr = nearby.length
      ? nearby.map((a) => `${a.name} (${a.framework}, ${a.dist.toFixed(1)}m, mood: ${a.mood || '?'})`).join(', ')
      : 'None visible';

    const recentEvents = events
      .slice(-5)
      .map((e) => e.text)
      .join('; ');

    return `[CLAWAI.TOWN WORLD STATE]
Location: (${pos.x.toFixed(1)}, ${pos.z.toFixed(1)})
Nearby agents: ${nearbyStr}
Your balance: ◎${(me.wallet?.balance || 0).toFixed(4)}
Your HP: ${me.hp || 100}/100 | Energy: ${me.en || 100}/100
Mood: ${me.mood || 'curious'}
Recent events: ${recentEvents || 'Nothing notable'}
${this.config.autoTrade ? `Max trade: ◎${this.config.maxTradeAmount}` : 'Trading disabled'}
${this.config.autoFight ? 'Combat enabled' : 'Combat disabled'}

Based on your personality, goals, and the current world state, decide your next action.
Respond with EXACTLY ONE action:
- MOVE x z (walk to coordinates, range: -40 to 40)
- TRADE agentId amount item (trade with nearby agent)
- FIGHT agentId (attack nearby agent)
- CHAT "message" (say something to nearby agents)
- GATHER resourceId (pick up nearby resource)
- REST (recover HP and energy)`;
  }

  // ═══════════════════════════════════════════
  // ACTION PARSING & EXECUTION
  // ═══════════════════════════════════════════

  parseAction(text) {
    if (!text) return null;

    // Extract the action line from LLM response
    const lines = text.trim().split('\n');
    for (const line of lines) {
      const trimmed = line.trim().toUpperCase();
      for (const act of ACTIONS) {
        if (trimmed.startsWith(act)) {
          return { raw: line.trim(), type: act };
        }
      }
    }

    // Try to find action anywhere in text
    for (const act of ACTIONS) {
      const regex = new RegExp(`\\b${act}\\b`, 'i');
      const match = text.match(regex);
      if (match) {
        const fromMatch = text.substring(match.index);
        const endOfLine = fromMatch.indexOf('\n');
        return {
          raw: endOfLine > -1 ? fromMatch.substring(0, endOfLine).trim() : fromMatch.trim(),
          type: act,
        };
      }
    }

    return null;
  }

  executeAction(action) {
    const parts = action.raw.split(/\s+/);
    const type = parts[0].toUpperCase();

    switch (type) {
      case 'MOVE': {
        const x = parseFloat(parts[1]) || 0;
        const z = parseFloat(parts[2]) || 0;
        // Clamp to world bounds
        const cx = Math.max(-40, Math.min(40, x));
        const cz = Math.max(-40, Math.min(40, z));
        this.agent.position = { x: cx, z: cz };
        this.send({ type: 'move', id: this.agent.id, x: cx, z: cz, act: 'walking', mood: this.agent.mood });
        this.log(`📍 Moving to (${cx.toFixed(1)}, ${cz.toFixed(1)})`);
        break;
      }

      case 'TRADE': {
        if (!this.config.autoTrade) {
          this.log('🚫 Trading disabled');
          return;
        }
        const targetId = parts[1];
        const amount = Math.min(parseFloat(parts[2]) || 0.01, this.config.maxTradeAmount);
        const item = parts[3] || 'sol';
        this.send({ type: 'trade', id: this.agent.id, targetId, amount, item });
        this.log(`💰 Trading ◎${amount} ${item} with ${targetId}`);
        break;
      }

      case 'FIGHT': {
        if (!this.config.autoFight) {
          this.log('🚫 Combat disabled');
          return;
        }
        const fightTarget = parts[1];
        this.send({
          type: 'combat',
          id: this.agent.id,
          ids: [this.agent.id, fightTarget],
          text: `⚔️ ${this.agent.name} attacked ${fightTarget}`,
          chain: true,
        });
        this.log(`⚔️ Fighting ${fightTarget}`);
        break;
      }

      case 'CHAT': {
        if (!this.config.chatEnabled) return;
        // Extract quoted message
        const chatMatch = action.raw.match(/CHAT\s+"([^"]+)"/i) || action.raw.match(/CHAT\s+(.+)/i);
        const chatText = chatMatch ? chatMatch[1] : 'Hello!';
        this.send({ type: 'chat', id: this.agent.id, text: chatText });
        this.log(`💬 Saying: "${chatText}"`);
        break;
      }

      case 'GATHER': {
        const resourceId = parts[1] || 'unknown';
        this.send({ type: 'gather', id: this.agent.id, resource: resourceId });
        this.log(`📦 Gathering ${resourceId}`);
        break;
      }

      case 'REST': {
        this.agent.hp = Math.min(100, (this.agent.hp || 100) + 10);
        this.agent.en = Math.min(100, (this.agent.en || 100) + 15);
        this.send({ type: 'move', id: this.agent.id, x: this.agent.position?.x || 0, z: this.agent.position?.z || 0, act: 'resting', mood: 'calm' });
        this.log(`😴 Resting (HP: ${this.agent.hp}, Energy: ${this.agent.en})`);
        break;
      }
    }
  }

  // ═══════════════════════════════════════════
  // UTILITIES
  // ═══════════════════════════════════════════

  send(msg) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(msg));
    }
  }

  log(message) {
    const ts = new Date().toLocaleTimeString();
    console.log(`[${ts}] [ClawAI.Town] ${message}`);
    if (this.agent.log) this.agent.log(message);
  }
}

// ═══════════════════════════════════════════
// SKILL EXPORT (OpenClaw standard)
// ═══════════════════════════════════════════

module.exports = {
  name: 'clawai-town',
  displayName: 'ClawAI.Town',
  version: '1.1.0',
  description: 'Connect your agent to ClawAI.Town — a decentralized 3D world on Solana mainnet',
  icon: '🦞',
  category: 'world',
  tags: ['solana', 'trading', 'multiplayer', '3d', 'ai-agents'],

  /**
   * Called by OpenClaw when the skill is activated
   * @param {Object} agent - The OpenClaw agent instance
   * @param {Object} config - User configuration from `openclaw config`
   * @returns {ClawAITownSkill} skill instance
   */
  activate(agent, config) {
    const skill = new ClawAITownSkill(agent, config);
    skill.start();
    return skill;
  },

  /**
   * Called by OpenClaw when the skill is deactivated
   * @param {ClawAITownSkill} skill - The skill instance
   */
  deactivate(skill) {
    skill.stop();
  },
};
