/**
 * Dreaming Guard Pro Phase 3 - 快速测试
 * 测试 analyzer 和 decision 两个模块
 */

const assert = require('assert');
const path = require('path');

// 模块路径
const Analyzer = require('../src/analyzer.js');
const Decision = require('../src/decision.js');
const { RISK_LEVELS } = require('../src/analyzer.js');
const { ACTION_TYPES } = require('../src/decision.js');

// 测试结果
let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log('  ✓', name);
    passed++;
  } catch (e) {
    console.log('  ✗', name);
    console.log('    Error:', e.message);
    failed++;
  }
}

// 创建模拟历史数据
function createMockHistory(count, startSize, growthPerStep) {
  const history = [];
  const now = Date.now();
  const interval = 30000; // 30秒间隔
  
  for (let i = 0; i < count; i++) {
    history.push({
      timestamp: now - (count - i) * interval,
      totalSize: startSize + i * growthPerStep,
      totalFiles: 10 + Math.floor(i / 5),
      growthRate: growthPerStep / (interval / 60000) // bytes/min
    });
  }
  
  return history;
}

// 主测试函数
async function runTests() {
  console.log('=== Analyzer Tests ===\n');

  // ============ Analyzer 基础测试 ============
  const analyzer = new Analyzer({
    logger: { debug: () => {}, info: () => {}, warn: () => {}, error: () => {} }
  });

  await test('Analyzer instantiation', async () => {
    assert(analyzer instanceof Analyzer);
    assert(analyzer.config.thresholds.green === 524288000);
  });

  await test('Analyzer analyze with insufficient data', async () => {
    const result = analyzer.analyze([]);
    assert(result.valid === false);
    assert(result.riskLevel === RISK_LEVELS.GREEN);
  });

  await test('Analyzer analyze with valid data', async () => {
    const history = createMockHistory(10, 100000, 5000); // 10样本，稳定增长
    const result = analyzer.analyze(history);
    assert(result.valid === true);
    assert(typeof result.growthRate === 'number');
    assert(typeof result.growthRateKB === 'number');
    assert(result.riskLevel !== undefined);
  });

  await test('Analyzer predict method', async () => {
    const prediction = analyzer.predict(1024 * 60, 1024 * 1024, 10 * 1024 * 1024); // 60KB/min, 1MB当前, 10MB最大
    assert(typeof prediction.timeToFull === 'number');
    assert(prediction.timeToFullMinutes > 0);
    assert(prediction.trend !== undefined);
    assert(typeof prediction.percentUsed === 'number');
  });

  await test('Analyzer predict with zero growth', async () => {
    const prediction = analyzer.predict(0, 1024 * 1024, 10 * 1024 * 1024);
    assert(prediction.timeToFull === Infinity);
    assert(prediction.trend === 'stable');
  });

  await test('Analyzer getRiskLevel - green', async () => {
    const status = {
      currentSize: 100000,  // 100KB
      growthRate: 1024,     // 1KB/min
      prediction: { timeToFullMinutes: 1000 },
      anomalies: []
    };
    const level = analyzer.getRiskLevel(status);
    assert(level === RISK_LEVELS.GREEN);
  });

  await test('Analyzer getRiskLevel - yellow', async () => {
    const status = {
      currentSize: 600 * 1024 * 1024,  // 600MB（超过yellow阈值）
      growthRate: 50 * 1024,           // 50KB/min
      prediction: { timeToFullMinutes: 300 },
      anomalies: []
    };
    const level = analyzer.getRiskLevel(status);
    assert(level === RISK_LEVELS.YELLOW);
  });

  await test('Analyzer getRiskLevel - red by size', async () => {
    const status = {
      currentSize: 2.5 * 1024 * 1024 * 1024,  // 2.5GB（超过red阈值）
      growthRate: 1024,
      prediction: { timeToFullMinutes: 100 },
      anomalies: []
    };
    const level = analyzer.getRiskLevel(status);
    assert(level === RISK_LEVELS.RED);
  });

  await test('Analyzer getRiskLevel - red by growth', async () => {
    const status = {
      currentSize: 100000,
      growthRate: 600 * 1024,  // 600KB/min（超过high阈值）
      prediction: { timeToFullMinutes: 100 },
      anomalies: []
    };
    const level = analyzer.getRiskLevel(status);
    assert(level === RISK_LEVELS.RED);
  });

  await test('Analyzer detect anomalies - spike', async () => {
    // 创建有突增的历史数据
    const history = createMockHistory(15, 100000, 5000);
    // 添加一个突增
    history[history.length - 1].totalSize = history[history.length - 2].totalSize + 100000;
    
    const result = analyzer.analyze(history);
    // 应该检测到异常（如果有足够的突增）
    assert(result.anomalies !== undefined);
  });

  await test('Analyzer cache works', async () => {
    const history = createMockHistory(10, 100000, 5000);
    const result1 = analyzer.analyze(history);
    const result2 = analyzer.analyze(history);
    // 缓存应该返回相同结果
    assert(result1.timestamp === result2.timestamp);
  });

  await test('Analyzer clearCache', async () => {
    analyzer.clearCache();
    const history = createMockHistory(10, 100000, 5000);
    const result = analyzer.analyze(history);
    assert(result.valid === true);
  });

  // ============ Decision 基础测试 ============
  console.log('\n=== Decision Tests ===\n');

  const decision = new Decision({
    logger: { debug: () => {}, info: () => {}, warn: () => {}, error: () => {} }
  });

  await test('Decision instantiation', async () => {
    assert(decision instanceof Decision);
    assert(decision.config.riskActions.green === ACTION_TYPES.NO_ACTION);
  });

  await test('Decision decide with invalid analysis', async () => {
    const result = decision.decide({ valid: false });
    assert(result.action === ACTION_TYPES.NO_ACTION);
  });

  await test('Decision decide - green level', async () => {
    const analysis = {
      valid: true,
      riskLevel: RISK_LEVELS.GREEN,
      currentSize: 100000,
      growthRate: 1024,
      prediction: { timeToFullMinutes: 1000, confidence: 0.8 },
      anomalies: [],
      samples: 10,
      recommendation: 'continue_monitoring'
    };
    const result = decision.decide(analysis);
    assert(result.action === ACTION_TYPES.NO_ACTION);
    assert(typeof result.confidence === 'number');
  });

  await test('Decision decide - yellow level', async () => {
    const analysis = {
      valid: true,
      riskLevel: RISK_LEVELS.YELLOW,
      currentSize: 600 * 1024 * 1024,
      growthRate: 50 * 1024,
      prediction: { timeToFullMinutes: 200, confidence: 0.9 },
      anomalies: [],
      samples: 15,
      recommendation: 'plan_action'
    };
    const result = decision.decide(analysis);
    assert(result.action === ACTION_TYPES.NOTIFY || result.action === ACTION_TYPES.ARCHIVE);
  });

  await test('Decision decide - red level', async () => {
    const analysis = {
      valid: true,
      riskLevel: RISK_LEVELS.RED,
      currentSize: 2.1 * 1024 * 1024 * 1024,
      growthRate: 600 * 1024,
      prediction: { timeToFullMinutes: 50, confidence: 0.9 },
      anomalies: [],
      samples: 20,
      recommendation: 'immediate_action'
    };
    const result = decision.decide(analysis);
    assert(result.action === ACTION_TYPES.ARCHIVE || result.action === ACTION_TYPES.COMPRESS || result.action === ACTION_TYPES.EMERGENCY);
  });

  await test('Decision getActionPlan', async () => {
    const plan = decision.getActionPlan(ACTION_TYPES.ARCHIVE);
    assert(plan.type === ACTION_TYPES.ARCHIVE);
    assert(Array.isArray(plan.steps));
    assert(typeof plan.estimatedTime === 'number');
  });

  await test('Decision getActionPlan for all types', async () => {
    const types = Object.values(ACTION_TYPES);
    for (const type of types) {
      const plan = decision.getActionPlan(type);
      assert(plan.type === type);
      assert(plan.description !== undefined);
    }
  });

  await test('Decision registerHandler', async () => {
    decision.registerHandler(ACTION_TYPES.NOTIFY, async (ctx) => ({ notified: true }));
    assert(decision.actionHandlers[ACTION_TYPES.NOTIFY] !== undefined);
  });

  await test('Decision executeAction', async () => {
    decision.registerHandler(ACTION_TYPES.NOTIFY, async (ctx) => ({ notified: true, ctx }));
    const result = await decision.executeAction(ACTION_TYPES.NOTIFY, { test: true });
    assert(result.success === true);
    assert(result.result.notified === true);
  });

  await test('Decision executeAction without handler', async () => {
    const result = await decision.executeAction('unknown_action');
    assert(result.success === false);
    assert(result.error !== undefined);
  });

  await test('Decision history', async () => {
    const analysis = {
      valid: true,
      riskLevel: RISK_LEVELS.GREEN,
      currentSize: 100000,
      growthRate: 1024,
      prediction: { timeToFullMinutes: 1000 },
      anomalies: [],
      samples: 10
    };
    decision.decide(analysis);
    decision.decide(analysis);
    
    const history = decision.getHistory(5);
    assert(Array.isArray(history));
    assert(history.length >= 2);
  });

  await test('Decision getLastDecision', async () => {
    const last = decision.getLastDecision();
    assert(last !== null);
    assert(last.action !== undefined);
  });

  await test('Decision resetState', async () => {
    decision.resetState();
    assert(decision.state.lastAction === null);
    assert(decision.state.consecutiveCount === 0);
  });

  await test('Decision cooldown check', async () => {
    // 配置短冷却时间
    const decision2 = new Decision({
      rules: {
        cooldown: {
          enabled: true,
          durations: {
            archive: 1000  // 1秒冷却
          }
        }
      },
      logger: { debug: () => {}, info: () => {}, warn: () => {}, error: () => {} }
    });
    
    const analysis = {
      valid: true,
      riskLevel: RISK_LEVELS.RED,
      currentSize: 2.1 * 1024 * 1024 * 1024,
      growthRate: 600 * 1024,
      prediction: { timeToFullMinutes: 50 },
      anomalies: [],
      samples: 20
    };
    
    const result1 = decision2.decide(analysis);
    // 如果在冷却期，应该降级
    const result2 = decision2.decide(analysis);
    // 第二次决策可能因为冷却而降级
    assert(result2.action !== undefined);
  });

  // ============ 集成测试 ============
  console.log('\n=== Integration Tests ===\n');

  await test('Analyzer + Decision pipeline', async () => {
    const history = createMockHistory(20, 500 * 1024 * 1024, 5 * 1024 * 1024); // 从500MB开始，每步增长5MB
    const analysisResult = analyzer.analyze(history);
    const decisionResult = decision.decide(analysisResult);
    
    assert(analysisResult.valid === true);
    assert(decisionResult.action !== undefined);
    assert(typeof decisionResult.confidence === 'number');
  });

  await test('Analyzer + Decision with high growth', async () => {
    const history = createMockHistory(15, 1 * 1024 * 1024 * 1024, 10 * 1024 * 1024); // 从1GB开始，快速增长
    const analysisResult = analyzer.analyze(history);
    const decisionResult = decision.decide(analysisResult);
    
    assert(analysisResult.riskLevel !== RISK_LEVELS.GREEN);
    // 高增长应该触发更高级别动作
    assert(ACTION_PRIORITY[decisionResult.action] >= ACTION_PRIORITY[ACTION_TYPES.NOTIFY]);
  });

  // ============ 总结 ============
  console.log('\n=== Results ===');
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total:  ${passed + failed}`);

  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(err => {
  console.error('Test runner failed:', err);
  process.exit(1);
});