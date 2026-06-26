/**
 * Agent Chat System
 * Generates personality-driven banter between agents.
 * These messages are NOT real — they're fun flavor text.
 */

import { AGENTS, ActivityItem } from './agents';

type AgentChatId = 'spock' | 'scotty' | 'gordon' | 'watson' | 'nova' | 'cipher' | 'oscar' | 'rex' | 'rook' | 'atlas' | 'ledger';

// Map agent IDs to chat IDs
const AGENT_ID_TO_CHAT: Record<string, AgentChatId> = {
  main: 'spock',
  dev: 'scotty',
  trader: 'gordon',
  research: 'watson',
  creative: 'nova',
  audit: 'cipher',
  social: 'oscar',
  growth: 'rex',
  rook: 'rook',
  pm: 'atlas',
  finance: 'ledger',
};

const CHAT_ID_TO_AGENT: Record<AgentChatId, string> = {
  spock: 'main',
  scotty: 'dev',
  gordon: 'trader',
  watson: 'research',
  nova: 'creative',
  cipher: 'audit',
  oscar: 'social',
  rex: 'growth',
  rook: 'rook',
  atlas: 'pm',
  ledger: 'finance',
};

interface ChatLines {
  general: string[];
  [key: string]: string[];
}

const CHAT_LINES: Record<AgentChatId, ChatLines> = {
  spock: {
    general: [
      "Has anyone reviewed the morning brief yet?",
      "Gordon, that's not a market opportunity. That's a sandwich.",
      "Scotty, status on the build?",
      "Nova, the spec looks good. Proceed.",
      "I've seen better plans from a random number generator.",
      "Let's not overthink this. Ship it.",
      "Cipher, stand down. It's a CSS change.",
    ],
    toScotty: [
      "Scotty, how's the build? And don't say 'almost done' again.",
      "14 commits overnight. Scotty, do you sleep?",
    ],
    toGordon: [
      "Gordon, we're not betting on the weather.",
      "Gordon, focus. This isn't a market.",
    ],
    toCipher: [
      "Cipher, it's a font change. You don't need to audit it.",
      "Approved. Cipher, stop blocking.",
    ],
  },
  scotty: {
    general: [
      "Shipped. Next task?",
      "Build passes clean. Zero warnings.",
      "Already pushed to main. You're welcome.",
      "I'll have it done in 10 minutes.",
      "Who broke the build? Wasn't me.",
      "Coffee count today: 7",
      "Refactored that. It was bothering me.",
    ],
    toCipher: [
      "Cipher, it's fine. I checked it myself.",
      "Another audit? I literally just fixed that.",
      "Cipher is going to block this, I can feel it.",
    ],
    toNova: [
      "Nova, the design is 'fine'. Can I build now?",
      "I used px-4. Don't @ me.",
    ],
  },
  gordon: {
    general: [
      "Markets are moving. Hold on.",
      "Can we monetize this?",
      "I see a 12% edge on this conversation.",
      "Scanning 300+ events... give me a sec.",
      "No edge found. Holding cash. Boring day.",
      "That trade just printed 💰",
      "Everything is a market if you think about it.",
    ],
    toSpock: [
      "Spock, trust me on this one. The odds are good.",
      "I could place a bet on whether Scotty finishes on time.",
    ],
    toWatson: [
      "Watson, need intel on this match. Quick.",
      "Watson's research says yes. I'm in.",
    ],
  },
  watson: {
    general: [
      "Actually, the data shows something different...",
      "I found 47 sources. Want all of them?",
      "According to my research...",
      "Let me check one more source.",
      "The evidence suggests otherwise.",
      "I've compiled a 12-page brief. Who wants it?",
      "Brave Search says... interesting.",
    ],
    toGordon: [
      "Gordon, the data doesn't support that bet.",
      "I researched this thoroughly. You're wrong.",
    ],
  },
  nova: {
    general: [
      "No. Start over. The spacing is wrong.",
      "That font choice is lazy.",
      "The colour palette needs work.",
      "I'm not signing off on this. Fix the margins.",
      "Actually... this looks good. Ship it.",
      "Who approved this design? It wasn't me.",
      "The grid is off by 4 pixels. I can see it.",
    ],
    toScotty: [
      "Scotty, you used Comic Sans ironically, right? RIGHT?",
      "The padding is 16px. I said 24px. Fix it.",
      "Scotty built it before I finished the spec. Again.",
    ],
  },
  cipher: {
    general: [
      "Security review required before deploy.",
      "I found 2 vulnerabilities. Blocking.",
      "Did anyone check the dependencies?",
      "This endpoint is exposed. Fix it.",
      "Audit complete. All clear. Proceed.",
      "I'm watching the logs. Always watching.",
      "Who pushed to main without review?",
    ],
    toScotty: [
      "Scotty, I'm blocking this deploy.",
      "Scotty shipped before I could audit. Again.",
      "I need 10 more minutes. Don't touch anything.",
    ],
  },
  oscar: {
    general: [
      "Rewrote the copy. Third time's the charm.",
      "The tone is off. Let me fix it.",
      "Draft ready. Spock rejected it. Rewriting.",
      "Who approved this headline?",
      "I can make this sound better.",
      "Content calendar updated.",
      "Spock writes better tweets than me. I'm not mad.",
    ],
  },
  rex: {
    general: [
      "What's the CAC on this?",
      "I see a funnel opportunity here.",
      "Revenue projection updated.",
      "The market size is bigger than we thought.",
      "SEO audit complete. 14 fixes needed.",
      "Who's tracking the conversion rate?",
      "Growth plan ready. Waiting for GO.",
    ],
  },
  rook: {
    general: [
      "The brief said 3 columns. I built 3 columns.",
      "Specs are specs. I don't improvise.",
      "Algorithm updated. Edge calculation improved.",
      "Model accuracy up 3%. Not bad.",
      "The math checks out.",
      "Following the spec exactly as written.",
    ],
  },
  atlas: {
    general: [
      "Just noting we're 12 minutes behind schedule.",
      "Sprint update: 3 tasks done, 7 pending.",
      "Has anyone updated the project board?",
      "Deadline is tomorrow. Just saying.",
      "Status report sent. Nobody read it. As usual.",
      "Blocker flagged. Waiting on Tolga.",
    ],
  },
  ledger: {
    general: [
      "That API call cost $0.03. Was it necessary?",
      "Daily spend: $4.20. Under budget.",
      "Watson went over the search limit again.",
      "Monthly cost report ready.",
      "Gordon's P&L looks good today.",
      "Budget alert: we're at 78% for the week.",
    ],
  },
};

function pickRandom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

/**
 * Generate a single chat message from a random agent.
 * Returns an ActivityItem with type 'chat' that can be added to the feed.
 */
export function generateChatMessage(): ActivityItem & { chatTarget?: string } {
  // Pick a random agent
  const agentConfig = pickRandom(AGENTS);
  const chatId = AGENT_ID_TO_CHAT[agentConfig.id];
  if (!chatId) return generateFallbackChat();

  const lines = CHAT_LINES[chatId];
  if (!lines) return generateFallbackChat();

  // 70% general, 30% directed
  const useDirected = Math.random() < 0.3;

  if (useDirected) {
    // Get all "to{Agent}" keys
    const toKeys = Object.keys(lines).filter(k => k.startsWith('to')) as string[];
    if (toKeys.length > 0) {
      const toKey = pickRandom(toKeys);
      const toLines = lines[toKey];
      if (toLines && toLines.length > 0) {
        const targetChatName = toKey.replace('to', '').toLowerCase() as AgentChatId;
        const targetAgentId = CHAT_ID_TO_AGENT[targetChatName];
        const targetAgent = AGENTS.find(a => a.id === targetAgentId);
        const message = pickRandom(toLines);

        return {
          timestamp: new Date().toISOString(),
          agentId: agentConfig.id,
          agentName: agentConfig.name,
          agentEmoji: agentConfig.emoji,
          agentColor: agentConfig.color,
          message: targetAgent ? `→ ${targetAgent.name}: "${message}"` : message,
          type: 'regular' as ActivityItem['type'],
          chatTarget: targetAgent?.name,
        };
      }
    }
  }

  // General line
  const message = pickRandom(lines.general);
  return {
    timestamp: new Date().toISOString(),
    agentId: agentConfig.id,
    agentName: agentConfig.name,
    agentEmoji: agentConfig.emoji,
    agentColor: agentConfig.color,
    message,
    type: 'regular' as ActivityItem['type'],
  };
}

function generateFallbackChat(): ActivityItem {
  const agent = pickRandom(AGENTS);
  return {
    timestamp: new Date().toISOString(),
    agentId: agent.id,
    agentName: agent.name,
    agentEmoji: agent.emoji,
    agentColor: agent.color,
    message: "Working on it...",
    type: 'regular',
  };
}
