/**
 * Bluesky Agent Helper
 */

import { BskyAgent } from '@atproto/api';
import { initAgent } from './auth.js';

let agent: BskyAgent | null = null;

/**
 * Get or initialize the Bluesky agent
 */
export async function getAgent(): Promise<BskyAgent> {
  if (!agent) {
    agent = await initAgent();
    if (!agent) {
      throw new Error('Not logged in. Run "clawbsky login" first.');
    }
  }
  return agent;
}

/**
 * Get agent synchronously (for authenticated commands)
 */
export function getAgentSync(): BskyAgent {
  if (!agent) {
    throw new Error('Agent not initialized. Call getAgent() first.');
  }
  return agent;
}

/**
 * Set the agent instance
 */
export function setAgent(newAgent: BskyAgent): void {
  agent = newAgent;
}