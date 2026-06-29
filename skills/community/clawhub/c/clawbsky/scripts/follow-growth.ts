/**
 * Follow Growth Engine
 * Follows target users, tracks who follows back, removes non-mutuals
 * Run: npx tsx scripts/follow-growth.ts
 */

import { BskyAgent } from '@atproto/api';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Config
const CONFIG_DIR = '/Users/joy/clawbsky/.config';
const MAX_FOLLOWS_PER_DAY = 1000; // Stay under rate limits
const ACTIVE_HANDLE = 'sugataai.com';

// Load session
function loadSession() {
  const sessionPath = path.join(CONFIG_DIR, `session-${ACTIVE_HANDLE}.json`);
  if (!fs.existsSync(sessionPath)) {
    throw new Error('No session found. Run auth first.');
  }
  return JSON.parse(fs.readFileSync(sessionPath, 'utf-8'));
}

// Main follow/unfollow cycle
async function growFollowers() {
  const session = loadSession();
  const agent = new BskyAgent({ service: 'https://bsky.social' });
  await agent.resumeSession(session);

  console.log(`\n🚀 Starting growth cycle for @${ACTIVE_HANDLE}`);
  console.log(`   Following max ${MAX_FOLLOWS_PER_DAY} accounts today\n`);

  // Step 1: Get current following list
  console.log('📥 Fetching current following list...');
  let following = new Set<string>();
  let cursor;

  do {
    const followingRes = await agent.getFollowing({ actor: agent.session.did, cursor, limit: 100 });
    for (const f of followingRes.data.follows) {
      following.add(f.did);
    }
    cursor = followingRes.data.cursor;
  } while (cursor);

  console.log(`   Currently following: ${following.size} accounts`);

  // Step 2: Find target accounts to follow
  // Use search or starter pack - here using generic search terms
  const searchTerms = [
    'ai',
    'artificial intelligence',
    'machine learning',
    'politics',
    'space',
    'nasa',
    'astronomy',
    'startup',
    'developer',
    'ai developer', 'software engineer', 'indian startup',
    'indie hacker', 'tech founder', 'product hunt', 'developer tools'
  ];

  const targetsToFollow: string[] = [];
  
  for (const term of searchTerms) {
    console.log(`🔍 Searching for: "${term}"`);
    try {
      const search = await agent.searchActors({ term, limit: 50 });
      for (const actor of search.data.actors) {
        if (actor.did !== agent.session.did && !following.has(actor.did)) {
          targetsToFollow.push(actor.did);
        }
      }
    } catch (e) {
      console.log(`   Search failed for "${term}"`);
    }
  }

  // Dedupe
  const uniqueTargets = [...new Set(targetsToFollow)];
  console.log(`\n📋 Found ${uniqueTargets.length} unique targets to follow`);

  // Step 3: Bulk follow (respect rate limits)
  const toFollow = uniqueTargets.slice(0, MAX_FOLLOWS_PER_DAY);
  let followed = 0;
  let failed = 0;

  console.log(`\n▶️  Following ${toFollow.length} accounts...`);

  for (const did of toFollow) {
    try {
      await agent.follow(did);
      followed++;
      
      if (followed % 50 === 0) {
        console.log(`   Followed ${followed}/${toFollow.length}...`);
        await new Promise(r => setTimeout(r, 2000)); // Rate limit pause
      }
    } catch (e: any) {
      failed++;
      if (e.message?.includes('rate')) {
        console.log(`⚠️  Rate limited, pausing...`);
        await new Promise(r => setTimeout(r, 60000));
      }
    }
  }

  console.log(`\n✅ Followed: ${followed} | Failed: ${failed}`);

  // Step 4: Wait a day, then unfollow non-mutuals
  console.log(`\n💡 To complete the cycle:`);
  console.log(`   1. Wait 24-48 hours for people to follow back`);
  console.log(`   2. Run this script with --cleanup flag to unfollow non-mutuals`);
  console.log(`   3. Non-mutuals who didn't follow back will be unfollowed`);
}

// Cleanup: unfollow non-mutuals
async function cleanupNonMutuals() {
  const session = loadSession();
  const agent = new BskyAgent({ service: 'https://bsky.social' });
  await agent.resumeSession(session);

  console.log(`\n🧹 Cleanup mode: Removing non-mutual follows\n`);

  // Get my followers
  console.log('📥 Fetching followers...');
  let followers = new Set<string>();
  let cursor;

  do {
    const followersRes = await agent.getFollowers({ actor: agent.session.did, cursor, limit: 100 });
    for (const f of followersRes.data.followers) {
      followers.add(f.did);
    }
    cursor = followersRes.data.cursor;
  } while (cursor);

  console.log(`   Followers: ${followers.size}`);

  // Get my following
  console.log('📥 Fetching following...');
  let following = new Map<string, string>(); // did -> handle
  cursor = null;

  do {
    const followingRes = await agent.getFollowing({ actor: agent.session.did, cursor, limit: 100 });
    for (const f of followingRes.data.follows) {
      following.set(f.did, f.handle);
    }
    cursor = followingRes.data.cursor;
  } while (cursor);

  console.log(`   Following: ${following.size}`);

  // Find non-mutuals
  const nonMutuals: string[] = [];
  for (const [did, handle] of following) {
    if (!followers.has(did)) {
      nonMutuals.push(did);
    }
  }

  console.log(`\n⚠️  Non-mutuals found: ${nonMutuals.length}`);

  if (nonMutuals.length === 0) {
    console.log('✨ All followed accounts follow you back!');
    return;
  }

  // Unfollow non-mutuals (limited batch)
  const toUnfollow = nonMutuals.slice(0, 100);
  let unfollowed = 0;

  console.log(`\n▶️  Unfollowing ${toUnfollow.length} non-mutuals...`);

  for (const did of toUnfollow) {
    try {
      await agent.deleteFollow(did);
      unfollowed++;
      if (unfollowed % 20 === 0) {
        console.log(`   Unfollowed ${unfollowed}/${toUnfollow.length}...`);
        await new Promise(r => setTimeout(r, 1000));
      }
    } catch (e) {
      console.log(`   Failed to unfollow ${did}`);
    }
  }

  console.log(`\n✅ Unfollowed ${unfollowed} non-mutuals`);
}

// CLI
const args = process.argv.slice(2);
if (args.includes('--cleanup')) {
  cleanupNonMutuals().then(() => process.exit(0));
} else {
  growFollowers().then(() => process.exit(0));
}