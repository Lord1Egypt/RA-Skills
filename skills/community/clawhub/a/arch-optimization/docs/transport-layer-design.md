# 传输层重构设计文档

## 设计目标
1. **统一抽象**: 为WebSocket、HTTP、文件系统提供统一接口
2. **性能优化**: 连接复用、批量处理、智能路由
3. **可靠性**: 统一错误处理、重试机制、降级策略
4. **可观测性**: 内置监控指标和追踪

## 架构概览

```
┌─────────────────────────────────────────────┐
│           UnifiedTransport                  │
├──────────────┬──────────────┬──────────────┤
│ WebSocket    │   HTTP       │  FileSystem  │
│ Transport    │  Transport   │  Transport   │
├──────────────┼──────────────┼──────────────┤
│ Connection   │  Connection  │  File        │
│ Pool         │  Pool        │  Manager     │
├──────────────┴──────────────┴──────────────┤
│           TransportStrategy                │ ← 智能传输选择
│           (基于延迟、可靠性、消息大小)      │
└─────────────────────────────────────────────┘
```

## 核心类设计

### 1. UnifiedTransport (主类)
```javascript
class UnifiedTransport {
    /**
     * 统一传输层
     * @param {Object} config - 传输配置
     */
    constructor(config = {}) {
        this.transports = {
            websocket: new WebSocketTransport(config.websocket),
            http: new HTTPTransport(config.http),
            filesystem: new FileSystemTransport(config.filesystem)
        };
        
        this.strategy = new TransportStrategy({
            defaultTransport: 'websocket',
            fallbackOrder: ['websocket', 'http', 'filesystem'],
            selectionRules: config.rules
        });
        
        this.metrics = new TransportMetrics();
        this.retryManager = new RetryManager(config.retry);
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
        
        try {
            // 1. 选择传输方式
            const transportType = this.strategy.selectTransport(message, options);
            const transport = this.transports[transportType];
            
            // 2. 应用传输优化
            const optimizedMessage = await transport.optimize(message);
            
            // 3. 发送（带重试）
            const result = await this.retryManager.execute(
                () => transport.send(optimizedMessage, options),
                { operation: 'send', transport: transportType }
            );
            
            // 4. 记录成功指标
            this.metrics.recordSuccess(traceId, {
                transport: transportType,
                latency: Date.now() - startTime,
                messageSize: JSON.stringify(message).length,
                optimizedSize: optimizedMessage.size || 0
            });
            
            return {
                ...result,
                metadata: {
                    transport: transportType,
                    latency: Date.now() - startTime,
                    traceId
                }
            };
            
        } catch (error) {
            // 5. 记录失败指标
            this.metrics.recordError(traceId, error, {
                transport: transportType,
                retryAttempts: this.retryManager.getAttempts()
            });
            
            // 6. 尝试降级传输
            return this.handleFallback(message, options, error, startTime, traceId);
        }
    }
    
    /**
     * 处理降级传输
     */
    async handleFallback(message, options, error, startTime, traceId) {
        const fallbackTransports = this.strategy.getFallbackTransports(options);
        
        for (const transportType of fallbackTransports) {
            try {
                const transport = this.transports[transportType];
                const result = await transport.send(message, options);
                
                this.metrics.recordFallbackSuccess(traceId, {
                    originalError: error.message,
                    fallbackTransport: transportType,
                    totalLatency: Date.now() - startTime
                });
                
                return {
                    ...result,
                    metadata: {
                        transport: transportType,
                        isFallback: true,
                        latency: Date.now() - startTime,
                        traceId
                    }
                };
            } catch (fallbackError) {
                // 继续尝试下一个降级选项
                continue;
            }
        }
        
        // 所有降级都失败
        throw new Error(`All transports failed: ${error.message}`);
    }
    
    /**
     * 获取统计信息
     */
    getStats() {
        return {
            metrics: this.metrics.getSummary(),
            transports: Object.fromEntries(
                Object.entries(this.transports).map(([name, transport]) => [
                    name, transport.getStats()
                ])
            ),
            strategy: this.strategy.getStats()
        };
    }
}
```

### 2. WebSocketTransport (WebSocket传输实现)
```javascript
class WebSocketTransport {
    constructor(config = {}) {
        this.config = {
            url: config.url || 'ws://localhost:8080',
            maxConnections: config.maxConnections || 10,
            idleTimeout: config.idleTimeout || 30000,
            reconnectAttempts: config.reconnectAttempts || 3,
            reconnectDelay: config.reconnectDelay || 1000,
            ...config
        };
        
        this.connectionPool = new ConnectionPool(this.config);
        this.messageQueue = new MessageQueue();
        this.compression = config.compression !== false;
    }
    
    async send(message, options = {}) {
        // 获取或创建连接
        const connection = await this.connectionPool.acquire(options.agent);
        
        try {
            // 序列化消息
            const serialized = this.serialize(message);
            
            // 应用压缩（如果需要）
            const data = this.compression ? 
                await this.compress(serialized) : serialized;
            
            // 发送消息
            await connection.send(data, options);
            
            return {
                success: true,
                connectionId: connection.id,
                timestamp: Date.now()
            };
            
        } finally {
            // 释放连接回池
            this.connectionPool.release(connection);
        }
    }
    
    async optimize(message) {
        // WebSocket特定优化
        return {
            ...message,
            _optimized: {
                transport: 'websocket',
                timestamp: Date.now(),
                // 可以添加消息合并、压缩等优化
            }
        };
    }
    
    getStats() {
        return {
            poolSize: this.connectionPool.size,
            activeConnections: this.connectionPool.activeCount,
            queueSize: this.messageQueue.size,
            compressionEnabled: this.compression
        };
    }
}
```

### 3. HTTPTransport (HTTP传输实现)
```javascript
class HTTPTransport {
    constructor(config = {}) {
        this.config = {
            baseURL: config.baseURL || 'http://localhost:3000',
            timeout: config.timeout || 5000,
            maxSockets: config.maxSockets || 50,
            keepAlive: config.keepAlive !== false,
            retry: config.retry || { attempts: 2, delay: 100 },
            ...config
        };
        
        this.agent = new http.Agent({
            keepAlive: this.config.keepAlive,
            maxSockets: this.config.maxSockets
        });
        
        this.requestQueue = new RequestQueue(this.config);
    }
    
    async send(message, options = {}) {
        const url = `${this.config.baseURL}/api/messages`;
        
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Agent-Id': options.agent || 'unknown',
                ...options.headers
            },
            body: JSON.stringify(message),
            timeout: options.timeout || this.config.timeout,
            agent: this.agent
        };
        
        return this.requestQueue.add(() => 
            fetch(url, requestOptions).then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
                return res.json();
            })
        );
    }
    
    async optimize(message) {
        // HTTP特定优化：批量处理、压缩、缓存
        return {
            ...message,
            _optimized: {
                transport: 'http',
                batchable: true,
                timestamp: Date.now()
            }
        };
    }
}
```

### 4. FileSystemTransport (文件系统传输实现)
```javascript
class FileSystemTransport {
    constructor(config = {}) {
        this.config = {
            baseDir: config.baseDir || '/home/kali/.openclaw/workspace/agent_comm',
            inboxDir: path.join(this.config.baseDir, 'inbox'),
            outboxDir: path.join(this.config.baseDir, 'outbox'),
            fileEncoding: config.fileEncoding || 'utf8',
            writeMode: config.writeMode || 'atomic', // atomic|direct
            fsync: config.fsync !== false,
            ...config
        };
        
        this.fileManager = new FileManager(this.config);
        this.watchManager = config.watch !== false ? 
            new FileWatchManager(this.config.inboxDir) : null;
    }
    
    async send(message, options = {}) {
        const recipient = options.to || message.to;
        if (!recipient) {
            throw new Error('Recipient is required for file system transport');
        }
        
        const filename = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}.json`;
        const filepath = path.join(this.config.inboxDir, recipient, filename);
        
        // 确保目录存在
        await fs.promises.mkdir(path.dirname(filepath), { recursive: true });
        
        // 写入文件（原子操作）
        const tempFile = `${filepath}.tmp`;
        await fs.promises.writeFile(
            tempFile, 
            JSON.stringify(message, null, 2), 
            this.config.fileEncoding
        );
        
        // 原子重命名
        await fs.promises.rename(tempFile, filepath);
        
        // 如果需要fsync，确保数据写入磁盘
        if (this.config.fsync) {
            const fd = await fs.promises.open(filepath, 'r');
            await fd.sync();
            await fd.close();
        }
        
        // 触发文件事件（如果启用了监听）
        if (this.watchManager) {
            this.watchManager.notify(recipient, filepath);
        }
        
        return {
            success: true,
            filepath,
            timestamp: Date.now(),
            recipient
        };
    }
    
    async optimize(message) {
        // 文件系统优化：批量写入、压缩存储
        return {
            ...message,
            _optimized: {
                transport: 'filesystem',
                compressable: JSON.stringify(message).length > 1024,
                timestamp: Date.now()
            }
        };
    }
}
```

### 5. TransportStrategy (智能传输策略)
```javascript
class TransportStrategy {
    constructor(config = {}) {
        this.config = {
            defaultTransport: config.defaultTransport || 'websocket',
            fallbackOrder: config.fallbackOrder || ['websocket', 'http', 'filesystem'],
            rules: config.rules || [],
            learning: config.learning !== false,
            ...config
        };
        
        this.history = new TransportHistory();
        this.ruleEngine = new RuleEngine(this.config.rules);
        this.learningModel = this.config.learning ? 
            new LearningModel() : null;
    }
    
    selectTransport(message, options = {}) {
        // 1. 检查显式指定的传输
        if (options.transport && this.transports[options.transport]) {
            return options.transport;
        }
        
        // 2. 应用规则引擎
        const ruleResult = this.ruleEngine.evaluate(message, options);
        if (ruleResult.transport) {
            return ruleResult.transport;
        }
        
        // 3. 机器学习推荐（如果启用）
        if (this.learningModel) {
            const prediction = this.learningModel.predict(message, options);
            if (prediction.confidence > 0.8) {
                return prediction.transport;
            }
        }
        
        // 4. 基于消息特性的选择
        return this.selectByMessageCharacteristics(message, options);
    }
    
    selectByMessageCharacteristics(message, options) {
        const messageStr = JSON.stringify(message);
        const messageSize = messageStr.length;
        
        // 基于大小的选择
        if (messageSize < 1024) {
            // 小消息：WebSocket（低延迟）
            return 'websocket';
        } else if (messageSize < 10240) {
            // 中等消息：HTTP（可靠）
            return 'http';
        } else {
            // 大消息：文件系统（避免内存压力）
            return 'filesystem';
        }
    }
    
    getFallbackTransports(options) {
        const selected = this.selectTransport({}, options);
        const order = this.config.fallbackOrder;
        const index = order.indexOf(selected);
        
        return index >= 0 ? 
            order.slice(index + 1) : 
            this.config.fallbackOrder;
    }
    
    recordOutcome(transport, success, latency, messageSize) {
        this.history.record({
            transport,
            success,
            latency,
            messageSize,
            timestamp: Date.now()
        });
        
        if (this.learningModel) {
            this.learningModel.update(transport, success, latency, messageSize);
        }
    }
}
```

## 性能优化特性

### 1. 连接池 (WebSocket)
- 连接复用减少握手开销
- 空闲连接自动关闭
- 连接健康检查
- 负载均衡

### 2. 批量处理 (HTTP/文件系统)
- 时间窗口批量发送
- 智能刷新策略
- 背压控制
- 优先级队列

### 3. 压缩优化
- 自动消息压缩（>1KB）
- 多种算法支持（gzip, brotli）
- 压缩级别自适应
- 缓存压缩结果

### 4. 智能路由
- 基于延迟的历史学习
- 故障自动检测和规避
- 成本感知路由（带宽、计算）
- QoS保障

## 监控指标

### 传输层指标
| 指标 | 描述 | 采集频率 |
|------|------|----------|
| transport.latency | 传输延迟分布 | 实时 |
| transport.success_rate | 传输成功率 | 每分钟 |
| transport.throughput | 消息吞吐量 | 每秒 |
| connection.pool_size | 连接池大小 | 实时 |
| connection.active | 活跃连接数 | 实时 |
| queue.backlog | 队列积压 | 实时 |

### 业务指标
| 指标 | 描述 | 告警阈值 |
|------|------|----------|
| end_to_end.latency | 端到端延迟 | >100ms |
| message.delivery_rate | 消息送达率 | <99.9% |
| error.rate | 错误率 | >0.1% |
| fallback.count | 降级次数 | >10/分钟 |

## 配置示例

```javascript
const transportConfig = {
    // WebSocket配置
    websocket: {
        url: 'ws://localhost:8080',
        maxConnections: 10,
        idleTimeout: 30000,
        reconnectAttempts: 3,
        compression: true
    },
    
    // HTTP配置
    http: {
        baseURL: 'http://localhost:3000',
        timeout: 5000,
        maxSockets: 50,
        keepAlive: true,
        retry: { attempts: 2, delay: 100 }
    },
    
    // 文件系统配置
    filesystem: {
        baseDir: '/home/kali/.openclaw/workspace/agent_comm',
        fsync: true,
        watch: true
    },
    
    // 策略配置
    strategy: {
        defaultTransport: 'websocket',
        fallbackOrder: ['websocket', 'http', 'filesystem'],
        rules: [
            {
                condition: 'message.size > 1048576', // 1MB
                action: 'selectTransport',
                params: { transport: 'filesystem' }
            },
            {
                condition: 'options.priority === "high"',
                action: 'selectTransport', 
                params: { transport: 'websocket' }
            }
        ],
        learning: true
    },
    
    // 重试配置
    retry: {
        maxAttempts: 3,
        backoffFactor: 2,
        initialDelay: 100,
        maxDelay: 5000
    }
};
```

## 向后兼容性

### 迁移策略
1. **并行运行**: 新旧系统同时运行
2. **流量切换**: 逐步将流量切换到新传输层
3. **回滚机制**: 一键回滚到旧版本
4. **兼容层**: 提供适配器支持旧API

### 兼容性保证
- ✅ 现有`comm-send.js` API保持不变
- ✅ 消息格式向后兼容
- ✅ 错误处理保持一致
- ✅ 监控数据可对比

## 测试策略

### 单元测试
- 传输层各组件独立测试
- 策略算法验证
- 错误场景模拟

### 集成测试
- 端到端消息流
- 降级场景测试
- 性能基准测试

### 负载测试
- 高并发消息发送
- 长时间运行稳定性
- 资源泄漏检测

## 实施计划

### 阶段1A: 核心实现 (今日)
1. 实现`UnifiedTransport`基类
2. 实现`FileSystemTransport`（最简单）
3. 实现基本策略选择

### 阶段1B: 优化增强 (明日)
1. 实现`WebSocketTransport`和连接池
2. 实现`HTTPTransport`
3. 完善智能策略

### 阶段1C: 测试验证 (第3天)
1. 性能对比测试
2. 兼容性验证
3. 稳定性测试

## 风险与缓解

### 技术风险
1. **连接池复杂性**: 简化设计，逐步增加功能
2. **策略算法准确性**: 基于简单规则开始，逐步优化
3. **性能倒退**: 充分基准测试，A/B对比

### 实施风险
1. **时间不足**: 聚焦核心功能，分阶段交付
2. **兼容性问题**: 严格测试，提供降级开关
3. **团队协作**: 明确接口，独立开发