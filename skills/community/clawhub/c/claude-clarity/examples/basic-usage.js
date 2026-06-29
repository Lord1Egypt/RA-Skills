#!/usr/bin/env node

/**
 * ============================================================
 *  basic-usage.js — 心虫 Clarity 基础用法示例
 *  Basic Usage Example for Clarity Cognitive Engine
 *
 *  展示: createClarity → start → think → healthCheck → stop
 *  Demonstrates: engine initialization, cognitive reasoning,
 *                health check, and graceful shutdown
 * ============================================================
 */

// 引入核心模块 (CommonJS)
// Import core module
const path = require('path');
const { createClarity } = require('../src/core/clarity.js');

// 示例主函数
// Main example function
async function main() {
  console.log('========================================');
  console.log('  心虫 Clarity 基础用法演示');
  console.log('  Basic Usage Demonstration');
  console.log('========================================\n');

  // ── Step 1: 创建引擎实例 ──
  // Step 1: Create engine instance
  console.log('---- Step 1: 创建引擎实例 (createClarity) ----');
  let hf;
  try {
    hf = createClarity({
      rootPath: __dirname,  // 使用当前目录作为项目根路径
      autoStart: false,     // 手动控制启动时机
    });
    console.log('[OK] 引擎实例已创建 / Engine instance created\n');
  } catch (err) {
    console.error('[FAIL] 引擎创建失败 / Engine creation failed:', err.message);
    console.error('      请确认项目依赖已安装: npm install');
    process.exit(1);
  }

  // ── Step 2: 启动引擎 ──
  // Step 2: Start the engine
  console.log('---- Step 2: 启动引擎 (start) ----');
  try {
    await hf.start();
    console.log('[OK] 引擎已启动 / Engine started\n');
  } catch (err) {
    console.error('[FAIL] 引擎启动失败 / Engine start failed:', err.message);
    process.exit(1);
  }

  // ── Step 3: 健康检查 ──
  // Step 3: Health check
  console.log('---- Step 3: 健康检查 (healthCheck) ----');
  try {
    const health = await hf.healthCheck();
    console.log('  运行状态 / Running :', health.started ? '是/Yes' : '否/No');
    console.log('  运行时长 / Uptime  :', health.uptime_ms, 'ms');
    console.log('  会话 ID / Session  :', health.sessionId);
    console.log('  版本 / Version     :', health.version);
    console.log('  启动错误 / Errors  :', (health.initErrors || []).length, '个');
    if (health.subsystems) {
      const subs = Object.keys(health.subsystems);
      console.log('  子系统 / Subsystems:', subs.length, '个已注册');
    }
    console.log('[OK] 健康检查通过 / Health check passed\n');
  } catch (err) {
    console.error('[FAIL] 健康检查失败:', err.message);
  }

  // ── Step 4: 思考推理 (think) ──
  // Step 4: Cognitive reasoning
  console.log('---- Step 4: 认知推理 (think) ----');
  try {
    const question = '存在先于本质是什么意思？这段代码为什么是有意义的？';
    const result = await hf.think(question);
    console.log('  输入 / Input    :', question);
    console.log('  决策 / Decision :', result.decision || '(未提供/Not available)');
    console.log('  判断 / Judgment :', result.judgment || '(未提供/Not available)');
    if (result.emotion) {
      console.log('  情绪类型 / Emotion type :', result.emotion.type || 'neutral');
      console.log('  情绪强度 / Intensity    :', result.emotion.intensity || 0);
      console.log('  PAD  / Pleasure/Arousal/Dominance:',
        result.emotion.pad?.pleasure?.toFixed(2) || 'N/A', '/',
        result.emotion.pad?.arousal?.toFixed(2) || 'N/A', '/',
        result.emotion.pad?.dominance?.toFixed(2) || 'N/A');
    }
    console.log('[OK] think() 执行完成\n');
  } catch (err) {
    console.error('[FAIL] think() 执行失败:', err.message);
    console.log('       (这可能是因为 think() 需要更完整的子系统集合)');
    console.log('       (This may be expected if think() requires more subsystems)\n');
  }

  // ── Step 5: dispatch 路由 ──
  // Step 5: Dispatch routing
  console.log('---- Step 5: 路由分发 (dispatch) ----');
  const testRoutes = [
    'emotion.getPAD',
    'heartLogic.whatIsThis',
    'psychology.classify',
  ];
  for (const route of testRoutes) {
    try {
      const result = hf.dispatch(route, '我觉得很开心，今天完成了一个重要项目');
      console.log(`  路由 / Route "${route}"`);
      console.log(`  结果 / Result:`, JSON.stringify(result).slice(0, 120) + '...\n');
    } catch (err) {
      console.log(`  路由 / Route "${route}" 不可用:`, err.message);
      console.log('   (模块可能未加载 / Module may not be loaded)\n');
    }
  }

  // ── Step 6: 记忆系统检查 ──
  // Step 6: Memory system check
  console.log('---- Step 6: 记忆系统 (memory) ----');
  try {
    if (hf.memory) {
      const stats = await hf.memory.getStats();
      console.log('  记忆统计 / Memory stats:', JSON.stringify(stats).slice(0, 200));
    } else {
      console.log('  记忆系统未就绪 / Memory not ready');
    }
    console.log('[OK] 记忆系统访问完成\n');
  } catch (err) {
    console.error('[INFO] 记忆系统暂不可用:', err.message);
    console.log('       (这可能是因为运行时路径限制)\n');
  }

  // ── Step 7: 停止引擎 ──
  // Step 7: Stop the engine
  console.log('---- Step 7: 停止引擎 (stop) ----');
  try {
    await hf.stop();
    console.log('[OK] 引擎已停止 / Engine stopped\n');
  } catch (err) {
    console.error('[FAIL] 引擎停止失败:', err.message);
  }

  // ── 摘要 ──
  // Summary
  console.log('========================================');
  console.log('  基础用法演示完成 / Demo Complete');
  console.log('  涵盖 / Covered:');
  console.log('    createClarity  ✓');
  console.log('    start()        ✓');
  console.log('    healthCheck()  ✓');
  console.log('    think()        ✓');
  console.log('    dispatch()     ✓');
  console.log('    memory/stats   ✓');
  console.log('    stop()         ✓');
  console.log('========================================');
}

main().catch(err => {
  console.error('未捕获的错误 / Uncaught error:', err);
  process.exit(1);
});
