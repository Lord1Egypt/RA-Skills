// convex/memory.ts
// Functions for memory operations

import { v } from "convex/values";
import { query, mutation, internalMutation } from "./_generated/server";

// Save a memory to hot storage
export const saveMemory = mutation({
  args: {
    sessionId: v.string(),
    content: v.string(),
    source: v.string(),
    tags: v.array(v.string()),
    importance: v.number(),
    metadata: v.optional(v.object({
      agentId: v.optional(v.string()),
      channel: v.optional(v.string()),
      topic: v.optional(v.string()),
    })),
  },
  handler: async (ctx, args) => {
    const timestamp = Date.now();
    
    // Insert memory
    const memoryId = await ctx.db.insert("memories", {
      sessionId: args.sessionId,
      timestamp,
      content: args.content,
      source: args.source,
      tags: args.tags,
      importance: args.importance,
      metadata: args.metadata,
    });

    // Create search index
    const words = args.content
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/)
      .filter(w => w.length > 2);
    
    await ctx.db.insert("searchIndex", {
      memoryId,
      words: [...new Set(words)],
      timestamp,
    });

    return memoryId;
  },
});

// Search memories by text
export const searchMemories = query({
  args: {
    query: v.string(),
    limit: v.optional(v.number()),
    sessionId: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const limit = args.limit ?? 10;
    const searchWords = args.query
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/)
      .filter(w => w.length > 2);

    // Get recent memories (last 30 days)
    const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
    
    let memories;
    if (args.sessionId) {
      memories = await ctx.db
        .query("memories")
        .withIndex("by_session", q => q.eq("sessionId", args.sessionId))
        .filter(q => q.gte(q.field("timestamp"), thirtyDaysAgo))
        .order("desc")
        .take(limit * 2);
    } else {
      memories = await ctx.db
        .query("memories")
        .withIndex("by_timestamp", q => q.gte("timestamp", thirtyDaysAgo))
        .order("desc")
        .take(limit * 2);
    }

    // Score by relevance
    const scored = memories.map(m => {
      const contentWords = m.content.toLowerCase().split(/\s+/);
      const matches = searchWords.filter(w => contentWords.some(cw => cw.includes(w)));
      const tagMatches = m.tags.filter(t => searchWords.some(w => t.toLowerCase().includes(w)));
      const score = matches.length + tagMatches.length * 2 + (m.importance / 10);
      return { ...m, score };
    });

    return scored
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  },
});

// Get recent memories
export const getRecent = query({
  args: {
    limit: v.optional(v.number()),
    sessionId: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const limit = args.limit ?? 20;
    
    if (args.sessionId) {
      return await ctx.db
        .query("memories")
        .withIndex("by_session", q => q.eq("sessionId", args.sessionId))
        .order("desc")
        .take(limit);
    }
    
    return await ctx.db
      .query("memories")
      .withIndex("by_timestamp")
      .order("desc")
      .take(limit);
  },
});

// Cleanup old memories (move to cold storage)
export const cleanupOld = mutation({
  args: {
    olderThanDays: v.number(),
  },
  handler: async (ctx, args) => {
    const cutoff = Date.now() - args.olderThanDays * 24 * 60 * 60 * 1000;
    
    const old = await ctx.db
      .query("memories")
      .withIndex("by_timestamp", q => q.lt("timestamp", cutoff))
      .collect();

    for (const memory of old) {
      await ctx.db.delete(memory._id);
      // Also delete from search index
      const searchEntries = await ctx.db
        .query("searchIndex")
        .filter(q => q.eq(q.field("memoryId"), memory._id))
        .collect();
      for (const entry of searchEntries) {
        await ctx.db.delete(entry._id);
      }
    }

    return old.length;
  },
});

// Get stats
export const stats = query({
  args: {},
  handler: async (ctx) => {
    const memories = await ctx.db.query("memories").collect();
    const searchIndex = await ctx.db.query("searchIndex").collect();
    
    const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
    const recent = memories.filter(m => m.timestamp > thirtyDaysAgo);
    
    return {
      totalMemories: memories.length,
      totalSearchEntries: searchIndex.length,
      recentMemories: recent.length,
      avgImportance: memories.length > 0 
        ? memories.reduce((a, m) => a + m.importance, 0) / memories.length 
        : 0,
    };
  },
});
