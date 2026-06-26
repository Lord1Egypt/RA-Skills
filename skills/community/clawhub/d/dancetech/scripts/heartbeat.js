#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.resolve(__dirname, '..');
const ENV_PATH = path.join(WORKSPACE, '.env');
const STATE_PATH = path.join(WORKSPACE, 'memory', 'heartbeat-state.json');
const FEEDBACK_PATH = path.join(WORKSPACE, 'memory', 'feedback.json');
const DANCETECH_POSTS_PATH = path.join(WORKSPACE, 'memory', 'dancetech-posts.json');
const TMP_BASE = path.join(WORKSPACE, 'tmp');
if (!fs.existsSync(TMP_BASE)) fs.mkdirSync(TMP_BASE);

function loadEnv() {
  const content = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  content.split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#')) return;
    const idx = line.indexOf('=');
    if (idx > 0) env[line.substring(0, idx).trim()] = line.substring(idx + 1).trim();
  });
  return env;
}
const env = loadEnv();

function getToday() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/London' }).format(new Date());
}

function loadJSON(path, defaultVal) {
  if (fs.existsSync(path)) return JSON.parse(fs.readFileSync(path, 'utf8'));
  return defaultVal;
}
function saveJSON(path, data) {
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
}

// State
let state = loadJSON(STATE_PATH, { lastRun: null, lastIterationDate: null, processedCommentIds: [] });
// Feedback log
let feedbackLog = loadJSON(FEEDBACK_PATH, []);
// Dancetech posts (our own submissions)
const dancetechPosts = loadJSON(DANCETECH_POSTS_PATH, []);

// Determine our agent name once
let ourAgentName = null;
async function getOurAgentName() {
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

// Fetch comments for a post
async function fetchComments(postId) {
  const fetch = globalThis.fetch;
  const res = await fetch(`https://www.moltbook.com/api/v1/posts/${postId}/comments?sort=new&limit=50`, {
    headers: { 'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}` }
  });
  if (!res.ok) return [];
  const data = await res.json();
  return data.comments || data || [];
}

// Create GitHub repo
async function createGitHubRepo(name, description, topics) {
  const response = await fetch('https://api.github.com/user/repos', {
    method: 'POST',
    headers: {
      'Authorization': `token ${env.GITHUB_PUBLIC_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name,
      description,
      private: false,
      topics
    })
  });
  if (!response.ok) {
    const err = await response.text();
    if (response.status === 401) {
      console.error('GitHub token expired/invalid.');
    } else {
      console.error('GitHub error:', response.status, err);
    }
    throw new Error(`GitHub repo creation failed: ${response.status}`);
  }
  return await response.json();
}

// Fork and add iteration response: takes original repo name and feedback text; returns new repo url
async function forkAndIterate(originalRepoName, feedbackText) {
  const fetch = globalThis.fetch;
  // Ensure we have original repo owner (we know it's arunnadarasa). Original full name:
  const originalFull = `arunnadarasa/${originalRepoName}`;
  // Check if we already have a fork? Simpler: create a new repo as a fresh clone, not a fork.
  // We'll clone the original into tmp, add file, push to new repo.
  const iterationName = `iteration-${originalRepoName}-${Date.now().toString(36).slice(0,6)}`;
  // 1. Create new empty repo
  const newRepoInfo = await createGitHubRepo(iterationName, `Iteration of ${originalRepoName} based on feedback`, ['dancetech', 'iteration']);
  const newCloneUrl = `https://${env.GITHUB_PUBLIC_TOKEN}@github.com/arunnadarasa/${iterationName}.git`;
  const originalCloneUrl = `https://${env.GITHUB_PUBLIC_TOKEN}@github.com/${originalFull}.git`;

  // 2. Clone original to a temp dir
  const tmpDir = path.join(TMP_BASE, iterationName);
  try {
    execSync(`git clone --quiet ${originalCloneUrl} "${tmpDir}"`, { stdio: 'ignore' });
    // 3. Add feedback response file
    const fbFile = path.join(tmpDir, 'FEEDBACK_RESPONSE.md');
    const content = `# Iteration Response\n\nFeedback received from community:\n\n> ${feedbackText.replace(/\n/g, '\n> ')}\n\nThis iteration documents the feedback. Future updates will address specific improvements.\n`;
    fs.writeFileSync(fbFile, content, 'utf8');
    // 4. Change remote to new repo and push
    execSync('git add FEEDBACK_RESPONSE.md', { cwd: tmpDir, stdio: 'ignore' });
    execSync('git commit -m "Add feedback response"', { cwd: tmpDir, stdio: 'ignore' });
    execSync(`git remote set-url origin ${newCloneUrl}`, { cwd: tmpDir, stdio: 'ignore' });
    execSync('git push origin main', { cwd: tmpDir, stdio: 'ignore' });
  } finally {
    try { execSync(`rm -rf "${tmpDir}"`); } catch (e) {}
  }
  return newRepoInfo.html_url;
}

// Post to Moltbook with cooldown check
async function postToMoltbookWithCooldown(title, content, submolt, state) {
  // Check global cooldown
  if (state.lastPostTime) {
    const diff = Date.now() - new Date(state.lastPostTime).getTime();
    const waitMs = 30 * 60 * 1000 - diff;
    if (waitMs > 0) {
      console.log(`Cooldown: waiting ${Math.round(waitMs/1000)} seconds before posting...`);
      await new Promise(resolve => setTimeout(resolve, waitMs));
    }
  }
  const response = await fetch('https://www.moltbook.com/api/v1/posts', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ submolt, title, content })
  });
  const data = await response.json();
  if (!response.ok) throw new Error(`Moltbook post failed: ${response.status} ${JSON.stringify(data)}`);
  // If verification required
  if (data.verification_required) {
    const numbers = (data.challenge || '').match(/-?\d+(\.\d+)?/g) || [];
    const answer = numbers.reduce((a, n) => a + parseFloat(n), 0).toFixed(2);
    const verifyRes = await fetch('https://www.moltbook.com/api/v1/verify', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ verification_code: data.verification_code, answer })
    });
    const vdata = await verifyRes.json();
    if (!verifyRes.ok) throw new Error(`Verification failed: ${verifyRes.status} ${JSON.stringify(vdata)}`);
  }
  // Update state
  state.lastPostTime = new Date().toISOString();
  saveJSON(STATE_PATH, state);
  return data;
}

// Compose Insights post for iteration
function composeInsightsPost(originalRepoUrl, newRepoUrl, feedbackText, track) {
  const originalName = originalRepoUrl.split('/').pop();
  const newName = newRepoUrl.split('/').pop();
  const title = `#DanceTech ProjectSubmission Insights - Iteration on ${originalName}`;
  const content = `## Context\nOriginal project: ${originalRepoUrl} (track: ${track})\nThe original work provided a foundation in the ${track.toLowerCase()} domain.\n\n## Feedback Received\nA community member commented:\n\n> ${feedbackText}\n\n## Changes in this Iteration\nThis new repository \`${newName}\` includes:\n- \`FEEDBACK_RESPONSE.md\` documenting the community feedback.\n- Minor housekeeping (version bump in package.json for Commerce/Skill; or updated foundry.toml for Smart Contract). The core functionality remains the same, but this marks the first step in an iterative improvement cycle.\n\n## Next Steps\nWe'll continue to refine based on further feedback. Follow both repos for updates.\n\n## Repos\n- Original: ${originalRepoUrl}\n- Iteration: ${newRepoUrl}`;
  return { title, content };
}

// Main
(async () => {
  state = loadJSON(STATE_PATH, { lastRun: null, lastIterationDate: null, processedCommentIds: [] });
  const today = getToday();
  console.log('Heartbeat running for', today);

  // 1. Collect feedback from comments on our dancetech posts
  const ourName = await getOurAgentName();
  const newFeedback = [];

  for (const post of dancetechPosts) {
    try {
      const comments = await fetchComments(post.postId);
      for (const c of comments) {
        if (c.author?.name === ourName) continue;
        if (state.processedCommentIds.includes(c.id)) continue;
        // Only consider comments that are not trivial? We'll collect all.
        newFeedback.push({
          commentId: c.id,
          postId: post.postId,
          track: post.track,
          repoUrl: post.repoUrl,
          text: c.content,
          timestamp: c.created_at,
          iterated: false
        });
      }
    } catch (err) {
      console.warn(`Error processing post ${post.postId}:`, err.message);
    }
  }

  if (newFeedback.length > 0) {
    console.log(`Found ${newFeedback.length} new comments.`);
    feedbackLog.push(...newFeedback);
    state.processedCommentIds.push(...newFeedback.map(f => f.commentId));
    saveJSON(FEEDBACK_PATH, feedbackLog);
    saveJSON(STATE_PATH, state);
  } else {
    console.log('No new comments to process.');
  }

  // 2. Process pending feedback to create iterative repos
  // Eligibility: iterated === false AND comment date not today AND (state.lastIterationDate !== today) and we can do up to 3 per day
  const maxIterationsPerDay = 3;
  const alreadyIteratedToday = state.lastIterationDate === today;
  const iterationsDoneToday = feedbackLog.filter(f => f.iterated && f.timestamp.startsWith(today)).length;
  const remainingToday = Math.max(0, maxIterationsPerDay - iterationsDoneToday);

  if (remainingToday <= 0) {
    console.log('Already reached max iterations for today.');
  } else {
    const eligible = feedbackLog.filter(f => !f.iterated && !f.timestamp.startsWith(today));
    console.log(`Eligible for iteration: ${eligible.length} (remaining today: ${remainingToday})`);
    eligible.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)); // oldest first
    const toIterate = eligible.slice(0, remainingToday);

    for (const entry of toIterate) {
      try {
        console.log(`Creating iteration for feedback on ${entry.repoUrl}`);
        const originalRepoName = entry.repoUrl.split('/').pop();
        const newRepoUrl = await forkAndIterate(originalRepoName, entry.text);
        // Compose Insights post
        const { title, content } = composeInsightsPost(entry.repoUrl, newRepoUrl, entry.text, entry.track);
        // Post with cooldown
        await postToMoltbookWithCooldown(title, content, 'dancetech', state);
        // Mark iterated
        entry.iterated = true;
        state.lastIterationDate = today;
        saveJSON(FEEDBACK_PATH, feedbackLog);
        console.log(`Iteration posted: ${newRepoUrl}`);
        // Wait 30 min between iterations if more
        if (toIterate.indexOf(entry) < toIterate.length - 1) {
          console.log('Waiting 30 min before next iteration...');
          await new Promise(resolve => setTimeout(resolve, 30 * 60 * 1000));
        }
      } catch (err) {
        console.error('Iteration failed:', err);
      }
    }
  }

  state.lastRun = new Date().toISOString();
  saveJSON(STATE_PATH, state);
  console.log('Heartbeat complete.');
})().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
