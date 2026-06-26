// convex/schema.ts
// Schema for memory storage in Convex

import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Hot storage: recent conversations and memories
  memories: defineTable({
    sessionId: v.string(),
    timestamp: v.number(),
    content: v.string(),
    source: v.string(), // 'conversation', 'note', 'extracted'
    tags: v.array(v.string()),
    importance: v.number(), // 1-10
    metadata: v.optional(v.object({
      agentId: v.optional(v.string()),
      channel: v.optional(v.string()),
      topic: v.optional(v.string()),
    })),
  })
    .index("by_session", ["sessionId"])
    .index("by_timestamp", ["timestamp"])
    .index("by_tags", ["tags"]),

  // Search index for full-text search
  searchIndex: defineTable({
    memoryId: v.id("memories"),
    words: v.array(v.string()),
    timestamp: v.number(),
  })
    .index("by_words", ["words"])
    .index("by_timestamp", ["timestamp"]),
});
