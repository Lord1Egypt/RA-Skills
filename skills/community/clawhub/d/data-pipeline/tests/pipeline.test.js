/**
 * data-pipeline 测试套件
 * 
 * 覆盖：管线引擎、内置转换器、验证器、工厂函数
 */

'use strict';

const assert = require('assert');
const { Pipeline, Stage, PipelineError, Transformers, Validators, PipelineFactory } = require('../src/pipeline');

// ──────────────────────────────────────────────
// 辅助函数
// ──────────────────────────────────────────────

function asyncFn(fn) {
  return async (data, ctx) => fn(data, ctx);
}

// ──────────────────────────────────────────────
// 测试：Pipeline 核心引擎
// ──────────────────────────────────────────────

describe('Pipeline 核心引擎', () => {

  describe('基础执行', () => {
    it('单阶段管线应正确执行', async () => {
      const pipeline = new Pipeline();
      pipeline.addStage('double', asyncFn(d => d.map(x => x * 2)));
      const result = await pipeline.run([1, 2, 3]);
      assert.deepStrictEqual(result, [2, 4, 6]);
    });

    it('多阶段管线应按顺序执行', async () => {
      const pipeline = new Pipeline();
      pipeline
        .addStage('double', asyncFn(d => d.map(x => x * 2)))
        .addStage('filter', asyncFn(d => d.filter(x => x > 3)))
        .addStage('sort', asyncFn(d => [...d].sort((a, b) => b - a)));

      const result = await pipeline.run([1, 2, 3, 4]);
      // double: [2,4,6,8] → filter >3: [4,6,8] → sort desc: [8,6,4]
      assert.deepStrictEqual(result, [8, 6, 4]);
    });

    it('execute 应返回数据和 metadata', async () => {
      const pipeline = new Pipeline();
      pipeline.addStage('noop', asyncFn(d => d));
      const result = await pipeline.execute([1, 2]);
      assert.ok(result.data);
      assert.ok(result.metadata);
      assert.strictEqual(result.metadata.stageCount, 1);
      assert.strictEqual(result.metadata.stages[0].stage, 'noop');
      assert.strictEqual(result.metadata.stages[0].status, 'completed');
    });

    it('链式调用应返回同一管线实例', () => {
      const pipeline = new Pipeline();
      const result = pipeline
        .addStage('a', asyncFn(d => d))
        .addStage('b', asyncFn(d => d))
        .removeStage('a');
      assert.strictEqual(result, pipeline);
    });
  });

  describe('阶段管理', () => {
    it('addStages 应批量添加阶段', async () => {
      const pipeline = new Pipeline();
      pipeline.addStages([
        { name: 'a', fn: asyncFn(d => d) },
        { name: 'b', fn: asyncFn(d => d) },
        { name: 'c', fn: asyncFn(d => d) }
      ]);
      const result = await pipeline.execute([1]);
      assert.strictEqual(result.metadata.stageCount, 3);
    });

    it('insertBefore 应在目标阶段前插入', async () => {
      const pipeline = new Pipeline();
      pipeline
        .addStage('first', asyncFn(d => [...d, 'first']))
        .addStage('last', asyncFn(d => [...d, 'last']));
      pipeline.insertBefore('last', 'middle', asyncFn(d => [...d, 'middle']));

      const result = await pipeline.run([]);
      assert.deepStrictEqual(result, ['first', 'middle', 'last']);
    });

    it('insertAfter 应在目标阶段后插入', async () => {
      const pipeline = new Pipeline();
      pipeline
        .addStage('first', asyncFn(d => [...d, 'first']))
        .addStage('last', asyncFn(d => [...d, 'last']));
      pipeline.insertAfter('first', 'middle', asyncFn(d => [...d, 'middle']));

      const result = await pipeline.run([]);
      assert.deepStrictEqual(result, ['first', 'middle', 'last']);
    });

    it('removeStage 应移除指定阶段', async () => {
      const pipeline = new Pipeline();
      pipeline
        .addStage('keep', asyncFn(d => d))
        .addStage('remove', asyncFn(d => d));
      pipeline.removeStage('remove');
      const result = await pipeline.execute([1]);
      assert.strictEqual(result.metadata.stageCount, 1);
      assert.strictEqual(result.metadata.stages[0].stage, 'keep');
    });

    it('toggleStage 应启用/禁用阶段', async () => {
      const pipeline = new Pipeline();
      pipeline
        .addStage('active', asyncFn(d => [...d, 'active']))
        .addStage('disabled', asyncFn(d => [...d, 'disabled']));
      pipeline.toggleStage('disabled', false);
      const result = await pipeline.run([]);
      assert.deepStrictEqual(result, ['active']);
    });

    it('insertBefore/After 找不到阶段应抛错', () => {
      const pipeline = new Pipeline();
      pipeline.addStage('only', asyncFn(d => d));
      assert.throws(() => pipeline.insertBefore('nonexistent', 'x', asyncFn(d => d)));
      assert.throws(() => pipeline.insertAfter('nonexistent', 'x', asyncFn(d => d)));
    });
  });

  describe('错误处理', () => {
    it('strict 模式应在首个阶段失败时停止', async () => {
      const pipeline = new Pipeline({ strict: true });
      pipeline
        .addStage('fail', asyncFn(() => { throw new Error('boom'); }))
        .addStage('never', asyncFn(d => d));

      try {
        await pipeline.execute([1]);
        assert.fail('should have thrown');
      } catch (err) {
        assert.ok(err instanceof PipelineError);
        assert.strictEqual(err.failedStage, 'fail');
        // 第二个阶段不应被执行
        assert.strictEqual(err.stageResults.length, 1);
      }
    });

    it('非 strict 模式应跳过失败阶段继续', async () => {
      const pipeline = new Pipeline({ strict: false });
      pipeline
        .addStage('ok1', asyncFn(d => [...d, 'ok1']))
        .addStage('fail', asyncFn(() => { throw new Error('boom'); }))
        .addStage('ok2', asyncFn(d => [...d, 'ok2']));

      const result = await pipeline.execute([]);
      assert.deepStrictEqual(result.data, ['ok1', 'ok2']);
      assert.strictEqual(result.metadata.stages[1].status, 'failed');
    });

    it('PipelineError 应携带阶段结果和部分数据', async () => {
      const pipeline = new Pipeline({ strict: true });
      pipeline
        .addStage('s1', asyncFn(d => [...d, 'done']))
        .addStage('s2', asyncFn(() => { throw new Error('fail'); }));

      try {
        await pipeline.execute([1, 2]);
      } catch (err) {
        assert.ok(err.stageResults);
        assert.ok(err.lastData);
        assert.deepStrictEqual(err.lastData, [1, 2, 'done']);
      }
    });
  });

  describe('重试机制', () => {
    it('阶段失败时应按配置重试', async () => {
      let attempts = 0;
      const pipeline = new Pipeline();
      pipeline.addStage('retry', asyncFn(() => {
        attempts++;
        if (attempts < 3) throw new Error(`attempt ${attempts}`);
        return 'success';
      }), { retryCount: 3, retryDelay: 10 });

      const result = await pipeline.run(null);
      assert.strictEqual(result, 'success');
      assert.strictEqual(attempts, 3);
    });

    it('重试耗尽后应抛错', async () => {
      const pipeline = new Pipeline();
      pipeline.addStage('fail', asyncFn(() => {
        throw new Error('always fails');
      }), { retryCount: 2, retryDelay: 10 });

      try {
        await pipeline.run(null);
        assert.fail('should have thrown');
      } catch (err) {
        assert.strictEqual(err.failedAttempt, 3); // initial + 2 retries
      }
    });
  });

  describe('超时机制', () => {
    it('阶段超时应抛错', async () => {
      const pipeline = new Pipeline();
      pipeline.addStage('slow', asyncFn(() =>
        new Promise(resolve => setTimeout(() => resolve('done'), 5000))
      ), { timeout: 50 });

      try {
        await pipeline.run(null);
        assert.fail('should have timed out');
      } catch (err) {
        // PipelineError wraps the original timeout error
        assert.ok(err.message.includes('timed out') ||
          (err.originalError && err.originalError.message.includes('timed out')));
      }
    });
  });

  describe('指标收集', () => {
    it('应记录管线运行指标', async () => {
      const pipeline = new Pipeline();
      pipeline.addStage('noop', asyncFn(d => d));
      await pipeline.execute([1]);
      await pipeline.execute([2]);

      const metrics = pipeline.getMetrics();
      assert.strictEqual(metrics.pipeline.totalRuns, 2);
      assert.strictEqual(metrics.stages[0].name, 'noop');
      assert.strictEqual(metrics.stages[0].calls, 2);
    });

    it('resetMetrics 应重置所有指标', async () => {
      const pipeline = new Pipeline();
      pipeline.addStage('noop', asyncFn(d => d));
      await pipeline.execute([1]);
      pipeline.resetMetrics();
      const metrics = pipeline.getMetrics();
      assert.strictEqual(metrics.pipeline.totalRuns, 0);
      assert.strictEqual(metrics.stages[0].calls, 0);
    });
  });

  describe('Context 传递', () => {
    it('context 应传递给所有阶段', async () => {
      const pipeline = new Pipeline({ context: { multiplier: 10 } });
      pipeline.addStage('multiply', asyncFn((d, ctx) => d.map(x => x * ctx.multiplier)));
      const result = await pipeline.run([1, 2, 3]);
      assert.deepStrictEqual(result, [10, 20, 30]);
    });
  });

  describe('Stage onComplete 回调', () => {
    it('每个阶段完成时应触发回调', async () => {
      const completed = [];
      const pipeline = new Pipeline({
        onStageComplete: async (name, data, elapsed) => {
          completed.push({ name, dataLength: Array.isArray(data) ? data.length : 0, elapsed });
        }
      });
      pipeline
        .addStage('s1', asyncFn(d => [...d, 1]))
        .addStage('s2', asyncFn(d => [...d, 2]));

      await pipeline.execute([0]);
      assert.strictEqual(completed.length, 2);
      assert.strictEqual(completed[0].name, 's1');
      assert.strictEqual(completed[1].name, 's2');
    });
  });
});

// ──────────────────────────────────────────────
// 测试：Transformers
// ──────────────────────────────────────────────

describe('Transformers', () => {

  describe('filter', () => {
    it('应过滤数组', () => {
      const result = Transformers.filter(x => x > 2)([1, 2, 3, 4, 5]);
      assert.deepStrictEqual(result, [3, 4, 5]);
    });
    it('非数组输入应抛错', () => {
      assert.throws(() => Transformers.filter(x => true)('not array'));
    });
  });

  describe('map', () => {
    it('应映射数组', () => {
      const result = Transformers.map(x => x * 2)([1, 2, 3]);
      assert.deepStrictEqual(result, [2, 4, 6]);
    });
    it('非数组输入应抛错', () => {
      assert.throws(() => Transformers.map(x => x)(42));
    });
  });

  describe('reduce', () => {
    it('应归约数组', () => {
      const result = Transformers.reduce((acc, x) => acc + x, 0)([1, 2, 3, 4]);
      assert.strictEqual(result, 10);
    });
    it('非数组输入应抛错', () => {
      assert.throws(() => Transformers.reduce((a, b) => a + b, 0)('nope'));
    });
  });

  describe('groupBy', () => {
    it('应按字段分组', () => {
      const data = [
        { dept: 'eng', name: 'A' },
        { dept: 'eng', name: 'B' },
        { dept: 'mkt', name: 'C' }
      ];
      const result = Transformers.groupBy('dept')(data);
      assert.strictEqual(result.eng.length, 2);
      assert.strictEqual(result.mkt.length, 1);
    });
    it('应按函数结果分组', () => {
      const data = [{ v: 1 }, { v: 2 }, { v: 3 }];
      const result = Transformers.groupBy(x => x.v % 2 === 0 ? 'even' : 'odd')(data);
      assert.strictEqual(result.odd.length, 2);
      assert.strictEqual(result.even.length, 1);
    });
  });

  describe('sort', () => {
    it('应按字段升序排序', () => {
      const data = [{ v: 3 }, { v: 1 }, { v: 2 }];
      const result = Transformers.sort('v', 'asc')(data);
      assert.deepStrictEqual(result.map(x => x.v), [1, 2, 3]);
    });
    it('应按字段降序排序', () => {
      const data = [{ v: 3 }, { v: 1 }, { v: 2 }];
      const result = Transformers.sort('v', 'desc')(data);
      assert.deepStrictEqual(result.map(x => x.v), [3, 2, 1]);
    });
    it('应支持自定义比较函数', () => {
      const data = ['b', 'aaa', 'cc'];
      const result = Transformers.sort((a, b) => a.length - b.length)(data);
      assert.deepStrictEqual(result, ['b', 'cc', 'aaa']);
    });
    it('不应修改原数组', () => {
      const data = [{ v: 3 }, { v: 1 }];
      const original = JSON.stringify(data);
      Transformers.sort('v')(data);
      assert.strictEqual(JSON.stringify(data), original);
    });
  });

  describe('dedup', () => {
    it('应按字段去重', () => {
      const data = [{ id: 1, v: 'a' }, { id: 1, v: 'b' }, { id: 2, v: 'c' }];
      const result = Transformers.dedup('id')(data);
      assert.strictEqual(result.length, 2);
      assert.strictEqual(result[0].v, 'a');
    });
    it('应支持函数去重', () => {
      const data = ['a', 'A', 'b', 'B'];
      const result = Transformers.dedup(x => x.toLowerCase())(data);
      assert.deepStrictEqual(result, ['a', 'b']);
    });
  });

  describe('flatten', () => {
    it('应扁平化嵌套数组', () => {
      const result = Transformers.flatten(2)([[1, [2, 3]], [4]]);
      assert.deepStrictEqual(result, [1, 2, 3, 4]);
    });
  });

  describe('paginate', () => {
    it('应返回指定页数据', () => {
      const data = [1, 2, 3, 4, 5, 6, 7];
      const page1 = Transformers.paginate(1, 3)(data);
      assert.deepStrictEqual(page1, [1, 2, 3]);
      const page2 = Transformers.paginate(2, 3)(data);
      assert.deepStrictEqual(page2, [4, 5, 6]);
    });
  });

  describe('limit', () => {
    it('应返回前 N 项', () => {
      const result = Transformers.limit(3)([1, 2, 3, 4, 5]);
      assert.deepStrictEqual(result, [1, 2, 3]);
    });
  });

  describe('pick', () => {
    it('应从对象中选择字段', () => {
      const result = Transformers.pick(['name', 'age'])({ name: 'A', age: 30, extra: 'x' });
      assert.deepStrictEqual(result, { name: 'A', age: 30 });
    });
    it('应处理数组', () => {
      const data = [{ name: 'A', age: 30 }, { name: 'B', age: 25 }];
      const result = Transformers.pick(['name'])(data);
      assert.deepStrictEqual(result, [{ name: 'A' }, { name: 'B' }]);
    });
  });

  describe('rename', () => {
    it('应重命名字段', () => {
      const result = Transformers.rename({ old_name: 'newName', age: 'years' })({ old_name: 'A', age: 30 });
      assert.deepStrictEqual(result, { newName: 'A', years: 30 });
    });
    it('应处理数组', () => {
      const data = [{ old_name: 'A' }, { old_name: 'B' }];
      const result = Transformers.rename({ old_name: 'name' })(data);
      assert.deepStrictEqual(result, [{ name: 'A' }, { name: 'B' }]);
    });
  });

  describe('merge', () => {
    it('应按键合并多个数组', () => {
      const base = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }];
      const extra = [{ id: 1, score: 90 }, { id: 2, score: 85 }];
      const result = Transformers.merge('id', extra)(base);
      assert.deepStrictEqual(result, [
        { id: 1, name: 'A', score: 90 },
        { id: 2, name: 'B', score: 85 }
      ]);
    });
  });
});

// ──────────────────────────────────────────────
// 测试：Validators
// ──────────────────────────────────────────────

describe('Validators', () => {

  describe('schema', () => {
    const schema = {
      name: { required: true, type: 'string', minLength: 1, maxLength: 50 },
      age: { required: true, type: 'number', min: 0, max: 150 },
      email: { type: 'string', pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
      role: { type: 'string', enum: ['admin', 'user', 'guest'] }
    };

    it('应通过有效数据', () => {
      const result = Validators.schema(schema)([
        { name: 'Alice', age: 30, email: 'alice@example.com', role: 'admin' }
      ]);
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.validItems, 1);
    });

    it('应捕获缺失的必填字段', () => {
      const result = Validators.schema(schema)([{ age: 30 }]);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors[0].errors.some(e => e.field === 'name' && e.rule === 'required'));
    });

    it('应捕获类型错误', () => {
      const result = Validators.schema(schema)([{ name: 'Alice', age: 'not a number' }]);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors[0].errors.some(e => e.field === 'age' && e.rule === 'type'));
    });

    it('应捕获范围错误', () => {
      const result = Validators.schema(schema)([{ name: 'Alice', age: 200 }]);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors[0].errors.some(e => e.field === 'age' && e.rule === 'max'));
    });

    it('应捕获模式不匹配', () => {
      const result = Validators.schema(schema)([{ name: 'Alice', age: 30, email: 'invalid' }]);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors[0].errors.some(e => e.field === 'email' && e.rule === 'pattern'));
    });

    it('应捕获枚举错误', () => {
      const result = Validators.schema(schema)([{ name: 'Alice', age: 30, role: 'superadmin' }]);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors[0].errors.some(e => e.field === 'role' && e.rule === 'enum'));
    });

    it('应支持自定义验证函数', () => {
      const customSchema = {
        password: {
          validate: (val) => val.length >= 8 ? true : 'Password must be at least 8 characters'
        }
      };
      const result = Validators.schema(customSchema)([{ password: 'short' }]);
      assert.strictEqual(result.valid, false);
      assert.strictEqual(result.errors[0].errors[0].message, 'Password must be at least 8 characters');
    });

    it('应报告所有无效项', () => {
      const result = Validators.schema(schema)([
        { name: 'Alice', age: 30 },
        { age: 30 },
        { name: '', age: 30 }
      ]);
      assert.strictEqual(result.totalItems, 3);
      assert.strictEqual(result.errors.length, 2);
    });

    it('应处理单个对象（非数组）', () => {
      const result = Validators.schema(schema)({ name: 'Alice', age: 30 });
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.totalItems, 1);
    });
  });
});

// ──────────────────────────────────────────────
// 测试：PipelineFactory
// ──────────────────────────────────────────────

describe('PipelineFactory', () => {

  describe('createCleaner', () => {
    it('应清洗和验证数据', async () => {
      const schema = {
        name: { required: true, type: 'string' },
        age: { type: 'number', min: 0 }
      };
      const pipeline = PipelineFactory.createCleaner(schema, { age: 0 });

      const result = await pipeline.execute([
        { name: '  Alice  ', age: 30 },
        { name: 'Bob' },
        { name: '' }
      ]);

      // name 应被 trim，缺失 age 应设为 0，空项应被移除
      const data = result.data;
      assert.strictEqual(data[0].name, 'Alice');
      assert.strictEqual(data[1].name, 'Bob');
      assert.strictEqual(data[1].age, 0);
    });
  });

  describe('createAnalyzer', () => {
    it('应按组聚合数据', async () => {
      const pipeline = PipelineFactory.createAnalyzer('dept', {
        avgSalary: { field: 'salary', fn: vals => Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) },
        maxSalary: { field: 'salary', fn: vals => Math.max(...vals) },
        minSalary: { field: 'salary', fn: vals => Math.min(...vals) }
      });

      const data = [
        { dept: 'eng', salary: 100 },
        { dept: 'eng', salary: 120 },
        { dept: 'mkt', salary: 80 },
        { dept: 'mkt', salary: 90 },
        { dept: 'mkt', salary: 70 }
      ];

      const result = await pipeline.run(data);
      const eng = result.find(r => r.dept === 'eng');
      const mkt = result.find(r => r.dept === 'mkt');

      assert.strictEqual(eng.count, 2);
      assert.strictEqual(eng.avgSalary, 110);
      assert.strictEqual(eng.maxSalary, 120);
      assert.strictEqual(mkt.count, 3);
      assert.strictEqual(mkt.avgSalary, 80);
    });
  });

  describe('createETL', () => {
    it('应创建并执行 ETL 管线', async () => {
      const extract = asyncFn(() => [
        { id: 1, name: 'A', value: '10' },
        { id: 2, name: 'B', value: '20' }
      ]);

      const load = asyncFn((d) => d);

      const pipeline = PipelineFactory.createETL(extract, [
        { name: 'parse', fn: asyncFn(d => d.map(x => ({ ...x, value: parseInt(x.value) }))) },
        { name: 'filter', fn: asyncFn(d => d.filter(x => x.value > 15)) }
      ], load);

      const result = await pipeline.run(null);
      assert.deepStrictEqual(result, [{ id: 2, name: 'B', value: 20 }]);
    });
  });
});

// ──────────────────────────────────────────────
// 测试：Stage
// ──────────────────────────────────────────────

describe('Stage', () => {
  it('默认应启用', () => {
    const stage = new Stage('test', asyncFn(d => d));
    assert.strictEqual(stage.enabled, true);
  });

  it('可通过选项禁用', () => {
    const stage = new Stage('test', asyncFn(d => d), { enabled: false });
    assert.strictEqual(stage.enabled, false);
  });

  it('getMetrics 应返回正确的指标', async () => {
    const stage = new Stage('test', asyncFn(d => d * 2));
    await stage.execute(5, {});
    await stage.execute(10, {});
    const metrics = stage.getMetrics();
    assert.strictEqual(metrics.calls, 2);
    assert.strictEqual(metrics.errors, 0);
  });

  it('禁用阶段执行应原样返回数据', async () => {
    const stage = new Stage('test', asyncFn(() => { throw new Error('should not run'); }), { enabled: false });
    const result = await stage.execute('original', {});
    assert.strictEqual(result, 'original');
  });
});

// ──────────────────────────────────────────────
// 运行
// ──────────────────────────────────────────────

// Simple test runner for environments without mocha
if (require.main === module) {
  console.log('Running data-pipeline tests...\n');

  const testSuites = [
    'Pipeline 核心引擎',
    'Transformers',
    'Validators',
    'PipelineFactory',
    'Stage'
  ];

  // We use the describe/it blocks above which are mocha-compatible
  // For direct execution, we provide a summary
  console.log('All test suites defined:');
  for (const suite of testSuites) {
    console.log(`  ✅ ${suite}`);
  }
  console.log('\nRun with: npx mocha tests/pipeline.test.js');
}
