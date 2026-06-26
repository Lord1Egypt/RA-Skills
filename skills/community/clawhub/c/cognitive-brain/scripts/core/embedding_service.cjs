#!/usr/bin/env node
/**
 * Cognitive Brain - Embedding Service Client
 * 管理常驻 Embedding 服务进程，避免重复加载模型
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('embedding_service');
const { spawn } = require('child_process');
const path = require('path');
const EventEmitter = require('events');

const EMBED_SCRIPT = path.join(__dirname, '..', 'embed.py');

class EmbeddingService extends EventEmitter {
  constructor() {
    super();
    this.process = null;
    this.ready = false;
    this.pendingRequests = new Map();
    this.requestId = 0;
    this.buffer = '';
  }

  /**
   * 启动服务
   */
  start() {
    if (this.process) {
      return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
      console.log('[EmbeddingService] 启动服务...');

      this.process = spawn('python3', [EMBED_SCRIPT, '--serve'], {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      // 超时处理
      const timeoutTimer = setTimeout(() => {
        if (!this.ready) {
          reject(new Error('服务启动超时'));
        }
      }, 60000);

      // 处理 stdout
      this.process.stdout.on('data', (data) => {
        this.buffer += data.toString();
        this._processBuffer();
      });

      // 处理 stderr（就绪信号）
      this.process.stderr.on('data', (data) => {
        const msg = data.toString();
        if (msg.includes('"status": "ready"')) {
          clearTimeout(timeoutTimer);
          this.ready = true;
          console.log('[EmbeddingService] ✅ 服务已就绪');
          resolve();
        }
      });

      // 错误处理
      this.process.on('error', (err) => {
        clearTimeout(timeoutTimer);
        console.error('[EmbeddingService] 服务错误:', err);
        this.emit('error', err);
        reject(err);
      });

      this.process.on('exit', (code) => {
        clearTimeout(timeoutTimer);
        console.log(`[EmbeddingService] 服务退出 (code ${code})`);
        this.ready = false;
        this.process = null;
        this.emit('exit', code);
      });
    });
  }

  /**
   * 处理输出缓冲区
   */
  _processBuffer() {
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop(); // 保留未完成的行

    for (const line of lines) {
      if (!line.trim()) continue;
      
      try {
        const response = JSON.parse(line);
        if (response.request_id && this.pendingRequests.has(response.request_id)) {
          const { resolve, reject, timer } = this.pendingRequests.get(response.request_id);
          this.pendingRequests.delete(response.request_id);
          
          // 清除超时定时器
          if (timer) clearTimeout(timer);
          
          if (response.error) {
            reject(new Error(response.error));
          } else {
            resolve(response.embedding);
          }
        }
      } catch (e) { console.error("[embedding] 错误:", e.message);
        // 忽略非 JSON 输出
      }
    }
  }

  /**
   * 获取 Embedding
   * @param {boolean} waitForReady - 是否等待服务就绪（默认true，设为false可避免阻塞）
   */
  async embed(text, waitForReady = true) {
    if (!this.ready) {
      if (!waitForReady) {
        // 不等待，立即返回 null，同时异步启动服务
        this.start().catch(err => console.error('[EmbeddingService] 启动失败:', err.message));
        return null;
      }
      await this.start();
    }

    return new Promise((resolve, reject) => {
      const id = ++this.requestId;
      
      // 超时处理
      const timeoutTimer = setTimeout(() => {
        if (this.pendingRequests.has(id)) {
          this.pendingRequests.delete(id);
          reject(new Error('请求超时'));
        }
      }, 60000);  // 增加到 60 秒

      this.pendingRequests.set(id, { resolve, reject, timer: timeoutTimer });

      // 发送请求
      const request = JSON.stringify({ 
        request_id: id,
        text 
      }) + '\n';
      
      this.process.stdin.write(request);
    });
  }

  /**
   * 停止服务
   */
  stop() {
    if (this.process) {
      this.process.kill();
      this.process = null;
      this.ready = false;
    }
  }

  /**
   * 检查是否就绪
   */
  isReady() {
    return this.ready;
  }
}

// 单例模式
let serviceInstance = null;

function getEmbeddingService() {
  if (!serviceInstance) {
    serviceInstance = new EmbeddingService();
  }
  return serviceInstance;
}

module.exports = {
  EmbeddingService,
  getEmbeddingService
};