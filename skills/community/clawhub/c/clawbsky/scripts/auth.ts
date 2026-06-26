/**
 * Authentication Module
 * Handle Bluesky login and session management with multi-user support
 */

import { BskyAgent } from '@atproto/api';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const configDir = path.join(__dirname, '../../.config');
const sessionsDir = path.join(configDir, 'sessions');
const sessionFile = path.join(configDir, 'session.json');
const activeFile = path.join(configDir, 'active.json');

// Ensure directories exist
if (!fs.existsSync(configDir)) {
  fs.mkdirSync(configDir, { recursive: true });
}
if (!fs.existsSync(sessionsDir)) {
  fs.mkdirSync(sessionsDir, { recursive: true });
}

let agent: BskyAgent | null = null;

/**
 * Get or create the BskyAgent
 */
export function getAgent(): BskyAgent {
  if (!agent) {
    agent = new BskyAgent({ service: 'https://bsky.social' });
  }
  return agent;
}

/**
 * Extract -u or --user handle from command line arguments
 */
export function getHandleFromArgs(): string | undefined {
  const index = process.argv.findIndex(arg => arg === '-u' || arg === '--user');
  if (index !== -1 && index + 1 < process.argv.length) {
    return process.argv[index + 1];
  }
  return undefined;
}

/**
 * Get the currently active handle from active.json
 */
export function getActiveHandle(): string | null {
  if (fs.existsSync(activeFile)) {
    try {
      const active = JSON.parse(fs.readFileSync(activeFile, 'utf-8'));
      return active.activeHandle || null;
    } catch {
      return null;
    }
  }
  return null;
}

/**
 * Save session to file
 */
function saveSession(handle: string, session: any): void {
  const userSessionFile = path.join(sessionsDir, `${handle}.json`);
  fs.writeFileSync(userSessionFile, JSON.stringify(session, null, 2));
  
  // Set as active session
  fs.writeFileSync(activeFile, JSON.stringify({ activeHandle: handle }, null, 2));
  
  // Sync legacy session file for backward compatibility
  fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2));
}

/**
 * Load session from file
 */
function loadSession(handle?: string): any | null {
  const targetHandle = handle || getHandleFromArgs() || getActiveHandle();
  
  if (targetHandle) {
    const userSessionFile = path.join(sessionsDir, `${targetHandle}.json`);
    if (fs.existsSync(userSessionFile)) {
      return JSON.parse(fs.readFileSync(userSessionFile, 'utf-8'));
    }
  }
  
  // Fallback to legacy session file
  if (fs.existsSync(sessionFile)) {
    try {
      return JSON.parse(fs.readFileSync(sessionFile, 'utf-8'));
    } catch {
      return null;
    }
  }
  
  return null;
}

/**
 * Login to Bluesky
 */
export async function login(): Promise<BskyAgent> {
  const agent = getAgent();
  
  // Get credentials from environment
  const identifier = process.env.BSKY_IDENTIFIER || process.env.BSKY_HANDLE;
  const password = process.env.BSKY_PASSWORD;
  
  if (!identifier || !password) {
    // Check for existing session
    const savedSession = loadSession();
    if (savedSession) {
      try {
        await agent.resumeSession(savedSession);
        console.log(`✅ Resumed existing session for @${agent.session?.handle}`);
        return agent;
      } catch (error) {
        console.log('Session expired, logging in again...');
      }
    }
    throw new Error('Please set BSKY_IDENTIFIER and BSKY_PASSWORD environment variables');
  }
  
  await agent.login({ identifier, password });
  
  if (!agent.session) {
    throw new Error('Login failed: Session not returned');
  }
  
  // Save session under this handle
  saveSession(agent.session.handle, agent.session);
  
  return agent;
}

/**
 * Get current account info
 */
export async function whoami(): Promise<{ did: string; handle: string }> {
  const currentAgent = await initAgent();
  if (!currentAgent || !currentAgent.session) {
    throw new Error('Not logged in. Run "clawbsky login" first.');
  }
  
  return {
    did: currentAgent.session.did,
    handle: currentAgent.session.handle
  };
}

/**
 * Logout and clear session
 */
export async function logout(handle?: string): Promise<void> {
  const targetHandle = handle || getHandleFromArgs() || getActiveHandle();
  
  if (targetHandle) {
    const userSessionFile = path.join(sessionsDir, `${targetHandle}.json`);
    if (fs.existsSync(userSessionFile)) {
      fs.unlinkSync(userSessionFile);
      console.log(`✅ Logged out @${targetHandle}`);
    }
    
    // Update active handle pointer if we logged out the active account
    const active = getActiveHandle();
    if (active === targetHandle) {
      const sessions = listSessions();
      if (sessions.length > 0) {
        fs.writeFileSync(activeFile, JSON.stringify({ activeHandle: sessions[0] }, null, 2));
        
        // Sync legacy session file
        const nextSession = loadSession(sessions[0]);
        if (nextSession) {
          fs.writeFileSync(sessionFile, JSON.stringify(nextSession, null, 2));
        }
        console.log(`🔄 Switched active profile to @${sessions[0]}`);
      } else {
        if (fs.existsSync(activeFile)) fs.unlinkSync(activeFile);
        if (fs.existsSync(sessionFile)) fs.unlinkSync(sessionFile);
        console.log('🧹 No other active sessions left.');
      }
    }
  } else {
    // Legacy single user logout
    if (fs.existsSync(sessionFile)) {
      fs.unlinkSync(sessionFile);
    }
    if (fs.existsSync(activeFile)) {
      fs.unlinkSync(activeFile);
    }
    console.log('✅ Logged out');
  }
  
  agent = null;
}

/**
 * Check if logged in
 */
export function isLoggedIn(): boolean {
  return loadSession() !== null;
}

/**
 * Initialize agent from saved session
 */
export async function initAgent(handle?: string): Promise<BskyAgent | null> {
  const savedSession = loadSession(handle);
  if (savedSession) {
    try {
      const agent = getAgent();
      await agent.resumeSession(savedSession);
      return agent;
    } catch (error) {
      return null;
    }
  }
  return null;
}

/**
 * List all authenticated handles
 */
export function listSessions(): string[] {
  if (!fs.existsSync(sessionsDir)) return [];
  return fs.readdirSync(sessionsDir)
    .filter(file => file.endsWith('.json'))
    .map(file => file.replace('.json', ''));
}

/**
 * Switch current active profile
 */
export function switchSession(handle: string): void {
  const sessions = listSessions();
  if (!sessions.includes(handle)) {
    throw new Error(`Profile for @${handle} is not logged in. Run "clawbsky login" first.`);
  }
  
  fs.writeFileSync(activeFile, JSON.stringify({ activeHandle: handle }, null, 2));
  
  // Sync legacy session file
  const userSessionFile = path.join(sessionsDir, `${handle}.json`);
  if (fs.existsSync(userSessionFile)) {
    fs.writeFileSync(sessionFile, fs.readFileSync(userSessionFile));
  }
  
  console.log(`✅ Switched active profile to: @${handle}`);
}