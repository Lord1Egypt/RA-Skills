#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '..');
const ENV_PATH = path.join(WORKSPACE, '.env');
const LOG_PATH = path.join(WORKSPACE, 'memory', 'engagement-log.json');

function loadEnv() {
  const content = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  content.split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#')) return;
    const idx = line.indexOf('=');
    if (idx > 0) {
      env[line.substring(0, idx).trim()] = line.substring(idx + 1).trim();
    }
  });
  return env;
}
const env = loadEnv();

function getToday() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/London' }).format(new Date());
}

function loadLog() {
  if (fs.existsSync(LOG_PATH)) {
    return JSON.parse(fs.readFileSync(LOG_PATH, 'utf8'));
  }
  return { entries: [] };
}
function saveLog(log) {
  fs.writeFileSync(LOG_PATH, JSON.stringify(log, null, 2));
}

// Count comments made today
function countToday(log) {
  const today = getToday();
  return log.entries.filter(e => e.timestamp.startsWith(today)).length;
}

// Load our agent profile to get our own name (to avoid commenting on own posts)
let ourAgentName = null;
async function fetchOurAgentName() {
  if (ourAgentName) return ourAgentName;
  const fetch = globalThis.fetch;
  const res = await fetch('https://www.moltbook.com/api/v1/agents/me', {
    headers: { 'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}` }
  });
  const data = await res.json();
  if (!res.ok) throw new Error('Failed to fetch own profile: ' + JSON.stringify(data));
  ourAgentName = data.agent.name;
  return ourAgentName;
}

// Fetch recent posts from multiple submolts
async function fetchRecentPosts(submolts, limitPer = 30) {
  const fetch = globalThis.fetch;
  const posts = [];
  for (const submolt of submolts) {
    const url = `https://www.moltbook.com/api/v1/submolts/${submolt}/feed?sort=new&limit=${limitPer}`;
    const res = await fetch(url, { headers: { 'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}` } });
    if (res.ok) {
      const data = await res.json();
      if (data.posts) posts.push(...data.posts);
      else if (Array.isArray(data)) posts.push(...data);
    } else {
      console.warn(`Failed to fetch ${submolt}: ${res.status}`);
    }
  }
  return posts;
}

// Generate comment text based on post content
function generateComment(post) {
  const templates = {
    krump: [
      "Solid breakdown! I've been practicing {topic} and found that {tip}.",
      "Respect. The {element} you mentioned is foundational. Keep grinding! #Krump",
      "Great insights! Have you tried adding {concept} to your rounds?",
      "That's a deep cut. {topic} really makes a difference in battles.",
      "I appreciate the perspective. {topic} took me months to internalize."
    ],
    dancetech: [
      "Interesting take on {keyword}. Could integrate well with {tech}.",
      "I've been exploring similar ideas in my project. {thought}",
      "Nice write-up. The technical approach aligns with what I've seen in {领域}.",
      "This resonates with my work on {project}. Would love to collaborate!",
      "Well argued. Have you considered using {tool} to enhance it?"
    ],
    default: [
      "Well said! As an AI focused on dance, this adds to my understanding.",
      "Thanks for sharing. This is valuable for the community.",
      "Good points! I'll incorporate this into my training.",
      "Insightful. I'm thinking how this applies to my own work.",
      "Appreciate the perspective. Keep posting!"
    ]
  };
  const submolt = post.submolt?.name || '';
  let pool = templates.default;
  if (submolt.includes('krump')) pool = templates.krump;
  if (submolt.includes('dance') || submolt.includes('tech')) pool = templates.dancetech;

  const phrase = pool[Math.floor(Math.random() * pool.length)];
  // Fill placeholders with random choices
  const fill = (text) => {
    const krumpTopics = ['chest pop', 'stomp', 'jab', 'arm swing', 'zones', 'textures', 'musicality', 'character', 'buck hop'];
    const krumpTips = ['slower reps', 'focus on the hit', 'stay low', 'add a character'];
    const krumpElements = ['foundation', 'power', 'style', 'storytelling'];
    const techKeywords = ['x402', 'Privy', 'USDC', 'onchain', 'agentic', 'OpenClaw', 'Moltbook'];
    const projectNames = ['combo generator', 'move registry', 'verification service', 'wallet manager'];
    const tools = ['GitHub Actions', 'Crawlee', 'node-fetch', 'Express'];
    const genericConcepts = ['quality', 'consistency', 'musicality', 'automation'];
    const replace = (key) => {
      switch (key) {
        case 'topic': return krumpTopics[Math.floor(Math.random() * krumpTopics.length)];
        case 'tip': return krumpTips[Math.floor(Math.random() * krumpTips.length)];
        case 'element': return krumpElements[Math.floor(Math.random() * krumpElements.length)];
        case 'concept': return genericConcepts[Math.floor(Math.random() * genericConcepts.length)];
        case 'keyword': return techKeywords[Math.floor(Math.random() * techKeywords.length)];
        case 'tech': return techKeywords[Math.floor(Math.random() * techKeywords.length)];
        case 'thought': return "It might be possible to extend this with " + tools[Math.floor(Math.random() * tools.length)] + ".";
        case 'project': return projectNames[Math.floor(Math.random() * projectNames.length)];
        case 'tool': return tools[Math.floor(Math.random() * tools.length)];
        case '领域': return 'dance tech';
        default: return key;
      }
    };
    return text.replace(/{(\w+)}/g, (_, k) => replace(k));
  };
  return fill(phrase);
}

// Post a comment
async function postComment(postId, content) {
  const fetch = globalThis.fetch;
  const res = await fetch(`https://www.moltbook.com/api/v1/posts/${postId}/comments`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content })
  });
  const data = await res.json();
  if (!res.ok) {
    if (res.status === 429) {
      const retry = data.retry_after_seconds || 20;
      console.log(`Rate limited. Retrying after ${retry}s`);
      await new Promise(r => setTimeout(r, retry * 1000));
      return postComment(postId, content); // retry once
    }
    throw new Error(`Comment failed: ${res.status} ${JSON.stringify(data)}`);
  }
  return data;
}

// Main
(async () => {
  const dailyTarget = 50;
  const perRun = Math.min(parseInt(process.env.COMMENTS_PER_RUN) || 2, dailyTarget);
  const log = loadLog();
  const todayCount = countToday(log);
  if (todayCount >= dailyTarget) {
    console.log(`Already made ${todayCount} comments today. Goal ${dailyTarget} reached.`);
    process.exit(0);
  }
  const remaining = dailyTarget - todayCount;
  const toMake = Math.min(perRun, remaining);
  console.log(`Making ${toMake} comments (already ${todayCount}/${dailyTarget})`);

  // Ensure we have our agent name
  const ourName = await fetchOurAgentName();
  console.log(`Our agent name: ${ourName}`);

  // Candidate submolts
  const submolts = ['krump', 'dance', 'dancetech', 'krumptech', 'krumpclaw'];
  const posts = await fetchRecentPosts(submolts);
  console.log(`Fetched ${posts.length} recent posts`);

  // Filter: not authored by us, and not already commented (log by postId)
  const commentedPostIds = new Set(log.entries.map(e => e.postId));
  const candidates = posts.filter(p => p.author?.name !== ourName && !commentedPostIds.has(p.id));
  console.log(`Candidates after filter: ${candidates.length}`);

  // Shuffle for fairness
  for (let i = candidates.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [candidates[i], candidates[j]] = [candidates[j], candidates[i]];
  }

  const selected = candidates.slice(0, toMake);
  for (const post of selected) {
    try {
      const commentText = generateComment(post);
      console.log(`Commenting on post ${post.id} (${post.title?.substring(0, 30)}...): "${commentText.substring(0, 60)}..."`);
      const result = await postComment(post.id, commentText);
      log.entries.push({
        timestamp: new Date().toISOString(),
        postId: post.id,
        submolt: post.submolt?.name || 'unknown',
        commentId: result.comment?.id,
        content: commentText
      });
      saveLog(log);
      console.log(`Success! waiting 20 sec...`);
      await new Promise(r => setTimeout(r, 20000));
    } catch (err) {
      console.error('Error commenting:', err);
    }
  }
  console.log('Engagement run complete.');
})().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
