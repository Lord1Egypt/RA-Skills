/**
 * Manager-Worker Agent 完整示例 - 多 Agent 代码审查系统
 * 
 * 运行方式：node examples/manager-worker-full-example.js
 */

const { ManagerAgent, WorkerAgent } = require('../src/agents/manager-worker-agent');

// ============================================
// Mock LLM
// ============================================

class MockLLM {
  constructor() {
    this.callCount = 0;
  }

  async generate(prompt) {
    this.callCount++;
    
    // 任务分解
    if (prompt.includes('将以下任务分解为独立的子任务')) {
      return JSON.stringify([
        {
          id: 'task-1',
          description: '语法和格式检查',
          requiredSkills: ['javascript', 'eslint']
        },
        {
          id: 'task-2',
          description: '代码逻辑审查',
          requiredSkills: ['javascript', 'code-review']
        },
        {
          id: 'task-3',
          description: '安全性检查',
          requiredSkills: ['security', 'javascript']
        },
        {
          id: 'task-4',
          description: '性能优化建议',
          requiredSkills: ['performance', 'javascript']
        }
      ]);
    }
    
    // 整合结果
    if (prompt.includes('请整合所有成功结果')) {
      return `## 代码审查报告

### 审查概览
- 审查文件：user-service.js
- 审查维度：语法、逻辑、安全、性能
- 发现问题：5 个
- 建议改进：3 处

---

### 1. 语法和格式检查 ✅

**通过项**：
- 代码格式符合 ESLint 标准
- 命名规范清晰
- 注释完整

**问题**：
- 第 15 行：缺少 JSDoc 注释
- 第 28 行：函数过长（建议拆分为小函数）

---

### 2. 代码逻辑审查 ⚠️

**问题**：
1. **空值处理不当**（第 23 行）
   ```javascript
   // 问题代码
   const user = users.find(u => u.id === userId);
   return user.name; // 可能抛出 TypeError
   
   // 建议修改
   const user = users.find(u => u.id === userId);
   if (!user) throw new Error('User not found');
   return user.name;
   ```

2. **重复代码**（第 35-42 行和第 58-65 行）
   - 建议提取为公共函数

---

### 3. 安全性检查 ❌

**严重问题**：

1. **SQL 注入风险**（第 45 行）
   ```javascript
   // 危险代码
   const query = \`SELECT * FROM users WHERE id = \${userId}\`;
   
   // 安全做法
   const query = 'SELECT * FROM users WHERE id = ?';
   db.execute(query, [userId]);
   ```

2. **敏感信息泄露**（第 12 行）
   - 不要在日志中打印用户密码

---

### 4. 性能优化建议 💡

**优化点**：

1. **避免重复查询**（第 50 行）
   - 添加缓存机制
   - 使用 DataLoader

2. **减少循环嵌套**（第 70 行）
   - 当前：O(n²)
   - 优化：使用 Map，O(n)

---

### 总结

**优先级**：
- 🔴 高：修复 SQL 注入漏洞
- 🟡 中：添加空值处理
- 🟢 低：代码重构和优化

**总体评分**：6/10

建议优先修复安全问题，然后改进代码质量。`;
    }
    
    return 'Generated.';
  }
}

// ============================================
// 创建 Worker Agents
// ============================================

const syntaxWorker = new WorkerAgent('syntax-checker', ['javascript', 'eslint'], {
  codeReview: true
});

const logicWorker = new WorkerAgent('logic-reviewer', ['javascript', 'code-review'], {
  codeReview: true
});

const securityWorker = new WorkerAgent('security-scanner', ['security', 'javascript'], {
  codeReview: true
});

const performanceWorker = new WorkerAgent('performance-analyzer', ['performance', 'javascript'], {
  codeReview: true
});

// Mock LLM for workers
[syntaxWorker, logicWorker, securityWorker, performanceWorker].forEach(worker => {
  worker.llm = new MockLLM();
});

// ============================================
// Mock Worker 执行
// ============================================

syntaxWorker.execute = async (subtask) => {
  return `语法检查完成：
- 格式：✅ 符合规范
- 命名：✅ 清晰
- 注释：⚠️ 部分缺失
- 问题：2 个`;
};

logicWorker.execute = async (subtask) => {
  return `逻辑审查完成：
- 空值处理：❌ 缺失
- 错误处理：⚠️ 不完整
- 代码复用：❌ 有重复
- 问题：2 个`;
};

securityWorker.execute = async (subtask) => {
  return `安全检查完成：
- SQL 注入：❌ 发现风险
- XSS 防护：✅ 良好
- 敏感信息：❌ 日志泄露
- 问题：2 个严重`;
};

performanceWorker.execute = async (subtask) => {
  return `性能分析完成：
- 时间复杂度：⚠️ 有优化空间
- 数据库查询：❌ 重复查询
- 缓存使用：❌ 未使用
- 建议：3 处优化`;
};

// ============================================
// 创建 Manager Agent
// ============================================

const manager = new ManagerAgent(
  [syntaxWorker, logicWorker, securityWorker, performanceWorker],
  {
    maxRetries: 3,
    timeout: 30000,
    verbose: true,
    llm: new MockLLM()
  }
);

// ============================================
// 运行示例
// ============================================

async function runExample() {
  console.log('=== Manager-Worker Agent 示例 - 多 Agent 代码审查系统 ===\n');
  
  const codeToReview = `// user-service.js
function getUser(userId) {
  const users = db.query('SELECT * FROM users');
  const user = users.find(u => u.id === userId);
  return user.name;
}

function createUser(data) {
  const query = \`INSERT INTO users (name, email, password) 
                 VALUES ('\${data.name}', '\${data.email}', '\${data.password}')\`;
  db.execute(query);
  console.log('Created user:', data); // 问题：打印密码
}

// ... 更多代码 ...`;

  console.log('📝 任务：多 Agent 代码审查\n');
  console.log('待审查代码：');
  console.log(codeToReview);
  console.log('\n' + '='.repeat(50) + '\n');
  console.log('🤖 启动 4 个专家 Agent：');
  console.log('  - syntax-checker: 语法和格式检查');
  console.log('  - logic-reviewer: 代码逻辑审查');
  console.log('  - security-scanner: 安全性检查');
  console.log('  - performance-analyzer: 性能优化建议');
  console.log('\n' + '='.repeat(50) + '\n');
  
  const task = '审查以下代码，从语法、逻辑、安全、性能四个维度提供详细报告';
  
  const result = await manager.coordinate(task + '\n\n' + codeToReview);
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ 审查完成：');
  console.log(result);
  console.log('='.repeat(50));
}

// ============================================
// 运行
// ============================================

runExample().catch(console.error);
