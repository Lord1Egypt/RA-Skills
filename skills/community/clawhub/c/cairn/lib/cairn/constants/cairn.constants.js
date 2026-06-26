// Sub-1GB Q8 default. Doc-extraction skips silently if the model isn't
// available, so this default doesn't break users who haven't downloaded
// (embedded runtime) or pulled (ollama runtime) it.
export const DEFAULT_CHAT_MODEL_OLLAMA = 'hf.co/unsloth/Qwen3-0.6B-GGUF:UD-Q8_K_XL';
export const DEFAULT_CHAT_MODEL_EMBEDDED = 'qwen3-0.6b';
export const DEFAULT_OLLAMA_URL = 'http://127.0.0.1:11434';
export const DEFAULT_EMBED_MODEL = 'nomic-embed-text';
