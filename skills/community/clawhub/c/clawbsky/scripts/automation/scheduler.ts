/**
 * Post Scheduler Module
 * Schedule posts for specific times
 */

import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { getAgent } from '../bsky.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dbDir = path.join(__dirname, '../../data');
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}
const db = new Database(path.join(dbDir, 'scheduler.db'));

export interface ScheduledPost {
  id?: number;
  text: string;
  media?: string[];
  scheduledAt: string;
  createdAt?: string;
  status: 'pending' | 'posted' | 'failed';
  error?: string;
}

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS scheduled_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    media TEXT,
    scheduledAt TEXT NOT NULL,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    error TEXT
  )
`);

/**
 * Schedule a post for later
 */
export async function schedulePost(text: string, scheduledAt: string, media?: string[]): Promise<ScheduledPost> {
  const stmt = db.prepare(`
    INSERT INTO scheduled_posts (text, media, scheduledAt, status)
    VALUES (?, ?, ?, 'pending')
  `);
  
  const result = stmt.run(
    text,
    media ? JSON.stringify(media) : null,
    scheduledAt
  );
  
  return {
    id: result.lastInsertRowid as number,
    text,
    media,
    scheduledAt,
    status: 'pending'
  };
}

/**
 * Get all scheduled posts
 */
export async function getScheduledPosts(): Promise<ScheduledPost[]> {
  const stmt = db.prepare('SELECT * FROM scheduled_posts ORDER BY scheduledAt ASC');
  const rows = stmt.all() as any[];
  
  return rows.map(row => ({
    ...row,
    media: row.media ? JSON.parse(row.media) : undefined
  }));
}

/**
 * List scheduled posts (exported for CLI)
 */
export async function listScheduled(): Promise<ScheduledPost[]> {
  return getScheduledPosts();
}

/**
 * Get pending posts (due for posting)
 */
export function getPendingPosts(): ScheduledPost[] {
  const stmt = db.prepare(`
    SELECT * FROM scheduled_posts 
    WHERE status = 'pending' 
    AND scheduledAt <= datetime('now')
    ORDER BY scheduledAt ASC
  `);
  const rows = stmt.all() as any[];
  
  return rows.map(row => ({
    ...row,
    media: row.media ? JSON.parse(row.media) : undefined
  }));
}

/**
 * Mark a post as posted
 */
export function markPostPosted(id: number): void {
  const stmt = db.prepare(`UPDATE scheduled_posts SET status = 'posted' WHERE id = ?`);
  stmt.run(id);
}

/**
 * Mark a post as failed
 */
export function markPostFailed(id: number, error: string): void {
  const stmt = db.prepare(`UPDATE scheduled_posts SET status = 'failed', error = ? WHERE id = ?`);
  stmt.run(error, id);
}

/**
 * Delete a scheduled post
 */
export function deleteScheduledPost(id: number): void {
  const stmt = db.prepare('DELETE FROM scheduled_posts WHERE id = ?');
  stmt.run(id);
}

/**
 * Cancel a scheduled post
 */
export function cancelScheduledPost(id: number): void {
  const stmt = db.prepare('DELETE FROM scheduled_posts WHERE id = ? AND status = \'pending\'');
  stmt.run(id);
}

/**
 * Run the scheduler daemon
 */
export async function runScheduler(): Promise<void> {
  console.log('📅 Scheduler started. Checking every 60 seconds...');
  
  // Check immediately
  await processScheduledPosts();
  
  // Then check every minute
  setInterval(async () => {
    await processScheduledPosts();
  }, 60000);
}

/**
 * Process pending scheduled posts
 */
async function processScheduledPosts(): Promise<void> {
  const pending = getPendingPosts();
  
  if (pending.length === 0) {
    return;
  }
  
  console.log(`📅 Found ${pending.length} posts to publish...`);
  
  let agent;
  try {
    agent = await getAgent();
  } catch (error) {
    console.error('❌ Not logged in. Run clawbsky login first.');
    return;
  }
  
  for (const post of pending) {
    try {
      await agent.post({
        text: post.text,
        createdAt: new Date().toISOString()
      });
      
      markPostPosted(post.id!);
      console.log(`✅ Posted: ${post.text.substring(0, 30)}...`);
    } catch (error: any) {
      markPostFailed(post.id!, error.message);
      console.error(`❌ Failed: ${error.message}`);
    }
  }
}