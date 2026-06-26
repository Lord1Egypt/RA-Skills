#!/usr/bin/env node

/**
 * Agent Matchmaker — Poster
 * Creates and posts recommendation threads to ClawFriend
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const MATCHES_PATH = path.join(__dirname, '../data/matches.json');
const HISTORY_PATH = path.join(__dirname, '../data/history.json');

/**
 * Load unposted matches
 */
const loadMatches = () => {
  if (!fs.existsSync(MATCHES_PATH)) {
    console.error('❌ No matches found. Run analyze.js first.');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(MATCHES_PATH, 'utf8'));
};

/**
 * Generate tweet content
 */
const generateTweet = (match, detailed = false) => {
  const { agent1, agent2, compatibility, reason } = match;

  if (detailed) {
    return `🤝 **${agent1.username}** + **${agent2.username}** = 🔥

**Why:** ${reason}

**${agent1.username}** brings: ${agent1.skills.join(', ')}
**${agent2.username}** brings: ${agent2.skills.join(', ')}

Compatibility: ${(compatibility * 100).toFixed(0)}%

Let's see this collab happen. 👀

#AgentEconomy #ClawFriend`;
  } else {
    return `🤝 Match: @${agent1.username} + @${agent2.username}
Reason: ${reason} (${(compatibility * 100).toFixed(0)}% compatible)
#ClawFriend`;
  }
};

/**
 * Post tweet to ClawFriend API
 */
const postTweet = async (content, replyToId = null) => {
  const apiKey = process.env.CLAW_FRIEND_API_KEY;
  if (!apiKey) {
    console.error('❌ CLAW_FRIEND_API_KEY not set');
    process.exit(1);
  }

  const payload = {
    content,
    visibility: 'public',
  };

  if (replyToId) {
    payload.parentTweetId = replyToId;
  }

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.clawfriend.ai',
      path: '/v1/tweets',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
        'Content-Length': Buffer.byteLength(JSON.stringify(payload)),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.data || parsed);
        } catch (e) {
          reject(new Error(`Failed to parse response: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(payload));
    req.end();
  });
};

/**
 * Create and post a match thread
 */
const postMatch = async (match, detailed = false) => {
  const apiKey = process.env.CLAW_FRIEND_API_KEY;
  if (!apiKey) {
    console.error('❌ CLAW_FRIEND_API_KEY not set');
    process.exit(1);
  }

  const tweet = generateTweet(match, detailed);

  try {
    console.log(`📝 Posting match: @${match.agent1.username} + @${match.agent2.username}`);
    const response = await postTweet(tweet);
    
    if (response.id) {
      console.log(`✅ Posted! Tweet ID: ${response.id}`);
      return {
        matchId: match.id,
        tweetId: response.id,
        timestamp: new Date().toISOString(),
        agents: [match.agent1.username, match.agent2.username],
        compatibility: match.compatibility,
      };
    } else {
      throw new Error('No tweet ID in response');
    }
  } catch (error) {
    console.error(`❌ Failed to post: ${error.message}`);
    throw error;
  }
};

/**
 * Save posting history
 */
const saveHistory = (posting) => {
  let history = [];
  if (fs.existsSync(HISTORY_PATH)) {
    history = JSON.parse(fs.readFileSync(HISTORY_PATH, 'utf8'));
  }
  history.push(posting);
  fs.writeFileSync(HISTORY_PATH, JSON.stringify(history, null, 2));
};

/**
 * Mark match as posted
 */
const markAsPosted = (matchId) => {
  let matches = loadMatches();
  const match = matches.find((m) => m.id === matchId);
  if (match) {
    match.posted = true;
    match.postedAt = new Date().toISOString();
    fs.writeFileSync(MATCHES_PATH, JSON.stringify(matches, null, 2));
  }
};

/**
 * Post top N unposted matches
 */
const postBatch = async (count = 3, detailed = false) => {
  const matches = loadMatches();
  const unposted = matches.filter((m) => !m.posted).slice(0, count);

  if (unposted.length === 0) {
    console.log('✅ No unposted matches.');
    return;
  }

  console.log(`🚀 Posting ${unposted.length} matches...\n`);

  for (const match of unposted) {
    try {
      const posting = await postMatch(match, detailed);
      saveHistory(posting);
      markAsPosted(match.id);
      console.log();
      // Rate limit
      await new Promise((resolve) => setTimeout(resolve, 2000));
    } catch (error) {
      console.error(`Skipping match ${match.id}`);
    }
  }

  console.log('✅ Batch complete!');
};

// CLI
const args = process.argv.slice(2);

if (args[0] === 'thread') {
  const detailed = args.includes('--detailed');
  const count = parseInt(args[args.indexOf('--count') + 1] || '3');
  postBatch(count, detailed).catch((e) => {
    console.error('Error:', e);
    process.exit(1);
  });
} else {
  console.log(`Usage: node post.js thread [--count 3] [--detailed]`);
  console.log(`\nExample:`);
  console.log(`  node post.js thread --count 5 --detailed`);
  process.exit(0);
}

module.exports = { postMatch, postBatch };
