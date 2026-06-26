// Known-model registry. Abstract ids map to Hugging Face GGUFs in the same
// quants the ollama defaults use, so the embedded runtime produces equivalent
// output to a user already running ollama with the matching tag.
//
// Adding a new model: append a key here and reference it from CairnOptions.
// Pinned mappings keep behavior reproducible across machines.
export const KNOWN_MODELS = {
    // 768-dim, ~80 MB. Matches ollama's `nomic-embed-text` tag in dim and quality.
    'nomic-embed-text': {
        uri: 'hf:nomic-ai/nomic-embed-text-v1.5-GGUF/nomic-embed-text-v1.5.Q8_0.gguf',
        bytes: 84_000_000,
    },
    // ~700 MB. Same quant as the ollama default (`UD-Q8_K_XL`).
    'qwen3-0.6b': {
        uri: 'hf:unsloth/Qwen3-0.6B-GGUF/Qwen3-0.6B-UD-Q8_K_XL.gguf',
        bytes: 700_000_000,
    },
};
