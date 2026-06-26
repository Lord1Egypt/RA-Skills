"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIProductSpaceClient = void 0;
const fs_1 = require("fs");
const path_1 = require("path");
class AIProductSpaceClient {
    baseUrl;
    apiKey;
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiKey = apiKey;
    }
    get headers() {
        return {
            Authorization: `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
        };
    }
    async request(path, init) {
        const url = `${this.baseUrl}${path}`;
        const res = await fetch(url, {
            ...init,
            headers: {
                ...this.headers,
                ...init?.headers,
            },
        });
        const data = (await res.json());
        if (!res.ok) {
            const msg = data?.message || `HTTP ${res.status}`;
            throw new Error(`API error: ${msg}`);
        }
        return data;
    }
    // ── Space Management ──
    async createSpace(name) {
        const data = await this.request('/api/spaces', { method: 'POST', body: JSON.stringify({ name: name || '未命名空间' }) });
        return data.space;
    }
    async getSpace(spaceId) {
        const data = await this.request(`/api/space/${spaceId}`);
        return data.space;
    }
    // ── Upload ──
    mimeFromExt(ext) {
        switch (ext.toLowerCase()) {
            case '.jpg':
            case '.jpeg': return 'image/jpeg';
            case '.png': return 'image/png';
            case '.webp': return 'image/webp';
            default: return 'application/octet-stream';
        }
    }
    mimeFromContentType(contentType, fallbackExt) {
        if (contentType) {
            const base = contentType.split(';')[0].trim();
            if (['image/jpeg', 'image/png', 'image/webp'].includes(base))
                return base;
        }
        return fallbackExt ? this.mimeFromExt(fallbackExt) : 'image/jpeg';
    }
    buildMultipart(fileBuffer, fileName, mimeType) {
        const boundary = `----FormBoundary${Date.now()}`;
        const header = Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName}"\r\nContent-Type: ${mimeType}\r\n\r\n`);
        const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
        return { body: new Uint8Array(Buffer.concat([header, fileBuffer, footer])), boundary };
    }
    async uploadImage(spaceId, imagePath) {
        const fileBuffer = (0, fs_1.readFileSync)(imagePath);
        const fileName = (0, path_1.basename)(imagePath);
        const mimeType = this.mimeFromExt((0, path_1.extname)(imagePath));
        const { body, boundary } = this.buildMultipart(fileBuffer, fileName, mimeType);
        return this.request(`/api/space/${spaceId}/upload`, {
            method: 'POST',
            body,
            headers: {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
            },
        });
    }
    async uploadImageFromUrl(spaceId, imageUrl) {
        const response = await fetch(imageUrl);
        const arrayBuffer = await response.arrayBuffer();
        const fileBuffer = Buffer.from(arrayBuffer);
        const urlExt = (0, path_1.extname)(new URL(imageUrl).pathname);
        const mimeType = this.mimeFromContentType(response.headers.get('content-type'), urlExt);
        const ext = mimeType === 'image/png' ? '.png' : mimeType === 'image/webp' ? '.webp' : '.jpg';
        const fileName = `product${ext}`;
        const { body, boundary } = this.buildMultipart(fileBuffer, fileName, mimeType);
        return this.request(`/api/space/${spaceId}/upload`, {
            method: 'POST',
            body,
            headers: {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
            },
        });
    }
    // ── Pipeline ──
    async runPipeline(spaceId, language) {
        return this.request(`/api/space/${spaceId}/generate-pipeline`, {
            method: 'POST',
            body: JSON.stringify({ language: language || 'zh' }),
        });
    }
    async pollPipeline(spaceId) {
        return this.request(`/api/space/${spaceId}/generate-pipeline`);
    }
    /**
     * Poll pipeline until complete or failed, with configurable intervals.
     * Returns final pipeline status.
     */
    async waitForPipeline(spaceId, opts) {
        const interval = opts?.intervalMs ?? 10_000;
        const maxAttempts = opts?.maxAttempts ?? 120;
        let attempts = 0;
        while (attempts < maxAttempts) {
            const status = await this.pollPipeline(spaceId);
            if (status.status === 'completed' || status.status === 'failed') {
                return status;
            }
            await new Promise((r) => setTimeout(r, interval));
            attempts++;
        }
        throw new Error('Pipeline timed out');
    }
    // ── Single Image Generation ──
    async generateImage(spaceId, prompt, options) {
        await this.request(`/api/space/${spaceId}`, {
            method: 'PATCH',
            body: JSON.stringify({
                inputPrompt: prompt,
                ...(options ? { options } : {}),
            }),
        });
        return this.request(`/api/space/${spaceId}/generate`, {
            method: 'POST',
        });
    }
    // ── Video Generation ──
    async submitVideo(spaceId, imageUrls, prompt) {
        return this.request(`/api/space/${spaceId}/generate-video`, {
            method: 'POST',
            body: JSON.stringify({ imageUrls, prompt }),
        });
    }
    async pollVideo(spaceId, videoId) {
        return this.request(`/api/space/${spaceId}/generate-video?videoId=${encodeURIComponent(videoId)}`);
    }
    async waitForVideo(spaceId, videoId, opts) {
        const interval = opts?.intervalMs ?? 15_000;
        const maxAttempts = opts?.maxAttempts ?? 60;
        let attempts = 0;
        while (attempts < maxAttempts) {
            const status = await this.pollVideo(spaceId, videoId);
            if (status.status === 'completed' || status.status === 'failed') {
                return status;
            }
            await new Promise((r) => setTimeout(r, interval));
            attempts++;
        }
        throw new Error('Video generation timed out');
    }
    // ── Assets ──
    async listAssets(folderId) {
        const qs = folderId ? `?folderId=${encodeURIComponent(folderId)}` : '';
        return this.request(`/api/assets${qs}`);
    }
}
exports.AIProductSpaceClient = AIProductSpaceClient;
