/**
 * data-pipeline 使用示例
 * 
 * 演示常见数据处理场景
 */

'use strict';

const { Pipeline, Transformers, Validators, PipelineFactory } = require('../src/pipeline');

// ──────────────────────────────────────────────
// 示例 1: 数据清洗管线
// ──────────────────────────────────────────────

async function example1_cleanData() {
  console.log('=== 示例 1: 数据清洗管线 ===\n');

  const rawData = [
    { name: '  Alice  ', email: 'alice@example.com', age: 30 },
    { name: '  Bob  ', email: 'bob@example.com', age: 25 },
    { name: '  Charlie  ', email: 'charlie@example.com', age: 35 },
  ];

  const schema = {
    name: { required: true, type: 'string', minLength: 1, maxLength: 50 },
    email: { type: 'string', pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
    age: { type: 'number', min: 0, max: 150 }
  };

  // 使用 createCleaner：验证 → 填充默认值 → 修剪 → 移除空项
  const pipeline = PipelineFactory.createCleaner(schema, { age: 0 });
  const result = await pipeline.execute(rawData);
  console.log('输入:', JSON.stringify(rawData, null, 2));
  console.log('\n清洗后:', JSON.stringify(result.data, null, 2));
}

// ──────────────────────────────────────────────
// 示例 2: ETL 管线
// ──────────────────────────────────────────────

async function example2_etl() {
  console.log('\n=== 示例 2: ETL 管线 ===\n');

  const users = [
    { id: 1, first: 'Alice', last: 'Smith', dept_id: 10, salary: '8000' },
    { id: 2, first: 'Bob', last: 'Jones', dept_id: 20, salary: '7500' },
    { id: 3, first: 'Charlie', last: 'Brown', dept_id: 10, salary: '9000' },
  ];

  const departments = [
    { dept_id: 10, dept_name: 'Engineering' },
    { dept_id: 20, dept_name: 'Marketing' },
  ];

  const etl = PipelineFactory.createETL(
    // Extract
    () => users,
    // Transform
    [
      { name: 'rename', fn: Transformers.rename({ first: 'firstName', last: 'lastName' }) },
      { name: 'parseSalary', fn: Transformers.map(u => ({ ...u, salary: parseInt(u.salary) })) },
      { name: 'mergeDept', fn: Transformers.merge('dept_id', departments) },
      { name: 'calcTax', fn: Transformers.map(u => ({ ...u, afterTax: Math.round(u.salary * 0.8) })) },
      { name: 'sortBySalary', fn: Transformers.sort('salary', 'desc') }
    ],
    // Load
    (data) => data
  );

  const result = await etl.run(null);
  console.log('ETL 结果:', JSON.stringify(result, null, 2));
}

// ──────────────────────────────────────────────
// 示例 3: 数据分析管线
// ──────────────────────────────────────────────

async function example3_analyze() {
  console.log('\n=== 示例 3: 数据分析管线 ===\n');

  const sales = [
    { region: 'East', product: 'A', amount: 100, date: '2024-01' },
    { region: 'East', product: 'B', amount: 200, date: '2024-01' },
    { region: 'West', product: 'A', amount: 150, date: '2024-01' },
    { region: 'West', product: 'A', amount: 300, date: '2024-02' },
    { region: 'East', product: 'A', amount: 120, date: '2024-02' },
  ];

  const analyzer = PipelineFactory.createAnalyzer('region', {
    totalSales: { field: 'amount', fn: vals => vals.reduce((a, b) => a + b, 0) },
    avgSale: { field: 'amount', fn: vals => Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) },
    maxSale: { field: 'amount', fn: vals => Math.max(...vals) },
    minSale: { field: 'amount', fn: vals => Math.min(...vals) }
  });

  const result = await analyzer.run(sales);
  console.log('按地区分析:', JSON.stringify(result, null, 2));
}

// ──────────────────────────────────────────────
// 示例 4: 重试和错误恢复
// ──────────────────────────────────────────────

async function example4_retry() {
  console.log('\n=== 示例 4: 重试和错误恢复 ===\n');

  let apiCalls = 0;
  const flakyApi = async (data) => {
    apiCalls++;
    if (apiCalls < 3) {
      throw new Error(`API call ${apiCalls} failed (simulated)`);
    }
    return data.map(x => ({ ...x, enriched: true }));
  };

  const pipeline = new Pipeline();
  pipeline.addStage('flakyApi', flakyApi, {
    retryCount: 3,
    retryDelay: 50,
    timeout: 5000
  });

  const result = await pipeline.execute([{ id: 1 }, { id: 2 }]);
  console.log(`API 调用次数: ${apiCalls}`);
  console.log('结果:', JSON.stringify(result.data, null, 2));
}

// ──────────────────────────────────────────────
// 运行所有示例
// ──────────────────────────────────────────────

(async () => {
  await example1_cleanData();
  await example2_etl();
  await example3_analyze();
  await example4_retry();
  console.log('\n✅ 所有示例运行完成');
})();
