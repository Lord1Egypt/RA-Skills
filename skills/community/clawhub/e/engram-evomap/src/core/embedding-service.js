// src/core/embedding-service.js
const { Worker } = require('worker_threads');
const path = require('path');

/**
 * 嵌入服务管理器 (Manager)
 * 采用异步队列与后台线程 (Worker Threads)
 * 彻底解决模型下载/推理导致的主线程阻塞
 */
class EmbeddingService {
    constructor() {
        this.worker = null;
        this.ready = false;
        this.pendingTasks = new Map();
        this.taskIdCounter = 0;
        this.modelId = 'Xenova/all-MiniLM-L6-v2';
    }

    /**
     * 异步启动服务
     * 监听状态、进度及结果
     */
    async init() {
        if (this.ready) return;

        return new Promise((resolve, reject) => {
            const workerPath = path.resolve(__dirname, 'embedding-worker.js');
            this.worker = new Worker(workerPath, {
                workerData: { modelId: this.modelId }
            });

            this.worker.on('message', (msg) => {
                switch (msg.type) {
                    case 'status':
                        console.log(`[EvoMap-Embedding] ${msg.message}`);
                        break;
                    case 'progress':
                        // 实现“旁路初始化”进度展示
                        const percent = ((msg.loaded / msg.total) * 100).toFixed(1);
                        console.log(`[EvoMap-Embedding] Download Progress (${msg.file}): ${percent}%`);
                        break;
                    case 'ready':
                        this.ready = true;
                        console.log(`[EvoMap-Embedding] Ready to vectorize.`);
                        resolve();
                        break;
                    case 'result':
                        const task = this.pendingTasks.get(msg.id);
                        if (task) {
                            task.resolve(msg.vector);
                            this.pendingTasks.delete(msg.id);
                        }
                        break;
                    case 'error':
                        if (msg.id !== undefined) {
                            const pending = this.pendingTasks.get(msg.id);
                            if (pending) {
                                pending.reject(new Error(msg.message));
                                this.pendingTasks.delete(msg.id);
                            }
                        } else {
                            reject(new Error(msg.message));
                        }
                        break;
                }
            });

            this.worker.on('error', (err) => {
                console.error('[EvoMap-Embedding] Worker error:', err);
                reject(err);
            });

            this.worker.on('exit', (code) => {
                if (code !== 0) {
                    console.error(`[EvoMap-Embedding] Worker stopped with exit code ${code}`);
                }
            });
        });
    }

    /**
     * 核心接口：对文本进行向量化
     * @param {string} text - 待处理文本 (错误模式、意图等)
     * @returns {Promise<number[]>} 384维向量
     */
    async vectorize(text) {
        if (!this.ready) {
            console.warn('[EvoMap-Embedding] Service not ready, queuing task...');
            await this.init();
        }

        return new Promise((resolve, reject) => {
            const taskId = this.taskIdCounter++;
            this.pendingTasks.set(taskId, { resolve, reject });
            this.worker.postMessage({ type: 'vectorize', id: taskId, text });
        });
    }

    /**
     * 关闭工作线程
     */
    async terminate() {
        if (this.worker) {
            await this.worker.terminate();
            this.worker = null;
            this.ready = false;
        }
    }
}

module.exports = EmbeddingService;
