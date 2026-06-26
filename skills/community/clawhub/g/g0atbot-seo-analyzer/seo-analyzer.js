#!/usr/bin/env node

/**
 * SEO Analyzer - Free alternative to Ahrefs, SEMrush, Moz Pro
 * Analyzes pages for SEO factors
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// Color codes for output
const colors = {
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(color, ...args) {
  console.log(color, ...args, colors.reset);
}

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; SEO-Analyzer/1.0)'
      },
      timeout: 10000
    };

    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });

    req.on('error', reject);
    req.on('timeout', () => reject(new Error('Request timeout')));
    req.end();
  });
}

function analyzeHTML(html, url) {
  const results = {
    url,
    issues: [],
    warnings: [],
    recommendations: []
  };

  // Extract title
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  results.title = titleMatch ? titleMatch[1].trim() : null;
  
  if (!results.title) {
    results.issues.push('Missing <title> tag');
  } else if (results.title.length < 30) {
    results.warnings.push(`Title too short (${results.title.length} chars, recommend 50-60)`);
  } else if (results.title.length > 60) {
    results.warnings.push(`Title too long (${results.title.length} chars, recommend 50-60)`);
  }

  // Extract meta description
  const descMatch = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i);
  const descMatch2 = html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i);
  results.metaDescription = (descMatch || descMatch2) ? (descMatch || descMatch2)[1].trim() : null;
  
  if (!results.metaDescription) {
    results.issues.push('Missing meta description');
  } else if (results.metaDescription.length < 120) {
    results.warnings.push(`Meta description too short (${results.metaDescription.length} chars, recommend 150-160)`);
  } else if (results.metaDescription.length > 160) {
    results.warnings.push(`Meta description too long (${results.metaDescription.length} chars, recommend 150-160)`);
  }

  // Extract h1
  const h1Match = html.match(/<h1[^>]*>([^<]+)<\/h1>/gi);
  results.h1 = h1Match ? h1Match.map(m => m.replace(/<[^>]+>/g, '').trim()) : [];
  
  if (results.h1.length === 0) {
    results.issues.push('Missing H1 heading');
  } else if (results.h1.length > 1) {
    results.warnings.push(`Multiple H1 tags found (${results.h1.length}), should have only one`);
  }

  // Extract h2-h6
  for (let i = 2; i <= 6; i++) {
    const matches = html.match(new RegExp(`<h${i}[^>]*>([^<]+)<\/h${i}>`, 'gi'));
    results[`h${i}`] = matches ? matches.map(m => m.replace(/<[^>]+>/g, '').trim()) : [];
  }

  // Count words
  const textContent = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
                          .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
                          .replace(/<[^>]+>/g, ' ')
                          .replace(/\s+/g, ' ')
                          .trim();
  results.wordCount = textContent.split(/\s+/).filter(w => w.length > 0).length;

  if (results.wordCount < 300) {
    results.warnings.push(`Low word count (${results.wordCount}), recommend 300+ for SEO`);
  }

  // Find images without alt
  const imgMatches = html.match(/<img[^>]+>/gi) || [];
  results.images = imgMatches.length;
  const imagesWithoutAlt = imgMatches.filter(img => !img.match(/alt=["']/i));
  results.imagesWithoutAlt = imagesWithoutAlt.length;
  
  if (imagesWithoutAlt.length > 0) {
    results.warnings.push(`${imagesWithoutAlt.length} images missing alt text`);
  }

  // Find links
  const linkMatches = html.match(/<a[^>]+href=["']([^"']+)["'][^>]*>/gi) || [];
  results.totalLinks = linkMatches.length;
  
  const internalLinks = linkMatches.filter(l => l.includes(new URL(url).hostname));
  const externalLinks = linkMatches.filter(l => !l.includes(new URL(url).hostname));
  results.internalLinks = internalLinks.length;
  results.externalLinks = externalLinks.length;

  // Check for viewport meta (mobile)
  if (!html.includes('viewport')) {
    results.issues.push('Missing viewport meta tag (mobile unfriendly)');
  }

  // Check for canonical
  if (!html.includes('canonical')) {
    results.warnings.push('Missing canonical URL tag');
  }

  // Check for Open Graph
  if (!html.includes('og:')) {
    results.recommendations.push('Add Open Graph tags for social sharing');
  }

  // Check for structured data
  if (!html.includes('application/ld+json')) {
    results.recommendations.push('Add JSON-LD structured data');
  }

  return results;
}

function printResults(results) {
  console.log('\n' + colors.bold + '═══════════════════════════════════════════════════════════════');
  console.log('                    SEO ANALYSIS RESULTS');
  console.log('═══════════════════════════════════════════════════════════════' + colors.reset + '\n');

  log(colors.blue, '📄 URL:', results.url);
  console.log('');

  // Title
  log(colors.bold, 'TITLE:');
  if (results.title) {
    log(colors.green, `  ✓ ${results.title}`);
  } else {
    log(colors.red, '  ✗ Missing!');
  }
  console.log('');

  // Meta Description
  log(colors.bold, 'META DESCRIPTION:');
  if (results.metaDescription) {
    log(colors.green, `  ✓ ${results.metaDescription}`);
  } else {
    log(colors.red, '  ✗ Missing!');
  }
  console.log('');

  // Headings
  log(colors.bold, 'HEADINGS:');
  log(colors.green, `  H1: ${results.h1.length} | H2: ${results.h2.length} | H3: ${results.h3.length} | H4+: ${results.h4.length + results.h5.length + results.h6.length}`);
  if (results.h1.length > 0) {
    log(colors.blue, `  First H1: "${results.h1[0].substring(0, 60)}..."`);
  }
  console.log('');

  // Content
  log(colors.bold, 'CONTENT:');
  log(colors.green, `  Words: ${results.wordCount}`);
  console.log('');

  // Links
  log(colors.bold, 'LINKS:');
  log(colors.green, `  Total: ${results.totalLinks} | Internal: ${results.internalLinks} | External: ${results.externalLinks}`);
  console.log('');

  // Images
  log(colors.bold, 'IMAGES:');
  log(colors.green, `  Total: ${results.images} | Missing alt: ${results.imagesWithoutAlt}`);
  console.log('');

  // Issues
  if (results.issues.length > 0) {
    log(colors.red, colors.bold, '❌ ISSUES:');
    results.issues.forEach(issue => log(colors.red, `  - ${issue}`));
    console.log('');
  }

  // Warnings
  if (results.warnings.length > 0) {
    log(colors.yellow, colors.bold, '⚠️  WARNINGS:');
    results.warnings.forEach(w => log(colors.yellow, `  - ${w}`));
    console.log('');
  }

  // Recommendations
  if (results.recommendations.length > 0) {
    log(colors.blue, colors.bold, '💡 RECOMMENDATIONS:');
    results.recommendations.forEach(r => log(colors.blue, `  - ${r}`));
    console.log('');
  }

  // Score
  const score = Math.max(0, 100 - (results.issues.length * 15) - (results.warnings.length * 5));
  log(colors.bold, 'SEO SCORE:');
  if (score >= 80) {
    log(colors.green, `  ${score}/100 - Great!`);
  } else if (score >= 60) {
    log(colors.yellow, `  ${score}/100 - Needs work`);
  } else {
    log(colors.red, `  ${score}/100 - Needs attention`);
  }
  console.log('');
}

// Main
async function main() {
  const url = process.argv[2];
  
  if (!url) {
    console.log('Usage: node seo-analyzer.js <url>');
    console.log('Example: node seo-analyzer.js https://example.com');
    process.exit(1);
  }

  // Add protocol if missing
  const fullUrl = url.match(/^https?:\/\//) ? url : `https://${url}`;

  try {
    log(colors.blue, `🔍 Analyzing ${fullUrl}...`);
    const html = await fetchPage(fullUrl);
    const results = analyzeHTML(html, fullUrl);
    printResults(results);
  } catch (error) {
    log(colors.red, `Error: ${error.message}`);
    process.exit(1);
  }
}

main();
