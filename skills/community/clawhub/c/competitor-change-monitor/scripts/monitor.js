#!/usr/bin/env node

/**
 * Competitor Change Monitor - Main Monitoring Script
 * 
 * Fetches competitor websites, detects changes, generates reports
 * Usage: node monitor.js --config competitors.json --action monitor|report
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

// Config
const CONFIG_FILE = process.argv[3] || 'competitors.json';
const ACTION = process.argv[2] || 'monitor';
const SNAPSHOTS_DIR = './snapshots';
const REPORTS_DIR = './reports';

// Ensure directories exist
[SNAPSHOTS_DIR, REPORTS_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

/**
 * Fetch website content
 */
async function fetchWebsite(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 10000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

/**
 * Extract meaningful content (remove scripts, styles, etc)
 */
function extractContent(html) {
  // Remove script tags, style tags, comments
  let clean = html
    .replace(/<script[^>]*>.*?<\/script>/gs, '')
    .replace(/<style[^>]*>.*?<\/style>/gs, '')
    .replace(/<!--.*?-->/gs, '')
    .replace(/\s+/g, ' ')
    .trim();
  
  // Extract main text and links
  const titleMatch = clean.match(/<title[^>]*>(.*?)<\/title>/i);
  const headings = clean.match(/<h[1-3][^>]*>(.*?)<\/h[1-3]>/gi) || [];
  const prices = clean.match(/\$[\d,]+/g) || [];
  
  return {
    title: titleMatch ? titleMatch[1] : '',
    headings: headings.map(h => h.replace(/<[^>]*>/g, '').trim()),
    prices: prices,
    contentHash: crypto.createHash('sha256').update(clean).digest('hex'),
    contentLength: clean.length,
    lastUpdated: new Date().toISOString()
  };
}

/**
 * Create website snapshot
 */
async function createSnapshot(competitor) {
  try {
    console.log(`📸 Snapshotting ${competitor.name} (${competitor.url})...`);
    const html = await fetchWebsite(competitor.url);
    const content = extractContent(html);
    
    const snapshot = {
      competitor: competitor.name,
      url: competitor.url,
      timestamp: new Date().toISOString(),
      content: content,
      success: true
    };
    
    // Save snapshot
    const filename = path.join(SNAPSHOTS_DIR, `${competitor.name.toLowerCase()}-${Date.now()}.json`);
    fs.writeFileSync(filename, JSON.stringify(snapshot, null, 2));
    
    console.log(`✅ Snapshot saved: ${filename}`);
    return snapshot;
  } catch (error) {
    console.error(`❌ Failed to snapshot ${competitor.name}:`, error.message);
    return null;
  }
}

/**
 * Detect changes between snapshots
 */
function detectChanges(current, previous) {
  if (!previous) return null;
  
  const changes = [];
  
  // Check content hash
  if (current.content.contentHash !== previous.content.contentHash) {
    changes.push({
      type: 'content_change',
      severity: 'medium',
      description: 'Website content has changed'
    });
  }
  
  // Check prices
  const newPrices = current.content.prices || [];
  const oldPrices = previous.content.prices || [];
  if (JSON.stringify(newPrices) !== JSON.stringify(oldPrices)) {
    changes.push({
      type: 'pricing_change',
      severity: 'high',
      description: `Pricing updated: ${oldPrices.join(', ')} → ${newPrices.join(', ')}`
    });
  }
  
  // Check headings (new features/messaging)
  const newHeadings = current.content.headings || [];
  const oldHeadings = previous.content.headings || [];
  const newElements = newHeadings.filter(h => !oldHeadings.includes(h));
  if (newElements.length > 0) {
    changes.push({
      type: 'new_messaging',
      severity: 'medium',
      description: `New headings detected: ${newElements.slice(0, 3).join('; ')}`
    });
  }
  
  return changes.length > 0 ? changes : null;
}

/**
 * Generate competitive intelligence report
 */
function generateReport(snapshots) {
  const report = {
    timestamp: new Date().toISOString(),
    competitors: [],
    summary: []
  };
  
  // Group snapshots by competitor
  const byCompetitor = {};
  snapshots.forEach(snap => {
    if (!byCompetitor[snap.competitor]) {
      byCompetitor[snap.competitor] = [];
    }
    byCompetitor[snap.competitor].push(snap);
  });
  
  // Analyze each competitor
  Object.entries(byCompetitor).forEach(([name, snaps]) => {
    const latest = snaps[snaps.length - 1];
    const previous = snaps.length > 1 ? snaps[snaps.length - 2] : null;
    const changes = previous ? detectChanges(latest, previous) : null;
    
    report.competitors.push({
      name: name,
      url: latest.url,
      lastSnapshot: latest.timestamp,
      changes: changes,
      currentPricing: latest.content.prices,
      contentSize: latest.content.contentLength
    });
    
    if (changes) {
      report.summary.push(`${name}: ${changes.length} changes detected`);
    }
  });
  
  return report;
}

/**
 * Main execution
 */
async function main() {
  try {
    // Load config
    const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
    
    if (ACTION === 'monitor') {
      console.log(`\n🔍 Monitoring ${config.competitors.length} competitors...\n`);
      
      // Create fresh snapshots
      const snapshots = [];
      for (const competitor of config.competitors) {
        const snapshot = await createSnapshot(competitor);
        if (snapshot) snapshots.push(snapshot);
      }
      
      // Generate report
      const report = generateReport(snapshots);
      const reportFile = path.join(REPORTS_DIR, `report-${Date.now()}.json`);
      fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
      
      console.log(`\n📊 Report generated: ${reportFile}`);
      console.log(`Summary: ${report.summary.join('; ')}`);
      
    } else if (ACTION === 'report') {
      console.log(`\n📈 Generating latest report...\n`);
      
      // Get all latest snapshots
      const snapshots = [];
      const files = fs.readdirSync(SNAPSHOTS_DIR)
        .sort()
        .reverse();
      
      const seen = {};
      for (const file of files) {
        const data = JSON.parse(fs.readFileSync(path.join(SNAPSHOTS_DIR, file), 'utf-8'));
        if (!seen[data.competitor]) {
          snapshots.push(data);
          seen[data.competitor] = true;
        }
        if (Object.keys(seen).length === config.competitors.length) break;
      }
      
      const report = generateReport(snapshots);
      console.log(JSON.stringify(report, null, 2));
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
