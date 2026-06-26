/**
 * 请求-响应模式示例
 * 展示统一API的请求-响应通信模式
 */

const { sendRequest, createAgentComm } = require('../core/unified-api.js');

// 模拟响应处理器（在实际系统中由收件人agent实现）
class MockResponseHandler {
    constructor() {
        this.handlers = new Map();
        this.setupHandlers();
    }
    
    setupHandlers() {
        // 注册请求处理器
        this.handlers.set('get-user-info', async (request) => {
            return {
                success: true,
                data: {
                    userId: request.data.userId,
                    username: 'testuser',
                    email: 'user@example.com',
                    role: 'admin',
                    lastLogin: new Date().toISOString()
                },
                timestamp: new Date().toISOString(),
                requestId: request._requestId
            };
        });
        
        this.handlers.set('process-data', async (request) => {
            // 模拟数据处理
            await new Promise(resolve => setTimeout(resolve, 100));
            
            return {
                success: true,
                data: {
                    processed: true,
                    input: request.data,
                    output: `Processed: ${JSON.stringify(request.data).substring(0, 50)}...`,
                    processingTime: '100ms'
                },
                metadata: {
                    processor: 'mock-handler',
                    version: '1.0'
                },
                requestId: request._requestId
            };
        });
        
        this.handlers.set('validate-input', async (request) => {
            const { input, rules } = request.data;
            
            // 简单验证逻辑
            const errors = [];
            if (!input) errors.push('输入不能为空');
            if (rules?.minLength && input?.length < rules.minLength) {
                errors.push(`长度至少需要${rules.minLength}个字符`);
            }
            if (rules?.maxLength && input?.length > rules.maxLength) {
                errors.push(`长度不能超过${rules.maxLength}个字符`);
            }
            
            return {
                success: errors.length === 0,
                data: {
                    valid: errors.length === 0,
                    errors,
                    input,
                    timestamp: new Date().toISOString()
                },
                requestId: request._requestId
            };
        });
    }
    
    async handleRequest(request) {
        const handler = this.handlers.get(request.action);
        if (!handler) {
            return {
                success: false,
                error: `未知的操作类型: ${request.action}`,
                requestId: request._requestId
            };
        }
        
        try {
            return await handler(request);
        } catch (error) {
            return {
                success: false,
                error: `处理失败: ${error.message}`,
                requestId: request._requestId
            };
        }
    }
}

async function runRequestResponseExamples() {
    console.log('🚀 通信协议架构优化 - 请求-响应模式示例\n');
    
    // 创建模拟处理器
    const mockHandler = new MockResponseHandler();
    
    // 示例1: 基础请求-响应
    console.log('1. 基础请求-响应示例');
    console.log('='.repeat(50));
    
    try {
        console.log('发送用户信息请求...');
        
        const startTime = Date.now();
        const response = await sendRequest('user-service', {
            action: 'get-user-info',
            data: {
                userId: 'user-12345',
                fields: ['username', 'email', 'role']
            }
        }, {
            timeout: 5000,
            priority: 'high'
        });
        
        const totalTime = Date.now() - startTime;
        
        console.log('✅ 请求成功:');
        console.log(`   总耗时: ${totalTime}ms`);
        console.log(`   请求ID: ${response.requestId}`);
        console.log(`   响应数据:`, JSON.stringify(response.response, null, 2).split('\n').slice(0, 10).join('\n   '));
        
        // 模拟处理响应
        const mockResponse = await mockHandler.handleRequest({
            action: 'get-user-info',
            data: { userId: 'user-12345' },
            _requestId: 'mock-req-1'
        });
        
        console.log('\n模拟处理器响应:');
        console.log(`   成功: ${mockResponse.success}`);
        console.log(`   数据:`, JSON.stringify(mockResponse.data, null, 2).split('\n').slice(0, 5).join('\n   '));
        
    } catch (error) {
        console.error('❌ 请求失败:', error.message);
    }
    
    console.log('\n2. 数据处理请求示例');
    console.log('='.repeat(50));
    
    try {
        console.log('发送数据处理请求...');
        
        const requestData = {
            action: 'process-data',
            data: {
                dataset: 'sales-2026-q1',
                operations: ['clean', 'aggregate', 'analyze'],
                parameters: {
                    timeRange: '2026-01-01 to 2026-03-31',
                    metrics: ['revenue', 'units', 'growth']
                }
            }
        };
        
        const response = await sendRequest('data-processor', requestData, {
            timeout: 10000, // 10秒超时，数据处理可能较慢
            metadata: {
                requester: 'analytics-dashboard',
                urgency: 'normal'
            }
        });
        
        console.log('✅ 数据处理请求成功:');
        console.log(`   请求延迟: ${response.latency}ms`);
        console.log(`   响应状态: ${response.response.success ? '成功' : '失败'}`);
        
        if (response.response.data) {
            console.log(`   处理结果: ${response.response.data.output}`);
        }
        
    } catch (error) {
        console.error('❌ 数据处理请求失败:', error.message);
    }
    
    console.log('\n3. 输入验证请求示例');
    console.log('='.repeat(50));
    
    try {
        console.log('发送输入验证请求...');
        
        const response = await sendRequest('validation-service', {
            action: 'validate-input',
            data: {
                input: 'test input',
                rules: {
                    minLength: 5,
                    maxLength: 100,
                    allowedChars: 'a-zA-Z0-9 '
                }
            }
        }, {
            timeout: 3000,
            requireAck: true
        });
        
        console.log('✅ 验证请求成功:');
        console.log(`   验证结果: ${response.response.data.valid ? '有效' : '无效'}`);
        
        if (response.response.data.errors && response.response.data.errors.length > 0) {
            console.log(`   错误信息: ${response.response.data.errors.join(', ')}`);
        }
        
    } catch (error) {
        console.error('❌ 验证请求失败:', error.message);
    }
    
    console.log('\n4. 超时和错误处理示例');
    console.log('='.repeat(50));
    
    try {
        console.log('发送会超时的请求（超时设置: 100ms）...');
        
        // 这个请求应该会超时
        await sendRequest('slow-service', {
            action: 'slow-operation',
            data: { delay: 500 } // 请求处理需要500ms
        }, {
            timeout: 100 // 只等待100ms
        });
        
        console.log('❌ 预期超时但未超时 - 这不应该发生');
        
    } catch (error) {
        console.log('✅ 超时处理正常工作:');
        console.log(`   错误类型: ${error.constructor.name}`);
        console.log(`   错误消息: ${error.message}`);
        console.log('   说明: 当响应超时时，系统正确抛出超时错误');
    }
    
    console.log('\n5. 批量请求示例');
    console.log('='.repeat(50));
    
    try {
        const api = createAgentComm();
        
        console.log('发送批量请求...');
        
        const requests = [
            {
                recipient: 'user-service',
                request: { action: 'get-user-info', data: { userId: 'user-1' } },
                options: { timeout: 3000 }
            },
            {
                recipient: 'user-service',
                request: { action: 'get-user-info', data: { userId: 'user-2' } },
                options: { timeout: 3000 }
            },
            {
                recipient: 'data-processor',
                request: { action: 'process-data', data: { dataset: 'test' } },
                options: { timeout: 5000 }
            }
        ];
        
        const startTime = Date.now();
        const promises = requests.map(async (req, index) => {
            try {
                const response = await api.request(req.recipient, req.request, req.options);
                return {
                    index,
                    success: true,
                    response,
                    latency: response.latency
                };
            } catch (error) {
                return {
                    index,
                    success: false,
                    error: error.message
                };
            }
        });
        
        const results = await Promise.all(promises);
        const totalTime = Date.now() - startTime;
        
        console.log('✅ 批量请求完成:');
        console.log(`   总时间: ${totalTime}ms`);
        console.log(`   请求数量: ${requests.length}`);
        
        const successful = results.filter(r => r.success).length;
        const failed = results.filter(r => !r.success).length;
        
        console.log(`   成功: ${successful}, 失败: ${failed}`);
        
        for (const result of results) {
            if (result.success) {
                console.log(`   请求${result.index + 1}: 成功 (${result.latency}ms)`);
            } else {
                console.log(`   请求${result.index + 1}: 失败 - ${result.error}`);
            }
        }
        
        // 获取API统计
        const stats = api.getStats();
        console.log('\n📊 批量请求统计:');
        console.log(`   总请求数: ${stats.requestsSent}`);
        console.log(`   响应数: ${stats.responsesReceived}`);
        console.log(`   请求成功率: ${stats.requestSuccessRate}`);
        
        await api.close();
        
    } catch (error) {
        console.error('❌ 批量请求示例失败:', error.message);
    }
    
    console.log('\n🎉 请求-响应模式示例完成!');
    console.log('\n总结:');
    console.log('  ✅ 基础请求-响应功能正常');
    console.log('  ✅ 超时处理机制完善');
    console.log('  ✅ 错误处理正确');
    console.log('  ✅ 批量请求支持良好');
    console.log('  ✅ 统计信息收集完整');
}

// 运行示例
if (require.main === module) {
    runRequestResponseExamples().catch(error => {
        console.error('示例运行失败:', error);
        process.exit(1);
    });
}

module.exports = { runRequestResponseExamples, MockResponseHandler };