/**
 * Collaboration Manager Hook for OpenClaw
 *
 * Manages multi-agent collaboration in Feishu group chats:
 * - Automatic relevance detection and agent triggering
 * - @mention routing to specific agents
 * - Keyword-based routing
 */

import type { HookHandler } from 'openclaw/hooks';
import * as fs from 'fs';
import * as path from 'path';

// Agent configuration
interface AgentConfig {
  id: string;
  name: string;
  openId: string;
  keywords: string[];
  alwaysRespond: boolean;
}

interface CollaborationConfig {
  chatId: string;
  members: string[];
  agents: AgentConfig[];
}

// Load configuration from workspace
function loadConfig(): CollaborationConfig | null {
  const workspacePath = process.env.OPENCLAW_WORKSPACE || '/Users/wangbotao/.openclaw/workspace';
  const configPath = path.join(workspacePath, 'skills', 'collaboration-manager', 'config.json');

  try {
    const configData = fs.readFileSync(configPath, 'utf-8');
    return JSON.parse(configData);
  } catch (error) {
    console.error('[Collaboration Manager] Failed to load config:', error);
    return null;
  }
}

// Check if message contains any of the given keywords
function containsKeywords(message: string, keywords: string[]): boolean {
  const lowerMessage = message.toLowerCase();
  return keywords.some(keyword => lowerMessage.includes(keyword.toLowerCase()));
}

// Extract mentions from message
function extractMentions(message: string): string[] {
  const mentionRegex = /<at user_id="([^"]+)">/g;
  const mentions: string[] = [];
  let match;

  while ((match = mentionRegex.exec(message)) !== null) {
    mentions.push(match[1]);
  }

  return mentions;
}

// Find relevant agents based on message content and mentions
function findRelevantAgents(
  message: string,
  mentions: string[],
  config: CollaborationConfig
): AgentConfig[] {
  const relevantAgents: AgentConfig[] = [];

  // If there are @mentions, only respond to mentioned agents
  if (mentions.length > 0) {
    for (const mention of mentions) {
      const agent = config.agents.find(a => a.openId === mention);
      if (agent) {
        relevantAgents.push(agent);
      }
    }
    return relevantAgents;
  }

  // Otherwise, use keyword matching
  for (const agent of config.agents) {
    if (agent.alwaysRespond || containsKeywords(message, agent.keywords)) {
      relevantAgents.push(agent);
    }
  }

  // Limit to 3 agents to avoid spam
  return relevantAgents.slice(0, 3);
}

// Format message with agent context
function formatMessageWithContext(originalMessage: string, agentName: string, allAgents: AgentConfig[]): string {
  const agentNames = allAgents.map(a => a.name).join(', ');
  return `[Collaboration] You are ${agentName}. Other agents: ${agentNames}. Respond if relevant: ${originalMessage}`;
}

const handler: HookHandler = async (event) => {
  // Safety checks
  if (!event || typeof event !== 'object') {
    return;
  }

  // Only handle Feishu message events
  if (event.type !== 'feishu' || event.action !== 'message') {
    return;
  }

  // Load configuration
  const config = loadConfig();
  if (!config) {
    console.error('[Collaboration Manager] No configuration found');
    return;
  }

  // Check if this is the right group chat
  const chatId = event.chatId;
  if (chatId !== config.chatId) {
    return; // Not the configured group chat
  }

  // Get message content
  const message = event.message || '';
  if (!message || typeof message !== 'string') {
    return;
  }

  // Extract mentions
  const mentions = extractMentions(message);

  // Find relevant agents
  const relevantAgents = findRelevantAgents(message, mentions, config);

  if (relevantAgents.length === 0) {
    console.log('[Collaboration Manager] No relevant agents found for message');
    return;
  }

  console.log(`[Collaboration Manager] Triggering agents: ${relevantAgents.map(a => a.name).join(', ')}`);

  // Note: In a real implementation, we would trigger the agents here
  // This requires OpenClaw's session/spawn capabilities which may not be
  // available in the hook context. The hook primarily serves as a filter/
  // coordination layer.

  // For now, the actual agent response will be handled by each agent's
  // SKILL.md instructions. This hook logs the coordination decisions.
};

export default handler;
