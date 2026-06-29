/**
 * Analytics Module - Engagement Metrics & Insights
 * Track likes, reposts, replies per post
 * Track follower trends
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
const db = new Database(path.join(dbDir, 'analytics.db'));

// Initialize analytics tables
db.exec(`
  CREATE TABLE IF NOT EXISTS post_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uri TEXT UNIQUE NOT NULL,
    text TEXT,
    likes INTEGER DEFAULT 0,
    reposts INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    quotes INTEGER DEFAULT 0,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP,
    lastUpdated TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS follower_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count INTEGER NOT NULL,
    recordedAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE NOT NULL,
    posts INTEGER DEFAULT 0,
    likesGiven INTEGER DEFAULT 0,
    newFollowers INTEGER DEFAULT 0,
    newFollowing INTEGER DEFAULT 0
  )
`);

/**
 * Track a post's engagement
 */
export function trackPost(uri: string, text: string): void {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO post_analytics (uri, text, likes, reposts, replies, quotes)
    VALUES (?, ?, 0, 0, 0, 0)
  `);
  stmt.run(uri, text);
}

/**
 * Update engagement metrics for a post
 */
export function updatePostMetrics(uri: string, metrics: {
  likes?: number;
  reposts?: number;
  replies?: number;
  quotes?: number;
}): void {
  const fields = [];
  const values = [];
  
  if (metrics.likes !== undefined) { fields.push('likes = ?'); values.push(metrics.likes); }
  if (metrics.reposts !== undefined) { fields.push('reposts = ?'); values.push(metrics.reposts); }
  if (metrics.replies !== undefined) { fields.push('replies = ?'); values.push(metrics.replies); }
  if (metrics.quotes !== undefined) { fields.push('quotes = ?'); values.push(metrics.quotes); }
  
  if (fields.length === 0) return;
  
  fields.push("lastUpdated = datetime('now')");
  values.push(uri);
  
  const stmt = db.prepare(`
    UPDATE post_analytics SET ${fields.join(', ')} WHERE uri = ?
  `);
  stmt.run(...values);
}

/**
 * Get engagement metrics for a post
 */
export function getPostMetrics(uri: string): any {
  const stmt = db.prepare('SELECT * FROM post_analytics WHERE uri = ?');
  return stmt.get(uri);
}

/**
 * Get top performing posts
 */
export function getTopPosts(limit: number = 10, sortBy: 'likes' | 'reposts' | 'replies' = 'likes'): any[] {
  const stmt = db.prepare(`
    SELECT * FROM post_analytics 
    ORDER BY ${sortBy} DESC 
    LIMIT ?
  `);
  return stmt.all(limit);
}

/**
 * Get overall engagement stats
 */
export function getEngagementStats(days: number = 7): any {
  const stmt = db.prepare(`
    SELECT 
      COUNT(*) as totalPosts,
      SUM(likes) as totalLikes,
      SUM(reposts) as totalReposts,
      SUM(replies) as totalReplies,
      AVG(likes) as avgLikes,
      AVG(reposts) as avgReposts,
      AVG(replies) as avgReplies
    FROM post_analytics
    WHERE julianday('now') - julianday(createdAt) <= ?
  `);
  
  const result = stmt.get(days) as any;
  
  return {
    totalPosts: result?.totalPosts || 0,
    totalLikes: result?.totalLikes || 0,
    totalReposts: result?.totalReposts || 0,
    totalReplies: result?.totalReplies || 0,
    avgLikes: Math.round(result?.avgLikes || 0),
    avgReposts: Math.round(result?.avgReposts || 0),
    avgReplies: Math.round(result?.avgReplies || 0)
  };
}

/**
 * Record follower count
 */
export function recordFollowerCount(count: number): void {
  const stmt = db.prepare(`
    INSERT INTO follower_history (count) VALUES (?)
  `);
  stmt.run(count);
}

/**
 * Get follower history
 */
export function getFollowerHistory(days: number = 30): any[] {
  const stmt = db.prepare(`
    SELECT * FROM follower_history 
    WHERE julianday('now') - julianday(recordedAt) <= ?
    ORDER BY recordedAt ASC
  `);
  return stmt.all(days);
}

/**
 * Calculate follower growth
 */
export function getFollowerGrowth(days: number = 30): { growth: number; percentage: number; trend: 'up' | 'down' | 'stable' } {
  const history = getFollowerHistory(days);
  
  if (history.length < 2) {
    return { growth: 0, percentage: 0, trend: 'stable' };
  }
  
  const oldest = history[0].count;
  const latest = history[history.length - 1].count;
  const growth = latest - oldest;
  const percentage = oldest > 0 ? Math.round((growth / oldest) * 100) : 0;
  
  return {
    growth,
    percentage,
    trend: growth > 0 ? 'up' : growth < 0 ? 'down' : 'stable'
  };
}

/**
 * Update daily stats
 */
export function updateDailyStats(stats: {
  posts?: number;
  likesGiven?: number;
  newFollowers?: number;
  newFollowing?: number;
}): void {
  const today = new Date().toISOString().split('T')[0];
  
  const fields = [];
  const values = [];
  
  if (stats.posts !== undefined) { fields.push('posts = posts + ?'); values.push(stats.posts); }
  if (stats.likesGiven !== undefined) { fields.push('likesGiven = likesGiven + ?'); values.push(stats.likesGiven); }
  if (stats.newFollowers !== undefined) { fields.push('newFollowers = newFollowers + ?'); values.push(stats.newFollowers); }
  if (stats.newFollowing !== undefined) { fields.push('newFollowing = newFollowing + ?'); values.push(stats.newFollowing); }
  
  if (fields.length === 0) return;
  
  values.push(today);
  
  const stmt = db.prepare(`
    INSERT INTO daily_stats (date, ${Object.keys(stats).join(', ')})
    VALUES (?, ${Object.keys(stats).map(() => '?').join(', ')})
    ON CONFLICT(date) DO UPDATE SET ${fields.join(', ')}
  `);
  stmt.run(today, ...values);
}

/**
 * Get daily stats
 */
export function getDailyStats(days: number = 7): any[] {
  const stmt = db.prepare(`
    SELECT * FROM daily_stats
    WHERE julianday('now') - julianday(date) <= ?
    ORDER BY date DESC
  `);
  return stmt.all(days);
}