---
name: "debug-master"
version: "1.0.0"
description: "AI调试大师，集成7步调试法+根因分析+自动化测试+错误模式识别。触发词：'报错'、'出错了'、'debug'、'帮我看看'、'代码有问题'、'程序崩溃'、'修复bug'。相比原版debug-pro，新增AI根因分析、自动测试生成、错误模式库、跨语言调试。"
---

# Debug Master

AI调试大师，让Bug无处遁形。

## 核心升级

| 功能 | 原版 | 增强版 |
|------|------|--------|
| 调试方法 | 7步法 | **7步法 + AI根因分析** |
| 测试生成 | 手动 | **自动生成测试用例** |
| 错误模式 | 基础 | **智能错误模式库** |
| 跨语言 | 有限 | **15+主流语言全覆盖** |
| 修复建议 | 通用 | **上下文感知智能建议** |
| 预防机制 | 无 | **代码质量扫描预警** |

## 触发词

当用户说以下内容时激活：
- "报错"、"出错了"、"bug"
- "debug"、"帮我看看"
- "代码有问题"、"程序崩溃"
- "修复bug"、"这个错误"
- "为什么不行"、"怎么回事"

## 7步调试法 + AI增强

### Step 1: 复现问题

```
❌ 不要：直接猜测原因
✅ 要：精确复现错误

复现命令：
node --trace-errors app.js
python -v debug script.py
```

### Step 2: 捕获错误信息

```
错误类型识别：
├── SyntaxError → 语法错误（最容易修）
├── TypeError → 类型错误（检查变量类型）
├── ReferenceError → 引用错误（检查是否定义）
├── NetworkError → 网络错误（检查API/连接）
└── RuntimeError → 运行时错误（需要详细分析）
```

### Step 3: AI根因分析（新增）

```
分析错误不只是表象，要找根本原因

Why-Tree 分析法：
Why: 报错 "Cannot read property 'map' of undefined"
  → Why: data变量是undefined
    → Why: API返回数据为空
      → Why: 接口超时未处理
        → 根本原因：缺少空值判断和超时处理
```

### Step 4: 定位代码

```javascript
// 错误定位技巧
const debug = require('debug')('app:*');

// 添加断点日志
console.log('🔍 DEBUG: 变量值', { variable: value });

// 使用source map
source-map /path/to/bundle.js.map
```

### Step 5: 修复方案

```
修复优先级：
1. 立即止血（try-catch包裹）
2. 找到根本原因
3. 系统性修复（防止复发）
4. 添加测试用例
```

### Step 6: 验证修复

```bash
# 自动测试
npm test
# 集成测试
npm run test:integration
# 端到端测试
npm run test:e2e
```

### Step 7: 预防复发

```
添加到错误模式库
记录：错误类型 + 根本原因 + 修复方案 + 预防措施
```

## 支持语言

| 语言 | 调试命令 | 常见错误 |
|------|---------|---------|
| JavaScript | `node --inspect` | TypeError, ReferenceError |
| TypeScript | `ts-node` | 类型错误 |
| Python | `pdb` / `ipdb` | IndentationError, ImportError |
| Java | jdb / IntelliJ | NullPointerException |
| Go | `delve` | nil pointer, race condition |
| Rust | `rust-gdb` / `rust-lldb` | borrow checker |
| C/C++ | gdb / lldb | segmentation fault |
| Ruby | byebug | NoMethodError |
| PHP | Xdebug | Fatal Error |
| SQL | EXPLAIN | 语法错误 |

## 错误模式库

### 模式1: JavaScript类型错误

```
症状: "Cannot read property 'x' of undefined"
原因: 访问undefined/null的属性
修复:
  // ❌ 错误
  data.items.map(x => x.name)

  // ✅ 正确
  data?.items?.map(x => x.name) || []
```

### 模式2: Python导入错误

```
症状: "ModuleNotFoundError: No module named 'xxx'"
原因: 模块未安装或路径错误
修复:
  pip install xxx
  # 或检查 PYTHONPATH
```

### 模式3: 异步错误

```
症状: "UnhandledPromiseRejection"
原因: Promise错误未被捕获
修复:
  // 添加错误处理
  promise.catch(err => console.error(err))
  // 或使用 try-await
  try { await asyncFn() } catch (err) {}
```

### 模式4: 并发竞争

```
症状: 数据不一致 / 状态错乱
原因: 多线程同时修改同一数据
修复:
  // 使用锁或原子操作
  // Go: sync.Mutex
  // Python: threading.Lock
  // JS: async-await + 状态管理
```

## 自动测试生成

### 根据错误生成测试用例

```
当修复一个bug时，自动生成防止复发的测试：

原始错误：
TypeError: Cannot read property 'name' of undefined

自动生成测试：
test('should handle undefined user gracefully', () => {
  const result = getUserName(undefined);
  expect(result).toBe('Guest');
});
```

## 调试工具箱

```javascript
// 通用调试工具
const debug = {
  log: (...args) => console.log('[DEBUG]', ...args),
  error: (...args) => console.error('[ERROR]', ...args),
  warn: (...args) => console.warn('[WARN]', ...args),
};

// 检查变量
const inspect = (obj) => JSON.stringify(obj, null, 2);

// 性能分析
console.time('operation');
// ... operation ...
console.timeEnd('operation');
```

## 常见场景解决方案

### 场景1: API调用失败

```
排查步骤：
1. 检查网络请求（F12 Network）
2. 查看请求头/参数
3. 检查CORS配置
4. 验证API Key/Token
5. 测试API直接访问

常见修复：
- 添加超时处理
- 添加重试逻辑
- 添加错误边界
```

### 场景2: 内存泄漏

```
排查工具：
- Chrome DevTools Memory
- Node: node --inspect

特征：
- 内存持续增长
- 页面越来越卡
- 定时任务越来越慢

常见原因：
- 事件监听未移除
- 全局变量累积
- 闭包引用未释放
```

### 场景3: 性能问题

```
排查工具：
- Chrome DevTools Performance
- Lighthouse
- Web Vitals

优化方向：
- 减少重排重绘
- 代码分割懒加载
- 优化数据库查询
- 使用缓存
```

## 调试报告模板

```markdown
# Bug调试报告

## 问题描述
[简短描述]

## 错误信息
```
[粘贴错误日志]
```

## 复现步骤
1. [步骤1]
2. [步骤2]

## 根因分析
**直接原因**: [表象]
**根本原因**: [深层原因]

## 修复方案
```[代码]
[修复代码]
```

## 预防措施
- [ ] 添加测试用例
- [ ] 增加空值判断
- [ ] 添加日志监控

## 验证结果
[测试通过截图/日志]
```
