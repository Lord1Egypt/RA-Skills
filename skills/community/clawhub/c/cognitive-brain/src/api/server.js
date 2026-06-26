/**
 * API 服务器
 * RESTful API for Cognitive Brain
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const fs = require('fs');
const path = require('path');
const { getBrain } = require('../index.js');
const { metrics } = require('../utils/metrics.cjs');
const { createLogger } = require('../utils/logger.cjs');
const { validateEncode, validateRecall, validateId } = require('../utils/validation.cjs');
const { WebSocketManager } = require('./websocket.js');
const { CONSTANTS } = require('../utils/constants.cjs');

// 加载配置
function loadConfig() {
  try {
    const configPath = path.join(process.cwd(), 'config.json');
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
  } catch (e) {
    console.warn('Warning: Could not load config.json');
  }
  return { api: { port: CONSTANTS.API.DEFAULT_PORT } };
}

// 简单的速率限制中间件
const rateLimitMap = new Map();
let rateLimitCleanupInterval = null;

function startRateLimitCleanup() {
  // 定期清理过期的 rate limit 条目（每5分钟）
  rateLimitCleanupInterval = setInterval(() => {
    const now = Date.now();
    for (const [key, data] of rateLimitMap) {
      if (now > data.resetTime + CONSTANTS.API.RATE_LIMIT_WINDOW_MS) {
        rateLimitMap.delete(key);
      }
    }
  }, 5 * 60 * 1000);
}

function rateLimitMiddleware(req, res, next) {
  const key = req.ip || 'unknown';
  const now = Date.now();

  if (!rateLimitMap.has(key)) {
    rateLimitMap.set(key, { count: 1, resetTime: now + CONSTANTS.API.RATE_LIMIT_WINDOW_MS });
    return next();
  }

  const data = rateLimitMap.get(key);

  if (now > data.resetTime) {
    // 重置窗口
    data.count = 1;
    data.resetTime = now + CONSTANTS.API.RATE_LIMIT_WINDOW_MS;
    return next();
  }

  if (data.count >= CONSTANTS.API.RATE_LIMIT_MAX_REQUESTS) {
    return res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil((data.resetTime - now) / 1000)
    });
  }

  data.count++;
  next();
}

const logger = createLogger('api');
const apiConfig = loadConfig().api || {};

class ApiServer {
  constructor(port = apiConfig.port || CONSTANTS.API.DEFAULT_PORT) {
    this.app = express();
    this.port = port;
    this.brain = null;
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    // 安全头
    this.app.use(helmet());
    
    // CORS
    this.app.use(cors({
      origin: process.env.CORS_ORIGIN || apiConfig.cors?.origin || '*',
      methods: apiConfig.cors?.methods || ['GET', 'POST', 'PUT', 'DELETE'],
      allowedHeaders: ['Content-Type', 'Authorization']
    }));
    
    // 请求体限制
    this.app.use(express.json({ limit: CONSTANTS.API.REQUEST_BODY_LIMIT }));
    this.app.use(express.urlencoded({ extended: true, limit: CONSTANTS.API.REQUEST_BODY_LIMIT }));

    // 速率限制
    this.app.use(rateLimitMiddleware);

    // 请求日志和指标收集
    this.app.use((req, res, next) => {
      logger.info(`${req.method} ${req.path}`, {
        ip: req.ip,
        userAgent: req.get('user-agent')
      });

      const timer = metrics.startTimer('http_request_duration', {
        method: req.method,
        path: req.path
      });

      res.on('finish', () => {
        timer.end();
        metrics.inc('http_requests_total', {
          method: req.method,
          path: req.path,
          status: res.statusCode
        });
      });

      next();
    });
  }

  setupRoutes() {
    // 健康检查
    this.app.get('/health', async (req, res) => {
      try {
        const stats = await this.brain.stats();
        res.json({
          status: 'ok',
          version: require('../../package.json').version,
          stats
        });
      } catch (e) {
        res.status(503).json({
          status: 'error',
          message: e.message
        });
      }
    });

    // 编码记忆
    this.app.post('/api/memories', validateEncode, async (req, res) => {
      try {
        const { content, metadata = {} } = req.body;
        
        if (!content) {
          return res.status(400).json({ error: 'content is required' });
        }
        
        const timer = metrics.startTimer('encode_duration');
        const memory = await this.brain.memory.encode(content, metadata);
        timer.end();
        
        metrics.inc('memories_encoded_total');
        res.status(201).json(memory);
      } catch (e) {
        metrics.inc('encode_errors_total');
        logger.error('编码记忆失败', { error: e.message, stack: e.stack });
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // 检索记忆
    this.app.get('/api/memories', validateRecall, async (req, res) => {
      try {
        const { q, limit = 10, type } = req.query;

        if (!q) {
          return res.status(400).json({ error: 'q (query) is required' });
        }

        const timer = metrics.startTimer('recall_duration');
        const memories = await this.brain.memory.recall(q, {
          limit: parseInt(limit),
          type
        });
        timer.end();

        metrics.inc('memories_recalled_total');
        res.json({
          query: q,
          count: memories.length,
          memories
        });
      } catch (e) {
        metrics.inc('recall_errors_total');
        logger.error('检索记忆失败', { error: e.message, stack: e.stack });
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // 获取记忆详情
    this.app.get('/api/memories/:id', validateId, async (req, res) => {
      try {
        const memory = await this.brain.memory.memoryRepo.findById(req.params.id);
        if (!memory) {
          return res.status(404).json({ error: 'Memory not found' });
        }
        res.json(memory);
      } catch (e) {
        logger.error('获取记忆详情失败', { error: e.message, id: req.params.id });
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // 获取统计
    this.app.get('/api/stats', async (req, res) => {
      try {
        const stats = await this.brain.stats();
        res.json(stats);
      } catch (e) {
        logger.error('获取统计失败', { error: e.message });
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // 获取概念
    this.app.get('/api/concepts', async (req, res) => {
      try {
        const { limit = 10 } = req.query;
        const concepts = await this.brain.concept.getTopConcepts(parseInt(limit));
        res.json(concepts);
      } catch (e) {
        logger.error('获取概念失败', { error: e.message });
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // 预测
    this.app.post('/api/predict', async (req, res) => {
      try {
        const { userId, messages = [] } = req.body;
        const result = await this.brain.memory.predictAndPreload(userId, messages);
        res.json(result);
      } catch (e) {
        logger.error('预测失败', { error: e.message, userId });
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // Metrics 端点 (Prometheus 格式)
    this.app.get('/metrics', (req, res) => {
      res.set('Content-Type', 'text/plain');
      res.send(metrics.toPrometheus());
    });

    // 404
    this.app.use((req, res) => {
      res.status(404).json({ error: 'Not found' });
    });

    // 错误处理
    this.app.use((err, req, res, next) => {
      logger.error('API Error', { error: err.message, stack: err.stack });
      res.status(500).json({ error: 'Internal server error' });
    });
  }

  async start() {
    this.brain = getBrain ? getBrain() : new (require('../index.js').CognitiveBrain)();

    // 启动 rate limit 清理定时器
    startRateLimitCleanup();

    return new Promise((resolve) => {
      this.server = this.app.listen(this.port, () => {
        console.log(`🚀 API Server running on http://localhost:${this.port}`);
        console.log(`   Health: http://localhost:${this.port}/health`);
        console.log(`   Metrics: http://localhost:${this.port}/metrics`);
        console.log(`   WebSocket: ws://localhost:${this.port}`);
        resolve();
      });

      // 启动 WebSocket
      this.wsManager = new WebSocketManager(this.server);
    });
  }

  async stop() {
    logger.info('正在关闭服务...');

    // 关闭 WebSocket
    if (this.wsManager) {
      logger.info('关闭 WebSocket 连接...');
      await this.wsManager.close();
    }

    // 关闭 HTTP server
    if (this.server) {
      logger.info('关闭 HTTP 服务...');
      await new Promise((resolve, reject) => {
        this.server.close((err) => {
          if (err) reject(err);
          else resolve();
        });
      });
    }

    // 关闭数据库连接
    if (this.brain && this.brain.pool) {
      logger.info('关闭数据库连接池...');
      // 移除所有监听器避免泄漏
      this.brain.pool.removeAllListeners();
      await this.brain.pool.end();
    }

    // 清理 rate limit map 和定时器
    if (rateLimitCleanupInterval) {
      clearInterval(rateLimitCleanupInterval);
      rateLimitCleanupInterval = null;
    }
    rateLimitMap.clear();

    logger.info('服务已关闭');
  }
}

// 全局异常处理
process.on('uncaughtException', (err) => {
  logger.error('未捕获的异常', { error: err.message, stack: err.stack });
  // 给日志系统时间写入后退出
  setTimeout(() => process.exit(1), 1000);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('未处理的 Promise 拒绝', { reason, promise });
});

// 优雅关闭处理
process.on('SIGTERM', async () => {
  console.log('收到 SIGTERM 信号，开始优雅关闭...');
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('收到 SIGINT 信号，开始优雅关闭...');
  process.exit(0);
});

// CLI
if (require.main === module) {
  const port = process.env.PORT || 3000;
  const server = new ApiServer(parseInt(port));
  server.start().catch(console.error);
}

module.exports = { ApiServer };

