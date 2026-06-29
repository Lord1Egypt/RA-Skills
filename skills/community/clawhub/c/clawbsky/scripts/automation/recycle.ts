/**
 * Recycle Posts Module
 * Automatically repost top-performing content
 */

import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dbDir = path.join(__dirname, '../../data');
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}
const db = new Database(path.join(dbDir, 'recycle.db'));

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS recycled_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    originalUri TEXT NOT NULL,
    originalCid TEXT NOT NULL,
    originalText TEXT NOT NULL,
    originalEngagement INTEGER DEFAULT 0,
    recycledCount INTEGER DEFAULT 0,
    lastRecycledAt TEXT,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS recycle_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    minEngagement INTEGER DEFAULT 100,
    recycleAfterDays INTEGER DEFAULT 30,
    maxRecycles INTEGER DEFAULT 3,
    enabled INTEGER DEFAULT 1
  )
`);

// Default rules
const defaultRules = {
  minEngagement: 100,
  recycleAfterDays: 30,
  maxRecycles: 3,
  enabled: 1
};

/**
 * Track a post for recycling
 */
export function trackPost(
  uri: string,
  cid: string,
  text: string,
  engagement: number = 0
): void {
  const stmt = db.prepare(`
    INSERT OR REPLACE INTO recycled_posts (originalUri, originalCid, originalText, originalEngagement, recycledCount)
    VALUES (?, ?, ?, ?, 0)
  `);
  
  stmt.run(uri, cid, text, engagement);
}

/**
 * Get posts eligible for recycling
 */
export function getRecyclablePosts(): any[] {
  const stmt = db.prepare(`
    SELECT * FROM recycled_posts
    WHERE recycledCount < 3
    AND julianday('now') - julianday(createdAt) >= 30
    AND originalEngagement >= 100
    ORDER BY originalEngagement DESC
  `);
  
  return stmt.all();
}

/**
 * Mark a post as recycled
 */
export function markRecycled(uri: string): void {
  const stmt = db.prepare(`
    UPDATE recycled_posts 
    SET recycledCount = recycledCount + 1, 
        lastRecycledAt = datetime('now')
    WHERE originalUri = ?
  `);
  
  stmt.run(uri);
}

/**
 * Get recycle rules
 */
export function getRecycleRules(): any {
  const stmt = db.prepare('SELECT * FROM recycle_rules LIMIT 1');
  const rules = stmt.get();
  
  return rules || defaultRules;
}

/**
 * Update recycle rules
 */
export function updateRecycleRules(rules: {
  minEngagement?: number;
  recycleAfterDays?: number;
  maxRecycles?: number;
}): void {
  const current = getRecycleRules();
  const merged = { ...current, ...rules };
  
  const stmt = db.prepare(`
    INSERT OR REPLACE INTO recycle_rules (id, minEngagement, recycleAfterDays, maxRecycles, enabled)
    VALUES (1, ?, ?, ?, ?)
  `);
  
  stmt.run(
    merged.minEngagement,
    merged.recycleAfterDays,
    merged.maxRecycles,
    merged.enabled
  );
}

/**
 * AI generates new variation of post
 */
export async function generatePostVariation(originalText: string): Promise<string> {
  const { getOllamaClient } = await import('../llm.js');
  const ollama = getOllamaClient();
  
  const prompt = `Generate a new variation of this Bluesky post. 
Keep the same meaning but use different words and phrasing.
Add new hashtags if appropriate.
Keep it under 280 characters.

Original: "${originalText}"

New variation:`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    console.error('Error generating post variation:', error);
    return originalText; // Fallback to original
  }
}

/**
 * Get recycled post stats
 */
export function getRecycleStats(): { totalRecycled: number; postsTracked: number; avgEngagement: number } {
  const stmt = db.prepare(`
    SELECT 
      SUM(recycledCount) as totalRecycled,
      COUNT(*) as postsTracked,
      AVG(originalEngagement) as avgEngagement
    FROM recycled_posts
  `);
  
  const result = stmt.get() as any;
  
  return {
    totalRecycled: result?.totalRecycled || 0,
    postsTracked: result?.postsTracked || 0,
    avgEngagement: Math.round(result?.avgEngagement || 0)
  };
}