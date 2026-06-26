/**
 * WebSocket 服务器
 * 实时推送记忆变更
 */

const { WebSocketServer } = require('ws');
const { createLogger } = require('../utils/logger.cjs');
const { CONSTANTS } = require('../utils/constants.cjs');

const logger = createLogger('websocket');

class WebSocketManager {
  constructor(server) {
    this.wss = new WebSocketServer({ server });
    this.clients = new Map();
    this.heartbeatInterval = null;
    this.setupHandlers();
    this.startHeartbeat();
  }

  setupHandlers() {
    this.wss.on('connection', (ws, req) => {
      const clientId = this.generateClientId();
      this.clients.set(clientId, {
        ws,
        subscriptions: new Set(),
        connectedAt: new Date()
      });

      logger.info(`WebSocket client connected: ${clientId}`, {
        ip: req.socket.remoteAddress
      });

      // 记录连接时间
      this.clients.get(clientId).lastActivity = Date.now();

      // 发送欢迎消息
      ws.send(JSON.stringify({
        type: 'connected',
        clientId,
        timestamp: new Date().toISOString()
      }));

      ws.on('message', (data) => {
        // 更新活动时间
        const client = this.clients.get(clientId);
        if (client) {
          client.lastActivity = Date.now();
        }

        try {
          const message = JSON.parse(data);
          this.handleMessage(clientId, message);
        } catch (e) {
          logger.warn('Invalid WebSocket message', { error: e.message });
          ws.send(JSON.stringify({
            type: 'error',
            message: 'Invalid message format'
          }));
        }
      });

      ws.on('close', () => {
        logger.info(`WebSocket client disconnected: ${clientId}`);
        this.clients.delete(clientId);
      });

      ws.on('error', (error) => {
        logger.error(`WebSocket error for client ${clientId}`, { error: error.message });
      });
    });
  }

  handleMessage(clientId, message) {
    const client = this.clients.get(clientId);
    if (!client) return;

    switch (message.type) {
      case 'subscribe':
        // 订阅频道
        if (message.channel) {
          client.subscriptions.add(message.channel);
          client.ws.send(JSON.stringify({
            type: 'subscribed',
            channel: message.channel
          }));
        }
        break;

      case 'unsubscribe':
        // 取消订阅
        if (message.channel) {
          client.subscriptions.delete(message.channel);
          client.ws.send(JSON.stringify({
            type: 'unsubscribed',
            channel: message.channel
          }));
        }
        break;

      case 'ping':
        client.ws.send(JSON.stringify({ type: 'pong' }));
        break;

      default:
        client.ws.send(JSON.stringify({
          type: 'error',
          message: `Unknown message type: ${message.type}`
        }));
    }
  }

  /**
   * 广播消息到所有客户端
   */
  broadcast(channel, data) {
    const message = JSON.stringify({
      type: 'broadcast',
      channel,
      data,
      timestamp: new Date().toISOString()
    });

    for (const [clientId, client] of this.clients) {
      if (client.subscriptions.has(channel) || client.subscriptions.has('all')) {
        if (client.ws.readyState === 1) { // WebSocket.OPEN
          client.ws.send(message);
        }
      }
    }
  }

  /**
   * 通知记忆创建
   */
  notifyMemoryCreated(memory) {
    this.broadcast('memory', {
      event: 'created',
      memory: {
        id: memory.id,
        type: memory.type,
        importance: memory.importance,
        entities: memory.entities
      }
    });
  }

  /**
   * 通知概念关联更新
   */
  notifyAssociationUpdated(association) {
    this.broadcast('association', {
      event: 'updated',
      association: {
        fromId: association.fromId,
        toId: association.toId,
        weight: association.weight
      }
    });
  }

  /**
   * 获取连接数
   */
  getConnectionCount() {
    return this.clients.size;
  }

  generateClientId() {
    return `ws_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 启动心跳检测
   */
  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      this.checkConnections();
    }, CONSTANTS.WEBSOCKET.HEARTBEAT_INTERVAL_MS);
  }

  /**
   * 检查连接健康状态
   */
  checkConnections() {
    const now = Date.now();
    for (const [clientId, client] of this.clients) {
      // 如果客户端超过活动超时时间没有活动，发送 ping
      if (now - client.lastActivity > CONSTANTS.WEBSOCKET.ACTIVITY_TIMEOUT_MS) {
        if (client.ws.readyState === 1) {
          client.ws.send(JSON.stringify({ type: 'ping', timestamp: new Date().toISOString() }));
        }
      }
      // 如果超过断开超时时间无响应，断开连接
      if (now - client.lastActivity > CONSTANTS.WEBSOCKET.DISCONNECT_TIMEOUT_MS) {
        logger.warn(`Closing inactive WebSocket client: ${clientId}`);
        client.ws.terminate();
        this.clients.delete(clientId);
      }
    }
  }

  /**
   * 关闭 WebSocket 服务器
   */
  async close() {
    // 停止心跳检测
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }

    // 关闭所有客户端连接
    for (const [clientId, client] of this.clients) {
      try {
        client.ws.terminate();
      } catch (e) {
        logger.warn(`Error closing client ${clientId}: ${e.message}`);
      }
    }
    this.clients.clear();

    // 移除所有监听器
    this.wss.removeAllListeners();

    // 关闭服务器
    return new Promise((resolve) => {
      this.wss.close(() => {
        logger.info('WebSocket server closed');
        resolve();
      });
    });
  }
}

module.exports = { WebSocketManager };

