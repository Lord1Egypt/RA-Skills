/**
 * Plan-and-Solve Agent 示例 - 项目开发场景
 * 
 * 运行方式：node examples/plan-and-solve-example.js
 */

const { PlanAndSolveAgent } = require('../src/agents/plan-and-solve-agent');

// ============================================
// Mock LLM
// ============================================

class MockLLM {
  constructor() {
    this.callCount = 0;
  }

  async generate(prompt) {
    this.callCount++;
    
    // 模拟 LLM 响应
    if (prompt.includes('请分析这个任务')) {
      return JSON.stringify({
        goal: '开发一个简单的待办事项 Web 应用',
        constraints: ['使用 JavaScript 技术栈', '开发时间<1 天', '支持基本 CRUD 操作'],
        successCriteria: ['可以添加待办', '可以删除待办', '可以标记完成', '界面简洁易用']
      });
    }
    
    if (prompt.includes('请制定详细的执行计划')) {
      return JSON.stringify({
        steps: [
          {
            id: 1,
            description: '设计数据模型',
            dependencies: [],
            expectedOutput: 'Todo 数据模型定义'
          },
          {
            id: 2,
            description: '创建 HTML 结构',
            dependencies: [],
            expectedOutput: 'HTML 文件'
          },
          {
            id: 3,
            description: '实现添加待办功能',
            dependencies: [1, 2],
            expectedOutput: '添加功能代码'
          },
          {
            id: 4,
            description: '实现删除待办功能',
            dependencies: [3],
            expectedOutput: '删除功能代码'
          },
          {
            id: 5,
            description: '实现标记完成功能',
            dependencies: [3],
            expectedOutput: '标记完成代码'
          },
          {
            id: 6,
            description: '添加 CSS 样式',
            dependencies: [2],
            expectedOutput: '样式文件'
          }
        ]
      });
    }
    
    if (prompt.includes('当前步骤：设计数据模型')) {
      return `// 数据模型
class Todo {
  constructor(id, title) {
    this.id = id;
    this.title = title;
    this.completed = false;
    this.createdAt = new Date();
  }
}`;
    }
    
    if (prompt.includes('当前步骤：创建 HTML 结构')) {
      return `<!DOCTYPE html>
<html>
<head>
  <title>Todo App</title>
</head>
<body>
  <h1>待办事项</h1>
  <input type="text" id="todo-input" placeholder="输入待办...">
  <button id="add-btn">添加</button>
  <ul id="todo-list"></ul>
</body>
</html>`;
    }
    
    if (prompt.includes('当前步骤：实现添加待办功能')) {
      return `// 添加待办
document.getElementById('add-btn').addEventListener('click', () => {
  const input = document.getElementById('todo-input');
  const title = input.value.trim();
  if (title) {
    const todo = new Todo(Date.now(), title);
    todos.push(todo);
    renderTodos();
    input.value = '';
  }
});`;
    }
    
    if (prompt.includes('当前步骤：实现删除待办功能')) {
      return `// 删除待办
function deleteTodo(id) {
  todos = todos.filter(todo => todo.id !== id);
  renderTodos();
}`;
    }
    
    if (prompt.includes('当前步骤：实现标记完成功能')) {
      return `// 标记完成
function toggleComplete(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    renderTodos();
  }
}`;
    }
    
    if (prompt.includes('当前步骤：添加 CSS 样式')) {
      return `/* 样式 */
body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }
#todo-input { padding: 10px; width: 70%; }
#add-btn { padding: 10px 20px; }
.todo-item { padding: 10px; border-bottom: 1px solid #eee; }
.todo-item.completed { text-decoration: line-through; color: #999; }
.delete-btn { color: red; cursor: pointer; }`;
    }
    
    if (prompt.includes('请整合所有执行结果')) {
      return `## 待办事项应用 - 开发完成

### 功能清单
✅ 添加待办事项
✅ 删除待办事项
✅ 标记完成状态
✅ 简洁界面

### 技术栈
- HTML5
- CSS3
- JavaScript (ES6+)

### 使用说明
1. 在输入框中输入待办内容
2. 点击"添加"按钮
3. 点击待办项可标记完成
4. 点击删除按钮可删除

### 代码结构
- index.html - HTML 结构
- style.css - 样式
- app.js - 应用逻辑

所有功能已完成并测试通过！`;
    }
    
    return 'Generated.';
  }
}

// ============================================
// 创建 Agent
// ============================================

const agent = new PlanAndSolveAgent({
  maxSteps: 20,
  verbose: true,
  llm: new MockLLM()
});

// ============================================
// 运行示例
// ============================================

async function runExample() {
  console.log('=== Plan-and-Solve Agent 示例 - 项目开发 ===\n');
  
  const task = '开发一个简单的待办事项 Web 应用，支持添加、删除、标记完成功能';
  
  console.log('📝 任务：项目开发\n');
  console.log('需求：' + task);
  console.log('\n' + '='.repeat(50) + '\n');
  
  const result = await agent.execute(task);
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ 项目完成：');
  console.log(result);
  console.log('='.repeat(50));
}

// ============================================
// 运行
// ============================================

runExample().catch(console.error);
