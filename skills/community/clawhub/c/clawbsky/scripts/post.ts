/**
 * Post Module - Posting, replying, liking
 */

import { BskyAgent } from '@atproto/api';

export async function post(agent: BskyAgent, text: string, media?: string[]): Promise<void> {
  try {
    await agent.post({
      text,
      createdAt: new Date().toISOString()
    });
    console.log('✅ Posted successfully!');
  } catch (error: any) {
    console.error('Error posting:', error.message);
    throw error;
  }
}

export async function reply(
  agent: BskyAgent, 
  text: string, 
  parentUri: string, 
  parentCid?: string
): Promise<void> {
  try {
    // Get parent post if CID not provided
    if (!parentCid) {
      const parentPost = await agent.getPostThread({ uri: parentUri });
      const post = parentPost.data.thread.post;
      if ('cid' in post) {
        parentCid = post.cid as string;
      } else {
        throw new Error('Could not retrieve parent CID');
      }
    }

    await agent.post({
      text,
      reply: {
        parent: { uri: parentUri, cid: parentCid },
        root: { uri: parentUri, cid: parentCid }
      },
      createdAt: new Date().toISOString()
    });
    console.log('✅ Reply posted successfully!');
  } catch (error: any) {
    console.error('Error replying:', error.message);
    throw error;
  }
}

export async function quote(
  agent: BskyAgent, 
  text: string, 
  embedUri: string
): Promise<void> {
  try {
    const embedPostResponse = await agent.getPostThread({ uri: embedUri });
    const embedPost = embedPostResponse.data.thread.post;
    if (!('cid' in embedPost)) {
      throw new Error('Could not retrieve quote post CID');
    }

    await agent.post({
      text,
      embed: {
        $type: 'app.bsky.embed.record',
        record: {
          uri: embedUri,
          cid: embedPost.cid as string
        }
      },
      createdAt: new Date().toISOString()
    });
    console.log('✅ Quote post created successfully!');
  } catch (error: any) {
    console.error('Error creating quote:', error.message);
    throw error;
  }
}

export async function thread(
  agent: BskyAgent, 
  posts: string[]
): Promise<void> {
  try {
    let rootUri = '';
    let rootCid = '';

    for (let i = 0; i < posts.length; i++) {
      const postRecord = {
        text: posts[i],
        createdAt: new Date().toISOString()
      };

      if (i === 0) {
        // First post - just post it
        const result = await agent.post(postRecord);
        rootUri = result.uri;
        rootCid = result.cid;
      } else {
        // Subsequent posts - reply to root
        await agent.post({
          ...postRecord,
          reply: {
            parent: { uri: rootUri, cid: rootCid },
            root: { uri: rootUri, cid: rootCid }
          }
        });
      }
    }
    console.log(`✅ Thread of ${posts.length} posts created!`);
  } catch (error: any) {
    console.error('Error creating thread:', error.message);
    throw error;
  }
}

export async function like(agent: BskyAgent, uri: string, cid: string): Promise<void> {
  try {
    await agent.like(uri, cid);
    console.log('✅ Liked!');
  } catch (error: any) {
    console.error('Error liking:', error.message);
    throw error;
  }
}

export async function repost(agent: BskyAgent, uri: string, cid: string): Promise<void> {
  try {
    await agent.repost(uri, cid);
    console.log('✅ Reposted!');
  } catch (error: any) {
    console.error('Error reposting:', error.message);
    throw error;
  }
}

export async function deletePost(agent: BskyAgent, uri: string): Promise<void> {
  try {
    await agent.deletePost(uri);
    console.log('✅ Post deleted!');
  } catch (error: any) {
    console.error('Error deleting post:', error.message);
    throw error;
  }
}