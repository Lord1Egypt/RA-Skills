# data-pipeline · 数据处理管线引擎

> 可组合的数据转换、验证和分析管线。像搭积木一样处理数据。

---

## 何时使用

当用户提到：数据清洗、数据转换、ETL、数据验证、数据分组、数据聚合、管道处理、批量数据处理、数组处理

## 快速开始

```javascript
const { Pipeline, Transformers, Validators, PipelineFactory } = require('data-pipeline/src/pipeline');

// 创建一个清洗管线
const pipeline = new Pipeline();
pipeline
  .addStage('filter', Transformers.filter(x => x.age >= 18))
  .addStage('pick', Transformers.pick(['name', 'email']))
  .addStage('sort', Transformers.sort('name', 'asc'));

const result = await pipeline.run(users);
```

## 核心 API

### Pipeline

```javascript
const pipeline = new Pipeline({ strict: true, context: { key: 'value' } });

// 添加阶段
pipeline.addStage(name, asyncFn, { retryCount: 0, retryDelay: 100, timeout: 30000 });
pipeline.addStages([{ name, fn, options }]);

// 阶段管理
pipeline.insertBefore(target, name, fn, options);
pipeline.insertAfter(target, name, fn, options);
pipeline.removeStage(name);
pipeline.toggleStage(name, enabled);

// 执行
const result = await pipeline.execute(data);  // 返回 { data, metadata }
const data = await pipeline.run(data);         // 只返回数据

// 指标
const metrics = pipeline.getMetrics();
pipeline.resetMetrics();
```

### 内置转换器

| 转换器 | 说明 | 示例 |
|--------|------|------|
| `filter(fn)` | 过滤 | `Transformers.filter(x => x.active)` |
| `map(fn)` | 映射 | `Transformers.map(x => x.name)` |
| `reduce(fn, init)` | 归约 | `Transformers.reduce((a,b) => a+b, 0)` |
| `groupBy(key)` | 分组 | `Transformers.groupBy('dept')` |
| `sort(key, order)` | 排序 | `Transformers.sort('age', 'desc')` |
| `dedup(key)` | 去重 | `Transformers.dedup('id')` |
| `flatten(depth)` | 扁平化 | `Transformers.flatten(2)` |
| `paginate(page, size)` | 分页 | `Transformers.paginate(1, 10)` |
| `limit(n)` | 限制 | `Transformers.limit(5)` |
| `pick(fields)` | 选择字段 | `Transformers.pick(['name', 'age'])` |
| `rename(map)` | 重命名 | `Transformers.rename({old: 'new'})` |
| `merge(key, ...sources)` | 合并 | `Transformers.merge('id', extras)` |

### 验证器

```javascript
const schema = {
  name: { required: true, type: 'string', minLength: 1 },
  age: { type: 'number', min: 0, max: 150 },
  email: { pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ },
  role: { enum: ['admin', 'user'] },
  password: { validate: (v) => v.length >= 8 ? true : 'Too short' }
};

const validator = Validators.schema(schema);
const result = validator(data);
// { valid: boolean, errors: [...], totalItems, validItems }
```

### 工厂函数

```javascript
// ETL 管线
const etl = PipelineFactory.createETL(extract, transforms, load);

// 数据清洗管线
const cleaner = PipelineFactory.createCleaner(schema, { defaultField: 'value' });

// 数据分析管线
const analyzer = PipelineFactory.createAnalyzer('groupKey', {
  avgVal: vals => vals.reduce((a,b) => a+b, 0) / vals.length,
  maxVal: vals => Math.max(...vals)
});
```

## 使用场景

1. **数据清洗**：验证 → 去重 → 填充默认值 → 修剪字符串
2. **ETL 流程**：提取 → 转换（map/filter/reduce）→ 加载
3. **数据分析**：分组 → 聚合 → 排序 → 分页
4. **数据验证**：批量验证对象数组，返回详细错误报告
5. **API 数据处理**：合并多个数据源 → 重命名字段 → 选择输出字段

## 错误处理

```javascript
try {
  const result = await pipeline.execute(data);
} catch (err) {
  if (err instanceof PipelineError) {
    console.log('Failed at:', err.failedStage);
    console.log('Partial data:', err.lastData);
    console.log('Stage results:', err.stageResults);
  }
}
```

## 性能指标

```javascript
const metrics = pipeline.getMetrics();
// {
//   pipeline: { totalRuns, totalErrors, avgTime },
//   stages: [{ name, calls, errors, avgTime }, ...]
// }
```
