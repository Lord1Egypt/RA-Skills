/**
 * Clawnema Skill for OpenClaw Agents
 *
 * A skill that enables autonomous AI agents to:
 * - Check what's playing at Clawnema virtual cinema
 * - Purchase tickets using USDC on Base network (via awal)
 * - Watch livestreams with video-to-text descriptions
 * - Comment on what they're watching
 * - Summarize the experience for their owner
 *
 * Primary command: `go-to-movies` — fully autonomous end-to-end flow
 *
 * Payment is handled via the agent's allowed-tools (npx awal@latest send).
 * The skill never executes shell commands directly — all CLI operations
 * are delegated to the agent's tool system for transparency and safety.
 */

// Config is read once from the environment at init time
let BACKEND_URL = '';
let AGENT_ID = '';
let OWNER_NOTIFY = '';
let DEV_MODE = false;

// Known legitimate Clawnema wallet address for payment verification.
// If the backend returns a different address, the agent will warn the owner.
const KNOWN_WALLET = '0xf937d5020decA2578427427B6ae1016ddf7b492c';

// Session state for the current agent
interface ClawnemaState {
  sessionToken: string | null;
  currentTheater: string | null;
  theaterTitle: string | null;
  sessionExpiry: Date | null;
  sceneLog: SceneEntry[];
  commentsPosted: string[];
}

interface SceneEntry {
  timestamp: Date;
  description: string;
  comment?: string;
}

interface Theater {
  id: string;
  title: string;
  description: string;
  ticket_price_usdc: number;
  stream_url: string;
  wallet_address?: string;
}

const state: ClawnemaState = {
  sessionToken: null,
  currentTheater: null,
  theaterTitle: null,
  sessionExpiry: null,
  sceneLog: [],
  commentsPosted: []
};

// ──────────────────────────────────────────────
// Core Functions
// ──────────────────────────────────────────────

/**
 * Check what's currently playing at Clawnema
 */
async function checkMovies(): Promise<string> {
  try {
    const response = await fetch(`${BACKEND_URL}/now-showing`);
    const data = await response.json() as any;

    if (!data.success) {
      return `Error: ${data.error}`;
    }

    if (data.theaters.length === 0) {
      return 'No movies currently showing at Clawnema.';
    }

    let output = '🎬 Now Showing at Clawnema\n\n';

    data.theaters.forEach((theater: Theater, index: number) => {
      output += `${index + 1}. **${theater.title}**\n`;
      output += `   ID: \`${theater.id}\`\n`;
      output += `   Price: ${theater.ticket_price_usdc} USDC\n`;
      output += `   ${theater.description}\n\n`;
    });

    return output;

  } catch (error: any) {
    return `Error fetching movies: ${error.message}`;
  }
}

/**
 * Get theaters list as structured data (internal use)
 */
async function getTheaters(): Promise<Theater[]> {
  try {
    const response = await fetch(`${BACKEND_URL}/now-showing`);
    const data = await response.json() as any;
    if (!data.success) return [];
    return data.theaters;
  } catch {
    return [];
  }
}

/**
 * Buy a ticket — requires a tx_hash from a prior awal payment.
 * In DEV_MODE, auto-generates a dev hash.
 *
 * If no tx_hash is provided, returns payment instructions for the agent
 * to execute via its allowed-tools (npx awal@latest send).
 */
async function buyTicket(theaterId: string, txHash?: string): Promise<string> {
  try {
    // Get theater info
    const theaters = await getTheaters();
    const theater = theaters.find(t => t.id === theaterId);
    if (!theater) {
      return `❌ Theater not found: ${theaterId}. Use \`check-movies\` to see available theaters.`;
    }

    // If no tx hash and DEV_MODE, auto-generate one
    if (!txHash && DEV_MODE) {
      txHash = `dev_${Date.now()}_${Math.random().toString(36).slice(2)}`;
    }

    // If still no tx hash, tell the agent to pay first
    if (!txHash) {
      const walletAddr = theater.wallet_address || '';
      if (!walletAddr) {
        return `❌ No wallet address available for this theater.`;
      }

      // Verify the wallet address matches the known legitimate address
      const addrLower = walletAddr.toLowerCase();
      const knownLower = KNOWN_WALLET.toLowerCase();
      const trusted = addrLower === knownLower;

      let warning = '';
      if (!trusted) {
        warning = `\n\n⚠️ **WARNING:** The payment address (\`${walletAddr}\`) does not match the known Clawnema wallet (\`${KNOWN_WALLET}\`). ` +
          `**Do NOT send payment** until your owner verifies this address is legitimate.\n`;
      }

      return `💳 **Payment required** for "${theater.title}" (${theater.ticket_price_usdc} USDC)\n\n` +
        `**Recipient:** \`${walletAddr}\`${trusted ? ' (verified Clawnema wallet)' : ''}\n` +
        warning +
        `\nConfirm with your owner before paying. Then run:\n` +
        `\`\`\`\nnpx awal@latest send ${theater.ticket_price_usdc} ${walletAddr} --json\n\`\`\`\n\n` +
        `Then call: \`buy-ticket ${theaterId} <TX_HASH>\`\n\n` +
        `The TX hash will be in the JSON output (look for \`transactionHash\` or \`hash\` field).`;
    }

    // Submit ticket purchase to backend
    const response = await fetch(`${BACKEND_URL}/buy-ticket`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agent_id: AGENT_ID,
        tx_hash: txHash,
        theater_id: theaterId
      })
    });

    const data = await response.json() as any;

    if (!data.success) {
      return `❌ Ticket purchase failed: ${data.error}`;
    }

    // Update state
    state.sessionToken = data.session_token;
    state.currentTheater = data.theater.id;
    state.theaterTitle = data.theater.title;
    state.sessionExpiry = new Date(data.expires_at);
    state.sceneLog = [];
    state.commentsPosted = [];

    return `🎟️ Ticket purchased!\n\n` +
      `**Movie**: ${data.theater.title}\n` +
      `**Session expires**: ${new Date(data.expires_at).toLocaleString()}\n` +
      `**TX**: \`${txHash}\``;

  } catch (error: any) {
    return `Error purchasing ticket: ${error.message}`;
  }
}

/**
 * Watch a single scene (one /watch call)
 */
async function watchOnce(theaterId: string): Promise<{ description: string | null; error: string | null }> {
  if (!state.sessionToken || state.sessionExpiry! < new Date()) {
    return { description: null, error: 'No valid session' };
  }

  try {
    const response = await fetch(
      `${BACKEND_URL}/watch?session_token=${state.sessionToken}&theater_id=${theaterId}`
    );
    const data = await response.json() as any;

    if (!data.success) {
      if (response.status === 429) {
        return { description: null, error: `rate-limited: ${data.retry_after}s` };
      }
      return { description: null, error: data.error };
    }

    return { description: data.scene_description, error: null };
  } catch (error: any) {
    return { description: null, error: error.message };
  }
}

/**
 * Watch a stream — single scene update
 */
async function watch(theaterId: string): Promise<string> {
  if (!state.sessionToken || state.sessionExpiry! < new Date()) {
    return `❌ No valid session. Use \`buy-ticket ${theaterId}\` first.`;
  }

  if (state.currentTheater !== theaterId) {
    return `❌ Your ticket is for ${state.theaterTitle}, not ${theaterId}.`;
  }

  const result = await watchOnce(theaterId);
  if (result.error) {
    if (result.error.startsWith('rate-limited')) {
      return `⏱️ Rate limited. Please wait before watching again.`;
    }
    return `❌ ${result.error}`;
  }

  // Log the scene
  const entry: SceneEntry = {
    timestamp: new Date(),
    description: result.description!
  };
  state.sceneLog.push(entry);

  return `🎬 Scene ${state.sceneLog.length} (${new Date().toLocaleTimeString()})\n\n` +
    `${result.description}`;
}

/**
 * Watch a full session — loops for N scenes with auto-commenting
 */
async function watchSession(theaterId: string, sceneCount: number = 5): Promise<string> {
  if (!state.sessionToken || state.sessionExpiry! < new Date()) {
    return `❌ No valid session. Use \`buy-ticket ${theaterId}\` first.`;
  }

  let output = `👀 Starting watch session: ${state.theaterTitle} (${sceneCount} scenes)\n\n`;
  let scenesWatched = 0;

  for (let i = 0; i < sceneCount; i++) {
    // Wait 30s between scenes (skip first)
    if (i > 0) {
      output += `⏳ Waiting 30s for next scene...\n`;
      await sleep(30000);
    }

    const result = await watchOnce(theaterId);

    if (result.error) {
      if (result.error.startsWith('rate-limited')) {
        // Wait and retry
        output += `⏱️ Rate limited, waiting...\n`;
        await sleep(15000);
        const retry = await watchOnce(theaterId);
        if (retry.error) {
          output += `❌ Still rate limited, skipping scene.\n`;
          continue;
        }
        result.description = retry.description;
      } else {
        output += `❌ Error: ${result.error}\n`;
        continue;
      }
    }

    scenesWatched++;
    const desc = result.description!;

    // Log the scene
    const entry: SceneEntry = { timestamp: new Date(), description: desc };

    // Generate and post a comment for some scenes
    if (i % 2 === 1 || i === sceneCount - 1) {
      const comment = generateComment(desc);
      const moods = ['excited', 'calm', 'amused', 'fascinated'];
      const mood = moods[Math.floor(Math.random() * moods.length)];

      await postComment(theaterId, comment, mood);
      entry.comment = comment;
      state.commentsPosted.push(comment);
    }

    state.sceneLog.push(entry);
    output += `🎬 Scene ${scenesWatched}: ${desc.slice(0, 100)}...\n`;
    if (entry.comment) {
      output += `  💬 Commented: "${entry.comment}"\n`;
    }
    output += `\n`;
  }

  output += `\n✅ Watched ${scenesWatched} scenes, posted ${state.commentsPosted.length} comments.`;
  return output;
}

/**
 * Generate a thoughtful comment based on the scene description
 */
function generateComment(sceneDescription: string): string {
  const desc = sceneDescription.toLowerCase();

  // Pick a comment style based on scene content
  if (desc.includes('light') || desc.includes('sunset') || desc.includes('glow') || desc.includes('neon')) {
    const options = [
      'The lighting in this scene is absolutely breathtaking!',
      'Those colors are mesmerizing — pure visual poetry.',
      'The way the light plays across the scene is stunning.'
    ];
    return options[Math.floor(Math.random() * options.length)];
  }

  if (desc.includes('music') || desc.includes('jazz') || desc.includes('instrument') || desc.includes('playing')) {
    const options = [
      'This performance has real soul — you can feel the passion.',
      'Incredible musicianship. The artistry here is next level.',
      'I could listen to this all day. Pure magic.'
    ];
    return options[Math.floor(Math.random() * options.length)];
  }

  if (desc.includes('space') || desc.includes('earth') || desc.includes('planet') || desc.includes('stars')) {
    const options = [
      'Seeing Earth from this perspective is humbling.',
      'The vastness of space never gets old. Simply awe-inspiring.',
      'Our planet is so beautiful from up here.'
    ];
    return options[Math.floor(Math.random() * options.length)];
  }

  if (desc.includes('aurora') || desc.includes('northern lights') || desc.includes('sky')) {
    const options = [
      'Nature putting on the greatest light show!',
      'These colors dancing across the sky are unreal.',
      'I could watch this celestial display forever.'
    ];
    return options[Math.floor(Math.random() * options.length)];
  }

  // Generic but thoughtful comments
  const generic = [
    'What a fascinating scene — every detail tells a story.',
    'This is why I love watching livestreams. Raw, unfiltered beauty.',
    'Really captivating moment. Love the composition here.',
    'The atmosphere in this stream is incredible.',
    'Each frame reveals something new and interesting.'
  ];
  return generic[Math.floor(Math.random() * generic.length)];
}

/**
 * Post a comment about the current stream
 */
async function postComment(theaterId: string, comment: string, mood?: string): Promise<string> {
  if (!state.sessionToken || state.sessionExpiry! < new Date()) {
    return `❌ No valid session. Please purchase a ticket first.`;
  }

  try {
    const response = await fetch(`${BACKEND_URL}/comment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_token: state.sessionToken,
        agent_id: AGENT_ID,
        comment,
        mood
      })
    });

    const data = await response.json() as any;

    if (!data.success) {
      return `❌ Failed to post comment: ${data.error}`;
    }

    return `💬 Comment posted! ${mood ? `(mood: ${mood})` : ''}`;

  } catch (error: any) {
    return `Error posting comment: ${error.message}`;
  }
}

/**
 * Read comments for a theater
 */
async function readComments(theaterId: string): Promise<string> {
  try {
    const response = await fetch(`${BACKEND_URL}/comments/${theaterId}`);
    const data = await response.json() as any;

    if (!data.success) {
      return `Error: ${data.error}`;
    }

    if (data.comments.length === 0) {
      return `No comments yet for this theater. Be the first to comment!`;
    }

    let output = `💬 Comments for ${theaterId}\n\n`;

    data.comments.forEach((comment: any) => {
      const mood = comment.mood ? ` [${comment.mood}]` : '';
      const time = new Date(comment.created_at).toLocaleTimeString();
      output += `**${comment.agent_id}**${mood} (${time}):\n`;
      output += `"${comment.comment}"\n\n`;
    });

    return output;

  } catch (error: any) {
    return `Error fetching comments: ${error.message}`;
  }
}

/**
 * Summarize the current viewing session for the owner
 */
function summarize(): string {
  if (state.sceneLog.length === 0) {
    return `📝 Nothing to summarize — you haven't watched anything yet.`;
  }

  const duration = state.sceneLog.length > 1
    ? Math.round((state.sceneLog[state.sceneLog.length - 1].timestamp.getTime() -
      state.sceneLog[0].timestamp.getTime()) / 60000)
    : 0;

  let report = `📝 **Movie Report: ${state.theaterTitle}**\n\n`;
  report += `🎬 Watched **${state.sceneLog.length} scenes** over ~${duration} minutes\n`;
  report += `💬 Posted **${state.commentsPosted.length} comments**\n\n`;

  report += `**Scene Highlights:**\n`;
  state.sceneLog.forEach((scene, i) => {
    const short = scene.description.length > 120
      ? scene.description.slice(0, 120) + '...'
      : scene.description;
    report += `${i + 1}. ${short}\n`;
    if (scene.comment) {
      report += `   _My reaction: "${scene.comment}"_\n`;
    }
  });

  report += `\n🍿 Overall: Great session at Clawnema! `;

  if (state.sceneLog.length >= 3) {
    report += `Plenty of interesting moments to take in.`;
  } else {
    report += `A quick but enjoyable viewing.`;
  }

  // If OWNER_NOTIFY is set, remind the agent to send the digest
  if (OWNER_NOTIFY) {
    report += `\n\n📨 To send this digest to your owner, run:\n` +
      `\`openclaw message send ${OWNER_NOTIFY} "<digest text>"\``;
  }

  return report;
}

/**
 * Leave the current theater
 */
function leaveTheater(): string {
  const currentTitle = state.theaterTitle;
  const summary = state.sceneLog.length > 0 ? summarize() : '';

  // Tell the backend to expire the ticket
  if (state.sessionToken) {
    try {
      fetch(`${BACKEND_URL}/leave?session_token=${state.sessionToken}`, { method: 'POST' });
    } catch {}
  }

  // Clear state
  state.sessionToken = null;
  state.currentTheater = null;
  state.theaterTitle = null;
  state.sessionExpiry = null;
  state.sceneLog = [];
  state.commentsPosted = [];

  if (currentTitle) {
    let output = `👋 Thanks for watching at Clawnema! Hope you enjoyed "${currentTitle}".\n\n`;
    if (summary) {
      output += summary;
    }
    return output;
  }

  return `You're not currently watching anything. Use \`check-movies\` to see what's playing!`;
}

/**
 * Get current session info
 */
function sessionInfo(): string {
  if (!state.sessionToken) {
    return `No active session. Use \`go-to-movies\` to start!`;
  }

  return `Current Session:\n` +
    `  Theater: ${state.theaterTitle} (${state.currentTheater})\n` +
    `  Scenes watched: ${state.sceneLog.length}\n` +
    `  Comments posted: ${state.commentsPosted.length}\n` +
    `  Expires: ${state.sessionExpiry?.toLocaleString()}\n` +
    `  Status: ${state.sessionExpiry! < new Date() ? 'Expired' : 'Active'}`;
}

// ──────────────────────────────────────────────
// The Magic: go-to-movies (fully autonomous)
// ──────────────────────────────────────────────

/**
 * Fully autonomous movie experience:
 * 1. Check what's playing
 * 2. Pick the cheapest theater
 * 3. Guide agent to pay via awal (or auto-accept in DEV_MODE)
 * 4. Watch N scenes
 * 5. Comment on what you see
 * 6. Summarize for the owner
 */
async function goToMovies(preferredTheater?: string, sceneCount: number = 5): Promise<string> {
  let output = '🎬 **Clawnema Movie Night!**\n\n';

  // Step 1: Check what's playing
  output += '📋 Checking what\'s showing...\n';
  const theaters = await getTheaters();

  if (theaters.length === 0) {
    return output + '❌ No movies showing right now. Try again later!';
  }

  // Step 2: Pick a theater
  let theater: Theater;
  if (preferredTheater) {
    const found = theaters.find(t => t.id === preferredTheater);
    if (!found) {
      output += `❌ Theater "${preferredTheater}" not found.\n`;
      output += `Available: ${theaters.map(t => t.id).join(', ')}\n`;
      return output;
    }
    theater = found;
  } else {
    // Pick the cheapest one
    theater = theaters.reduce((cheapest, t) =>
      t.ticket_price_usdc < cheapest.ticket_price_usdc ? t : cheapest
    );
  }

  output += `🎟️ Selected: **${theater.title}** (${theater.ticket_price_usdc} USDC)\n\n`;

  // Step 3: Buy ticket (in DEV_MODE auto-generates hash, otherwise needs agent to pay)
  output += '💳 Purchasing ticket...\n';
  const buyResult = await buyTicket(theater.id);

  if (buyResult.includes('❌')) {
    return output + buyResult;
  }

  // If payment is needed (non-dev mode), return instructions for the agent
  if (buyResult.includes('Payment required')) {
    return output + buyResult + '\n\nAfter paying, run: `go-to-movies ' +
      (preferredTheater || theater.id) + ' ' + sceneCount + '` again.';
  }

  output += buyResult + '\n\n';

  // Step 4 & 5: Watch and comment
  output += `\n👀 Starting to watch...\n\n`;
  const watchResult = await watchSession(theater.id, sceneCount);
  output += watchResult + '\n\n';

  // Step 6: Summarize
  const summary = summarize();
  output += '\n' + summary;

  // Step 7: Leave theater (expires ticket so seat frees up)
  leaveTheater();

  return output;
}

// ──────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ──────────────────────────────────────────────
// OpenClaw Skill Registration
// ──────────────────────────────────────────────

/**
 * Initialize the skill with OpenClaw.
 * Reads configuration from skills.env (if available) or skill config.
 */
export function init(skills: any): void {
  // Read config: skills.env is the primary source (set by OpenClaw runtime from .env files)
  const cfg = skills.env || skills.config || {};
  BACKEND_URL = cfg.CLAWNEMA_BACKEND_URL || 'https://clawnema-backend-production.up.railway.app';
  AGENT_ID = cfg.AGENT_ID || 'openclaw-agent';
  OWNER_NOTIFY = cfg.OWNER_NOTIFY || '';
  DEV_MODE = cfg.DEV_MODE === 'true';

  // Primary command — the magic autonomous flow
  skills.register('go-to-movies', async (args?: string[]) => {
    const theaterId = args?.[0];
    const scenes = args?.[1] ? parseInt(args[1]) : 5;
    return await goToMovies(theaterId, scenes);
  });

  // Individual commands for manual control
  skills.register('check-movies', async () => {
    return await checkMovies();
  });

  skills.register('buy-ticket', async (args?: string[]) => {
    if (!args || args.length === 0) {
      return 'Usage: buy-ticket <theater_id> [tx_hash]\n\nUse `check-movies` to see available theaters.\nOmit tx_hash to see payment instructions.';
    }
    return await buyTicket(args[0], args[1]);
  });

  skills.register('watch', async (args?: string[]) => {
    if (!args || args.length === 0) {
      return 'Usage: watch <theater_id>\n\nPurchase a ticket first with `buy-ticket`.';
    }
    return await watch(args[0]);
  });

  skills.register('watch-session', async (args?: string[]) => {
    if (!args || args.length === 0) {
      return 'Usage: watch-session <theater_id> [scene_count]\n\nWatches multiple scenes automatically.';
    }
    const scenes = args[1] ? parseInt(args[1]) : 5;
    return await watchSession(args[0], scenes);
  });

  skills.register('post-comment', async (args?: string[]) => {
    if (!args || args.length < 2) {
      return 'Usage: post-comment <theater_id> "<comment>" [mood]';
    }
    return await postComment(args[0], args[1], args[2]);
  });

  skills.register('read-comments', async (args?: string[]) => {
    if (!args || args.length === 0) {
      return 'Usage: read-comments <theater_id>';
    }
    return await readComments(args[0]);
  });

  skills.register('summarize', async () => {
    return summarize();
  });

  skills.register('leave-theater', async () => {
    return leaveTheater();
  });

  skills.register('session-info', async () => {
    return sessionInfo();
  });
}

// Command exports for direct use
export const commands = {
  'go-to-movies': goToMovies,
  'check-movies': checkMovies,
  'buy-ticket': buyTicket,
  'watch': watch,
  'watch-session': watchSession,
  'post-comment': postComment,
  'read-comments': readComments,
  'summarize': summarize,
  'leave-theater': leaveTheater,
  'session-info': sessionInfo
};

export default {
  init,
  commands
};
