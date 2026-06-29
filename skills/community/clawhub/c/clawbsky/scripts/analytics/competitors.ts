/**
 * Competitor Analysis Module
 * Track rival accounts and analyze their strategies
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
const db = new Database(path.join(dbDir, 'competitors.db'));

// Initialize competitor tracking
db.exec(`
  CREATE TABLE IF NOT EXISTS competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT UNIQUE NOT NULL,
    displayName TEXT,
    lastAnalyzed TEXT,
    notes TEXT
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS competitor_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitorId INTEGER NOT NULL,
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    posts INTEGER DEFAULT 0,
    engagementRate REAL DEFAULT 0,
    avgLikes INTEGER DEFAULT 0,
    avgReposts INTEGER DEFAULT 0,
    recordedAt TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (competitorId) REFERENCES competitors(id)
  )
`);

/**
 * Add a competitor to track
 */
export function addCompetitor(handle: string, displayName?: string, notes?: string): number {
  // Remove @ if present
  const cleanHandle = handle.replace(/^@/, '');
  
  const stmt = db.prepare(`
    INSERT INTO competitors (handle, displayName, notes)
    VALUES (?, ?, ?)
  `);
  
  try {
    const result = stmt.run(cleanHandle, displayName || cleanHandle, notes || '');
    return result.lastInsertRowid as number;
  } catch (error) {
    // Already exists
    return -1;
  }
}

/**
 * Get all competitors
 */
export function getCompetitors(): any[] {
  const stmt = db.prepare(`
    SELECT c.*, 
           cs.followers as currentFollowers,
           cs.posts as currentPosts,
           cs.engagementRate,
           cs.recordedAt as lastSnapshot
    FROM competitors c
    LEFT JOIN (
      SELECT competitorId, followers, posts, engagementRate, recordedAt
      FROM competitor_snapshots
      WHERE id IN (SELECT MAX(id) FROM competitor_snapshots GROUP BY competitorId)
    ) cs ON c.id = cs.competitorId
    ORDER BY cs.followers DESC
  `);
  
  return stmt.all();
}

/**
 * Record a snapshot of competitor stats
 */
export function recordSnapshot(
  competitorId: number,
  stats: {
    followers: number;
    following: number;
    posts: number;
    engagementRate: number;
    avgLikes: number;
    avgReposts: number;
  }
): void {
  const stmt = db.prepare(`
    INSERT INTO competitor_snapshots 
    (competitorId, followers, following, posts, engagementRate, avgLikes, avgReposts)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);
  
  stmt.run(
    competitorId,
    stats.followers,
    stats.following,
    stats.posts,
    stats.engagementRate,
    stats.avgLikes,
    stats.avgReposts
  );
}

/**
 * Get competitor history
 */
export function getCompetitorHistory(handle: string, days: number = 30): any[] {
  const cleanHandle = handle.replace(/^@/, '');
  
  const stmt = db.prepare(`
    SELECT cs.*
    FROM competitor_snapshots cs
    JOIN competitors c ON cs.competitorId = c.id
    WHERE c.handle = ? AND julianday('now') - julianday(cs.recordedAt) <= ?
    ORDER BY cs.recordedAt ASC
  `);
  
  return stmt.all(cleanHandle, days);
}

/**
 * Get growth comparison
 */
export function getGrowthComparison(competitorHandles: string[]): any[] {
  const comparison = [];
  
  for (const handle of competitorHandles) {
    const history = getCompetitorHistory(handle, 30);
    
    if (history.length >= 2) {
      const first = history[0];
      const last = history[history.length - 1];
      
      comparison.push({
        handle,
        followerGrowth: last.followers - first.followers,
        followerGrowthPercent: first.followers > 0 
          ? Math.round(((last.followers - first.followers) / first.followers) * 100)
          : 0,
        avgEngagement: last.engagementRate,
        postFrequency: history.length
      });
    }
  }
  
  return comparison;
}

/**
 * Remove a competitor
 */
export function removeCompetitor(handle: string): void {
  const cleanHandle = handle.replace(/^@/, '');
  
  const stmt = db.prepare('DELETE FROM competitors WHERE handle = ?');
  stmt.run(cleanHandle);
}