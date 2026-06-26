/**
 * 广播模式示例
 * 展示统一API的广播通信功能
 */

const { broadcastMessage, createAgentComm } = require('../core/unified-api.js');

async function runBroadcastExamples() {
    console.log('🚀 通信协议架构优化 - 广播模式示例\n');
    
    // 定义测试收件人列表
    const testRecipients = [
        'product-manager',
        'frontend-dev',
        'backend-dev',
        'ui-designer',
        'qa-engineer',
        'data-analyst',
        'sys-admin'
    ];
    
    console.log(`测试收件人列表: ${testRecipients.join(', ')}`);
    console.log(`收件人数量: ${testRecipients.length}\n`);
    
    // 示例1: 基础广播
    console.log('1. 基础广播示例');
    console.log('='.repeat(50));
    
    try {
        console.log('发送系统通知广播...');
        
        const startTime = Date.now();
        const result = await broadcastMessage(testRecipients, {
            id: 'broadcast-system-notification',
            type: 'system-notification',
            title: '系统维护通知',
            content: '系统将于今晚23:00进行维护，预计持续2小时。请提前保存工作。',
            severity: 'info',
            timestamp: new Date().toISOString(),
            metadata: {
                sender: 'system-admin',
                broadcast: true,
                expiry: '2026-03-22T01:00:00Z'
            }
        }, {
            priority: 'medium',
            timeout: 10000
        });
        
        const totalTime = Date.now() - startTime;
        
        console.log('✅ 广播发送成功:');
        console.log(`   广播ID: ${result.broadcastId}`);
        console.log(`   总收件人: ${result.totalRecipients}`);
        console.log(`   成功发送: ${result.successful}`);
        console.log(`   发送失败: ${result.failed}`);
        console.log(`   总耗时: ${totalTime}ms`);
        console.log(`   平均每人耗时: ${(totalTime / result.totalRecipients).toFixed(2)}ms`);
        
        // 显示详细结果
        if (result.failed > 0) {
            console.log('\n   失败详情:');
            const failedResults = result.results.filter(r => !r.success);
            for (const failed of failedResults.slice(0, 3)) { // 只显示前3个失败
                console.log(`     - ${failed.recipient}: ${failed.error}`);
            }
            if (failedResults.length > 3) {
                console.log(`     ... 还有${failedResults.length - 3}个失败`);
            }
        }
        
    } catch (error) {
        console.error('❌ 广播失败:', error.message);
    }
    
    console.log('\n2. 紧急广播示例');
    console.log('='.repeat(50));
    
    try {
        console.log('发送紧急警报广播...');
        
        // 紧急广播只发送给关键人员
        const urgentRecipients = ['product-manager', 'backend-dev', 'sys-admin'];
        
        const result = await broadcastMessage(urgentRecipients, {
            type: 'emergency-alert',
            title: '🚨 紧急: 系统异常检测',
            content: '检测到数据库连接异常，请立即检查系统状态。',
            severity: 'critical',
            timestamp: new Date().toISOString(),
            actionRequired: true,
            metadata: {
                alertCode: 'DB-CONN-ERROR',
                detectedAt: new Date().toISOString(),
                suggestedAction: '检查数据库连接和服务状态'
            }
        }, {
            priority: 'high', // 高优先级
            timeout: 5000,
            requireAck: true,
            metadata: {
                emergency: true,
                escalation: 'immediate'
            }
        });
        
        console.log('✅ 紧急广播发送成功:');
        console.log(`   广播ID: ${result.broadcastId}`);
        console.log(`   收件人: ${urgentRecipients.join(', ')}`);
        console.log(`   成功: ${result.successful}/${result.totalRecipients}`);
        
        if (result.failed > 0) {
            console.log(`   ⚠️  有${result.failed}个收件人失败，可能需要人工通知`);
        }
        
    } catch (error) {
        console.error('❌ 紧急广播失败:', error.message);
    }
    
    console.log('\n3. 选择性广播示例');
    console.log('='.repeat(50));
    
    try {
        console.log('根据角色选择性广播...');
        
        // 按角色分组
        const roleGroups = {
            developers: ['frontend-dev', 'backend-dev'],
            designers: ['ui-designer'],
            managers: ['product-manager'],
            testers: ['qa-engineer']
        };
        
        // 发送给开发团队
        const devResult = await broadcastMessage(roleGroups.developers, {
            type: 'team-update',
            title: '开发团队更新',
            content: '本周冲刺目标已完成90%，代码审查会议定于明天10:00。',
            team: 'development',
            timestamp: new Date().toISOString()
        }, {
            priority: 'normal'
        });
        
        // 发送给设计团队
        const designResult = await broadcastMessage(roleGroups.designers, {
            type: 'design-review',
            title: '设计评审通知',
            content: '新UI设计已准备好评审，请准备反馈意见。',
            team: 'design',
            timestamp: new Date().toISOString()
        });
        
        console.log('✅ 选择性广播完成:');
        console.log(`   开发团队: ${devResult.successful}/${devResult.totalRecipients} 成功`);
        console.log(`   设计团队: ${designResult.successful}/${designResult.totalRecipients} 成功`);
        
    } catch (error) {
        console.error('❌ 选择性广播失败:', error.message);
    }
    
    console.log('\n4. 大规模广播性能测试');
    console.log('='.repeat(50));
    
    try {
        const api = createAgentComm();
        
        // 创建大规模收件人列表（模拟）
        const largeRecipientList = [];
        for (let i = 1; i <= 20; i++) {
            largeRecipientList.push(`agent-${i}`);
        }
        
        console.log(`测试大规模广播: ${largeRecipientList.length} 个收件人`);
        console.log('开始测试...');
        
        const startTime = Date.now();
        const result = await api.broadcast(largeRecipientList, {
            type: 'mass-notification',
            title: '月度报告提醒',
            content: '请在本周五前提交月度工作报告。',
            importance: 'normal',
            timestamp: new Date().toISOString()
        }, {
            priority: 'low', // 低优先级，避免影响系统
            timeout: 15000 // 15秒超时
        });
        
        const totalTime = Date.now() - startTime;
        
        console.log('✅ 大规模广播完成:');
        console.log(`   总收件人: ${result.totalRecipients}`);
        console.log(`   成功: ${result.successful}`);
        console.log(`   失败: ${result.failed}`);
        console.log(`   总耗时: ${totalTime}ms`);
        console.log(`   吞吐量: ${(result.totalRecipients / (totalTime / 1000)).toFixed(2)} 消息/秒`);
        console.log(`   成功率: ${((result.successful / result.totalRecipients) * 100).toFixed(2)}%`);
        
        // 性能分析
        if (result.successful > 0) {
            const avgPerRecipient = totalTime / result.successful;
            console.log(`   平均每人耗时: ${avgPerRecipient.toFixed(2)}ms`);
            
            if (avgPerRecipient < 100) {
                console.log(`   🟢 性能优秀: 平均延迟 < 100ms`);
            } else if (avgPerRecipient < 500) {
                console.log(`   🟡 性能良好: 平均延迟 < 500ms`);
            } else {
                console.log(`   🔴 性能需优化: 平均延迟 ≥ 500ms`);
            }
        }
        
        // 获取API统计
        const stats = api.getStats();
        console.log('\n📊 广播统计信息:');
        console.log(`   广播发送次数: ${stats.broadcastSent}`);
        console.log(`   总消息发送数: ${stats.messagesSent}`);
        console.log(`   成功率: ${stats.successRate}`);
        
        await api.close();
        
    } catch (error) {
        console.error('❌ 大规模广播测试失败:', error.message);
    }
    
    console.log('\n5. 广播错误处理示例');
    console.log('='.repeat(50));
    
    try {
        console.log('测试包含无效收件人的广播...');
        
        // 包含一些无效收件人
        const mixedRecipients = [
            'valid-agent-1',
            'valid-agent-2',
            '', // 空收件人
            'valid-agent-3',
            null, // null收件人
            'valid-agent-4'
        ].filter(Boolean); // 过滤掉空值
        
        const result = await broadcastMessage(mixedRecipients, {
            type: 'test-broadcast',
            content: '测试错误处理'
        });
        
        console.log('✅ 广播完成（包含错误处理）:');
        console.log(`   有效收件人: ${result.totalRecipients}`);
        console.log(`   成功: ${result.successful}`);
        console.log(`   失败: ${result.failed}`);
        
        // 测试空收件人列表
        console.log('\n测试空收件人列表...');
        try {
            await broadcastMessage([], {
                type: 'empty-test',
                content: '这应该失败'
            });
            console.log('❌ 预期失败但未失败');
        } catch (error) {
            console.log('✅ 空收件人列表正确处理:');
            console.log(`   错误消息: ${error.message}`);
        }
        
    } catch (error) {
        console.error('❌ 广播错误处理测试失败:', error.message);
    }
    
    console.log('\n6. 广播事件监听示例');
    console.log('='.repeat(50));
    
    try {
        const api = createAgentComm();
        
        // 注册事件监听器
        api.on('broadcast:completed', (data) => {
            console.log(`   📢 广播完成事件: ${data.broadcastId}`);
            console.log(`       收件人: ${data.recipients.length}`);
            console.log(`       成功: ${data.successful}, 失败: ${data.failed}`);
            console.log(`       总耗时: ${data.totalLatency}ms`);
        });
        
        api.on('message:sent', (data) => {
            // 在实际使用中，这里可能会有很多事件
            // 我们只记录第一个作为示例
            if (data.recipient === testRecipients[0]) {
                console.log(`   📤 第一个消息发送事件: ${data.messageId} (${data.latency}ms)`);
            }
        });
        
        console.log('事件监听器已注册，发送测试广播...');
        
        const result = await api.broadcast(testRecipients.slice(0, 3), {
            type: 'event-test',
            content: '测试广播事件系统'
        });
        
        console.log('✅ 广播完成，事件已触发');
        console.log(`   广播ID: ${result.broadcastId}`);
        
        await api.close();
        
    } catch (error) {
        console.error('❌ 广播事件示例失败:', error.message);
    }
    
    console.log('\n🎉 广播模式示例完成!');
    console.log('\n总结:');
    console.log('  ✅ 基础广播功能正常');
    console.log('  ✅ 紧急广播支持高优先级');
    console.log('  ✅ 选择性广播支持灵活分组');
    console.log('  ✅ 大规模广播性能可接受');
    console.log('  ✅ 错误处理机制完善');
    console.log('  ✅ 事件系统支持广播事件');
    console.log('\n建议使用场景:');
    console.log('  • 系统通知和公告');
    console.log('  • 团队更新和协调');
    console.log('  • 紧急警报和事件通知');
    console.log('  • 批量任务分配');
}

// 运行示例
if (require.main === module) {
    runBroadcastExamples().catch(error => {
        console.error('示例运行失败:', error);
        process.exit(1);
    });
}

module.exports = { runBroadcastExamples };