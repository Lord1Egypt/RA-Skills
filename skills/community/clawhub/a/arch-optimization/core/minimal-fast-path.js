/**
 * 极度简化的快速路径实现
 * 移除所有缓存、批量处理，只保留最简单的同步写入
 */

const fs = require('fs');
const path = require('path');

// 极度简化的快速路径传输
class MinimalFastPath {
    constructor(config = {}) {
        this.config = {
            baseDir: config.baseDir || '/home/kali/.openclaw/workspace/agent_comm',
            enabled: config.enabled !== false,
            ...config
        };
        
        this.stats = {
            messagesSent: 0,
            totalLatency: 0,
            errors: 0,
            startTime: Date.now()
        };
        
        console.log('MinimalFastPath initialized (sync mode)');
    }
    
    /**
     * 同步发送消息 - 最简单的实现
     */
    send(message, options = {}) {
        const startTime = Date.now();
        this.stats.messagesSent++;
        
        if (!this.config.enabled) {
            this.stats.errors++;
            throw new Error('Minimal fast path is disabled');
        }
        
        try {
            const recipient = options.to || message.to;
            if (!recipient) {
                throw new Error('Recipient is required');
            }
            
            // 准备文件路径
            const timestamp = Date.now();
            const random = Math.random().toString(36).substr(2, 9);
            const filename = `minimal_${timestamp}_${random}.json`;
            const recipientDir = path.join(this.config.baseDir, 'inbox', recipient);
            const filepath = path.join(recipientDir, filename);
            
            // 同步创建目录（如果需要）
            if (!fs.existsSync(recipientDir)) {
                fs.mkdirSync(recipientDir, { recursive: true });
            }
            
            // 准备消息数据
            const messageData = {
                ...message,
                _minimalPath: true,
                _timestamp: timestamp
            };
            
            // 同步写入文件（无原子操作，最简单的写入）
            const messageStr = JSON.stringify(messageData);
            fs.writeFileSync(filepath, messageStr, 'utf8');
            
            const latency = Date.now() - startTime;
            this.stats.totalLatency += latency;
            
            return {
                success: true,
                filepath,
                latency,
                size: Buffer.byteLength(messageStr, 'utf8'),
                timestamp: Date.now(),
                minimalPath: true,
                syncOperation: true
            };
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`Minimal fast path failed: ${error.message}`);
        }
    }
    
    /**
     * 异步发送（兼容接口，但内部使用同步操作）
     */
    async sendAsync(message, options = {}) {
        return this.send(message, options);
    }
    
    getStats() {
        const uptime = Date.now() - this.stats.startTime;
        const avgLatency = this.stats.messagesSent > 0 ? 
            this.stats.totalLatency / this.stats.messagesSent : 0;
        
        const successRate = this.stats.messagesSent > 0 ?
            ((this.stats.messagesSent - this.stats.errors) / this.stats.messagesSent * 100) : 0;
        
        return {
            ...this.stats,
            uptime: `${uptime}ms`,
            avgLatency: `${avgLatency.toFixed(2)}ms`,
            successRate: `${successRate.toFixed(2)}%`,
            config: {
                enabled: this.config.enabled,
                baseDir: this.config.baseDir
            }
        };
    }
    
    resetStats() {
        this.stats = {
            messagesSent: 0,
            totalLatency: 0,
            errors: 0,
            startTime: Date.now()
        };
    }
}

// 简化的智能传输层
class SimpleSmartTransport {
    constructor(config = {}) {
        this.config = {
            fastPath: {
                enabled: config.fastPath?.enabled !== false,
                thresholdBytes: config.fastPath?.thresholdBytes || 500, // 调整阈值
                ...config.fastPath
            },
            filesystem: { enabled: true },
            ...config
        };
        
        // 初始化快速路径
        this.fastPath = new MinimalFastPath({
            enabled: this.config.fastPath.enabled,
            baseDir: this.config.baseDir
        });
        
        // 决策统计
        this.decisionStats = {
            totalMessages: 0,
            fastPathUsed: 0,
            fullPathUsed: 0,
            decisionsBySize: {
                tiny: 0,      // <100字节
                small: 0,     // 100-500字节
                medium: 0,    // 500-1024字节
                large: 0      // >1024字节
            }
        };
        
        console.log(`SimpleSmartTransport initialized with threshold ${this.config.fastPath.thresholdBytes} bytes`);
    }
    
    async send(message, options = {}) {
        const startTime = Date.now();
        this.decisionStats.totalMessages++;
        
        // 计算消息大小
        const messageSize = JSON.stringify(message).length;
        
        // 智能决策：基于消息大小选择路径
        const useFastPath = this.shouldUseFastPath(messageSize, options);
        
        if (useFastPath) {
            this.decisionStats.fastPathUsed++;
            
            // 更新大小分类统计
            if (messageSize < 100) {
                this.decisionStats.decisionsBySize.tiny++;
            } else if (messageSize < 500) {
                this.decisionStats.decisionsBySize.small++;
            } else if (messageSize < 1024) {
                this.decisionStats.decisionsBySize.medium++;
            } else {
                this.decisionStats.decisionsBySize.large++;
            }
            
            try {
                const result = this.fastPath.send(message, options);
                
                // 添加决策信息
                result.decision = 'minimal-fast-path';
                result.decisionTime = Date.now() - startTime;
                result.messageSize = messageSize;
                
                return result;
                
            } catch (error) {
                // 快速路径失败，抛出错误（不降级，保持简单）
                throw new Error(`Minimal fast path failed: ${error.message}`);
            }
        } else {
            this.decisionStats.fullPathUsed++;
            
            // 对于完整路径，我们使用标准文件系统传输
            // 这里简化实现，直接使用类似的同步写入但带更多特性
            return this.sendViaFullPath(message, options, startTime, messageSize);
        }
    }
    
    shouldUseFastPath(messageSize, options) {
        if (!this.config.fastPath.enabled) {
            return false;
        }
        
        // 检查显式指定的传输方式
        if (options.transport === 'minimal-fast-path') {
            return true;
        }
        if (options.transport === 'full-path') {
            return false;
        }
        
        // 基于消息大小决策
        if (messageSize <= this.config.fastPath.thresholdBytes) {
            return true;
        }
        
        // 高优先级消息使用完整路径（更可靠）
        if (options.priority === 'high') {
            return false;
        }
        
        // 默认：超过阈值使用完整路径
        return false;
    }
    
    sendViaFullPath(message, options, startTime, messageSize) {
        // 简化版的完整路径实现
        // 与快速路径类似，但使用异步写入和更多错误处理
        
        const recipient = options.to || message.to;
        if (!recipient) {
            throw new Error('Recipient is required');
        }
        
        const fs = require('fs');
        const path = require('path');
        
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        const filename = `full_${timestamp}_${random}.json`;
        const recipientDir = path.join(this.config.baseDir || '/home/kali/.openclaw/workspace/agent_comm', 'inbox', recipient);
        const filepath = path.join(recipientDir, filename);
        
        // 创建目录
        if (!fs.existsSync(recipientDir)) {
            fs.mkdirSync(recipientDir, { recursive: true });
        }
        
        // 准备消息
        const messageData = {
            ...message,
            _fullPath: true,
            _timestamp: timestamp
        };
        
        const messageStr = JSON.stringify(messageData);
        
        // 同步写入（保持简单）
        fs.writeFileSync(filepath, messageStr, 'utf8');
        
        const latency = Date.now() - startTime;
        
        return {
            success: true,
            filepath,
            latency,
            size: Buffer.byteLength(messageStr, 'utf8'),
            timestamp: Date.now(),
            fullPath: true,
            decision: 'full-path',
            decisionTime: latency,
            messageSize
        };
    }
    
    getStats() {
        const fastPathStats = this.fastPath.getStats();
        
        const fastPathUsageRate = this.decisionStats.totalMessages > 0 ?
            (this.decisionStats.fastPathUsed / this.decisionStats.totalMessages * 100) : 0;
        
        return {
            decisions: this.decisionStats,
            fastPathUsageRate: `${fastPathUsageRate.toFixed(2)}%`,
            fastPath: fastPathStats,
            config: this.config.fastPath
        };
    }
    
    resetStats() {
        this.fastPath.resetStats();
        this.decisionStats = {
            totalMessages: 0,
            fastPathUsed: 0,
            fullPathUsed: 0,
            decisionsBySize: {
                tiny: 0,
                small: 0,
                medium: 0,
                large: 0
            }
        };
    }
}

// 工厂函数
function createSimpleSmartTransport(config = {}) {
    return new SimpleSmartTransport(config);
}

// 便捷发送函数（同步版本）
function sendMinimalFast(message, options = {}, transportConfig = {}) {
    const transport = createSimpleSmartTransport(transportConfig);
    return transport.send(message, options);
}

// 测试函数
function testMinimalFastPath() {
    console.log('🧪 测试极度简化快速路径...');
    
    const fastPath = new MinimalFastPath();
    
    const testMessage = {
        id: 'test-minimal',
        type: 'test',
        content: 'Test minimal fast path',
        timestamp: new Date().toISOString()
    };
    
    try {
        const result = fastPath.send(testMessage, { to: 'product-manager' });
        console.log('✅ 测试成功:', {
            success: result.success,
            latency: result.latency,
            size: result.size
        });
        
        const stats = fastPath.getStats();
        console.log('📊 统计:', stats);
        
        return result;
    } catch (error) {
        console.error('❌ 测试失败:', error.message);
        throw error;
    }
}

module.exports = {
    MinimalFastPath,
    SimpleSmartTransport,
    createSimpleSmartTransport,
    sendMinimalFast,
    testMinimalFastPath
};