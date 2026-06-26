#!/usr/bin/env node

/**
 * 快速测试：极度简化快速路径 vs 标准文件系统
 * 专注于小消息性能验证
 */

const { MinimalFastPath } = require('./minimal-fast-path.js');

// 标准文件系统实现（与MinimalFastPath类似但无优化标签）
class StandardFileSystem {
    constructor() {
        this.stats = {
            messagesSent: 0,
            totalLatency: 0,
            errors: 0
        };
    }
    
    send(message, options = {}) {
        const startTime = Date.now();
        this.stats.messagesSent++;
        
        try {
            const recipient = options.to || message.to;
            if (!recipient) {
                throw new Error('Recipient is required');
            }
            
            const fs = require('fs');
            const path = require('path');
            
            const timestamp = Date.now();
            const random = Math.random().toString(36).substr(2, 9);
            const filename = `std_${timestamp}_${random}.json`;
            const recipientDir = path.join('/home/kali/.openclaw/workspace/agent_comm', 'inbox', recipient);
            const filepath = path.join(recipientDir, filename);
            
            // 创建目录
            if (!fs.existsSync(recipientDir)) {
                fs.mkdirSync(recipientDir, { recursive: true });
            }
            
            // 准备消息
            const messageData = {
                ...message,
                _standard: true,
                _timestamp: timestamp
            };
            
            const messageStr = JSON.stringify(messageData);
            
            // 同步写入
            fs.writeFileSync(filepath, messageStr, 'utf8');
            
            const latency = Date.now() - startTime;
            this.stats.totalLatency += latency;
            
            return {
                success: true,
                filepath,
                latency,
                size: Buffer.byteLength(messageStr, 'utf8'),
                timestamp: Date.now(),
                standard: true
            };
            
        } catch (error) {
            this.stats.errors++;
            throw new Error(`Standard filesystem failed: ${error.message}`);
        }
    }
    
    getStats() {
        const avgLatency = this.stats.messagesSent > 0 ? 
            this.stats.totalLatency / this.stats.messagesSent : 0;
        
        const successRate = this.stats.messagesSent > 0 ?
            ((this.stats.messagesSent - this.stats.errors) / this.stats.messagesSent * 100) : 0;
        
        return {
            ...this.stats,
            avgLatency: `${avgLatency.toFixed(2)}ms`,
            successRate: `${successRate.toFixed(2)}%`
        };
    }
}

// 生成测试消息
function generateMessage(size) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ';
    let result = '[test] ';
    while (result.length < size) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result.substring(0, size);
}

// 创建测试消息对象
function createTestMessage(size) {
    const content = generateMessage(size - 50);
    
    return {
        id: `test-${Date.now()}`,
        type: 'performance-test',
        timestamp: new Date().toISOString(),
        content,
        metadata: {
            test: true,
            size
        }
    };
}

// 清理测试文件
function cleanupTestFiles(recipient) {
    const fs = require('fs');
    const path = require('path');
    const inboxDir = `/home/kali/.openclaw/workspace/agent_comm/inbox/${recipient}`;
    
    try {
        if (fs.existsSync(inboxDir)) {
            const files = fs.readdirSync(inboxDir);
            let cleaned = 0;
            
            for (const file of files) {
                if (file.includes('.json')) {
                    try {
                        const filepath = path.join(inboxDir, file);
                        const content = fs.readFileSync(filepath, 'utf8');
                        const msg = JSON.parse(content);
                        
                        if ((msg.metadata && msg.metadata.test === true) ||
                            (msg.id && msg.id.includes('test-'))) {
                            fs.unlinkSync(filepath);
                            cleaned++;
                        }
                    } catch (e) {
                        // 忽略错误
                    }
                }
            }
            
            if (cleaned > 0) {
                console.log(`清理了 ${cleaned} 个测试文件`);
            }
        }
    } catch (error) {
        // 忽略错误
    }
}

// 高精度计时（使用performance.now()）
function highResTime() {
    if (typeof performance !== 'undefined' && performance.now) {
        return performance.now();
    }
    return Date.now();
}

// 运行性能测试
function runPerformanceTest() {
    console.log('🚀 快速性能测试：极度简化快速路径 vs 标准文件系统\n');
    
    const recipient = 'product-manager';
    const iterations = 20;
    
    // 清理测试文件
    console.log('🧹 清理测试文件...');
    cleanupTestFiles(recipient);
    
    // 初始化传输实例（每个场景只创建一次）
    console.log('🔄 初始化传输实例...');
    const standardTransport = new StandardFileSystem();
    const minimalFastPath = new MinimalFastPath();
    
    const testSizes = [
        { name: '50字节', size: 50 },
        { name: '100字节', size: 100 },
        { name: '500字节', size: 500 },
        { name: '1024字节', size: 1024 }
    ];
    
    const results = {};
    
    for (const sizeConfig of testSizes) {
        console.log(`\n📤 测试 ${sizeConfig.name} 消息`);
        console.log('='.repeat(40));
        
        const sizeResults = {
            standard: { latencies: [], total: 0 },
            minimal: { latencies: [], total: 0 }
        };
        
        // 预热（忽略前几次结果）
        console.log('  预热...');
        for (let i = 0; i < 3; i++) {
            const testMessage = createTestMessage(sizeConfig.size);
            try {
                standardTransport.send(testMessage, { to: recipient });
                minimalFastPath.send(testMessage, { to: recipient });
            } catch (e) {
                // 忽略预热错误
            }
        }
        
        // 正式测试
        console.log(`  正式测试 ${iterations} 次迭代:`);
        
        for (let i = 0; i < iterations; i++) {
            const testMessage = createTestMessage(sizeConfig.size);
            
            // 测试标准传输
            const stdStart = highResTime();
            try {
                standardTransport.send(testMessage, { to: recipient });
                const stdLatency = highResTime() - stdStart;
                sizeResults.standard.latencies.push(stdLatency);
                sizeResults.standard.total += stdLatency;
            } catch (error) {
                console.log(`    标准传输 迭代 ${i + 1} 失败: ${error.message}`);
            }
            
            // 短暂延迟
            const delayStart = Date.now();
            while (Date.now() - delayStart < 5) {
                // 空循环延迟
            }
            
            // 测试快速路径
            const fastStart = highResTime();
            try {
                minimalFastPath.send(testMessage, { to: recipient });
                const fastLatency = highResTime() - fastStart;
                sizeResults.minimal.latencies.push(fastLatency);
                sizeResults.minimal.total += fastLatency;
            } catch (error) {
                console.log(`    快速路径 迭代 ${i + 1} 失败: ${error.message}`);
            }
            
            // 进度显示
            if ((i + 1) % 5 === 0) {
                process.stdout.write(`    ${i + 1}/${iterations}... `);
                
                if (sizeResults.standard.latencies.length > 0 && sizeResults.minimal.latencies.length > 0) {
                    const stdAvg = sizeResults.standard.total / sizeResults.standard.latencies.length;
                    const fastAvg = sizeResults.minimal.total / sizeResults.minimal.latencies.length;
                    const improvement = ((stdAvg - fastAvg) / stdAvg) * 100;
                    const arrow = improvement > 0 ? '⬇️' : '⬆️';
                    const color = improvement > 0 ? '🟢' : '🔴';
                    process.stdout.write(`${color} ${improvement.toFixed(2)}% ${arrow}\n`);
                } else {
                    process.stdout.write('\n');
                }
            }
        }
        
        // 计算结果
        if (sizeResults.standard.latencies.length > 0 && sizeResults.minimal.latencies.length > 0) {
            const stdAvg = sizeResults.standard.total / sizeResults.standard.latencies.length;
            const fastAvg = sizeResults.minimal.total / sizeResults.minimal.latencies.length;
            const improvement = ((stdAvg - fastAvg) / stdAvg) * 100;
            
            const stdMin = Math.min(...sizeResults.standard.latencies);
            const stdMax = Math.max(...sizeResults.standard.latencies);
            const fastMin = Math.min(...sizeResults.minimal.latencies);
            const fastMax = Math.max(...sizeResults.minimal.latencies);
            
            // 计算标准差
            const stdStdDev = Math.sqrt(
                sizeResults.standard.latencies.reduce((sum, lat) => sum + Math.pow(lat - stdAvg, 2), 0) / 
                sizeResults.standard.latencies.length
            );
            
            const fastStdDev = Math.sqrt(
                sizeResults.minimal.latencies.reduce((sum, lat) => sum + Math.pow(lat - fastAvg, 2), 0) / 
                sizeResults.minimal.latencies.length
            );
            
            console.log(`\n  📊 标准传输: ${stdAvg.toFixed(3)}ms (最小: ${stdMin.toFixed(3)}ms, 最大: ${stdMax.toFixed(3)}ms, 标准差: ${stdStdDev.toFixed(3)}ms)`);
            console.log(`  📊 快速路径: ${fastAvg.toFixed(3)}ms (最小: ${fastMin.toFixed(3)}ms, 最大: ${fastMax.toFixed(3)}ms, 标准差: ${fastStdDev.toFixed(3)}ms)`);
            console.log(`  🎯 性能改进: ${improvement.toFixed(2)}% ${improvement > 0 ? '⬇️' : '⬆️'}`);
            
            // 检查是否达到30%目标
            if (sizeConfig.size <= 100) {
                if (improvement >= 30) {
                    console.log(`  ✅ ${sizeConfig.name} 达到30%改进目标!`);
                } else {
                    console.log(`  ⚠️  ${sizeConfig.name} 未达到30%目标，当前: ${improvement.toFixed(2)}%`);
                }
            }
            
            results[sizeConfig.name] = {
                size: sizeConfig.size,
                standard: {
                    avg: stdAvg,
                    min: stdMin,
                    max: stdMax,
                    stdDev: stdStdDev,
                    samples: sizeResults.standard.latencies.length
                },
                minimal: {
                    avg: fastAvg,
                    min: fastMin,
                    max: fastMax,
                    stdDev: fastStdDev,
                    samples: sizeResults.minimal.latencies.length
                },
                improvement,
                targetAchieved: sizeConfig.size <= 100 ? improvement >= 30 : null
            };
        } else {
            console.log(`  ⚠️  数据不足，无法计算性能`);
            results[sizeConfig.name] = {
                size: sizeConfig.size,
                error: 'Insufficient data'
            };
        }
    }
    
    // 总体评估
    console.log('\n🎯 **总体性能评估**');
    console.log('==================\n');
    
    let smallMessageImprovement = 0;
    let smallMessageCount = 0;
    let allTargetsAchieved = true;
    
    for (const [name, result] of Object.entries(results)) {
        if (result.improvement !== undefined) {
            console.log(`  ${name}: ${result.improvement.toFixed(2)}% 改进`);
            
            if (result.size <= 100) {
                smallMessageImprovement += result.improvement;
                smallMessageCount++;
                
                if (!result.targetAchieved) {
                    allTargetsAchieved = false;
                }
            }
        }
    }
    
    if (smallMessageCount > 0) {
        const avgSmallImprovement = smallMessageImprovement / smallMessageCount;
        console.log(`\n  📈 小消息平均改进: ${avgSmallImprovement.toFixed(2)}%`);
        
        if (allTargetsAchieved && avgSmallImprovement >= 30) {
            console.log('\n  ✅ **所有小消息达到30%改进目标!**');
        } else {
            console.log(`\n  ⚠️  **未完全达到30%改进目标**`);
            console.log(`     需要进一步优化小消息性能`);
        }
    }
    
    // 显示统计信息
    console.log('\n📊 **传输统计信息**');
    console.log('==================\n');
    console.log('标准传输:', standardTransport.getStats());
    console.log('快速路径:', minimalFastPath.getStats());
    
    // 保存结果
    const fs = require('fs');
    const outputFile = '/home/kali/.openclaw/workspace/agent_comm/quick-test-results.json';
    fs.writeFileSync(
        outputFile,
        JSON.stringify({
            timestamp: new Date().toISOString(),
            config: {
                iterations,
                testSizes: testSizes.map(s => ({ name: s.name, size: s.size }))
            },
            results
        }, null, 2),
        'utf8'
    );
    
    console.log(`\n💾 测试结果保存到: ${outputFile}`);
    
    // 清理测试文件
    console.log('\n🧹 清理测试文件...');
    cleanupTestFiles(recipient);
    
    console.log('\n🚀 快速测试完成!');
    
    return {
        allTargetsAchieved,
        results
    };
}

// 运行测试
try {
    const result = runPerformanceTest();
    
    // 根据测试结果退出码
    if (result.allTargetsAchieved) {
        process.exit(0);
    } else {
        process.exit(1);
    }
} catch (error) {
    console.error('❌ 测试运行失败:', error);
    process.exit(1);
}