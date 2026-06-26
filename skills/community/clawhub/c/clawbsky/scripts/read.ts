/**
 * Read Module - Reading posts, threads, users
 */

import { getAgent } from './bsky.js';

export async function readPost(uri: string): Promise<void> {
  const agent = await getAgent();
  
  try {
    const threadResponse = await agent.getPostThread({ uri });
    const post = threadResponse.data.thread.post;
    if (!post || !('record' in post)) {
      throw new Error('Post record not found');
    }
    
    console.log(`\n📝 Post by @${post.author.handle}:\n`);
    console.log((post.record as any).text);
    console.log(`\n❤️ ${post.likeCount || 0} | 🔄 ${post.repostCount || 0} | 💬 ${post.replyCount || 0}`);
    console.log(`📅 ${new Date(post.indexedAt).toLocaleString()}\n`);
  } catch (error: any) {
    console.error('Error reading post:', error.message);
    throw error;
  }
}

export async function readThread(uri: string): Promise<void> {
  const agent = await getAgent();
  
  try {
    const threadResponse = await agent.getPostThread({ uri });
    const thread = threadResponse.data.thread;
    
    if (!thread) {
      console.log('Thread not found');
      return;
    }
    
    // Print root post
    const root = 'post' in thread ? thread.post : null;
    if (root && 'record' in root) {
      console.log(`\n🧵 Thread by @${root.author.handle}:\n`);
      console.log((root.record as any).text);
      console.log('---\n');
    }
    
    // Print replies
    if ('replies' in thread && thread.replies) {
      for (const reply of thread.replies) {
        if ('post' in reply && 'record' in reply.post) {
          console.log(`↳ @${reply.post.author.handle}:`);
          console.log((reply.post.record as any).text);
          console.log(`   ❤️ ${reply.post.likeCount || 0} | 🔄 ${reply.post.repostCount || 0}\n`);
        }
      }
    }
  } catch (error: any) {
    console.error('Error reading thread:', error.message);
    throw error;
  }
}

export async function readUser(handle: string): Promise<void> {
  const agent = await getAgent();
  
  try {
    const cleanHandle = handle.replace(/^@/, '');
    const profileResponse = await agent.getProfile({ actor: cleanHandle });
    const profile = profileResponse.data;
    
    console.log(`\n👤 @${profile.handle}\n`);
    console.log(`Display Name: ${profile.displayName || 'N/A'}`);
    console.log(`Description: ${profile.description || 'N/A'}`);
    console.log(`\n📊 Stats:`);
    console.log(`   Followers: ${profile.followersCount || 0}`);
    console.log(`   Following: ${profile.followingCount || 0}`);
    console.log(`   Posts: ${profile.postsCount || 0}`);
    console.log(`\n📅 Joined: ${profile.indexedAt ? new Date(profile.indexedAt).toLocaleString() : 'N/A'}\n`);
  } catch (error: any) {
    console.error('Error reading user:', error.message);
    throw error;
  }
}

export async function readHome(): Promise<void> {
  const agent = await getAgent();
  
  try {
    const timeline = await agent.getTimeline({ limit: 20 });
    
    console.log('\n🏠 Home Timeline:\n');
    for (const feedItem of timeline.data.feed) {
      if ('post' in feedItem) {
        const post = feedItem.post;
        if ('record' in post) {
          console.log(`@${post.author.handle}:`);
          console.log((post.record as any).text);
          console.log(`❤️ ${post.likeCount || 0} | 🔄 ${post.repostCount || 0} | 💬 ${post.replyCount || 0}`);
          console.log('---\n');
        }
      }
    }
  } catch (error: any) {
    console.error('Error reading home:', error.message);
    throw error;
  }
}

export async function readMentions(): Promise<void> {
  const agent = await getAgent();
  
  try {
    const mentions = await agent.listNotifications({ limit: 20 });
    
    console.log('\n💬 Mentions:\n');
    for (const notification of mentions.data.notifications) {
      if (notification.reason === 'mention' || notification.reason === 'reply') {
        console.log(`@${notification.author.handle} ${notification.reason}`);
        console.log((notification.record as any)?.text || '');
        console.log('---\n');
      }
    }
  } catch (error: any) {
    console.error('Error reading mentions:', error.message);
    throw error;
  }
}