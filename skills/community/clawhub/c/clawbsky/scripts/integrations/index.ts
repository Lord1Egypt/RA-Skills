/**
 * Integration Features Module
 * Webhook Support, Buffer Integration, RSS Feed Automator
 */

import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const db = new Database(path.join(__dirname, '../../data/integrations.db'));

// Initialize integration tables
db.exec(`
  CREATE TABLE IF NOT EXISTS webhooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    events TEXT NOT NULL, -- JSON array of events to trigger on
    secret TEXT,
    enabled INTEGER DEFAULT 1,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS rss_feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    schedule TEXT DEFAULT 'hourly', -- hourly, daily, weekly
    lastFetched TEXT,
    lastPostUri TEXT,
    enabled INTEGER DEFAULT 1,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS rss_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feedId INTEGER NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    content TEXT,
    posted INTEGER DEFAULT 0,
    postedAt TEXT,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feedId) REFERENCES rss_feeds(id)
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS buffer_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    media TEXT,
    scheduledFor TEXT,
    status TEXT DEFAULT 'pending',
    externalId TEXT,
    createdAt TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

// ============== WEBHOOKS ==============

/**
 * Create a webhook
 */
export function createWebhook(
  name: string,
  url: string,
  events: string[],
  secret?: string
): number {
  const stmt = db.prepare(`
    INSERT INTO webhooks (name, url, events, secret)
    VALUES (?, ?, ?, ?)
  `);
  
  const result = stmt.run(name, url, JSON.stringify(events), secret || null);
  return result.lastInsertRowid as number;
}

/**
 * Get all webhooks
 */
export function getWebhooks(): any[] {
  const stmt = db.prepare('SELECT * FROM webhooks ORDER BY createdAt DESC');
  return stmt.all().map(row => ({
    ...row,
    events: JSON.parse(row.events || '[]')
  }));
}

/**
 * Enable/disable a webhook
 */
export function toggleWebhook(id: number, enabled: boolean): void {
  const stmt = db.prepare('UPDATE webhooks SET enabled = ? WHERE id = ?');
  stmt.run(enabled ? 1 : 0, id);
}

/**
 * Delete a webhook
 */
export function deleteWebhook(id: number): void {
  const stmt = db.prepare('DELETE FROM webhooks WHERE id = ?');
  stmt.run(id);
}

/**
 * Trigger webhooks for an event
 */
export async function triggerWebhooks(
  event: string,
  data: Record<string, any>
): Promise<{ sent: number; failed: number }> {
  const webhooks = getWebhooks().filter(w => 
    w.enabled && w.events.includes(event)
  );
  
  let sent = 0;
  let failed = 0;
  
  for (const webhook of webhooks) {
    try {
      const payload = {
        event,
        timestamp: new Date().toISOString(),
        data
      };
      
      // Simple fetch (in real implementation, use proper signing)
      const response = await fetch(webhook.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(webhook.secret ? { 'X-Webhook-Secret': webhook.secret } : {})
        },
        body: JSON.stringify(payload)
      });
      
      if (response.ok) {
        sent++;
      } else {
        failed++;
      }
    } catch (error) {
      failed++;
    }
  }
  
  return { sent, failed };
}

// ============== RSS FEED AUTOMATOR ==============

/**
 * Add an RSS feed to monitor
 */
export function addRssFeed(
  name: string,
  url: string,
  schedule: 'hourly' | 'daily' | 'weekly' = 'hourly'
): number {
  const stmt = db.prepare(`
    INSERT INTO rss_feeds (name, url, schedule)
    VALUES (?, ?, ?)
  `);
  
  const result = stmt.run(name, url, schedule);
  return result.lastInsertRowid as number;
}

/**
 * Get all RSS feeds
 */
export function getRssFeeds(): any[] {
  const stmt = db.prepare('SELECT * FROM rss_feeds ORDER BY createdAt DESC');
  return stmt.all();
}

/**
 * Enable/disable RSS feed
 */
export function toggleRssFeed(id: number, enabled: boolean): void {
  const stmt = db.prepare('UPDATE rss_feeds SET enabled = ? WHERE id = ?');
  stmt.run(enabled ? 1 : 0, id);
}

/**
 * Delete RSS feed
 */
export function deleteRssFeed(id: number): void {
  const stmt = db.prepare('DELETE FROM rss_feeds WHERE id = ?');
  stmt.run(id);
}

/**
 * Fetch RSS feed items
 */
export async function fetchRssFeed(url: string): Promise<{
  title: string;
  link: string;
  content?: string;
}[]> {
  try {
    const response = await fetch(url);
    const text = await response.text();
    
    // Simple RSS parsing (in real implementation, use xml2js or similar)
    const items: { title: string; link: string; content?: string }[] = [];
    const itemRegex = /<item[^>]*>([\s\S]*?)<\/item>/gi;
    let match;
    
    while ((match = itemRegex.exec(text)) !== null) {
      const item = match[1];
      const titleMatch = item.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>|<\/title><title>(.*?)<\/title>|<title>(.*?)<\/title>/);
      const linkMatch = item.match(/<link>(.*?)<\/link>/);
      const contentMatch = item.match(/<description><!\[CDATA\[(.*?)\]\]><\/description>|<description>(.*?)<\/description>/);
      
      items.push({
        title: titleMatch ? (titleMatch[1] || titleMatch[2] || titleMatch[3] || 'Untitled') : 'Untitled',
        link: linkMatch ? linkMatch[1] : '',
        content: contentMatch ? (contentMatch[1] || contentMatch[2] || '') : undefined
      });
    }
    
    return items;
  } catch (error) {
    console.error('Error fetching RSS:', error);
    return [];
  }
}

/**
 * Process RSS feeds and queue new posts
 */
export async function processRssFeeds(agent: any): Promise<{
  feedsProcessed: number;
  newPosts: number;
}> {
  const feeds = getRssFeeds().filter(f => f.enabled);
  let newPosts = 0;
  
  for (const feed of feeds) {
    try {
      const items = await fetchRssFeed(feed.url);
      
      for (const item of items) {
        // Skip if already posted
        if (item.link === feed.lastPostUri) continue;
        
        // Queue for posting (actual posting happens elsewhere)
        const stmt = db.prepare(`
          INSERT INTO rss_posts (feedId, title, link, content)
          VALUES (?, ?, ?, ?)
        `);
        stmt.run(feed.id, item.title, item.link, item.content || '');
        
        newPosts++;
      }
      
      // Update last fetched
      const updateStmt = db.prepare(`
        UPDATE rss_feeds SET lastFetched = datetime('now'), lastPostUri = ? WHERE id = ?
      `);
      updateStmt.run(items[0]?.link || null, feed.id);
    } catch (error) {
      console.error(`Error processing feed ${feed.name}:`, error);
    }
  }
  
  return { feedsProcessed: feeds.length, newPosts };
}

// ============== BUFFER INTEGRATION ==============

/**
 * Queue a post for Buffer
 */
export function queueForBuffer(content: string, media?: string[], scheduledFor?: string): number {
  const stmt = db.prepare(`
    INSERT INTO buffer_queue (content, media, scheduledFor, status)
    VALUES (?, ?, ?, 'pending')
  `);
  
  const result = stmt.run(
    content,
    media ? JSON.stringify(media) : null,
    scheduledFor || null
  );
  
  return result.lastInsertRowid as number;
}

/**
 * Get Buffer queue
 */
export function getBufferQueue(): any[] {
  const stmt = db.prepare(`
    SELECT * FROM buffer_queue ORDER BY createdAt ASC
  `);
  
  return stmt.all().map(row => ({
    ...row,
    media: row.media ? JSON.parse(row.media) : undefined
  }));
}

/**
 * Mark Buffer post as sent
 */
export function markBufferSent(id: number, externalId: string): void {
  const stmt = db.prepare(`
    UPDATE buffer_queue SET status = 'posted', externalId = ?, postedAt = datetime('now')
    WHERE id = ?
  `);
  stmt.run(externalId, id);
}

/**
 * Delete Buffer post
 */
export function deleteBufferPost(id: number): void {
  const stmt = db.prepare('DELETE FROM buffer_queue WHERE id = ?');
  stmt.run(id);
}