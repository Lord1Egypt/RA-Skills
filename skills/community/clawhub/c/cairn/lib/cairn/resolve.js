import { homedir } from 'node:os';
import { join } from 'node:path';
import { KNOWN_MODELS } from './constants/models.constants.js';
import { isOffline } from './offline.js';
// Resolve `id` to a local GGUF path, downloading on first use.
// Accepts:
//   - a known id from the registry (e.g. 'nomic-embed-text')
//   - a hf: URI (e.g. 'hf:user/repo/file.gguf')
//   - an absolute filesystem path to a .gguf file
export const resolveModel = async (id, cacheDir) => {
    const dir = cacheDir ?? join(homedir(), '.cairn', 'models');
    // Absolute path: trust the caller, no download. Allowed under CAIRN_OFFLINE.
    if (id.startsWith('/') || /^[A-Za-z]:[\\/]/.test(id)) {
        return { path: id, id, bytes: 0 };
    }
    const known = KNOWN_MODELS[id];
    const uri = known?.uri ?? id;
    if (!uri.startsWith('hf:') && !uri.startsWith('http')) {
        throw new Error(`cairn: unknown model id "${id}". Pass a registry key, a hf: URI, or an absolute .gguf path.`);
    }
    // Under CAIRN_OFFLINE we refuse non-local resolution outright. node-llama-cpp's
    // resolveModelFile would skip the download for cache hits, but it doesn't
    // expose a "cached only" probe — and we want fail-fast, not a network attempt
    // that succeeds-because-cached. For pre-cached models pass `modelPath` directly.
    if (isOffline()) {
        throw new Error(`cairn: model resolution blocked by CAIRN_OFFLINE for "${id}". ` +
            `Pass an absolute modelPath to a pre-cached GGUF, or unset CAIRN_OFFLINE.`);
    }
    // Lazy import so users on the ollama runtime never load llama.cpp bindings.
    const { resolveModelFile } = await import('node-llama-cpp');
    const path = await resolveModelFile(uri, { directory: dir });
    return { path, id, bytes: known?.bytes ?? 0 };
};
