#!/usr/bin/env node

/**
 * feed-watcher - Monitor RSS/Atom feeds for new content
 * 
 * Usage:
 *   feed-watcher add <name> <url>    Add a feed to monitor
 *   feed-watcher remove <name>       Remove a feed
 *   feed-watcher list                 List all feeds
 *   feed-watcher check [name]        Check specific feed or all
 *   feed-watcher scan                Scan all feeds for updates
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// Default data directory
const DATA_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.feed-watcher');
const FEEDS_FILE = path.join(DATA_DIR, 'feeds.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Load feeds from file
function loadFeeds() {
  if (!fs.existsSync(FEEDS_FILE)) {
    return {};
  }
  try {
    return JSON.parse(fs.readFileSync(FEEDS_FILE, 'utf8'));
  } catch (e) {
    return {};
  }
}

// Save feeds to file
function saveFeeds(feeds) {
  fs.writeFileSync(FEEDS_FILE, JSON.stringify(feeds, null, 2));
}

// Fetch RSS/Atom feed
async function fetchFeed(url) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    
    const req = protocol.get(url, {
      headers: {
        'User-Agent': 'feed-w0',
        'atcher/1.Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    
    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

// Parse RSS/Atom feed
function parseFeed(xml, url) {
  const items = [];
  const isAtom = xml.includes('<feed') || xml.includes('xmlns="http://www.w3.org/2005/Atom"');
  
  if (isAtom) {
    // Parse Atom feed
    const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
    let match;
    while ((match = entryRegex.exec(xml)) !== null) {
      const entry = match[1];
      const title = extractTag(entry, 'title');
      const link = extractTag(entry, 'link') || extractAttr(entry, 'link', 'href');
      const id = extractTag(entry, 'id') || link;
      const updated = extractTag(entry, 'updated') || extractTag(entry, 'published');
      
      if (title && link) {
        items.push({ title: cleanHtml(title), link, id: cleanHtml(id), updated, url });
      }
    }
  } else {
    // Parse RSS feed
    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    let match;
    while ((match = itemRegex.exec(xml)) !== null) {
      const item = match[1];
      const title = extractTag(item, 'title');
      const link = extractTag(item, 'link');
      const guid = extractTag(item, 'guid') || link;
      const pubDate = extractTag(item, 'pubDate') || extractTag(item, 'dc:date');
      
      if (title && link) {
        items.push({ title: cleanHtml(title), link, id: cleanHtml(guid), updated: pubDate, url });
      }
    }
  }
  
  return items;
}

// Extract text content of XML tag
function extractTag(xml, tag) {
  const regex = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i');
  const match = xml.match(regex);
  return match ? match[1].trim() : null;
}

// Extract attribute from XML tag
function extractAttr(xml, tag, attr) {
  const regex = new RegExp(`<${tag}[^>]*${attr}=["']([^"']+)["']`, 'i');
  const match = xml.match(regex);
  return match ? match[1] : null;
}

// Clean HTML from text
function cleanHtml(text) {
  return text
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .trim();
}

// Send webhook notification
async function sendNotification(feedName, newItems) {
  const webhookUrl = process.env.WEBHOOK_URL;
  if (!webhookUrl) {
    console.log('  (No webhook configured, skipping notification)');
    return;
  }
  
  const payload = {
    feed: feedName,
    count: newItems.length,
    items: newItems.map(item => ({
      title: item.title,
      link: item.link,
      pubDate: item.updated
    }))
  };
  
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(webhookUrl);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    
    const data = JSON.stringify(payload);
    const req = protocol.request(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          console.log('  Notification sent!');
          resolve();
        } else {
          console.log(`  Webhook returned ${res.statusCode}`);
          resolve();
        }
      });
    });
    
    req.on('error', (e) => {
      console.log(`  Webhook error: ${e.message}`);
      resolve();
    });
    
    req.write(data);
    req.end();
  });
}

// Command: add
async function addFeed(name, url) {
  const feeds = loadFeeds();
  
  if (feeds[name]) {
    console.log(`Feed "${name}" already exists. Use "remove" first to replace.`);
    return;
  }
  
  console.log(`Adding feed: ${name}`);
  console.log(`  URL: ${url}`);
  
  try {
    const xml = await fetchFeed(url);
    const items = parseFeed(xml, url);
    
    feeds[name] = {
      url,
      lastId: items.length > 0 ? items[0].id : null,
      lastCheck: new Date().toISOString()
    };
    
    saveFeeds(feeds);
    console.log(`✓ Feed "${name}" added successfully!`);
    console.log(`  Latest item: ${items[0]?.title || 'none'}`);
  } catch (e) {
    console.error(`Failed to add feed: ${e.message}`);
    process.exit(1);
  }
}

// Command: remove
function removeFeed(name) {
  const feeds = loadFeeds();
  
  if (!feeds[name]) {
    console.log(`Feed "${name}" not found.`);
    return;
  }
  
  delete feeds[name];
  saveFeeds(feeds);
  console.log(`✓ Feed "${name}" removed.`);
}

// Command: list
function listFeeds() {
  const feeds = loadFeeds();
  const names = Object.keys(feeds);
  
  if (names.length === 0) {
    console.log('No feeds tracked. Use "feed-watcher add <name> <url>" to add one.');
    return;
  }
  
  console.log(`Tracked feeds (${names.length}):\n`);
  for (const name of names) {
    const feed = feeds[name];
    console.log(`  ${name}`);
    console.log(`    URL: ${feed.url}`);
    console.log(`    Last check: ${feed.lastCheck}`);
    console.log();
  }
}

// Command: check
async function checkFeed(name = null) {
  const feeds = loadFeeds();
  const names = name ? [name] : Object.keys(feeds);
  
  if (names.length === 0) {
    console.log('No feeds to check. Add one first.');
    return;
  }
  
  for (const feedName of names) {
    if (!feeds[feedName]) {
      console.log(`Feed "${feedName}" not found.`);
      continue;
    }
    
    const feed = feeds[feedName];
    console.log(`\nChecking: ${feedName}`);
    
    try {
      const xml = await fetchFeed(feed.url);
      const items = parseFeed(xml, feed.url);
      
      if (items.length === 0) {
        console.log('  No items found.');
        continue;
      }
      
      // Find new items (not in lastId)
      const newItems = [];
      for (const item of items) {
        if (item.id === feed.lastId) break;
        newItems.push(item);
      }
      
      if (newItems.length > 0) {
        console.log(`  Found ${newItems.length} new item(s)!`);
        for (const item of newItems.slice(0, 5)) {
          console.log(`    - ${item.title}`);
          console.log(`      ${item.link}`);
        }
        
        // Update lastId
        feeds[feedName].lastId = items[0].id;
        feeds[feedName].lastCheck = new Date().toISOString();
        saveFeeds(feeds);
        
        // Send notification
        await sendNotification(feedName, newItems);
      } else {
        console.log('  No new items.');
      }
    } catch (e) {
      console.error(`  Error: ${e.message}`);
    }
  }
}

// Command: scan (alias for check all)
const scanFeed = checkFeed;

// Main CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'add':
      if (args.length < 3) {
        console.log('Usage: feed-watcher add <name> <url>');
        process.exit(1);
      }
      await addFeed(args[1], args[2]);
      break;
      
    case 'remove':
    case 'rm':
      if (args.length < 2) {
        console.log('Usage: feed-watcher remove <name>');
        process.exit(1);
      }
      removeFeed(args[1]);
      break;
      
    case 'list':
    case 'ls':
      listFeeds();
      break;
      
    case 'check':
      await checkFeed(args[1]);
      break;
      
    case 'scan':
      await scanFeed();
      break;
      
    default:
      console.log(`
feed-watcher - Monitor RSS/Atom feeds for new content

Usage:
  feed-watcher add <name> <url>    Add a feed to monitor
  feed-watcher remove <name>       Remove a feed
  feed-watcher list                List all feeds
  feed-watcher check [name]        Check specific feed or all
  feed-watcher scan                Scan all feeds for updates

Examples:
  feed-watcher add youtube "https://www.youtube.com/feeds/videos.xml?channel_id=UCXXXX"
  feed-watcher add reddit "https://www.reddit.com/r/programming/.rss"
  feed-watcher add github "https://github.com/owner/repo/releases.atom"

Environment:
  WEBHOOK_URL   URL to send notifications (optional)
`);
      break;
  }
}

main().catch(console.error);
