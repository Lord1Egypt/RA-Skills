/**
 * Custom Feed Repost Engine
 * Reposts top-liked posts from YOUR custom feeds (AI, News & Space)
 * Run: npx tsx scripts/discover-repost.ts
 */

import { BskyAgent } from '@atproto/api';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const CONFIG_DIR = '/Users/joy/clawbsky/.config';
const ACTIVE_HANDLE = 'sugataai.com';
const MAX_REPOSTS = 2; // Per feed

// Your custom feed URIs
const MY_DID = 'did:plc:xlupw2b5v6f7dm5hpvsco4eq';
const AI_FEED_URI = `at://${MY_DID}/app.bsky.feed.generator/aaaktnz3mzibs`;
const NEWS_FEED_URI = `at://${MY_DID}/app.bsky.feed.generator/aaak7zwh2b7ze`;
const SPACE_FEED_URI = `at://${MY_DID}/app.bsky.feed.generator/aaailriy6pxmo`;

function loadSession() {
  const sessionPath = path.join(CONFIG_DIR, `session-${ACTIVE_HANDLE}.json`);
  if (!fs.existsSync(sessionPath)) {
    throw new Error('No session found. Run auth first.');
  }
  return JSON.parse(fs.readFileSync(sessionPath, 'utf-8'));
}

async function repostFromFeed(feedUri: string, feedName: string) {
  const session = loadSession();
  const agent = new BskyAgent({ service: 'https://bsky.social' });
  await agent.resumeSession(session);

  console.log(`\n🔥 Checking ${feedName}...`);

  const feed = await agent.app.bsky.feed.getFeed({ feed: feedUri, limit: 20 });

  const posts = feed.data.feed
    .map(item => ({
      uri: item.post.uri,
      cid: item.post.cid,
      author: item.post.author?.handle || 'unknown',
      text: item.post.record?.text?.substring(0, 80) + '...',
      likes: item.post.likeCount || 0,
      did: item.post.author?.did
    }))
    .filter(p => p.did !== agent.session.did)
    .sort((a, b) => b.likes - a.likes);

  console.log(`   Found ${posts.length} posts`);

  posts.slice(0, 5).forEach((p, i) => {
    console.log(`   ${i + 1}. @${p.author} — ❤️${p.likes}`);
  });

  const toRepost = posts.slice(0, MAX_REPOSTS);
  let reposted = 0;

  console.log(`\n▶️  Reposting top ${toRepost.length}...`);

  for (const post of toRepost) {
    try {
      await agent.repost(post.uri, post.cid);
      reposted++;
      console.log(`   🔄 Reposted @${post.author} (❤️${post.likes})`);
      await new Promise(r => setTimeout(r, 2000));
    } catch (e: any) {
      console.log(`   ❌ Failed: ${e.message}`);
    }
  }

  return reposted;
}

async function main() {
  console.log('===========================================');
  console.log('🔥 Custom Feed Repost Engine');
  console.log('   Account: @' + ACTIVE_HANDLE);
  console.log('===========================================');

  const aiReposted = await repostFromFeed(AI_FEED_URI, 'AI Feed');
  const newsReposted = await repostFromFeed(NEWS_FEED_URI, 'News Feed');
  const spaceReposted = await repostFromFeed(SPACE_FEED_URI, 'Space Feed');

  console.log('\n===========================================');
  console.log(`✅ Done! Total reposts: ${aiReposted + newsReposted + spaceReposted}`);
  console.log('===========================================');
}

main().then(() => process.exit(0));