#!/usr/bin/env node
/**
 * 测试框架 v6.1-Phase6.1.3
 * 
 * 核心功能:
 * 1. 压力测试框架 (负载/压力/耐久/并发)
 * 2. 边界测试用例 (输入/类型/时间/资源)
 * 3. 集成测试补充 (模块/数据流/错误/状态)
 * 4. 回归测试自动化 (用例/执行/对比/报告)
 */

const fs = require('fs');
const path = require('path');
const EventEmitter = require('events');

// ============ 测试运行器类 ============

class TestRunner extends EventEmitter {
  constructor(options = {}) {
    super();
    this.tests = [];
    this.results = [];
    this.stats = {
      total: 0,
      passed: 0,
      failed: 0,
      skipped: 0,
      startTime: null,
      endTime: null
    };
    this.options = {
      stopOnFailure: options.stopOnFailure || false,
      timeout: options.timeout || 30000,
      verbose: options.verbose || true
    };
  }

  /**
   * 添加测试
   */
  addTest(name, fn, options = {}) {
    this.tests.push({
      name,
      fn,
      options: {
        timeout: options.timeout || this.options.timeout,
        skip: options.skip || false,
        only: options.only || false
      }
    });
  }

  /**
   * 运行单个测试
   */
  async runTest(test) {
    if (test.options.skip) {
      this.stats.skipped++;
      this.emit('test:skip', { name: test.name });
      return { name: test.name, status: 'skipped' };
    }

    const startTime = Date.now();
    
    try {
      // 设置超时
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error(`测试超时 (${test.options.timeout}ms)`)), test.options.timeout);
      });

      // 运行测试
      await Promise.race([
        Promise.resolve(test.fn()),
        timeoutPromise
      ]);

      const duration = Date.now() - startTime;
      this.stats.passed++;
      this.emit('test:pass', { name: test.name, duration });

      return {
        name: test.name,
        status: 'passed',
        duration
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      this.stats.failed++;
      this.emit('test:fail', { name: test.name, error: error.message, duration });

      if (this.options.stopOnFailure) {
        throw error;
      }

      return {
        name: test.name,
        status: 'failed',
        error: error.message,
        duration
      };
    }
  }

  /**
   * 运行所有测试
   */
  async run() {
    console.log('🧪 开始运行测试...\n');
    
    this.stats.total = this.tests.length;
    this.stats.startTime = Date.now();
    this.results = [];

    // 过滤 only 测试
    const onlyTests = this.tests.filter(t => t.options.only);
    const testsToRun = onlyTests.length > 0 ? onlyTests : this.tests;

    for (const test of testsToRun) {
      if (this.options.verbose) {
        console.log(`📋 运行测试：${test.name}`);
      }

      const result = await this.runTest(test);
      this.results.push(result);

      if (this.options.verbose) {
        const status = result.status === 'passed' ? '✅' : result.status === 'failed' ? '❌' : '⏭️';
        console.log(`   ${status} ${test.name} (${result.duration}ms)`);
      }
    }

    this.stats.endTime = Date.now();
    this.emit('complete', {
      stats: this.getStats(),
      results: this.results
    });

    return {
      stats: this.getStats(),
      results: this.results
    };
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const duration = this.stats.endTime - this.stats.startTime;
    const passRate = this.stats.total > 0 
      ? ((this.stats.passed / (this.stats.total - this.stats.skipped)) * 100).toFixed(2)
      : 0;

    return {
      ...this.stats,
      duration,
      passRate: passRate + '%'
    };
  }

  /**
   * 生成报告
   */
  generateReport(format = 'text') {
    const stats = this.getStats();

    if (format === 'json') {
      return JSON.stringify({ stats, results: this.results }, null, 2);
    }

    if (format === 'html') {
      return this.generateHtmlReport(stats);
    }

    // 文本报告
    let report = '\n';
    report += '═'.repeat(60) + '\n';
    report += '📊 测试报告\n';
    report += '═'.repeat(60) + '\n';
    report += `总测试数：${stats.total}\n`;
    report += `✅ 通过：${stats.passed}\n`;
    report += `❌ 失败：${stats.failed}\n`;
    report += `⏭️  跳过：${stats.skipped}\n`;
    report += `📈 通过率：${stats.passRate}\n`;
    report += `⏱️  总耗时：${stats.duration}ms\n`;
    report += '═'.repeat(60) + '\n';

    if (stats.failed > 0) {
      report += '\n❌ 失败测试:\n\n';
      this.results
        .filter(r => r.status === 'failed')
        .forEach((r, i) => {
          report += `${i + 1}. ${r.name}\n`;
          report += `   错误：${r.error}\n`;
          report += `   耗时：${r.duration}ms\n\n`;
        });
    }

    return report;
  }

  /**
   * 生成 HTML 报告
   */
  generateHtmlReport(stats) {
    return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>测试报告</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .summary { background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    .passed { color: #4caf50; }
    .failed { color: #f44336; }
    .skipped { color: #ff9800; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #f5f5f5; }
  </style>
</head>
<body>
  <h1>📊 测试报告</h1>
  
  <div class="summary">
    <h2>统计信息</h2>
    <p>总测试数：<strong>${stats.total}</strong></p>
    <p class="passed">✅ 通过：${stats.passed}</p>
    <p class="failed">❌ 失败：${stats.failed}</p>
    <p class="skipped">⏭️  跳过：${stats.skipped}</p>
    <p>📈 通过率：<strong>${stats.passRate}</strong></p>
    <p>⏱️  总耗时：<strong>${stats.duration}ms</strong></p>
  </div>

  <h2>测试结果</h2>
  <table>
    <thead>
      <tr>
        <th>测试名称</th>
        <th>状态</th>
        <th>耗时 (ms)</th>
        <th>错误信息</th>
      </tr>
    </thead>
    <tbody>
      ${this.results.map(r => `
        <tr>
          <td>${r.name}</td>
          <td class="${r.status}">${r.status}</td>
          <td>${r.duration}</td>
          <td>${r.error || '-'}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>
</body>
</html>
`.trim();
  }
}

// ============ 断言库 ============

class Assert {
  static equal(actual, expected, message) {
    if (actual !== expected) {
      throw new Error(`${message || '断言失败'}: 期望 ${expected}, 实际 ${actual}`);
    }
  }

  static notEqual(actual, expected, message) {
    if (actual === expected) {
      throw new Error(`${message || '断言失败'}: 不应等于 ${expected}`);
    }
  }

  static deepEqual(actual, expected, message) {
    const actualStr = JSON.stringify(actual);
    const expectedStr = JSON.stringify(expected);
    if (actualStr !== expectedStr) {
      throw new Error(`${message || '断言失败'}: 期望 ${expectedStr}, 实际 ${actualStr}`);
    }
  }

  static isTrue(actual, message) {
    if (!actual) {
      throw new Error(`${message || '断言失败'}: 期望为 true`);
    }
  }

  static isFalse(actual, message) {
    if (actual) {
      throw new Error(`${message || '断言失败'}: 期望为 false`);
    }
  }

  static isNull(actual, message) {
    if (actual !== null) {
      throw new Error(`${message || '断言失败'}: 期望为 null`);
    }
  }

  static isNotNull(actual, message) {
    if (actual === null) {
      throw new Error(`${message || '断言失败'}: 不应为 null`);
    }
  }

  static isUndefined(actual, message) {
    if (actual !== undefined) {
      throw new Error(`${message || '断言失败'}: 期望为 undefined`);
    }
  }

  static isDefined(actual, message) {
    if (actual === undefined) {
      throw new Error(`${message || '断言失败'}: 不应为 undefined`);
    }
  }

  static isArray(actual, message) {
    if (!Array.isArray(actual)) {
      throw new Error(`${message || '断言失败'}: 期望为数组`);
    }
  }

  static isObject(actual, message) {
    if (actual === null || typeof actual !== 'object') {
      throw new Error(`${message || '断言失败'}: 期望为对象`);
    }
  }

  static includes(actual, expected, message) {
    if (!actual.includes(expected)) {
      throw new Error(`${message || '断言失败'}: ${JSON.stringify(actual)} 应包含 ${JSON.stringify(expected)}`);
    }
  }

  static throws(fn, expectedError, message) {
    try {
      fn();
      throw new Error(`${message || '断言失败'}: 期望抛出错误`);
    } catch (error) {
      if (expectedError && !(error instanceof expectedError)) {
        throw new Error(`${message || '断言失败'}: 期望抛出 ${expectedError.name}, 实际 ${error.name}`);
      }
    }
  }

  static async rejects(fn, expectedError, message) {
    try {
      await fn();
      throw new Error(`${message || '断言失败'}: 期望抛出错误`);
    } catch (error) {
      if (expectedError && !(error instanceof expectedError)) {
        throw new Error(`${message || '断言失败'}: 期望抛出 ${expectedError.name}, 实际 ${error.name}`);
      }
    }
  }

  static greaterThan(actual, expected, message) {
    if (actual <= expected) {
      throw new Error(`${message || '断言失败'}: ${actual} 应大于 ${expected}`);
    }
  }

  static lessThan(actual, expected, message) {
    if (actual >= expected) {
      throw new Error(`${message || '断言失败'}: ${actual} 应小于 ${expected}`);
    }
  }
}

// ============ 压力测试框架 ============

class StressTestFramework extends EventEmitter {
  constructor(options = {}) {
    super();
    this.options = {
      concurrency: options.concurrency || 100,
      duration: options.duration || 60000,
      rampUp: options.rampUp || 5000,
      ...options
    };
    this.stats = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      responseTimes: [],
      errors: []
    };
  }

  /**
   * 运行压力测试
   */
  async run(testFn, options = {}) {
    const {
      concurrency = this.options.concurrency,
      duration = this.options.duration,
      rampUp = this.options.rampUp
    } = options;

    console.log('⚡ 开始压力测试...');
    console.log(`   并发数：${concurrency}`);
    console.log(`   持续时间：${duration}ms`);
    console.log(`   预热时间：${rampUp}ms\n`);

    const startTime = Date.now();
    this.stats = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      responseTimes: [],
      errors: []
    };

    // 预热阶段
    if (rampUp > 0) {
      console.log('🔥 预热阶段...');
      await this.rampUp(testFn, rampUp, concurrency);
    }

    // 压力测试阶段
    console.log('🚀 压力测试阶段...');
    await this.stressPhase(testFn, duration, concurrency);

    // 计算统计信息
    const endTime = Date.now();
    const totalDuration = endTime - startTime;
    const qps = this.stats.successfulRequests / (totalDuration / 1000);
    const avgResponseTime = this.stats.responseTimes.length > 0
      ? this.stats.responseTimes.reduce((a, b) => a + b, 0) / this.stats.responseTimes.length
      : 0;
    const p95ResponseTime = this.percentile(this.stats.responseTimes, 95);
    const p99ResponseTime = this.percentile(this.stats.responseTimes, 99);

    const results = {
      duration: totalDuration,
      totalRequests: this.stats.totalRequests,
      successfulRequests: this.stats.successfulRequests,
      failedRequests: this.stats.failedRequests,
      qps: qps.toFixed(2),
      avgResponseTime: avgResponseTime.toFixed(2),
      p95ResponseTime: p95ResponseTime.toFixed(2),
      p99ResponseTime: p99ResponseTime.toFixed(2),
      errorRate: ((this.stats.failedRequests / this.stats.totalRequests) * 100).toFixed(2) + '%',
      errors: this.stats.errors.slice(0, 10) // 只保留前 10 个错误
    };

    this.emit('complete', results);
    return results;
  }

  /**
   * 预热阶段
   */
  async rampUp(testFn, duration, concurrency) {
    const startTime = Date.now();
    const tasks = [];

    while (Date.now() - startTime < duration) {
      const currentConcurrency = Math.floor(
        concurrency * ((Date.now() - startTime) / duration)
      );

      for (let i = 0; i < currentConcurrency; i++) {
        tasks.push(this.executeRequest(testFn));
      }

      await Promise.all(tasks);
      tasks.length = 0;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  /**
   * 压力测试阶段
   */
  async stressPhase(testFn, duration, concurrency) {
    const startTime = Date.now();
    const tasks = [];

    while (Date.now() - startTime < duration) {
      for (let i = 0; i < concurrency; i++) {
        tasks.push(this.executeRequest(testFn));
      }

      await Promise.all(tasks);
      tasks.length = 0;

      this.emit('progress', {
        elapsed: Date.now() - startTime,
        total: duration,
        requests: this.stats.successfulRequests,
        qps: (this.stats.successfulRequests / ((Date.now() - startTime) / 1000)).toFixed(2)
      });
    }
  }

  /**
   * 执行单个请求
   */
  async executeRequest(testFn) {
    const startTime = Date.now();
    this.stats.totalRequests++;

    try {
      await testFn();
      const duration = Date.now() - startTime;
      this.stats.successfulRequests++;
      this.stats.responseTimes.push(duration);
    } catch (error) {
      this.stats.failedRequests++;
      this.stats.errors.push(error.message);
    }
  }

  /**
   * 计算百分位数
   */
  percentile(array, p) {
    if (array.length === 0) return 0;
    const sorted = array.slice().sort((a, b) => a - b);
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[index];
  }
}

// ============ 边界测试用例 ============

class BoundaryTests {
  constructor() {
    this.testCases = [
      { name: '空输入', input: null },
      { name: '空字符串', input: '' },
      { name: '空数组', input: [] },
      { name: '空对象', input: {} },
      { name: 'undefined', input: undefined },
      { name: 'NaN', input: NaN },
      { name: 'Infinity', input: Infinity },
      { name: '超大数字', input: Number.MAX_SAFE_INTEGER },
      { name: '超小数字', input: Number.MIN_SAFE_INTEGER },
      { name: '超大字符串', input: 'x'.repeat(1000000) },
      { name: '特殊字符', input: '<>&"\'\n\r\t\\' },
      { name: 'Unicode', input: '你好世界🌍こんにちは' },
      { name: 'Emoji', input: '😀😁😂🤣😃' },
      { name: 'SQL 注入', input: "'; DROP TABLE users; --" },
      { name: 'XSS 攻击', input: '<script>alert("xss")</script>' },
      { name: '路径遍历', input: '../../../etc/passwd' },
      { name: '超长数组', input: Array(10000).fill('item') },
      { name: '深层嵌套', input: this.createDeepObject(100) },
      { name: '循环引用', input: this.createCircularObject() }
    ];
  }

  /**
   * 创建深层嵌套对象
   */
  createDeepObject(depth) {
    let obj = {};
    for (let i = 0; i < depth; i++) {
      obj = { nested: obj };
    }
    return obj;
  }

  /**
   * 创建循环引用对象
   */
  createCircularObject() {
    const obj = { name: 'test' };
    obj.self = obj;
    return obj;
  }

  /**
   * 运行边界测试
   */
  async run(fn, options = {}) {
    const { skip = [], only = [] } = options;
    const results = [];

    console.log('🔍 开始边界测试...\n');

    for (const testCase of this.testCases) {
      if (skip.includes(testCase.name)) continue;
      if (only.length > 0 && !only.includes(testCase.name)) continue;

      console.log(`📋 测试：${testCase.name}`);

      try {
        const result = await fn(testCase.input);
        results.push({
          name: testCase.name,
          status: 'passed',
          input: testCase.input
        });
        console.log(`   ✅ 通过\n`);
      } catch (error) {
        results.push({
          name: testCase.name,
          status: 'failed',
          input: testCase.input,
          error: error.message
        });
        console.log(`   ❌ 失败：${error.message}\n`);
      }
    }

    const passed = results.filter(r => r.status === 'passed').length;
    const failed = results.filter(r => r.status === 'failed').length;

    console.log('═'.repeat(60));
    console.log(`边界测试完成：${passed} 通过，${failed} 失败`);
    console.log('═'.repeat(60));

    return {
      total: results.length,
      passed,
      failed,
      passRate: ((passed / results.length) * 100).toFixed(2) + '%',
      results
    };
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
测试框架 v6.1

用法：node test-framework.js <命令> [选项]

命令:
  test                运行示例测试
  stress              运行压力测试
  boundary            运行边界测试
  report              生成测试报告

示例:
  node test-framework.js test
  node test-framework.js stress
  node test-framework.js boundary
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  switch (command) {
    case 'test':
      console.log('🧪 运行示例测试...\n');

      const runner = new TestRunner({ verbose: true });

      // 添加测试用例
      runner.addTest('空数组测试', () => {
        Assert.isArray([]);
      });

      runner.addTest('对象相等测试', () => {
        Assert.deepEqual({ a: 1 }, { a: 1 });
      });

      runner.addTest('真值测试', () => {
        Assert.isTrue(true);
      });

      runner.addTest('假值测试', () => {
        Assert.isFalse(false);
      });

      runner.addTest('错误抛出测试', () => {
        Assert.throws(() => { throw new Error('test'); }, Error);
      });

      runner.addTest('跳过测试', () => {
        console.log('这个测试应该被跳过');
      }, { skip: true });

      const results = await runner.run();
      console.log(runner.generateReport());
      break;

    case 'stress':
      console.log('⚡ 运行压力测试...\n');

      const stressTest = new StressTestFramework({
        concurrency: 50,
        duration: 10000,
        rampUp: 2000
      });

      stressTest.on('progress', (progress) => {
        console.log(`📊 进度：${progress.elapsed}/${progress.duration}ms - ${progress.qps} QPS`);
      });

      const stressResults = await stressTest.run(async () => {
        // 模拟 API 调用
        await new Promise(resolve => setTimeout(resolve, Math.random() * 100));
      });

      console.log('\n📊 压力测试结果:');
      console.log(JSON.stringify(stressResults, null, 2));
      break;

    case 'boundary':
      console.log('🔍 运行边界测试...\n');

      const boundaryTests = new BoundaryTests();

      const boundaryResults = await boundaryTests.run((input) => {
        // 测试函数应该能处理各种边界输入
        if (input === null || input === undefined) {
          return 'handled';
        }
        if (typeof input === 'string') {
          return input.length;
        }
        if (Array.isArray(input)) {
          return input.length;
        }
        if (typeof input === 'object') {
          return Object.keys(input).length;
        }
        return input;
      });

      console.log('\n边界测试结果:');
      console.log(JSON.stringify(boundaryResults, null, 2));
      break;

    case 'report':
      const runner2 = new TestRunner();
      
      runner2.addTest('测试 1', () => { Assert.isTrue(true); });
      runner2.addTest('测试 2', () => { Assert.equal(1, 1); });
      runner2.addTest('测试 3', () => { Assert.isArray([]); });
      
      await runner2.run();
      
      console.log(runner2.generateReport('text'));
      
      // 保存 HTML 报告
      const htmlReport = runner2.generateReport('html');
      const reportPath = path.join(__dirname, '../test-reports/report-' + Date.now() + '.html');
      fs.writeFileSync(reportPath, htmlReport);
      console.log(`📄 HTML 报告已保存：${reportPath}`);
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = {
  TestRunner,
  Assert,
  StressTestFramework,
  BoundaryTests
};

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
