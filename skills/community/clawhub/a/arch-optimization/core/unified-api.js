/**
 * 统一通信API
 * 提供简洁一致的接口，取代多个现有通信方式
 */

const { createSmartTransport } = require('./smart-transport.js');
const { ProtocolManager } = require('./protocol-layer.js');

// 默认配置
const DEFAULT_API_CONFIG = {
    // 传输层配置
    transport: {
        // 智能传输配置
        fastPath: {
            enabled: true,
            thresholdBytes: 1024, // 1KB以下使用快速路径
            cacheEnabled: true,
            batchEnabled: true
        },
        
        // 基础传输配置
        websocket: { enabled: false },
        http: { enabled: false },
        filesystem: { enabled: true },
        
        // 监控
        monitoring: { enabled: true, metricsInterval: 60000 }
    },
    
    // 协议层配置
    protocol: {
        defaultProtocol: 'auto', // 自动协商
        enableMessagePack: true,
        enableLearning: true
    },
    
    // API行为配置
    behavior: {
        defaultTimeout: 5000, // 5秒超时
        retryAttempts: 3,
        requireAck: false, // 是否需要确认
        enableBroadcast: true,
        enableRequestResponse: true
    }
};

/**
 * 统一通信API类
 */
class UnifiedAgentComm {
    constructor(config = {}) {
        this.config = {
            ...DEFAULT_API_CONFIG,
            ...config
        };
        
        // 初始化传输层
        this.transport = createSmartTransport(this.config.transport);
        
        // 初始化协议层
        this.protocolManager = new ProtocolManager(this.config.protocol);
        
        // 请求-响应映射表
        this.pendingRequests = new Map();
        this.requestTimeout = 30000; // 30秒请求超时
        
        // 事件监听器
        this.eventListeners = new Map();
        
        // 统计信息
        this.stats = {
            messagesSent: 0,
            messagesReceived: 0,
            requestsSent: 0,
            responsesReceived: 0,
            broadcastSent: 0,
            errors: 0,
            startTime: Date.now()
        };
        
        console.log('UnifiedAgentComm API initialized');
    }
    
    /**
     * 发送消息到指定agent（基础功能）
     * @param {string} recipient - 收件人agent名称
     * @param {Object|string} message - 消息内容
     * @param {Object} options - 发送选项
     * @returns {Promise<Object>} 发送结果
     */
    async send(recipient, message, options = {}) {
        const startTime = Date.now();
        this.stats.messagesSent++;
        
        try {
            // 准备消息对象
            const messageObj = this.prepareMessage(message, recipient, options);
            
            // 序列化消息
            const serialized = await this.protocolManager.serialize(
                messageObj,
                options.protocol || this.config.protocol.defaultProtocol
            );
            
            // 准备传输选项
            const transportOptions = {
                to: recipient,
                timeout: options.timeout || this.config.behavior.defaultTimeout,
                priority: options.priority || 'medium',
                requireAck: options.requireAck || this.config.behavior.requireAck,
                metadata: {
                    ...options.metadata,
                    serialization: serialized.metadata,
                    messageId: messageObj.id
                },
                ...options
            };
            
            // 发送消息
            const result = await this.transport.send(serialized.data, transportOptions);
            
            // 触发发送完成事件
            this.emit('message:sent', {
                messageId: messageObj.id,
                recipient,
                result,
                latency: Date.now() - startTime
            });
            
            return {
                success: true,
                messageId: messageObj.id,
                recipient,
                protocol: serialized.protocol,
                transport: result.metadata?.transport || 'unknown',
                latency: Date.now() - startTime,
                metadata: {
                    serialization: serialized.metadata,
                    transport: result.metadata,
                    timestamp: Date.now()
                }
            };
            
        } catch (error) {
            this.stats.errors++;
            
            this.emit('message:error', {
                recipient,
                message,
                error: error.message,
                latency: Date.now() - startTime
            });
            
            throw new Error(`Failed to send message to ${recipient}: ${error.message}`);
        }
    }
    
    /**
     * 发送请求并等待响应（请求-响应模式）
     * @param {string} recipient - 收件人agent名称
     * @param {Object|string} request - 请求内容
     * @param {Object} options - 请求选项
     * @returns {Promise<Object>} 响应结果
     */
    async request(recipient, request, options = {}) {
        if (!this.config.behavior.enableRequestResponse) {
            throw new Error('Request-response mode is disabled');
        }
        
        const requestId = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const startTime = Date.now();
        this.stats.requestsSent++;
        
        return new Promise((resolve, reject) => {
            // 设置超时
            const timeout = options.timeout || this.config.behavior.defaultTimeout;
            const timeoutId = setTimeout(() => {
                this.pendingRequests.delete(requestId);
                reject(new Error(`Request timeout after ${timeout}ms`));
            }, timeout);
            
            // 保存待处理请求
            this.pendingRequests.set(requestId, {
                resolve,
                reject,
                timeoutId,
                startTime,
                recipient,
                request
            });
            
            // 发送请求消息
            const requestMessage = {
                ...this.prepareMessage(request, recipient, options),
                _type: 'request',
                _requestId: requestId,
                _expectResponse: true,
                _responseTimeout: timeout
            };
            
            this.send(recipient, requestMessage, {
                ...options,
                messageId: requestId,
                requireAck: true
            }).catch(error => {
                clearTimeout(timeoutId);
                this.pendingRequests.delete(requestId);
                reject(new Error(`Failed to send request: ${error.message}`));
            });
        });
    }
    
    /**
     * 广播消息到多个agents
     * @param {string[]} recipients - 收件人列表
     * @param {Object|string} message - 消息内容
     * @param {Object} options - 发送选项
     * @returns {Promise<Object[]>} 发送结果数组
     */
    async broadcast(recipients, message, options = {}) {
        if (!this.config.behavior.enableBroadcast) {
            throw new Error('Broadcast mode is disabled');
        }
        
        if (!Array.isArray(recipients) || recipients.length === 0) {
            throw new Error('Recipients must be a non-empty array');
        }
        
        const broadcastId = `bcast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const startTime = Date.now();
        this.stats.broadcastSent++;
        
        // 准备广播消息
        const broadcastMessage = {
            ...this.prepareMessage(message, 'broadcast', options),
            _type: 'broadcast',
            _broadcastId: broadcastId,
            _recipientCount: recipients.length
        };
        
        // 并行发送到所有收件人
        const sendPromises = recipients.map(recipient => 
            this.send(recipient, broadcastMessage, {
                ...options,
                messageId: `${broadcastId}_${recipient}`,
                priority: options.priority || 'low' // 广播通常优先级较低
            }).catch(error => ({
                success: false,
                recipient,
                error: error.message
            }))
        );
        
        const results = await Promise.all(sendPromises);
        
        // 统计成功/失败
        const successful = results.filter(r => r.success).length;
        const failed = results.filter(r => !r.success).length;
        
        this.emit('broadcast:completed', {
            broadcastId,
            recipients,
            successful,
            failed,
            totalLatency: Date.now() - startTime
        });
        
        return {
            broadcastId,
            totalRecipients: recipients.length,
            successful,
            failed,
            results,
            totalLatency: Date.now() - startTime
        };
    }
    
    /**
     * 处理接收到的消息（由agent调用）
     * @param {Object} rawMessage - 原始消息数据
     * @returns {Object} 处理结果
     */
    async receive(rawMessage) {
        this.stats.messagesReceived++;
        const startTime = Date.now();
        
        try {
            // 自动检测协议并反序列化
            const deserialized = await this.protocolManager.autoDeserialize(rawMessage);
            const message = deserialized.message;
            
            // 触发消息接收事件
            this.emit('message:received', {
                message,
                protocol: deserialized.protocol,
                metadata: deserialized.metadata,
                latency: Date.now() - startTime
            });
            
            // 处理请求-响应
            if (message._type === 'request' && message._requestId) {
                this.stats.responsesReceived++;
                
                // 查找对应的待处理请求
                const pendingRequest = this.pendingRequests.get(message._requestId);
                if (pendingRequest) {
                    clearTimeout(pendingRequest.timeoutId);
                    this.pendingRequests.delete(message._requestId);
                    
                    pendingRequest.resolve({
                        success: true,
                        requestId: message._requestId,
                        response: message,
                        latency: Date.now() - pendingRequest.startTime
                    });
                }
                
                this.emit('request:response', {
                    requestId: message._requestId,
                    response: message,
                    latency: Date.now() - startTime
                });
            }
            
            return {
                success: true,
                message,
                protocol: deserialized.protocol,
                metadata: deserialized.metadata,
                processingTime: Date.now() - startTime
            };
            
        } catch (error) {
            this.stats.errors++;
            
            this.emit('receive:error', {
                rawMessage,
                error: error.message,
                latency: Date.now() - startTime
            });
            
            throw new Error(`Failed to receive message: ${error.message}`);
        }
    }
    
    /**
     * 订阅事件
     * @param {string} eventName - 事件名称
     * @param {Function} listener - 事件监听器
     */
    on(eventName, listener) {
        if (!this.eventListeners.has(eventName)) {
            this.eventListeners.set(eventName, []);
        }
        this.eventListeners.get(eventName).push(listener);
    }
    
    /**
     * 取消事件订阅
     * @param {string} eventName - 事件名称
     * @param {Function} listener - 事件监听器
     */
    off(eventName, listener) {
        if (this.eventListeners.has(eventName)) {
            const listeners = this.eventListeners.get(eventName);
            const index = listeners.indexOf(listener);
            if (index !== -1) {
                listeners.splice(index, 1);
            }
        }
    }
    
    /**
     * 触发事件
     * @param {string} eventName - 事件名称
     * @param {Object} data - 事件数据
     */
    emit(eventName, data) {
        if (this.eventListeners.has(eventName)) {
            const listeners = this.eventListeners.get(eventName);
            for (const listener of listeners) {
                try {
                    listener(data);
                } catch (error) {
                    console.error(`Event listener error for ${eventName}:`, error);
                }
            }
        }
    }
    
    /**
     * 准备消息对象
     */
    prepareMessage(content, recipient, options = {}) {
        const messageId = options.messageId || `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        const message = {
            id: messageId,
            type: 'message',
            timestamp: new Date().toISOString(),
            from: options.from || 'unknown',
            to: recipient,
            content: typeof content === 'string' ? content : content,
            metadata: {
                ...options.metadata,
                version: '1.0',
                api: 'unified-agent-comm'
            }
        };
        
        // 如果content是对象，合并到消息中
        if (typeof content === 'object' && content !== null && !Array.isArray(content)) {
            Object.assign(message, content);
            delete message.content; // 移除重复的content字段
        }
        
        return message;
    }
    
    /**
     * 获取统计信息
     */
    getStats() {
        const uptime = Date.now() - this.stats.startTime;
        const successRate = this.stats.messagesSent > 0 ?
            ((this.stats.messagesSent - this.stats.errors) / this.stats.messagesSent * 100) : 0;
        
        const requestSuccessRate = this.stats.requestsSent > 0 ?
            (this.stats.responsesReceived / this.stats.requestsSent * 100) : 0;
        
        return {
            ...this.stats,
            uptime: `${uptime}ms`,
            successRate: `${successRate.toFixed(2)}%`,
            requestSuccessRate: `${requestSuccessRate.toFixed(2)}%`,
            pendingRequests: this.pendingRequests.size,
            config: {
                transport: this.config.transport.fastPath.enabled ? 'smart' : 'standard',
                protocol: this.config.protocol.defaultProtocol,
                features: {
                    requestResponse: this.config.behavior.enableRequestResponse,
                    broadcast: this.config.behavior.enableBroadcast
                }
            }
        };
    }
    
    /**
     * 重置统计信息
     */
    resetStats() {
        this.stats = {
            messagesSent: 0,
            messagesReceived: 0,
            requestsSent: 0,
            responsesReceived: 0,
            broadcastSent: 0,
            errors: 0,
            startTime: Date.now()
        };
        
        // 清除所有待处理请求
        for (const [requestId, request] of this.pendingRequests.entries()) {
            clearTimeout(request.timeoutId);
        }
        this.pendingRequests.clear();
        
        // 重置传输层统计
        if (this.transport.resetStats) {
            this.transport.resetStats();
        }
    }
    
    /**
     * 关闭API，清理资源
     */
    async close() {
        // 清理待处理请求
        for (const [requestId, request] of this.pendingRequests.entries()) {
            clearTimeout(request.timeoutId);
            request.reject(new Error('API closed'));
        }
        this.pendingRequests.clear();
        
        // 清理事件监听器
        this.eventListeners.clear();
        
        console.log('UnifiedAgentComm API closed');
    }
}

/**
 * 便捷函数：创建统一API实例
 */
function createAgentComm(config = {}) {
    return new UnifiedAgentComm(config);
}

/**
 * 便捷函数：发送消息
 */
async function sendMessage(recipient, message, options = {}, apiConfig = {}) {
    const api = createAgentComm(apiConfig);
    try {
        return await api.send(recipient, message, options);
    } finally {
        await api.close();
    }
}

/**
 * 便捷函数：发送请求
 */
async function sendRequest(recipient, request, options = {}, apiConfig = {}) {
    const api = createAgentComm(apiConfig);
    try {
        return await api.request(recipient, request, options);
    } finally {
        await api.close();
    }
}

/**
 * 便捷函数：广播消息
 */
async function broadcastMessage(recipients, message, options = {}, apiConfig = {}) {
    const api = createAgentComm(apiConfig);
    try {
        return await api.broadcast(recipients, message, options);
    } finally {
        await api.close();
    }
}

// 导出
module.exports = {
    UnifiedAgentComm,
    createAgentComm,
    sendMessage,
    sendRequest,
    broadcastMessage,
    DEFAULT_API_CONFIG
};