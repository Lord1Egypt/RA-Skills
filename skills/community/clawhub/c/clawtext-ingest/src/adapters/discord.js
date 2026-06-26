/**
 * Discord Adapter for ClawText-Ingest
 * Fetches messages from Discord channels, threads, and forums
 * Integrates with ClawText deduplication framework
 *
 * Phase 1: Core forum/channel/thread fetching
 */

import { Client, ChannelType } from 'discord.js';
import fs from 'fs';
import path from 'path';

class DiscordAdapter {
  constructor(options = {}) {
    this.token = options.token || process.env.DISCORD_TOKEN;
    if (!this.token) {
      throw new Error('DISCORD_TOKEN required: set env var or pass token in options');
    }

    this.client = new Client({
      intents: ['Guilds', 'GuildMessages', 'DirectMessages', 'MessageContent'],
    });

    this.includeEmbeds = options.includeEmbeds ?? false;
    this.includeAttachments = options.includeAttachments ?? false;
    this.resolveUsers = options.resolveUsers ?? true;
    this.threadDepth = options.threadDepth ?? 'full'; // 'none', 'replies-only', 'full'
    this.concurrency = options.concurrency ?? 3;
    this.batchSize = options.batchSize ?? 50;
    this.progressCallback = options.progressCallback;
    this.autoBatchThreshold = options.autoBatchThreshold ?? 500; // Auto-switch to batch at 500+ posts

    this.isAuthenticated = false;
  }

  /**
   * Authenticate with Discord
   */
  async authenticate() {
    if (this.isAuthenticated) return;
    await this.client.login(this.token);
    this.isAuthenticated = true;
  }

  /**
   * Cleanup: logout from Discord
   */
  async disconnect() {
    if (this.isAuthenticated) {
      await this.client.destroy();
      this.isAuthenticated = false;
    }
  }

  /**
   * Get lightweight forum metadata without fetching messages
   * Returns: { id, name, topic, postCount, estimatedMessageCount, tags }
   */
  async describeForumStructure(forumId) {
    await this.authenticate();

    const channel = await this.client.channels.fetch(forumId);
    if (!channel) throw new Error(`Forum ${forumId} not found`);
    if (channel.type !== ChannelType.GuildForum) {
      throw new Error(`Channel ${forumId} is not a forum`);
    }

    // Fetch only thread list, no messages
    const threads = await channel.threads.fetchArchived({ limit: 100 });
    const activeThreads = channel.threads.cache;

    // Combine active + archived
    const allThreadPosts = [...activeThreads.values(), ...threads.threads.values()];

    // Extract tags from channel
    const availableTags = channel.availableTags || [];
    const tagNames = availableTags.map(t => t.name);

    // Estimate message count (rough: assume 10 messages per post)
    const estimatedMessageCount = allThreadPosts.reduce((sum, post) => {
      return sum + (post.messageCount || 1);
    }, 0);

    return {
      id: forumId,
      name: channel.name,
      topic: channel.topic || '',
      postCount: allThreadPosts.length,
      estimatedMessageCount,
      tags: tagNames,
      fetchedAt: new Date().toISOString(),
    };
  }

  /**
   * Fetch forum hierarchy: list all posts without fetching messages
   * Returns: [{ postId, title, authorId, postCount, tags, solved, createdAt }]
   */
  async fetchForumHierarchy(forumId) {
    await this.authenticate();

    const channel = await this.client.channels.fetch(forumId);
    if (!channel || channel.type !== ChannelType.GuildForum) {
      throw new Error(`Forum ${forumId} not found or not a forum`);
    }

    // Fetch active threads
    const activeThreads = channel.threads.cache.map(t => ({
      postId: t.id,
      postName: t.name,
      authorId: t.ownerId,
      messageCount: t.messageCount || 0,
      tags: t.appliedTags || [],
      createdAt: t.createdTimestamp,
      updatedAt: t.archiveTimestamp || Date.now(),
      archived: t.archived,
    }));

    // Fetch archived threads (up to 100, paginated)
    const archivedCollection = await channel.threads.fetchArchived({ limit: 100 });
    const archivedThreads = archivedCollection.threads.map(t => ({
      postId: t.id,
      postName: t.name,
      authorId: t.ownerId,
      messageCount: t.messageCount || 0,
      tags: t.appliedTags || [],
      createdAt: t.createdTimestamp,
      updatedAt: t.archiveTimestamp || Date.now(),
      archived: t.archived,
    }));

    const allPosts = [...activeThreads, ...archivedThreads];
    return allPosts.sort((a, b) => b.createdAt - a.createdAt);
  }

  /**
   * Fetch entire forum + all messages at once (for small forums)
   * Returns: { records: Message[], relationshipMap: { postId -> replyIds } }
   */
  async fetchForumCompletely(forumId, options = {}) {
    await this.authenticate();

    const channel = await this.client.channels.fetch(forumId);
    if (!channel || channel.type !== ChannelType.GuildForum) {
      throw new Error(`Forum ${forumId} not found or not a forum`);
    }

    const records = [];
    const relationshipMap = {};
    let processedPosts = 0;
    let totalPosts = 0;

    // Get all posts (active + archived)
    const activeThreads = Array.from(channel.threads.cache.values());
    const archivedCollection = await channel.threads.fetchArchived({ limit: 100 });
    const archivedThreads = Array.from(archivedCollection.threads.values());
    const allPosts = [...activeThreads, ...archivedThreads];
    totalPosts = allPosts.length;

    if (totalPosts >= this.autoBatchThreshold) {
      throw new Error(
        `Forum has ${totalPosts} posts (>= ${this.autoBatchThreshold}). Use fetchForumInBatches() for large forums.`
      );
    }

    // Fetch messages from each post
    for (const post of allPosts) {
      const { records: postMessages, relationshipMap: postRelMap } = 
        await this._fetchPostMessages(post, forumId, channel.name);
      
      records.push(...postMessages);
      Object.assign(relationshipMap, postRelMap);

      processedPosts++;
      if (this.progressCallback) {
        this.progressCallback({
          processed: processedPosts,
          total: totalPosts,
          currentPost: post.name,
          mode: 'full',
        });
      }
    }

    return {
      forumMetadata: {
        forumId,
        forumName: channel.name,
        forumTopic: channel.topic || '',
        totalPosts: allPosts.length,
        totalMessages: records.length,
        tags: channel.availableTags?.map(t => t.name) || [],
        fetchedAt: new Date().toISOString(),
      },
      records,
      relationshipMap,
    };
  }

  /**
   * Stream forum in batches (for large forums)
   * Generator yields: { batchNumber, records: [], relationshipMap: {} }
   */
  async *fetchForumInBatches(forumId, options = {}) {
    await this.authenticate();

    const channel = await this.client.channels.fetch(forumId);
    if (!channel || channel.type !== ChannelType.GuildForum) {
      throw new Error(`Forum ${forumId} not found or not a forum`);
    }

    // Get all posts (active + archived)
    const activeThreads = Array.from(channel.threads.cache.values());
    const archivedCollection = await channel.threads.fetchArchived({ limit: 100 });
    const archivedThreads = Array.from(archivedCollection.threads.values());
    const allPosts = [...activeThreads, ...archivedThreads];
    const totalPosts = allPosts.length;

    let batchNumber = 0;
    let processedPosts = 0;

    for (const post of allPosts) {
      const { records: postMessages, relationshipMap: postRelMap } = 
        await this._fetchPostMessages(post, forumId, channel.name);

      // Yield batch after reaching batchSize messages or last post
      if (
        postMessages.length >= (options.batchSize || this.batchSize) ||
        processedPosts === totalPosts - 1
      ) {
        batchNumber++;
        yield {
          batchNumber,
          records: postMessages,
          relationshipMap: postRelMap,
          forumId,
          forumName: channel.name,
        };
      }

      processedPosts++;
      if (this.progressCallback) {
        this.progressCallback({
          processed: processedPosts,
          total: totalPosts,
          currentPost: post.name,
          batchNumber,
          mode: 'batch',
        });
      }
    }
  }

  /**
   * Fetch single channel (non-forum)
   * Returns: { records: [], relationshipMap: {} }
   */
  async fetchChannel(channelId, options = {}) {
    await this.authenticate();

    const channel = await this.client.channels.fetch(channelId);
    if (!channel || channel.type !== ChannelType.GuildText) {
      throw new Error(`Channel ${channelId} not found or not a text channel`);
    }

    const messages = await channel.messages.fetch({ limit: options.limit || 100 });
    const records = messages
      .reverse()
      .map((msg, idx) => this._normalizeMessage(msg, channelId, channel.name, idx === 0));

    return {
      channelMetadata: {
        channelId,
        channelName: channel.name,
        totalMessages: records.length,
        fetchedAt: new Date().toISOString(),
      },
      records,
      relationshipMap: {}, // Channels don't have post structure
    };
  }

  /**
   * Fetch single thread
   * Returns: { records: [], relationshipMap: {} }
   */
  async fetchThread(threadId, options = {}) {
    await this.authenticate();

    const thread = await this.client.channels.fetch(threadId);
    if (!thread || thread.type !== ChannelType.PublicThread) {
      throw new Error(`Thread ${threadId} not found or not a thread`);
    }

    const messages = await thread.messages.fetch({ limit: options.limit || 100 });
    const recordArray = messages
      .reverse()
      .map((msg, idx) => this._normalizeMessage(msg, threadId, thread.name, idx === 0));

    const relationshipMap = {
      [threadId]: {
        rootMessageId: recordArray[0]?.id,
        replyIds: recordArray.slice(1).map(r => r.id),
      },
    };

    return {
      threadMetadata: {
        threadId,
        threadName: thread.name,
        parentChannelId: thread.parentId,
        totalMessages: recordArray.length,
        fetchedAt: new Date().toISOString(),
      },
      records: recordArray,
      relationshipMap,
    };
  }

  /**
   * Internal: Fetch all messages from a single forum post
   */
  async _fetchPostMessages(post, forumId, forumName) {
    const messages = await post.messages.fetch({ limit: 100 });
    const recordArray = [];
    const messageIds = [];

    // First message is the post root
    let isFirst = true;
    for (const msg of messages.reverse()) {
      const normalized = this._normalizeMessage(msg, post.id, post.name, isFirst, {
        forumId,
        forumName,
        postId: post.id,
        postAuthor: post.ownerId,
        depth: isFirst ? 0 : 1,
      });
      recordArray.push(normalized);
      messageIds.push(msg.id);
      isFirst = false;
    }

    const relationshipMap = {
      [post.id]: {
        rootMessageId: recordArray[0]?.id,
        replyIds: recordArray.slice(1).map(r => r.id),
        postAuthor: post.ownerId,
        postTags: post.appliedTags || [],
        postName: post.name,
      },
    };

    return { records: recordArray, relationshipMap };
  }

  /**
   * Internal: Normalize Discord message to ClawText record format
   */
  _normalizeMessage(msg, channelOrThreadId, channelName, isRoot, forumContext = null) {
    const content = this._extractContent(msg);

    const record = {
      id: msg.id,
      source: 'discord',
      sourceType: forumContext ? 'forum_post_reply' : 'channel_message',
      content,
      author: this.resolveUsers ? msg.author.username : msg.author.id,
      authorId: msg.author.id,
      timestamp: msg.createdTimestamp,

      metadata: {
        reactionsCount: msg.reactions.cache.size,
        edited: !!msg.editedTimestamp,
        editedAt: msg.editedTimestamp,
        mentions: Array.from(msg.mentions.users?.values?.() || []).map(u => 
          this.resolveUsers ? u.username : u.id
        ),
        links: this._extractLinks(msg),
      },
    };

    // Add forum-specific hierarchy if present
    if (forumContext) {
      record.sourceType = isRoot ? 'forum_post_root' : 'forum_post_reply';
      record.forumHierarchy = {
        forumId: forumContext.forumId,
        forumName: forumContext.forumName,
        postId: forumContext.postId,
        postName: channelName,
        postAuthor: this.resolveUsers ? null : forumContext.postAuthor, // Resolved by post metadata
        depth: forumContext.depth,
        threadPath: `${forumContext.forumName} > ${channelName}`,
      };

      record.replyContext = {
        isReply: !isRoot,
        parentMessageId: isRoot ? null : null, // Could be set by indexing
        replyCount: isRoot ? 0 : 0, // Would need post metadata
      };
    } else {
      // Channel/thread context
      record.threadContext = {
        channelId: channelOrThreadId,
        channelName,
        isForumPost: false,
      };
    }

    // Add embeds/attachments if requested
    if (this.includeEmbeds && msg.embeds.length > 0) {
      record.embeds = msg.embeds.map(e => ({
        title: e.title,
        description: e.description,
        url: e.url,
      }));
    }

    if (this.includeAttachments && msg.attachments.size > 0) {
      record.attachments = Array.from(msg.attachments.values()).map(a => ({
        name: a.name,
        url: a.url,
        size: a.size,
        contentType: a.contentType,
      }));
    }

    return record;
  }

  /**
   * Extract message content, stripping embeds/attachments from text if not included
   */
  _extractContent(msg) {
    let content = msg.content || '';

    // Remove embed/attachment indicators from text if not including them
    if (!this.includeEmbeds) {
      // Discord embeds often have links; strip them
      content = content.replace(/<?(https?:\/\/[^\s>]+)\s*([A-Za-z0-9\-_.~:/?#\[\]@!$&'()*+,;=]*)?>?/g, '');
    }

    // Remove sticker references
    if (msg.stickers.size > 0) {
      content = content.replace(/\[sticker:.*?\]/g, '');
    }

    return content.trim();
  }

  /**
   * Extract URLs from message content and embeds
   */
  _extractLinks(msg) {
    const links = [];
    const urlRegex = /(https?:\/\/[^\s>]+)/g;

    // From content
    const contentMatches = msg.content?.match(urlRegex) || [];
    links.push(...contentMatches);

    // From embeds
    if (msg.embeds.length > 0) {
      msg.embeds.forEach(e => {
        if (e.url) links.push(e.url);
      });
    }

    return [...new Set(links)]; // Dedupe
  }
}

export default DiscordAdapter;
