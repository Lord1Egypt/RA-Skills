/**
 * Andrew Memory Layer V2 - LanceDB Memory Client (ESM)
 * 
 * Pure ESM implementation for Node.js 22+
 * LanceDB for local vector storage
 * MiniMax API (or Ollama) for embeddings + distillation
 */

import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

// Lazy load LanceDB
let lancedb = null;

async function loadLanceDB() {
    if (!lancedb) {
        lancedb = (await import('@lancedb/lancedb')).default;
    }
    return lancedb;
}

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_DATA_DIR = path.join(os.homedir(), '.andrew-memory', 'data');
const VECTOR_DIM = 1536; // MiniMax embo-01

class AndrewMemoryClient {
    constructor(options = {}) {
        this.dataDir = options.dataDir || DEFAULT_DATA_DIR;
        this.llmMode = options.llmMode || 'api'; // 'local' or 'api'
        this.embeddingModel = options.embeddingModel || 'MiniMax';
        this.apiKey = process.env.MINIMAX_API_KEY || '';
        this.localLlmUrl = options.localLlmUrl || 'http://localhost:11434';
        this.vectorDim = options.vectorDim || VECTOR_DIM;

        this.db = null;
        this.memoryTable = null;
        this.identityTable = null;
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;

        const LanceDB = await loadLanceDB();

        // Create data directory
        if (!fs.existsSync(this.dataDir)) {
            fs.mkdirSync(this.dataDir, { recursive: true });
        }

        this.db = await LanceDB.connect(this.dataDir);
        this.initialized = true;
    }

    async generateEmbedding(text) {
        if (this.llmMode === 'local') {
            try {
                const response = await fetch(`${this.localLlmUrl}/api/embeddings`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: 'nomic-embed-text',
                        prompt: text
                    })
                });
                const data = await response.json();
                return data.embedding;
            } catch (e) {
                console.error('[Embedding] Ollama error:', e.message);
            }
        }

        // API mode: MiniMax
        try {
            const response = await fetch('https://api.minimaxi.com/v1/embeddings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify({
                    model: 'embo-01',
                    texts: [text],
                    type: 'query'
                })
            });
            const data = await response.json();
            if (data.vectors && data.vectors[0]) {
                return data.vectors[0];
            }
        } catch (e) {
            console.error('[Embedding] MiniMax API error:', e.message);
        }

        return this._dummyEmbedding();
    }

    _dummyEmbedding() {
        return new Array(this.vectorDim).fill(0);
    }

    async add(options = {}) {
        await this.init();

        const {
            text,
            memoryType = 'general',
            category = 'general',
            importance = 3,
            confidence = 0.5,
            executable = false,
            reuseCount = 0,
            sourceFile = 'manual',
            fullData = {}
        } = options;

        const id = `mem_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
        const timestamp = new Date().toISOString();
        const vector = await this.generateEmbedding(text);

        const row = {
            id,
            text,
            vector,
            memoryType,
            category,
            importance,
            confidence,
            executable,
            reuseCount,
            sourceFile,
            fullData: JSON.stringify(fullData),
            timestamp
        };

        try {
            this.memoryTable = await this.db.openTable('memory');
        } catch (e) {
            const LanceDB = await loadLanceDB();
            const { makeArrowTable } = LanceDB;
            const placeholderRow = {
                id: 'placeholder',
                text: 'placeholder',
                vector: this._dummyEmbedding(),
                memoryType: 'general',
                category: 'general',
                importance: 0,
                confidence: 0,
                executable: false,
                reuseCount: 0,
                sourceFile: 'system',
                fullData: '{}',
                timestamp: new Date().toISOString()
            };
            const table = makeArrowTable([placeholderRow]);
            await this.db.createTable('memory', table);
            this.memoryTable = await this.db.openTable('memory');
            await this.memoryTable.delete('id = "placeholder"');
        }

        await this.memoryTable.add([row]);
        console.log(`[Andrew Memory] Added: ${text.substring(0, 60)}...`);

        return id;
    }

    async search(query, options = {}) {
        await this.init();

        const topK = options.topK || 5;
        const vector = await this.generateEmbedding(query);

        this.memoryTable = await this.db.openTable('memory');

        let results;
        try {
            results = await this.memoryTable
                .vectorSearch(vector, { column: 'vector', k: topK })
                .toArray();
        } catch (e) {
            console.warn('[Search] Vector search failed, using fallback:', e.message);
            const all = await this.memoryTable.query().limit(topK).toArray();
            return all.map(row => ({
                id: row.id,
                text: row.text,
                memoryType: row.memoryType,
                category: row.category,
                importance: row.importance,
                confidence: row.confidence,
                executable: row.executable,
                reuseCount: row.reuseCount,
                sourceFile: row.sourceFile,
                fullData: JSON.parse(row.fullData || '{}'),
                timestamp: row.timestamp,
                score: 0
            }));
        }

        return results.map(row => ({
            id: row.id,
            text: row.text,
            memoryType: row.memoryType,
            category: row.category,
            importance: row.importance,
            confidence: row.confidence,
            executable: row.executable,
            reuseCount: row.reuseCount,
            sourceFile: row.sourceFile,
            fullData: JSON.parse(row.fullData || '{}'),
            timestamp: row.timestamp,
            score: row._distance || 0
        }));
    }

    async setIdentity(content, fullData = {}) {
        await this.init();

        const id = 'core_identity';
        const timestamp = new Date().toISOString();

        try {
            this.identityTable = await this.db.openTable('identity');
        } catch (e) {
            const LanceDB = await loadLanceDB();
            const { makeArrowTable } = LanceDB;
            const placeholder = [{
                id: 'core_identity_ph',
                content: '',
                fullData: '{}',
                timestamp: new Date().toISOString()
            }];
            const table = makeArrowTable(placeholder);
            await this.db.createTable('identity', table);
            this.identityTable = await this.db.openTable('identity');
            await this.identityTable.delete('id = "core_identity_ph"');
        }

        await this.identityTable.add([{ id, content, fullData: JSON.stringify(fullData), timestamp }]);
        console.log('[Andrew Memory] Core Identity updated');
    }

    async getIdentity() {
        await this.init();

        try {
            this.identityTable = await this.db.openTable('identity');
            const results = await this.identityTable
                .query()
                .where('id = "core_identity"')
                .limit(1)
                .execute();

            if (results.length > 0) {
                return {
                    content: results[0].content,
                    fullData: JSON.parse(results[0].fullData || '{}')
                };
            }
        } catch (e) {
            console.error('[Memory] GetIdentity error:', e.message);
        }

        return null;
    }

    async distill(messages, options = {}) {
        const conversation = messages.map(m => `${m.role}: ${m.content}`).join('\n');

        const prompt = `请将以下对话总结为1-3条独立的记忆原子。
格式：每条记忆包含内容
只输出记忆内容，不要解释。

对话：
${conversation}

记忆：`;

        const response = await this._callLLM(prompt);
        const lines = response.split('\n').filter(l => l.trim());
        const saved = [];

        for (const line of lines.slice(0, 3)) {
            const cleaned = line.replace(/^[-\d.]\s*/, '').trim();
            if (cleaned) {
                await this.add({
                    text: cleaned,
                    memoryType: 'distilled',
                    importance: 3,
                    confidence: 0.5,
                    sourceFile: 'distill',
                    fullData: { source: 'distill' }
                });
                saved.push(cleaned);
            }
        }

        return saved;
    }

    async _callLLM(prompt) {
        if (this.llmMode === 'local') {
            try {
                const response = await fetch(`${this.localLlmUrl}/api/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model: 'qwen2.5:7b', prompt, stream: false })
                });
                const data = await response.json();
                return data.response || '';
            } catch (e) {
                console.error('[LLM] Ollama error:', e.message);
            }
        }

        try {
            const response = await fetch('https://api.minimaxi.com/anthropic/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.apiKey,
                    'anthropic-version': '2023-06-01'
                },
                body: JSON.stringify({
                    model: 'MiniMax-M2.7',
                    messages: [{ role: 'user', content: prompt }],
                    max_tokens: 500
                })
            });
            const data = await response.json();
            if (data.content) {
                for (const block of data.content) {
                    if (block.type === 'text') return block.text;
                }
            }
        } catch (e) {
            console.error('[LLM] MiniMax API error:', e.message);
        }

        return '';
    }

    async regenerateAllVectors() {
        await this.init();

        this.memoryTable = await this.db.openTable('memory');
        const all = await this.memoryTable.query().execute();

        const start = Date.now();
        let count = 0;

        for (const row of all) {
            if (row.id === 'placeholder') continue;
            const newVector = await this.generateEmbedding(row.text);
            await this.memoryTable.update([{ where: `id = "${row.id}"`, values: { vector: newVector } }]);
            count++;
        }

        return { count, duration: Date.now() - start };
    }

    async close() {
        if (this.db) {
            await this.db.close();
            this.initialized = false;
        }
    }
}

// Singleton
let instance = null;

export function getInstance(options) {
    if (!instance) {
        instance = new AndrewMemoryClient(options);
    }
    return instance;
}

export { AndrewMemoryClient };

export default {
    getInstance,
    init: () => getInstance().init(),
    add: (options) => getInstance().add(options),
    search: (query, options) => getInstance().search(query, options),
    setIdentity: (content, fullData) => getInstance().setIdentity(content, fullData),
    getIdentity: () => getInstance().getIdentity(),
    distill: (messages) => getInstance().distill(messages),
    close: () => getInstance().close()
};
