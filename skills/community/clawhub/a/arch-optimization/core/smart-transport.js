/**
 * 智能传输层 - 带小消息旁路优化
 * 扩展UnifiedTransport，为小消息提供快速路径
 */

const { UnifiedTransport, FileSystemTransport } = require('./transport-layer.js');

// 快速路径传输实现（优化小消息）
class FastPathTransport {
    constructor(config = {}) {
        this.config = {
            baseDir: config.baseDir || '/home/kali/.openclaw/workspace/agent_comm',
            maxCacheSize: config.maxCacheSize || 100,
            batchWindowMs: config.batchWindowMs || 10, // 更小的批量窗口
            enabled: config.enabled !== false,
            ...config
        };
        
        this.cache = new Map(); // 简单缓存
        this.batchQueue = [];
        this.batchTimer = null;
        this.stats = {
            messagesSent: 0,
            cacheHits: 0,
            cacheMisses: 0,
            batchesSent: 0,
            fastPathUsed: 0,
            totalLatency: 0,
            errors: 0
        };
        
        console.log('FastPathTransport initialized');
    }
    
    async send(message, options = {}) {
        const startTime = Date.now();
        
        if (!this.config.enabled) {
            throw new Error('Fast path transport is disabled');
        }
        
        try {
            const recipient = options.to || message.to;
            if (!recipient) {
                throw new Error('Recipient is required');
            }
            
            // 检查缓存（适用于小消息重复发送）
            const cacheKey = this.getCacheKey(recipient, message);
            if (this.cache.has(cacheKey)) {
                const cached = this.cache.get(cacheKey);
                this.stats.cacheHits++;
                
                // 更新缓存访问时间
                this.cache.set(cacheKey, {
                    ...cached,
                    lastAccessed: Date.now()
                });
                
                const latency = Date.now() - startTime;
                this.stats.totalLatency += latency;
                this.stats.messagesSent++;
                
                return {
                    success: true,
                    fromCache: true,
                    cacheKey,
                    latency,
                    timestamp: Date.now(),
                    simulated: true // 缓存命中，不需要实际发送
                };
            }
            
            this.stats.cacheMisses++;
            
            // 批量处理（适用于高频小消息）
            if (this.config.batchWindowMs > 0) {
                return this.sendViaBatch(message, options, startTime);
            }
            
            // 直接发送
            return this.sendDirect(message, options, startTime);
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`Fast path transport failed: ${error.message}`);
        }
    }
    
    async sendViaBatch(message, options, startTime) {
        return new Promise((resolve, reject) => {
            const batchItem = {
                message,
                options,
                startTime,
                resolve,
                reject
            };
            
            this.batchQueue.push(batchItem);
            
            // 启动或重置批量计时器
            if (!this.batchTimer) {
                this.batchTimer = setTimeout(() => {
                    this.flushBatch();
                }, this.config.batchWindowMs);
            }
            
            // 如果批量队列达到一定大小，立即刷新
            if (this.batchQueue.length >= 5) {
                this.flushBatch();
            }
        });
    }
    
    async flushBatch() {
        if (this.batchTimer) {
            clearTimeout(this.batchTimer);
            this.batchTimer = null;
        }
        
        if (this.batchQueue.length === 0) {
            return;
        }
        
        const batchItems = [...this.batchQueue];
        this.batchQueue = [];
        
        try {
            // 批量处理所有消息
            const results = [];
            
            for (const item of batchItems) {
                try {
                    const result = await this.sendDirect(item.message, item.options, item.startTime);
                    item.resolve(result);
                    results.push({ success: true, result });
                } catch (error) {
                    item.reject(error);
                    results.push({ success: false, error });
                }
            }
            
            this.stats.batchesSent++;
            
            // 更新缓存
            for (let i = 0; i < batchItems.length; i++) {
                if (results[i].success) {
                    const item = batchItems[i];
                    const cacheKey = this.getCacheKey(item.options.to || item.message.to, item.message);
                    this.cache.set(cacheKey, {
                        message: item.message,
                        timestamp: Date.now(),
                        lastAccessed: Date.now()
                    });
                    
                    // 限制缓存大小
                    if (this.cache.size > this.config.maxCacheSize) {
                        const oldestKey = Array.from(this.cache.keys())[0];
                        this.cache.delete(oldestKey);
                    }
                }
            }
            
        } catch (error) {
            // 批量处理失败，回退到逐个处理
            console.warn(`Batch processing failed: ${error.message}, falling back to individual sends`);
            
            for (const item of batchItems) {
                try {
                    const result = await this.sendDirect(item.message, item.options, item.startTime);
                    item.resolve(result);
                } catch (error) {
                    item.reject(error);
                }
            }
        }
    }
    
    async sendDirect(message, options, startTime) {
        const recipient = options.to || message.to;
        
        // 使用优化的文件系统写入
        const fs = require('fs').promises;
        const path = require('path');
        
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        const filename = `fast_${timestamp}_${random}.json`;
        const recipientDir = path.join(this.config.baseDir, 'inbox', recipient);
        const filepath = path.join(recipientDir, filename);
        
        // 确保目录存在（同步操作，更快）
        try {
            require('fs').mkdirSync(recipientDir, { recursive: true });
        } catch (error) {
            // 目录可能已存在
        }
        
        // 准备消息（简化版）
        const messageData = {
            ...message,
            _fastPath: true,
            _timestamp: timestamp
        };
        
        const messageStr = JSON.stringify(messageData);
        
        // 直接写入（不使用原子操作，减少开销）
        await fs.writeFile(filepath, messageStr, 'utf8');
        
        const latency = Date.now() - startTime;
        
        this.stats.messagesSent++;
        this.stats.fastPathUsed++;
        this.stats.totalLatency += latency;
        
        return {
            success: true,
            filepath,
            latency,
            size: Buffer.byteLength(messageStr, 'utf8'),
            timestamp: Date.now(),
            fastPath: true
        };
    }
    
    getCacheKey(recipient, message) {
        // 简化的缓存键生成
        const messageStr = JSON.stringify(message);
        return `${recipient}:${messageStr.length}:${hashString(messageStr)}`;
    }
    
    getStats() {
        const avgLatency = this.stats.messagesSent > 0 ? 
            this.stats.totalLatency / this.stats.messagesSent : 0;
        
        const cacheHitRate = (this.stats.cacheHits + this.stats.cacheMisses) > 0 ?
            (this.stats.cacheHits / (this.stats.cacheHits + this.stats.cacheMisses) * 100) : 0;
        
        return {
            ...this.stats,
            avgLatency: `${avgLatency.toFixed(2)}ms`,
            cacheHitRate: `${cacheHitRate.toFixed(2)}%`,
            cacheSize: this.cache.size,
            queueSize: this.batchQueue.length,
            config: {
                enabled: this.config.enabled,
                maxCacheSize: this.config.maxCacheSize,
                batchWindowMs: this.config.batchWindowMs
            }
        };
    }
    
    resetStats() {
        this.stats = {
            messagesSent: 0,
            cacheHits: 0,
            cacheMisses: 0,
            batchesSent: 0,
            fastPathUsed: 0,
            totalLatency: 0,
            errors: 0
        };
    }
}

// 辅助函数：简单字符串哈希
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0; // 转换为32位整数
    }
    return hash.toString(36);
}

// 智能传输层主类
class SmartTransport extends UnifiedTransport {
    constructor(config = {}) {
        // 调用父类构造函数
        super(config);
        
        // 快速路径配置
        this.fastPathConfig = {
            enabled: config.fastPath?.enabled !== false,
            thresholdBytes: config.fastPath?.thresholdBytes || 1024, // 1KB以下使用快速路径
            cacheEnabled: config.fastPath?.cacheEnabled !== false,
            batchEnabled: config.fastPath?.batchEnabled !== false,
            ...config.fastPath
        };
        
        // 初始化快速路径传输
        this.fastPath = new FastPathTransport({
            enabled: this.fastPathConfig.enabled,
            batchWindowMs: this.fastPathConfig.batchEnabled ? 10 : 0,
            maxCacheSize: this.fastPathConfig.cacheEnabled ? 100 : 0,
            ...config.fastPath
        });
        
        // 智能决策统计
        this.decisionStats = {
            totalMessages: 0,
            fastPathUsed: 0,
            fullPathUsed: 0,
            decisionsBySize: {
                small: 0,
                medium: 0,
                large: 0
            }
        };
        
        console.log(`SmartTransport initialized with fast path ${this.fastPathConfig.enabled ? 'enabled' : 'disabled'}`);
    }
    
    async send(message, options = {}) {
        const startTime = Date.now();
        this.decisionStats.totalMessages++;
        
        // 智能路由决策
        const useFastPath = this.shouldUseFastPath(message, options);
        
        if (useFastPath) {
            this.decisionStats.fastPathUsed++;
            
            // 更新按大小统计
            const messageSize = JSON.stringify(message).length;
            if (messageSize < 500) {
                this.decisionStats.decisionsBySize.small++;
            } else if (messageSize < 5000) {
                this.decisionStats.decisionsBySize.medium++;
            } else {
                this.decisionStats.decisionsBySize.large++;
            }
            
            try {
                const result = await this.fastPath.send(message, options);
                
                // 记录快速路径使用
                result.metadata = {
                    ...result.metadata,
                    transport: 'fast-path',
                    decision: 'fast-path',
                    messageSize: JSON.stringify(message).length,
                    latency: Date.now() - startTime
                };
                
                return result;
                
            } catch (error) {
                // 快速路径失败，降级到完整传输层
                console.warn(`Fast path failed, falling back to full transport: ${error.message}`);
                return this.sendViaFullTransport(message, options, startTime, 'fast-path-fallback');
            }
        } else {
            this.decisionStats.fullPathUsed++;
            return this.sendViaFullTransport(message, options, startTime, 'full-path');
        }
    }
    
    shouldUseFastPath(message, options) {
        if (!this.fastPathConfig.enabled) {
            return false;
        }
        
        // 检查显式指定的传输方式
        if (options.transport === 'fast-path') {
            return true;
        }
        if (options.transport === 'full-path') {
            return false;
        }
        
        // 基于消息大小决策
        const messageSize = JSON.stringify(message).length;
        
        // 小消息使用快速路径
        if (messageSize <= this.fastPathConfig.thresholdBytes) {
            return true;
        }
        
        // 高优先级消息使用完整路径（更可靠）
        if (options.priority === 'high') {
            return false;
        }
        
        // 调试模式使用完整路径
        if (options.debug === true) {
            return false;
        }
        
        // 默认：中等和大消息使用完整路径
        return false;
    }
    
    async sendViaFullTransport(message, options, startTime, decisionReason) {
        // 使用父类的完整传输层
        const result = await super.send(message, options);
        
        // 添加决策信息
        if (result.metadata) {
            result.metadata.decision = decisionReason;
            result.metadata.decisionTime = Date.now() - startTime;
        }
        
        return result;
    }
    
    getStats() {
        const parentStats = super.getStats();
        const fastPathStats = this.fastPath.getStats();
        
        const fastPathUsageRate = this.decisionStats.totalMessages > 0 ?
            (this.decisionStats.fastPathUsed / this.decisionStats.totalMessages * 100) : 0;
        
        const avgDecisionTime = this.decisionStats.totalMessages > 0 ?
            parentStats.summary.avgLatency : '0ms';
        
        return {
            ...parentStats,
            smartTransport: {
                decisions: this.decisionStats,
                fastPathUsageRate: `${fastPathUsageRate.toFixed(2)}%`,
                config: this.fastPathConfig
            },
            fastPath: fastPathStats
        };
    }
    
    resetStats() {
        super.resetStats();
        this.fastPath.resetStats();
        this.decisionStats = {
            totalMessages: 0,
            fastPathUsed: 0,
            fullPathUsed: 0,
            decisionsBySize: {
                small: 0,
                medium: 0,
                large: 0
            }
        };
    }
}

// 工厂函数
function createSmartTransport(config = {}) {
    return new SmartTransport(config);
}

// 便捷发送函数
async function sendSmart(message, options = {}, transportConfig = {}) {
    const transport = createSmartTransport(transportConfig);
    return transport.send(message, options);
}

module.exports = {
    SmartTransport,
    FastPathTransport,
    createSmartTransport,
    sendSmart
};