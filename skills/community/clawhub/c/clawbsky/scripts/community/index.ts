/**
 * Community Management Module
 * List Management, Mute/Unmute Bulk, Welcome New Followers, Follower Cleanup
 */

import { BskyAgent } from '@atproto/api';
import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const db = new Database(path.join(__dirname, '../../data/community.db'));

// Initialize community management tables
db.exec(`
  CREATE TABLE IF NOT EXISTS lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT DEFAULT 'curated',
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS list_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listId INTEGER NOT NULL,
    did TEXT NOT NULL,
    addedAt TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listId) REFERENCES lists(id),
    UNIQUE(listId, did)
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS muted_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    did TEXT UNIQUE NOT NULL,
    reason TEXT,
    mutedAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS follower_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    did TEXT UNIQUE NOT NULL,
    handle TEXT NOT NULL,
    followedAt TEXT,
    lastSeenAt TEXT DEFAULT CURRENT_TIMESTAMP,
    isActive INTEGER DEFAULT 1
  )
`);

// ============== LIST MANAGEMENT ==============

/**
 * Create a new list
 */
export function createList(name: string, description?: string, type: 'curated' | 'private' = 'curated'): number {
  const stmt = db.prepare('INSERT INTO lists (name, description, type) VALUES (?, ?, ?)');
  const result = stmt.run(name, description || '', type);
  return result.lastInsertRowid as number;
}

/**
 * Get all lists
 */
export function getLists(): any[] {
  const stmt = db.prepare(`
    SELECT l.*, 
           (SELECT COUNT(*) FROM list_members WHERE listId = l.id) as memberCount
    FROM lists l
    ORDER BY l.createdAt DESC
  `);
  return stmt.all();
}

/**
 * Add user to a list
 */
export function addToList(listId: number, did: string): void {
  const stmt = db.prepare('INSERT OR IGNORE INTO list_members (listId, did) VALUES (?, ?)');
  stmt.run(listId, did);
}

/**
 * Remove user from a list
 */
export function removeFromList(listId: number, did: string): void {
  const stmt = db.prepare('DELETE FROM list_members WHERE listId = ? AND did = ?');
  stmt.run(listId, did);
}

/**
 * Get list members
 */
export function getListMembers(listId: number): any[] {
  const stmt = db.prepare(`
    SELECT lm.*, 
           p.displayName, p.handle, p.description, p.avatar
    FROM list_members lm
    LEFT JOIN profile_cache p ON lm.did = p.did
    WHERE lm.listId = ?
    ORDER BY lm.addedAt DESC
  `);
  return stmt.all(listId);
}

/**
 * Create a list from search (bulk add)
 */
export function createListFromSearch(name: string, handles: string[]): number {
  const listId = createList(name);
  
  // Note: Need to resolve handles to DIDs first
  // This is a placeholder - real implementation would use agent.resolveHandle()
  
  return listId;
}

// ============== MUTE/UNMUTE BULK ==============

/**
 * Bulk mute users
 */
export async function bulkMute(agent: BskyAgent, dids: string[], reason?: string): Promise<{
  succeeded: number;
  failed: number;
}> {
  let succeeded = 0;
  let failed = 0;
  
  for (const did of dids) {
    try {
      await agent.app.bsky.graph.muteActor({ actor: did });
      
      // Track in database
      const stmt = db.prepare('INSERT OR IGNORE INTO muted_users (did, reason) VALUES (?, ?)');
      stmt.run(did, reason || 'bulk mute');
      
      succeeded++;
    } catch (error) {
      failed++;
    }
  }
  
  return { succeeded, failed };
}

/**
 * Bulk unmute users
 */
export async function bulkUnmute(agent: BskyAgent, dids: string[]): Promise<{
  succeeded: number;
  failed: number;
}> {
  let succeeded = 0;
  let failed = 0;
  
  for (const did of dids) {
    try {
      await agent.app.bsky.graph.unmuteActor({ actor: did });
      
      // Remove from database
      const stmt = db.prepare('DELETE FROM muted_users WHERE did = ?');
      stmt.run(did);
      
      succeeded++;
    } catch (error) {
      failed++;
    }
  }
  
  return { succeeded, failed };
}

/**
 * Get muted users
 */
export function getMutedUsers(): any[] {
  const stmt = db.prepare('SELECT * FROM muted_users ORDER BY mutedAt DESC');
  return stmt.all();
}

// ============== FOLLOWER CLEANUP ==============

/**
 * Track a follower
 */
export function trackFollower(did: string, handle: string): void {
  const stmt = db.prepare(`
    INSERT INTO follower_tracking (did, handle, followedAt, lastSeenAt, isActive)
    VALUES (?, ?, datetime('now'), datetime('now'), 1)
    ON CONFLICT(did) DO UPDATE SET lastSeenAt = datetime('now'), isActive = 1
  `);
  stmt.run(did, handle);
}

/**
 * Mark follower as inactive
 */
export function markInactive(did: string): void {
  const stmt = db.prepare('UPDATE follower_tracking SET isActive = 0 WHERE did = ?');
  stmt.run(did);
}

/**
 * Get inactive followers
 */
export function getInactiveFollowers(days: number = 30): any[] {
  const stmt = db.prepare(`
    SELECT * FROM follower_tracking 
    WHERE isActive = 0 
    OR julianday('now') - julianday(lastSeenAt) > ?
    ORDER BY lastSeenAt ASC
  `);
  return stmt.all(days);
}

/**
 * Identify inactive followers (based on their last post)
 */
export async function findInactiveFollowers(agent: BskyAgent): Promise<string[]> {
  // Get followers
  const followers = await agent.getFollowers({ actor: agent.did });
  
  const inactive = [];
  
  for (const follower of followers.data.followers) {
    try {
      // Get their recent posts
      const posts = await agent.getAuthorFeed({ actor: follower.did, limit: 1 });
      
      if (posts.data.feed.length === 0) {
        inactive.push(follower.did);
      } else {
        const lastPost = posts.data.feed[0].post;
        const lastPostDate = new Date(lastPost.indexedAt);
        const daysSince = (Date.now() - lastPostDate.getTime()) / (1000 * 60 * 60 * 24);
        
        if (daysSince > 90) {
          inactive.push(follower.did);
        }
      }
    } catch (error) {
      // If we can't get posts, consider them inactive
      inactive.push(follower.did);
    }
  }
  
  return inactive;
}

/**
 * Bulk unfollow inactive
 */
export async function cleanupInactiveFollowers(
  agent: BskyAgent, 
  dryRun: boolean = true
): Promise<{ toUnfollow: number; details: any[] }> {
  const inactive = await findInactiveFollowers(agent);
  
  if (dryRun) {
    return { toUnfollow: inactive.length, details: [] };
  }
  
  let unfollowed = 0;
  for (const did of inactive) {
    try {
      await agent.deleteFollow(did);
      unfollowed++;
    } catch (error) {
      console.error('Failed to unfollow:', did);
    }
  }
  
  return { toUnfollow: unfollowed, details: [] };
}