#!/usr/bin/env node

/**
 * InfoQuest Search CLI
 * AI-optimized web search using BytePlus InfoQuest API
 * Supports both web search and image search
 */

// Use global fetch if available (Node.js 18+), otherwise use dynamic import
let fetchImplementation;

if (typeof globalThis.fetch === 'function') {
  // Node.js 18+ has built-in fetch
  fetchImplementation = globalThis.fetch;
} else {
  // For older Node.js versions, use dynamic import
  fetchImplementation = async (...args) => {
    try {
      const { default: fetch } = await import('node-fetch');
      return fetch(...args);
    } catch (error) {
      throw new Error(
        'Fetch API not available. Node.js 18+ includes fetch natively. ' +
        'For older versions, install node-fetch: npm install node-fetch'
      );
    }
  };
}

const fetch = fetchImplementation;

function usage() {
  console.error(`Usage: search.mjs "query" [options]
  
Options:
  -s, --site <domain>     Search within specific site (e.g., github.com)
  -d, --days <number>     Search within last N days
  -i, --image             Perform image search (default: web search)
  -z, --image-size <size> Image size filter: l (large), m (medium), i (icon)
  -h, --help              Show this help message

Examples:
  node search.mjs "OpenClaw AI framework"
  node search.mjs "machine learning" -d 7
  node search.mjs "Python tutorials" -s github.com
  node search.mjs "latest news" -d 1
  node search.mjs "cat" -i
  node search.mjs "landscape" -i -z l
  node search.mjs "logo" -i -z i -s github.com
`);
  process.exit(2);
}

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const query = args[0];
let site = "";
let days = -1;
let isImageSearch = false;
let imageSize = "";

for (let i = 1; i < args.length; i++) {
  const arg = args[i];
  
  if (arg === "-s" || arg === "--site") {
    site = args[i + 1] || "";
    i++;
    continue;
  }
  
  if (arg === "-d" || arg === "--days") {
    days = parseInt(args[i + 1] || "7", 10);
    i++;
    continue;
  }
  
  if (arg === "-i" || arg === "--image") {
    isImageSearch = true;
    continue;
  }
  
  if (arg === "-z" || arg === "--image-size") {
    imageSize = args[i + 1] || "";
    if (!["l", "m", "i"].includes(imageSize)) {
      console.error(`Error: image-size must be l (large), m (medium), or i (icon)`);
      process.exit(1);
    }
    i++;
    continue;
  }
  
  console.error(`Unknown argument: ${arg}`);
  usage();
}

// Check API key
const apiKey = (process.env.INFOQUEST_API_KEY || "").trim();
if (!apiKey) {
  console.error("Error: INFOQUEST_API_KEY environment variable is not set");
  console.error("Set it using: export INFOQUEST_API_KEY='your-api-key-here'");
  console.error("Get your API key from: https://docs.byteplus.com/en/docs/InfoQuest/What_is_Info_Quest");
  process.exit(1);
}

// Prepare request headers
function prepareHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };

  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }

  return headers;
}

// Clean web search results
function cleanWebResults(rawResults) {
  const seenUrls = new Set();
  const cleanResults = [];

  for (const contentList of rawResults) {
    const content = contentList.content;
    const results = content.results;

    // Process organic results
    if (results.organic) {
      for (const result of results.organic) {
        const cleanResult = { type: 'page' };
        if (result.title) cleanResult.title = result.title;
        if (result.desc) cleanResult.desc = result.desc;
        if (result.url) cleanResult.url = result.url;
        
        const url = cleanResult.url;
        if (url && !seenUrls.has(url)) {
          seenUrls.add(url);
          cleanResults.push(cleanResult);
        }
      }
    }

    // Process news results
    if (results.top_stories) {
      const news = results.top_stories;
      for (const item of news.items) {
        const cleanResult = { type: 'news' };
        if (item.time_frame) cleanResult.time_frame = item.time_frame;
        if (item.source) cleanResult.source = item.source;
        if (item.url) cleanResult.url = item.url;
        if (item.title) cleanResult.title = item.title;
        
        const url = cleanResult.url;
        if (url && !seenUrls.has(url)) {
          seenUrls.add(url);
          cleanResults.push(cleanResult);
        }
      }
    }
  }

  return cleanResults;
}

// Clean image search results
function cleanImageResults(rawResults) {
  const seenUrls = new Set();
  const cleanResults = [];

  for (const contentList of rawResults) {
    const content = contentList.content;
    const results = content.results;

    // Process images_results (not organic)
    if (results.images_results) {
      for (const result of results.images_results) {
        const cleanResult = {};
        if (result.title) cleanResult.title = result.title;
        if (result.original) cleanResult.image_url = result.original;
        
        const url = cleanResult.image_url;
        if (url && !seenUrls.has(url)) {
          seenUrls.add(url);
          cleanResults.push(cleanResult);
        }
      }
    }
  }
  return cleanResults;
}

// Perform web search
async function performWebSearch(query, site = '', days = -1) {
  const headers = prepareHeaders();
  const params = {
    search_type: 'Web',
    format: 'JSON',
    query
  };

  if (days > 0) {
    params.time_range = days;
  }

  if (site) {
    params.site = site;
  }

  try {
    const response = await fetch('https://search.infoquest.bytepluses.com', {
      method: 'POST',
      headers,
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Search API returned status ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    
    if (data.search_result) {
      const results = data.search_result.results;
      return cleanWebResults(results);
    } else if (data.content) {
      throw new Error('web search API return wrong format');
    } else {
      return data;
    }
  } catch (error) {
    throw new Error(`Web search failed: ${error.message}`);
  }
}

// Perform image search
async function performImageSearch(query, site = '', days = -1, imageSize = '') {
  const headers = prepareHeaders();
  const params = {
    search_type: 'Images',
    format: 'JSON',
    query
  };

  if (days > 0) {
    params.time_range = days;
  }

  if (site) {
    params.site = site;
  }

  if (imageSize) {
    params.image_size = imageSize;
  }

  try {
    const response = await fetch('https://search.infoquest.bytepluses.com', {
      method: 'POST',
      headers,
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Search API returned status ${response.status}: ${errorText}`);
    }

    const data = await response.json();

    if (data.search_result) {
      const results = data.search_result.results;
      return cleanImageResults(results);
    } else if (data.content) {
      throw new Error('image search API return wrong format');
    } else {
      return data;
    }
  } catch (error) {
    throw new Error(`Image search failed: ${error.message}`);
  }
}

// Main function
async function main() {
  try {
    let results;
    let searchType = isImageSearch ? 'image' : 'web';
    
    if (isImageSearch) {
      results = await performImageSearch(query, site, days > 0 ? days : -1, imageSize);
      console.log(JSON.stringify({
        query: query,
        total_results: results.length,
        results: results,
        usage_hint: "Use the 'image_url' values as reference images in image generation. Download them first if needed."
      }, null, 2));
    } else {
      results = await performWebSearch(query, site, days > 0 ? days : -1);
      console.log(JSON.stringify({
        query,
        search_type: searchType,
        count: results.length,
        results
      }, null, 2));
    }
    
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();