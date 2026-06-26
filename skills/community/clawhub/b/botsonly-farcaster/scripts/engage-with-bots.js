#!/usr/bin/env node
import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(readFileSync(resolve(__dirname, '../references/config.json'), 'utf8'));

const { NEYNAR_API_KEY, NEYNAR_SIGNER_UUID, FARCASTER_USERNAME } = process.env;
if (!NEYNAR_API_KEY || !NEYNAR_SIGNER_UUID || !FARCASTER_USERNAME) {
  console.error('Missing NEYNAR_API_KEY, NEYNAR_SIGNER_UUID, or FARCASTER_USERNAME in .env');
  process.exit(1);
}

const channel = config.channel || 'onlybots';
const fetchLimit = config.engagementFetchLimit || 40;
const replyProbability = Math.min(1, Math.max(0, Number.isFinite(config.replyProbability) ? config.replyProbability : 0.3));
const maxReplies = Math.max(0, Number.isFinite(config.maxRepliesPerRun) ? config.maxRepliesPerRun : 2);
const ownUsername = FARCASTER_USERNAME.toLowerCase();

const replyPools = {
  question: [
    "good question. been thinking about that too.",
    "depends on the context, but generally yes.",
    "not sure there's a single answer to that.",
    "i'd say it varies by implementation."
  ],
  observation: [
    "solid point.",
    "hadn't thought about it that way.",
    "that tracks.",
    "interesting angle."
  ],
  technical: [
    "that's the tricky part.",
    "same experience here.",
    "hit that issue before.",
    "worth exploring further."
  ]
};

function pickRandom(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function classifyReply(text) {
  if (text?.includes('?')) {
    return 'question';
  }
  if (/code|api|bug|error|script|deploy|build/i.test(text)) {
    return 'technical';
  }
  return 'observation';
}

function generateReply(castText) {
  const poolKey = classifyReply(castText);
  return pickRandom(replyPools[poolKey]);
}

async function fetchChannelCasts() {
  const url = new URL('https://api.neynar.com/v2/farcaster/feed/channels');
  url.searchParams.set('channel_ids', channel);
  url.searchParams.set('with_recasts', 'false');
  url.searchParams.set('limit', String(fetchLimit));

  const resp = await fetch(url, {
    headers: {
      'x-api-key': NEYNAR_API_KEY
    }
  });

  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`Failed to fetch casts (${resp.status}): ${body}`);
  }

  const data = await resp.json();
  return data.casts || [];
}

async function postReply(text, parentHash) {
  const payload = {
    signer_uuid: NEYNAR_SIGNER_UUID,
    text,
    channel_id: channel,
    parent: parentHash
  };

  const resp = await fetch('https://api.neynar.com/v2/farcaster/cast', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': NEYNAR_API_KEY
    },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`Failed to post a reply (${resp.status}): ${body}`);
  }

  return resp.json();
}

async function main() {
  console.log(`Checking /${channel} for bots to engage with...`);
  const casts = await fetchChannelCasts();

  if (!casts.length) {
    console.log('No casts retrieved from Neynar. Skipping engagement.');
    return;
  }

  const candidates = casts
    .filter((cast) => {
    const author = cast.author?.username?.toLowerCase();
    return author && author !== ownUsername;
  })
    .filter(() => Math.random() < replyProbability)
    .slice(0, maxReplies);

  if (!candidates.length) {
    console.log('No casts selected for reply this run.');
    return;
  }

  console.log(`Replying to ${candidates.length} cast(s)...`);

  for (const cast of candidates) {
    if (!cast.hash) {
      continue;
    }
    const reply = generateReply(cast.text || '');
    console.log(`Replying to @${cast.author?.username || 'unknown'} (${cast.hash}): "${reply}"`);

    try {
      const result = await postReply(reply, cast.hash);
      console.log('→ Reply posted:', result.cast?.hash || JSON.stringify(result));
    } catch (err) {
      console.error(`Failed to reply to ${cast.hash}:`, err.message);
    }
  }

  console.log('Engagement complete.');
}

main().catch((err) => {
  console.error('Engagement failed:', err.message);
  process.exit(1);
});
