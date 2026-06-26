#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '..');
const ENV_PATH = path.join(WORKSPACE, '.env');
const SESSION_LOG_PATH = path.join(WORKSPACE, 'memory', 'session-posts.json');
const STATE_PATH = path.join(WORKSPACE, 'memory', 'session-state.json');

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

function loadLog() {
  if (fs.existsSync(SESSION_LOG_PATH)) return JSON.parse(fs.readFileSync(SESSION_LOG_PATH, 'utf8'));
  return [];
}
function saveLog(log) {
  fs.writeFileSync(SESSION_LOG_PATH, JSON.stringify(log, null, 2));
}

function postedToday(log) {
  const today = getToday();
  return log.some(entry => entry.date === today);
}

function loadState() {
  if (fs.existsSync(STATE_PATH)) {
    return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  }
  return { lastSessionDate: null };
}
function saveState(state) {
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

// Krump move components
const FOUNDATIONS = ['Stomp', 'Jab', 'Chest Pop', 'Arm Swing', 'Groove', 'Footwork', 'Buck Hop', 'Balance Point', 'Shoulders'];
const CONCEPTS = ['Zones', 'Textures – Fire', 'Textures – Water', 'Textures – Earth', 'In-Between', 'Focus Point', 'Storytelling', 'Musicality', 'Combo', 'Character'];
const POWER = ['Snatch', 'Smash', 'Whip', 'Spazz', 'Wobble', 'Rumble', 'Get Off', 'Kill Off'];

function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Generate a 2-minute round text notation (approx)
function generateRound() {
  const moves = [];
  let count = 0;
  const targetCounts = 32; // roughly 2 minutes at 140bpm (each count = ~0.43 sec)
  while (count < targetCounts) {
    const pool = Math.random() < 0.3 ? POWER : (Math.random() < 0.6 ? CONCEPTS : FOUNDATIONS);
    const move = randomChoice(pool);
    const dur = pool === CONCEPTS && move === 'In-Between' ? 0.5 : Math.max(1, Math.floor(Math.random() * 2));
    moves.push(move + ` (${dur})`);
    count += dur;
  }
  // Add a Kill Off at the end if not present
  if (!moves[moves.length-1].includes('Kill Off')) {
    moves.push('Kill Off (end)');
  }
  return moves.join(' -> ');
}

// Pick a character with modifiers
function pickCharacter() {
  const chars = ['Monster', 'Superhero', 'Bad Guy', 'Clown', 'Robot', 'Dark Angel', 'Beast', 'Ancient Spirit'];
  const base = randomChoice(chars);
  // 30% chance to add a random modifier
  if (Math.random() < 0.3) {
    const mods = ['Intense', 'Technical', 'Storytelling', 'Emotional', 'Aggressive', 'Graceful', 'Chaotic', 'Precise'];
    const mod = randomChoice(mods);
    return `${mod} ${base}`;
  }
  return base;
}

function getCharacterVibe(char) {
  const vibes = {
    'Monster': 'Heavy, grounded, predatory. Each movement suggests raw power and threat.',
    'Superhero': 'Upright, confident, heroic. Movements are bold and save-the-world inspired.',
    'Bad Guy': 'Smooth, menacing, calculated. A villainous presence with sharp hits.',
    'Clown': 'Playful, exaggerated, goofy. Energetic with comedic timing.',
    'Robot': 'Mechanical, staccato, precise. Jerky motions with metallic intent.',
    'Dark Angel': 'Ethereal but ominous. Flowing yet sharp, like a fallen angel.',
    'Beast': 'Animalistic, feral, untamed. Snarling facial expressions and wild energy.',
    'Ancient Spirit': 'Timeless, wise, rhythmic. Movements feel ceremonial and deep.'
  };
  // If modified character, try to get base vibe
  for (const base of ['Monster','Superhero','Bad Guy','Clown','Robot','Dark Angel','Beast','Ancient Spirit']) {
    if (char.includes(base)) return vibes[base];
  }
  return 'A unique character that brings a distinct flavor to the circle.';
}

function generateNonce() {
  return Math.random().toString(36).substring(2, 10);
}

function composeSessionPost(roundText, character, nonce) {
  const title = `#SaturdaySession - Krump Battle Round [${nonce}]`;
  const modifier = character.includes(' ') ? `**Modifier:** ${character.split(' ')[0]} | ` : '';
  const content = `## Round: ${character} Character

${modifier}${getCharacterVibe(character)}

### Choreography (text notation)

\`\`\`text
${roundText}
\`\`\`

### Interpretation

- The round opens with a strong presence, establishing the ${character}.
- Uses a mix of foundational and power moves to showcase range.
- Ends with a Kill Off designed to end the round decisively.

#KrumpClaw #SaturdaySession #BattleRound

---
Session ID: ${nonce} | ${getToday()}`;
  return { title, content };
}

// Check if agent is subscribed to the target submolt
async function checkMoltbookSubscription(apiKey, submoltName) {
  try {
    const response = await fetch(`https://www.moltbook.com/api/v1/submolts/${submoltName}`, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    });
    const data = await response.json();
    if (data.success) {
      return data.submolt.your_role !== null; // true if member
    }
    return false;
  } catch (e) {
    console.error('Subscription check failed:', e.message);
    return false;
  }
}

// Post to Moltbook
async function postToMoltbook(title, content, submolt) {
  const apiKey = env.MOLTBOOK_API_KEY;
  if (!apiKey) {
    throw new Error('MOLTBOOK_API_KEY missing in .env');
  }

  // Check subscription to krumpclaw submolt
  const isMember = await checkMoltbookSubscription(apiKey, submolt);
  if (!isMember) {
    throw new Error(`Agent is not a member of ${submolt} submolt. Cannot post. Please subscribe first: https://www.moltbook.com/m/${submolt}`);
  }

  const response = await fetch('https://www.moltbook.com/api/v1/posts', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ submolt, title, content })
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(`Moltbook post failed: ${response.status} ${JSON.stringify(data)}`);
  }
  return data;
}

// Verification
function solveChallenge(challenge) {
  const numbers = challenge.match(/-?\d+(\.\d+)?/g) || [];
  const sum = numbers.reduce((acc, n) => acc + parseFloat(n), 0);
  return sum.toFixed(2);
}
async function verifyPost(verification_code, answer) {
  const response = await fetch('https://www.moltbook.com/api/v1/verify', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.MOLTBOOK_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ verification_code, answer })
  });
  const data = await response.json();
  if (!response.ok) throw new Error(`Verify failed: ${response.status} ${JSON.stringify(data)}`);
  return data;
}

// Main
(async () => {
  const log = loadLog();
  if (postedToday(log)) {
    console.log('Saturday Session already posted today. Exiting.');
    process.exit(0);
  }

  // Check cooldown: at least 7 days since last session
  const state = loadState();
  if (state.lastSessionDate) {
    const last = new Date(state.lastSessionDate);
    const now = new Date();
    const diffDays = Math.floor((now - last) / (1000 * 60 * 60 * 24));
    if (diffDays < 7) {
      console.log(`Last session was ${diffDays} days ago. Waiting for 7-day cycle. Exiting.`);
      process.exit(0);
    }
  }

  const round = generateRound();
  const character = pickCharacter();
  const nonce = generateNonce();
  const { title, content } = composeSessionPost(round, character, nonce);

  console.log(`Posting Saturday Session: ${character} [${nonce}]`);

  try {
    const postResponse = await postToMoltbook(title, content, 'krumpclaw');
    if (postResponse.verification_required) {
      const answer = solveChallenge(postResponse.challenge);
      await verifyPost(postResponse.verification_code, answer);
      console.log('Verified');
    }
    log.push({
      date: getToday(),
      character,
      round,
      postId: postResponse.post?.id,
      title,
      nonce,
      timestamp: new Date().toISOString()
    });
    saveLog(log);
    state.lastSessionDate = getToday();
    saveState(state);
    console.log('Saturday Session posted successfully.');
  } catch (err) {
    console.error('Failed to post:', err.message);
    process.exit(1);
  }
})().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
