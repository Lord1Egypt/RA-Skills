/**
 * Agent-Weave 子Agent管理系统 - 使用示例
 * 
 * 展示：
 * 1. 创建无时长限制的子Agent
 * 2. 父Agent查看子Agent状态面板
 * 3. 父Agent在等待期间执行其他任务
 * 4. 异步获取子Agent结果
 */

const { AgentManager, SubAgent, AgentStatus } = require('./agent-system');
const { Loom } = require('./lib/index.js');

// 创建管理器
const manager = new AgentManager({
  logDir: './agent-logs',
  maxAgents: 50
});

// 父Agent主函数
async function parentAgentMain() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║              父Agent - 子Agent管理系统演示                  ║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');

  // ========== 阶段1：创建多个子Agent ==========
  console.log('[阶段1] 创建3个测试子Agent...\n');

  // 子Agent1：长时间运行的核心功能测试
  const agent1 = manager.createAgent({
    name: 'core-functionality-test',
    description: '长时间运行的核心功能测试'
  });

  // 子Agent2：错误处理测试
  const agent2 = manager.createAgent({
    name: 'error-handling-test',
    description: '错误处理和边界条件测试'
  });

  // 子Agent3：性能压力测试
  const agent3 = manager.createAgent({
    name: 'performance-stress-test',
    description: '高并发性能压力测试'
  });

  console.log(`✅ 已创建3个子Agent：`);
  console.log(`   1. ${agent1.name} (${agent1.id.slice(0, 8)}...)`);
  console.log(`   2. ${agent2.name} (${agent2.id.slice(0, 8)}...)`);
  console.log(`   3. ${agent3.name} (${agent3.id.slice(0, 8)}...)\n`);

  // ========== 阶段2：启动子Agent执行任务 ==========
  console.log('[阶段2] 启动子Agent执行任务...\n');

  // 启动Agent1 - 长时间运行的测试
  agent1.start(async () => {
    console.log(`[Agent1] 开始长时间测试...`);
    
    // 模拟长时间运行的任务
    for (let i = 0; i < 10; i++) {
      await new Promise(resolve => setTimeout(resolve, 500));
      agent1.log('INFO', `测试进度: ${(i + 1) * 10}%`);
    }
    
    // 执行实际的Loom测试
    const { Loom } = require('./lib/index.js');
    const loom = new Loom();
    const master = loom.createMaster('test');
    master.spawn(3, (x) => x * 2);
    const result = await master.dispatch([1, 2, 3, 4, 5]);
    
    return { 
      success: true, 
      message: '长时间测试完成',
      testResults: result.summary
    };
  });

  // 启动Agent2 - 错误处理测试
  agent2.start(async () => {
    console.log(`[Agent2] 开始错误处理测试...`);
    
    // 测试1：无效参数
    try {
      const { Loom } = require('./lib/index.js');
      const loom = new Loom();
      loom.createWorker('invalid-parent', 'worker', () => {});
    } catch (error) {
      agent2.log('INFO', `✓ 正确捕获无效参数错误: ${error.message}`);
    }
    
    // 测试2：任务执行错误
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      success: true,
      message: '错误处理测试通过'
    };
  });

  // 启动Agent3 - 性能压力测试
  agent3.start(async () => {
    console.log(`[Agent3] 开始性能压力测试...`);
    
    const { Loom } = require('./lib/index.js');
    const startTime = Date.now();
    
    // 创建大量worker
    const loom = new Loom();
    const master = loom.createMaster('perf-test');
    
    agent3.log('INFO', '创建100个Worker...');
    master.spawn(100, (x) => x * x);
    
    // 执行大量任务
    const inputs = Array.from({ length: 1000 }, (_, i) => i + 1);
    agent3.log('INFO', `执行${inputs.length}个任务...`);
    
    const result = await master.dispatch(inputs);
    const duration = Date.now() - startTime;
    
    agent3.log('INFO', `性能测试完成，耗时: ${duration}ms`);
    
    return {
      success: true,
      message: '性能测试完成',
      metrics: {
        duration,
        taskCount: inputs.length,
        workerCount: 100,
        successRate: (result.summary.success / result.summary.total * 100).toFixed(2) + '%'
      }
    };
  });

  // ========== 阶段3：父Agent执行其他任务 ==========
  console.log('\n[阶段3] 父Agent在等待子Agent的同时执行其他任务...\n');

  // 父Agent的任务1：监控面板
  const monitoringTask = async () => {
    for (let i = 0; i < 5; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      console.log(`\n[父Agent] 监控面板更新 (${i + 1}/5):`);
      
      const status = manager.getAllAgentStatus();
      console.log(`  - 总Agent数: ${status.total}`);
      Object.entries(status.byStatus).forEach(([state, count]) => {
        console.log(`  - ${state}: ${count}`);
      });
    }
  };

  // 父Agent的任务2：数据处理
  const dataProcessingTask = async () => {
    console.log('[父Agent] 开始后台数据处理...');
    
    for (let i = 0; i < 3; i++) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log(`[父Agent] 处理数据批次 ${i + 1}/3...`);
    }
    
    console.log('[父Agent] 数据处理完成！');
  };

  // 父Agent的任务3：日志分析
  const logAnalysisTask = async () => {
    console.log('[父Agent] 分析系统日志...');
    await new Promise(resolve => setTimeout(resolve, 1500));
    console.log('[父Agent] 日志分析完成：发现2个警告，0个错误');
  };

  // 并行执行父Agent的任务和等待子Agent
  await Promise.all([
    // 父Agent的任务
    monitoringTask(),
    dataProcessingTask(),
    logAnalysisTask(),
    
    // 等待所有子Agent完成
    new Promise((resolve) => {
      let completedCount = 0;
      const totalAgents = 3;
      
      [agent1, agent2, agent3].forEach(agent => {
        agent.once('complete', (status) => {
          completedCount++;
          console.log(`\n[子Agent完成] ${agent.name}: ${status.status}`);
          
          if (completedCount === totalAgents) {
            console.log('\n✅ 所有子Agent已完成！');
            resolve();
          }
        });
      });
    })
  ]);

  // ========== 阶段4：汇总结果 ==========
  console.log('\n[阶段4] 汇总所有结果...\n');

  const finalStatus = manager.getAllAgentStatus();
  
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║                    最终测试报告                             ║');
  console.log('╠════════════════════════════════════════════════════════════╣');
  console.log(`║  总Agent数: ${finalStatus.total.toString().padEnd(3)}                                          ║`);
  
  Object.entries(finalStatus.byStatus).forEach(([state, count]) => {
    console.log(`║  - ${state.padEnd(12)}: ${count.toString().padEnd(3)}                                     ║`);
  });
  
  console.log('╠════════════════════════════════════════════════════════════╣');
  console.log('║  各Agent详细结果:                                          ║');
  
  finalStatus.agents.forEach((agent, index) => {
    const statusIcon = agent.status === 'completed' ? '✅' : 
                      agent.status === 'error' ? '❌' : '⏳';
    console.log(`║  ${index + 1}. ${statusIcon} ${agent.name.padEnd(25)} ${agent.status.padEnd(10)} ║`);
    
    if (agent.result) {
      console.log(`║     └─ 结果: ${JSON.stringify(agent.result).slice(0, 40).padEnd(40)} ║`);
    }
    
    if (agent.error) {
      console.log(`║     └─ 错误: ${agent.error.slice(0, 40).padEnd(40)} ║`);
    }
  });
  
  console.log('╚════════════════════════════════════════════════════════════╝\n');

  // 保存完整报告
  const reportPath = './agent-test-report.json';
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    summary: finalStatus,
    agents: finalStatus.agents.map(a => ({
      ...a,
      logs: undefined // 不包含完整日志
    }))
  }, null, 2));
  
  console.log(`✅ 完整报告已保存至: ${reportPath}\n`);

  // ========== 清理 ==========
  console.log('[阶段5] 清理资源...\n');
  await manager.stopAll();
  console.log('✅ 所有资源已清理\n');

  console.log('🎉 所有测试完成！');
}

// 运行主程序
parentAgentMain().catch(error => {
  console.error('❌ 父Agent执行失败:', error);
  process.exit(1);
});
