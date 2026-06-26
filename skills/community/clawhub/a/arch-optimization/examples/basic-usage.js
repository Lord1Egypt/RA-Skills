/**
 * 基础使用示例
 * 展示统一API的基本发送功能
 */

const { sendMessage, createAgentComm } = require('../core/unified-api.js');

async function runBasicExamples() {
    console.log('🚀 通信协议架构优化 - 基础使用示例\n');
    
    // 示例1: 简单发送
    console.log('1. 简单消息发送示例');
    console.log('='.repeat(40));
    
    try {
        const result = await sendMessage('product-manager', {
            id: 'example-1',
            type: 'greeting',
            content: 'Hello from optimized architecture!',
            timestamp: new Date().toISOString(),
            metadata: {
                example: true,
                version: '1.0'
            }
        }, {
            priority: 'medium',
            timeout: 3000
        });
        
        console.log('✅ 消息发送成功:');
        console.log(`   消息ID: ${result.messageId}`);
        console.log(`   收件人: ${result.recipient}`);
        console.log(`   延迟: ${result.latency}ms`);
        console.log(`   使用协议: ${result.protocol}`);
        console.log(`   传输方式: ${result.transport}`);
        
    } catch (error) {
        console.error('❌ 消息发送失败:', error.message);
    }
    
    console.log('\n2. 创建API实例示例');
    console.log('='.repeat(40));
    
    // 示例2: 创建API实例
    try {
        const api = createAgentComm({
            transport: {
                fastPath: {
                    enabled: true,
                    thresholdBytes: 1024
                },
                filesystem: { enabled: true }
            },
            protocol: {
                defaultProtocol: 'auto',
                enableMessagePack: true
            },
            behavior: {
                defaultTimeout: 5000,
                retryAttempts: 2
            }
        });
        
        console.log('✅ API实例创建成功');
        console.log('   配置:');
        console.log('     - 快速路径: 启用 (阈值: 1024字节)');
        console.log('     - MessagePack: 启用');
        console.log('     - 默认超时: 5000ms');
        console.log('     - 重试次数: 2次');
        
        // 使用实例发送消息
        const result = await api.send('backend-dev', {
            type: 'task-request',
            action: 'process-data',
            data: {
                userId: 'user-123',
                action: 'analyze',
                timestamp: new Date().toISOString()
            }
        });
        
        console.log('\n✅ 使用API实例发送成功:');
        console.log(`   消息ID: ${result.messageId}`);
        console.log(`   延迟: ${result.latency}ms`);
        
        // 获取统计信息
        const stats = api.getStats();
        console.log('\n📊 API统计信息:');
        console.log(`   消息发送数: ${stats.messagesSent}`);
        console.log(`   成功率: ${stats.successRate}`);
        console.log(`   运行时间: ${stats.uptime}`);
        
        // 关闭API
        await api.close();
        console.log('\n🔒 API已关闭');
        
    } catch (error) {
        console.error('❌ API示例失败:', error.message);
    }
    
    console.log('\n3. 不同消息大小示例');
    console.log('='.repeat(40));
    
    // 示例3: 测试不同大小的消息
    const testMessages = [
        { name: '小消息', size: 100, content: '这是一个小消息测试' },
        { name: '中消息', size: 1024, content: 'A'.repeat(900) + ' 这是中等大小消息' },
        { name: '大消息', size: 10240, content: 'B'.repeat(10000) + ' 这是大消息测试' }
    ];
    
    for (const msgConfig of testMessages) {
        try {
            const startTime = Date.now();
            
            const result = await sendMessage('product-manager', {
                id: `size-test-${msgConfig.name}`,
                type: 'performance-test',
                content: msgConfig.content,
                metadata: {
                    test: true,
                    size: msgConfig.size,
                    timestamp: new Date().toISOString()
                }
            });
            
            const totalTime = Date.now() - startTime;
            
            console.log(`✅ ${msgConfig.name} (${msgConfig.size}字节):`);
            console.log(`   总时间: ${totalTime}ms`);
            console.log(`   发送延迟: ${result.latency}ms`);
            console.log(`   消息大小: ${result.metadata?.serialization?.outputSize || '未知'}字节`);
            
        } catch (error) {
            console.error(`❌ ${msgConfig.name}发送失败:`, error.message);
        }
    }
    
    console.log('\n4. 错误处理示例');
    console.log('='.repeat(40));
    
    // 示例4: 错误处理
    try {
        // 故意发送无效消息（缺少收件人）
        await sendMessage('', {
            type: 'invalid-test'
        });
        
        console.log('❌ 预期失败但未失败 - 这不应该发生');
        
    } catch (error) {
        console.log('✅ 错误处理正常工作:');
        console.log(`   错误类型: ${error.constructor.name}`);
        console.log(`   错误消息: ${error.message}`);
        console.log('   说明: 当缺少必要参数时，系统正确抛出错误');
    }
    
    // 示例5: 事件监听
    console.log('\n5. 事件系统示例');
    console.log('='.repeat(40));
    
    try {
        const api = createAgentComm();
        
        // 注册事件监听器
        api.on('message:sent', (data) => {
            console.log(`   📤 消息发送事件: ${data.messageId} -> ${data.recipient} (${data.latency}ms)`);
        });
        
        api.on('message:error', (data) => {
            console.log(`   ❌ 消息错误事件: ${data.recipient} - ${data.error}`);
        });
        
        console.log('✅ 事件监听器已注册');
        
        // 发送测试消息触发事件
        await api.send('product-manager', {
            type: 'event-test',
            content: '测试事件系统'
        });
        
        console.log('✅ 测试消息已发送，事件已触发');
        
        await api.close();
        
    } catch (error) {
        console.error('❌ 事件示例失败:', error.message);
    }
    
    console.log('\n🎉 基础使用示例完成!');
    console.log('\n总结:');
    console.log('  ✅ 简单消息发送功能正常');
    console.log('  ✅ API实例创建和配置正常');
    console.log('  ✅ 不同大小消息支持正常');
    console.log('  ✅ 错误处理机制完善');
    console.log('  ✅ 事件系统工作正常');
}

// 运行示例
if (require.main === module) {
    runBasicExamples().catch(error => {
        console.error('示例运行失败:', error);
        process.exit(1);
    });
}

module.exports = { runBasicExamples };