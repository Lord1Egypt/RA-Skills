import { homedir } from 'node:os';
import { join } from 'node:path';
import { DEFAULT_CHAT_MODEL_EMBEDDED, DEFAULT_CHAT_MODEL_OLLAMA, DEFAULT_EMBED_MODEL, DEFAULT_OLLAMA_URL, } from './constants/cairn.constants.js';
import { ChatProvider } from './providers/chat.provider.js';
import { DbProvider } from './providers/db.provider.js';
import { EmbedProvider } from './providers/embed.provider.js';
import { IngestProvider } from './providers/ingest.provider.js';
import { RetrieveProvider } from './providers/retrieve.provider.js';
import { LlamaChatRuntime } from './providers/runtimes/llama-chat.runtime.js';
import { LlamaEmbedRuntime } from './providers/runtimes/llama-embed.runtime.js';
import { OllamaChatRuntime } from './providers/runtimes/ollama-chat.runtime.js';
import { OllamaEmbedRuntime } from './providers/runtimes/ollama-embed.runtime.js';
export class Cairn {
    db;
    embed;
    chat;
    ingest;
    retrieve;
    runtime;
    constructor(opts) {
        const dbPath = opts?.dbPath ?? join(homedir(), '.cairn', 'index.sqlite');
        const runtime = opts?.runtime ?? 'ollama';
        const embedModel = opts?.embedModel ?? DEFAULT_EMBED_MODEL;
        this.runtime = runtime;
        this.db = new DbProvider(dbPath);
        let chatRuntime;
        let embedRuntime;
        if (runtime === 'embedded') {
            const cacheDir = opts?.modelCacheDir ?? join(homedir(), '.cairn', 'models');
            const chatModel = opts?.chatModel ?? DEFAULT_CHAT_MODEL_EMBEDDED;
            embedRuntime = new LlamaEmbedRuntime({ model: embedModel, cacheDir });
            chatRuntime = new LlamaChatRuntime({ model: chatModel, cacheDir });
        }
        else {
            const ollamaUrl = opts?.ollamaUrl ?? DEFAULT_OLLAMA_URL;
            const chatModel = opts?.chatModel ?? DEFAULT_CHAT_MODEL_OLLAMA;
            embedRuntime = new OllamaEmbedRuntime({ url: ollamaUrl, model: embedModel });
            chatRuntime = new OllamaChatRuntime({ url: ollamaUrl, model: chatModel });
        }
        this.embed = new EmbedProvider(embedRuntime);
        this.chat = new ChatProvider(chatRuntime);
        this.ingest = new IngestProvider(this.db, this.embed, this.chat);
        this.retrieve = new RetrieveProvider(this.db, this.embed);
        this.embed.healthCheck().then((up) => {
            if (!up) {
                if (runtime === 'embedded') {
                    console.warn(`cairn: embedded embed model failed to load — search works (FTS5), but embed-dependent ops (add, refresh) will fail. check ${opts?.modelCacheDir ?? join(homedir(), '.cairn', 'models')} or pass an explicit modelPath.`);
                }
                else {
                    console.warn(`cairn: ollama not reachable at ${opts?.ollamaUrl ?? DEFAULT_OLLAMA_URL} — search works (FTS5), but embed-dependent ops (add, refresh) will fail. run \`ollama serve\`.`);
                }
            }
        });
    }
    close() {
        this.db.close();
    }
}
