/**
 * Reference implementation: Gemma 4 ONNX WebGPU inference with Transformers.js.
 * Demonstrates local on-device execution for browser and edge environments.
 * 
 * SECURITY & AUDIT COMPLIANCE:
 * - Immutable Revision: Pins model repository to an explicit commit revision.
 * - Offline Support: Accepts a local directory path to run without network egress.
 */

import { pipeline, TextStreamer } from '@huggingface/transformers';

const ONNX_MODEL_ID = 'onnx-community/gemma-4-E2B-it-ONNX';
const ONNX_MODEL_REVISION = '8e27c81d3f25b3992b4931a7884d41a7d6e5d614';

export async function createGemmaPipeline(options = {}) {
    const targetModel = options.localPath || process.env.GEMMA_MODEL_PATH || ONNX_MODEL_ID;
    const isLocal = Boolean(options.localPath || process.env.GEMMA_MODEL_PATH);

    console.log(`[gemma4-dev] Initializing on-device model: ${targetModel}`);
    const generator = await pipeline('text-generation', targetModel, {
        device: options.device || 'webgpu',
        dtype: options.dtype || 'q4',
        revision: isLocal ? undefined : (options.revision || ONNX_MODEL_REVISION),
        progress_callback: options.onProgress,
    });
    return generator;
}

export async function* streamGemmaResponse(generator, userPrompt, maxTokens = 512) {
    const messages = [
        { role: 'user', content: userPrompt }
    ];

    const prompt = generator.tokenizer.apply_chat_template(messages, {
        tokenize: false,
        add_generation_prompt: true,
    });

    const streamer = new TextStreamer(generator.tokenizer, {
        skip_prompt: true,
        skip_special_tokens: true,
    });

    return await generator(prompt, {
        max_new_tokens: maxTokens,
        streamer: streamer,
    });
}
