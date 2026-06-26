#!/usr/bin/env node

/**
 * 架构优化性能对比测试
 * 比较新旧架构的性能差异
 */

const fs = require('fs').promises;
const path = require('path');
const { performance } = require('perf_hooks');

// 导入新架构
const { createTransport } = require('./transport-layer.js');
const { ProtocolManager } = require('./protocol-layer.js');

// 测试配置
const TEST_CONFIG = {
    iterations: 10,
    messageSizes: [
        { name: 'small', size: 100 },
        { name: 'medium', size: 1024 },
        { name: 'large', size: 10240 }
    ],
    recipient: 'product-manager',
    outputFile: path.join(__dirname, 'performance-comparison-results.json'),
    cleanupAfterTest: true
};

// 生成测试消息
function generateMessage(size, prefix = '') {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ';
    let result = prefix || '';
    while (result.length < size) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result.substring(0, size);
}

// 创建完整消息对象
function createTestMessage(size, testType) {
    const content = generateMessage(size - 500, `[${testType}] `); // 留出空间给元数据
    
    return {
        id: `test-${testType}-${Date.now()}-${Math.random().toString(36).substr(2, 8)}`,
        type: 'performance-test',
        testType,
        timestamp: new Date().toISOString(),
        content,
        metadata: {
            test: true,
            iteration: 0,
            size,
            testType
        }
    };
}

// 旧架构：直接文件系统写入
class LegacyFileSystem {
    constructor() {
        this.baseDir = '/home/kali/.openclaw/workspace/agent_comm';
        this.inboxDir = path.join(this.baseDir, 'inbox');
        this.stats = {
            operations: 0,
            totalLatency: 0,
            errors: 0
        };
    }
    
    async send(message, recipient) {
        const startTime = performance.now();
        
        try {
            const timestamp = Date.now();
            const random = Math.random().toString(36).substr(2, 9);
            const filename = `${timestamp}_${random}.json`;
            const recipientDir = path.join(this.inboxDir, recipient);
            const filepath = path.join(recipientDir, filename);
            
            // 确保目录存在
            try {
                await fs.mkdir(recipientDir, { recursive: true });
            } catch (error) {
                // 目录可能已存在
            }
            
            // 准备消息
            const messageData = {
                ...message,
                _legacy: true,
                _timestamp: timestamp
            };
            
            const messageStr = JSON.stringify(messageData, null, 2);
            
            // 写入文件（原子操作）
            const tempFile = `${filepath}.tmp`;
            await fs.writeFile(tempFile, messageStr, 'utf8');
            await fs.rename(tempFile, filepath);
            
            const latency = performance.now() - startTime;
            
            this.stats.operations++;
            this.stats.totalLatency += latency;
            
            return {
                success: true,
                filepath,
                latency,
                size: Buffer.byteLength(messageStr, 'utf8')
            };
            
        } catch (error) {
            this.stats.operations++;
            this.stats.errors++;
            
            throw new Error(`Legacy filesystem failed: ${error.message}`);
        }
    }
    
    getStats() {
        const avgLatency = this.stats.operations > 0 ? 
            this.stats.totalLatency / this.stats.operations : 0;
        const successRate = this.stats.operations > 0 ? 
            ((this.stats.operations - this.stats.errors) / this.stats.operations * 100) : 0;
        
        return {
            ...this.stats,
            avgLatency: avgLatency.toFixed(2) + 'ms',
            successRate: successRate.toFixed(2) + '%'
        };
    }
}

// 清理测试文件
async function cleanupTestFiles(recipient) {
    const inboxDir = `/home/kali/.openclaw/workspace/agent_comm/inbox/${recipient}`;
    
    try {
        if (await fs.access(inboxDir).then(() => true).catch(() => false)) {
            const files = await fs.readdir(inboxDir);
            let cleaned = 0;
            
            for (const file of files) {
                if (file.includes('.json')) {
                    try {
                        const filepath = path.join(inboxDir, file);
                        const content = await fs.readFile(filepath, 'utf8');
                        const msg = JSON.parse(content);
                        
                        if ((msg.metadata && msg.metadata.test === true) || 
                            (msg._legacy === true) ||
                            (msg.id && msg.id.includes('test-'))) {
                            await fs.unlink(filepath);
                            cleaned++;
                        }
                    } catch (e) {
                        // 忽略错误
                    }
                }
            }
            
            if (cleaned > 0) {
                console.log(`   清理了 ${cleaned} 个测试文件`);
            }
        }
    } catch (error) {
        // 忽略清理错误
    }
}

// 运行单个测试场景
async function runTestScenario(scenarioName, testFunction, messageSize, iteration) {
    const message = createTestMessage(messageSize, scenarioName);
    
    try {
        const startTime = performance.now();
        const result = await testFunction(message);
        const latency = performance.now() - startTime;
        
        return {
            success: true,
            latency,
            result,
            error: null
        };
    } catch (error) {
        return {
            success: false,
            latency: 0,
            result: null,
            error: error.message
        };
    }
}

// 主测试函数
async function runPerformanceComparison() {
    console.log('🔬 架构优化性能对比测试');
    console.log('=========================\n');
    
    // 清理之前的测试文件
    console.log('🧹 清理之前的测试文件...');
    await cleanupTestFiles(TEST_CONFIG.recipient);
    
    // 初始化测试系统
    console.log('🔄 初始化测试系统...');
    
    // 1. 旧架构（直接文件系统）
    const legacySystem = new LegacyFileSystem();
    
    // 2. 新传输层（文件系统传输）
    const newTransport = createTransport({
        websocket: { enabled: false },
        http: { enabled: false },
        filesystem: { enabled: true },
        monitoring: { enabled: false }
    });
    
    // 3. 协议层
    const protocolManager = new ProtocolManager({
        enableMessagePack: true,
        enableLearning: false
    });
    
    const results = {
        timestamp: new Date().toISOString(),
        config: TEST_CONFIG,
        scenarios: {}
    };
    
    // 定义测试场景
    const scenarios = {
        // 场景1: 旧架构（直接文件系统）
        legacy: {
            name: '旧架构 (直接文件系统)',
            runner: async (message) => {
                return legacySystem.send(message, TEST_CONFIG.recipient);
            }
        },
        
        // 场景2: 新传输层（统一传输层）
        newTransport: {
            name: '新传输层 (统一传输层)',
            runner: async (message) => {
                return newTransport.send(message, {
                    to: TEST_CONFIG.recipient,
                    priority: 'medium'
                });
            }
        },
        
        // 场景3: JSON序列化 + 新传输层
        jsonTransport: {
            name: 'JSON协议 + 新传输层',
            runner: async (message) => {
                // 先序列化
                const serialized = await protocolManager.serialize(message, 'json');
                
                // 通过传输层发送
                return newTransport.send(serialized.data, {
                    to: TEST_CONFIG.recipient,
                    protocol: 'json',
                    metadata: {
                        serialization: serialized.metadata
                    }
                });
            }
        },
        
        // 场景4: MessagePack序列化 + 新传输层
        msgpackTransport: {
            name: 'MessagePack协议 + 新传输层',
            runner: async (message) => {
                // 先序列化
                const serialized = await protocolManager.serialize(message, 'msgpack');
                
                // 通过传输层发送
                return newTransport.send(serialized.data, {
                    to: TEST_CONFIG.recipient,
                    protocol: 'msgpack',
                    metadata: {
                        serialization: serialized.metadata
                    }
                });
            }
        }
    };
    
    // 运行所有测试场景
    for (const msgConfig of TEST_CONFIG.messageSizes) {
        console.log(`\n📤 测试 ${msgConfig.name} 消息 (${msgConfig.size} 字节)`);
        console.log('='.repeat(50));
        
        const sizeResults = {
            messageSize: msgConfig.name,
            sizeBytes: msgConfig.size,
            scenarios: {}
        };
        
        for (const [scenarioId, scenario] of Object.entries(scenarios)) {
            console.log(`\n  🎯 ${scenario.name}:`);
            
            const scenarioResults = {
                name: scenario.name,
                iterations: [],
                latencies: [],
                successes: 0,
                failures: 0
            };
            
            // 运行多次迭代
            for (let i = 0; i < TEST_CONFIG.iterations; i++) {
                process.stdout.write(`    迭代 ${i + 1}/${TEST_CONFIG.iterations}... `);
                
                const result = await runTestScenario(
                    scenarioId,
                    scenario.runner,
                    msgConfig.size,
                    i
                );
                
                if (result.success) {
                    scenarioResults.latencies.push(result.latency);
                    scenarioResults.successes++;
                    scenarioResults.iterations.push({
                        iteration: i + 1,
                        latency: result.latency,
                        success: true,
                        result: result.result
                    });
                    
                    console.log(`${result.latency.toFixed(2)}ms`);
                } else {
                    scenarioResults.failures++;
                    scenarioResults.iterations.push({
                        iteration: i + 1,
                        latency: 0,
                        success: false,
                        error: result.error
                    });
                    
                    console.log(`失败: ${result.error.substring(0, 50)}...`);
                }
                
                // 短暂延迟，避免系统过载
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            
            // 计算统计信息
            if (scenarioResults.latencies.length > 0) {
                const sum = scenarioResults.latencies.reduce((a, b) => a + b, 0);
                const avg = sum / scenarioResults.latencies.length;
                const min = Math.min(...scenarioResults.latencies);
                const max = Math.max(...scenarioResults.latencies);
                
                // 计算百分位数
                const sorted = [...scenarioResults.latencies].sort((a, b) => a - b);
                const p50 = sorted[Math.floor(sorted.length * 0.5)];
                const p90 = sorted[Math.floor(sorted.length * 0.9)];
                const p95 = sorted[Math.floor(sorted.length * 0.95)];
                
                scenarioResults.summary = {
                    average: avg,
                    min,
                    max,
                    p50,
                    p90,
                    p95,
                    totalIterations: TEST_CONFIG.iterations,
                    successfulIterations: scenarioResults.successes,
                    successRate: (scenarioResults.successes / TEST_CONFIG.iterations * 100).toFixed(2) + '%'
                };
                
                console.log(`    📊 平均延迟: ${avg.toFixed(2)}ms (最小: ${min.toFixed(2)}ms, 最大: ${max.toFixed(2)}ms)`);
                console.log(`    📈 成功率: ${scenarioResults.summary.successRate}`);
            } else {
                console.log(`    ⚠️  无成功迭代`);
            }
            
            sizeResults.scenarios[scenarioId] = scenarioResults;
        }
        
        // 计算改进百分比（相对于旧架构）
        const legacyResults = sizeResults.scenarios.legacy;
        if (legacyResults && legacyResults.summary) {
            const legacyAvg = legacyResults.summary.average;
            
            for (const [scenarioId, scenarioResults] of Object.entries(sizeResults.scenarios)) {
                if (scenarioId !== 'legacy' && scenarioResults.summary) {
                    const newAvg = scenarioResults.summary.average;
                    const improvement = ((legacyAvg - newAvg) / legacyAvg) * 100;
                    
                    scenarioResults.improvement = {
                        vsLegacy: improvement.toFixed(2) + '%',
                        absolute: (legacyAvg - newAvg).toFixed(2) + 'ms',
                        legacyAverage: legacyAvg,
                        newAverage: newAvg
                    };
                    
                    const arrow = improvement > 0 ? '⬇️' : '⬆️';
                    const color = improvement > 0 ? '🟢' : '🔴';
                    console.log(`    ${color} ${scenarioResults.name}: ${improvement.toFixed(2)}% ${arrow} 改进`);
                }
            }
        }
        
        results.scenarios[msgConfig.name] = sizeResults;
    }
    
    // 收集最终统计
    console.log('\n📊 **最终性能对比摘要**');
    console.log('=====================');
    
    const finalComparison = {};
    
    for (const [sizeName, sizeResults] of Object.entries(results.scenarios)) {
        console.log(`\n  ${sizeName.toUpperCase()} 消息:`);
        
        finalComparison[sizeName] = {};
        
        for (const [scenarioId, scenarioResults] of Object.entries(sizeResults.scenarios)) {
            if (scenarioResults.summary) {
                console.log(`    ${scenarioResults.name}: ${scenarioResults.summary.average.toFixed(2)}ms`);
                finalComparison[sizeName][scenarioId] = scenarioResults.summary.average;
                
                if (scenarioResults.improvement) {
                    console.log(`      改进: ${scenarioResults.improvement.vsLegacy} (${scenarioResults.improvement.absolute})`);
                }
            }
        }
    }
    
    // 计算总体改进
    console.log('\n🎯 **总体性能分析**');
    console.log('==================');
    
    let totalImprovement = 0;
    let improvementCount = 0;
    
    for (const [sizeName, sizeResults] of Object.entries(results.scenarios)) {
        const legacyAvg = sizeResults.scenarios.legacy?.summary?.average;
        
        if (legacyAvg) {
            // 计算新传输层的改进
            const newTransportAvg = sizeResults.scenarios.newTransport?.summary?.average;
            if (newTransportAvg) {
                const improvement = ((legacyAvg - newTransportAvg) / legacyAvg) * 100;
                console.log(`  ${sizeName}: 传输层改进 ${improvement.toFixed(2)}%`);
                totalImprovement += improvement;
                improvementCount++;
            }
            
            // 计算MessagePack的额外改进
            const msgpackAvg = sizeResults.scenarios.msgpackTransport?.summary?.average;
            if (msgpackAvg && newTransportAvg) {
                const additionalImprovement = ((newTransportAvg - msgpackAvg) / newTransportAvg) * 100;
                console.log(`  ${sizeName}: 协议层额外改进 ${additionalImprovement.toFixed(2)}%`);
            }
        }
    }
    
    if (improvementCount > 0) {
        const avgImprovement = totalImprovement / improvementCount;
        console.log(`\n📈 **平均性能改进: ${avgImprovement.toFixed(2)}%**`);
        
        // 评估是否达到30%目标
        if (avgImprovement >= 30) {
            console.log('✅ **达到30%性能改进目标!**');
        } else {
            console.log(`⚠️  未达到30%目标，当前改进: ${avgImprovement.toFixed(2)}%`);
        }
    }
    
    // 获取各组件统计
    console.log('\n🔧 **组件统计信息**');
    console.log('==================');
    
    console.log('旧架构统计:', legacySystem.getStats());
    console.log('新传输层统计:', newTransport.getStats().summary);
    console.log('协议层统计:', protocolManager.getStats().metrics);
    
    // 保存结果
    await fs.writeFile(
        TEST_CONFIG.outputFile,
        JSON.stringify(results, null, 2),
        'utf8'
    );
    
    console.log(`\n💾 测试结果保存到: ${TEST_CONFIG.outputFile}`);
    
    // 清理测试文件
    if (TEST_CONFIG.cleanupAfterTest) {
        console.log('\n🧹 清理测试文件...');
        await cleanupTestFiles(TEST_CONFIG.recipient);
    }
    
    console.log('\n🚀 性能对比测试完成!');
    
    return results;
}

// 运行测试
runPerformanceComparison().catch(error => {
    console.error('❌ 测试运行失败:', error);
    process.exit(1);
});