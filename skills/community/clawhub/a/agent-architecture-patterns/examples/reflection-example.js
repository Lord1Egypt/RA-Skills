/**
 * Reflection Agent 示例 - 代码审查场景
 * 
 * 运行方式：node examples/reflection-example.js
 */

const { ReflectionAgent } = require('../src/agents/reflection-agent');

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
    if (prompt.includes('生成初始输出')) {
      return `function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}`;
    }
    
    if (prompt.includes('评估这个输出')) {
      if (this.callCount === 2) {
        return `反馈：

【问题】
1. 缺少边界条件处理：当 items 为空数组时，函数返回 0，但没有明确处理
2. 缺少错误处理：如果 items[i].price 或 items[i].quantity 不是数字，会导致计算错误
3. 缺少输入验证：没有检查 items 是否为数组
4. 代码风格：可以使用 reduce 方法使代码更简洁

【改进建议】
- 添加输入验证
- 添加边界条件处理
- 使用更现代 JavaScript 语法`;
      } else {
        return `反馈：

【评估】
代码质量已经很好，覆盖了主要问题。

【小建议】
- 可以添加 JSDoc 注释
- 可以考虑添加类型检查`;
      }
    }
    
    if (prompt.includes('根据反馈修改')) {
      if (this.callCount === 3) {
        return `/**
 * 计算商品总价
 * @param {Array} items - 商品数组
 * @returns {number} 总价
 */
function calculateTotal(items) {
  // 输入验证
  if (!Array.isArray(items) || items.length === 0) {
    return 0;
  }
  
  // 使用 reduce 方法计算
  return items.reduce((total, item) => {
    const price = Number(item.price) || 0;
    const quantity = Number(item.quantity) || 0;
    return total + price * quantity;
  }, 0);
}`;
      } else {
        return `/**
 * 计算商品总价（最终版本）
 * @param {Array} items - 商品数组
 * @returns {number} 总价
 */
function calculateTotal(items) {
  if (!Array.isArray(items) || items.length === 0) {
    return 0;
  }
  
  return items.reduce((total, item) => {
    const price = Number(item.price) || 0;
    const quantity = Number(item.quantity) || 0;
    return total + price * quantity;
  }, 0);
}`;
      }
    }
    
    return 'Generated output.';
  }
}

// ============================================
// 创建 Agent
// ============================================

const agent = new ReflectionAgent({
  maxIterations: 5,
  verbose: true,
  criteria: [
    '代码正确性：是否能正确运行，无 bug',
    '边界条件：是否处理了边界情况（空数组、null 等）',
    '错误处理：是否有输入验证和异常处理',
    '代码质量：是否遵循最佳实践，代码简洁',
    '可读性：是否有注释，命名是否清晰'
  ],
  llm: new MockLLM()
});

// ============================================
// 运行示例
// ============================================

async function runExample() {
  console.log('=== Reflection Agent 示例 - 代码审查 ===\n');
  
  const task = `审查并改进以下代码：

function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}`;

  console.log('📝 任务：代码审查与改进\n');
  console.log('原始代码：');
  console.log(task.split('\n').slice(2).join('\n'));
  console.log('\n' + '='.repeat(50) + '\n');
  
  const result = await agent.execute(task);
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ 最终代码：');
  console.log(result);
  console.log('='.repeat(50));
}

// ============================================
// 运行
// ============================================

runExample().catch(console.error);
