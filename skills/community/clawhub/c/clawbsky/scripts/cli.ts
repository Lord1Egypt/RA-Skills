#!/usr/bin/env tsx
/**
 * Clawbsky CLI - Main Entry Point
 * Bluesky CLI for power users with AI capabilities
 */

import { Command } from 'commander';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

dotenv.config();

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, '../package.json'), 'utf-8'));

const program = new Command();

// Configure root program options and details
program
  .name('clawbsky')
  .description('🦞 Powerful Bluesky CLI with AI capabilities')
  .version(packageJson.version)
  .option('-u, --user <handle>', 'Specify which Bluesky handle/session to execute this command under');

// ============== CORE AUTHENTICATION ==============

import { login, whoami, logout, listSessions, switchSession, getActiveHandle } from './auth.js';
import { getAgent } from './bsky.js';

program
  .command('login')
  .description('Login to Bluesky')
  .action(async () => {
    try {
      await login();
      console.log('✅ Logged in successfully!');
    } catch (error: any) {
      console.error('❌ Login failed:', error.message);
      process.exit(1);
    }
  });

program
  .command('whoami')
  .description('Show current account details')
  .action(async () => {
    try {
      const account = await whoami();
      console.log(`\n🦞 Currently active session: @${account.handle}`);
      console.log(`DID: ${account.did}\n`);
      
      const sessions = listSessions();
      if (sessions.length > 1) {
        console.log('Other profiles logged in:');
        sessions.forEach(s => {
          if (s !== account.handle) {
            console.log(`  - @${s}`);
          }
        });
        console.log('');
      }
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Multi-user authentication profile command group
const authCmd = program.command('auth').description('Manage multi-user authentication profiles');

authCmd
  .command('list')
  .description('List all logged-in profiles')
  .action(() => {
    try {
      const sessions = listSessions();
      const active = getActiveHandle();
      console.log('\n👤 Authenticated Profiles:\n');
      if (sessions.length === 0) {
        console.log('  No logged-in accounts. Run "clawbsky login" first.');
      } else {
        sessions.forEach(handle => {
          const isActive = handle === active;
          console.log(`  ${isActive ? '👉 \x1b[32m[Active]\x1b[0m' : '   '} @${handle}`);
        });
      }
      console.log('');
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

authCmd
  .command('switch <handle>')
  .description('Switch the default active profile')
  .action((handle: string) => {
    try {
      const cleanHandle = handle.startsWith('@') ? handle.substring(1) : handle;
      switchSession(cleanHandle);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

authCmd
  .command('logout [handle]')
  .description('Log out of a specific profile or the active profile')
  .action(async (handle: string | undefined) => {
    try {
      const cleanHandle = handle && handle.startsWith('@') ? handle.substring(1) : handle;
      await logout(cleanHandle);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });


// ============== READING COMMANDS ==============

import { readPost, readThread, readUser, readHome, readMentions } from './read.js';

const readCmd = program.command('read').description('Read posts');
readCmd.command('post <uri>').description('Read a single post').action(readPost);
readCmd.command('thread <uri>').description('Read a thread').action(readThread);
readCmd.command('user <handle>').description('Read user profile').action(readUser);
readCmd.command('home').description('Read home timeline').action(readHome);
readCmd.command('mentions').description('Read mentions').action(readMentions);

// ============== POSTING COMMANDS ==============

import { post, reply, quote, thread, like, repost, deletePost } from './post.js';

const postCmd = program.command('post').description('Post content');
postCmd.command('text <text>').description('Post text').action(async (text: string) => {
  const agent = await getAgent();
  await post(agent, text);
});

postCmd.command('reply <text> <uri>').description('Reply to a post').action(async (text: string, uri: string) => {
  const agent = await getAgent();
  await reply(agent, text, uri);
});

// ============== AI GENERATION COMMANDS ==============

import { generate, generateThread, improveText, replyAi, analyze } from './ai/generate.js';

program
  .command('generate')
  .description('AI-powered content generation')
  .argument('<prompt>', 'Prompt for content generation')
  .option('-t, --tone <tone>', 'Tone: professional, casual, funny, helpful', 'helpful')
  .option('--thread', 'Generate a thread instead of single post')
  .option('--posts <number>', 'Number of posts in thread', '5')
  .option('--improve <text>', 'Improve existing text')
  .option('-- hashtags', 'Generate hashtags')
  .action(async (prompt: string, options: any) => {
    try {
      if (options.improve) {
        const result = await improveText(options.improve);
        console.log('\n✨ Improved:\n' + result);
      } else if (options.thread) {
        const result = await generateThread(prompt, parseInt(options.posts));
        console.log('\n🧵 Generated Thread:\n');
        result.forEach((p, i) => console.log(`${i + 1}/${result.length}: ${p}\n`));
      } else {
        const result = await generate(prompt, options.tone);
        console.log('\n🤖 AI Generated:\n' + result);
      }
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('reply-ai <uri>')
  .description('AI reply suggestions for a post')
  .option('-c, --count <number>', 'Number of suggestions', '3')
  .option('--post', 'Post the best reply automatically')
  .action(async (uri: string, options: any) => {
    try {
      const suggestions = await replyAi(uri, parseInt(options.count));
      console.log('\n💬 AI Reply Suggestions:\n');
      suggestions.forEach((s, i) => console.log(`${i + 1}. ${s}\n`));
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('analyze <target>')
  .description('AI analysis of a profile or post')
  .option('-p, --post', 'Analyze a post instead of profile')
  .action(async (target: string, options: any) => {
    try {
      const result = await analyze(target, options.post);
      console.log('\n📊 Analysis:\n' + result);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// ============== SCHEDULER COMMANDS ==============

import { schedulePost, listScheduled, runScheduler } from './automation/scheduler.js';

program
  .command('schedule')
  .description('Schedule posts for later')
  .argument('<text>', 'Post text')
  .option('-a, --at <datetime>', 'Schedule time (ISO format)', '')
  .option('--in <duration>', 'Schedule in relative time (e.g., 1h, 2d)')
  .action(async (text: string, options: any) => {
    try {
      let scheduledAt = options.at;
      
      // Parse relative time
      if (options.in) {
        const match = options.in.match(/(\d+)([hHdDmM])/);
        if (match) {
          const amount = parseInt(match[1]);
          const unit = match[2].toLowerCase();
          const date = new Date();
          
          if (unit === 'm') date.setMinutes(date.getMinutes() + amount);
          if (unit === 'h') date.setHours(date.getHours() + amount);
          if (unit === 'd') date.setDate(date.getDate() + amount);
          
          scheduledAt = date.toISOString();
        }
      }
      
      if (!scheduledAt) {
        console.log('Please specify --at or --in');
        process.exit(1);
      }
      
      const result = await schedulePost(text, scheduledAt);
      console.log(`✅ Post scheduled for ${scheduledAt}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('scheduled')
  .description('List scheduled posts')
  .action(async () => {
    try {
      const posts = await listScheduled();
      console.log('\n📅 Scheduled Posts:\n');
      posts.forEach((p: any) => {
        console.log(`[${p.id}] ${p.text.substring(0, 50)}...`);
        console.log(`    Scheduled: ${p.scheduledAt}`);
        console.log(`    Status: ${p.status}\n`);
      });
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('scheduler')
  .description('Run the scheduler daemon')
  .action(async () => {
    console.log('🚀 Starting scheduler daemon...');
    await runScheduler();
  });

// ============== ANALYTICS COMMANDS ==============

import { getEngagementStats, getTopPosts, getFollowerGrowth } from './analytics/engagement.js';
import { suggestBestPostTimes } from './analytics/besttimes.js';

program
  .command('stats')
  .description('Show engagement statistics')
  .option('-d, --days <number>', 'Number of days', '7')
  .action(async (options: any) => {
    try {
      const stats = getEngagementStats(parseInt(options.days));
      console.log('\n📊 Engagement Stats:\n');
      console.log(`Total Posts: ${stats.totalPosts}`);
      console.log(`Total Likes: ${stats.totalLikes}`);
      console.log(`Total Reposts: ${stats.totalReposts}`);
      console.log(`Total Replies: ${stats.totalReplies}`);
      console.log(`\nAverages per post:`);
      console.log(`  Likes: ${stats.avgLikes}`);
      console.log(`  Reposts: ${stats.avgReposts}`);
      console.log(`  Replies: ${stats.avgReplies}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('top')
  .description('Show top performing posts')
  .option('-l, --limit <number>', 'Number of posts', '10')
  .option('-s, --sort <sort>', 'Sort by: likes, reposts, replies', 'likes')
  .action(async (options: any) => {
    try {
      const posts = await getTopPosts(parseInt(options.limit), options.sort as any);
      console.log(`\n🏆 Top ${posts.length} Posts:\n`);
      posts.forEach((p: any, i: number) => {
        console.log(`${i + 1}. ${p.text.substring(0, 50)}...`);
        console.log(`   ❤️ ${p.likes} | 🔄 ${p.reposts} | 💬 ${p.replies}\n`);
      });
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('growth')
  .description('Show follower growth')
  .option('-d, --days <number>', 'Number of days', '30')
  .action(async (options: any) => {
    try {
      const growth = getFollowerGrowth(parseInt(options.days));
      console.log('\n📈 Follower Growth:\n');
      console.log(`Growth: ${growth.growth > 0 ? '+' : ''}${growth.growth}`);
      console.log(`Percentage: ${growth.percentage}%`);
      console.log(`Trend: ${growth.trend}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('best-times')
  .description('AI suggests best posting times')
  .action(async () => {
    try {
      const times = await suggestBestPostTimes();
      console.log('\n⏰ Best Times to Post:\n');
      times.recommendations.forEach((r: any, i: number) => {
        console.log(`${i + 1}. ${r.day} at ${r.time}`);
        console.log(`   Score: ${r.score}/100 - ${r.reason}\n`);
      });
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// ============== COMMUNITY MANAGEMENT ==============

import { createList, getLists, addToList, getMutedUsers, findInactiveFollowers } from './community/index.js';

program
  .command('list')
  .description('List management')
  .argument('<action>', 'Action: create, add, remove, show')
  .option('-n, --name <name>', 'List name')
  .option('-m, --members <handles>', 'Comma-separated handles')
  .action(async (action: string, options: any) => {
    try {
      if (action === 'create' && options.name) {
        const id = createList(options.name);
        console.log(`✅ List "${options.name}" created (ID: ${id})`);
      } else if (action === 'show') {
        const lists = getLists();
        console.log('\n📋 Your Lists:\n');
        lists.forEach((l: any) => console.log(`[${l.id}] ${l.name} (${l.memberCount} members)`));
      }
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// Mute and cleanup require login - comment out for now
// These would need agent to be passed

program
  .command('cleanup')
  .description('Cleanup inactive followers (requires login)')
  .option('-d, --days <number>', 'Days of inactivity', '90')
  .option('-l, --limit <number>', 'Limit of followers to cleanup at a time', '500')
  .action(async (options: any) => {
    try {
      const agent = await getAgent();
      const days = parseInt(options.days, 10) || 90;
      const limit = parseInt(options.limit, 10) || 500;
      console.log(`🔍 Scanning for followers inactive for more than ${days} days (looking for up to ${limit} inactive ones)...`);
      const inactive = await findInactiveFollowers(agent, days, limit);

      if (inactive.length === 0) {
        console.log('✨ No inactive followers found!');
        return;
      }

      console.log(`⚠️ Found ${inactive.length} inactive followers.`);
      const toClean = inactive.slice(0, limit);

      console.log(`\n🚀 Starting cleanup of ${toClean.length} inactive followers...`);
      let count = 0;
      const myDid = agent.session!.did;

      for (const did of toClean) {
        try {
          const profile = await agent.getProfile({ actor: did });
          
          // 1. Unfollow if we follow them
          const followUri = profile.data.viewer?.following;
          if (followUri) {
            const rkey = followUri.split("/").pop();
            if (rkey) {
              await agent.app.bsky.graph.follow.delete({
                repo: myDid,
                rkey: rkey
              });
            }
          }

          // 2. Soft-block (block & unblock) to remove them from our followers list
          const blockRes = await agent.app.bsky.graph.block.create(
            { repo: myDid },
            { subject: did, createdAt: new Date().toISOString() }
          );
          const blockRkey = blockRes.uri.split("/").pop();
          if (blockRkey) {
            await agent.app.bsky.graph.block.delete({
              repo: myDid,
              rkey: blockRkey
            });
          }

          count++;
          console.log(`[${count}/${toClean.length}] ✅ Cleaned up @${profile.data.handle}`);

          if (count < toClean.length) {
            await new Promise(r => setTimeout(r, 500));
          }
        } catch (err: any) {
          console.warn(`\n❌ Failed to clean up ${did}: ${err.message}`);
        }
      }

      console.log(`\nDone! Cleaned up ${count} inactive followers.`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('unfollow-non-mutuals')
  .description('Unfollow a specific number of non-mutuals')
  .option('-n, --count <number>', 'Number of non-mutuals to unfollow', '500')
  .option('--dry-run', 'Preview who would be unfollowed')
  .action(async (options: any) => {
    try {
      const agent = await getAgent();
      const myDid = agent.session!.did;
      const targetLimit = parseInt(options.count, 10) || 500;

      console.log(`🔍 Identifying non-mutuals (limit: ${targetLimit})...`);

      let cursor: string | undefined;
      const nonMutuals: any[] = [];
      let totalFollowsChecked = 0;
      let noMoreNonMutuals = false;

      // 1. Traverse follows to find non-mutuals
      while (nonMutuals.length < targetLimit) {
        const res = await agent.getFollows({
          actor: myDid,
          cursor,
          limit: 100,
        });

        if (!res.data.follows || res.data.follows.length === 0) {
          noMoreNonMutuals = true;
          break;
        }

        for (const follow of res.data.follows) {
          if (nonMutuals.length >= targetLimit) break;

          totalFollowsChecked++;
          if (!follow.viewer?.followedBy) {
            nonMutuals.push(follow);
          }
        }

        cursor = res.data.cursor;
        process.stdout.write(`\rScanned ${totalFollowsChecked} follows, found ${nonMutuals.length}/${targetLimit} non-mutuals...`);
        if (!cursor) {
          if (nonMutuals.length < targetLimit) {
            noMoreNonMutuals = true;
          }
          break;
        }
      }
      process.stdout.write("\n");

      if (nonMutuals.length === 0) {
        console.log("✨ All your follows are mutual! Nothing to cleanup.");
        return;
      }

      if (noMoreNonMutuals) {
        console.log("ℹ️ No more non-mutuals to unfollow (reached the end of your follows list).");
      }

      console.log(`⚠️ Found ${nonMutuals.length} accounts that do not follow you back.`);

      const isDryRun = options.dryRun;

      if (isDryRun) {
        console.log("\n[DRY RUN] The following accounts would be unfollowed:");
        for (const user of nonMutuals) {
          console.log(`- @${user.handle}${user.displayName ? ` (${user.displayName})` : ""}`);
        }
        console.log("\nTo perform the unfollow, run without --dry-run");
        return;
      }

      console.log(`\n🚀 Starting unfollow process for ${nonMutuals.length} accounts...`);
      let count = 0;
      for (const user of nonMutuals) {
        const followUri = user.viewer?.following;
        if (!followUri) continue;

        const rkey = followUri.split("/").pop();
        if (!rkey) continue;

        try {
          await agent.app.bsky.graph.follow.delete({
            repo: myDid,
            rkey: rkey
          });
          count++;
          console.log(`[${count}/${nonMutuals.length}] ✅ Unfollowed @${user.handle}`);

          if (count < nonMutuals.length) {
            await new Promise(r => setTimeout(r, 500));
          }
        } catch (err: any) {
          console.warn(`\n❌ Failed to unfollow @${user.handle}: ${err.message}`);
          if (err.message.toLowerCase().includes("rate limit")) {
            console.log("Stopped due to rate limiting.");
            break;
          }
        }
      }

      console.log(`\nDone! Cleaned up ${count} non-mutual follows.`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('follow <handle>')
  .description('Follow a user')
  .action(async (handle: string) => {
    try {
      const agent = await getAgent();
      const profile = await agent.getProfile({ actor: handle });
      const did = profile.data.did;
      await agent.follow(did);
      console.log(`✅ Now following @${handle}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('unfollow <handle>')
  .description('Unfollow a user')
  .action(async (handle: string) => {
    try {
      const agent = await getAgent();
      const profile = await agent.getProfile({ actor: handle });
      const followUri = profile.data.viewer?.following;
      if (!followUri) {
        console.error(`You are not following @${handle}`);
        process.exit(1);
      }
      const rkey = followUri.split("/").pop();
      if (!rkey) throw new Error("Invalid follow URI");
      await agent.app.bsky.graph.follow.delete({
        repo: agent.session!.did,
        rkey: rkey
      });
      console.log(`✅ Unfollowed @${handle}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('followers <handle>')
  .description("List a user's followers")
  .option('-n, --count <number>', 'Number of results', '20')
  .action(async (handle: string, options: any) => {
    try {
      const agent = await getAgent();
      const limit = parseInt(options.count, 10) || 20;
      const res = await agent.getFollowers({ actor: handle, limit });
      console.log(`\n👥 Followers of @${handle}:\n`);
      for (const f of res.data.followers) {
        console.log(`@${f.handle}${f.displayName ? ` (${f.displayName})` : ""}`);
      }
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('following <handle>')
  .description("List who a user is following")
  .option('-n, --count <number>', 'Number of results', '20')
  .action(async (handle: string, options: any) => {
    try {
      const agent = await getAgent();
      const limit = parseInt(options.count, 10) || 20;
      const res = await agent.getFollows({ actor: handle, limit });
      console.log(`\n👤 @${handle} follows:\n`);
      for (const f of res.data.follows) {
        console.log(`@${f.handle}${f.displayName ? ` (${f.displayName})` : ""}`);
      }
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('like <uri>')
  .description('Like a post')
  .action(async (uri: string) => {
    try {
      const agent = await getAgent();
      const res = await agent.getPosts({ uris: [uri] });
      if (res.data.posts.length === 0) {
        console.error("Post not found");
        process.exit(1);
      }
      const post = res.data.posts[0];
      await agent.like(uri, post.cid);
      console.log(`✅ Liked post: ${uri}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('unlike <uri>')
  .description('Unlike a post')
  .action(async (uri: string) => {
    try {
      const agent = await getAgent();
      const res = await agent.getPosts({ uris: [uri] });
      if (res.data.posts.length === 0) {
        console.error("Post not found");
        process.exit(1);
      }
      const post = res.data.posts[0];
      const likeUri = post.viewer?.like;
      if (!likeUri) {
        console.error("You haven't liked this post.");
        process.exit(1);
      }
      await agent.deleteLike(likeUri);
      console.log(`✅ Unliked post: ${uri}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('repost <uri>')
  .description('Repost a post')
  .action(async (uri: string) => {
    try {
      const agent = await getAgent();
      const res = await agent.getPosts({ uris: [uri] });
      if (res.data.posts.length === 0) {
        console.error("Post not found");
        process.exit(1);
      }
      const post = res.data.posts[0];
      await agent.repost(uri, post.cid);
      console.log(`✅ Reposted post: ${uri}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('unrepost <uri>')
  .description('Unrepost a post')
  .action(async (uri: string) => {
    try {
      const agent = await getAgent();
      const res = await agent.getPosts({ uris: [uri] });
      if (res.data.posts.length === 0) {
        console.error("Post not found");
        process.exit(1);
      }
      const post = res.data.posts[0];
      const repostUri = post.viewer?.repost;
      if (!repostUri) {
        console.error("You haven't reposted this post.");
        process.exit(1);
      }
      await agent.deleteRepost(repostUri);
      console.log(`✅ Unreposted post: ${uri}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('block <handle>')
  .description('Block a user')
  .action(async (handle: string) => {
    try {
      const agent = await getAgent();
      const profile = await agent.getProfile({ actor: handle });
      await agent.app.bsky.graph.block.create(
        { repo: agent.session!.did },
        {
          subject: profile.data.did,
          createdAt: new Date().toISOString()
        }
      );
      console.log(`✅ Blocked @${handle}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('unblock <handle>')
  .description('Unblock a user')
  .action(async (handle: string) => {
    try {
      const agent = await getAgent();
      const profile = await agent.getProfile({ actor: handle });
      const blockUri = profile.data.viewer?.blocking;
      if (!blockUri) {
        console.error(`You are not blocking @${handle}`);
        process.exit(1);
      }
      const rkey = blockUri.split("/").pop();
      if (!rkey) throw new Error("Invalid block URI");
      await agent.app.bsky.graph.block.delete({
        repo: agent.session!.did,
        rkey: rkey
      });
      console.log(`✅ Unblocked @${handle}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('mute <handle>')
  .description('Mute a user')
  .action(async (handle: string) => {
    try {
      const agent = await getAgent();
      await agent.mute(handle);
      console.log(`✅ Muted @${handle}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('unmute <handle>')
  .description('Unmute a user')
  .action(async (handle: string) => {
    try {
      const agent = await getAgent();
      await agent.unmute(handle);
      console.log(`✅ Unmuted @${handle}`);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// ============== RSS & INTEGRATIONS ==============

import { addRssFeed, getRssFeeds, processRssFeeds } from './integrations/index.js';

program
  .command('rss')
  .description('RSS feed automation')
  .argument('<action>', 'Action: add, list, process')
  .option('-n, --name <name>', 'Feed name')
  .option('--url <url>', 'Feed URL')
  .option('-s, --schedule <schedule>', 'Schedule: hourly, daily, weekly')
  .action(async (action: string, options: any) => {
    try {
      if (action === 'add' && options.name && options.url) {
        const id = addRssFeed(options.name, options.url, options.schedule as any);
        console.log(`✅ RSS feed "${options.name}" added (ID: ${id})`);
      } else if (action === 'list') {
        const feeds = getRssFeeds();
        console.log('\n📰 RSS Feeds:\n');
        feeds.forEach((f: any) => console.log(`[${f.id}] ${f.name} - ${f.url}`));
      } else if (action === 'process') {
        console.log('RSS processing requires login - run clawbsky login first');
      }
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// ============== CONTENT ENHANCEMENT ==============

import { generateAltTextFromDescription, generateQuoteCard, repurposeContent } from './content/index.js';

program
  .command('alt-text')
  .description('Generate ALT text for images')
  .argument('<description>', 'Image description')
  .action(async (description: string) => {
    try {
      const alt = await generateAltTextFromDescription(description);
      console.log('\n🖼️ ALT Text:\n' + alt);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('quote')
  .description('Create a quote card')
  .argument('<quote>', 'Quote text')
  .option('-a, --author <author>', 'Quote author')
  .action(async (quote: string, options: any) => {
    try {
      const result = await generateQuoteCard(quote, options.author);
      console.log('\n📝 Quote Card:\n' + result.text);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('repurpose')
  .description('Repurpose content for different formats')
  .argument('<content>', 'Original content')
  .option('-f, --format <format>', 'Target format: thread, blog, tweet, linkedin', 'thread')
  .action(async (content: string, options: any) => {
    try {
      const result = await repurposeContent(content, options.format as any);
      console.log(`\n🔄 Repurposed (${options.format}):\n` + result);
    } catch (error: any) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

// ============== MAIN ==============

program.parse();