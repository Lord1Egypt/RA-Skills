/**
 * 协议层简化实现
 * 支持JSON和模拟MessagePack，协议自动协商
 */

class ProtocolMetrics {
    constructor() {
        this.metrics = {
            totalOperations: 0,
            serializations: 0,
            deserializations: 0,
            byProtocol: {},
            errors: []
        };
        
        this.traces = new Map();
        this.startTime = Date.now();
    }
    
    startTrace(operation, context) {
        const traceId = `protocol_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        this.traces.set(traceId, {
            id: traceId,
            operation,
            startTime: Date.now(),
            status: 'started',
            context
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
        this.metrics.totalOperations++;
        
        if (trace.operation === 'serialize') {
            this.metrics.serializations++;
        } else if (trace.operation === 'deserialize') {
            this.metrics.deserializations++;
        }
        
        // 按协议统计
        const protocol = metadata.protocol || 'unknown';
        if (!this.metrics.byProtocol[protocol]) {
            this.metrics.byProtocol[protocol] = {
                operations: 0,
                serializations: 0,
                deserializations: 0,
                totalLatency: 0,
                totalInputBytes: 0,
                totalOutputBytes: 0,
                errors: 0
            };
        }
        
        const protocolStats = this.metrics.byProtocol[protocol];
        protocolStats.operations++;
        
        if (trace.operation === 'serialize') {
            protocolStats.serializations++;
        } else {
            protocolStats.deserializations++;
        }
        
        protocolStats.totalLatency += latency;
        
        if (metadata.inputSize) {
            protocolStats.totalInputBytes += metadata.inputSize;
        }
        
        if (metadata.outputSize) {
            protocolStats.totalOutputBytes += metadata.outputSize;
        }
    }
    
    recordError(traceId, error, metadata = {}) {
        const trace = this.traces.get(traceId);
        if (!trace) return;
        
        trace.status = 'error';
        trace.endTime = Date.now();
        trace.error = error.message;
        trace.metadata = metadata;
        
        // 记录错误
        this.metrics.errors.push({
            timestamp: Date.now(),
            traceId,
            error: error.message,
            operation: trace.operation,
            protocol: metadata.protocol
        });
        
        // 保留最近50个错误
        if (this.metrics.errors.length > 50) {
            this.metrics.errors.shift();
        }
        
        // 更新协议错误统计
        const protocol = metadata.protocol || 'unknown';
        if (!this.metrics.byProtocol[protocol]) {
            this.metrics.byProtocol[protocol] = {
                operations: 0,
                serializations: 0,
                deserializations: 0,
                totalLatency: 0,
                totalInputBytes: 0,
                totalOutputBytes: 0,
                errors: 0
            };
        }
        
        this.metrics.byProtocol[protocol].errors++;
    }
    
    getSummary() {
        const uptime = Date.now() - this.startTime;
        
        const protocolStats = {};
        for (const [protocol, stats] of Object.entries(this.metrics.byProtocol)) {
            const successRate = stats.operations > 0 ? 
                ((stats.operations - stats.errors) / stats.operations * 100) : 0;
            
            const avgLatency = stats.operations > 0 ? 
                stats.totalLatency / stats.operations : 0;
            
            const avgInputSize = stats.serializations > 0 ?
                stats.totalInputBytes / stats.serializations : 0;
            
            const avgOutputSize = stats.serializations > 0 ?
                stats.totalOutputBytes / stats.serializations : 0;
            
            const compressionRatio = avgInputSize > 0 ? 
                avgOutputSize / avgInputSize : 1;
            
            protocolStats[protocol] = {
                operations: stats.operations,
                serializations: stats.serializations,
                deserializations: stats.deserializations,
                errors: stats.errors,
                successRate: `${successRate.toFixed(2)}%`,
                avgLatency: `${avgLatency.toFixed(2)}ms`,
                avgInputSize: `${Math.round(avgInputSize)} bytes`,
                avgOutputSize: `${Math.round(avgOutputSize)} bytes`,
                compressionRatio: compressionRatio.toFixed(3),
                spaceSavings: `${((1 - compressionRatio) * 100).toFixed(1)}%`
            };
        }
        
        return {
            uptime: `${uptime}ms`,
            totalOperations: this.metrics.totalOperations,
            serializations: this.metrics.serializations,
            deserializations: this.metrics.deserializations,
            protocols: protocolStats,
            recentErrors: this.metrics.errors.slice(-5)
        };
    }
}

class JSONProtocol {
    constructor(config = {}) {
        this.config = {
            prettyPrint: config.prettyPrint || false,
            space: config.prettyPrint ? 2 : undefined,
            ...config
        };
        
        this.name = 'json';
        this.stats = {
            operations: 0,
            serializations: 0,
            deserializations: 0,
            totalInputBytes: 0,
            totalOutputBytes: 0,
            errors: 0
        };
    }
    
    async serialize(message) {
        const startTime = Date.now();
        
        try {
            const jsonStr = JSON.stringify(message, null, this.config.space);
            const inputSize = Buffer.from(JSON.stringify(message)).length;
            const outputSize = Buffer.from(jsonStr).length;
            
            this.stats.operations++;
            this.stats.serializations++;
            this.stats.totalInputBytes += inputSize;
            this.stats.totalOutputBytes += outputSize;
            
            return {
                data: jsonStr,
                protocol: this.name,
                metadata: {
                    inputSize,
                    outputSize,
                    compressionRatio: 1.0,
                    latency: Date.now() - startTime
                }
            };
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`JSON serialization failed: ${error.message}`);
        }
    }
    
    async deserialize(data, options = {}) {
        const startTime = Date.now();
        
        try {
            const jsonStr = typeof data === 'string' ? data : data.toString('utf8');
            const message = JSON.parse(jsonStr);
            
            this.stats.operations++;
            this.stats.deserializations++;
            
            return {
                message,
                protocol: this.name,
                metadata: {
                    inputSize: Buffer.from(jsonStr).length,
                    outputSize: Buffer.from(JSON.stringify(message)).length,
                    latency: Date.now() - startTime
                }
            };
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`JSON deserialization failed: ${error.message}`);
        }
    }
    
    getStats() {
        const avgInputSize = this.stats.serializations > 0 ?
            this.stats.totalInputBytes / this.stats.serializations : 0;
        const avgOutputSize = this.stats.serializations > 0 ?
            this.stats.totalOutputBytes / this.stats.serializations : 0;
        const successRate = this.stats.operations > 0 ?
            ((this.stats.operations - this.stats.errors) / this.stats.operations * 100) : 0;
        
        return {
            ...this.stats,
            avgInputSize: Math.round(avgInputSize),
            avgOutputSize: Math.round(avgOutputSize),
            successRate: `${successRate.toFixed(2)}%`,
            compressionRatio: '1.000 (基准)'
        };
    }
}

class SimulatedMessagePackProtocol {
    constructor(config = {}) {
        this.config = {
            compressionRatio: config.compressionRatio || 0.65, // 模拟35%体积减少
            speedBoost: config.speedBoost || 0.3, // 模拟30%速度提升
            enabled: config.enabled !== false,
            ...config
        };
        
        this.name = 'msgpack';
        this.stats = {
            operations: 0,
            serializations: 0,
            deserializations: 0,
            totalInputBytes: 0,
            totalOutputBytes: 0,
            errors: 0
        };
        
        if (!this.config.enabled) {
            console.log('MessagePack protocol is disabled (simulation mode)');
        }
    }
    
    async serialize(message) {
        const startTime = Date.now();
        
        if (!this.config.enabled) {
            throw new Error('MessagePack protocol is disabled');
        }
        
        try {
            const jsonStr = JSON.stringify(message);
            const inputSize = Buffer.from(jsonStr).length;
            
            // 模拟MessagePack压缩
            const outputSize = Math.round(inputSize * this.config.compressionRatio);
            
            // 模拟序列化时间（比JSON快）
            const baseTime = 1; // 基准时间
            const simulatedTime = baseTime * (1 - this.config.speedBoost);
            await this.delay(simulatedTime);
            
            // 创建模拟的二进制数据
            const simulatedData = Buffer.from(`MPK${Date.now()}${Math.random().toString(36).substr(2, 9)}`);
            
            this.stats.operations++;
            this.stats.serializations++;
            this.stats.totalInputBytes += inputSize;
            this.stats.totalOutputBytes += outputSize;
            
            return {
                data: simulatedData,
                protocol: this.name,
                metadata: {
                    inputSize,
                    outputSize,
                    compressionRatio: this.config.compressionRatio,
                    latency: Date.now() - startTime,
                    simulated: true
                }
            };
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`MessagePack serialization failed: ${error.message}`);
        }
    }
    
    async deserialize(data, options = {}) {
        const startTime = Date.now();
        
        if (!this.config.enabled) {
            throw new Error('MessagePack protocol is disabled');
        }
        
        try {
            // 模拟反序列化时间
            const baseTime = 1;
            const simulatedTime = baseTime * (1 - this.config.speedBoost);
            await this.delay(simulatedTime);
            
            // 从模拟数据中提取信息（简化）
            const dataStr = data.toString();
            const message = {
                id: `msgpack-${Date.now()}`,
                content: 'Simulated MessagePack message',
                metadata: {
                    protocol: 'msgpack',
                    simulated: true,
                    originalData: dataStr.substring(0, 50) + '...'
                }
            };
            
            const outputSize = Buffer.from(JSON.stringify(message)).length;
            const inputSize = Buffer.from(data).length;
            
            this.stats.operations++;
            this.stats.deserializations++;
            
            return {
                message,
                protocol: this.name,
                metadata: {
                    inputSize,
                    outputSize,
                    latency: Date.now() - startTime,
                    simulated: true
                }
            };
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`MessagePack deserialization failed: ${error.message}`);
        }
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    getStats() {
        const avgInputSize = this.stats.serializations > 0 ?
            this.stats.totalInputBytes / this.stats.serializations : 0;
        const avgOutputSize = this.stats.serializations > 0 ?
            this.stats.totalOutputBytes / this.stats.serializations : 0;
        const successRate = this.stats.operations > 0 ?
            ((this.stats.operations - this.stats.errors) / this.stats.operations * 100) : 0;
        const actualCompression = avgInputSize > 0 ? avgOutputSize / avgInputSize : this.config.compressionRatio;
        
        return {
            ...this.stats,
            avgInputSize: Math.round(avgInputSize),
            avgOutputSize: Math.round(avgOutputSize),
            successRate: `${successRate.toFixed(2)}%`,
            compressionRatio: actualCompression.toFixed(3),
            spaceSavings: `${((1 - actualCompression) * 100).toFixed(1)}%`,
            simulated: true
        };
    }
}

class ProtocolNegotiator {
    constructor(config = {}) {
        this.config = {
            defaultProtocol: config.defaultProtocol || 'json',
            availableProtocols: config.availableProtocols || ['json'],
            learning: config.learning !== false,
            decisionThreshold: config.decisionThreshold || 10,
            ...config
        };
        
        this.history = [];
        this.performance = {};
        
        // 初始化性能记录
        for (const protocol of this.config.availableProtocols) {
            this.performance[protocol] = {
                uses: 0,
                totalLatency: 0,
                totalSizeReduction: 0,
                errors: 0
            };
        }
    }
    
    selectProtocol(message, context = {}) {
        // 1. 检查显式指定的协议
        if (context.protocol && this.config.availableProtocols.includes(context.protocol)) {
            return context.protocol;
        }
        
        // 2. 应用简单规则
        const messageSize = JSON.stringify(message).length;
        
        // 规则1: 小消息使用JSON
        if (messageSize < 500) {
            return 'json';
        }
        
        // 规则2: 如果有MessagePack且消息较大，使用MessagePack
        if (this.config.availableProtocols.includes('msgpack') && messageSize > 1024) {
            // 如果有学习数据，使用性能最好的
            if (this.config.learning && this.history.length >= this.config.decisionThreshold) {
                const bestProtocol = this.getBestProtocolForSize(messageSize);
                if (bestProtocol) {
                    return bestProtocol;
                }
            }
            return 'msgpack';
        }
        
        // 3. 默认协议
        return this.config.defaultProtocol;
    }
    
    getBestProtocolForSize(messageSize) {
        let bestProtocol = null;
        let bestScore = -Infinity;
        
        for (const protocol of this.config.availableProtocols) {
            const perf = this.performance[protocol];
            if (perf.uses === 0) continue;
            
            // 计算得分：考虑延迟和体积减少
            const avgLatency = perf.totalLatency / perf.uses;
            const avgReduction = perf.totalSizeReduction / perf.uses;
            const successRate = (perf.uses - perf.errors) / perf.uses;
            
            // 根据消息大小调整权重
            const sizeWeight = messageSize > 5120 ? 0.6 : 
                              messageSize > 1024 ? 0.4 : 0.2;
            
            const score = (successRate * 0.5) + 
                         ((1 / (avgLatency + 1)) * 0.3) + 
                         (avgReduction * sizeWeight);
            
            if (score > bestScore) {
                bestScore = score;
                bestProtocol = protocol;
            }
        }
        
        return bestProtocol;
    }
    
    recordOutcome(protocol, success, latency, sizeReduction = 0) {
        if (!this.performance[protocol]) {
            this.performance[protocol] = {
                uses: 0,
                totalLatency: 0,
                totalSizeReduction: 0,
                errors: 0
            };
        }
        
        const perf = this.performance[protocol];
        perf.uses++;
        perf.totalLatency += latency;
        perf.totalSizeReduction += sizeReduction;
        
        if (!success) {
            perf.errors++;
        }
        
        // 记录历史
        this.history.push({
            protocol,
            success,
            latency,
            sizeReduction,
            timestamp: Date.now()
        });
        
        // 限制历史大小
        if (this.history.length > 1000) {
            this.history.shift();
        }
    }
    
    getStats() {
        const protocolStats = {};
        
        for (const [protocol, perf] of Object.entries(this.performance)) {
            if (perf.uses > 0) {
                const successRate = ((perf.uses - perf.errors) / perf.uses * 100).toFixed(2);
                const avgLatency = (perf.totalLatency / perf.uses).toFixed(2);
                const avgReduction = (perf.totalSizeReduction / perf.uses).toFixed(3);
                
                protocolStats[protocol] = {
                    uses: perf.uses,
                    successRate: `${successRate}%`,
                    avgLatency: `${avgLatency}ms`,
                    avgSizeReduction: avgReduction
                };
            }
        }
        
        return {
            totalDecisions: this.history.length,
            protocols: protocolStats,
            config: {
                availableProtocols: this.config.availableProtocols,
                defaultProtocol: this.config.defaultProtocol,
                learningEnabled: this.config.learning
            }
        };
    }
}

class ProtocolManager {
    constructor(config = {}) {
        this.config = {
            defaultProtocol: config.defaultProtocol || 'json',
            enableMessagePack: config.enableMessagePack !== false,
            enableLearning: config.enableLearning !== false,
            ...config
        };
        
        // 初始化协议
        this.protocols = {
            json: new JSONProtocol(config.json)
        };
        
        // 条件启用MessagePack
        if (this.config.enableMessagePack) {
            this.protocols.msgpack = new SimulatedMessagePackProtocol({
                ...config.msgpack,
                enabled: true
            });
        }
        
        // 初始化协商器
        const availableProtocols = Object.keys(this.protocols);
        this.negotiator = new ProtocolNegotiator({
            availableProtocols,
            defaultProtocol: this.config.defaultProtocol,
            learning: this.config.enableLearning,
            ...config.negotiator
        });
        
        // 初始化指标
        this.metrics = new ProtocolMetrics();
        
        console.log(`ProtocolManager initialized with protocols: ${availableProtocols.join(', ')}`);
    }
    
    async serialize(message, preferredProtocol = 'auto') {
        const traceId = this.metrics.startTrace('serialize', {
            messageId: message.id || 'unknown',
            preferredProtocol
        });
        
        try {
            // 选择协议
            const protocolName = preferredProtocol === 'auto' ?
                this.negotiator.selectProtocol(message, {}) :
                preferredProtocol;
            
            const protocol = this.protocols[protocolName];
            if (!protocol) {
                throw new Error(`Protocol ${protocolName} not available`);
            }
            
            // 序列化
            const result = await protocol.serialize(message);
            
            // 计算性能指标
            const jsonSize = Buffer.from(JSON.stringify(message)).length;
            const sizeReduction = 1 - (result.metadata.outputSize / jsonSize);
            
            // 记录指标
            this.metrics.recordSuccess(traceId, {
                protocol: protocolName,
                latency: result.metadata.latency,
                inputSize: jsonSize,
                outputSize: result.metadata.outputSize,
                compressionRatio: result.metadata.compressionRatio
            });
            
            // 更新协商器
            this.negotiator.recordOutcome(
                protocolName,
                true,
                result.metadata.latency,
                sizeReduction
            );
            
            return {
                data: result.data,
                protocol: protocolName,
                metadata: {
                    ...result.metadata,
                    traceId,
                    originalSize: jsonSize,
                    sizeReduction: sizeReduction.toFixed(3)
                }
            };
            
        } catch (error) {
            this.metrics.recordError(traceId, error, {
                protocol: preferredProtocol === 'auto' ? 'auto' : preferredProtocol
            });
            
            // 降级到JSON
            if (preferredProtocol !== 'json' && preferredProtocol !== 'auto') {
                console.warn(`Protocol ${preferredProtocol} failed, falling back to JSON: ${error.message}`);
                return this.serialize(message, 'json');
            }
            
            throw error;
        }
    }
    
    async deserialize(data, protocol, options = {}) {
        const traceId = this.metrics.startTrace('deserialize', {
            protocol,
            dataSize: data.length
        });
        
        try {
            const protocolImpl = this.protocols[protocol];
            if (!protocolImpl) {
                throw new Error(`Protocol ${protocol} not available`);
            }
            
            const result = await protocolImpl.deserialize(data, options);
            
            this.metrics.recordSuccess(traceId, {
                protocol,
                latency: result.metadata.latency,
                inputSize: result.metadata.inputSize,
                outputSize: result.metadata.outputSize
            });
            
            return {
                message: result.message,
                protocol,
                metadata: {
                    ...result.metadata,
                    traceId
                }
            };
            
        } catch (error) {
            this.metrics.recordError(traceId, error, { protocol });
            throw error;
        }
    }
    
    autoDeserialize(data) {
        // 简单协议检测
        if (typeof data === 'string') {
            try {
                JSON.parse(data);
                return this.deserialize(data, 'json');
            } catch (e) {
                // 不是有效的JSON
            }
        }
        
        // 检测模拟的MessagePack
        if (Buffer.isBuffer(data) && data.toString().startsWith('MPK')) {
            return this.deserialize(data, 'msgpack');
        }
        
        // 默认尝试JSON
        const dataStr = typeof data === 'string' ? data : data.toString();
        return this.deserialize(dataStr, 'json');
    }
    
    getStats() {
        const protocolStats = {};
        for (const [name, protocol] of Object.entries(this.protocols)) {
            protocolStats[name] = protocol.getStats();
        }
        
        return {
            metrics: this.metrics.getSummary(),
            protocols: protocolStats,
            negotiator: this.negotiator.getStats(),
            config: {
                availableProtocols: Object.keys(this.protocols),
                defaultProtocol: this.config.defaultProtocol,
                enableMessagePack: this.config.enableMessagePack,
                enableLearning: this.config.enableLearning
            }
        };
    }
}

/**
 * 便捷函数：序列化消息
 */
async function serializeMessage(message, protocol = 'auto', config = {}) {
    const manager = new ProtocolManager(config);
    return manager.serialize(message, protocol);
}

/**
 * 便捷函数：反序列化消息
 */
async function deserializeMessage(data, protocol = 'auto', config = {}) {
    const manager = new ProtocolManager(config);
    
    if (protocol === 'auto') {
        return manager.autoDeserialize(data);
    }
    
    return manager.deserialize(data, protocol);
}

// 导出
module.exports = {
    ProtocolManager,
    JSONProtocol,
    SimulatedMessagePackProtocol,
    ProtocolNegotiator,
    ProtocolMetrics,
    serializeMessage,
    deserializeMessage
};