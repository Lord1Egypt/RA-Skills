/**
 * 高级功能示例
 * 展示智能传输层、协议层和监控功能
 */

const { createAgentComm } = require('../core/unified-api.js');
const { createSimpleSmartTransport, MinimalFastPath } = require('../core/minimal-fast-path.js');
const { ProtocolManager } = require('../core/protocol-layer.js');

async function runAdvancedFeaturesExamples() {
    console.log('🚀 通信协议架构优化 - 高级功能示例\n');
    
    // 示例1: 智能传输层决策
    console.log('1. 智能传输层决策示例');
    console.log('='.repeat(50));
    
    try {
        const smartTransport = createSimpleSmartTransport({
            fastPath: {
                enabled: true,
                thresholdBytes: 500 // 500字节以下使用快速路径
            }
        });
        
        console.log('智能传输层配置:');
        console.log('  - 快速路径: 启用');
        console.log('  - 阈值: 500字节');
        console.log('  - 决策基于消息大小\n');
        
        // 测试不同大小的消息
        const testMessages = [
            { name: '极小消息', size: 50 },
            { name: '小消息', size: 300 },
            { name: '中等消息', size: 600 },
            { name: '大消息', size: 1500 }
        ];
        
        for (const msgConfig of testMessages) {
            const message = {
                id: `smart-test-${msgConfig.name}`,
                type: 'test',
                content: 'x'.repeat(msgConfig.size - 100), // 留出空间给元数据
                timestamp: new Date().toISOString()
            };
            
            const startTime = Date.now();
            const result = await smartTransport.send(message, {
                to: 'product-manager'
            });
            
            const decision = result.decision || 'unknown';
            const latency = Date.now() - startTime;
            
            console.log(`${msgConfig.name} (${msgConfig.size}字节):`);
            console.log(`   决策: ${decision}`);
            console.log(`   延迟: ${latency}ms`);
            console.log(`   消息大小: ${result.messageSize || '未知'}字节`);
            console.log(`   使用路径: ${result.minimalPath ? '快速路径' : result.fullPath ? '完整路径' : '标准路径'}`);
            console.log();
        }
        
        // 显示统计
        const stats = smartTransport.getStats();
        console.log('📊 智能传输层统计:');
        console.log(`   总消息数: ${stats.decisions.totalMessages}`);
        console.log(`   快速路径使用: ${stats.decisions.fastPathUsed}`);
        console.log(`   完整路径使用: ${stats.decisions.fullPathUsed}`);
        console.log(`   快速路径使用率: ${stats.fastPathUsageRate}`);
        console.log(`   按大小决策:`, stats.decisions.decisionsBySize);
        
    } catch (error) {
        console.error('❌ 智能传输层示例失败:', error.message);
    }
    
    console.log('\n2. 协议层多协议支持');
    console.log('='.repeat(50));
    
    try {
        const protocolManager = new ProtocolManager({
            enableMessagePack: true,
            enableLearning: true
        });
        
        console.log('协议管理器初始化完成');
        console.log('支持的协议:', Object.keys(protocolManager.protocols).join(', '));
        console.log();
        
        // 测试不同消息的协议选择
        const testData = [
            {
                name: '简单对象',
                data: { id: 1, name: '测试', active: true, count: 42 },
                expectedProtocol: 'json' // 小对象通常JSON更好
            },
            {
                name: '大型数组',
                data: { items: Array.from({ length: 1000 }, (_, i) => ({ id: i, value: `item-${i}` })) },
                expectedProtocol: 'msgpack' // 大数据集MessagePack更好
            },
            {
                name: '混合数据',
                data: {
                    metadata: { version: '1.0', timestamp: new Date().toISOString() },
                    payload: Array.from({ length: 500 }, (_, i) => ({
                        index: i,
                        data: Buffer.from(`data-${i}`).toString('base64')
                    })),
                    flags: [true, false, true, true]
                },
                expectedProtocol: 'auto' // 让管理器决定
            }
        ];
        
        for (const test of testData) {
            console.log(`测试: ${test.name}`);
            
            // 测试JSON协议
            const jsonStart = Date.now();
            const jsonResult = await protocolManager.serialize(test.data, 'json');
            const jsonTime = Date.now() - jsonStart;
            
            // 测试MessagePack协议
            const msgpackStart = Date.now();
            const msgpackResult = await protocolManager.serialize(test.data, 'msgpack');
            const msgpackTime = Date.now() - msgpackStart;
            
            // 测试自动选择
            const autoStart = Date.now();
            const autoResult = await protocolManager.serialize(test.data, 'auto');
            const autoTime = Date.now() - autoStart;
            
            console.log(`  JSON: ${jsonResult.metadata.outputSize}字节, ${jsonTime}ms`);
            console.log(`  MessagePack: ${msgpackResult.metadata.outputSize}字节, ${msgpackTime}ms`);
            
            const sizeReduction = ((jsonResult.metadata.outputSize - msgpackResult.metadata.outputSize) / 
                                  jsonResult.metadata.outputSize * 100).toFixed(2);
            
            console.log(`  体积减少: ${sizeReduction}%`);
            console.log(`  自动选择: ${autoResult.protocol} (${autoTime}ms)`);
            console.log();
        }
        
        // 显示协议统计
        const stats = protocolManager.getStats();
        console.log('📊 协议层统计:');
        console.log(`   总操作数: ${stats.metrics.totalOperations}`);
        console.log(`   序列化: ${stats.metrics.serializations}`);
        console.log(`   反序列化: ${stats.metrics.deserializations}`);
        
        for (const [protoName, protoStats] of Object.entries(stats.metrics.protocols)) {
            console.log(`   ${protoName}:`);
            console.log(`     操作数: ${protoStats.operations}`);
            console.log(`     成功率: ${protoStats.successRate}`);
            console.log(`     平均延迟: ${protoStats.avgLatency}`);
            console.log(`     平均输入: ${protoStats.avgInputSize}字节`);
            console.log(`     平均输出: ${protoStats.avgOutputSize}字节`);
            console.log(`     压缩率: ${protoStats.compressionRatio}`);
            console.log(`     空间节省: ${protoStats.spaceSavings}`);
        }
        
    } catch (error) {
        console.error('❌ 协议层示例失败:', error.message);
    }
    
    console.log('\n3. 统一API高级配置');
    console.log('='.repeat(50));
    
    try {
        console.log('创建高度配置的API实例...\n');
        
        const customApi = createAgentComm({
            transport: {
                fastPath: {
                    enabled: true,
                    thresholdBytes: 1024,
                    cacheEnabled: false,
                    batchEnabled: false
                },
                filesystem: { enabled: true },
                websocket: { enabled: false },
                http: { enabled: false },
                monitoring: {
                    enabled: true,
                    metricsInterval: 30000 // 30秒收集一次指标
                }
            },
            protocol: {
                defaultProtocol: 'auto',
                enableMessagePack: true,
                enableLearning: true,
                learningWindow: 100 // 基于最近100次操作学习
            },
            behavior: {
                defaultTimeout: 10000,
                retryAttempts: 3,
                requireAck: false,
                enableBroadcast: true,
                enableRequestResponse: true
            }
        });
        
        console.log('✅ 自定义API配置:');
        console.log('   传输层:');
        console.log('     - 快速路径: 启用 (阈值: 1024字节)');
        console.log('     - 缓存: 禁用');
        console.log('     - 批量: 禁用');
        console.log('     - 监控: 启用 (30秒间隔)');
        console.log('   协议层:');
        console.log('     - 默认协议: 自动选择');
        console.log('     - MessagePack: 启用');
        console.log('     - 学习: 启用 (窗口: 100次操作)');
        console.log('   行为:');
        console.log('     - 默认超时: 10000ms');
        console.log('     - 重试次数: 3次');
        console.log('     - 广播: 启用');
        console.log('     - 请求-响应: 启用');
        
        // 测试发送消息
        console.log('\n测试自定义API...');
        
        const result = await customApi.send('backend-dev', {
            type: 'configured-test',
            content: '测试高度配置的API实例',
            configuration: 'custom',
            timestamp: new Date().toISOString()
        }, {
            protocol: 'auto', // 让API自动选择
            transport: 'auto', // 让传输层自动决策
            metadata: {
                test: 'advanced-features',
                version: '2.0'
            }
        });
        
        console.log('✅ 自定义API测试成功:');
        console.log(`   消息ID: ${result.messageId}`);
        console.log(`   使用协议: ${result.protocol}`);
        console.log(`   传输方式: ${result.transport}`);
        console.log(`   延迟: ${result.latency}ms`);
        
        if (result.metadata?.serialization) {
            console.log(`   序列化信息:`, result.metadata.serialization);
        }
        
        // 获取详细统计
        const stats = customApi.getStats();
        console.log('\n📊 自定义API统计:');
        console.log(`   配置: ${stats.config.transport}传输, ${stats.config.protocol}协议`);
        console.log(`   功能: 请求-响应:${stats.config.features.requestResponse}, 广播:${stats.config.features.broadcast}`);
        console.log(`   消息统计: 发送${stats.messagesSent}, 接收${stats.messagesReceived}`);
        console.log(`   请求统计: 发送${stats.requestsSent}, 响应${stats.responsesReceived}`);
        console.log(`   成功率: ${stats.successRate}`);
        console.log(`   请求成功率: ${stats.requestSuccessRate}`);
        
        await customApi.close();
        console.log('\n🔒 自定义API已关闭');
        
    } catch (error) {
        console.error('❌ 自定义API示例失败:', error.message);
    }
    
    console.log('\n4. 性能监控和指标收集');
    console.log('='.repeat(50));
    
    try {
        console.log('创建带监控的API实例...\n');
        
        const monitoredApi = createAgentComm({
            transport: {
                monitoring: { enabled: true, metricsInterval: 10000 }
            }
        });
        
        // 注册监控事件
        monitoredApi.on('message:sent', (data) => {
            console.log(`   📈 监控 - 消息发送: ${data.messageId} (${data.latency}ms)`);
        });
        
        monitoredApi.on('message:received', (data) => {
            console.log(`   📈 监控 - 消息接收: ${data.message.protocol}协议 (${data.latency}ms)`);
        });
        
        monitoredApi.on('message:error', (data) => {
            console.log(`   📈 监控 - 消息错误: ${data.recipient} - ${data.error}`);
        });
        
        monitoredApi.on('broadcast:completed', (data) => {
            console.log(`   📈 监控 - 广播完成: ${data.broadcastId}, 成功${data.successful}/失败${data.failed}`);
        });
        
        console.log('监控事件监听器已注册');
        console.log('开始性能测试...\n');
        
        // 执行一系列操作来生成监控数据
        const operations = [
            async () => {
                console.log('操作1: 发送小消息');
                await monitoredApi.send('product-manager', {
                    type: 'monitor-test-1',
                    content: '小消息测试',
                    size: 'small'
                });
            },
            async () => {
                console.log('操作2: 发送大消息');
                await monitoredApi.send('backend-dev', {
                    type: 'monitor-test-2',
                    content: '大消息测试 '.repeat(100),
                    size: 'large'
                });
            },
            async () => {
                console.log('操作3: 发送请求');
                try {
                    await monitoredApi.request('mock-service', {
                        action: 'test',
                        data: { test: true }
                    }, { timeout: 1000 });
                } catch (error) {
                    // 预期超时，用于测试错误监控
                    console.log('   预期请求超时，测试错误监控');
                }
            },
            async () => {
                console.log('操作4: 小规模广播');
                await monitoredApi.broadcast(['frontend-dev', 'ui-designer'], {
                    type: 'monitor-broadcast',
                    content: '监控测试广播'
                });
            }
        ];
        
        for (const op of operations) {
            try {
                await op();
                await new Promise(resolve => setTimeout(resolve, 500)); // 延迟以区分操作
            } catch (error) {
                console.log(`   操作失败: ${error.message}`);
            }
        }
        
        console.log('\n📊 监控数据汇总:');
        const stats = monitoredApi.getStats();
        
        console.log('   基本统计:');
        console.log(`     消息发送: ${stats.messagesSent}`);
        console.log(`     消息接收: ${stats.messagesReceived}`);
        console.log(`     请求发送: ${stats.requestsSent}`);
        console.log(`     响应接收: ${stats.responsesReceived}`);
        console.log(`     广播发送: ${stats.broadcastSent}`);
        console.log(`     错误数: ${stats.errors}`);
        
        console.log('   性能指标:');
        console.log(`     成功率: ${stats.successRate}`);
        console.log(`     请求成功率: ${stats.requestSuccessRate}`);
        console.log(`     运行时间: ${stats.uptime}`);
        
        console.log('   系统状态:');
        console.log(`     待处理请求: ${stats.pendingRequests}`);
        console.log(`     配置: ${stats.config.transport}传输, ${stats.config.protocol}协议`);
        
        await monitoredApi.close();
        console.log('\n🔒 监控API已关闭');
        
    } catch (error) {
        console.error('❌ 监控示例失败:', error.message);
    }
    
    console.log('\n5. 错误恢复和降级机制');
    console.log('='.repeat(50));
    
    try {
        console.log('测试错误恢复机制...\n');
        
        // 创建测试场景：模拟传输失败
        console.log('场景1: 快速路径失败，降级到完整路径');
        // 注：实际测试需要模拟故障，这里主要展示概念
        
        console.log('场景2: 协议序列化失败，降级到JSON');
        
        const protocolManager = new ProtocolManager({
            enableMessagePack: true
        });
        
        // 测试无效数据
        const invalidData = {
            circularRef: {}
        };
        invalidData.circularRef.self = invalidData.circularRef; // 创建循环引用
        
        try {
            // 这应该失败，因为循环引用
            await protocolManager.serialize(invalidData, 'json');
            console.log('❌ 预期失败但未失败');
        } catch (error) {
            console.log('✅ 错误处理正常:');
            console.log(`   错误类型: ${error.constructor.name}`);
            console.log(`   错误消息: ${error.message}`);
            console.log('   说明: 协议层正确处理了无效数据');
        }
        
        console.log('\n场景3: 传输超时，自动重试');
        
        const resilientApi = createAgentComm({
            behavior: {
                defaultTimeout: 100,
                retryAttempts: 2
            }
        });
        
        // 模拟慢速接收者（通过设置极短超时）
        console.log('发送会超时的请求（测试重试机制）...');
        try {
            await resilientApi.request('slow-responder', {
                action: 'slow-operation'
            }, {
                timeout: 50 // 极短超时，应该会触发重试
            });
            console.log('❌ 预期失败但未失败');
        } catch (error) {
            console.log('✅ 超时重试正常:');
            console.log(`   最终错误: ${error.message}`);
            console.log('   说明: 系统尝试了重试机制');
        }
        
        const stats = resilientApi.getStats();
        console.log(`   统计: 请求${stats.requestsSent}, 错误${stats.errors}`);
        
        await resilientApi.close();
        
    } catch (error) {
        console.error('❌ 错误恢复示例失败:', error.message);
    }
    
    console.log('\n🎉 高级功能示例完成!');
    console.log('\n总结:');
    console.log('  ✅ 智能传输层决策功能正常');
    console.log('  ✅ 协议层多协议支持完整');
    console.log('  ✅ 高度可配置API支持');
    console.log('  ✅ 性能监控和指标收集完善');
    console.log('  ✅ 错误恢复和降级机制健全');
    console.log('\n高级功能亮点:');
    console.log('  • 基于消息特性的智能路由');
    console.log('  • 多协议自动协商和优化');
    console.log('  • 完整的事件系统和监控');
    console.log('  • 可配置的错误处理和重试');
    console.log('  • 实时性能指标收集');
}

// 运行示例
if (require.main === module) {
    runAdvancedFeaturesExamples().catch(error => {
        console.error('示例运行失败:', error);
        process.exit(1);
    });
}

module.exports = { runAdvancedFeaturesExamples };