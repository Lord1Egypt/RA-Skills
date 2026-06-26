/**
 * 统一传输层实现
 * 为WebSocket、HTTP、文件系统提供统一接口
 * 支持连接复用、智能路由、错误处理和监控
 */

const fs = require('fs').promises;
const path = require('path');
const { EventEmitter } = require('events');

// 默认配置
const DEFAULT_CONFIG = {
    // WebSocket配置
    websocket: {
        enabled: true,
        url: 'ws://localhost:8080',
        maxConnections: 10,
        idleTimeout: 30000,
        reconnectAttempts: 3,
        compression: true
    },
    
    // HTTP配置
    http: {
        enabled: true,
        baseURL: 'http://localhost:3000',
        timeout: 5000,
        maxSockets: 50,
        keepAlive: true,
        retry: { attempts: 2, delay: 100 }
    },
    
    // 文件系统配置
    filesystem: {
        enabled: true,
        baseDir: '/home/kali/.openclaw/workspace/agent_comm',
        fileEncoding: 'utf8',
        writeMode: 'atomic',
        fsync: false,
        watch: false
    },
    
    // 策略配置
    strategy: {
        defaultTransport: 'filesystem', // 默认使用文件系统（最可靠）
        fallbackOrder: ['websocket', 'http', 'filesystem'],
        rules: [],
        learning: false
    },
    
    // 重试配置
    retry: {
        maxAttempts: 3,
        backoffFactor: 2,
        initialDelay: 100,
        maxDelay: 5000
    },
    
    // 监控配置
    monitoring: {
        enabled: true,
        metricsInterval: 60000
    }
};

/**
 * 传输指标收集器
 */
class TransportMetrics {
    constructor() {
        this.metrics = {
            totalMessages: 0,
            successfulMessages: 0,
            failedMessages: 0,
            totalLatency: 0,
            byTransport: {},
            errors: []
        };
        
        this.traces = new Map();
        this.startTime = Date.now();
    }
    
    startTrace(operation, message) {
        const traceId = `trace_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        this.traces.set(traceId, {
            id: traceId,
            operation,
            messageId: message.id || 'unknown',
            startTime: Date.now(),
            status: 'started'
        });
        
        return traceId;
    }
    
    recordSuccess(traceId, metadata = {}) {
        const trace = this.traces.get(traceId);
        if (!trace) return;
        
        const latency = Date.now() - trace.startTime;
        
        trace.status = 'success';
        trace.endTime = Date.now();
        trace.latency = latency;
        trace.metadata = metadata;
        
        // 更新聚合指标
        this.metrics.totalMessages++;
        this.metrics.successfulMessages++;
        this.metrics.totalLatency += latency;
        
        // 按传输类型统计
        const transport = metadata.transport || 'unknown';
        if (!this.metrics.byTransport[transport]) {
            this.metrics.byTransport[transport] = {
                count: 0,
                totalLatency: 0,
                errors: 0
            };
        }
        
        this.metrics.byTransport[transport].count++;
        this.metrics.byTransport[transport].totalLatency += latency;
    }
    
    recordError(traceId, error, metadata = {}) {
        const trace = this.traces.get(traceId);
        if (!trace) return;
        
        trace.status = 'error';
        trace.endTime = Date.now();
        trace.error = error.message;
        trace.metadata = metadata;
        
        // 更新聚合指标
        this.metrics.totalMessages++;
        this.metrics.failedMessages++;
        
        // 记录错误详情
        this.metrics.errors.push({
            timestamp: Date.now(),
            traceId,
            error: error.message,
            transport: metadata.transport,
            operation: trace.operation
        });
        
        // 保留最近100个错误
        if (this.metrics.errors.length > 100) {
            this.metrics.errors.shift();
        }
        
        // 按传输类型统计错误
        const transport = metadata.transport || 'unknown';
        if (!this.metrics.byTransport[transport]) {
            this.metrics.byTransport[transport] = {
                count: 0,
                totalLatency: 0,
                errors: 0
            };
        }
        
        this.metrics.byTransport[transport].errors++;
    }
    
    getSummary() {
        const uptime = Date.now() - this.startTime;
        const successRate = this.metrics.totalMessages > 0 ? 
            (this.metrics.successfulMessages / this.metrics.totalMessages * 100) : 0;
        
        const avgLatency = this.metrics.successfulMessages > 0 ?
            this.metrics.totalLatency / this.metrics.successfulMessages : 0;
        
        // 按传输类型计算指标
        const transportStats = {};
        for (const [transport, stats] of Object.entries(this.metrics.byTransport)) {
            const successRate = stats.count > 0 ? 
                ((stats.count - stats.errors) / stats.count * 100) : 0;
            const avgLatency = (stats.count - stats.errors) > 0 ?
                stats.totalLatency / (stats.count - stats.errors) : 0;
                
            transportStats[transport] = {
                messages: stats.count,
                errors: stats.errors,
                successRate,
                avgLatency
            };
        }
        
        return {
            uptime,
            totalMessages: this.metrics.totalMessages,
            successfulMessages: this.metrics.successfulMessages,
            failedMessages: this.metrics.failedMessages,
            successRate: `${successRate.toFixed(2)}%`,
            avgLatency: `${avgLatency.toFixed(2)}ms`,
            transports: transportStats,
            recentErrors: this.metrics.errors.slice(-10)
        };
    }
}

/**
 * 重试管理器
 */
class RetryManager {
    constructor(config = {}) {
        this.config = {
            maxAttempts: config.maxAttempts || 3,
            backoffFactor: config.backoffFactor || 2,
            initialDelay: config.initialDelay || 100,
            maxDelay: config.maxDelay || 5000,
            ...config
        };
        
        this.attempts = new Map();
    }
    
    async execute(operation, context = {}) {
        let lastError;
        
        for (let attempt = 1; attempt <= this.config.maxAttempts; attempt++) {
            try {
                const result = await operation();
                
                // 记录成功尝试
                this.recordAttempt(context, attempt, true);
                return result;
                
            } catch (error) {
                lastError = error;
                
                // 记录失败尝试
                this.recordAttempt(context, attempt, false, error);
                
                // 如果是最后一次尝试，不再等待
                if (attempt === this.config.maxAttempts) break;
                
                // 计算退避延迟
                const delay = this.calculateBackoff(attempt);
                await this.sleep(delay);
            }
        }
        
        throw lastError;
    }
    
    calculateBackoff(attempt) {
        const delay = this.config.initialDelay * Math.pow(this.config.backoffFactor, attempt - 1);
        return Math.min(delay, this.config.maxDelay);
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    recordAttempt(context, attempt, success, error = null) {
        const key = `${context.operation || 'unknown'}_${context.transport || 'unknown'}`;
        
        if (!this.attempts.has(key)) {
            this.attempts.set(key, []);
        }
        
        this.attempts.get(key).push({
            timestamp: Date.now(),
            attempt,
            success,
            error: error ? error.message : null
        });
        
        // 保留最近100次尝试记录
        const attempts = this.attempts.get(key);
        if (attempts.length > 100) {
            attempts.shift();
        }
    }
    
    getAttempts() {
        const summary = {};
        
        for (const [key, attempts] of this.attempts.entries()) {
            const successful = attempts.filter(a => a.success).length;
            const total = attempts.length;
            const successRate = total > 0 ? (successful / total * 100) : 0;
            
            summary[key] = {
                totalAttempts: total,
                successfulAttempts: successful,
                successRate: `${successRate.toFixed(1)}%`,
                lastAttempt: attempts[attempts.length - 1]
            };
        }
        
        return summary;
    }
}

/**
 * 文件系统传输实现
 */
class FileSystemTransport {
    constructor(config = {}) {
        this.config = {
            baseDir: config.baseDir || '/home/kali/.openclaw/workspace/agent_comm',
            inboxDir: path.join(config.baseDir || '/home/kali/.openclaw/workspace/agent_comm', 'inbox'),
            outboxDir: path.join(config.baseDir || '/home/kali/.openclaw/workspace/agent_comm', 'outbox'),
            fileEncoding: config.fileEncoding || 'utf8',
            writeMode: config.writeMode || 'atomic',
            fsync: config.fsync !== undefined ? config.fsync : false,
            watch: config.watch !== undefined ? config.watch : false,
            ...config
        };
        
        // 确保目录存在
        this.ensureDirectories();
        
        // 文件事件监听器
        this.eventEmitter = new EventEmitter();
        this.watchers = new Map();
        
        if (this.config.watch) {
            this.initializeWatch();
        }
        
        this.stats = {
            filesWritten: 0,
            bytesWritten: 0,
            errors: 0,
            lastWriteTime: 0
        };
    }
    
    ensureDirectories() {
        const dirs = [this.config.inboxDir, this.config.outboxDir];
        
        for (const dir of dirs) {
            try {
                // 使用同步方法确保目录存在
                if (!fs.existsSync) {
                    // 如果fs.existsSync不存在，尝试其他方法
                    require('fs').mkdirSync(dir, { recursive: true });
                } else if (!fs.existsSync(dir)) {
                    require('fs').mkdirSync(dir, { recursive: true });
                }
            } catch (error) {
                console.warn(`Failed to create directory ${dir}: ${error.message}`);
            }
        }
    }
    
    async send(message, options = {}) {
        const startTime = Date.now();
        const recipient = options.to || message.to;
        
        if (!recipient) {
            throw new Error('Recipient is required for file system transport');
        }
        
        try {
            // 生成文件名
            const timestamp = Date.now();
            const random = Math.random().toString(36).substr(2, 9);
            const filename = `${timestamp}_${random}.json`;
            
            // 目标目录
            const recipientDir = path.join(this.config.inboxDir, recipient);
            const filepath = path.join(recipientDir, filename);
            
            // 确保收件人目录存在
            try {
                await fs.mkdir(recipientDir, { recursive: true });
            } catch (error) {
                // 目录可能已存在，继续
            }
            
            // 准备消息数据
            const messageData = {
                ...message,
                _metadata: {
                    id: message.id || `msg_${timestamp}_${random}`,
                    timestamp,
                    from: options.from || 'unknown',
                    to: recipient,
                    transport: 'filesystem',
                    delivery: {
                        attempt: 1,
                        timestamp
                    }
                }
            };
            
            const messageStr = JSON.stringify(messageData, null, 2);
            
            // 写入文件
            if (this.config.writeMode === 'atomic') {
                // 原子写入：先写临时文件，然后重命名
                const tempFile = `${filepath}.tmp`;
                await fs.writeFile(tempFile, messageStr, this.config.fileEncoding);
                await fs.rename(tempFile, filepath);
            } else {
                // 直接写入
                await fs.writeFile(filepath, messageStr, this.config.fileEncoding);
            }
            
            // 可选：同步到磁盘
            if (this.config.fsync) {
                const fd = await fs.open(filepath, 'r');
                await fd.sync();
                await fd.close();
            }
            
            // 更新统计
            this.stats.filesWritten++;
            this.stats.bytesWritten += Buffer.byteLength(messageStr, 'utf8');
            this.stats.lastWriteTime = Date.now();
            
            // 触发文件创建事件
            if (this.config.watch) {
                this.eventEmitter.emit('fileCreated', {
                    filepath,
                    recipient,
                    size: Buffer.byteLength(messageStr, 'utf8'),
                    timestamp: Date.now()
                });
            }
            
            return {
                success: true,
                filepath,
                recipient,
                size: Buffer.byteLength(messageStr, 'utf8'),
                latency: Date.now() - startTime,
                timestamp: Date.now()
            };
            
        } catch (error) {
            this.stats.errors++;
            
            throw new Error(`File system transport failed: ${error.message}`);
        }
    }
    
    async optimize(message) {
        // 文件系统优化：可以添加压缩、批量等优化
        const messageSize = JSON.stringify(message).length;
        
        return {
            ...message,
            _optimized: {
                transport: 'filesystem',
                timestamp: Date.now(),
                compressable: messageSize > 1024,
                originalSize: messageSize
            }
        };
    }
    
    initializeWatch() {
        // 简化的文件监听实现
        // 注意：生产环境应使用chokidar等库
        console.log('File system watch initialized (basic implementation)');
    }
    
    getStats() {
        return {
            ...this.stats,
            config: {
                baseDir: this.config.baseDir,
                writeMode: this.config.writeMode,
                fsync: this.config.fsync,
                watch: this.config.watch
            }
        };
    }
}

/**
 * 传输策略管理器
 */
class TransportStrategy {
    constructor(config = {}) {
        this.config = {
            defaultTransport: config.defaultTransport || 'filesystem',
            fallbackOrder: config.fallbackOrder || ['websocket', 'http', 'filesystem'],
            rules: config.rules || [],
            learning: config.learning !== undefined ? config.learning : false,
            ...config
        };
        
        this.history = [];
        this.ruleCache = new Map();
    }
    
    selectTransport(message, options = {}) {
        // 1. 检查显式指定的传输方式
        if (options.transport) {
            return options.transport;
        }
        
        // 2. 应用规则引擎
        const ruleResult = this.applyRules(message, options);
        if (ruleResult) {
            return ruleResult;
        }
        
        // 3. 基于消息特性的简单选择
        return this.selectByMessageCharacteristics(message, options);
    }
    
    applyRules(message, options) {
        for (const rule of this.config.rules) {
            try {
                if (this.evaluateRule(rule, message, options)) {
                    return rule.action.transport;
                }
            } catch (error) {
                console.warn(`Rule evaluation failed: ${error.message}`);
            }
        }
        return null;
    }
    
    evaluateRule(rule, message, options) {
        // 简化的规则评估
        // 生产环境应使用更复杂的规则引擎
        
        const condition = rule.condition;
        if (!condition) return true;
        
        // 支持简单的条件评估
        if (condition.includes('message.size')) {
            const messageSize = JSON.stringify(message).length;
            const threshold = parseInt(condition.match(/\d+/)[0]);
            
            if (condition.includes('>')) {
                return messageSize > threshold;
            } else if (condition.includes('<')) {
                return messageSize < threshold;
            }
        }
        
        if (condition.includes('options.priority')) {
            const priority = options.priority || 'medium';
            const requiredPriority = condition.match(/=== "(\w+)"/)[1];
            return priority === requiredPriority;
        }
        
        return false;
    }
    
    selectByMessageCharacteristics(message, options) {
        const messageStr = JSON.stringify(message);
        const messageSize = messageStr.length;
        
        // 基于消息大小的简单策略
        if (messageSize < 1024) {
            // 小消息：尝试WebSocket（如果可用）
            return this.config.defaultTransport;
        } else if (messageSize < 10240) {
            // 中等消息：HTTP或文件系统
            return 'filesystem';
        } else {
            // 大消息：文件系统（避免内存压力）
            return 'filesystem';
        }
    }
    
    getFallbackTransports(selectedTransport, options = {}) {
        const order = this.config.fallbackOrder;
        const index = order.indexOf(selectedTransport);
        
        return index >= 0 ? 
            order.slice(index + 1) : 
            this.config.fallbackOrder;
    }
    
    recordOutcome(transport, success, latency, messageSize) {
        const record = {
            transport,
            success,
            latency,
            messageSize,
            timestamp: Date.now()
        };
        
        this.history.push(record);
        
        // 保留最近1000条记录
        if (this.history.length > 1000) {
            this.history.shift();
        }
        
        // 如果启用了学习，更新内部模型
        if (this.config.learning) {
            this.updateLearningModel(record);
        }
    }
    
    updateLearningModel(record) {
        // 简化的学习模型
        // 生产环境应使用更复杂的机器学习算法
        console.log('Learning model updated with record:', record);
    }
    
    getStats() {
        const transportStats = {};
        
        for (const record of this.history) {
            const transport = record.transport;
            if (!transportStats[transport]) {
                transportStats[transport] = {
                    count: 0,
                    successes: 0,
                    totalLatency: 0
                };
            }
            
            transportStats[transport].count++;
            if (record.success) {
                transportStats[transport].successes++;
                transportStats[transport].totalLatency += record.latency;
            }
        }
        
        // 计算成功率
        const summary = {};
        for (const [transport, stats] of Object.entries(transportStats)) {
            summary[transport] = {
                attempts: stats.count,
                successRate: stats.count > 0 ? (stats.successes / stats.count * 100).toFixed(2) + '%' : '0%',
                avgLatency: stats.successes > 0 ? (stats.totalLatency / stats.successes).toFixed(2) + 'ms' : 'N/A'
            };
        }
        
        return {
            totalDecisions: this.history.length,
            transports: summary,
            config: {
                defaultTransport: this.config.defaultTransport,
                fallbackOrder: this.config.fallbackOrder,
                ruleCount: this.config.rules.length,
                learningEnabled: this.config.learning
            }
        };
    }
}

/**
 * WebSocket传输实现（简化版）
 */
class WebSocketTransport {
    constructor(config = {}) {
        this.config = {
            enabled: config.enabled !== undefined ? config.enabled : true,
            url: config.url || 'ws://localhost:8080',
            maxConnections: config.maxConnections || 10,
            idleTimeout: config.idleTimeout || 30000,
            reconnectAttempts: config.reconnectAttempts || 3,
            compression: config.compression !== undefined ? config.compression : true,
            ...config
        };
        
        this.stats = {
            enabled: this.config.enabled,
            connections: 0,
            messagesSent: 0,
            errors: 0,
            lastActivity: 0
        };
        
        console.log('WebSocketTransport initialized (simplified implementation)');
    }
    
    async send(message, options = {}) {
        if (!this.config.enabled) {
            throw new Error('WebSocket transport is disabled');
        }
        
        const startTime = Date.now();
        
        // 简化实现：记录但不实际发送
        // 生产环境应实现完整的WebSocket客户端
        
        await new Promise(resolve => setTimeout(resolve, 10)); // 模拟网络延迟
        
        this.stats.messagesSent++;
        this.stats.lastActivity = Date.now();
        
        return {
            success: true,
            transport: 'websocket',
            simulated: true,
            latency: Date.now() - startTime,
            timestamp: Date.now(),
            message: `WebSocket message would be sent to ${options.to || 'unknown'}`
        };
    }
    
    async optimize(message) {
        return {
            ...message,
            _optimized: {
                transport: 'websocket',
                timestamp: Date.now(),
                websocketOptimized: true
            }
        };
    }
    
    getStats() {
        return {
            ...this.stats,
            config: {
                url: this.config.url,
                maxConnections: this.config.maxConnections,
                compression: this.config.compression
            }
        };
    }
}

/**
 * HTTP传输实现（简化版）
 */
class HTTPTransport {
    constructor(config = {}) {
        this.config = {
            enabled: config.enabled !== undefined ? config.enabled : true,
            baseURL: config.baseURL || 'http://localhost:3000',
            timeout: config.timeout || 5000,
            maxSockets: config.maxSockets || 50,
            keepAlive: config.keepAlive !== undefined ? config.keepAlive : true,
            retry: config.retry || { attempts: 2, delay: 100 },
            ...config
        };
        
        this.stats = {
            enabled: this.config.enabled,
            requests: 0,
            successfulRequests: 0,
            errors: 0,
            lastRequest: 0
        };
        
        console.log('HTTPTransport initialized (simplified implementation)');
    }
    
    async send(message, options = {}) {
        if (!this.config.enabled) {
            throw new Error('HTTP transport is disabled');
        }
        
        const startTime = Date.now();
        
        // 简化实现：记录但不实际发送
        // 生产环境应实现完整的HTTP客户端
        
        await new Promise(resolve => setTimeout(resolve, 15)); // 模拟网络延迟
        
        this.stats.requests++;
        this.stats.successfulRequests++;
        this.stats.lastRequest = Date.now();
        
        return {
            success: true,
            transport: 'http',
            simulated: true,
            latency: Date.now() - startTime,
            timestamp: Date.now(),
            message: `HTTP request would be sent to ${this.config.baseURL}`
        };
    }
    
    async optimize(message) {
        return {
            ...message,
            _optimized: {
                transport: 'http',
                timestamp: Date.now(),
                batchable: true
            }
        };
    }
    
    getStats() {
        return {
            ...this.stats,
            successRate: this.stats.requests > 0 ? 
                (this.stats.successfulRequests / this.stats.requests * 100).toFixed(2) + '%' : '0%',
            config: {
                baseURL: this.config.baseURL,
                timeout: this.config.timeout,
                keepAlive: this.config.keepAlive
            }
        };
    }
}

/**
 * 统一传输层主类
 */
class UnifiedTransport {
    constructor(config = {}) {
        // 合并配置
        this.config = {
            ...DEFAULT_CONFIG,
            ...config
        };
        
        // 初始化传输实例
        this.transports = {
            websocket: new WebSocketTransport(this.config.websocket),
            http: new HTTPTransport(this.config.http),
            filesystem: new FileSystemTransport(this.config.filesystem)
        };
        
        // 初始化策略管理器
        this.strategy = new TransportStrategy(this.config.strategy);
        
        // 初始化监控和重试
        this.metrics = new TransportMetrics();
        this.retryManager = new RetryManager(this.config.retry);
        
        // 定期输出统计信息
        if (this.config.monitoring.enabled) {
            this.setupMonitoring();
        }
        
        console.log('UnifiedTransport initialized with transports:', 
            Object.keys(this.transports).filter(t => this.transports[t].config.enabled !== false));
    }
    
    setupMonitoring() {
        setInterval(() => {
            const stats = this.getStats();
            console.log('\n📊 Transport Layer Metrics:');
            console.log('========================');
            console.log(`Uptime: ${stats.summary.uptime}ms`);
            console.log(`Total Messages: ${stats.summary.totalMessages}`);
            console.log(`Success Rate: ${stats.summary.successRate}`);
            console.log(`Avg Latency: ${stats.summary.avgLatency}`);
            
            if (stats.summary.recentErrors.length > 0) {
                console.log('\nRecent Errors:');
                stats.summary.recentErrors.forEach(error => {
                    console.log(`  [${new Date(error.timestamp).toISOString()}] ${error.error}`);
                });
            }
        }, this.config.monitoring.metricsInterval || 60000);
    }
    
    /**
     * 发送消息
     * @param {Object} message - 消息对象
     * @param {Object} options - 发送选项
     * @returns {Promise<Object>} 发送结果
     */
    async send(message, options = {}) {
        const startTime = Date.now();
        const traceId = this.metrics.startTrace('send', message);
        
        let selectedTransport;
        let result;
        
        try {
            // 1. 选择传输方式
            selectedTransport = this.strategy.selectTransport(message, options);
            
            if (!this.transports[selectedTransport]) {
                throw new Error(`Transport ${selectedTransport} not available`);
            }
            
            // 2. 应用传输优化
            const transport = this.transports[selectedTransport];
            const optimizedMessage = await transport.optimize(message);
            
            // 3. 发送消息（带重试）
            result = await this.retryManager.execute(
                () => transport.send(optimizedMessage, options),
                { operation: 'send', transport: selectedTransport }
            );
            
            // 4. 记录成功指标
            this.metrics.recordSuccess(traceId, {
                transport: selectedTransport,
                latency: Date.now() - startTime,
                messageSize: JSON.stringify(message).length,
                result
            });
            
            // 5. 记录策略结果
            this.strategy.recordOutcome(
                selectedTransport,
                true,
                Date.now() - startTime,
                JSON.stringify(message).length
            );
            
            return {
                ...result,
                metadata: {
                    transport: selectedTransport,
                    latency: Date.now() - startTime,
                    traceId,
                    timestamp: Date.now()
                }
            };
            
        } catch (error) {
            // 6. 记录失败指标
            this.metrics.recordError(traceId, error, {
                transport: selectedTransport,
                retryAttempts: this.retryManager.getAttempts()[`send_${selectedTransport}`]?.totalAttempts || 0
            });
            
            if (selectedTransport) {
                this.strategy.recordOutcome(
                    selectedTransport,
                    false,
                    Date.now() - startTime,
                    JSON.stringify(message).length
                );
            }
            
            // 7. 尝试降级传输
            return this.handleFallback(message, options, error, startTime, traceId, selectedTransport);
        }
    }
    
    /**
     * 处理降级传输
     */
    async handleFallback(message, options, originalError, startTime, traceId, failedTransport) {
        const fallbackTransports = this.strategy.getFallbackTransports(failedTransport, options);
        
        for (const transportType of fallbackTransports) {
            if (!this.transports[transportType]) {
                continue;
            }
            
            try {
                const transport = this.transports[transportType];
                const optimizedMessage = await transport.optimize(message);
                
                const result = await transport.send(optimizedMessage, options);
                
                // 记录降级成功
                this.metrics.recordSuccess(traceId, {
                    transport: transportType,
                    latency: Date.now() - startTime,
                    messageSize: JSON.stringify(message).length,
                    isFallback: true,
                    originalError: originalError.message,
                    result
                });
                
                this.strategy.recordOutcome(
                    transportType,
                    true,
                    Date.now() - startTime,
                    JSON.stringify(message).length
                );
                
                return {
                    ...result,
                    metadata: {
                        transport: transportType,
                        isFallback: true,
                        originalError: originalError.message,
                        latency: Date.now() - startTime,
                        traceId,
                        timestamp: Date.now()
                    }
                };
                
            } catch (fallbackError) {
                // 继续尝试下一个降级选项
                continue;
            }
        }
        
        // 所有降级都失败
        const finalError = new Error(
            `All transport fallbacks failed. Original error: ${originalError.message}. ` +
            `Tried fallbacks: ${fallbackTransports.join(', ')}`
        );
        
        this.metrics.recordError(traceId, finalError, {
            transport: 'all',
            fallbackAttempts: fallbackTransports.length
        });
        
        throw finalError;
    }
    
    /**
     * 获取统计信息
     */
    getStats() {
        return {
            summary: this.metrics.getSummary(),
            transports: Object.fromEntries(
                Object.entries(this.transports).map(([name, transport]) => [
                    name, transport.getStats()
                ])
            ),
            strategy: this.strategy.getStats(),
            retry: this.retryManager.getAttempts()
        };
    }
    
    /**
     * 重置统计信息
     */
    resetStats() {
        this.metrics = new TransportMetrics();
        this.retryManager = new RetryManager(this.config.retry);
        
        // 重置各传输的统计
        for (const transport of Object.values(this.transports)) {
            if (transport.resetStats) {
                transport.resetStats();
            }
        }
    }
}

/**
 * 创建统一传输层实例的工厂函数
 */
function createTransport(config = {}) {
    return new UnifiedTransport(config);
}

/**
 * 直接发送消息的便捷函数
 */
async function sendMessage(message, options = {}, transportConfig = {}) {
    const transport = createTransport(transportConfig);
    return transport.send(message, options);
}

// 导出主要类
module.exports = {
    UnifiedTransport,
    FileSystemTransport,
    WebSocketTransport,
    HTTPTransport,
    TransportStrategy,
    TransportMetrics,
    RetryManager,
    createTransport,
    sendMessage,
    DEFAULT_CONFIG
};