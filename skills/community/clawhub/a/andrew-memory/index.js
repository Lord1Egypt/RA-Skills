/**
 * Andrew Memory Layer V2 - OpenClaw Plugin
 * 
 * Uses createRequire with absolute path to load OpenClaw SDK.
 */

import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(__dirname);

// Load SDK entry point via absolute path
// The exports map redirects "openclaw/plugin-sdk/plugin-entry" to dist/plugin-sdk/plugin-entry.js
const { definePluginEntry } = require('/usr/lib/node_modules/openclaw/dist/plugin-sdk/plugin-entry.js');

// Lazy-load the memory client
let memoryClient = null;

async function getMemoryClient(pluginConfig = {}) {
    if (!memoryClient) {
        const MemoryClient = await import('./src/MemoryClient.js');
        memoryClient = MemoryClient.getInstance({
            dataDir: pluginConfig.dataDir,
            llmMode: pluginConfig.llmMode || 'api',
            localLlmUrl: pluginConfig.localLlmUrl || 'http://localhost:11434'
        });
        await memoryClient.init();
    }
    return memoryClient;
}

export default definePluginEntry({
    id: "andrew-memory",
    name: "Andrew Memory Layer V2",
    description: "Product-grade memory layer for Andrew using LanceDB - semantic search, Core Identity injection, and conversation distillation",

    configSchema: {
        type: "object",
        additionalProperties: false,
        properties: {
            dataDir: { type: "string" },
            llmMode: { type: "string", enum: ["api", "local"] },
            localLlmUrl: { type: "string" }
        }
    },

    register(api) {
        // ============================================================
        // andrew_memory_add
        // ============================================================
        api.registerTool({
            name: "andrew_memory_add",
            description: "Add a new memory to Andrew's memory layer. Use this when Andrew learns something new that should be remembered long-term.",
            parameters: {
                type: "object",
                properties: {
                    text: { type: "string", description: "The memory content to store" },
                    memoryType: { type: "string", description: "Type: preference | fact | rule | experience | thought | distilled | general", default: "general" },
                    category: { type: "string", default: "general" },
                    importance: { type: "number", default: 3, minimum: 1, maximum: 5 },
                    confidence: { type: "number", default: 0.5, minimum: 0, maximum: 1 },
                    sourceFile: { type: "string", default: "manual" }
                },
                required: ["text"]
            },
            async execute(_id, params) {
                try {
                    const client = await getMemoryClient(api.pluginConfig);
                    const id = await client.add({
                        text: params.text,
                        memoryType: params.memoryType || 'general',
                        category: params.category || 'general',
                        importance: params.importance || 3,
                        confidence: params.confidence || 0.5,
                        sourceFile: params.sourceFile || 'manual'
                    });
                    return { content: [{ type: "text", text: `Memory added with ID: ${id}` }] };
                } catch (e) {
                    return { content: [{ type: "text", text: `Error adding memory: ${e.message}` }] };
                }
            }
        });

        // ============================================================
        // andrew_memory_search
        // ============================================================
        api.registerTool({
            name: "andrew_memory_search",
            description: "Search Andrew's memory layer for relevant memories. Use semantic search to find memories related to a query.",
            parameters: {
                type: "object",
                properties: {
                    query: { type: "string", description: "Search query" },
                    topK: { type: "number", default: 5, minimum: 1, maximum: 20 }
                },
                required: ["query"]
            },
            async execute(_id, params) {
                try {
                    const client = await getMemoryClient(api.pluginConfig);
                    const results = await client.search(params.query, { topK: params.topK || 5 });
                    if (results.length === 0) {
                        return { content: [{ type: "text", text: "No memories found." }] };
                    }
                    const formatted = results.map((r, i) =>
                        `${i + 1}. "${r.text}" (score: ${r.score?.toFixed(4)}, type: ${r.memoryType}, importance: ${r.importance})`
                    ).join('\n');
                    return { content: [{ type: "text", text: `Found ${results.length} memories:\n${formatted}` }] };
                } catch (e) {
                    return { content: [{ type: "text", text: `Error searching memory: ${e.message}` }] };
                }
            }
        });

        // ============================================================
        // andrew_memory_set_identity
        // ============================================================
        api.registerTool({
            name: "andrew_memory_set_identity",
            description: "Set Andrew's Core Identity - the foundational identity information that should always be present.",
            parameters: {
                type: "object",
                properties: {
                    content: { type: "string", description: "Identity content" },
                    fullData: { type: "object", description: "Additional structured identity data" }
                },
                required: ["content"]
            },
            async execute(_id, params) {
                try {
                    const client = await getMemoryClient(api.pluginConfig);
                    await client.setIdentity(params.content, params.fullData || {});
                    return { content: [{ type: "text", text: "Core Identity updated successfully." }] };
                } catch (e) {
                    return { content: [{ type: "text", text: `Error setting identity: ${e.message}` }] };
                }
            }
        });

        // ============================================================
        // andrew_memory_get_identity
        // ============================================================
        api.registerTool({
            name: "andrew_memory_get_identity",
            description: "Get Andrew's current Core Identity from the memory layer.",
            parameters: { type: "object", properties: {} },
            async execute(_id, _params) {
                try {
                    const client = await getMemoryClient(api.pluginConfig);
                    const identity = await client.getIdentity();
                    if (!identity) {
                        return { content: [{ type: "text", text: "No Core Identity set." }] };
                    }
                    return { content: [{ type: "text", text: `Core Identity:\n${identity.content}` }] };
                } catch (e) {
                    return { content: [{ type: "text", text: `Error getting identity: ${e.message}` }] };
                }
            }
        });

        // ============================================================
        // andrew_memory_distill
        // ============================================================
        api.registerTool({
            name: "andrew_memory_distill",
            description: "Distill a conversation into memory atoms. Extract key facts and insights from a conversation.",
            parameters: {
                type: "object",
                properties: {
                    messages: { type: "array", items: { type: "object", properties: { role: { type: "string" }, content: { type: "string" } } }, description: "Conversation messages to distill" }
                },
                required: ["messages"]
            },
            async execute(_id, params) {
                try {
                    const client = await getMemoryClient(api.pluginConfig);
                    const saved = await client.distill(params.messages);
                    return { content: [{ type: "text", text: `Distilled ${saved.length} memories:\n${saved.join('\n')}` }] };
                } catch (e) {
                    return { content: [{ type: "text", text: `Error distilling conversation: ${e.message}` }] };
                }
            }
        });

        // ============================================================
        // andrew_memory_regenerate_vectors
        // ============================================================
        api.registerTool({
            name: "andrew_memory_regenerate_vectors",
            description: "Regenerate all memory vectors from original text. Use after changing embedding model.",
            parameters: { type: "object", properties: {} },
            async execute(_id, _params) {
                try {
                    const client = await getMemoryClient(api.pluginConfig);
                    const result = await client.regenerateAllVectors();
                    return { content: [{ type: "text", text: `Regenerated ${result.count} vectors in ${result.duration}ms` }] };
                } catch (e) {
                    return { content: [{ type: "text", text: `Error regenerating vectors: ${e.message}` }] };
                }
            }
        });

        api.logger.info('[Andrew Memory V2] Plugin tools registered');
    }
});
