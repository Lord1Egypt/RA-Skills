// Lazy singleton wrapper around node-llama-cpp's getLlama(). The native lib
// initializes Metal/CUDA/Vulkan once per process; loading it twice wastes VRAM
// and (on Metal) can fail. Both LlamaEmbedRuntime and LlamaChatRuntime go
// through here.
//
// Set CAIRN_CPU_ONLY=1 to force CPU-only inference. Useful when Cairn shares
// the box with another GPU-resident model and you want to dedicate VRAM there.
let llamaPromise = null;
export const getLlamaRuntime = async () => {
    if (!llamaPromise) {
        llamaPromise = (async () => {
            const { getLlama } = await import('node-llama-cpp');
            const cpuOnly = process.env.CAIRN_CPU_ONLY === '1' || process.env.CAIRN_CPU_ONLY === 'true';
            return getLlama(cpuOnly ? { gpu: false } : undefined);
        })();
    }
    return llamaPromise;
};
